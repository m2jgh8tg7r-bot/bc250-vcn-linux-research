"""Compare retained ELF function bytes and relocations, without executing modules."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();rows=[]
names=['amdgpu_discovery_set_ip_blocks','amdgpu_discovery_reg_base_init']
for cp in ['05','06','07']:
 f=a.root/f'research/r297-checkpoint-panic/r297-cp{cp}-home-package/amdgpu-r297-cp{cp}-signed.ko'
 sy=subprocess.check_output(['readelf','-sW',str(f)],text=True);se=subprocess.check_output(['readelf','-SW',str(f)],text=True);relo=subprocess.check_output(['readelf','-rW',str(f)],text=True)
 out={}
 for name in names:
  m=re.findall(r'^\s*\d+:\s*([0-9a-f]+)\s+(\d+)\s+FUNC\s+\S+\s+DEFAULT\s+(\d+)\s+'+name+r'$',sy,re.M);assert len(m)==1
  start,size,index=m[0];start=int(start,16);size=int(size)
  sm=re.search(r'^\s*\[\s*'+index+r'\]\s+(\S+)\s+PROGBITS\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)',se,re.M);assert sm
  section,addr,offset,length=sm.groups();addr=int(addr,16);offset=int(offset,16);length=int(length,16);assert 0<=start-addr and start-addr+size<=length
  with f.open('rb') as stream:stream.seek(offset+start-addr);data=stream.read(size)
  assert len(data)==size
  current='';rels=[]
  for line in relo.splitlines():
   if line.startswith('Relocation section'):current=line.split("'")[1]
   if current!='.rela'+section:continue
   rm=re.match(r'([0-9a-f]+)\s+\S+\s+(R_\S+)\s+\S+\s+(.+)$',line)
   if rm and start<=int(rm[1],16)<start+size:rels.append([int(rm[1],16)-start,rm[2],rm[3]])
  dis=subprocess.check_output(['objdump','-dr','--disassemble='+name,str(f)],text=True)
  lines=dis.splitlines();snips=[]
  if name==names[0]:
   for i,line in enumerate(lines):
    if 'testb' in line and '$0x40,0x690(%rdi)' in line:snips.append('\n'.join(lines[i:i+7]))
    if 'R_X86_64_PLT32\tcyan_skillfish_reg_base_init' in line:snips.append('\n'.join(lines[i-1:i+1]))
   assert len(snips)==2
  strings={}
  if name==names[1]:
   ro=re.search(r'\]\s+\.rodata\s+PROGBITS\s+[0-9a-f]+\s+([0-9a-f]+)',se);assert ro
   for rel in rels:
    if rel[0] not in [165,269,405,635,813,1379]:continue
    assert rel[2].startswith('.rodata + ')
    with f.open('rb') as stream:
     stream.seek(int(ro[1],16)+int(rel[2].split(' + ')[1],16));raw=stream.read(256)
    assert b'\0' in raw
    strings[str(rel[0])]=raw.split(b'\0')[0].decode('ascii')
  out[name]={'resolved_selected_strings':strings,'start':start,'size':size,'sha256':hashlib.sha256(data).hexdigest(),'relocations':rels,'branch_excerpts':snips}
 rows.append({'checkpoint':'CP'+cp,'functions':out})
comparisons={n:{'bytes_equal':len({r['functions'][n]['sha256'] for r in rows})==1,'relocations_equal':all(r['functions'][n]['relocations']==rows[0]['functions'][n]['relocations'] for r in rows)} for n in names}
n=names[1]
normalized=[]
for row in rows:
 f=row['functions'][n]
 normalized.append([[off,kind,{'cstring':f['resolved_selected_strings'][str(off)]} if str(off) in f['resolved_selected_strings'] else target] for off,kind,target in f['relocations']])
comparisons[n]['equal_after_resolving_six_selected_string_relocations']=all(x==normalized[0] for x in normalized)
v={'classification':'PROVEN_STATICALLY','scope':'Retained compiled functions and relocations only; not loaded failed-boot memory','rows':rows,'comparisons':comparisons,'hardware_access':False,'limitations':['Relocation targets and external callees are not recursively attested','Runtime apu_flags, discovery data and branch execution remain unproven','Fixed disassembly pattern is specific to these retained x86-64 artifacts']}
Path(__file__).with_name('results.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(comparisons))
