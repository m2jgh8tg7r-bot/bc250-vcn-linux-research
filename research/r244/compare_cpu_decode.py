"""Compare ordinary generated H.264 clips with FFmpeg in a GPU-free sandbox.

This checks CPU decoder output, not VA-API integration, performance or VCN.
No malformed input generation, fuzzing, firmware or hardware access.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
IMAGE = 'localhost/q36-agent-runtime:fedora44'
FRAMES = 96


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def command(args, log, timeout=180):
    start = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(args, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
    return dict(returncode=result.returncode, wall_seconds=time.monotonic()-start)


def run():
    clips = HERE/'clips'
    clips.mkdir(exist_ok=True)
    version = subprocess.check_output(['ffmpeg','-version'], text=True)
    (HERE/'ffmpeg-version.txt').write_text(version)
    rows = []
    base = ['podman','run','--rm','--userns=keep-id',
        f'--user={os.getuid()}:{os.getgid()}', '--network=none','--read-only',
        '--cap-drop=ALL','--security-opt=no-new-privileges','--security-opt=label=disable',
        '--tmpfs','/tmp:rw,nosuid,nodev,size=64m','--memory=2g','--cpus=2','--pids-limit=128',
        '--mount',f'type=bind,src={HERE},dst=/work,rw=true',IMAGE]
    device_check = subprocess.check_output(base+['sh','-c',
        'test ! -e /dev/dri && printf "NO_DRI_DEVICE\n"'], text=True).strip()
    assert device_check == 'NO_DRI_DEVICE'
    for width,height in [(640,360),(1280,720),(1920,1080)]:
        for profile in ['baseline','main','high']:
            for slices in [1,4]:
                name = f'{width}x{height}-{profile}-s{slices}'
                clip, reference, candidate = [clips/(name+ext) for ext in ['.264','.reference.yuv','.candidate.yuv']]
                encode = ['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi',
                    '-i',f'testsrc2=size={width}x{height}:rate=30','-frames:v',str(FRAMES),
                    '-c:v','libx264','-threads','2','-preset','medium','-profile:v',profile,
                    '-pix_fmt','yuv420p','-bf','0','-g','32','-keyint_min','32',
                    '-x264-params',f'scenecut=0:slices={slices}:ref=3','-f','h264',str(clip)]
                e = command(encode, clips/(name+'.encode.log'))
                if e['returncode']:
                    raise RuntimeError('Ordinary fixture generation failed: '+name)
                ref = command(['ffmpeg','-hide_banner','-loglevel','error','-y',
                    '-hwaccel','none','-c:v','h264','-threads','2','-i',str(clip),
                    '-fps_mode','passthrough','-pix_fmt','yuv420p','-f','rawvideo',str(reference)],
                    clips/(name+'.reference.log'))
                dec = command(base+['/work/h264dec','/work/clips/'+clip.name,
                    '/work/clips/'+candidate.name], clips/(name+'.candidate.log'))
                row = dict(case=name, width=width, height=height, profile=profile,
                    slices=slices, frames=FRAMES, b_frames=0, gop=32,
                    fixture_sha256=sha(clip), reference=ref, candidate=dec,
                    expected_raw_bytes=width*height*3//2*FRAMES)
                if ref['returncode']==0 and dec['returncode']==0:
                    row.update(reference_bytes=reference.stat().st_size,
                        candidate_bytes=candidate.stat().st_size,
                        reference_sha256=sha(reference), candidate_sha256=sha(candidate))
                    row['equal'] = (row['reference_bytes']==row['candidate_bytes']==row['expected_raw_bytes']
                        and row['reference_sha256']==row['candidate_sha256'])
                else:
                    row['equal'] = False
                rows.append(row)
                result = dict(result='RUNNING', scope='CPU decoder reference output only',
                    source_commit='7d9c38bdfdc469505eeb94864a203c0b4ffee12c',
                    binary_sha256=sha(HERE/'h264dec'), gpu_device_exposed=False,
                    device_check=device_check, network='none', cases=rows)
                (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
                print(name, 'MATCH' if row['equal'] else 'MISMATCH', flush=True)
                if row['equal']:
                    reference.unlink()
                    candidate.unlink()
                if dec['returncode'] != 0:
                    raise RuntimeError('Decoder did not complete; preserving evidence, no crash exploration')
    result.update(result='PASS' if all(x['equal'] for x in rows) else 'MISMATCH',
        case_count=len(rows), total_frames=sum(x['frames'] for x in rows),
        matched_cases=sum(x['equal'] for x in rows),
        limitations=['Generated I/P clips only; not a full conformance suite',
            'No VA-API driver integration or GPU surface upload tested',
            'No dedicated VCN execution or physical hardware-state inference',
            'Cgroup-limited wall times are not performance benchmarks'])
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['result'],result['matched_cases'],'/',result['case_count'])


if __name__ == '__main__':
    run()
