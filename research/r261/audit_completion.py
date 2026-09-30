"""Audit normal VCN2 test/completion attribution without executing a driver."""
import argparse,hashlib,json,re
from pathlib import Path

def function(text,name):
    match=re.search(r'^(?:static\s+)?(?:inline\s+)?[\w\s*]+\b'+re.escape(name)+r'\s*\([^;]*?\)\s*\{',text,re.M)
    assert match,name
    start=text.index('{',match.start());pos=start+1;depth=1
    while depth:depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
    return text[match.start():pos],text.count('\n',0,match.start())+1

def audit(root):
    base='drivers/gpu/drm/amd/amdgpu/'
    paths=[base+x for x in ['vcn_v2_0.c','amdgpu_vcn.c','amdgpu_job.c','amdgpu_ib.c','amdgpu_fence.c','amdgpu_ring.c']]+['drivers/dma-buf/dma-fence.c','include/linux/dma-fence.h']
    texts={p:(root/p).read_text() for p in paths};rows=[];bounded=[]
    def check(path,fn,claim,pattern):
        body,line=function(texts[path],fn);match=re.search(pattern,body,re.S);assert match,(fn,claim)
        rows.append({'claim':claim,'path':path,'function':fn,'line':line+body.count('\n',0,match.start()),'matched_source':match.group()})
        return body
    check(base+'vcn_v2_0.c','vcn_v2_0_dec_ring_get_wptr','doorbell write-pointer getter returns host shadow memory',
          r'if \(ring->use_doorbell\)\s*return \*ring->wptr_cpu_addr;\s*else\s*return RREG32_SOC15\(UVD, 0, mmUVD_RBC_RB_WPTR\);')
    check(base+'vcn_v2_0.c','vcn_v2_0_dec_ring_test_ring','VF scratch-test path returns zero without executing the test',
          r'if \(amdgpu_sriov_vf\(adev\)\)\s*return 0;')
    check(base+'amdgpu_ring.c','amdgpu_ring_test_helper','scheduler readiness is assigned from the scratch-test return',r'ring->sched.ready = !r;')
    check(base+'amdgpu_ib.c','amdgpu_ib_ring_tests','aggregate IB testing skips rings not ready or without a test callback',
          r'if \(!ring->sched.ready \|\| !ring->funcs->test_ib\)\s*continue;')
    for name in ['amdgpu_vcn_dec_ring_test_ib','amdgpu_vcn_enc_ring_test_ib']:
        body=check(base+'amdgpu_vcn.c',name,'positive fence wait maps to test success',
              r'r = dma_fence_wait_timeout\(fence, false, timeout\);\s*if \(r == 0\)\s*r = -ETIMEDOUT;\s*else if \(r > 0\)\s*r = 0;')
        assert 'dma_fence_get_status' not in body and 'fence->error' not in body
        bounded.append({'function':name,'no_fence_error_query_in_complete_body':True,'function_sha256':hashlib.sha256(body.encode()).hexdigest()})
    body=check(base+'amdgpu_vcn.c','amdgpu_vcn_dec_ring_test_ib','decode IB test sends create without a returned caller fence and destroy with one',
          r'amdgpu_vcn_dec_send_msg\(ring, &ib, NULL\);.*?amdgpu_vcn_dec_get_destroy_msg\(ring, 1, &ib\);.*?amdgpu_vcn_dec_send_msg\(ring, &ib, &fence\);')
    assert 'get_create_msg' in body and 'decode_frame' not in body
    check(base+'amdgpu_vcn.c','amdgpu_vcn_dec_send_msg','message helper schedules a direct job and returns its fence reference',
          r'r = amdgpu_job_submit_direct\(job, ring, &f\);.*?if \(fence\)\s*\*fence = dma_fence_get\(f\);')
    check(base+'amdgpu_job.c','amdgpu_job_submit_direct','direct submit forwards the IB scheduling fence',
          r'r = amdgpu_ib_schedule\(ring, job->num_ibs, job->ibs, job, fence\);')
    check(base+'amdgpu_ib.c','amdgpu_ib_schedule','IB scheduler returns the emitted AMDGPU fence base',
          r'amdgpu_fence_emit\(ring, af, fence_flags\);\s*\*f = &af->base;')
    check(base+'amdgpu_fence.c','amdgpu_fence_emit','emitted fence is initialized with AMDGPU fence operations',
          r'dma_fence_init\(fence, &amdgpu_fence_ops,')
    text=texts[base+'amdgpu_fence.c'];m=re.search(r'static const struct dma_fence_ops amdgpu_fence_ops = \{(.*?)\n};',text,re.S);assert m and '.wait' not in m.group(1)
    rows.append({'claim':'AMDGPU fence operations initializer does not install a custom wait','path':base+'amdgpu_fence.c','line':text.count('\n',0,m.start())+1,'initializer_sha256':hashlib.sha256(m.group().encode()).hexdigest(),'absence_scope':'complete named initializer'})
    check('drivers/dma-buf/dma-fence.c','dma_fence_wait_timeout','no custom wait delegates to default wait',
          r'ret = dma_fence_default_wait\(fence, intr, timeout\);')
    body=check('drivers/dma-buf/dma-fence.c','dma_fence_default_wait','already-signaled fence returns positive timeout-or-one without inspecting its error field',
          r'signed long ret = timeout \? timeout : 1;.*?if \(dma_fence_test_signaled_flag\(fence\)\)\s*goto out;')
    assert 'fence->error' not in body and 'dma_fence_get_status' not in body
    check('include/linux/dma-fence.h','dma_fence_get_status_locked','completion error status is a separate query',
          r'if \(dma_fence_is_signaled_locked\(fence\)\)\s*return fence->error \?: 1;')
    check(base+'amdgpu_fence.c','amdgpu_fence_driver_force_completion','software force-completion assigns errors then writes the latest sequence and invokes processing',
          r'dma_fence_set_error\(fence, -ETIME\);.*?dma_fence_set_error\(fence, -ECANCELED\);.*?amdgpu_fence_write\(ring, ring->fence_drv.sync_seq\);\s*amdgpu_fence_process\(ring\);')
    check(base+'amdgpu_fence.c','amdgpu_fence_process','fence processing signals the fence objects it processes',r'dma_fence_signal\(fence\);')
    check(base+'amdgpu_fence.c','amdgpu_debugfs_fence_info_show','fence-info read invokes fence processing before printing',r'amdgpu_fence_process\(ring\);\s*seq_printf\(')
    v2=texts[base+'vcn_v2_0.c']
    for fn in ['amdgpu_vcn_dec_ring_test_ib','amdgpu_vcn_enc_ring_test_ib']:
        assert re.search(r'\.test_ib\s*=\s*'+fn+r'\s*,',v2),fn
    return {'result':'PASS','classification':'PROVEN_STATICALLY','findings':rows,'bounded_absence_checks':bounded,
            'source_files':[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in paths],
            'conditional_examples':[
                {'condition':'default-wait fence already signaled, positive timeout, no fence error','test_wait_result':'positive','test_return':0},
                {'condition':'default-wait fence already signaled, positive timeout, negative completion error','test_wait_result':'positive','test_return':0,'negative_completion_error_observed_by_test':False}],
            'conclusions':['IB-test success is a wait-result contract, not a decoded-frame check or an explicit completion-error check',
                           'Software force completion exists, so fence signaling needs provenance',
                           'A write-pointer callback can report a host shadow rather than an MMIO read',
                           'Reading fence debug information can process and signal existing fence state'],
            'limitations':['No claim of an observed false-positive test, VCPU execution or codec output',
                           'No evidence that reset/force-completion occurred during any external test',
                           'No fault injection, device access, recovery trigger or failure reproduction performed',
                           'Does not establish which hardware or firmware agent implements each ring command',
                           'Absence of a firmware-response check here is bounded to the inspected test/helper contract']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['findings']),'completion-contract witnesses')
