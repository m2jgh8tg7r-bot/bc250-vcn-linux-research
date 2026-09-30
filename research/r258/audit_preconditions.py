"""Source-only observations about readiness provenance and helper contracts."""
import argparse, hashlib, json, re
from pathlib import Path

def audit(root):
    base = root / 'drivers/gpu/drm/amd/amdgpu'
    texts = {name: (base / name).read_text() for name in
             ['vcn_v2_0.c', 'amdgpu_vcn.c', 'amdgpu_vcn.h']}
    findings = []
    def witness(file, label, pattern):
        text = texts[file]
        match = re.search(pattern, text, re.S)
        assert match, label
        findings.append({'claim': label, 'path': 'drivers/gpu/drm/amd/amdgpu/' + file,
                         'line': text.count('\n', 0, match.start()) + 1,
                         'matched_source': match.group()})
    witness('vcn_v2_0.c', 'busy marker preserves other input status bits at the C expression level',
            r'tmp = RREG32_SOC15\(UVD, 0, mmUVD_STATUS\) \| UVD_STATUS__UVD_BUSY;\s*WREG32_SOC15\(UVD, 0, mmUVD_STATUS, tmp\);')
    witness('vcn_v2_0.c', 'ready predicate does not itself require an observed transition',
            r'status = RREG32_SOC15\(UVD, 0, mmUVD_STATUS\);\s*if \(status & 2\)\s*break;')
    witness('vcn_v2_0.c', 'normal stop explicitly clears status after requesting VCPU reset',
            r'/\* reset VCPU \*/\s*WREG32_P\([^;]+;\s*/\* clear status \*/\s*WREG32_SOC15\(VCN, 0, mmUVD_STATUS, 0\);')
    witness('vcn_v2_0.c', 'static power helper returns void',
            r'static void vcn_v2_0_disable_static_power_gating\([^)]*\)')
    text = texts['vcn_v2_0.c']
    start = text.index('static void vcn_v2_0_disable_static_power_gating(')
    end = text.index('\n}', start) + 2
    helper = text[start:end]
    waits = re.findall(r'^\s*SOC15_WAIT_ON_RREG\([^;]+;', helper, re.M)
    assert len(waits) == 2
    assert helper.count('mmUVD_PGFSM_CONFIG, data') == 2
    findings.append({'claim': 'both static power-policy branches request PGFSM configuration and discard wait return values',
                     'path': 'drivers/gpu/drm/amd/amdgpu/vcn_v2_0.c',
                     'line': text.count('\n', 0, start) + 1,
                     'wait_calls': [x.strip() for x in waits],
                     'limitation': 'Does not establish an actual timeout or physical power transition'})
    witness('amdgpu_vcn.c', 'vcn_reset_mask returns supported reset methods, not live held-reset state',
            r'return amdgpu_show_reset_mask\(buf, adev->vcn.supported_reset\);')
    witness('vcn_v2_0.c', 'power-state wrapper can return success before invoking start or stop',
            r'if \(amdgpu_sriov_vf\(adev\)\) \{\s*vinst->cur_state = AMD_PG_STATE_UNGATE;\s*return 0;\s*\}\s*if \(state == vinst->cur_state\)\s*return 0;')
    witness('amdgpu_vcn.h', 'indirect DPG branch appends offset and value to host staging storage',
            r'\} else \{[^\n]*\\\n\s*\*adev->vcn.inst\[inst_idx\].dpg_sram_curr_addr\+\+ =.*?value;')
    witness('amdgpu_vcn.c', 'DPG SRAM update uses RAM firmware IDs and calls the PSP load helper',
            r'int amdgpu_vcn_psp_update_sram\(.*?return psp_execute_ip_fw_load\(&adev->psp, &ucode\);')
    return {'result': 'PASS', 'classification': 'PROVEN_STATICALLY',
            'source_files': [{'path': 'drivers/gpu/drm/amd/amdgpu/' + n,
                              'sha256': hashlib.sha256((base/n).read_bytes()).hexdigest()} for n in texts],
            'findings': findings,
            'conditional_scalar_examples': [
                {'input_status': hex(v), 'host_busy_expression': hex(v | 4),
                 'ready_if_value_remains_unchanged': bool((v | 4) & 2),
                 'actual_hardware_persistence_proven': False} for v in [0, 2, 4, 6, 0xffffffff]],
            'limitations': [
                'Scalar examples are not a hardware model or a demonstrated stale-status bug',
                'Power and reset side effects can change hardware status independently of host expressions',
                'No reset, power, cache or firmware request performed',
                'No-ready observations cannot exclude partial execution before a firmware handshake',
                'Current upstream reference path is not evidence of the loaded BC250 module path']}

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--source-root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True); args = p.parse_args()
    result = audit(args.source_root)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print('PASS', len(result['findings']), 'source witnesses; conditional scalar examples only')
