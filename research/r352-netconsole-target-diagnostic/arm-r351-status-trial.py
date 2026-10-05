"""Arm a visible manual GRUB menu for the token-gated single R351 STATUS read."""
from pathlib import Path
import hashlib,json,os,shutil,signal,subprocess
OUT=Path('/var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic');ENV=Path('/boot/grub2/grubenv')
if os.geteuid()!=0:raise SystemExit('Run with sudo python3 after R351 trial verification PASS.')
if os.uname().release!='7.2.1-ogc4.1.fc44.x86_64':raise SystemExit('Expected normal Bazzite kernel.')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def env():return dict(line.split('=',1) for line in subprocess.check_output(['grub2-editenv',str(ENV),'list'],text=True).splitlines() if '=' in line)
a=json.loads((OUT/'R351_TRIAL_INSTALL_RESULT.json').read_text());v=json.loads((OUT/'R351_TRIAL_VERIFY_RESULT.json').read_text());assert a.get('contract')=='PASS' and v.get('contract')=='PASS'
for n,d in a['installed_hashes'].items():assert sha(Path(n))==d,'R351 artifact changed: '+n
for n,d in a['protected_hashes'].items():assert sha(Path(n))==d,'Protected file changed: '+n
assert v.get('protected_hashes_match') is True and sha(ENV)==a['grubenv_sha256_at_install']
assert Path('/sys/module/efi_pstore/parameters/pstore_disable').read_text().strip()=='Y'
assert Path('/proc/sys/kernel/nmi_watchdog').read_text().strip()=='1'
assert not Path('/sys/module/netconsole').exists(),'Inspect normal-boot netconsole before arming.'
records=[p.name for p in Path('/sys/fs/pstore').iterdir() if p.is_file()];assert not records,'Preserve pstore records before arming: '+','.join(records)
before=env();assert before=={'boot_success':'1'},'GRUB environment not at baseline: '+repr(before)
backup=OUT/'grubenv-before-r351-vcn-trial-menu.bin';result=OUT/'R351_TRIAL_MENU_RESULT.json';assert not backup.exists() and not result.exists(),'R351 trial menu already armed; inspect.'
shutil.copy2(ENV,backup);os.sync();assert sha(backup)==sha(ENV)
def interrupted(signum,frame):raise InterruptedError('R351 trial menu arming interrupted')
for s in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(s,interrupted)
try:
 subprocess.run(['grub2-editenv',str(ENV),'set','menu_show_once_timeout=30'],check=True);os.sync();after=env();assert after=={**before,'menu_show_once_timeout':'30'}
 for n,d in a['protected_hashes'].items():assert sha(Path(n))==d,'Protected file changed: '+n
 r={'contract':'PASS','entry':'boot-entry-r351-statusread.conf','manual_selection_required':True,'menu_timeout_seconds':30,'saved_default_unchanged':True,'next_entry_absent':True,'pstore_changed':False,'fresh_grubenv_backup_sha256':sha(backup),'receiver_token_required':'R351-STATUS-READ','boot_selection_change':False,'reboot':False,'hardware_access':False}
 result.write_text(json.dumps(r,indent=2)+'\n');os.chown(result,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())));print(json.dumps(r,indent=2))
except BaseException:
 for s in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(s,signal.SIG_IGN)
 shutil.copy2(backup,ENV);os.sync();assert sha(ENV)==sha(backup);result.unlink(missing_ok=True);print('GRUBENV_RESTORED=YES');raise
