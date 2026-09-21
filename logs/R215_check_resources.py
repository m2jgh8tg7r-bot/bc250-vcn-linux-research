"""Bounded instruction-text execution on synthetic RAM. No devices or firmware execution.
Context switching and fatal handling are stopping boundaries, not emulated callees.
"""
import argparse, copy, hashlib, json, random, re, struct
from pathlib import Path
MASK=0xffffffff
CURRENT=0xaec0; GLOBAL=0xaee8; TABLE=0xaec8; STATES=0x15000
TASKS=[0x16000+0x80*i for i in range(5)]

class CPU:
 def __init__(self,ins):
  self.ins=ins;self.mem=bytearray(0x20000);self.r=[0]*16;self.r[1]=0x18000
  self.ps=0x123400;self.trace=[];self.fatal=None
 def load(self,a,n):
  assert 0<=a<=len(self.mem)-n
  return int.from_bytes(self.mem[a:a+n],'little')
 def store(self,a,n,v):
  assert 0<=a<=len(self.mem)-n
  self.mem[a:a+n]=(v&((1<<(8*n))-1)).to_bytes(n,'little')
 def val(self,x):return self.r[int(x[1:])] if re.fullmatch(r'a\d+',x) else int(x,0)
 def put(self,x,v):self.r[int(x[1:])]=v&MASK
 def run(self,start,arg):
  self.r[2]=arg;pc=start;loop_begin=loop_end=None;left=0
  for _ in range(5000):
   size,text,scalars=self.ins[pc];op,_,tail=text.partition(' ');a=[x for x in tail.split(',') if x];v=self.val
   nxt=pc+size;taken=False;self.trace.append(pc)
   if op in ('entry','memw','nop.n'):pass
   elif op in ('movi','movi.n'):self.put(a[0],scalars[1])
   elif op in ('mov','mov.n'):self.put(a[0],v(a[1]))
   elif op in ('addi','addi.n'):self.put(a[0],v(a[1])+scalars[2])
   elif op in ('add','add.n'):self.put(a[0],v(a[1])+v(a[2]))
   elif op in ('addx2','addx4'):self.put(a[0],v(a[1])*(2 if op=='addx2' else 4)+v(a[2]))
   elif op in ('and','or','xor'):
    x,y=v(a[1]),v(a[2]);self.put(a[0],x&y if op=='and' else x|y if op=='or' else x^y)
   elif op=='extui':self.put(a[0],(v(a[1])>>v(a[2]))&((1<<v(a[3]))-1))
   elif op=='l32r':self.put(a[0],self.load(v(a[1]),4))
   elif op in ('l8ui','l32i','l32i.n'):self.put(a[0],self.load(v(a[1])+v(a[2]),1 if op=='l8ui' else 4))
   elif op in ('s8i','s32i','s32i.n'):self.store(v(a[1])+v(a[2]),1 if op=='s8i' else 4,v(a[0]))
   elif op=='rsil':self.put(a[0],self.ps);self.ps=(self.ps&~15)|v(a[1])
   elif op=='wsr':
    if a[1]=='PS':self.ps=v(a[0])
    else:assert a[1]=='MISC1'
   elif op in ('bnone','bany','ball'):
    dest,x,y=map(v,a);take=(x&y)==0 if op=='bnone' else (x&y)!=0 if op=='bany' else (x&y)==y
    if take:nxt=dest;taken=True
   elif op in ('beqz.n','beqz','bnez','bnez.n','bgeu','bnei'):
    if op.startswith('beqz'):take=v(a[0])==0
    elif op.startswith('bnez'):take=v(a[0])!=0
    elif op=='bgeu':take=v(a[0])>=v(a[1])
    else:take=v(a[0])!=v(a[1])
    if take:nxt=v(a[-1]);taken=True
   elif op=='loopgtz':
    n=v(a[0]);n=n-2**32 if n&0x80000000 else n;loop_begin=pc+size;loop_end=v(a[1]);left=n-1
    if n<=0:nxt=loop_end;taken=True
   elif op=='call8':
    target=v(a[0])
    if target==0x1b78:self.fatal=list(self.r[10:14]);return 'fatal'
    assert target==0x1f74
    # Separately execute the saved state setter with its own register window.
    outer=self.r;self.r=[0]*16;self.r[1]=0x18100;self.r[3]=outer[11]
    result=self.run(target,outer[10]);assert result=='returned';self.r=outer
   elif op=='call0':assert v(a[0])==0x2de8;return 'context_boundary'
   elif op=='retw.n':return 'returned'
   else:raise AssertionError((hex(pc),text))
   if not taken and nxt==loop_end and left>0:nxt=loop_begin;left-=1
   pc=nxt
  raise AssertionError('instruction budget')

