"""Replay existing ordinary clips through the isolated CPU diagnostic variant."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'type2-wrap-variant/replay'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    binary = ROOT/'type2-wrap-variant/h264dec'
    rows = []
    base = ['podman','run','--rm','--userns=keep-id',f'--user={os.getuid()}:{os.getgid()}',
        '--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges',
        '--security-opt=label=disable','--tmpfs','/tmp:rw,nosuid,nodev,size=64m',
        '--memory=2g','--cpus=2','--pids-limit=128',
        '--mount',f'type=bind,src={ROOT},dst=/data,ro=true',
        '--mount',f'type=bind,src={OUT},dst=/out,rw=true',
        'localhost/q36-agent-runtime:fedora44']
    for relative, group in [('.', 'gop32'), ('gop12-control', 'gop12')]:
        original = json.loads((ROOT/relative/'results.json').read_text())
        for case in original['cases']:
            clip = ROOT/relative/'clips'/(case['case']+'.264')
            assert sha(clip)==case['fixture_sha256']
            name = group+'-'+case['case']
            output = OUT/(name+'.yuv')
            start = time.monotonic()
            with (OUT/(name+'.log')).open('w') as stream:
                result = subprocess.run(base+['/data/type2-wrap-variant/h264dec',
                    '/data/'+str(clip.relative_to(ROOT)), '/out/'+output.name],
                    stdout=stream, stderr=subprocess.STDOUT, timeout=180)
            row = dict(case=name, frames=case['frames'], fixture_sha256=case['fixture_sha256'],
                returncode=result.returncode, seconds=time.monotonic()-start,
                expected_sha256=case['reference_sha256'], expected_bytes=case['expected_raw_bytes'])
            if result.returncode==0:
                row.update(actual_sha256=sha(output), actual_bytes=output.stat().st_size)
                row['equal'] = row['actual_sha256']==row['expected_sha256'] and row['actual_bytes']==row['expected_bytes']
            else:
                row['equal'] = False
            rows.append(row)
            record = dict(result='RUNNING', binary_sha256=sha(binary), gpu_device_exposed=False,
                network='none', decoder_core_modified=False, cases=rows)
            (OUT/'results.json').write_text(json.dumps(record,indent=2)+'\n')
            print(name, 'MATCH' if row['equal'] else 'MISMATCH', flush=True)
            if row['equal']:
                output.unlink()
            if result.returncode:
                raise RuntimeError('Non-completion; no crash investigation')
    record.update(result='PASS' if all(x['equal'] for x in rows) else 'MISMATCH',
        case_count=len(rows), matched_cases=sum(x['equal'] for x in rows),
        total_frames=sum(x['frames'] for x in rows),
        scope='Diagnostic CPU harness ordering variant on the existing I/P matrix only')
    (OUT/'results.json').write_text(json.dumps(record,indent=2)+'\n')
    print(record['result'],record['matched_cases'],'/',record['case_count'])


if __name__ == '__main__':
    run()
