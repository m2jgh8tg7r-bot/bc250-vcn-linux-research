from pathlib import Path
import argparse,hashlib,json,os,shutil,signal,subprocess
out=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='Default: read-only R325 installation preflight')
parser.add_argument('--install',action='store_true');args=parser.parse_args()
assert os.geteuid()==0,'sudo required for protected boot identities'
assert os.uname().release=='7.2.1-ogc4.1.fc44.x86_64'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,r):
 p=out/name;p.write_text(json.dumps(r,indent=2)+'\n');os.chown(p,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())));print(json.dumps(r,indent=2))
e=dict(s.split('=',1) for s in subprocess.check_output(['grub2-editenv','/boot/grub2/grubenv','list'],text=True).splitlines() if '=' in s)
assert e.get('boot_success')=='1'
assert not any(k in e for k in ('next_entry','menu_show_once','menu_show_once_timeout'))
assert Path('/sys/module/efi_pstore/parameters/pstore_disable').read_text().strip()=='Y'
a=json.loads((out/'PACKAGE_AUDIT.json').read_text());assert a['contract']=='PASS'
new={Path('/boot/initramfs-7.2.3-r325-finalptr.img'):(out/'initramfs-7.2.3-r325-finalptr.img',a['image_sha256']),Path('/boot/loader/entries/boot-entry-r325-finalptr.conf'):(out/'boot-entry-r325-finalptr.conf',a['bls_sha256'])}
old={Path('/boot/initramfs-7.2.3-r318-nethold.img'):'99ce2746bc8ce353df06e407dbc58c7894c3d9e0009a0dcef733aeb475b62de9',Path('/boot/loader/entries/boot-entry-r318-nethold.conf'):'ae581209c69f07f39ddb77f0e56f8c9eb221866edf2fdc7e2b57d1d1b7750423'}
for dst,(src,h) in new.items():assert not dst.exists() and sha(src)==h
for p,h in old.items():assert sha(p)==h,'R318 changed; stop'
assert sha(out/'init')==a['init_sha256']
protected=[Path('/boot/grub2/grub.cfg'),Path('/boot/grub2/grubenv'),Path('/boot/vmlinuz-7.2.3-r138'),Path('/boot/initramfs-7.2.3-r180-observation.img'),Path('/boot/initramfs-7.2.3-r298-netobs1.img')]
entries=sorted(p for p in Path('/boot/loader/entries').glob('*.conf') if p not in old)
assert any(p.name.startswith('ostree-') for p in entries)
from boot_default import check_default
before_entries={p.name:p.read_text() for p in Path('/boot/loader/entries').glob('*.conf')}
after_entries={n:t for n,t in before_entries.items() if n!='boot-entry-r318-nethold.conf'}
after_entries['boot-entry-r325-finalptr.conf']=(out/'boot-entry-r325-finalptr.conf').read_text()
include_paths={n:Path('/boot/grub2')/n for n in ['bootuuid.cfg','console.cfg','user.cfg']}
for p in include_paths.values():assert not p.is_symlink(), 'Unexpected include symlink; review required'
includes={n:p.read_text() if p.is_file() else None for n,p in include_paths.items()}
include_state={n:sha(p) if p.is_file() else None for n,p in include_paths.items()}
default_check=check_default(e,Path('/boot/grub2/grub.cfg').read_text(),before_entries,after_entries,includes)
protected += [p for p in include_paths.values() if p.is_file()]
assert Path('/boot/loader/entries/boot-entry-r180-observation.conf') in entries
for p in entries:
 for line in p.read_text().splitlines():
  if line.startswith(('linux ','initrd ')):
   q=Path('/boot')/line.split(None,1)[1].lstrip('/');assert q.is_file();protected.append(q)
protected+=entries
hashes={str(p):sha(p) for p in protected}
assert hashes['/boot/vmlinuz-7.2.3-r138']=='c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6'
st=os.statvfs('/boot');free=st.f_bavail*st.f_frsize;margin=50*1024*1024
assert free+sum(p.stat().st_size for p in old)>=sum(s.stat().st_size for s,h in new.values())+margin
snapshot={'include_state':include_state,'include_checker_sha256':sha(out/'boot_includes.py'),'default_check':default_check,'default_checker_sha256':sha(out/'boot_default.py'),'contract':'PASS','protected_hashes':hashes,'old_hashes':{str(p):h for p,h in old.items()},'package_sha256':sha(out/'PACKAGE_AUDIT.json'),'installer_sha256':sha(Path(__file__)),'free_bytes':free,'new_image_bytes':a['image_size'],'margin_bytes':margin,'boot_write':False,'boot_selection_change':False,'reboot':False}
if not args.install:save('PREFLIGHT_RESULT.json',snapshot)
else:
 f=json.loads((out/'PREFLIGHT_RESULT.json').read_text())
 for k in ('contract','protected_hashes','old_hashes','package_sha256','installer_sha256','default_check','default_checker_sha256','include_state','include_checker_sha256'):assert f[k]==snapshot[k]
 backup=out/'r318-retirement-backup';assert not backup.exists();backup.mkdir()
 for p,h in old.items():
  q=backup/p.name;shutil.copy2(p,q);assert sha(q)==h
 os.sync()
 def interrupted(signum,frame):raise InterruptedError('installation interrupted')
 for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,interrupted)
 removed=[];created=[]
 try:
  for p in old:removed.append(p);p.unlink()
  for dst,(src,h) in new.items():
   created.append(dst)
   with dst.open('xb') as stream,src.open('rb') as source:shutil.copyfileobj(source,stream)
   os.chmod(dst,0o644);assert sha(dst)==h
  os.sync();assert all(sha(Path(p))==h for p,h in hashes.items())
  assert {n:sha(p) if p.is_file() else None for n,p in include_paths.items()}==include_state
  st=os.statvfs('/boot');assert st.f_bavail*st.f_frsize>=margin
  save('INSTALLED_RESULT.json',{'contract':'PASS','installed_hashes':{str(p):h for p,(s,h) in new.items()},'protected_hashes':hashes,'r318_backed_up':True,'boot_selection_change':False,'module_load':False,'reboot':False})
 except BaseException:
  for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,signal.SIG_IGN)
  for p in created:p.unlink(missing_ok=True)
  for p in removed:shutil.copy2(backup/p.name,p);assert sha(p)==old[p]
  os.sync();print('R325_ROLLBACK=PASS');raise
