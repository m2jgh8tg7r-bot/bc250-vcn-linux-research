"""Guarded in-place correction of the currently installed R352 initramfs."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, signal, subprocess
OUT=Path('/var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic')
parser=argparse.ArgumentParser(description='R352 image correction preflight; --install replaces only the exact currently installed initramfs')
parser.add_argument('--install',action='store_true');args=parser.parse_args()
if os.geteuid()!=0: raise SystemExit('Run with sudo python3 for protected /boot checks.')
IMAGE=Path('/boot/initramfs-7.2.3-r352-netdiag.img')
ENTRY=Path('/boot/loader/entries/boot-entry-r352-netdiag.conf')
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
 audit=load(OUT/'PACKAGE_AUDIT.json');installed=load(OUT/'INSTALLED_RESULT.json')
 req(audit.get('contract')=='PASS' and audit.get('result')=='CORRECTED_R352_IMAGE_PREPARED_NOT_INSTALLED','corrected R352 package audit not PASS')
 req(audit.get('amdgpu_module_files')==[],'R352 package audit does not confirm amdgpu absent')
 req(sha(OUT/'initramfs-7.2.3-r352-netdiag.img')==audit.get('image_sha256'),'corrected image hash mismatch')
 req(sha(OUT/'boot-entry-r352-netdiag.conf')==audit.get('bls_sha256'),'BLS hash mismatch')
 req(installed.get('contract')=='PASS','previous R352 install result unavailable')
 previous=installed.get('installed_hashes',{}).get(str(IMAGE))
 req(IMAGE.is_file() and not IMAGE.is_symlink() and sha(IMAGE)==previous,'currently installed R352 image differs from recorded hash')
 req(previous!=audit.get('image_sha256'),'corrected image is already installed or hashes are inconsistent')
 req(ENTRY.is_file() and not ENTRY.is_symlink() and sha(ENTRY)==installed.get('installed_hashes',{}).get(str(ENTRY))==audit.get('bls_sha256'),'installed R352 BLS entry mismatch')
 protected=installed.get('protected_hashes',{});actual={}
 for name,expected in protected.items():
  p=Path(name);got=sha(p) if p.is_file() and not p.is_symlink() else None;actual[name]=got;req(got==expected,'protected file changed: '+name)
 e=env();req(e=={'boot_success':'1'},'GRUB env is not normal recovered baseline: '+repr(e))
 req(os.uname().release=='7.2.1-ogc4.1.fc44.x86_64','running kernel is not normal Bazzite')
 ps=Path('/sys/module/efi_pstore/parameters/pstore_disable');req(ps.is_file() and ps.read_text().strip()=='Y','EFI pstore is not restored to Y')
 nw=Path('/proc/sys/kernel/nmi_watchdog');req(nw.read_text().strip()=='1','NMI watchdog is not enabled')
 records={p.name:sha(p) for p in Path('/sys/fs/pstore').iterdir() if p.is_file()};req(not records,'pstore records exist; preserve and review before correcting image')
 fs=os.statvfs('/boot');free=fs.f_bavail*fs.f_frsize;oldsz=IMAGE.stat().st_size if IMAGE.is_file() else 0
 req(free+oldsz>=audit['image_bytes']+MARGIN,'/boot lacks 50 MiB post-replacement margin')
 req(not Path('/boot/vmlinuz-7.2.3-r138').is_symlink(),'unexpected recovery kernel symlink')
 return {'contract':'PASS' if not issues else 'FAIL','issues':issues,'normal_kernel':os.uname().release,'grub_environment_keys':e,'pstore_records_preserved':records,'current_image_sha256':previous,'corrected_image_sha256':audit['image_sha256'],'bls_sha256':sha(ENTRY),'protected_hashes':actual,'grubenv_sha256':sha(ENV),'free_bytes':free,'old_image_bytes':oldsz,'new_image_bytes':audit['image_bytes'],'safety_margin_bytes':MARGIN,'boot_selection_change':False,'reboot':False,'hardware_access':False}
def save(name,data):
 p=OUT/name;p.write_text(json.dumps(data,indent=2)+'\n');os.chown(p,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())));print(json.dumps(data,indent=2))
snapshot=capture()
if not args.install:
 save('CORRECTION_PREFLIGHT_RESULT.json',snapshot);raise SystemExit(0 if snapshot['contract']=='PASS' else 2)
if snapshot['contract']!='PASS':save('CORRECTION_BLOCKED.json',snapshot);raise SystemExit(2)
pre=load(OUT/'CORRECTION_PREFLIGHT_RESULT.json')
if {k:v for k,v in pre.items() if k!='free_bytes'}!={k:v for k,v in snapshot.items() if k!='free_bytes'}:raise SystemExit('Protected state changed since correction preflight.')
backup=OUT/'r352-initial-bad-build-backup'
if backup.exists():raise SystemExit('Correction backup already exists; inspect first.')
backup.mkdir();shutil.copy2(IMAGE,backup/IMAGE.name)
if sha(backup/IMAGE.name)!=snapshot['current_image_sha256']:raise SystemExit('Backup hash mismatch; /boot unchanged.')
os.sync()
def interrupted(signum,frame):raise InterruptedError('R352 correction interrupted')
for s in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(s,interrupted)
removed=False;created=False;tmp=IMAGE.with_name('.'+IMAGE.name+'.r352-fix-tmp')
try:
 IMAGE.unlink();removed=True;os.sync()
 with tmp.open('xb') as dst,(OUT/'initramfs-7.2.3-r352-netdiag.img').open('rb') as src:shutil.copyfileobj(src,dst)
 os.chmod(tmp,0o644)
 if sha(tmp)!=snapshot['corrected_image_sha256']:raise RuntimeError('corrected image temporary hash mismatch')
 os.replace(tmp,IMAGE);created=True;os.sync()
 if sha(ENTRY)!=snapshot['bls_sha256']:raise RuntimeError('BLS entry changed during correction')
 for name,digest in snapshot['protected_hashes'].items():
  if sha(Path(name))!=digest:raise RuntimeError('protected file changed: '+name)
 if sha(ENV)!=snapshot['grubenv_sha256']:raise RuntimeError('GRUB env changed during correction')
 if IMAGE.stat().st_size!=snapshot['new_image_bytes']:raise RuntimeError('corrected image size mismatch')
 remaining=os.statvfs('/boot').f_bavail*os.statvfs('/boot').f_frsize
 if remaining<MARGIN:raise RuntimeError('post-correction /boot margin below 50 MiB')
 out=load(OUT/'INSTALLED_RESULT.json');out['installed_hashes'][str(IMAGE)]=sha(IMAGE);out['protected_hashes']=snapshot['protected_hashes'];out['grubenv_sha256_at_correction']=snapshot['grubenv_sha256'];out['correction_backup']={p.name:sha(p) for p in backup.iterdir()};out['corrected_image_embedded_init']='R352';out['remaining_boot_free_bytes']=remaining;out['contract']='PASS'
 p=OUT/'INSTALLED_RESULT.json';p.write_text(json.dumps(out,indent=2)+'\n');os.chown(p,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())))
 print(json.dumps(out,indent=2))
except BaseException:
 for s in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(s,signal.SIG_IGN)
 if tmp.exists():tmp.unlink()
 if created:IMAGE.unlink()
 if removed or created:shutil.copy2(backup/IMAGE.name,IMAGE);assert sha(IMAGE)==sha(backup/IMAGE.name)
 os.sync();print('R352_CORRECTION_ROLLBACK=RESTORED_PREVIOUS_IMAGE');raise
