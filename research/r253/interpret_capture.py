"""Interpret supplied register *values* offline. No collection, MMIO or writes.

All conclusions describe input bits or missing evidence, never PROVEN_LIVE.
Input may deliberately omit values; absence is not read as zero.
"""
import argparse,json
from pathlib import Path
MODES={'normal','dpg-direct','dpg-indirect-table','sriov','unknown'}
REFERENCE_MAP='vcn_2_0_0'
FIELDS={
 'UVD_VCPU_CNTL':{'clock_enable_requested':0x200,'pmb_reset_requested':0x40,'rbbm_reset_requested':0x80,'cabac_mb_acc_named_bit':0x10000000},
 'UVD_SOFT_RESET':{'vcpu_reset_requested':8,'rbc_reset_requested':1,'vcpu_vclk_reset_status_bit':0x80000,'lmi_reset_requested':4,'lmi_umc_reset_requested':0x2000},
 'UVD_STATUS':{'reference_ready_bit':2,'driver_busy_bit':4,'rbc_busy_bit':1},
 'UVD_RBC_RB_CNTL':{'no_fetch_bit':0x10000,'no_update_bit':0x1000000,'rptr_write_enable_bit':0x10000000},
 'CC_UVD_HARVESTING':{'mmsch_disable_bit':1,'uvd_disable_bit':2},
 'UVD_RB_ARB_CTRL':{'vcpu_dis_named_bit':8},
 'UVD_CGC_GATE':{'rbc_gate_named_bit':0x10,'vcpu_gate_named_bit':0x40000},
 'UVD_CGC_CTRL':{'dynamic_clock_mode_named_bit':1,'rbc_mode_named_bit':0x100000,'vcpu_mode_named_bit':0x20000000},
 'UVD_LMI_CTRL2':{'stall_arb_umc_named_bit':0x100}}
SCALARS={'UVD_LMI_VCPU_CACHE_64BIT_BAR_LOW','UVD_LMI_VCPU_CACHE_64BIT_BAR_HIGH','UVD_VCPU_CACHE_OFFSET0','UVD_VCPU_CACHE_SIZE0','UVD_RBC_RB_RPTR','UVD_RBC_RB_WPTR'}

def u32(x):
 if x is None:return None
 if isinstance(x,bool):raise ValueError('Boolean is not a register value')
 if isinstance(x,str):
  try:x=int(x,0)
  except ValueError as e:raise ValueError('Invalid numeric string') from e
 if not isinstance(x,int) or not 0<=x<=0xffffffff:raise ValueError('Expected an unsigned 32-bit register value')
 return x

def interpret(data):
 if not isinstance(data,dict):raise ValueError('Expected object')
 register_map=data.get('register_map',REFERENCE_MAP)
 if register_map!=REFERENCE_MAP:raise ValueError('Only the vcn_2_0_0 reference map is supported; exact hardware applicability remains unverified')
 mode=data.get('mode','unknown')
 if not isinstance(mode,str) or mode not in MODES:raise ValueError('Unknown mode')
 regs=data.get('registers',{})
 if not isinstance(regs,dict):raise ValueError('registers must be an object')
 unknown=set(regs)-set(FIELDS)-SCALARS
 if unknown:raise ValueError('Unknown register symbols: '+','.join(sorted(unknown)))
 values={k:u32(v) for k,v in regs.items()};decoded={};notes=[]
 if 'register_map' not in data:notes.append('Using vcn_2_0_0 reference definitions by default; the input did not identify a register map')
 notes.append('Reference decoding does not establish exact BC2502.0.3 silicon applicability')
 if values.get('UVD_VCPU_CNTL') is not None and values['UVD_VCPU_CNTL']&0x10000000:notes.append('Bit0x10000000 is CABAC_MB_ACC in this map, not the BLK_RST field used in later VCN generations')
 if values.get('UVD_RB_ARB_CTRL') is not None:notes.append('VCPU_DIS is a named field only; inspected VCN2.0 source does not reference it, and its physical role here is unproven')
 if any(values.get(k) is not None for k in ['UVD_CGC_GATE','UVD_CGC_CTRL','UVD_LMI_CTRL2']):notes.append('Clock-controller and LMI fields are named input bits; physical clocks, power domains and memory progress are not measured')
 for reg,fields in FIELDS.items():
  v=values.get(reg)
  decoded[reg]={'provided':v is not None,'raw':None if v is None else hex(v),'fields':{n:None if v is None else bool(v&m) for n,m in fields.items()}}
  if v==0xffffffff:notes.append(reg+': all-ones input; read validity is not established by this decoder')
 if values.get('UVD_STATUS') is not None:
  v=values['UVD_STATUS'];decoded['UVD_STATUS']['vcpu_report_field']=(v&0xfe)>>1
  if v&2:notes.append('Input satisfies normal-source readiness predicate; origin, freshness, read validity and actual execution remain unverified')
  if v&4:notes.append('Busy bit can be driver-written; do not infer autonomous VCPU activity')
 lo=values.get('UVD_LMI_VCPU_CACHE_64BIT_BAR_LOW');hi=values.get('UVD_LMI_VCPU_CACHE_64BIT_BAR_HIGH')
 base=None if lo is None or hi is None else (hi<<32)|lo
 cache={'configured_bar_from_inputs':None if base is None else hex(base),'offset0':values.get('UVD_VCPU_CACHE_OFFSET0'),'size0':values.get('UVD_VCPU_CACHE_SIZE0'),'backing_bytes_verified':False,'instruction_fetch_proven':False}
 if mode=='dpg-indirect-table':notes.append('Indirect DPG table zeros can be placeholders; do not interpret this table as final live mappings')
 elif base==0:notes.append('Zero configured BAR in supplied values needs load-path/provenance analysis; no physical failure or universal invalid-address rule inferred')
 if values.get('UVD_RBC_RB_CNTL') is not None and values['UVD_RBC_RB_CNTL']&0x10000:notes.append('Reference start code sets NO_FETCH during initialization; an isolated set bit does not uniquely diagnose a defect')
 if 'CC_UVD_HARVESTING' in values:notes.append('Harvest field names do not specify whole-block power isolation or the pre-ABL writer')
 required=['register_map','source_revision','module_identity','firmware_identity','boot_context','capture_phase','mapping_provenance','read_method','load_mode']
 missing=[k for k in required if not isinstance(data.get(k),str) or not data[k].strip()]
 if mode=='unknown':missing.append('mode')
 return {'classification':'PROVEN_STATICALLY','scope':'Decoding supplied scalar values only; no hardware access or authenticity verification','register_map':register_map,'mode':mode,'decoded':decoded,'cache':cache,'missing_provenance':missing,'notes':notes,'execution_proven':False,'hardware_failure_proven':False,'external_capture_authenticity':'UNPROVEN'}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=interpret(json.loads(a.input.read_text()));a.output.write_text(json.dumps(r,indent=2)+'\n')
