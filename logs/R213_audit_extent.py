"""Inspect saved regular files only; print structural metadata, never ROM contents."""
import argparse, hashlib, json, stat, struct
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('analysis'); p.add_argument('rom')
a=p.parse_args()
paths=[Path(x).resolve() for x in (a.analysis,a.rom)]
assert all(stat.S_ISREG(x.stat().st_mode) and not str(x).startswith(('/dev/','/sys/','/proc/')) for x in paths)
f,b=[x.read_bytes() for x in paths]
assert hashlib.sha256(f).hexdigest()=='8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675'
s=b.find(f); assert s==0x8ff100 and b.find(f,s+1)==-1
h=b[s-0x100:s]; u=lambda o:struct.unpack_from('<I',h,o)[0]
assert h[0x10:0x14]==b'$PS1'
fields={name:u(off) for name,off in [('size_signed',0x14),('encrypted',0x18),('signed',0x30),('signature_type',0x34),('compressed',0x48),('size_uncompressed',0x50),('load_addr',0x68),('rom_size',0x6c)]}
assert fields==dict(size_signed=0x40000,encrypted=0,signed=1,signature_type=0,compressed=0,size_uncompressed=0x40000,load_addr=0,rom_size=0x40200)
body=f[:0x40000]; tail=f[0x40000:]
result=dict(header_rom_offset=hex(s-256),analysis_length=len(f),fields=fields,
 body_length=len(body),trailer_length=len(tail),
 body_sha256=hashlib.sha256(body).hexdigest(),
 header_body_sha256_matches=hashlib.sha256(body).digest()==h[0xd0:0xf0],
 full_analysis_sha256_matches_header=hashlib.sha256(f).digest()==h[0xd0:0xf0],
 container_end=hex(s-256+fields['rom_size']),
 body_end=hex(s+len(body)),signature_verified=False,hardware_access=False)
assert result['header_body_sha256_matches'] and len(tail)==256
print(json.dumps(result,indent=2))
