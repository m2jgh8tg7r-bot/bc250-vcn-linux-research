"""FFmpeg input-pacing CPU control; no display/audio or real-player claim."""
import json
import random
from pathlib import Path
import benchmark as b

original_command=b.command
rate=1

def paced_command(config,clip,output):
    cmd=original_command(config,clip,output)
    index=cmd.index('-i')
    return cmd[:index]+['-readrate',str(rate)]+cmd[index:]

def main():
    global rate
    assert not Path('/dev/dri').exists()
    b.command=paced_command
    rows=[]
    configurations=[(threads,r) for threads in (1,4) for r in (1,2)]
    rng=random.Random(2451)
    for trial in range(1,4):
        order=configurations.copy();rng.shuffle(order)
        for threads,rate in order:
            config=dict(case='1920x1080-high-s1',engine='ffmpeg',threads=threads)
            row=b.run_one(config,b.OUT/'clips'/'1920x1080-high-s1-repeat4.264',Path('/dev/null'),
                          f'paced-{trial}-{threads}-{rate}',384)
            row.update(trial=trial,readrate=rate,nominal_target_fps=30*rate)
            rows.append(row)
            b.save('paced-control.json',dict(result='RUNNING',rows=rows))
        print('Paced CPU control round',trial,flush=True)
    b.save('paced-control.json',dict(result='PASS',rows=rows,trials=len(rows),frames=len(rows)*384,
        scope='Input-paced FFmpeg CPU decode to null output; not displayed playback',
        container_launch_timed=False,process_launch_timed=True,gpu_device_exposed=False,
        q36_concurrent=False,warmup='Previously validated same stream; no separate paced warm-up'))

if __name__=='__main__':
    main()
