"""Read-only check of the installed R353 artifacts and boot safety invariants."""
from pathlib import Path
import hashlib,json,os,subprocess
LIVE=Path('/var/home/kazuyuki/bc250-research/research/r353-vcnstatus-netconsole-guard')
if os.geteuid()!=0: raise SystemExit('Run with sudo for read-only protected /boot verification.')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
 return h.hexdigest()
a=json.loads((LIVE/'INSTALLED_RESULT.json').read_text()); assert a.get('contract')=='PASS'
for p,d in a['installed_hashes'].items(): assert sha(p)==d,'Installed artifact changed: '+p
for p,d in a['protected_hashes'].items(): assert sha(p)==d,'Protected artifact changed: '+p
e=dict(x.split('=',1) for x in subprocess.check_output(['grub2-editenv','/boot/grub2/grubenv','list'],text=True).splitlines() if '=' in x)
assert e=={'boot_success':'1'},'GRUB environment not clean baseline'
assert os.uname().release=='7.2.1-ogc4.1.fc44.x86_64'
assert Path('/sys/module/efi_pstore/parameters/pstore_disable').read_text().strip()=='Y'
assert Path('/proc/sys/kernel/nmi_watchdog').read_text().strip()=='1'
records=[p.name for p in Path('/sys/fs/pstore').iterdir() if p.is_file()]; assert not records,'Preserve pstore records: '+','.join(records)
r={'contract':'PASS','installed_hashes':a['installed_hashes'],'protected_hashes_match':True,'boot_success':'1','pending_boot_override':False,'efi_pstore_currently_disabled':'Y','nmi_watchdog':'1','pstore_records':{},'boot_selection_change':False,'reboot':False,'hardware_access':False}
p=LIVE/'VERIFY_RESULT.json';p.write_text(json.dumps(r,indent=2)+'\n');os.chown(p,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())))
print(json.dumps(r,indent=2))
