"""Aggregate the complete pipeline comparison without discarding trials."""
import csv
import json
from pathlib import Path
from statistics import median

ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/'measurements.json').read_text())
    assert data['result']=='PASS' and len(data['rows'])==54
    rows=data['rows'];summary=[]
    for clip in ['ip','b3']:
        for mode in ['copy_null','decode_null','decode_raw']:
            for rate in [0,1,2]:
                rr=[x for x in rows if (x['clip'],x['mode'],x['readrate'])==(clip,mode,rate)]
                assert len(rr)==3 and {x['trial'] for x in rr}=={1,2,3}
                assert all(x['reported_frames']==960 for x in rr)
                r=dict(clip=clip,mode=mode,readrate=rate,trials=3)
                for field in ['fps','wall_seconds','user_seconds','system_seconds','cpu_seconds',
                              'busy_core_equivalents','cpu_seconds_per_frame',
                              'voluntary_switches','involuntary_switches','minor_faults','major_faults']:
                    v=[x[field] for x in rr]
                    r[field]=dict(median=median(v),minimum=min(v),maximum=max(v))
                if rate:
                    assert all(0.9*30*rate <= x['fps'] <= 1.1*30*rate for x in rr)
                summary.append(r)
    contrasts=[]
    for r in summary:
        if not r['readrate']:continue
        ref=next(x for x in summary if x['clip']==r['clip'] and x['mode']==r['mode'] and x['readrate']==0)
        estimate=ref['cpu_seconds_per_frame']['median']*30*r['readrate']
        contrasts.append(dict(clip=r['clip'],mode=r['mode'],readrate=r['readrate'],
            unpaced_estimate=estimate,observed_paced_cores=r['busy_core_equivalents']['median'],
            observed_over_estimate=r['busy_core_equivalents']['median']/estimate))
    result=dict(result='PASS',configurations=18,trials=54,reported_picture_units=54*960,decoded_frames=36*960,streamcopy_picture_units=18*960,
                excluded_warmups=6,excluded_measured_trials=0,summary=summary,contrasts=contrasts,
                limits=['Pipeline contrasts, not additive causal attribution',
                    'No display, audio, energy, game concurrency or dedicated VCN',
                    'Synthetic repeated content, not32seconds of unique scenes',
                    'Decoder/output each requested1 thread; total process thread count may differ',
                    'CPU clocks and unrelated background load uncontrolled'])
    (ROOT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    with (ROOT/'measurements.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    lines=['| Input | Pipeline | Read rate | Median fps | Median busy cores (range) | CPU sec/frame |',
           '|---|---|---:|---:|---:|---:|']
    for r in summary:
        c=r['busy_core_equivalents'];fps=r['fps']['median'];cpu=r['cpu_seconds_per_frame']['median']
        lines.append(f'| {r["clip"]} | {r["mode"]} | {r["readrate"]} | {fps:.2f} | {c["median"]:.4f} ({c["minimum"]:.4f}–{c["maximum"]:.4f}) | {cpu:.6f} |')
    (ROOT/'TABLE.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))

if __name__=='__main__':main()
