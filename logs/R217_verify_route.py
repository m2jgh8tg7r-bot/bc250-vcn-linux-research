"""Offline evidence checks; pass extracted type-2 body as the first argument.
This checks bytes and relative dispatch arithmetic, not live firmware behavior.
"""
from pathlib import Path
import hashlib,json,struct,sys
root=Path(__file__).resolve().parent
b=Path(sys.argv[1] if len(sys.argv)>1 else root/'tos-body.bin').read_bytes()
assert len(b)==0x14150
assert hashlib.sha256(b).hexdigest()=='19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d'
p=root/'instructions.txt'
if not p.exists():p=root/'R217_instructions.txt'
ins={}
for line in p.read_text().splitlines():
 if not line.startswith('INS='):continue
 addr,hx,asm=line[4:].split(' ',2);off=int(addr,16)-0x200000;raw=bytes.fromhex(hx)
 assert b[off:off+len(raw)]==raw,(addr,hx)
 ins[off]=asm
assert 0x10582+2*b[0x10582+6]==0x10616
assert 0x4f62+2*b[0x4f62+2]==0x4f74
assert 0x45e4+struct.unpack_from('<I',b,0x45e4+4*(0x74-0x51))[0]==0x4c82
checks={0x10624:'bl 0x0020f3ca',0x10628:'mov r7,r0',0xf404:'svc 0xf2',0x4f78:'b.w 0x00201ab8',0x3806:'strb r3,[r1,r2]',0x4c88:'bl 0x002037ec',0x121f6:'svc 0x74'}
for off,asm in checks.items():assert ins[off]==asm,(hex(off),ins.get(off),asm)
for off,value in [(0x1c80,0x8430),(0x380c,0x8430),(0x1c84,0x6054),(0x173c,0x69b0)]:assert struct.unpack_from('<I',b,off)[0]==value
out=dict(evidence='PROVEN_STATICALLY',body_sha256=hashlib.sha256(b).hexdigest(),instruction_byte_matches=len(ins),command6_target='body+0x10616',svc_f2_target='body+0x4f74 -> body+0x1ab8',svc_74_target='body+0x4c82 -> body+0x37ec',service_map_literal='0x8430',service_map_writer='body+0x3806',runtime_identity='UNPROVEN',runtime_service_registration='UNPROVEN',rejection_cause='UNPROVEN',hardware_access=False)
print(json.dumps(out,indent=2))
