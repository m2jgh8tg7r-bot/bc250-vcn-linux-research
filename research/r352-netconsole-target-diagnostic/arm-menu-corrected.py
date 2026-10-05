"""Arm a fresh visible GRUB menu for the corrected R352 image; no reboot."""
from pathlib import Path
import hashlib,json,os,shutil,signal,subprocess
OUT=Path('/var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic');ENV=Path('/boot/grub2/grubenv')
if os.geteuid()!=0:raise SystemExit('Run with sudo python3 after corrected R352 verification PASS.')
if os.uname().release!='7.2.1-ogc4.1.fc44.x86_64':raise SystemExit('Expected normal Bazzite kernel.')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def env():return dict(line.split('=',1) for line in subprocess.check_output(['grub2-editenv',str(ENV),'list'],text=True).splitlines() if '=' in line)
installed=json.loads((OUT/'INSTALLED_RESULT.json').read_text());verified=json.loads((OUT/'VERIFY_RESULT.json').read_text())
assert installed.get('contract')=='PASS' and installed.get('corrected_image_embedded_init')=='R352','Corrected R352 install missing.'
assert verified.get('contract')=='PASS' and verified.get('protected_hashes_match') is True,'Corrected R352 verification not PASS.'
for name,expected in installed['installed_hashes'].items():assert sha(Path(name))==expected,'R352 artifact changed: '+name
for name,expected in installed['protected_hashes'].items():assert sha(Path(name))==expected,'Protected file changed: '+name
expected_env=installed.get('grubenv_sha256_at_correction',installed['grubenv_sha256_at_install'])
assert sha(ENV)==expected_env,'GRUB environment changed since corrected install verification.'
assert Path('/sys/module/efi_pstore/parameters/pstore_disable').read_text().strip()=='Y'
assert Path('/proc/sys/kernel/nmi_watchdog').read_text().strip()=='1','Enable kernel.nmi_watchdog=1 then retry.'
assert not Path('/sys/module/netconsole').exists(),'Inspect normal-boot netconsole state before arming.'
records=[p.name for p in Path('/sys/fs/pstore').iterdir() if p.is_file()];assert not records,'Preserve pstore records before arming: '+','.join(records)
before=env();assert before=={'boot_success':'1'},'GRUB environment is not baseline: '+repr(before)
backup=OUT/'grubenv-before-r352-corrected-menu.bin';result_path=OUT/'MENU_CORRECTED_RESULT.json'
assert not backup.exists() and not result_path.exists(),'Corrected R352 menu arm already recorded; inspect before continuing.'
shutil.copy2(ENV,backup);os.sync();assert sha(backup)==sha(ENV)
def interrupted(signum,frame):raise InterruptedError('Corrected R352 menu arming interrupted')
for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,interrupted)
try:
 subprocess.run(['grub2-editenv',str(ENV),'set','menu_show_once_timeout=30'],check=True);os.sync()
 after=env();assert after=={**before,'menu_show_once_timeout':'30'}
 for name,expected in installed['protected_hashes'].items():assert sha(Path(name))==expected,'Protected file changed: '+name
 result={'contract':'PASS','entry':'boot-entry-r352-netdiag.conf','corrected_image_embedded_init':'R352','manual_selection_required':True,'menu_timeout_seconds':30,'saved_default_unchanged':True,'next_entry_absent':True,'pstore_changed':False,'fresh_grubenv_backup_sha256':sha(backup),'boot_selection_change':False,'reboot':False,'hardware_access':False}
 result_path.write_text(json.dumps(result,indent=2)+'\n');os.chown(result_path,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())))
 print(json.dumps(result,indent=2))
except BaseException:
 for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,signal.SIG_IGN)
 shutil.copy2(backup,ENV);os.sync();assert sha(ENV)==sha(backup);result_path.unlink(missing_ok=True);print('GRUBENV_RESTORED=YES');raise
