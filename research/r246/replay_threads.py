"""Replay the same ordinary B-picture clips at two extra worker settings."""
import json
from pathlib import Path
import subprocess
import check_b_pictures as b

def main():
    original=json.loads((b.ROOT/'results.json').read_text())
    assert original['result']=='PASS' and original['matched_cases']==8
    rows=[]
    for threads in (1,8):
        for case in original['cases']:
            name=case['case']
            clip=b.ROOT/'clips'/(name+'.264')
            assert b.sha(clip)==case['fixture_sha256']
            output=b.ROOT/'clips'/f'{name}-t{threads}.yuv'
            cmd=['podman','run','--rm','--name','bc250-r246-thread-control','--userns=keep-id',
                '--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges',
                '--security-opt=label=disable','--memory=2g','--cpus=2','--pids-limit=128',
                '--env',f'BC250_H264_THREADS={threads}',
                '--mount',f'type=bind,src={b.PREVIOUS},dst=/data,ro=true',
                '--mount',f'type=bind,src={b.ROOT},dst=/out,rw=true',
                'localhost/q36-agent-runtime:fedora44','/data/type2-wrap-variant/h264dec',
                '/out/clips/'+clip.name,'/out/clips/'+output.name]
            r=b.command(cmd,b.ROOT/'clips'/f'{name}-t{threads}.log')
            assert r['returncode']==0, 'Non-completion; no crash investigation'
            r.update(case=name,threads=threads,fixture_sha256=case['fixture_sha256'],
                expected_sha256=case['reference_sha256'],actual_sha256=b.sha(output),
                expected_bytes=case['expected_bytes'],actual_bytes=output.stat().st_size)
            r['equal']=r['expected_sha256']==r['actual_sha256'] and r['expected_bytes']==r['actual_bytes']
            rows.append(r)
            (b.ROOT/'thread-replay.json').write_text(json.dumps(dict(result='RUNNING',cases=rows),indent=2)+'\n')
            assert r['equal'],name
            output.unlink()
        print('B-picture thread setting PASS',threads,flush=True)
    (b.ROOT/'thread-replay.json').write_text(json.dumps(dict(result='PASS',matched_cases=len(rows),
        frames=len(rows)*96,cases=rows),indent=2)+'\n')

if __name__=='__main__':
    main()
