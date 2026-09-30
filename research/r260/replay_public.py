"""Replay published static checks in a separate work directory.

Only source files are downloaded. Nothing is compiled, loaded into a driver,
or sent to a device. Existing published results are never overwritten.
"""
import argparse, concurrent.futures, hashlib, json, os, shutil, subprocess, sys
import urllib.request
from pathlib import Path

def digest(data):
    return hashlib.sha256(data).hexdigest()

def prepare_sources(public, work, download):
    manifests=[(public/'r260/source-manifest.json',work/'reference/upstream'),
               (public/'r257/source-manifest.json',work/'research/r257/sources')]
    jobs=[]
    for manifest,dest in manifests:
        data=json.loads(manifest.read_text())
        for row in data['files']: jobs.append((row,dest))
    history=json.loads((public/'r254/source-manifest.json').read_text())
    for version in history['versions']:
        for row in version['files']:
            jobs.append((row,work/'research/r254/sources'/version['tag']))
    def obtain(job):
        row,root=job;rel=Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts: raise ValueError('Nonrelative source path')
        if not row['url'].startswith('https://raw.githubusercontent.com/torvalds/linux/'):
            raise ValueError('Unexpected source host/repository')
        target=root/rel
        if target.exists():
            data=target.read_bytes()
        elif download:
            with urllib.request.urlopen(row['url'],timeout=45) as response:data=response.read()
            if digest(data)!=row['sha256']:raise ValueError('Downloaded source hash mismatch: '+row['path'])
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        else:raise FileNotFoundError('Missing pinned source; use --download or prepopulate the work cache: '+row['path'])
        if digest(data)!=row['sha256']:raise ValueError('Cached source hash mismatch: '+row['path'])
        return {'path':row['path'],'sha256':row['sha256']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        rows=list(pool.map(obtain,jobs))
    (work/'reference').mkdir(exist_ok=True)
    shutil.copyfile(public/'r260/source-manifest.json',work/'reference/source-manifest.json')
    return rows

def main():
    if not __debug__:raise RuntimeError('Audit assertions must be enabled; do not use Python -O')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True)
    p.add_argument('--download',action='store_true',help='Fetch hash-pinned public Linux source files')
    p.add_argument('--saved-firmware',type=Path,help='Optional locally held matching firmware file for R255; never loaded or uploaded')
    args=p.parse_args();public=Path(__file__).resolve().parent.parent;work=args.work.resolve()
    if work==public or public in work.parents:raise ValueError('Choose a work directory outside the published research tree')
    work.mkdir(parents=True,exist_ok=True)
    for number in range(251,260):
        dest=work/'research'/('r'+str(number));dest.mkdir(parents=True,exist_ok=True)
        for src in (public/('r'+str(number))).glob('*'):
            if src.is_file() and (src.suffix=='.py' or src.name in ['source-manifest.json','capture-template.json']):
                shutil.copyfile(src,dest/src.name)
    rows=prepare_sources(public,work,args.download)
    source=work/'reference/upstream'; header=source/'drivers/gpu/drm/amd/include/asic_reg/vcn/vcn_2_0_0_sh_mask.h'
    commands=[]
    def add(stage,script,arguments,output):commands.append((stage,script,arguments,output))
    for stage,script in [('r251','audit_start.py'),('r252','audit_calls.py'),
                         ('r256','audit_observation.py'),('r258','audit_preconditions.py'),
                         ('r259','audit_provenance.py')]:
        add(stage,script,['--source-root',str(source),'--output',str(work/'research'/stage/'results.json')],'results.json')
    add('r251','audit_inventory.py',['--source-root',str(source),'--output',str(work/'research/r251/register-inventory.json')],'register-inventory.json')
    add('r253','verify_interpretation.py',[],'verification.json')
    add('r253','verify_comparison.py',[],'comparison-verification.json')
    add('r253','verify_source_fields.py',[str(header),'--output',str(work/'research/r253/source-field-verification.json')],'source-field-verification.json')
    add('r253','interpret_capture.py',[str(work/'research/r253/capture-template.json'),'--output',str(work/'research/r253/template-result.json')],'template-result.json')
    add('r254','compare_history.py',['--current-source',str(source)],'results.json')
    add('r257','audit_generations.py',['--current-source',str(source)],'results.json')
    if args.saved_firmware:
        add('r255','audit_cache.py',['--source-root',str(source),'--saved-firmware',str(args.saved_firmware.resolve()),'--output',str(work/'research/r255/results.json')],'results.json')
    outcomes=[];env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
    for stage,script,arguments,output in commands:
        result=subprocess.run([sys.executable,str(work/'research'/stage/script),*arguments],capture_output=True,text=True,timeout=60,env=env)
        if result.returncode:
            raise RuntimeError(stage+'/'+script+' failed: '+result.stderr)
        actual=json.loads((work/'research'/stage/output).read_text())
        expected=json.loads((public/stage/output).read_text())
        if stage=='r252':
            # Private retained-source witnesses are deliberately not replayed.
            for value in [actual,expected]:
                value.pop('retained_local_source',None)
                value['conclusions']=[x for x in value['conclusions'] if not x.startswith('Retained diagnostic source')]
        if actual!=expected:raise AssertionError('Public result differs: '+stage+'/'+output)
        outcomes.append({'stage':stage,'script':script,'result':'MATCH','published_result':output})
    report={'result':'PASS','scope':'Pinned source and synthetic offline replay only',
            'source_file_instances_verified':len(rows),'matched_checks':outcomes,
            'r255_saved_file_replayed':bool(args.saved_firmware),
            'retained_private_source_replayed':False,'hardware_access':False,
            'firmware_upload_or_load':False}
    (work/'replay-result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
