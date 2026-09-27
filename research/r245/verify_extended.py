"""Check concatenated benchmark clips against repeated original reference YUV."""
import hashlib
import json
from pathlib import Path
import benchmark as b

def main():
    rows=[]
    cases=[c for c in json.loads((b.DATA/'results.json').read_text())['cases']
           if c['profile']=='high' and c['width'] in (1280,1920)]
    output=Path('/tmp/check.yuv')
    for c in cases:
        config=dict(case=c['case'],engine='ffmpeg',threads=1)
        b.run_one(config,b.DATA/'clips'/(c['case']+'.264'),output,'long-ref-'+c['case'],96)
        assert b.sha(output)==c['reference_sha256']
        expected=hashlib.sha256()
        for _ in range(4):
            with output.open('rb') as f:
                for block in iter(lambda:f.read(1024*1024),b''):
                    expected.update(block)
        output.unlink()
        for engine,threads in [('candidate',1),('candidate',8),('ffmpeg',1)]:
            config=dict(case=c['case'],engine=engine,threads=threads)
            r=b.run_one(config,b.OUT/'clips'/(c['case']+'-repeat4.264'),output,
                        f'long-{c["case"]}-{engine}-{threads}',384)
            r.update(expected_sha256=expected.hexdigest(),actual_sha256=b.sha(output),
                     expected_bytes=c['expected_raw_bytes']*4,actual_bytes=output.stat().st_size)
            r['equal']=r['expected_sha256']==r['actual_sha256'] and r['expected_bytes']==r['actual_bytes']
            rows.append(r)
            b.save('extended-correctness.json',dict(cases=rows))
            output.unlink()
            assert r['equal'],config
        print('Extended correctness PASS',c['case'],flush=True)
    b.save('extended-correctness.json',dict(result='PASS',cases=rows,matched_cases=len(rows)))

if __name__=='__main__':
    main()
