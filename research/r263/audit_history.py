"""Compare limited lifecycle/test contracts, not whole-driver equivalence."""
import argparse,hashlib,json,re
from pathlib import Path

def function(text,name):
    m=re.search(r'^(?:static\s+)?[\w\s*]+\b'+re.escape(name)+r'\s*\([^;]*?\)\s*\{',text,re.M)
    assert m,name
    pos=text.index('{',m.start())+1;depth=1
    while depth:depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
    return text[m.start():pos],text.count('\n',0,m.start())+1

def audit(history,current):
    manifest=json.loads((history/'source-manifest.json').read_text())
    versions=[(v['tag'],v['sha'],history/'sources'/v['tag']) for v in manifest['versions']]
    versions.append(('current',json.loads((current.parent/'source-manifest.json').read_text())['commit'],current))
    rows=[];prefix='drivers/gpu/drm/amd/amdgpu/'
    for tag,commit,root in versions:
        paths=[prefix+'vcn_v2_0.c',prefix+'amdgpu_vcn.c'];texts=[(root/p).read_text() for p in paths];v,c=texts
        names=['vcn_v2_0_stop','vcn_v2_0_start']
        wrapper='vcn_v2_0_set_pg_state' if 'static int vcn_v2_0_set_pg_state(' in v else 'vcn_v2_0_set_powergating_state'
        bodies={name:function(v,name) for name in names+[wrapper]}
        for name in ['amdgpu_vcn_ring_begin_use','amdgpu_vcn_idle_work_handler','amdgpu_vcn_dec_ring_test_ib','amdgpu_vcn_enc_ring_test_ib']:
            bodies[name]=function(c,name)
        stop=bodies['vcn_v2_0_stop'][0];start=bodies['vcn_v2_0_start'][0];wrap=bodies[wrapper][0]
        begin=bodies['amdgpu_vcn_ring_begin_use'][0];idle=bodies['amdgpu_vcn_idle_work_handler'][0]
        checks={}
        def check(key,value):assert value,(tag,key);checks[key]=True
        markers=['/* stall UMC channel */','tmp = UVD_LMI_STATUS__UMC_READ_CLEAN_RAW_MASK','/* disable VCPU clock */','/* reset VCPU */','/* clear status */']
        offsets=[stop.index(x) for x in markers]
        check('stop_phase_order',offsets==sorted(offsets))
        segment=stop[offsets[0]:offsets[2]]
        check('stall_before_checked_umc_wait',bool(re.search(r'STALL_ARB_UMC_MASK;.*?SOC15_WAIT_ON_RREG\(VCN, 0, mmUVD_LMI_STATUS, tmp, tmp(?:, r)?\);\s*if \(r\)\s*return r;',segment,re.S)))
        check('stop_disables_clock',bool(re.search(r'WREG32_P\(SOC15_REG_OFFSET\(UVD, 0, mmUVD_VCPU_CNTL\), 0,\s*~\(UVD_VCPU_CNTL__CLK_EN_MASK\)\);',stop)))
        check('stop_asserts_vcpu_reset_then_zero_status',bool(re.search(r'/\* reset VCPU \*/\s*WREG32_P\([^;]+UVD_SOFT_RESET__VCPU_SOFT_RESET_MASK[^;]+;\s*/\* clear status \*/\s*WREG32_SOC15\(VCN, 0, mmUVD_STATUS, 0\);',stop)))
        check('wrapper_same_state_guard_before_start',bool(re.search(r'if \(state == [^\n]+cur_state\)\s*return 0;',wrap)) and wrap.index('if (state ==')<wrap.index('vcn_v2_0_start('))
        check('wrapper_state_only_on_success',bool(re.search(r'if \(!ret\)\s*[^\n]+cur_state = state;',wrap)))
        check('start_contains_unstall_request',bool(re.search(r'WREG32_P\(SOC15_REG_OFFSET\(UVD, 0, mmUVD_LMI_CTRL2\), 0,\s*~UVD_LMI_CTRL2__STALL_ARB_UMC_MASK\);',start)))
        for name,short in [('amdgpu_vcn_dec_ring_test_ib','decode'),('amdgpu_vcn_enc_ring_test_ib','encode')]:
            body=bodies[name][0]
            check(short+'_positive_wait_maps_to_zero',bool(re.search(r'dma_fence_wait_timeout\(fence, false, timeout\);\s*if \(r == 0\)\s*r = -ETIMEDOUT;\s*else if \(r > 0\)\s*r = 0;',body)))
            check(short+'_no_completion_error_query','dma_fence_get_status' not in body and 'fence->error' not in body)
        state_prefix='per-instance' if 'vinst->cur_state' in wrap else 'device-wide VCN'
        variation={
            'state_storage':state_prefix,
            'wait_result_form':'output argument' if 'tmp, tmp, r)' in segment else 'assignment',
            'begin_submission_counter':'total_submission_cnt' in begin,
            'begin_cancel_only_first_submission':'atomic_fetch_inc' in begin,
            'begin_has_pg_lock':'mutex_lock(' in begin,
            'idle_has_pg_lock':'mutex_lock(' in idle,
            'idle_submission_counter_predicate':'total_submission_cnt' in idle,
            'legacy_uvd_dpm_branch':'amdgpu_dpm_enable_uvd' in begin,
            'begin_power_profile_helper':'amdgpu_vcn_get_profile' in begin,
            'vf_wrapper_shortcut':'amdgpu_sriov_vf' in wrap,
        }
        rows.append({'version':tag,'commit':commit,'source_files':[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in paths],
                     'invariant_checks':checks,'lifecycle_variations':variation,
                     'function_witnesses':[{'function':n,'line':line,'sha256':hashlib.sha256(body.encode()).hexdigest()} for n,(body,line) in bodies.items()]})
    return {'result':'PASS','classification':'PROVEN_STATICALLY','versions':rows,'checks_per_revision':11,
            'findings':['The limited normal-stop ordering, conditional local return and wrapper bookkeeping pattern persist in all six samples',
                        'Decode and encode IB tests map positive wait returns to success without their own completion-error queries in all six samples',
                        'Idle locking, submission accounting, callback routing and state storage differ; do not transplant the entire current lifecycle'],
            'limits':['Six samples only, not an introduction or regression bisection',
                      'Old wait-macro result plumbing differs; this audit checks call-site use, not full historical macro implementations',
                      'Historical fence internals and full reachability chains are not re-proven; R261 complete fence reasoning is for its current pin',
                      'No hardware failure or vulnerable condition reproduced; no physical diagnosis from source invariants']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--history-root',type=Path,required=True);p.add_argument('--current-source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=audit(a.history_root,a.current_source);a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['versions']),'revisions;',r['checks_per_revision'],'bounded checks per revision')
