"""Saved-source evidence extraction only; never opens a device or live sysfs."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def audit(source, history):
    base = 'drivers/gpu/drm/amd/amdgpu/'
    specs = [
        ('sos_ioctl', base+'amdgpu_kms.c', r'case AMDGPU_INFO_FW_SOS:.*?break;'),
        ('sos_debugfs', base+'amdgpu_kms.c', r'/\* PSP SOS \*/.*?fw_info.feature, fw_info.ver\);'),
        ('sysfs_value_and_visibility', base+'amdgpu_ucode.c', r'static inline int amdgpu_ucode_is_valid.*?static DEVICE_ATTR\(name, mode, show_##name, NULL\)'),
        ('sos_sysfs_field', base+'amdgpu_ucode.c', r'FW_VERSION_ATTR\(sos_fw_version[^;]+;'),
        ('sysfs_visibility_callback', base+'amdgpu_ucode.c', r'static umode_t amdgpu_ucode_sys_visible.*?\n}'),
        ('sos_coredump', base+'amdgpu_dev_coredump.c', r'drm_printf\(p, "PSP SOS feature version:.*?adev->psp.sos.fw_version\);'),
        ('attestation_support', base+'amdgpu_fw_attestation.c', r'static int amdgpu_is_fw_attestation_supported.*?\n}'),
        ('attestation_registration', base+'amdgpu_fw_attestation.c', r'void amdgpu_fw_attestation_debugfs_init.*?\n}'),
        ('attestation_record_format', base+'amdgpu_fw_attestation.c', r'struct FW_ATT_RECORD \{.*?\n};'),
        ('attestation_requests_psp', base+'amdgpu_psp.c', r'int psp_get_fw_attestation_records_addr.*?\n}'),
        ('cyan_pci_flag', base+'amdgpu_drv.c', r'\{0x1002, 0x13FE[^\n]+'),
        ('sos_file_origin', base+'amdgpu_psp.c', r'static int psp_init_sos_base_fw.*?\n}'),
        ('other_generation_counterexample', base+'psp_v13_0.c', r'static inline void psp_v13_0_init_sos_version.*?\n}'),
        ('cyan_callback_table', base+'psp_v11_0_8.c', r'static const struct psp_funcs psp_v11_0_8_funcs = \{.*?\n};'),
        ('cyan_psp_selection', base+'amdgpu_psp.c', r'case IP_VERSION\(11, 0, 8\):.*?break;'),
    ]
    rows = []
    for label, relative, pattern in specs:
        data = (source/relative).read_bytes()
        text = data.decode()
        matches = list(re.finditer(pattern, text, re.S))
        assert len(matches) == 1, (label, len(matches))
        m = matches[0]
        rows.append(dict(label=label, path=relative, source_sha256=digest(data),
                         line=text[:m.start()].count('\n')+1, excerpt=m.group()))
    uapi = source/'include/uapi/drm/amdgpu_drm.h'
    selectors = re.findall(r'^\s*#define (AMDGPU_INFO_FW_\w+)\s+(0x[0-9a-fA-F]+)', uapi.read_text(), re.M)
    assert ('AMDGPU_INFO_FW_SOS', '0x0c') in selectors
    assert not any('KDB' in name or 'SERVICE' in name for name, _ in selectors)
    saved = history.read_bytes()
    matches = [dict(line=i, text=line) for i, line in enumerate(saved.decode().splitlines(), 1)
               if line.startswith('SOS feature version:')]
    assert matches == [dict(line=4450, text='SOS feature version: 0, firmware version: 0x00000000')]
    return dict(result='PASS', classification='PROVEN_STATICALLY',
                scope='Exact saved source and historical text; no live API invocation',
                sources=rows, firmware_selectors=selectors, uapi_sha256=digest(uapi.read_bytes()),
                historical_sos=dict(source=history.name, sha256=digest(saved), matches=matches,
                                    attribution='Historical recorded output; not a new measurement or same-boot attribution'),
                limits=['No universal absence claim for all possible interfaces',
                        'PSP 13 has a register-backed version producer: conclusions are Cyan/version-specific',
                        'Absent sysfs value does not imply absent running SOS',
                        'No KDB selector in this bounded UAPI selector list'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--history', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = audit(a.source, a.history)
    a.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'result':result['result'], 'source_excerpts':len(result['sources']),
                      'firmware_selectors':len(result['firmware_selectors'])}))
