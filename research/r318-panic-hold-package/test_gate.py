"""Exercise the actual init gate with CPU-only command stubs and a PTY."""
from pathlib import Path
import json, os, pty, select, subprocess, time

out = Path(__file__).resolve().parent
source = (out / 'init').read_text()
fragment = source[source.index('export LC_ALL=C'):source.rindex('\nhold')]
fragment = fragment.replace('stty -a </dev/console', 'stty -a <&0 2>/dev/null || true')
fragment = fragment.replace('[[ ! -d /sys/module/amdgpu ]]', '[[ "$MOCK_GPU_PRESENT" != YES ]]')
script = '''marker() { printf '%s\n' "$*"; }
fail() { marker "FAIL $*"; exit 23; }
sleep() { :; }
modprobe() { printf 'MOCK_GPU_LOAD %s\n' "$*"; return 17; }
''' + fragment
cases = [
    ('exact', b'R299-CP03-RECEIVED\n', 'INPUT_EXACT_MATCH', True, False),
    ('trailing_space', b'R299-CP03-RECEIVED \n', 'INPUT_MISMATCH', False, False),
    ('pipe_crlf', b'R299-CP03-RECEIVED\r\n', 'INPUT_MISMATCH', False, False),
    ('empty_line', b'\n', 'INPUT_MISMATCH', False, False),
    ('eof', b'', 'INPUT_READ_FAILURE', False, False),
    ('exact_without_newline', b'R299-CP03-RECEIVED', 'INPUT_READ_FAILURE', False, False),
    ('unicode_dash', 'R299–CP03-RECEIVED\n'.encode(), 'INPUT_MISMATCH', False, False),
    ('long_input', b'x' * 200 + b'\n', 'INPUT_MISMATCH', False, False),
    ('gpu_already_present', b'R299-CP03-RECEIVED\n', 'GPU loaded before gate', False, True),
    ('queued_wrong_line', b'wrong\nR299-CP03-RECEIVED\n', 'INPUT_MISMATCH', False, False),
]
results = []
for name, data, expected, load, gpu in cases:
    env = dict(os.environ, MOCK_GPU_PRESENT='YES' if gpu else 'NO')
    run = subprocess.run(['bash', '-c', script], input=data, capture_output=True, env=env, timeout=5)
    log = run.stdout.decode()
    assert expected in log, (name, log)
    assert ('MOCK_GPU_LOAD' in log) == load, (name, log)
    assert log.count('MOCK_GPU_LOAD') == int(load)
    assert run.returncode == (0 if load else 23), (name, run.returncode)
    if load:
        markers = ['INPUT_RESULT read_rc=0 bytes=18', 'INPUT_EXACT_MATCH',
                   'RECEIVER_CONFIRMED', 'AMDGPU_MODPROBE_BEGIN', 'MOCK_GPU_LOAD',
                   'UNEXPECTED_MODPROBE_RETURN rc=17']
        positions = [log.index(x) for x in markers]
        assert positions == sorted(positions)
    results.append(dict(case=name, pass_result=True, mocked_gpu_loads=int(load), output=log))

master, slave = pty.openpty()
process = subprocess.Popen(['bash', '-c', script], stdin=slave, stdout=slave, stderr=slave,
                           env=dict(os.environ, MOCK_GPU_PRESENT='NO'))
os.close(slave)
buf = b''
deadline = time.monotonic() + 5
try:
    while b'INPUT_READY' not in buf:
        assert time.monotonic() < deadline
        if select.select([master], [], [], .1)[0]:
            buf += os.read(master, 4096)
    os.write(master, b'R299-CP03-RECEIVED\n')
    while time.monotonic() < deadline:
        if select.select([master], [], [], .1)[0]:
            try:
                buf += os.read(master, 4096)
            except OSError:
                break
    process.wait(timeout=1)
finally:
    os.close(master)
    if process.poll() is None:
        process.kill()
        process.wait()
assert process.returncode == 0
assert b'stdin_tty=YES' in buf and b'INPUT_EXACT_MATCH' in buf
assert buf.count(b'MOCK_GPU_LOAD') == 1
results.append(dict(case='pty_exact', pass_result=True, mocked_gpu_loads=1, output=buf.decode()))
(out / 'GATE_TEST.json').write_text(json.dumps(dict(result='PASS', tests=results,
    real_gpu_load=False, live_console_test=False, limits='Command stubs and PTY do not prove boot-console or panic delivery'), indent=2) + '\n')
print(f'PASS {len(results)}/{len(results)}; no real module load')