def read_instructions(path,image):
 raw=image.read_bytes();assert hashlib.sha256(raw).hexdigest()=='8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675'
 ins={}
 for line in path.read_text().splitlines()[1:]:
  addr,hexb,text,*extras=line.split('\t');pc=int(addr,16);b=bytes.fromhex(hexb);assert raw[pc:pc+len(b)]==b
  scalars={int(m[1]):int(m[2]) for x in extras if (m:=re.fullmatch(r'op(\d+)=(-?\d+):\d+:\d+',x))}
  ins[pc]=(len(b),text,scalars)
 assert [struct.unpack_from('<I',raw,x)[0] for x in [0xd00,0xd20,0xcfc]]==[0xae80,0xae84,0xaec0]
 assert ins[0x2347][2][1]==-1
 return ins

def fixture(ins,tasks,global_mask,current=0,ps=0x123400):
 c=CPU(ins);c.ps=ps
 for off,value in [(0xd00,0xae80),(0xd20,0xae84),(0xcfc,0xaec0),(0xcf8,0x14ff0),(0xb68,0x14000),(0x14ff0,STATES),(CURRENT,TASKS[current]),(GLOBAL,global_mask)]:c.store(off,4,value)
 for i,t in enumerate(tasks):
  base=TASKS[i];c.store(TABLE+i*4,4,base);c.store(base+0x14,4,i)
  for off,key,n in [(0x28,'state',1),(0x29,'priority',1),(0x2a,'base_priority',1),(0x2c,'claim',4),(0x30,'wait',4)]:c.store(base+off,n,t[key])
  c.store(STATES+i,1,t['state'])
 return c

def read_tasks(c):
 return [dict(state=c.load(b+0x28,1),priority=c.load(b+0x29,1),base_priority=c.load(b+0x2a,1),claim=c.load(b+0x2c,4),wait=c.load(b+0x30,4)) for b in TASKS]

def task(state=0,priority=7,claim=0,wait=0):return dict(state=state,priority=priority,base_priority=priority,claim=claim,wait=wait)

def expected_acquire(tasks,g,mask):
 ts=copy.deepcopy(tasks);cur=ts[0]
 if cur['claim']&mask:return 'fatal',ts,g
 cur['claim']|=mask
 if not(g&mask):return 'returned',ts,g|mask
 cur['state']=2;cur['wait']=mask
 for t in ts:
  if t['state'] and t['claim']&cur['claim']:t['priority']=min(t['priority'],cur['priority'])
 return 'context_boundary',ts,g

def expected_release(tasks,g,mask):
 ts=copy.deepcopy(tasks);cur=ts[0]
 if cur['claim']&mask!=mask:return 'fatal',ts,g
 cur['claim']&=~mask;g&=~mask;switch=False
 while True:
  eligible=[i for i,t in enumerate(ts) if t['state']==2 and not(t['wait']&g)]
  if not eligible:break
  i=min(eligible,key=lambda i:(ts[i]['priority'],i));t=ts[i]
  g|=t['claim'];t['state']=1;t['wait']=0
  switch|=t['priority']<=cur['priority']
 cur['priority']=cur['base_priority']
 if cur['claim']:
  peers=[t['priority'] for t in ts if t['state']==2 and t['claim']&cur['claim']]
  if peers:cur['priority']=min(cur['priority'],*peers)
 return ('context_boundary' if switch else 'returned'),ts,g

