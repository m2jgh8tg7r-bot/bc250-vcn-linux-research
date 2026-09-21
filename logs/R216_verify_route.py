"""Saved-image routing audit and queue-backed abstract ordering witness. No hardware.
Requires the unchanged R165/R169 saved model artifacts under research_root.
"""
import argparse,hashlib,importlib.util,json,re,struct
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('image',type=Path);p.add_argument('instructions',type=Path);p.add_argument('research_root',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
b=a.image.read_bytes();assert hashlib.sha256(b).hexdigest()=='8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675'
ins={}
for line in a.instructions.read_text().splitlines()[1:]:
 addr,h,text,*extras=line.split('\t');pc=int(addr,16);raw=bytes.fromhex(h);assert b[pc:pc+len(raw)]==raw;ins[pc]=text
u=lambda off:struct.unpack_from('<I',b,off)[0]
entries=[]
for ch in range(8):
 table=u(u(0xb88)+ch*4+0x1fc);count=struct.unpack_from('<H',b,u(0xb84)+ch*2+0xfc)[0];assert table+count*8<=len(b)
 for msg in range(count):
  off=table+msg*8
  if u(off)==0x2e6c8:
   entries.append(dict(channel=ch,message=hex(msg),table=hex(table),handler=hex(u(off)),metadata=hex(u(off+4)),priority=b[off+4],permission_mask=b[off+5]&127,direct_call=bool(b[off+5]&128)))
assert len(entries)==2 and [x['channel'] for x in entries]==[3,4]
assert all(x['priority']==6 and x['permission_mask']==0 and not x['direct_call'] for x in entries)
assert ins[0xf4d]=='call8 0x000026b4' and ins[0x1041]=='call8 0x000026b4'
assert u(0xba4)==0x1b154 and ins[0x1037]=='movi.n a11,0x4'
assert ins[0x202f]=='wsr a3,PS'
assert ins[0x1e96]=='callx8 a12' and ins[0x1e99]=='call8 0x00002040'
for lo,hi in [(0xebc,0xf74),(0x1e78,0x1e9e),(0x1fc4,0x203e),(0x26b4,0x27f7)]:
 assert not any('0x00002268' in text or '0x0000231c' in text for pc,text in ins.items() if lo<=pc<=hi)
root=a.research_root
spec=importlib.util.spec_from_file_location('consumer',root/'r169-queue-consumer/check_sequences.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def queue_order(arrivals):
 memory,_=mod.q.init([]);c=mod.CPU(memory)
 for callback,priority in arrivals:
  assert c.run(priority,0,0,callback,4 if callback==0x2e6c8 else 0)==0
  assert c.context_calls==0 # context blocked in synthetic fixture, no dispatch callee assumed
 out=[]
 while c.pop(7):out.append(c.load(mod.OUT,4))
 return out

def apply(state):
 if state['A']!=state['B']:state['old']=state['target'];state['A']=state['B']

def run_callbacks(order):
 s=dict(A=1,B=0,target=0,old=0);trace=[]
 for callback in order:
  if callback==0x2e6c8:s['target']=1250
  else:assert callback==0x1b154
  apply(s);trace.append(dict(callback=hex(callback),state=dict(s)))
 return s,trace
witnesses=[]
for arrivals in [[(0x2e6c8,6),(0x1b154,4)],[(0x1b154,4),(0x2e6c8,6)]]:
 order=queue_order(arrivals);assert order==[0x1b154,0x2e6c8]
 state,trace=run_callbacks(order);assert state==dict(A=0,B=0,target=1250,old=0)
 witnesses.append(dict(arrival_callbacks=[hex(x[0]) for x in arrivals],dequeue_callbacks=[hex(x) for x in order],trace=trace))
control,control_trace=run_callbacks(queue_order([(0x2e6c8,6)]));assert control==dict(A=0,B=0,target=1250,old=1250)
# A counterexample to any claim that enqueue order alone fixes callback order.
fifo,_=run_callbacks([0x2e6c8,0x1b154]);assert fifo['old']==1250
paths=['r165-r1-queue-model/check_queue.py','r164-r1-queue-flow/queue-instructions.json','r169-queue-consumer/check_sequences.py','r169-queue-consumer/consumer-functions.txt']
result=dict(passed=True,entries=entries,walker_priority=4,setter_priority=6,verified_instruction_count=len(ins),
 queue_witnesses=witnesses,without_walker_control=control,assumed_fifo_control=fifo,
 model_dependencies=[dict(path=x,sha256=hashlib.sha256((root/x).read_bytes()).hexdigest()) for x in paths],
 hardware_access=False,scope='Actual bounded saved queue interpreters; abstract target/old/selector callback model; synthetic arrivals, context inhibition, threshold7, pending availability and callback registration. No hardware code conversion or real timer interleaving.')
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
