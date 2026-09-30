"""Synthetic negative controls for cross-capture attribution."""
import copy,json
from pathlib import Path
from compare_captures import compare
base={'register_map':'vcn_2_0_0','source_revision':'synthetic-source','module_identity':'synthetic-module','firmware_identity':'synthetic-firmware','boot_context':'synthetic-boot',
      'mapping_provenance':'synthetic-map','read_method':'synthetic-input','load_mode':'synthetic-load',
      'mode':'normal','capture_phase':'synthetic-left','registers':{'UVD_STATUS':0,'UVD_RBC_RB_RPTR':None}}
right=copy.deepcopy(base);right['capture_phase']='synthetic-right';right['registers']={'UVD_STATUS':2,'UVD_RBC_RB_RPTR':0}
checks=[]
def check(name,condition):
    assert condition,name
    checks.append(name)
r=compare(base,right)
check('delta_is_not_execution_or_chronology',r['metadata_compatible'] and len(r['differences'])==1 and not r['execution_proven'] and not r['chronology_proven'])
check('missing_pointer_is_not_zero_transition',r['unknown_comparisons']==['UVD_RBC_RB_RPTR'])
for key in ['source_revision','module_identity','firmware_identity','boot_context','mapping_provenance','read_method','load_mode']:
    other=copy.deepcopy(right);other[key]='different'
    r=compare(base,other);check('reject_cross_'+key,not r['metadata_compatible'] and not r['differences'] and key in r['mismatched_labels'])
other=copy.deepcopy(right);other['mode']='dpg-indirect-table';check('reject_cross_mode',not compare(base,other)['metadata_compatible'])
other=copy.deepcopy(right);del other['register_map'];check('missing_map_not_silently_matched',not compare(base,other)['metadata_compatible'])
other=copy.deepcopy(base);other['registers']['UVD_STATUS']='0x0';check('equal_scalar_different_notation',not compare(base,other)['differences'])
other=copy.deepcopy(right);other['registers']['UVD_STATUS']=0xffffffff;r=compare(base,other)
check('all_ones_delta_stays_unverified',not r['execution_proven'] and any('all-ones' in x for x in r['notes']))
other=copy.deepcopy(right);other['register_map']='vcn_2_5_0'
try:compare(base,other)
except ValueError:check('reject_other_generation',True)
else:raise AssertionError('other map accepted')
Path(__file__).with_name('comparison-verification.json').write_text(json.dumps({'result':'PASS','controls':checks,'scope':'Synthetic comparison only; no supplied external captures tested'},indent=2)+'\n')
print('PASS',len(checks),'cross-capture controls')
