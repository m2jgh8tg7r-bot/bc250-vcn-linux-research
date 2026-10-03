"""Read-only independent installed-file audit; no module load or boot selection."""
from pathlib import Path
import hashlib,json,os,subprocess
out=Path(__file__).resolve().parent
assert os.geteuid()==0,'sudo required for protected boot audit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((out/'INSTALLED_RESULT.json').read_text());assert a['contract']=='PASS'
p=json.loads((out/'PREFLIGHT_RESULT.json').read_text())
for n,h in {**a['installed_hashes'],**a['protected_hashes']}.items():assert sha(Path(n))==h,'Changed artifact: '+n
for n,h in p['old_hashes'].items():
 assert not Path(n).exists(),'Old boot artifact still present'
 assert sha(out/'r318-retirement-backup'/Path(n).name)==h,'Retirement backup mismatch'
e=dict(line.split('=',1) for line in subprocess.check_output(['grub2-editenv','/boot/grub2/grubenv','list'],text=True).splitlines() if '=' in line)
assert e.get('boot_success')=='1'
assert not any(n in e for n in ['next_entry','menu_show_once','menu_show_once_timeout'])
for n,h in p['include_state'].items():
 q=Path('/boot/grub2')/n;assert not q.is_symlink()
 assert (sha(q) if q.is_file() else None)==h
assert os.uname().release=='7.2.1-ogc4.1.fc44.x86_64'
result={'contract':'PASS','installed_files_exact':True,'protected_files_unchanged':True,'retirement_backup_verified':True,'normal_kernel_unchanged':True,'boot_selection_change':False,'module_load':False,'reboot':False}
q=out/'INSTALLED_INDEPENDENT_AUDIT.json';q.write_text(json.dumps(result,indent=2)+'\n');os.chown(q,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())));print(json.dumps(result,indent=2))
