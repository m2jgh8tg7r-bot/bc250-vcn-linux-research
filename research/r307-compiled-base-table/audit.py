"""Read an existing ELF data symbol; never execute the module."""
from pathlib import Path
import argparse,hashlib,json,re,struct,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=a.root
header=r/'r152-psp-boundary-src/drivers/gpu/drm/amd/include/cyan_skillfish_ip_offset.h'
s=header.read_text();init=s.split('static const struct IP_BASE UVD0_BASE',1)[1].split(';',1)[0].split('=',1)[1]
nums=[int(x,0) for x in re.findall(r'0x[0-9A-Fa-f]+|\b[0-9]+\b',init)]
assert len(nums)==30 and '#define MAX_INSTANCE                                       6' in s and '#define MAX_SEGMENT                                        5' in s
expected=struct.pack('<30I',*nums);records=[]
for cp in ['05','06','07']:
 module=r/('research/r297-checkpoint-panic/r297-cp'+cp+'-home-package/amdgpu-r297-cp'+cp+'-signed.ko')
 symbols=subprocess.check_output(['readelf','-sW',str(module)],text=True)
 matches=re.findall(r'^\s*\d+:\s*([0-9a-f]+)\s+(\d+)\s+OBJECT\s+LOCAL\s+DEFAULT\s+(\d+)\s+UVD0_BASE$',symbols,re.M)
 assert len(matches)==1
 value,size,index=matches[0];value=int(value,16);size=int(size);index=int(index)
 sections=subprocess.check_output(['readelf','-SW',str(module)],text=True)
 match=re.search(r'^\s*\[\s*'+str(index)+r'\]\s+(\S+)\s+(\S+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s',sections,re.M);assert match
 name,kind,addr,offset,length=match.groups();addr=int(addr,16);offset=int(offset,16);length=int(length,16)
 assert name=='.rodata' and kind=='PROGBITS' and size==120 and value>=addr and value-addr+size<=length
 with module.open('rb') as f:
  magic=f.read(18);assert magic[:6]==b'\x7fELF\x02\x01' and struct.unpack('<H',magic[16:18])[0]==1
  f.seek(offset+value-addr);data=f.read(size)
 assert len(data)==120
 digest=hashlib.sha256()
 with module.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):digest.update(b)
 funcs=re.findall(r'^\s*\d+:\s*([0-9a-f]+)\s+(\d+)\s+FUNC\s+GLOBAL\s+DEFAULT\s+(\d+)\s+cyan_skillfish_reg_base_init$',symbols,re.M)
 assert len(funcs)==1
 func_value,func_size,func_index=funcs[0];func_value=int(func_value,16);func_size=int(func_size)
 fm=re.search(r'^\s*\[\s*'+func_index+r'\]\s+(\S+)\s',sections,re.M);assert fm
 rels=subprocess.check_output(['readelf','-rW',str(module)],text=True);current='';refs=[]
 for line in rels.splitlines():
  if line.startswith('Relocation section'):current=line.split("'")[1]
  if current!='.rela'+fm[1]:continue
  rm=re.match(r'([0-9a-f]+)\s+\S+\s+(\S+)\s+\S+\s+(\S+)\s+\+\s+([0-9a-f]+)$',line)
  if rm and func_value<=int(rm[1],16)<func_value+func_size and rm[3]==name and value<=int(rm[4],16)<value+size:
   refs.append({'function_relative_offset':int(rm[1],16)-func_value,'relocation_type':rm[2],'table_relative_addend':int(rm[4],16)-value})
 records.append({'compiled_init_references':refs,'checkpoint':'CP'+cp,'module':str(module.relative_to(r)),'module_sha256':digest.hexdigest(),'symbol':'UVD0_BASE','symbol_size':size,'section':name,'compiled_data_sha256':hashlib.sha256(data).hexdigest(),'matches_retained_header_initializer':data==expected})
result={'classification':'PROVEN_STATICALLY','header':str(header.relative_to(r)),'header_sha256':hashlib.sha256(header.read_bytes()).hexdigest(),'initializer_bytes':120,'initializer_sha256':hashlib.sha256(expected).hexdigest(),'modules':records,'all_match':all(x['matches_retained_header_initializer'] for x in records),'limits':['UVD0_BASE belongs to the non-Skillfish2 fallback branch; retained source selects discovery-derived bases for PCI 13FE','Data-symbol equality is not proof that initialization ran','Not proof of failed-boot reg_offset contents or runtime device response','Six storage slots and zero entries are not physical-instance discovery evidence','Not a complete transitive-header or module-equivalence claim'],'hardware_access':False,'module_executed':False}
a.output.write_text(json.dumps(result,indent=2)+'\n');print('UVD0_BASE static data matches:',[(x['checkpoint'],x['matches_retained_header_initializer']) for x in records])
