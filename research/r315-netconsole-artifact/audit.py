#!/usr/bin/env python3
import hashlib,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
paths={
 'staged':ROOT/'research/r312-metadata-boot-package/tree/usr/lib/modules/7.2.3+/kernel/drivers/net/netconsole.ko',
 'roundtrip':ROOT/'research/r312-metadata-boot-package/roundtrip/usr/lib/modules/7.2.3+/kernel/drivers/net/netconsole.ko',
 'build':ROOT/'research/r310-preaccess-metadata/build-tree/drivers/net/netconsole.ko'}
def sections(data):
    assert data[:6]==b'\x7fELF\x02\x01'
    h=struct.unpack_from('<16sHHIQQQIHHHHHH',data)
    offset,entsize,count,names=h[6],h[11],h[12],h[13]
    headers=[struct.unpack_from('<IIQQQQIIQQ',data,offset+i*entsize) for i in range(count)]
    sh=headers[names];strings=data[sh[4]:sh[4]+sh[5]]
    return {strings[s[0]:].split(b'\0',1)[0].decode():data[s[4]:s[4]+s[5]] for s in headers if s[2]&4 and s[1]!=8}
blobs={k:p.read_bytes() for k,p in paths.items()};ss={k:sections(v) for k,v in blobs.items()}
result={'module_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in blobs.items()},'staged_roundtrip_equal':blobs['staged']==blobs['roundtrip'],'executable_section_names_equal':ss['staged'].keys()==ss['build'].keys(),'executable_sections':{k:{'size':len(v),'sha256':hashlib.sha256(v).hexdigest(),'build_equal':ss['build'].get(k)==v} for k,v in ss['staged'].items()},'limits':'Executable bytes only; not relocation/data equality, running module identity or live delivery proof'}
print(json.dumps(result,indent=2))
