"""Arm a visible one-time manual GRUB menu for R353; never select or reboot."""
from pathlib import Path
import hashlib,json,os,shutil,signal,subprocess
LIVE=Path('/var/home/kazuyuki/bc250-research/research/r353-vcnstatus-netconsole-guard')
ENV=Path('/boot/grub2/grubenv')
if os.geteuid()!=0: raise SystemExit('Run with sudo after R353 verify_installed.py reports PASS.')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
 return h.hexdigest()
def env(): return dict(x.split('=',1) for x in subprocess.check_output(['grub2-editenv',str(ENV),'list'],text=True).splitlines() if '=' in x)
a=json.loads((LIVE/'INSTALLED_RESULT.json').read_text());v=json.loads((LIVE/'VERIFY_RESULT.json').read_text())
assert a.get('contract')=='PASS' and v.get('contract')=='PASS'
for p,d in a['installed_hashes'].items(): assert sha(p)==d,'R353 artifact changed: '+p
for p,d in a['protected_hashes'].items(): assert sha(p)==d,'Protected artifact changed: '+p
assert sha(ENV)==a['grubenv_sha256_at_install']
assert Path('/sys/module/efi_pstore/parameters/pstore_disable').read_text().strip()=='Y'
assert Path('/proc/sys/kernel/nmi_watchdog').read_text().strip()=='1'
records=[p.name for p in Path('/sys/fs/pstore').iterdir() if p.is_file()];assert not records,'Preserve pstore before arming: '+','.join(records)
assert os.uname().release=='7.2.1-ogc4.1.fc44.x86_64'
assert env()=={'boot_success':'1'},'GRUB not at normal baseline'
assert not Path('/sys/module/netconsole').exists(),'Unexpected normal-boot netconsole state'
backup=LIVE/'grubenv-before-r353-menu.bin';result=LIVE/'MENU_RESULT.json'
assert not backup.exists() and not result.exists(),'R353 menu already armed; inspect state'
shutil.copy2(ENV,backup);os.sync();assert sha(backup)==sha(ENV)
def interrupted(sig,frame): raise InterruptedError('R353 menu arm interrupted')
for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,interrupted)
try:
 subprocess.run(['grub2-editenv',str(ENV),'set','menu_show_once_timeout=30'],check=True);os.sync()
 assert env()=={'boot_success':'1','menu_show_once_timeout':'30'}
 for p,d in a['protected_hashes'].items():assert sha(p)==d,'Protected file changed: '+p
 r={'contract':'PASS','entry':'boot-entry-r353-vcnstatus.conf','manual_selection_required':True,'menu_timeout_seconds':30,'saved_default_unchanged':True,'next_entry_absent':True,'pstore_changed':False,'fresh_grubenv_backup_sha256':sha(backup),'receiver_token_required':'R353-STATUS-READ','boot_selection_change':False,'reboot':False,'hardware_access':False}
 result.write_text(json.dumps(r,indent=2)+'\n');os.chown(result,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())));print(json.dumps(r,indent=2))
except BaseException:
 for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,signal.SIG_IGN)
 shutil.copy2(backup,ENV);os.sync();assert sha(ENV)==sha(backup);result.unlink(missing_ok=True);print('GRUBENV_RESTORED=YES');raise
