"""Read retained artifacts and manifests only. Never build or load modules."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();r=a.root

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
rows=[]
for name in ['r305-register-access-static','r304-checkpoint-decision']:
 manifest=r/'research'/name/'INPUT_SHA256.json'
 for path,want in json.loads(manifest.read_text()).items():
  p=r/path
  rows.append({'manifest':str(manifest.relative_to(r)),'path':path,'expected':want,'actual':sha(p) if p.is_file() else None})
base=r/'research/r297-checkpoint-panic';m=base/'cp07-v1/BUILD_MANIFEST.json'
for path,want in json.loads(m.read_text()).items():
 p=m.parent/path;rows.append({'manifest':str(m.relative_to(r)),'path':str(p.relative_to(r)),'expected':want,'actual':sha(p) if p.is_file() else None})
for row in rows:row['matches']=row['expected']==row['actual']
debug=[];pairs=[]
for cp in ['05','06','07']:
 obj=base/('cp'+cp+'-v1')/('vcn_v2_0-r297-cp'+cp+'.o')
 s=subprocess.check_output(['readelf','--debug-dump=rawline',str(obj)],text=True)
 versions=re.findall(r'DWARF Version:\s*(\d+)',s)
 tables=[line.strip() for line in s.splitlines() if line.startswith(' The File Name Table')]
 headers=[line.strip() for line in s.splitlines() if line.strip().startswith('Entry\tDir')]
 sections=subprocess.check_output(['readelf','-SW',str(obj)],text=True)
 debug.append({'object':str(obj.relative_to(r)),'sha256':sha(obj),'dwarf_versions':versions,'file_table_descriptions':tables,'file_table_column_headers':headers,'macro_section':bool(re.search(r'\s\.debug_macro\s',sections)),'macinfo_section':bool(re.search(r'\s\.debug_macinfo\s',sections)),'file_table_has_md5_column':'MD5' in '\n'.join(headers)})
 pkg=base/('r297-cp'+cp+'-home-package')/('amdgpu-r297-cp'+cp+'-signed.ko')
 installed=base/('r297-cp'+cp+'-installed-final-audit')/'installed-amdgpu.ko'
 if cp=='07':installed=None
 pairs.append({'checkpoint':'CP'+cp,'package_module':str(pkg.relative_to(r)),'package_sha256':sha(pkg),'saved_installed_module':str(installed.relative_to(r)) if installed else None,'saved_installed_sha256':sha(installed) if installed and installed.is_file() else None,'saved_installed_match':sha(pkg)==sha(installed) if installed and installed.is_file() else None})
package=json.loads((base/'r297-cp07-home-package/PACKAGE_AUDIT.json').read_text())
installed_record=json.loads((base/'cp07-v1/INSTALLED_FINAL_AUDIT.json').read_text())
image=base/'r297-cp07-home-package/initramfs-7.2.3-r297-cp07.img'
actual_image=sha(image)
cp07_chain={'saved_image_sha256':actual_image,'matches_package_image_record':actual_image==package['image_sha256'],'matches_historical_installed_image_record':actual_image==installed_record['installed_hashes']['/boot/initramfs-7.2.3-r297-cp07.img'],'module_matches_package_record':pairs[-1]['package_sha256']==package['signed_module_sha256'],'roundtrip_evidence':'Historical package audit reports exact archive roundtrip; not rerun here','current_boot_files_read':False}
result={'classification':'PROVEN_STATICALLY','scope':'Retained artifacts only; no failed-boot runtime attestation','manifest_rows':rows,'manifest_matches':sum(x['matches'] for x in rows),'manifest_total':len(rows),'object_debug':debug,'package_installed_pairs':pairs,'cp07_saved_chain':cp07_chain,'hardware_access':False,'build_or_install_performed':False,'limits':['Current source hashes do not establish complete historical build-input identity','Missing saved-installed module here is not a claim that no historical package/install audit exists','DWARF filename/line presence is not a header-content digest','No failed-boot access instruction or physical state inferred']}
a.output.write_text(json.dumps(result,indent=2)+'\n');print('Manifest matches',result['manifest_matches'],'/',len(rows));print('Saved installed module matches',[(x['checkpoint'],x['saved_installed_match']) for x in pairs])
