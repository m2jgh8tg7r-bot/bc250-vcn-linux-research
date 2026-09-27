"""Separate ordinary FFmpeg pipeline costs; no GPU/video firmware access."""
import hashlib
import json
import os
from pathlib import Path
import random
import re
import resource
import subprocess
import time

OUT=Path('/out')
FF=['/hostlib/ld-linux-x86-64.so.2','--library-path',
    '/hostlib:/hostlib/pipewire-0.3/jack:/hostlib/pulseaudio:/hostlib/samba','/host-ffmpeg']
FRAMES=960

def save(name,data):
    target=OUT/name;tmp=target.with_suffix('.tmp')
    tmp.write_text(json.dumps(data,indent=2)+'\n');tmp.replace(target)

def command(c,verbose=False):
    args=FF+['-hide_banner','-nostdin','-loglevel','info' if verbose else 'error','-y',
             '-hwaccel','none','-c:v','h264','-threads:v','1']
    if c['readrate']:args+=['-readrate',str(c['readrate'])]
    args+=['-i',str(OUT/'clips'/(c['clip']+'.264')),'-map','0:v:0','-an','-sn','-dn',
           '-fps_mode','passthrough','-threads:v','1','-progress','pipe:1','-nostats']
    if c['mode']=='copy_null':args+=['-c:v','copy','-f','null','/dev/null']
    elif c['mode']=='decode_null':args+=['-c:v','wrapped_avframe','-f','null','/dev/null']
    else:args+=['-c:v','rawvideo','-pix_fmt','yuv420p','-f','rawvideo','/dev/null']
    return args

def measure(c,label,verbose=False):
    before=resource.getrusage(resource.RUSAGE_CHILDREN);start=time.perf_counter()
    run=subprocess.run(command(c,verbose),capture_output=True,timeout=90)
    wall=time.perf_counter()-start;after=resource.getrusage(resource.RUSAGE_CHILDREN)
    text=(run.stdout+run.stderr).decode(errors='replace')
    (OUT/'logs'/(label+'.log')).write_text(text)
    assert run.returncode==0,(label,run.returncode,text[-1000:])
    counts=re.findall(r'^frame=(\d+)$',text,re.M)
    assert counts and int(counts[-1])==FRAMES,(label,counts[-1:] )
    user=after.ru_utime-before.ru_utime;system=after.ru_stime-before.ru_stime
    return dict(c,label=label,returncode=run.returncode,reported_frames=int(counts[-1]),
        wall_seconds=wall,user_seconds=user,system_seconds=system,cpu_seconds=user+system,
        fps=FRAMES/wall,busy_core_equivalents=(user+system)/wall,
        cpu_seconds_per_frame=(user+system)/FRAMES,
        voluntary_switches=after.ru_nvcsw-before.ru_nvcsw,
        involuntary_switches=after.ru_nivcsw-before.ru_nivcsw,
        minor_faults=after.ru_minflt-before.ru_minflt,
        major_faults=after.ru_majflt-before.ru_majflt)

def main():
    assert not Path('/dev/dri').exists()
    (OUT/'logs').mkdir(exist_ok=True)
    fixtures=json.loads((OUT/'fixtures.json').read_text())
    for f in fixtures['clips']:
        assert hashlib.sha256((OUT/'clips'/(f['clip']+'.264')).read_bytes()).hexdigest()==f['sha256']
    env=dict(gpu_device_exposed=False,affinity=sorted(os.sched_getaffinity(0)),
        cpu_max=Path('/sys/fs/cgroup/cpu.max').read_text().strip(),
        cpu_stat_before=Path('/sys/fs/cgroup/cpu.stat').read_text(),
        ffmpeg_sha256=hashlib.sha256(Path('/host-ffmpeg').read_bytes()).hexdigest(),
        container_launch_timed=False,process_launch_timed=True,q36_concurrent=False,
        decoder_threads_requested=1,output_threads_requested=1,
        frames_per_run=FRAMES,shuffle_seed=247,governor_modified=False)
    save('environment.json',env)
    modes=['copy_null','decode_null','decode_raw']
    warm=[]
    for clip in ['ip','b3']:
        for mode in modes:
            warm.append(measure(dict(clip=clip,mode=mode,readrate=0),f'warm-{clip}-{mode}',True))
    save('warmups.json',dict(rows=warm,excluded=True))
    configs=[dict(clip=clip,mode=mode,readrate=rate) for clip in ['ip','b3']
             for mode in modes for rate in [0,1,2]]
    rng=random.Random(247);rows=[]
    for trial in [1,2,3]:
        order=configs.copy();rng.shuffle(order)
        for index,c in enumerate(order):
            row=measure(c,f'trial{trial}-{index}');row['trial']=trial;rows.append(row)
            save('measurements.json',dict(result='RUNNING',rows=rows))
            print('Completed',len(rows),'/',54,c,flush=True)
    env['cpu_stat_after']=Path('/sys/fs/cgroup/cpu.stat').read_text()
    save('environment.json',env)
    save('measurements.json',dict(result='PASS',rows=rows,trials=len(rows),frames=len(rows)*FRAMES))

if __name__=='__main__':main()
