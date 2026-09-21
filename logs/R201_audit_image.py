"""CPU-only evidence extraction; never opens a device."""
import hashlib,json,struct,sys
from pathlib import Path
image=Path(sys.argv[1]).read_bytes()
expected="8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675"
assert hashlib.sha256(image).hexdigest()==expected
u32=lambda a:struct.unpack_from("<I",image,a)[0]
def signed(v,n):return v-(1<<n) if v&(1<<(n-1)) else v
def decode(a,kind):
 b=image[a:a+3];v=int.from_bytes(b,"little")
 if kind=="call8":
  assert v&63==0x25
  displacement=signed(v>>6,18)*4; target=(a&~3)+4+displacement
 else:
  assert v&255 in (0x16,0x56)
  displacement=signed(v>>12,12);target=a+4+displacement
 return dict(pc=hex(a),bytes=b.hex(),kind=kind,displacement=displacement,target=hex(target))
branches=[decode(a,k) for a,k in [(0x1edd9,"call8"),(0x1eddc,"beqz"),(0x1ede5,"bnez"),(0x1eea3,"call8"),(0x1eeac,"call8")]]
assert [x["target"] for x in branches]==["0x1db54","0x1eeb4","0x1eeb4","0x241ac","0x241ac"]
descriptors=[]
for i in [3,4,6]:
 a=u32(0x17434)+i*0x48;base=u32(a+8)
 descriptors.append(dict(index=i,address=hex(a),words=[hex(u32(a+j)) for j in range(0,0x48,4)],registers={hex(j):hex(base+u32(a+j)) for j in [0x1c,0x20,0x24,0x28,0x2c,0x30]}))
slotbase=u32(0x178ac)
slotmap={hex(i):image[slotbase+i*0x1c+0x80] for i in [15,0x16,0x17,0x18]}
featurebase=u32(0x17374)
featurecallbacks={str(i):dict(enable=hex(u32(featurebase+0x10+i*4)),disable=hex(u32(featurebase+0x110+i*4))) for i in [11,13]}
result=dict(slot_descriptor_map=slotmap,feature_callbacks=featurecallbacks,sha256=expected,size=len(image),version=hex(u32(0)),address_rule="file offset equals firmware address; validated separately against Ghidra memory",branches=branches,gate=dict(base=hex(u32(0x171d4)),offset="0x19",address=hex(u32(0x171d4)+0x19),saved_byte=image[0xcee1],runtime_value="UNPROVEN"),predicate=dict(base=hex(u32(0x17374)),arg=11,word=hex(u32(0x17374)+8),bit=11),descriptors=descriptors)
print(json.dumps(result,indent=2))
