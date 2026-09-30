"""Synthetic ambiguity/validation controls for the offline evidence interpreter."""
from interpret_capture import interpret
import json
from pathlib import Path
checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name)
r=interpret({});check('missing_is_not_zero',all(not x['provided'] for x in r['decoded'].values()))
for value,ready,busy in [(0,False,False),(1,False,False),(2,True,False),(4,False,True),(6,True,True),(0xffffffff,True,True)]:
 r=interpret({'mode':'normal','registers':{'UVD_STATUS':value}});f=r['decoded']['UVD_STATUS']['fields'];check('status_'+hex(value),f['reference_ready_bit']==ready and f['driver_busy_bit']==busy and not r['execution_proven'])
r=interpret({'registers':{'UVD_VCPU_CNTL':0x200,'UVD_SOFT_RESET':8}});check('clock_request_does_not_clear_reset',r['decoded']['UVD_VCPU_CNTL']['fields']['clock_enable_requested'] and r['decoded']['UVD_SOFT_RESET']['fields']['vcpu_reset_requested'] and not r['execution_proven'])
r=interpret({'registers':{'UVD_VCPU_CNTL':0xc0,'UVD_SOFT_RESET':0x80000}});check('reset_request_and_status_are_distinct',not r['decoded']['UVD_SOFT_RESET']['fields']['vcpu_reset_requested'] and r['decoded']['UVD_SOFT_RESET']['fields']['vcpu_vclk_reset_status_bit'])
r=interpret({'mode':'dpg-indirect-table','registers':{'UVD_LMI_VCPU_CACHE_64BIT_BAR_LOW':0,'UVD_LMI_VCPU_CACHE_64BIT_BAR_HIGH':0,'UVD_VCPU_CACHE_SIZE0':0}});check('indirect_zero_is_not_failure',not r['hardware_failure_proven'] and any('placeholders' in x for x in r['notes']))
r=interpret({'registers':{'CC_UVD_HARVESTING':3,'UVD_STATUS':2}});check('harvest_and_ready_inputs_do_not_prove_hardware',all(r['decoded']['CC_UVD_HARVESTING']['fields'].values()) and not r['execution_proven'] and not r['hardware_failure_proven'])
for value in [True,-1,0x100000000,1.5,'nonsense']:
 try:interpret({'registers':{'UVD_STATUS':value}})
 except ValueError:check('reject_'+repr(value),True)
 else:raise AssertionError(value)
for data in [{'mode':'invented'},{'registers':{'WRONG_REGISTER':2}},{'registers':[]}]:
 try:interpret(data)
 except ValueError:check('reject_schema_'+str(len(checks)),True)
 else:raise AssertionError(data)
r=interpret({'registers':{'UVD_LMI_VCPU_CACHE_64BIT_BAR_LOW':'0x12345678','UVD_LMI_VCPU_CACHE_64BIT_BAR_HIGH':'0x12345678'}});check('bar_composition_preserves_width',r['cache']['configured_bar_from_inputs']=='0x1234567812345678')
r=interpret({'register_map':'vcn_2_0_0','registers':{'UVD_VCPU_CNTL':0x10000000,'UVD_RB_ARB_CTRL':8}})
check('generation_specific_bit_is_not_reset',r['decoded']['UVD_VCPU_CNTL']['fields']['cabac_mb_acc_named_bit'] and not r['decoded']['UVD_SOFT_RESET']['provided'] and not r['execution_proven'])
check('unreferenced_named_field_remains_unproven',r['decoded']['UVD_RB_ARB_CTRL']['fields']['vcpu_dis_named_bit'] and any('physical role' in n for n in r['notes']))
for data in [{'register_map':'vcn_2_5_0'},{'register_map':None},{'mode':[]}]:
 try:interpret(data)
 except ValueError:check('reject_generation_or_mode_'+str(len(checks)),True)
 else:raise AssertionError(data)
check('unspecified_map_is_declared_assumption','register_map' in interpret({})['missing_provenance'])
for raw in [0,0x10,0x40000,0x40010]:
 r=interpret({'registers':{'UVD_CGC_GATE':raw}});f=r['decoded']['UVD_CGC_GATE']['fields']
 check('separate_clock_field_'+hex(raw),f['rbc_gate_named_bit']==bool(raw&0x10) and f['vcpu_gate_named_bit']==bool(raw&0x40000) and not r['execution_proven'])
# Exhaustive combinations of named control bits, without hardware-model claims.
for status in range(256):
 r=interpret({'registers':{'UVD_STATUS':status}})
 assert r['decoded']['UVD_STATUS']['vcpu_report_field']==(status>>1) and not r['execution_proven']
result={'result':'PASS','named_controls':checks,'status_field_inputs':256,'scope':'Synthetic scalar interpretation; no external or live capture tested'}
Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(checks),'named controls and 256 status inputs')
