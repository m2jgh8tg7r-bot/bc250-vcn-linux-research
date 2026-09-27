"""Ordinary libx264 B-picture correctness controls, no malformed inputs."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'r244-cpu-decode-reference-check'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()

def command(cmd,log):
    start=time.monotonic()
    with log.open('w') as f:
        rc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=120).returncode
    return dict(returncode=rc,seconds=time.monotonic()-start)

def main():
    clips=ROOT/'clips'
    clips.mkdir(exist_ok=True)
    rows=[]
    base=['podman','run','--rm','--name','bc250-r246-cpu-control','--userns=keep-id',
        '--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges',
        '--security-opt=label=disable','--tmpfs','/tmp:rw,nosuid,nodev,size=64m',
        '--memory=2g','--cpus=2','--pids-limit=128','--env','BC250_H264_THREADS=2',
        '--mount',f'type=bind,src={PREVIOUS},dst=/data,ro=true',
        '--mount',f'type=bind,src={ROOT},dst=/out,rw=true',
        'localhost/q36-agent-runtime:fedora44']
    assert subprocess.check_output(base+['sh','-c','test ! -e /dev/dri && echo NO_DRI'],text=True).strip()=='NO_DRI'
    for w,h in [(1280,720),(1920,1080)]:
        for slices in [1,4]:
            for bframes in [2,3]:
                name=f'{w}x{h}-high-s{slices}-b{bframes}'
                clip=clips/(name+'.264')
                ref=clips/(name+'.reference.yuv')
                out=clips/(name+'.candidate.yuv')
                enc=command(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi',
                    '-i',f'testsrc2=size={w}x{h}:rate=30','-frames:v','96','-c:v','libx264',
                    '-threads','2','-preset','medium','-profile:v','high','-pix_fmt','yuv420p',
                    '-bf',str(bframes),'-g','48','-keyint_min','48','-x264-params',
                    f'scenecut=0:slices={slices}:ref=3','-f','h264',str(clip)],clips/(name+'.encode.log'))
                assert enc['returncode']==0
                pictures=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
                    '-show_entries','frame=pict_type','-of','json',str(clip)],text=True))['frames']
                counts={t:sum(x['pict_type']==t for x in pictures) for t in ('I','P','B')}
                assert sum(counts.values())==96 and counts['B']>0
                r=command(['ffmpeg','-hide_banner','-loglevel','error','-y','-hwaccel','none','-c:v','h264',
                    '-threads','2','-i',str(clip),'-fps_mode','passthrough','-pix_fmt','yuv420p',
                    '-threads:v','1','-f','rawvideo',str(ref)],clips/(name+'.reference.log'))
                c=command(base+['/data/type2-wrap-variant/h264dec','/out/clips/'+clip.name,
                    '/out/clips/'+out.name],clips/(name+'.candidate.log'))
                row=dict(case=name,width=w,height=h,slices=slices,max_b_frames=bframes,
                    picture_counts=counts,fixture_sha256=sha(clip),reference=r,candidate=c,
                    expected_bytes=w*h*3//2*96)
                if c['returncode']==0 and r['returncode']==0:
                    row.update(reference_sha256=sha(ref),candidate_sha256=sha(out),
                        reference_bytes=ref.stat().st_size,candidate_bytes=out.stat().st_size)
                    row['equal']=(row['reference_sha256']==row['candidate_sha256'] and
                        row['reference_bytes']==row['candidate_bytes']==row['expected_bytes'])
                else:
                    row['equal']=False
                log=(clips/(name+'.candidate.log')).read_text()
                m=re.search(r'(\d+) pictures decoded, (\d+) slices refused',log)
                row['reported_pictures']=int(m[1]) if m else None
                row['refused_slices']=int(m[2]) if m else None
                rows.append(row)
                (ROOT/'results.json').write_text(json.dumps(dict(result='RUNNING',cases=rows,
                    binary_sha256=sha(PREVIOUS/'type2-wrap-variant/h264dec'),gpu_device_exposed=False),indent=2)+'\n')
                print(name,'MATCH' if row['equal'] else 'MISMATCH',flush=True)
                if row['equal']:
                    ref.unlink();out.unlink()
                if c['returncode'] or r['returncode']:
                    raise RuntimeError('Non-completion recorded; no crash investigation')
    result=json.loads((ROOT/'results.json').read_text())
    result.update(result='PASS' if all(x['equal'] for x in rows) else 'MISMATCH',
        cases_completed=len(rows),matched_cases=sum(x['equal'] for x in rows),
        frames=sum(sum(x['picture_counts'].values()) for x in rows),
        scope='Ordinary progressive High-profile 8-bit 420 generated clips only; not full conformance or VAAPI')
    (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    main()
