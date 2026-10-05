"""R353 protected preflight; --install replaces only the exact prior R351 trial."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, signal, subprocess
from boot_default import check_default

OUT = Path(__file__).resolve().parent
LIVE = Path('/var/home/kazuyuki/bc250-research/research/r353-vcnstatus-netconsole-guard')
OLD = Path('/var/home/kazuyuki/bc250-research/research/r351-vcn-status-read-observation')
EXPECTED_KERNEL = '7.2.1-ogc4.1.fc44.x86_64'
OLD_IMAGE = Path('/boot/initramfs-7.2.3-r351-statusread.img')
OLD_ENTRY = Path('/boot/loader/entries/boot-entry-r351-statusread.conf')
NEW_IMAGE = Path('/boot/initramfs-7.2.3-r353-vcnstatus.img')
NEW_ENTRY = Path('/boot/loader/entries/boot-entry-r353-vcnstatus.conf')
GRUBENV = Path('/boot/grub2/grubenv')
MARGIN = 50 * 1024 * 1024
parser = argparse.ArgumentParser()
parser.add_argument('--install', action='store_true')
args = parser.parse_args()
if os.geteuid() != 0:
    raise SystemExit('Root required for protected /boot and GRUB preflight.')

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def env():
    return dict(line.split('=', 1) for line in subprocess.check_output(
        ['grub2-editenv', str(GRUBENV), 'list'], text=True).splitlines() if '=' in line)

def digest_map(paths):
    return {str(p): sha(p) if p.is_file() else None for p in paths}

def capture():
    issues = []
    def req(ok, message):
        if not ok: issues.append(message)
    pkg = json.loads((LIVE / 'PACKAGE_AUDIT.json').read_text())
    req(pkg.get('contract') == 'PASS' and pkg.get('result') == 'HOME_PACKAGE_PREPARED_NOT_INSTALLED', 'R353 package audit not PASS')
    for rel, key in [('initramfs-7.2.3-r353-vcnstatus.img','image_sha256'),('boot-entry-r353-vcnstatus.conf','bls_sha256'),('init','init_sha256')]:
        req((LIVE / rel).is_file() and sha(LIVE / rel) == pkg.get(key), 'R353 artifact hash mismatch: ' + rel)
module = LIVE / pkg['amdgpu_module_path']
    req(module.is_file() and sha(module) == pkg['amdgpu_module_sha256'], 'embedded R351 amdgpu module mismatch')
    old_audit = json.loads((OLD / 'INSTALLED_RESULT.json').read_text())
    req(old_audit.get('contract') == 'PASS', 'prior R351 installation record absent or not PASS')
    req(OLD_IMAGE.is_file() and sha(OLD_IMAGE) == old_audit['installed_hashes'].get(str(OLD_IMAGE)), 'live R351 image differs from recorded trial image')
    req(OLD_ENTRY.is_file() and sha(OLD_ENTRY) == old_audit['installed_hashes'].get(str(OLD_ENTRY)), 'live R351 BLS differs from recorded trial entry')
    actual_protected = {}
    for name, expected in old_audit.get('protected_hashes', {}).items():
        actual = sha(name) if Path(name).is_file() else None
        actual_protected[name] = actual
        if name != str(GRUBENV): req(actual == expected, 'protected file changed: ' + name)
    e = env()
    req(e == {'boot_success':'1'}, 'GRUB environment is not clean normal-boot baseline')
    req(os.uname().release == EXPECTED_KERNEL, 'not running expected normal Bazzite kernel')
    ps = Path('/sys/module/efi_pstore/parameters/pstore_disable')
    req(ps.is_file() and ps.read_text().strip() == 'Y', 'EFI pstore normal policy is not Y')
    req(Path('/proc/sys/kernel/nmi_watchdog').read_text().strip() == '1', 'NMI watchdog is not enabled')
    records = {p.name: sha(p) for p in Path('/sys/fs/pstore').iterdir() if p.is_file()}
    req(not records, 'pstore records must be preserved and reviewed before replacement')
    req(not NEW_IMAGE.exists() and not NEW_ENTRY.exists(), 'R353 destination already exists')
    before = {p.name:p.read_text() for p in Path('/boot/loader/entries').glob('*.conf')}
    req(OLD_ENTRY.name in before, 'current R351 BLS entry missing')
    after = {k:v for k,v in before.items() if k != OLD_ENTRY.name}
    after[NEW_ENTRY.name] = (LIVE/'boot-entry-r353-vcnstatus.conf').read_text()
    include_state = json.loads((OLD/'PREFLIGHT_RESULT.json').read_text())['include_state']
    includes = {}
    for name, expected in include_state.items():
        p = Path('/boot/grub2') / name
        actual = sha(p) if p.is_file() else None
        req(not p.is_symlink() and actual == expected, 'GRUB include changed: ' + name)
        includes[name] = p.read_text() if p.is_file() else None
    try:
        default = check_default(e, Path('/boot/grub2/grub.cfg').read_text(), before, after, includes)
    except Exception as ex:
        default = None
        issues.append('GRUB default/layout check failed: ' + str(ex))
    free = os.statvfs('/boot').f_bavail * os.statvfs('/boot').f_frsize
    old_size = OLD_IMAGE.stat().st_size if OLD_IMAGE.is_file() else 0
    req(free + old_size >= pkg['image_size_bytes'] + MARGIN, '/boot would have less than 50 MiB free margin')
    req(Path('/boot/vmlinuz-7.2.3-r138').is_file(), 'R138 recovery kernel missing')
    return {'contract':'PASS' if not issues else 'FAIL', 'issues':issues,
            'normal_kernel':os.uname().release, 'nmi_watchdog':'1', 'efi_pstore_disable':'Y',
            'grub_environment':e, 'default_check':default, 'protected_hashes':{k:v for k,v in actual_protected.items() if k != str(GRUBENV)},
            'grubenv_sha256':sha(GRUBENV), 'pstore_records':records,
            'old_installed':digest_map((OLD_IMAGE,OLD_ENTRY)), 'include_state':include_state,
            'free_bytes':free, 'old_image_bytes':old_size, 'new_image_bytes':pkg['image_size_bytes'],
            'safety_margin_bytes':MARGIN, 'r353_hashes':{'image':pkg['image_sha256'],'entry':pkg['bls_sha256']},
            'boot_selection_change':False,'reboot':False,'hardware_access':False}

def save(name, data):
    p=LIVE/name; p.write_text(json.dumps(data,indent=2)+'\n')
    os.chown(p,int(os.environ.get('SUDO_UID',os.getuid())),int(os.environ.get('SUDO_GID',os.getgid())))
    print(json.dumps(data,indent=2))

state=capture()
if not args.install:
    save('PREFLIGHT_RESULT.json',state)
    raise SystemExit(0 if state['contract']=='PASS' else 2)
if state['contract']!='PASS':
    save('INSTALL_BLOCKED.json',state); raise SystemExit(2)
pre=json.loads((LIVE/'PREFLIGHT_RESULT.json').read_text())
if {k:v for k,v in pre.items() if k!='free_bytes'} != {k:v for k,v in state.items() if k!='free_bytes'}:
    raise SystemExit('Protected state changed after preflight; rerun and review read-only check.')
backup=LIVE/'r351-statusread-retirement-backup'
if backup.exists(): raise SystemExit('R351 retirement backup already exists; inspect before proceeding.')
backup.mkdir()
for src in (OLD_IMAGE,OLD_ENTRY): shutil.copy2(src,backup/src.name)
for src in (OLD_IMAGE,OLD_ENTRY):
    if sha(backup/src.name)!=state['old_installed'][str(src)]: raise SystemExit('R351 backup hash mismatch')
os.sync(); removed=[]; created=[]; temps=[]
def interrupted(sig,frame): raise InterruptedError('R353 install interrupted')
for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP): signal.signal(sig,interrupted)
try:
    OLD_ENTRY.unlink(); removed.append(OLD_ENTRY); os.sync()
    OLD_IMAGE.unlink(); removed.append(OLD_IMAGE); os.sync()
    for src,dst,key in ((LIVE/'initramfs-7.2.3-r353-vcnstatus.img',NEW_IMAGE,'image'),(LIVE/'boot-entry-r353-vcnstatus.conf',NEW_ENTRY,'entry')):
        tmp=dst.with_name('.'+dst.name+'.r353-tmp')
        if tmp.exists(): raise RuntimeError('unexpected temporary file: '+str(tmp))
        temps.append(tmp)
        with src.open('rb') as fsrc,tmp.open('xb') as fdst: shutil.copyfileobj(fsrc,fdst)
        os.chmod(tmp,0o644)
        expected=state['r353_hashes'][key]
        if sha(tmp)!=expected: raise RuntimeError('R353 hash mismatch: '+str(tmp))
        os.replace(tmp,dst); temps.remove(tmp); created.append(dst); os.sync()
    for name,digest in state['protected_hashes'].items():
        if sha(name)!=digest: raise RuntimeError('protected file changed: '+name)
    if sha(GRUBENV)!=state['grubenv_sha256']: raise RuntimeError('GRUB environment changed')
    remain=os.statvfs('/boot').f_bavail*os.statvfs('/boot').f_frsize
    if remain<MARGIN: raise RuntimeError('post-install boot margin below 50 MiB')
    save('INSTALLED_RESULT.json',{'contract':'PASS','installed_hashes':{str(NEW_IMAGE):sha(NEW_IMAGE),str(NEW_ENTRY):sha(NEW_ENTRY)},
         'protected_hashes':state['protected_hashes'],'grubenv_sha256_at_install':state['grubenv_sha256'],
         'r351_retirement_backup':{p.name:sha(p) for p in backup.iterdir()},'boot_selection_change':False,
         'module_load':False,'reboot':False,'hardware_access':False,'remaining_boot_free_bytes':remain})
except BaseException:
    for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP): signal.signal(sig,signal.SIG_IGN)
    for p in created+temps: p.unlink(missing_ok=True)
    for src,dst in ((backup/OLD_IMAGE.name,OLD_IMAGE),(backup/OLD_ENTRY.name,OLD_ENTRY)):
        if src.exists(): shutil.copy2(src,dst); assert sha(src)==sha(dst)
    os.sync(); print('R353_INSTALL_ROLLBACK=RESTORED_R351'); raise
