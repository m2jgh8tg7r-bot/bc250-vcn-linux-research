"""Summarize all recorded trials without trimming observations."""
import json
from pathlib import Path
from statistics import median

ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/'measurements.json').read_text())
    assert data['result']=='PASS'
    rows=data['rows']
    assert len(rows)==96 and sum(x['warmup'] for x in rows)==24
    summary=[]
    keys=sorted({(x['case'],x['engine'],x['threads']) for x in rows})
    for case,engine,threads in keys:
        rr=[x for x in rows if not x['warmup'] and
            (x['case'],x['engine'],x['threads'])==(case,engine,threads)]
        assert len(rr)==3 and {x['trial'] for x in rr}=={1,2,3}
        assert all(x['reported_pictures']==384 for x in rr)
        r=dict(case=case,engine=engine,threads=threads,trials=len(rr))
        for field in ('fps','wall_seconds','cpu_seconds','average_busy_cores',
                      'cpu_seconds_per_frame','estimated_cores_at_30fps','estimated_cores_at_60fps'):
            values=[x[field] for x in rr]
            r[field]=dict(median=median(values),minimum=min(values),maximum=max(values))
        summary.append(r)
    out=dict(result='PASS',configurations=len(summary),warmups=24,measured_trials=72,
             measured_frames=72*384,excluded_measured_trials=0,summary=summary,
             classification='PROVEN_LIVE CPU-only synthetic process throughput',
             limitations=['Not VCN, VAAPI, display, audio synchronization, power or gaming concurrency',
               'Warm-cache generated I/P/B input, four repeats of each 96-frame clip',
               'Full process time includes process startup and rawvideo handling to /dev/null',
               'Thread settings control different parallel architectures; not identical thread counts',
               'CPU demand at target fps is an extrapolation, not paced-playback measurement',
               'No CPU frequency or background desktop workload control; one machine/session',
               'Selected B-picture clips only; decoder core built -O2 without explicit native ISA flags'])
    (ROOT/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
    lines=['| Clip | Decoder | Thread setting | Median fps (range) | Estimated cores at 30fps |',
           '|---|---|---:|---:|---:|']
    for r in summary:
        f=r['fps'];c=r['estimated_cores_at_30fps']['median']
        lines.append(f'| {r["case"]} | {r["engine"]} | {r["threads"]} | {f["median"]:.1f} ({f["minimum"]:.1f}–{f["maximum"]:.1f}) | {c:.3f} |')
    (ROOT/'TABLE.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))

if __name__=='__main__':
    main()
