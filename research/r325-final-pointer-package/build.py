"""HOME-only preparation. Never installs, boots, or loads a module."""
from pathlib import Path
import hashlib,json,subprocess,os,stat,re,shutil
out=Path(__file__).resolve().parent;old=out.parent/'r318-panic-hold-package';src=out.parent/'r324-final-pointer-checkpoint';base=src/'build-tree';tree=out/'tree';rt=out/'roundtrip'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(a,**kw):return subprocess.run(a,check=True,**kw)
def manifest(t):
 d={}
 for p in t.rglob('*'):
  n=str(p.relative_to(t))
  if p.is_symlink():d[n]=['link',os.readlink(p)]
  elif p.is_file():d[n]=['file',sha(p),stat.S_IMODE(p.stat().st_mode)]
  elif p.is_dir():d[n]=['directory',stat.S_IMODE(p.stat().st_mode)]
  else:raise ValueError('special file')
 return d
assert json.loads((src/'CLOSED_MODULE_AUDIT.json').read_text())['result']=='PASS'
assert sha(old/'initramfs-7.2.3-r318-nethold.img')==json.loads((old/'PACKAGE_AUDIT.json').read_text())['image_sha256']
assert not tree.exists() and not rt.exists()
full=src/'amdgpu.candidate.ko';signed=out/'amdgpu-r325-signed.ko';shutil.copy2(full,signed);run(['strip','--strip-debug',str(signed)])
run([str(base/'scripts/sign-file'),'sha512',str(base/'certs/signing_key.pem'),str(base/'certs/signing_key.x509'),str(signed)])
assert subprocess.check_output(['modinfo','-F','sig_id',str(signed)],text=True).strip()=='PKCS#7'
assert subprocess.check_output(['modinfo','-F','vermagic',str(signed)],text=True).startswith('7.2.3+')
sections=[]
for line in subprocess.check_output(['readelf','-SW',str(full)],text=True).splitlines():
 m=re.match(r'\s*\[\s*\d+\]\s+(\S+)\s+PROGBITS\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)',line)
 if not m or 'X' not in m[2]:continue
 q=[]
 for i,p in enumerate([full,signed]):
  dest=out/f'section-{i}.bin';run(['objcopy','-O','binary','--only-section='+m[1],str(p),str(dest)]);q.append(dest)
 assert q[0].read_bytes()==q[1].read_bytes();sections.append({'section':m[1],'sha256':sha(q[0])})
 for f in q:f.unlink()
assert sections
before=manifest(old/'tree');assert before==manifest(old/'roundtrip')
run(['cp','--reflink=always','-a',str(old/'tree'),str(tree)])
original=(tree/'init').read_text();candidate=original.replace('R318','R325').replace('R311 metadata control','R324 final-pointer control').replace('expected R311 metadata then panic','expected R324 final-pointer metadata then panic');(tree/'init').write_text(candidate);(out/'init').write_text(candidate);run(['bash','-n',str(tree/'init')])
modpath='usr/lib/modules/7.2.3+/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko';shutil.copy2(signed,tree/modpath)
with (out/'depmod.log').open('w') as f:run(['depmod','-b',str(tree),'7.2.3+'],stdout=f,stderr=subprocess.STDOUT)
assert not (out/'depmod.log').read_text().strip()
after=manifest(tree);changed=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k));assert all(k in ['init',modpath] or k.startswith('usr/lib/modules/7.2.3+/modules.') for k in changed),changed
image=out/'initramfs-7.2.3-r325-finalptr.img';paths=sorted(subprocess.check_output(['find','.','-print0'],cwd=tree).split(b'\0')[:-1])
with image.open('xb') as f:
 c=subprocess.Popen(['cpio','--null','-o','-H','newc','--owner=0:0','--quiet'],cwd=tree,stdin=subprocess.PIPE,stdout=subprocess.PIPE);g=subprocess.Popen(['gzip','-9n'],stdin=c.stdout,stdout=f);c.stdout.close();c.communicate(b'\0'.join(paths)+b'\0');assert c.returncode==0 and g.wait()==0
run(['gzip','-t',str(image)]);rt.mkdir()
with image.open('rb') as f:
 g=subprocess.Popen(['gzip','-dc'],stdin=f,stdout=subprocess.PIPE);run(['cpio','-idm','--quiet','--no-absolute-filenames'],stdin=g.stdout,cwd=rt);g.stdout.close();assert g.wait()==0
assert manifest(rt)==after;assert manifest(old/'tree')==before
bls=out/'boot-entry-r325-finalptr.conf';bls.write_text('title BC-250 R325 final pointer checkpoint - MANUAL RESET REQUIRED\nversion 0\nlinux /vmlinuz-7.2.3-r138\ninitrd /initramfs-7.2.3-r325-finalptr.img\noptions rdinit=/init console=tty0 loglevel=8 net.ifnames=0 efi_pstore.pstore_disable=Y sysrq_always_enabled panic=0\n')
result={'contract':'PASS','image_sha256':sha(image),'image_size':image.stat().st_size,'bls_sha256':sha(bls),'init_sha256':sha(out/'init'),'module_sha256':sha(signed),'signed_executable_sections_equal':sections,'changed_paths':changed,'dependencies':'depmod clean','baseline_unchanged':True,'roundtrip_exact':True,'installed':False,'booted':False,'hardware_access':False};(out/'PACKAGE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print('R325 HOME image roundtrip and signing PASS')
