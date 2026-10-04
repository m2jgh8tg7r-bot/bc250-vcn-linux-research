"""Read-only R352 installed-state verifier; requires root for protected /boot."""
from pathlib import Path
import hashlib, json, os, subprocess
OUT = Path('/var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic')
if os.geteuid() != 0:
    raise SystemExit('Run with sudo python3 at the protected read-only verification step.')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
    return h.hexdigest()
def env():
    return dict(line.split('=',1) for line in subprocess.check_output(['grub2-editenv','/boot/grub2/grubenv','list'],text=True).splitlines() if '=' in line)
audit=json.loads((OUT/'INSTALLED_RESULT.json').read_text())
assert audit.get('contract')=='PASS'
for path,expected in audit['installed_hashes'].items(): assert sha(Path(path))==expected,'Installed artifact changed: '+path
for path,expected in audit['protected_hashes'].items(): assert sha(Path(path))==expected,'Protected file changed: '+path
expected_env=audit.get('grubenv_sha256_at_correction',audit['grubenv_sha256_at_install'])
assert sha(Path('/boot/grub2/grubenv'))==expected_env,'GRUB environment changed since last install/correction'
e=env(); assert e=={'boot_success':'1'},'GRUB environment is not recovered baseline: '+repr(e)
assert os.uname().release=='7.2.1-ogc4.1.fc44.x86_64'
assert Path('/sys/module/efi_pstore/parameters/pstore_disable').read_text().strip()=='Y'
assert Path('/proc/sys/kernel/nmi_watchdog').read_text().strip()=='1'
assert not Path('/sys/module/netconsole').exists(),'Inspect normal-boot netconsole state before arming.'
records={p.name:sha(p) for p in Path('/sys/fs/pstore').iterdir() if p.is_file()}
assert not records,'Preserve and inspect pstore records before arming: '+','.join(records)
r={'contract':'PASS','installed_hashes':audit['installed_hashes'],'protected_hashes_match':True,'grubenv_sha256':sha(Path('/boot/grub2/grubenv')),'boot_success':'1','pending_boot_override':False,'efi_pstore_currently_disabled':'Y','nmi_watchdog':'1','pstore_records':records,'boot_selection_change':False,'reboot':False,'hardware_access':False}
p=OUT/'VERIFY_RESULT.json';p.write_text(json.dumps(r,indent=2)+'\n');os.chown(p,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())))
print(json.dumps(r,indent=2))
