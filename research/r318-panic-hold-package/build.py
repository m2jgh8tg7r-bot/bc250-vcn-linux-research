#!/usr/bin/env python3
"""Prepare an isolated R312-derived image; never install or boot it."""
from pathlib import Path
import hashlib,json,os,stat,subprocess
out=Path(__file__).resolve().parent
old=out.parent/'r316-extended-boot-package'
tree=out/'tree';rt=out/'roundtrip'
def run(args,**kwargs):return subprocess.run(args,check=True,**kwargs)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(t):
    result={}
    for p in t.rglob('*'):
        n=str(p.relative_to(t))
        if p.is_symlink():result[n]=['link',os.readlink(p)]
        elif p.is_file():result[n]=['file',sha(p),stat.S_IMODE(p.stat().st_mode)]
        elif p.is_dir():result[n]=['directory',stat.S_IMODE(p.stat().st_mode)]
        else:raise ValueError('Unexpected special file: '+n)
    return result
assert not tree.exists() and not rt.exists(),'Use a new output directory; do not overwrite'
assert sha(old/'initramfs-7.2.3-r316-netext.img')=='1f19bf6bd0dfffb8d27df5f981cc8c8cabc53b925491699ee5fbb4877a3c244c'
before=manifest(old/'tree')
assert before==manifest(old/'roundtrip')
run(['cp','--reflink=always','-a',str(old/'tree'),str(tree)])
original=(tree/'init').read_text()
assert original.count('"netconsole=')==1
assert original.count('"netconsole=+')==1
candidate=original.replace('R316','R318').replace('NETEXT','NETHOLD')
assert candidate.replace('R318','R316').replace('NETHOLD','NETEXT')==original
(tree/'init').write_text(candidate);(out/'init').write_text(candidate)
run(['bash','-n',str(tree/'init')])
after=manifest(tree)
changed=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
assert changed==['init'],changed
image=out/'initramfs-7.2.3-r318-nethold.img'
paths=sorted(subprocess.check_output(['find','.','-print0'],cwd=tree).split(b'\0')[:-1])
with image.open('xb') as f:
    c=subprocess.Popen(['cpio','--null','-o','-H','newc','--owner=0:0','--quiet'],cwd=tree,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    g=subprocess.Popen(['gzip','-9n'],stdin=c.stdout,stdout=f)
    c.stdout.close();c.communicate(b'\0'.join(paths)+b'\0')
    assert c.returncode==0 and g.wait()==0
run(['gzip','-t',str(image)]);rt.mkdir()
with image.open('rb') as f:
    g=subprocess.Popen(['gzip','-dc'],stdin=f,stdout=subprocess.PIPE)
    run(['cpio','-idm','--quiet','--no-absolute-filenames'],stdin=g.stdout,cwd=rt)
    g.stdout.close();assert g.wait()==0
assert manifest(rt)==after
assert manifest(old/'tree')==before
bls=out/'boot-entry-r318-nethold.conf'
bls.write_text('title BC-250 R318 panic hold - MANUAL RESET REQUIRED\nversion 0\nlinux /vmlinuz-7.2.3-r138\ninitrd /initramfs-7.2.3-r318-nethold.img\noptions rdinit=/init console=tty0 loglevel=8 net.ifnames=0 efi_pstore.pstore_disable=Y sysrq_always_enabled panic=0\n')
result={'contract':'PASS','image_sha256':sha(image),'image_size':image.stat().st_size,'bls_sha256':sha(bls),'init_sha256':sha(out/'init'),'changed_paths':changed,'roundtrip_exact':True,'baseline_unchanged':True,'all_modules_firmware_unchanged':True,'installed':False,'booted':False,'hardware_access':False}
(out/'PACKAGE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
