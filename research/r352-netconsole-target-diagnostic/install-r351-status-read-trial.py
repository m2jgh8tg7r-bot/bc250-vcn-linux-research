"""Protected preflight by default; --install swaps corrected R352 for the exact backed-up R351 trial."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,signal,subprocess,sys
OUT=Path('/var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic')
R351=Path('/var/home/kazuyuki/bc250-research/research/r351-vcn-status-read-observation')
BACK=OUT/'r351-retirement-backup'
sys.path.insert(0,str(R351))
from boot_default import check_default
pa=argparse.ArgumentParser(description='R351 one-read trial preflight; --install swaps current R352 image in-place')
pa.add_argument('--install',action='store_true');args=pa.parse_args()
if os.geteuid()!=0:raise SystemExit('Run with sudo python3 for protected /boot preflight.')
OLDI=Path('/boot/initramfs-7.2.3-r352-netdiag.img');OLDE=Path('/boot/loader/entries/boot-entry-r352-netdiag.conf')
NEWI=Path('/boot/initramfs-7.2.3-r351-statusread.img');NEWE=Path('/boot/loader/entries/boot-entry-r351-statusread.conf')
ENV=Path('/boot/grub2/grubenv');MARGIN=50*1024*1024

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def load(p):return json.loads(p.read_text())
def env():return dict(line.split('=',1) for line in subprocess.check_output(['grub2-editenv',str(ENV),'list'],text=True).splitlines() if '=' in line)
def capture():
 issues=[]
 def req(ok,msg):
  if not ok:issues.append(msg)
 r2=load(OUT/'INSTALLED_RESULT.json');r1=load(R351/'INSTALLED_RESULT.json')
 req(r2.get('contract')=='PASS' and r2.get('corrected_image_embedded_init')=='R352','corrected R352 install record not PASS')
 req(r1.get('contract')=='PASS','original R351 install record missing')
 req(not NEWI.exists() and not NEWE.exists(),'R351 already present in /boot; inspect before continuing')
 req(OLDI.is_file() and not OLDI.is_symlink() and sha(OLDI)==r2.get('installed_hashes',{}).get(str(OLDI)),'corrected R352 image mismatch')
 req(OLDE.is_file() and not OLDE.is_symlink() and sha(OLDE)==r2.get('installed_hashes',{}).get(str(OLDE)),'corrected R352 BLS mismatch')
 b_i=BACK/'initramfs-7.2.3-r351-statusread.img';b_e=BACK/'boot-entry-r351-statusread.conf'
 req(b_i.is_file() and sha(b_i)==r1.get('installed_hashes',{}).get(str(NEWI)),'retired R351 image backup mismatch')
 req(b_e.is_file() and sha(b_e)==r1.get('installed_hashes',{}).get(str(NEWE)),'retired R351 BLS backup mismatch')
 actual={}
 for name,expected in r2.get('protected_hashes',{}).items():
  p=Path(name);got=sha(p) if p.is_file() and not p.is_symlink() else None;actual[name]=got;req(got==expected,'protected file changed: '+name)
 e=env();req(e=={'boot_success':'1'},'GRUB env not recovered normal baseline: '+repr(e))
 req(os.uname().release=='7.2.1-ogc4.1.fc44.x86_64','running kernel is not normal Bazzite')
 ps=Path('/sys/module/efi_pstore/parameters/pstore_disable');req(ps.is_file() and ps.read_text().strip()=='Y','EFI pstore policy is not restored to Y')
 nw=Path('/proc/sys/kernel/nmi_watchdog');req(nw.read_text().strip()=='1','NMI watchdog is not enabled')
 req(not Path('/sys/module/netconsole').exists(),'normal-boot netconsole is loaded; inspect before swapping')
 records={p.name:sha(p) for p in Path('/sys/fs/pstore').iterdir() if p.is_file()};req(not records,'pstore records exist; preserve and review before proceeding')
 before={p.name:p.read_text() for p in Path('/boot/loader/entries').glob('*.conf') if not p.is_symlink()}
 req(OLDE.name in before,'R352 BLS entry missing from menu')
 after={n:t for n,t in before.items() if n!=OLDE.name};after[NEWE.name]=b_e.read_text()
 cfg=Path('/boot/grub2/grub.cfg').read_text();includes_state=load(OUT/'PREFLIGHT_RESULT.json')['include_state'];includes={}
 for name,expected in includes_state.items():
  p=Path('/boot/grub2')/name;req(not p.is_symlink(),'unexpected GRUB include symlink: '+name);got=sha(p) if p.is_file() else None;req(got==expected,'GRUB include changed: '+name);includes[name]=p.read_text() if p.is_file() else None
 try:default=check_default(e,cfg,before,after,includes)
 except Exception as exc:default=None;issues.append('GRUB default/layout check failed: '+str(exc))
 fs=os.statvfs('/boot');free=fs.f_bavail*fs.f_frsize;oldsize=OLDI.stat().st_size if OLDI.is_file() else 0;newsize=b_i.stat().st_size if b_i.is_file() else 0
 req(free+oldsize>=newsize+MARGIN,'/boot lacks 50 MiB margin after R352/R351 swap')
 req(Path('/boot/vmlinuz-7.2.3-r138').is_file(),'R138 recovery kernel missing')
 return {'contract':'PASS' if not issues else 'FAIL','issues':issues,'normal_kernel':os.uname().release,'grub_environment_keys':e,'default_check':default,'protected_hashes':actual,'grubenv_sha256':sha(ENV),'pstore_records_preserved':records,'current_r352_hashes':{str(OLDI):sha(OLDI),str(OLDE):sha(OLDE)},'restore_r351_hashes':{str(NEWI):sha(b_i),str(NEWE):sha(b_e)},'free_bytes':free,'old_image_bytes':oldsize,'new_image_bytes':newsize,'safety_margin_bytes':MARGIN,'boot_selection_change':False,'reboot':False,'hardware_access':False}
def save(name,data):
 p=OUT/name;p.write_text(json.dumps(data,indent=2)+'\n');os.chown(p,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())));print(json.dumps(data,indent=2))
snapshot=capture()
if not args.install:save('R351_TRIAL_PREFLIGHT.json',snapshot);raise SystemExit(0 if snapshot['contract']=='PASS' else 2)
if snapshot['contract']!='PASS':save('R351_TRIAL_BLOCKED.json',snapshot);raise SystemExit(2)
pre=load(OUT/'R351_TRIAL_PREFLIGHT.json')
if {k:v for k,v in pre.items() if k!='free_bytes'}!={k:v for k,v in snapshot.items() if k!='free_bytes'}:raise SystemExit('Protected state changed since preflight; rerun and review.')
backup=OUT/'r352-corrected-image-retirement-backup'
if backup.exists():raise SystemExit('Corrected R352 retirement backup already exists; inspect before continuing.')
backup.mkdir()
for src in (OLDI,OLDE):shutil.copy2(src,backup/src.name)
for src in (OLDI,OLDE):
 if sha(backup/src.name)!=snapshot['current_r352_hashes'][str(src)]:raise SystemExit('R352 retirement backup mismatch; /boot unchanged.')
(OUT/'grubenv-before-r351-vcn-trial-install.bin').write_bytes(ENV.read_bytes());os.sync()
def interrupted(signum,frame):raise InterruptedError('R351 trial install interrupted')
for s in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(s,interrupted)
removed=[];created=[];temps=[]
try:
 for p in (OLDE,OLDI):p.unlink();removed.append(p);os.sync()
 for src,dst,expected in ((BACK/'initramfs-7.2.3-r351-statusread.img',NEWI,snapshot['restore_r351_hashes'][str(NEWI)]),(BACK/'boot-entry-r351-statusread.conf',NEWE,snapshot['restore_r351_hashes'][str(NEWE)])):
  tmp=dst.with_name('.'+dst.name+'.r351trial-tmp')
  if tmp.exists():raise RuntimeError('unexpected temp file: '+str(tmp))
  temps.append(tmp)
  with tmp.open('xb') as target,src.open('rb') as source:shutil.copyfileobj(source,target)
  os.chmod(tmp,0o644)
  if sha(tmp)!=expected:raise RuntimeError('R351 restore hash mismatch: '+str(tmp))
  os.replace(tmp,dst);temps.remove(tmp);created.append(dst);os.sync()
 for name,digest in snapshot['protected_hashes'].items():
  if sha(Path(name))!=digest:raise RuntimeError('protected file changed: '+name)
 if sha(ENV)!=snapshot['grubenv_sha256']:raise RuntimeError('GRUB env changed during R351 trial install')
 if sha(NEWI)!=snapshot['restore_r351_hashes'][str(NEWI)] or sha(NEWE)!=snapshot['restore_r351_hashes'][str(NEWE)]:raise RuntimeError('installed R351 hash mismatch')
 remaining=os.statvfs('/boot').f_bavail*os.statvfs('/boot').f_frsize
 if remaining<MARGIN:raise RuntimeError('post-install /boot margin below 50 MiB')
 save('R351_TRIAL_INSTALL_RESULT.json',{'contract':'PASS','installed_hashes':{str(NEWI):sha(NEWI),str(NEWE):sha(NEWE)},'protected_hashes':snapshot['protected_hashes'],'grubenv_sha256_at_install':snapshot['grubenv_sha256'],'r352_corrected_backup':{p.name:sha(p) for p in backup.iterdir()},'boot_selection_change':False,'module_load':False,'reboot':False,'hardware_access':False,'remaining_boot_free_bytes':remaining})
except BaseException:
 for s in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(s,signal.SIG_IGN)
 for p in created:p.unlink(missing_ok=True)
 for p in temps:p.unlink(missing_ok=True)
 for src,dst in ((backup/OLDI.name,OLDI),(backup/OLDE.name,OLDE)):
  if src.exists():shutil.copy2(src,dst);assert sha(dst)==sha(src)
 os.sync();print('R351_TRIAL_ROLLBACK=RESTORED_CORRECTED_R352');raise
