"""Source-only audit of VCN idle/stop phases and conditional error residue."""
import argparse,hashlib,json,re
from pathlib import Path

def function(text,name):
    match=re.search(r'^(?:static\s+)?[\w\s*]+\b'+re.escape(name)+r'\s*\([^;]*?\)\s*\{',text,re.M);assert match,name
    pos=text.index('{',match.start())+1;depth=1
    while depth:depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
    return text[match.start():pos],text.count('\n',0,match.start())+1

def audit(root):
    prefix='drivers/gpu/drm/amd/amdgpu/';names=['vcn_v2_0.c','amdgpu_vcn.c','amdgpu_vcn.h']
    texts={n:(root/(prefix+n)).read_text() for n in names};rows=[]
    def witness(file,fn,claim,pattern):
        body,line=function(texts[file],fn);m=re.search(pattern,body,re.S);assert m,(fn,claim)
        rows.append({'claim':claim,'path':prefix+file,'function':fn,'line':line+body.count('\n',0,m.start()),'matched_source':m.group()})
        return body
    m=re.search(r'#define VCN_IDLE_TIMEOUT\s+msecs_to_jiffies\(1000\)',texts['amdgpu_vcn.h']);assert m
    rows.append({'claim':'nominal idle-work delay is1000ms converted to jiffies','path':prefix+'amdgpu_vcn.h','line':texts['amdgpu_vcn.h'].count('\n',0,m.start())+1,'matched_source':m.group()})
    witness('amdgpu_vcn.c','amdgpu_vcn_ring_end_use','last submission release schedules delayed idle work',
            r'if \(atomic_dec_and_test\(&ring->adev->vcn.inst\[ring->me\].total_submission_cnt\)\)\s*schedule_delayed_work\([^;]+VCN_IDLE_TIMEOUT\);')
    witness('amdgpu_vcn.c','amdgpu_vcn_ring_begin_use','first new submission cancels idle work synchronously',
            r'if \(!atomic_fetch_inc\(&vcn_inst->total_submission_cnt\)\)\s*cancel_delayed_work_sync\(&vcn_inst->idle_work\);')
    witness('amdgpu_vcn.c','amdgpu_vcn_ring_begin_use','begin-use requests ungate under the per-instance lock',
            r'mutex_lock\(&vcn_inst->vcn_pg_lock\);\s*vcn_inst->set_pg_state\(vcn_inst, AMD_PG_STATE_UNGATE\);')
    witness('amdgpu_vcn.c','amdgpu_vcn_idle_work_handler','idle worker requests gate only after no pending fences and no submissions',
            r'if \(!fences && !atomic_read\(&vcn_inst->total_submission_cnt\)\) \{\s*mutex_lock\(&vcn_inst->vcn_pg_lock\);\s*vcn_inst->set_pg_state\(vcn_inst, AMD_PG_STATE_GATE\);')
    witness('amdgpu_vcn.c','amdgpu_vcn_idle_work_handler','idle worker ignores gate return and releases its profile reference',
            r'vcn_inst->set_pg_state\(vcn_inst, AMD_PG_STATE_GATE\);\s*mutex_unlock\(&vcn_inst->vcn_pg_lock\);\s*amdgpu_vcn_put_profile\(adev\);')
    stop=witness('vcn_v2_0.c','vcn_v2_0_stop','DPG stop takes a distinct path to the final power-off section',
            r'if \(adev->pg_flags & AMD_PG_SUPPORT_VCN_DPG\) \{\s*r = vcn_v2_0_stop_dpg_mode\(vinst\);\s*if \(r\)\s*return r;\s*goto power_off;')
    witness('vcn_v2_0.c','vcn_v2_0_stop','normal stop first requires the idle status predicate',
            r'r = SOC15_WAIT_ON_RREG\(VCN, 0, mmUVD_STATUS, UVD_STATUS__IDLE, 0x7\);\s*if \(r\)\s*return r;')
    witness('vcn_v2_0.c','vcn_v2_0_stop','stall request precedes a checked UMC-clean wait and immediate error return',
            r'tmp \|= UVD_LMI_CTRL2__STALL_ARB_UMC_MASK;\s*WREG32_SOC15\(VCN, 0, mmUVD_LMI_CTRL2, tmp\);\s*tmp = UVD_LMI_STATUS__UMC_READ_CLEAN_RAW_MASK\|\s*UVD_LMI_STATUS__UMC_WRITE_CLEAN_RAW_MASK;\s*r = SOC15_WAIT_ON_RREG\(VCN, 0, mmUVD_LMI_STATUS, tmp, tmp\);\s*if \(r\)\s*return r;')
    witness('vcn_v2_0.c','vcn_v2_0_stop','successful normal stop explicitly clears the VCPU clock-enable request',
            r'WREG32_P\(SOC15_REG_OFFSET\(UVD, 0, mmUVD_VCPU_CNTL\), 0,\s*~\(UVD_VCPU_CNTL__CLK_EN_MASK\)\);')
    witness('vcn_v2_0.c','vcn_v2_0_stop','successful normal stop asserts VCPU reset then clears status',
            r'/\* reset VCPU \*/\s*WREG32_P\([^;]+UVD_SOFT_RESET__VCPU_SOFT_RESET_MASK[^;]+;\s*/\* clear status \*/\s*WREG32_SOC15\(VCN, 0, mmUVD_STATUS, 0\);')
    wrapper=witness('vcn_v2_0.c','vcn_v2_0_set_pg_state','same bookkeeping state returns zero before invoking start/stop',
            r'if \(state == vinst->cur_state\)\s*return 0;')
    witness('vcn_v2_0.c','vcn_v2_0_set_pg_state','bookkeeping state only changes after a successful stop/start result',
            r'if \(!ret\)\s*vinst->cur_state = state;\s*return ret;')
    power=witness('vcn_v2_0.c','vcn_v2_0_enable_static_power_gating','static power-off register configuration is conditional on the VCN PG flag',
            r'if \(adev->pg_flags & AMD_PG_SUPPORT_VCN\) \{.*?WREG32_SOC15\(VCN, 0, mmUVD_PGFSM_CONFIG, data\);')
    witness('vcn_v2_0.c','vcn_v2_0_start','normal start contains the corresponding LMI unstall request',
            r'WREG32_P\(SOC15_REG_OFFSET\(UVD, 0, mmUVD_LMI_CTRL2\), 0,\s*~UVD_LMI_CTRL2__STALL_ARB_UMC_MASK\);')
    needles=[('idle predicate','/* wait for uvd idle */'),('LMI clean predicate','tmp = UVD_LMI_STATUS__VCPU_LMI_WRITE_CLEAN_MASK'),('UMC stall request','/* stall UMC channel */'),('UMC clean predicate','tmp = UVD_LMI_STATUS__UMC_READ_CLEAN_RAW_MASK'),('clock request disabled','/* disable VCPU clock */'),('LMI UMC reset','/* reset LMI UMC */'),('LMI reset','/* reset LMI */'),('VCPU reset','/* reset VCPU */'),('status cleared','/* clear status */'),('clock gating helper','vcn_v2_0_enable_clock_gating(vinst)'),('static power gating helper','vcn_v2_0_enable_static_power_gating(vinst)'),('readback','RREG32_SOC15(VCN, 0, mmUVD_STATUS);'),('optional DPM request','amdgpu_dpm_enable_vcn(adev, false, 0)')]
    body,line=function(texts['vcn_v2_0.c'],'vcn_v2_0_stop');phases=[]
    for label,needle in needles:
        offset=body.index(needle);phases.append({'phase':label,'line':line+body.count('\n',0,offset),'offset':offset})
    assert [p['offset'] for p in phases]==sorted(p['offset'] for p in phases)
    assert wrapper.index('if (state == vinst->cur_state)')<wrapper.index('vcn_v2_0_start(vinst)')
    return {'result':'PASS','classification':'PROVEN_STATICALLY','findings':rows,'normal_stop_phases':phases,
            'source_files':[{'path':prefix+n,'sha256':hashlib.sha256((root/(prefix+n)).read_bytes()).hexdigest()} for n in names],
            'successful_stop_request_effects':{'VCPU_CNTL.CLK_EN':'cleared','SOFT_RESET.VCPU_SOFT_RESET':'asserted','UVD_STATUS':'host writes zero','physical_values_measured':False},
            'conditional_partial_stop':{'preconditions':['normal non-VF/non-DPG source path','software cur_state previously UNGATE','initial status and LMI-clean waits pass','post-stall UMC-clean wait returns an error','no intervening other state change before the later UNGATE request'],
                                        'source_consequence':'stop returns before clock-disable/reset/status-clear; cur_state remains UNGATE; later same-state UNGATE returns0 without calling start',
                                        'scope':'No explicit stall rollback in this inspected return path; no claim about autonomous hardware or other callbacks',
                                        'observed_on_hardware':False},
            'limitations':['Idle timeout is a nominal scheduling delay, not an exact observed shutdown time',
                           'A successful stopped-state snapshot does not show whether earlier startup succeeded or failed',
                           'Partial-stop reasoning is not an explanation of an initial cold-start failure without its stated preconditions',
                           'No physical clock, reset, stall, memory progress or RBC functionality measured',
                           'No wait failure induced and no hardware procedure proposed']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['findings']),'lifecycle witnesses;',len(r['normal_stop_phases']),'ordered stop phases')
