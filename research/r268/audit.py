"""Bounded, reproducible source witnesses; no hardware access."""
from pathlib import Path
import argparse,hashlib,json
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--source-root',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
src=args.source_root
paths=['drivers/gpu/drm/amd/amdgpu/vcn_v2_0.c','drivers/gpu/drm/amd/include/asic_reg/vcn/vcn_2_0_0_sh_mask.h']
files={p:(src/p).read_text() for p in paths}
c=files[paths[0]];h=files[paths[1]]
start=c.index('static int vcn_v2_0_process_interrupt(');end=c.index('\nint vcn_v2_0_dec_ring_test_ring(',start)
irq=c[start:end]
assert irq.count('amdgpu_fence_process(')==3
assert 'entry->src_id' in irq and 'entry->src_data[0]' in irq
assert 'mmUVD_SYS_INT_STATUS' not in c and 'mmUVD_VCPU_INT_ACK' not in c
assert c.count('mmUVD_LMI_STATUS')==2
assert 'UVD_LMI_STATUS__VCPU_LMI_WRITE_CLEAN_MASK' in c
symbols=['UVD_SYS_INT_STATUS__PIF_ADDR_ERR_INT_MASK','UVD_SYS_INT_STATUS__RBC_REG_PRIV_FAULT_INT_MASK','UVD_LMI_STATUS__VCPU_LMI_WRITE_CLEAN_MASK','UVD_LMI_STATUS__UMC_READ_CLEAN_RAW_MASK']
witnesses=[]
for symbol in symbols:
 matches=[{'line':i,'text':line} for i,line in enumerate(h.splitlines(),1) if line.startswith('#define '+symbol+' ')]
 assert len(matches)==1
 witnesses.append({'path':paths[1],'symbol':symbol,**matches[0]})
for token in ['mmUVD_LMI_STATUS','amdgpu_fence_process(&adev->vcn.inst->ring']:
 for i,line in enumerate(c.splitlines(),1):
  if token in line:witnesses.append({'path':paths[0],'line':i,'text':line.strip()})
r={'result':'PROVEN_STATICALLY','commit':'551c722f40809618230001baccf219193e22fc5a' ,'scope':'Two pinned source files; lexical witnesses, not hardware semantics verification','files':[{ 'path':p,'sha256':hashlib.sha256((src/p).read_bytes()).hexdigest()} for p in paths],'witnesses':witnesses,'checks':{'three_fence_dispatch_calls':True,'two_lmi_status_sites':True,'sys_status_and_ack_not_used_in_this_driver':True},'hardware_access':False}
args.output.write_text(json.dumps(r,indent=2)+'\n')
print('PASS bounded source witnesses')
