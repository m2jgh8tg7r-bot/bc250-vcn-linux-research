"""Repeat complete known-good elementary streams, preserving IDR boundaries."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    (ROOT/'clips').mkdir(exist_ok=True);rows=[]
    for stage,case,label in [
        ('r244-cpu-decode-reference-check','1920x1080-high-s1','ip'),
        ('r246-cpu-b-picture-control','1920x1080-high-s1-b3','b3')]:
        source=ROOT.parent/stage
        old=next(x for x in json.loads((source/'results.json').read_text())['cases'] if x['case']==case)
        raw=(source/'clips'/(case+'.264')).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==old['fixture_sha256']
        data=raw*10;(ROOT/'clips'/(label+'.264')).write_bytes(data)
        rows.append(dict(clip=label,source_stage=stage.split('-')[0],source_case=case,
            original_sha256=old['fixture_sha256'],original_reference_yuv_sha256=old['reference_sha256'],
            sha256=hashlib.sha256(data).hexdigest(),frames=960,repetitions=10,
            unique_frames=96,nominal_fps=30))
    (ROOT/'fixtures.json').write_text(json.dumps(dict(clips=rows),indent=2)+'\n')

if __name__=='__main__':main()
