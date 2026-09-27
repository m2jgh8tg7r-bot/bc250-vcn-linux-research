"""CPU-only warm-cache throughput; execute inside the recorded container.

No firmware, GPU device, malformed input, or decoder-core changes.
"""
import hashlib
import json
import os
from pathlib import Path
import random
import re
import resource
import subprocess
import time

DATA = Path('/data')
OUT = Path('/out')
LIBPATH = '/hostlib:/hostlib/pipewire-0.3/jack:/hostlib/pulseaudio:/hostlib/samba'
FF = ['/hostlib/ld-linux-x86-64.so.2', '--library-path', LIBPATH, '/host-ffmpeg']
REPEATS = 4
TRIALS = 5

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()

def save(name, data):
    p = OUT/name
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2)+'\n')
    tmp.replace(p)

def command(config, clip, output):
    engine, threads = config['engine'], config['threads']
    if engine == 'candidate':
        return ['/data/type2-wrap-variant/h264dec', str(clip), str(output)]
    return FF+['-hide_banner','-nostdin','-loglevel','error','-y',
               '-hwaccel','none','-c:v','h264','-threads',str(threads),
               '-i',str(clip),'-fps_mode','passthrough','-pix_fmt','yuv420p',
               '-threads:v','1','-progress','pipe:1','-nostats','-f','rawvideo',str(output)]

def run_one(c, clip, output, label, frames):
    env = dict(os.environ, BC250_H264_THREADS=str(c['threads']))
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.perf_counter()
    p = subprocess.run(command(c,clip,output), env=env, capture_output=True, timeout=120)
    wall = time.perf_counter()-start
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = after.ru_utime-before.ru_utime+after.ru_stime-before.ru_stime
    log = (p.stdout+p.stderr).decode(errors='replace')
    (OUT/'logs'/f'{label}.log').write_text(log)
    if p.returncode:
        raise RuntimeError(f'{label}: non-completion, no crash investigation')
    row = dict(c, label=label, frames=frames, wall_seconds=wall, cpu_seconds=cpu,
               fps=frames/wall, average_busy_cores=cpu/wall,
               cpu_seconds_per_frame=cpu/frames,
               estimated_cores_at_30fps=cpu/frames*30,
               estimated_cores_at_60fps=cpu/frames*60, returncode=p.returncode)
    if c['engine']=='candidate':
        m = re.search(r'(\d+) pictures decoded, (\d+) slices refused', log)
        assert m and int(m[1])==frames and int(m[2])==0, (label,log[-1000:])
        row['reported_pictures']=int(m[1])
        row['refused_slices']=int(m[2])
        m = re.search(r'decoding: ([\d.]+) ms',log)
        if m:
            row['internal_decode_seconds']=float(m[1])/1000
    else:
        counts=re.findall(r'^frame=(\d+)$',log,re.M)
        assert counts and int(counts[-1])==frames, (label,log[-1000:])
        row['reported_pictures']=int(counts[-1])
    return row

def main():
    assert not Path('/dev/dri').exists()
    (OUT/'logs').mkdir(exist_ok=True)
    (OUT/'clips').mkdir(exist_ok=True)
    cases = [r for r in json.loads((DATA/'results.json').read_text())['cases']
             if r['profile']=='high' and r['width'] in (1280,1920)]
    fixtures=[]
    for c in cases:
        original=DATA/'clips'/(c['case']+'.264')
        assert sha(original)==c['fixture_sha256']
        extended=OUT/'clips'/(c['case']+'-repeat4.264')
        extended.write_bytes(original.read_bytes()*REPEATS)
        fixtures.append(dict(case=c['case'], original_sha256=sha(original),
            extended_sha256=sha(extended), frames=96*REPEATS, repeats=REPEATS))
    env=dict(gpu_device_exposed=False, affinity=sorted(os.sched_getaffinity(0)),
        cpu_max=Path('/sys/fs/cgroup/cpu.max').read_text().strip(),
        cpu_stat_before=Path('/sys/fs/cgroup/cpu.stat').read_text(),
        candidate_sha256=sha(DATA/'type2-wrap-variant/h264dec'),
        ffmpeg_sha256=sha(Path('/host-ffmpeg')), frames_per_trial=96*REPEATS,
        trials=TRIALS, shuffle_seed=245, container_launch_timed=False,
        process_startup_timed=True, output='/dev/null rawvideo',
        q36_concurrent=False, fixtures=fixtures)
    save('environment.json',env)
    configs=[dict(case=c['case'],engine=e,threads=t) for c in cases
             for e in ('candidate','ffmpeg') for t in (1,2,4,8)]
    correct=[]
    for i,c in enumerate(configs):
        reference=next(x for x in cases if x['case']==c['case'])
        output=Path('/tmp/correct.yuv')
        row=run_one(c,DATA/'clips'/(c['case']+'.264'),output,f'correct-{i}',96)
        row.update(actual_sha256=sha(output), expected_sha256=reference['reference_sha256'],
                   actual_bytes=output.stat().st_size,expected_bytes=reference['expected_raw_bytes'])
        row['equal']=row['actual_sha256']==row['expected_sha256'] and row['actual_bytes']==row['expected_bytes']
        correct.append(row)
        save('correctness.json',dict(cases=correct))
        output.unlink()
        assert row['equal'], c
    print('Correctness PASS',len(correct),flush=True)
    rows=[]
    rng=random.Random(245)
    # Round zero warms every exact long-input configuration; it is excluded.
    for trial in range(TRIALS+1):
        order=configs.copy()
        rng.shuffle(order)
        for index,c in enumerate(order):
            row=run_one(c,OUT/'clips'/(c['case']+'-repeat4.264'),Path('/dev/null'),
                        f'trial{trial}-{index}',96*REPEATS)
            row.update(trial=trial,warmup=trial==0)
            rows.append(row)
            save('measurements.json',dict(result='RUNNING',rows=rows))
        print('Completed round',trial,'/',TRIALS,flush=True)
    env['cpu_stat_after']=Path('/sys/fs/cgroup/cpu.stat').read_text()
    save('environment.json',env)
    save('measurements.json',dict(result='PASS',rows=rows))

if __name__=='__main__':
    main()
