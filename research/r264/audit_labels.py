"""Inventory named cache/trace interfaces without assigning physical semantics."""
import argparse,hashlib,json,re
from pathlib import Path

def audit(root):
    base='drivers/gpu/drm/amd/include/asic_reg/vcn/'
    paths=[base+'vcn_2_0_0_offset.h',base+'vcn_2_0_0_sh_mask.h','drivers/gpu/drm/amd/amdgpu/vcn_v2_0.c','drivers/gpu/drm/amd/amdgpu/amdgpu_vcn.c']
    offset,mask,driver,common=[(root/p).read_text() for p in paths]
    offsets={k:int(v,16) for k,v in re.findall(r'^#define\s+(mm\w+)\s+(0x[0-9a-fA-F]+)\s*$',offset,re.M)}
    fields={k:int(v,16) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+)L?\s*$',mask,re.M)}
    rows=[]
    for name in sorted(offsets):
        if 'VCPU' not in name or 'CACHE' not in name:continue
        idx=re.search(r'^#define\s+'+name+r'_BASE_IDX\s+(\d+)\s*$',offset,re.M);assert idx
        rows.append({'symbol':name,'relative_dword_offset':hex(offsets[name]),'base_index':int(idx.group(1)),
                     'driver_reference_lines':[i for i,line in enumerate(driver.splitlines(),1) if re.search(r'\b'+name+r'\b',line)]})
    trace_names=['UVD_VCPU_TRCE__PC_MASK','UVD_VCPU_TRCE__PC__SHIFT','UVD_VCPU_TRCE_RD__DATA_MASK','UVD_VCPU_PRID__PRID_MASK','UVD_VCPU_CNTL__TRCE_EN_MASK','UVD_VCPU_CNTL__TRCE_MUX_MASK']
    selected={k:hex(fields[k]) for k in trace_names}
    assert selected['UVD_VCPU_TRCE__PC_MASK']=='0xfffffff'
    assert selected['UVD_VCPU_TRCE__PC__SHIFT']=='0x0'
    symbols=['mmUVD_VCPU_TRCE','mmUVD_VCPU_TRCE_RD','mmUVD_VCPU_PRID']
    usage={s:{'vcn_v2_0.c':len(re.findall(r'\b'+s+r'\b',driver)),'amdgpu_vcn.c':len(re.findall(r'\b'+s+r'\b',common))} for s in symbols}
    assert all(n==0 for d in usage.values() for n in d.values())
    assert 'UVD_VCPU_CNTL__TRCE_EN_MASK' not in driver
    return {'result':'PASS','classification':'PROVEN_STATICALLY','source_files':[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in paths],
            'cache_named_registers':rows,'trace_named_fields':selected,'bounded_driver_symbol_use':usage,
            'findings':['The cache-related names include BAR, OFFSET, SIZE and VMID configuration interfaces, including DPG and noncache variants',
                        'Header PC/trace names exist, but neither inspected driver file implements an observation contract for these three symbols',
                        'Header names alone do not specify trace enable/mux semantics, sampling, freshness, access side effects or BC250 applicability'],
            'limits':['Symbol inventory is not a complete hardware interface specification',
                      'No absolute MMIO addresses, acquisition procedure, trace activation or hardware writes are provided',
                      'No claim that an interface is absent from all other software or undocumented silicon',
                      'Cache register readback is not proof of backing-memory data access or instruction fetch',
                      'No unchanged/zero PC implication is asserted; no VCPU execution was observed']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['cache_named_registers']),'cache-related named registers;',len(r['trace_named_fields']),'trace/identity definitions')
