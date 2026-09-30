"""Source-only call/return and platform support audit; no driver execution."""
import argparse,hashlib,json,re
from pathlib import Path

def audit(root,local=None):
 base=root/'drivers/gpu/drm/amd';sources={};findings=[]
 def source(path):
  f=base/path;b=f.read_bytes();sources[path]={'path':'drivers/gpu/drm/amd/'+path,'sha256':hashlib.sha256(b).hexdigest()};return b.decode()
 def proof(path,label,pattern):
  t=source(path);m=re.search(pattern,t,re.S);assert m,(path,label)
  findings.append({'claim':label,'path':'drivers/gpu/drm/amd/'+path,'line':t.count('\n',0,m.start())+1,'matched_source':m.group(0)})
 proof('amdgpu/amdgpu_discovery.c','upstream VCN2.0.3 registration branch adds no IP block',r'case IP_VERSION\(2, 0, 3\):\s*break;\s*case IP_VERSION\(2, 5, 0\):')
 proof('amdgpu/amdgpu_discovery.c','Cyan source has discovery-based and static-assignment IP provenance branches',r'case CHIP_CYAN_SKILLFISH:\s*if \(adev->apu_flags & AMD_APU_IS_CYAN_SKILLFISH2\) \{.*?amdgpu_discovery_reg_base_init\(adev\);.*?\} else \{\s*cyan_skillfish_reg_base_init\(adev\);.*?adev->ip_versions\[UVD_HWIP\]\[0\] = IP_VERSION\(2, 0, 3\);')
 proof('amdgpu/nv.c','GC10.1.3/10.1.4 default cg and pg flags are zero',r'case IP_VERSION\(10, 1, 3\):\s*case IP_VERSION\(10, 1, 4\):\s*adev->cg_flags = 0;\s*adev->pg_flags = 0;')
 proof('amdgpu/amdgpu_device.c','global pg mask removes existing flags',r'adev->pg_flags &= amdgpu_pg_mask;')
 proof('amdgpu/vcn_v2_0.c','normal hardware init invokes ring test helper',r'r = amdgpu_ring_test_helper\(ring\);\s*if \(r\)\s*return r;')
 proof('amdgpu/vcn_v2_0.c','VCN2 uses specialized packet-start ring test',r'\.test_ring = vcn_v2_0_dec_ring_test_ring,')
 proof('amdgpu/vcn_v2_0.c','VCN2 ring begin-use is generic VCN helper',r'\.begin_use = amdgpu_vcn_ring_begin_use,')
 proof('amdgpu/amdgpu_ring.c','ring allocation invokes void begin_use then returns zero',r'if \(ring->funcs->begin_use\)\s*ring->funcs->begin_use\(ring\);\s*return 0;')
 proof('amdgpu/amdgpu_vcn.c','begin-use ignores set_pg_state return',r'void amdgpu_vcn_ring_begin_use\(struct amdgpu_ring \*ring\).*?mutex_lock\(&vcn_inst->vcn_pg_lock\);\s*vcn_inst->set_pg_state\(vcn_inst, AMD_PG_STATE_UNGATE\);')
 proof('amdgpu/vcn_v2_0.c','set_pg_state only updates bookkeeping after start/stop success',r'if \(state == AMD_PG_STATE_GATE\)\s*ret = vcn_v2_0_stop\(vinst\);\s*else\s*ret = vcn_v2_0_start\(vinst\);\s*if \(!ret\)\s*vinst->cur_state = state;\s*return ret;')
 proof('pm/amdgpu_dpm.c','DPM enable helper logs error but returns void',r'void amdgpu_dpm_enable_vcn\(struct amdgpu_device \*adev, bool enable, int inst\).*?\n}')
 proof('pm/swsmu/amdgpu_smu.c','missing VCN enable callback returns zero',r'if \(!smu->ppt_funcs->dpm_set_vcn_enable\)\s*return 0;')
 proof('pm/swsmu/amdgpu_smu.c','VCN absence/invalidity skips power operation',r'if \(!is_vcn_enabled\(smu->adev\)\)\s*return 0;')
 text=source('pm/swsmu/smu11/cyan_skillfish_ppt.c');table=re.search(r'static const struct pptable_funcs cyan_skillfish_ppt_funcs = \{(.*?)\n};',text,re.S);assert table and 'dpm_set_vcn_enable' not in table.group(1)
 findings.append({'claim':'Cyan static pptable initializer has no dpm_set_vcn_enable member','path':'drivers/gpu/drm/amd/pm/swsmu/smu11/cyan_skillfish_ppt.c','line':text.count('\n',0,table.start())+1,'initializer_sha256':hashlib.sha256(table.group(0).encode()).hexdigest(),'absence_scope':'this complete initializer only'})
 local_evidence=[]
 if local:
  f=local/'drivers/gpu/drm/amd/amdgpu/vcn_v2_0.c';t=f.read_text()
  for label,pattern in [('start explicitly rejects Cyan',r'static int vcn_v2_0_start\([^)]*\)\s*\{\s*if \(vcn_v2_0_is_cyan_2_0_3\(vinst->adev\)\)\s*return -EOPNOTSUPP;'),('hw_init skips Cyan',r'static int vcn_v2_0_hw_init\([^)]*\)\s*\{\s*if \(vcn_v2_0_is_cyan_2_0_3\(ip_block->adev\)\) \{.*?return 0;')]:
   m=re.search(pattern,t,re.S);assert m;local_evidence.append({'claim':label,'line':t.count('\n',0,m.start())+1,'matched_source':m.group(0)})
  local_evidence.append({'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'scope':'retained R152 working source, not an assertion about the current loaded module'})
 return {'result':'PASS','classification':'PROVEN_STATICALLY','source_files':list(sources.values()),'findings':findings,'retained_local_source':local_evidence,'conclusions':['Normal VCN2 reference startup is not upstream native enablement of VCN2.0.3','Cyan source defaults do not select DPG; an external custom configuration still needs attribution','Ring allocation returning zero does not propagate or prove VCPU startup success','Successful absent-callback return is not physical power evidence','Retained diagnostic source deliberately avoids VCPU startup for Cyan'],'limitations':['No live module or power-state measurement','No claim that an external custom BIOS/kernel uses these branches','No silicon-disable semantics derived from software omission','No hardware test or new kernel patch prepared']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--local-source-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root,a.local_source_root);a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['findings']),'source contract checks')
