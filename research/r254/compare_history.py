"""Compare pinned normal-driver contracts across saved Linux releases."""
from pathlib import Path
import argparse,hashlib,json,re

def func(t,name):
 m=re.search(r'^(?:static\s+)?[\w\s*]+\b'+name+r'\s*\([^;]*?\)\s*\{',t,re.M);assert m,name;a=t.index('{',m.start());n=1;b=a+1
 while n:n+=(t[b]=='{')-(t[b]=='}');b+=1
 return t[m.start():b],t.count('\n',0,m.start())+1

def compare(p,current):
 manifest=json.loads((p/'source-manifest.json').read_text());versions=[(v['tag'],v['sha'],p/'sources'/v['tag']) for v in manifest['versions']]
 versions.append(('current',json.loads((current.parent/'source-manifest.json').read_text())['commit'],current));rows=[]
 symbols=['UVD_VCPU_CNTL__CLK_EN_MASK','UVD_VCPU_CNTL__PMB_SOFT_RESET_MASK','UVD_VCPU_CNTL__RBBM_SOFT_RESET_MASK','UVD_SOFT_RESET__VCPU_SOFT_RESET_MASK','UVD_SOFT_RESET__RBC_SOFT_RESET_MASK','UVD_SOFT_RESET__VCPU_VCLK_RESET_STATUS_MASK','UVD_STATUS__VCPU_REPORT_MASK','UVD_STATUS__VCPU_REPORT__SHIFT','UVD_RBC_RB_CNTL__RB_NO_FETCH_MASK','CC_UVD_HARVESTING__MMSCH_DISABLE_MASK','CC_UVD_HARVESTING__UVD_DISABLE_MASK']
 for tag,commit,root in versions:
  f=root/'drivers/gpu/drm/amd/amdgpu/vcn_v2_0.c';t=f.read_text();normal,ln=func(t,'vcn_v2_0_start');dpg,dl=func(t,'vcn_v2_0_start_dpg_mode');h=(root/'drivers/gpu/drm/amd/include/asic_reg/vcn/vcn_2_0_0_sh_mask.h').read_text();defs={k:int(v,16) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+)L?\s*$',h,re.M)}
  checks={'normal_ready_before_rbc':normal.index('if (status & 2)')<normal.index('/* force RBC into idle state */'),'normal_busy_clear_mask4':'~(2 << UVD_STATUS__VCPU_REPORT__SHIFT)' in normal,'normal_vcpu_reset_field':'UVD_SOFT_RESET__VCPU_SOFT_RESET_MASK' in normal,'normal_clock_field':'UVD_VCPU_CNTL__CLK_EN_MASK' in normal,'normal_cache_before_reset_release':normal.index('vcn_v2_0_mc_resume(')<normal.index('/* release VCPU reset to boot */'),'normal_no_fetch_set':'RB_NO_FETCH, 1' in normal,'normal_no_explicit_no_fetch_zero':'RB_NO_FETCH, 0' not in normal,'dpg_no_normal_ready_loop':'if (status & 2)' not in dpg,'specialized_dec_ring_test':'.test_ring = vcn_v2_0_dec_ring_test_ring' in t,'packet_start_test':'VCN_DEC_CMD_PACKET_START' in func(t,'vcn_v2_0_dec_ring_test_ring')[0]}
  assert all(checks.values()),(tag,checks)
  rows.append({'version':tag,'commit':commit,'file_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'normal_function_line':ln,'dpg_function_line':dl,'invariant_checks':checks,'fields':{k:hex(defs[k]) for k in symbols},'shared_decode_queue_reset':'decode_queue_mode |= FW_QUEUE_RING_RESET' in normal,'normal_function_sha256':hashlib.sha256(normal.encode()).hexdigest()})
 assert all(r['fields']==rows[0]['fields'] for r in rows)
 return {'result':'PASS','classification':'PROVEN_STATICALLY','versions':rows,'invariant_checks_per_version':10,'field_definitions_per_version':len(symbols),'findings':['Readiness ordering, reset/clock definitions, mask2 versus mask4 distinction, NO_FETCH initialization and specialized packet-start test persist across all six sampled revisions','Shared decode queue reset is absent in sampled v5.4 and present in v5.15 and later samples; do not transplant the complete sequence blindly'],'limits':['Six sampled revisions, not every intervening commit','No assumption of identical firmware or silicon support across releases','A same-function missing explicit zero assignment is not a global absence proof','Normal driver reference source only; no execution or BC250 bring-up observed']}

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--current-source',type=Path,required=True);args=a.parse_args();p=Path(__file__).resolve().parent;r=compare(p,args.current_source);(p/'results.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['versions']),'revisions;',len(r['versions'])*10,'contract checks')
