"""Compare two supplied scalar captures offline; no acquisition or diagnosis."""
import argparse,json
from pathlib import Path
from interpret_capture import interpret,u32

def compare(left,right):
    decoded=[interpret(left),interpret(right)]
    keys=['register_map','source_revision','module_identity','firmware_identity','boot_context','mapping_provenance','read_method','load_mode','mode']
    missing=[{'side':side,'fields':item['missing_provenance']} for side,item in zip(['left','right'],decoded) if item['missing_provenance']]
    mismatches=[key for key in keys if left.get(key)!=right.get(key)]
    compatible=not missing and not mismatches
    result={'classification':'PROVEN_STATICALLY','scope':'Supplied scalar differences only; matching metadata labels are not identity or authenticity verification',
            'metadata_compatible':compatible,'missing_provenance':missing,'mismatched_labels':mismatches,
            'left_phase':left.get('capture_phase'),'right_phase':right.get('capture_phase'),
            'differences':[],'unknown_comparisons':[],
            'chronology_proven':False,'execution_proven':False,'hardware_failure_proven':False,
            'notes':['Values can be host-written, stale, invalid, or from different actual states despite equal supplied labels',
                     'A pointer delta or ready-bit delta does not by itself prove autonomous execution']}
    if not compatible:return result
    a=left.get('registers',{});b=right.get('registers',{})
    for reg in sorted(set(a)|set(b)):
        x=u32(a.get(reg));y=u32(b.get(reg))
        if x is None or y is None:
            result['unknown_comparisons'].append(reg)
        elif x!=y:
            result['differences'].append({'register':reg,'left':hex(x),'right':hex(y),'xor':hex(x^y)})
    result['notes']+=decoded[0]['notes']+decoded[1]['notes']
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('left',type=Path);p.add_argument('right',type=Path)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=compare(json.loads(a.left.read_text()),json.loads(a.right.read_text()))
    a.output.write_text(json.dumps(r,indent=2)+'\n')
