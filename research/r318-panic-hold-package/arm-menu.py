from pathlib import Path
import hashlib, json, os, signal, subprocess

out = Path(__file__).resolve().parent
assert os.geteuid() == 0, 'Run with sudo python3'
assert os.uname().release == '7.2.1-ogc4.1.fc44.x86_64'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def env(): return dict(line.split('=', 1) for line in subprocess.check_output(['grub2-editenv', '/boot/grub2/grubenv', 'list'], text=True).splitlines() if '=' in line)
audit = json.loads((out / 'INSTALLED_RESULT.json').read_text()); assert audit['contract'] == 'PASS'
for path, h in {**audit['installed_hashes'], **audit['protected_hashes']}.items(): assert sha(Path(path)) == h, 'State changed: ' + path
preflight = json.loads((out / 'PREFLIGHT_RESULT.json').read_text())
for name, expected in preflight['include_state'].items():
    path = Path('/boot/grub2') / name
    assert not path.is_symlink(), 'Include symlink appeared'
    assert (sha(path) if path.is_file() else None) == expected, 'Include state changed'
before = env(); assert before.get('boot_success') == '1'
assert not any(k in before for k in ('next_entry', 'menu_show_once', 'menu_show_once_timeout'))
assert Path('/sys/module/efi_pstore/parameters/pstore_disable').read_text().strip() == 'Y'
config = Path('/boot/grub2/grub.cfg').read_text()
assert 'if [ "${menu_show_once_timeout}" ]; then' in config and 'unset menu_show_once_timeout' in config
grubenv = Path('/boot/grub2/grubenv')
backup = out / 'grubenv-before-r318-menu.bin'; assert not backup.exists(), 'Menu already prepared; inspect before repeating'
backup.write_bytes(grubenv.read_bytes()); os.sync(); assert sha(backup) == sha(grubenv)
def interrupted(signum, frame): raise InterruptedError('Menu preparation interrupted')
for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP): signal.signal(sig, interrupted)
try:
    subprocess.run(['grub2-editenv', str(grubenv), 'set', 'menu_show_once_timeout=30'], check=True)
    os.sync(); assert env() == {**before, 'menu_show_once_timeout': '30'}
    assert all(sha(Path(p)) == h for p, h in audit['protected_hashes'].items() if p != str(grubenv))
    result = {'contract': 'PASS', 'manual_selection_required': True, 'next_entry_absent': True, 'menu_timeout': 30, 'pstore_changed': False, 'reboot': False, 'hardware_access': False}
    (out / 'MENU_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
except BaseException:
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP): signal.signal(sig, signal.SIG_IGN)
    grubenv.write_bytes(backup.read_bytes()); os.sync(); assert sha(grubenv) == sha(backup)
    print('GRUBENV_RESTORED=YES'); raise
