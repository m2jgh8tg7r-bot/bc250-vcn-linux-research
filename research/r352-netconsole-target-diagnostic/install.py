"""R352 read-only preflight by default; --install replaces only exact R351 files."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, signal, subprocess, sys

OUT = Path('/var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic')
R351 = Path('/var/home/kazuyuki/bc250-research/research/r351-vcn-status-read-observation')
sys.path.insert(0, str(R351))
from boot_default import check_default

parser = argparse.ArgumentParser(description='R352 protected /boot preflight; --install replaces only exact R351 files')
parser.add_argument('--install', action='store_true')
args = parser.parse_args()
if os.geteuid() != 0:
    raise SystemExit('Root required for protected read-only /boot and GRUB preflight; do not run unless operator is at the approved sudo boundary.')

EXPECTED_KERNEL = '7.2.1-ogc4.1.fc44.x86_64'
OLD_IMAGE = Path('/boot/initramfs-7.2.3-r351-statusread.img')
OLD_ENTRY = Path('/boot/loader/entries/boot-entry-r351-statusread.conf')
NEW_IMAGE = Path('/boot/initramfs-7.2.3-r352-netdiag.img')
NEW_ENTRY = Path('/boot/loader/entries/boot-entry-r352-netdiag.conf')
GRUBENV = Path('/boot/grub2/grubenv')
MARGIN = 50 * 1024 * 1024

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def load(path):
    return json.loads(path.read_text())

def env():
    return dict(line.split('=', 1) for line in subprocess.check_output(
        ['grub2-editenv', str(GRUBENV), 'list'], text=True).splitlines() if '=' in line)

def capture():
    issues = []
    def req(ok, message):
        if not ok:
            issues.append(message)
    audit = load(OUT / 'PACKAGE_AUDIT.json')
    req(audit.get('contract') == 'PASS' and audit.get('result') == 'OFFLINE_DIAGNOSTIC_IMAGE_PREPARED_NOT_INSTALLED', 'R352 package audit is not PASS')
    req(audit.get('amdgpu_module_files') == [], 'R352 audit does not prove amdgpu is absent')
    req(sha(OUT / 'initramfs-7.2.3-r352-netdiag.img') == audit.get('image_sha256'), 'R352 image hash mismatch')
    req(sha(OUT / 'boot-entry-r352-netdiag.conf') == audit.get('bls_sha256'), 'R352 BLS hash mismatch')
    req(sha(OUT / 'init') == audit.get('init_sha256'), 'R352 init hash mismatch')
    req(not NEW_IMAGE.exists() and not NEW_ENTRY.exists(), 'R352 target already exists in /boot; inspect before continuing')
    old_installed = load(R351 / 'INSTALLED_RESULT.json')
    req(old_installed.get('contract') == 'PASS', 'R351 installed audit is not PASS')
    req(OLD_IMAGE.is_file() and not OLD_IMAGE.is_symlink() and sha(OLD_IMAGE) == old_installed.get('installed_hashes', {}).get(str(OLD_IMAGE)), 'installed R351 image differs from its recorded exact hash')
    req(OLD_ENTRY.is_file() and not OLD_ENTRY.is_symlink() and sha(OLD_ENTRY) == old_installed.get('installed_hashes', {}).get(str(OLD_ENTRY)), 'installed R351 BLS entry differs from its recorded exact hash')
    actual_protected = {}
    for name, expected in old_installed.get('protected_hashes', {}).items():
        path = Path(name)
        actual = sha(path) if path.is_file() and not path.is_symlink() else None
        actual_protected[name] = actual
        req(actual == expected, 'protected file changed or unexpected symlink: ' + name)
    environment = env()
    req(environment.get('boot_success') == '1', 'GRUB does not report successful normal boot')
    req(not any(k in environment for k in ('next_entry', 'menu_show_once', 'menu_show_once_timeout')), 'GRUB has pending one-shot/menu override')
    req(os.uname().release == EXPECTED_KERNEL, 'running kernel is not the expected normal kernel')
    pstore_setting = Path('/sys/module/efi_pstore/parameters/pstore_disable')
    req(pstore_setting.is_file() and pstore_setting.read_text().strip() == 'Y', 'normal EFI pstore policy is not restored to Y')
    req(Path('/proc/sys/kernel/nmi_watchdog').read_text().strip() == '1', 'normal NMI watchdog is not enabled')
    req(not Path('/sys/fs/pstore').is_symlink(), 'unexpected pstore path type')
    pstore_records = {p.name: sha(p) for p in Path('/sys/fs/pstore').iterdir() if p.is_file()}
    req(not pstore_records, 'pstore is not empty; preserve and review records before proceeding')
    before = {p.name: text for p in Path('/boot/loader/entries').glob('*.conf') if not p.is_symlink() for text in [p.read_text()]}
    req(OLD_ENTRY.name in before, 'installed R351 BLS entry missing')
    after = {name: text for name, text in before.items() if name != OLD_ENTRY.name}
    after[NEW_ENTRY.name] = (OUT / 'boot-entry-r352-netdiag.conf').read_text()
    cfg = Path('/boot/grub2/grub.cfg').read_text()
    incl_state = load(R351 / 'PREFLIGHT_RESULT.json')['include_state']
    includes = {}
    for name, expected in incl_state.items():
        path = Path('/boot/grub2') / name
        req(not path.is_symlink(), 'unexpected GRUB include symlink: ' + name)
        actual = sha(path) if path.is_file() else None
        req(actual == expected, 'GRUB include changed: ' + name)
        includes[name] = path.read_text() if path.is_file() else None
    try:
        default = check_default(environment, cfg, before, after, includes)
    except Exception as exc:
        default = None
        issues.append('GRUB default/layout check failed: ' + str(exc))
    fs = os.statvfs('/boot')
    free = fs.f_bavail * fs.f_frsize
    old_size = OLD_IMAGE.stat().st_size if OLD_IMAGE.is_file() else 0
    req(free + old_size >= audit['image_bytes'] + MARGIN, '/boot lacks 50 MiB margin after exact R351 replacement')
    req(Path('/boot/vmlinuz-7.2.3-r138').is_file(), 'retained R138 recovery kernel is missing')
    req(not Path('/boot/initramfs-7.2.3-r180-observation.img').is_symlink(), 'unexpected R180 recovery image symlink')
    return {
        'contract': 'PASS' if not issues else 'FAIL', 'issues': issues,
        'normal_kernel': os.uname().release, 'running_nmi_watchdog': Path('/proc/sys/kernel/nmi_watchdog').read_text().strip(),
        'efi_pstore_disable': pstore_setting.read_text().strip() if pstore_setting.is_file() else None,
        'grub_environment_keys': {k: environment.get(k) for k in ('boot_success','saved_entry','next_entry','menu_show_once','menu_show_once_timeout') if k in environment},
        'default_check': default, 'protected_hashes': actual_protected,
        'grubenv_sha256': sha(GRUBENV), 'pstore_records_preserved': pstore_records,
        'old_installed': {str(OLD_IMAGE): sha(OLD_IMAGE) if OLD_IMAGE.is_file() else None, str(OLD_ENTRY): sha(OLD_ENTRY) if OLD_ENTRY.is_file() else None},
        'include_state': incl_state, 'free_bytes': free, 'old_image_bytes': old_size,
        'new_image_bytes': audit['image_bytes'], 'safety_margin_bytes': MARGIN,
        'r352_hashes': {'image': audit['image_sha256'], 'entry': audit['bls_sha256']},
        'boot_selection_change': False, 'reboot': False, 'hardware_access': False,
    }

def save(name, data):
    path = OUT / name
    path.write_text(json.dumps(data, indent=2) + '\n')
    uid = int(os.environ.get('SUDO_UID', os.getuid()))
    gid = int(os.environ.get('SUDO_GID', os.getgid()))
    os.chown(path, uid, gid)
    print(json.dumps(data, indent=2))

snapshot = capture()
if not args.install:
    save('PREFLIGHT_RESULT.json', snapshot)
    raise SystemExit(0 if snapshot['contract'] == 'PASS' else 2)
if snapshot['contract'] != 'PASS':
    save('INSTALL_BLOCKED.json', snapshot)
    raise SystemExit(2)
pre = load(OUT / 'PREFLIGHT_RESULT.json')
if {k:v for k,v in pre.items() if k != 'free_bytes'} != {k:v for k,v in snapshot.items() if k != 'free_bytes'}:
    raise SystemExit('Protected state changed since preflight; rerun read-only preflight and review.')
backup = OUT / 'r351-retirement-backup'
if backup.exists():
    raise SystemExit('R351 retirement backup already exists; inspect before continuing.')
backup.mkdir()
for src in (OLD_IMAGE, OLD_ENTRY):
    shutil.copy2(src, backup / src.name)
for src in (OLD_IMAGE, OLD_ENTRY):
    if sha(backup / src.name) != snapshot['old_installed'][str(src)]:
        raise SystemExit('R351 local retirement backup mismatch; no boot files changed.')
(OUT / 'grubenv-before-r352-install.bin').write_bytes(GRUBENV.read_bytes())
os.sync()
def interrupted(signum, frame):
    raise InterruptedError('R352 installation interrupted')
for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(sig, interrupted)
removed, created, temps = [], [], []
try:
    OLD_ENTRY.unlink(); removed.append(OLD_ENTRY); os.sync()
    OLD_IMAGE.unlink(); removed.append(OLD_IMAGE); os.sync()
    for src, dst, expected in ((OUT / 'initramfs-7.2.3-r352-netdiag.img', NEW_IMAGE, snapshot['r352_hashes']['image']), (OUT / 'boot-entry-r352-netdiag.conf', NEW_ENTRY, snapshot['r352_hashes']['entry'])):
        tmp = dst.with_name('.' + dst.name + '.r352-tmp')
        if tmp.exists():
            raise RuntimeError('unexpected temporary target: ' + str(tmp))
        temps.append(tmp)
        with tmp.open('xb') as target, src.open('rb') as source:
            shutil.copyfileobj(source, target)
        os.chmod(tmp, 0o644)
        if sha(tmp) != expected:
            raise RuntimeError('new file hash mismatch: ' + str(tmp))
        os.replace(tmp, dst); temps.remove(tmp); created.append(dst); os.sync()
    for name, digest in snapshot['protected_hashes'].items():
        if sha(Path(name)) != digest:
            raise RuntimeError('protected file changed: ' + name)
    if sha(GRUBENV) != snapshot['grubenv_sha256']:
        raise RuntimeError('GRUB environment changed during R352 install')
    if NEW_IMAGE.stat().st_size != snapshot['new_image_bytes']:
        raise RuntimeError('installed R352 image size mismatch')
    remaining = os.statvfs('/boot').f_bavail * os.statvfs('/boot').f_frsize
    if remaining < MARGIN:
        raise RuntimeError('post-install /boot margin fell below 50 MiB')
    save('INSTALLED_RESULT.json', {
        'contract':'PASS','installed_hashes':{str(NEW_IMAGE):sha(NEW_IMAGE),str(NEW_ENTRY):sha(NEW_ENTRY)},
        'protected_hashes':snapshot['protected_hashes'],'grubenv_sha256_at_install':snapshot['grubenv_sha256'],
        'r351_retirement_backup':{p.name:sha(p) for p in backup.iterdir()},
        'boot_selection_change':False,'module_load':False,'reboot':False,'hardware_access':False,
        'remaining_boot_free_bytes':remaining,
    })
except BaseException:
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, signal.SIG_IGN)
    for path in created:
        path.unlink(missing_ok=True)
    for path in temps:
        path.unlink(missing_ok=True)
    for src, dst in ((backup / OLD_IMAGE.name, OLD_IMAGE), (backup / OLD_ENTRY.name, OLD_ENTRY)):
        if src.exists():
            shutil.copy2(src, dst)
            assert sha(dst) == sha(src)
    os.sync()
    print('R352_INSTALL_ROLLBACK=RESTORED_R351')
    raise