def check(ins,operation,tasks,g,mask,ps=0x123400):
 c=fixture(ins,tasks,g,ps=ps);ref=expected_acquire if operation=='acquire' else expected_release
 result,expected,eg=ref(tasks,g,mask);got=c.run(0x2268 if operation=='acquire' else 0x231c,mask)
 assert got==result,(operation,tasks,g,mask,result,got)
 assert read_tasks(c)==expected,(operation,tasks,g,mask,expected,read_tasks(c))
 assert c.load(GLOBAL,4)==eg
 if result!='fatal':assert c.ps==ps,(hex(c.ps),hex(ps))
 else:assert c.fatal[:3]==[1,3 if operation=='acquire' else 10,mask]
 for i,t in enumerate(expected):assert c.load(STATES+i,1)==t['state']
 return result,c

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('image',type=Path);p.add_argument('instructions',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
 ins=read_instructions(a.instructions,a.image);rng=random.Random(215);counts={k:{'returned':0,'context_boundary':0,'fatal':0} for k in ['acquire','release']};cases=0
 masks=[0,1,2,3,0x40000,0x40001,0x80000000,0xffffffff]
 for n in range(2048):
  # Independent owned bits plus pending claims; global tracks granted owners only.
  owned=[0]*5
  for bit in [0,1,2,18,31]:
   owner=rng.randrange(6)
   if owner<5:owned[owner]|=1<<bit
  g=0
  for bits in owned:g|=bits
  ts=[task(1,rng.randrange(8),owned[0])]
  for i in range(1,5):
   wait=rng.choice(masks)&~owned[i]&MASK
   state=2 if wait and wait&g else 1 if owned[i] else 0
   ts.append(task(state,rng.randrange(8),owned[i]|(wait if state==2 else 0),wait if state==2 else 0))
  for operation in ['acquire','release']:
   m=rng.choice(masks) if n%2 else (rng.choice(masks)&ts[0]['claim'] if operation=='release' else rng.choice(masks)&~ts[0]['claim']&MASK)
   result,_=check(ins,operation,ts,g,m,ps=0x123400|(n%16));counts[operation][result]+=1;cases+=1
 # Exact disputed masks: another task holding 1 does not block acquiring 0x40000.
 ts=[task(1,4),task(1,3,1),task(),task(),task()]
 result,c=check(ins,'acquire',ts,1,0x40000);assert result=='returned' and c.ps==0x123400
 witnesses=[dict(scenario='other_task_holds_1_request_0x40000',result=result,global_mask=hex(c.load(GLOBAL,4)),ps_restored=True)]
 result,c=check(ins,'acquire',ts,1,1);assert result=='context_boundary';witnesses.append(dict(scenario='other_task_holds_1_request_1',result=result,ps_restored=True))
 # Completion guard is not a resource release: it aborts when claims remain.
 c=fixture(ins,[task(1,4,0x40000),task(),task(),task(),task()],0x40000);assert c.run(0x2040,0)=='fatal' and c.fatal[:3]==[1,1,0]
 out=dict(passed=True,cases=cases,outcomes=counts,directed_witnesses=witnesses,completion_claim_guard=True,
          aliases=dict(current_task='0xaec0',global_resource_mask='0xaee8'),
          instruction_bytes_verified=len(ins),movi_n_ff_signed_value=-1,hardware_access=False,
          scope='Sequential synthetic RAM; supplied callee register windows; state setter interpreted; stop before context switch/fatal callee; no callback timing, concurrency or physical hardware semantics.')
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
