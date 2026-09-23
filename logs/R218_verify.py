"""Verify selected static evidence against an independently supplied saved TOS body."""
from pathlib import Path
import hashlib,struct,json,sys
r=Path(__file__).resolve().parent
b=Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(b).hexdigest()=='19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d'
p=r/'R218_instructions.txt'
if not p.exists():p=r/'instructions.txt'
ins={}
for line in p.read_text().splitlines():
 if not line.startswith('INS='):continue
 addr,hx,asm=line[4:].split(' ',2);o=int(addr,16)-0x200000;v=bytes.fromhex(hx)
 assert b[o:o+len(v)]==v,(addr,hx)
 ins[o]=asm
for o,s in {0x1230c:'bl 0x00211a04',0x1230a:'str r4,[sp,#0x0]',0x11b6a:'movs r5,#0x1',0x11cc0:'svc 0x64',0x121f6:'svc 0x74',0x11652:'svc 0x73',0x116d4:'svc 0x80',0x50de:'str r1,[r2,#0x0]',0x120ca:'bne 0x002121be'}.items():assert ins[o]==s,(hex(o),ins.get(o))
u32=lambda o:struct.unpack_from('<I',b,o)[0]
for n,target in [(0x64,0x49ba),(0x73,0x4c7e),(0x80,0x4b6e)]:assert 0x45e4+u32(0x45e4+4*(n-0x51))==target
for off,v in [(0xe040,0x203609),(0x11770,0x2042c5),(0x12468,0x2060e8),(0x11e14,0x2060c8),(0x4f1c,0x601c),(0x510c,0x601c),(0x5104,0x6030),(0x50fc,0x3230000)]:assert u32(off)==v
assert (u32(0xe040)&~1)-0x200000+0xe000==0x11608
assert (u32(0x11770)&~1)-0x200000+0xe000==0x122c4
assert b[0xfe8c:0xfe9c]==b'amd.dr.driverID\0'
assert 13*4+0x13c==0x170
print(json.dumps(dict(body_sha256=hashlib.sha256(b).hexdigest(),instruction_byte_matches=len(ins),static_checks='PASS',user_section_mapping='STRONGLY_SUPPORTED',live_route='UNPROVEN',service_image_bytes='UNPROVEN',rejection_producer='UNPROVEN',hardware_access=False),indent=2))
