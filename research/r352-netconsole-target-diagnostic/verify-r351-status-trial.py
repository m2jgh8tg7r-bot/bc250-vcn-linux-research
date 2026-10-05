"""Read-only verification after exact backed-up R351 image is restored."""
from pathlib import Path
import hashlib,json,os,subprocess
OUT=Path('/var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic');ENV=Path('/boot/grub2/grubenv')
if os.geteuid()!=0:raise SystemExit('Run with sudo python3 for protected /boot verification.')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def env():return dict(line.split('=',1) for line in subprocess.check_output(['grub2-editenv',str(ENV),'list'],text=True).splitlines() if '=' in line)
a= json.loads((OUT/'R351_TRIAL_INSTALL_RESULT.json').read_text());assert a.get('contract')=='PASS'
for n,d in a['installed_hashes'].items():assert sha(Path(n))==d,'Installed R351 artifact changed: '+n
for n,d in a['protected_hashes'].items():assert sha(Path(n))==d,'Protected file changed: '+n
assert sha(ENV)==a['grubenv_sha256_at_install'],'GRUB environment changed since R351 trial install'
e=env();assert e=={'boot_success':'1'},'GRUB is not at recovered baseline: '+repr(e)
assert os.uname().release=='7.2.1-ogc4.1.fc44.x86_64'
assert Path('/sys/module/efi_pstore/parameters/pstore_disable').read_text().strip()=='Y'
assert Path('/proc/sys/kernel/nmi_watchdog').read_text().strip()=='1'
assert not Path('/sys/module/netconsole').exists(),'Inspect normal-boot netconsole before menu arming.'
records={p.name:sha(p) for p in Path('/sys/fs/pstore').iterdir() if p.is_file()};assert not records,'Preserve pstore before arming: '+','.join(records)
r={'contract':'PASS','installed_hashes':a['installed_hashes'],'protected_hashes_match':True,'grubenv_sha256':sha(ENV),'boot_success':'1','pending_boot_override':False,'efi_pstore_currently_disabled':'Y','nmi_watchdog':'1','pstore_records':records,'boot_selection_change':False,'reboot':False,'hardware_access':False}
p=OUT/'R351_TRIAL_VERIFY_RESULT.json';p.write_text(json.dumps(r,indent=2)+'\n');os.chown(p,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())));print(json.dumps(r,indent=2))
