"""Audit reference register naming, clock fields and read provenance offline."""
import argparse, hashlib, json, re
from pathlib import Path

def audit(root):
    base=root/'drivers/gpu/drm/amd'
    paths=['amdgpu/vcn_v2_0.c','amdgpu/soc15_common.h','amdgpu/amdgpu_reg_access.c',
           'amdgpu/amdgpu_ip.h','include/asic_reg/vcn/vcn_2_0_0_sh_mask.h',
           'include/asic_reg/vcn/vcn_2_0_0_offset.h']
    paths += ['amdgpu/amdgpu_vcn.h','amdgpu/amdgpu_discovery.c','include/amd_shared.h']
    texts={p:(base/p).read_text() for p in paths}; findings=[]
    def witness(path,claim,pattern):
        text=texts[path]; match=re.search(pattern,text,re.S); assert match,claim
        findings.append(dict(claim=claim,path='drivers/gpu/drm/amd/'+path,
                             line=text.count('\n',0,match.start())+1,matched_source=match.group()))
    witness('amdgpu/amdgpu_ip.h','UVD and VCN HWIP identifiers alias in this source',r'VCN_HWIP = UVD_HWIP,')
    witness('amdgpu/soc15_common.h','SOC15 register index depends on per-IP instance base and BASE_IDX',
            r'#define SOC15_REG_OFFSET\(ip, inst, reg\)[^\n]+')
    witness('amdgpu/soc15_common.h','SOC15 read dispatches through the configured RLC register helper',
            r'#define __RREG32_SOC15_RLC__[^\n]+\n[^\n]+')
    witness('amdgpu/amdgpu_reg_access.c','amdgpu_device_rreg may return software zero before any read',
            r'uint32_t amdgpu_device_rreg\([^)]*\)\s*\{\s*uint32_t ret;\s*if \(amdgpu_device_skip_hw_access\(adev\)\)\s*return 0;')
    witness('amdgpu/amdgpu_reg_access.c','direct MMIO branch converts dword register index to byte offset',
            r'ret = readl\(\(\(void __iomem \*\)adev->rmmio\) \+ \(reg \* 4\)\);')
    witness('amdgpu/vcn_v2_0.c','normal clock helper explicitly clears dynamic-clock mode when capability absent',
            r'if \(adev->cg_flags & AMD_CG_SUPPORT_VCN_MGCG\)\s*data \|= 1 << UVD_CGC_CTRL__DYN_CLOCK_MODE__SHIFT;\s*else\s*data &= ~UVD_CGC_CTRL__DYN_CLOCK_MODE_MASK;')
    witness('amdgpu/vcn_v2_0.c','normal clock helper clears distinct RBC and VCPU gate fields',
            r'data &= ~\(UVD_CGC_GATE__SYS_MASK.*?UVD_CGC_GATE__RBC_MASK.*?UVD_CGC_GATE__VCPU_MASK.*?WREG32_SOC15\(VCN, 0, mmUVD_CGC_GATE, data\);')
    witness('amdgpu/vcn_v2_0.c','normal clock helper also clears distinct RBC and VCPU mode fields',
            r'data &= ~\(UVD_CGC_CTRL__UDEC_RE_MODE_MASK.*?UVD_CGC_CTRL__RBC_MODE_MASK.*?UVD_CGC_CTRL__VCPU_MODE_MASK.*?WREG32_SOC15\(VCN, 0, mmUVD_CGC_CTRL, data\);')
    witness('amdgpu/amdgpu_vcn.h','software VCN harvest bits identify instances, not CC register subfields',
            r'#define AMDGPU_VCN_HARVEST_VCN0 \(1 << 0\)\s*#define AMDGPU_VCN_HARVEST_VCN1 \(1 << 1\)')
    witness('include/amd_shared.h','whole-IP harvest mask uses another namespace',
            r'enum amd_harvest_ip_mask \{\s*AMD_HARVEST_IP_VCN_MASK = 0x1,\s*AMD_HARVEST_IP_JPEG_MASK = 0x2,')
    witness('amdgpu/amdgpu_discovery.c','harvest table reader maps VCN instance numbers to software bits',
            r'case VCN_HWID:\s*\(\*vcn_harvest_count\)\+\+;\s*adev->vcn.harvest_config \|= BIT\(inst\);\s*adev->jpeg.harvest_config \|= BIT\(inst\);')
    witness('amdgpu/amdgpu_discovery.c','all-instances count condition sets whole-IP software masks',
            r'if \(vcn_harvest_count == adev->vcn.num_vcn_inst\) \{\s*adev->harvest_ip_mask \|= AMD_HARVEST_IP_VCN_MASK;\s*adev->harvest_ip_mask \|= AMD_HARVEST_IP_JPEG_MASK;')
    header=texts['include/asic_reg/vcn/vcn_2_0_0_sh_mask.h']
    defs={k:int(v,16) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+)L?\s*$',header,re.M)}
    symbols={'UVD_CGC_GATE__RBC_MASK':0x10,'UVD_CGC_GATE__VCPU_MASK':0x40000,
             'UVD_CGC_CTRL__DYN_CLOCK_MODE_MASK':1,'UVD_CGC_CTRL__RBC_MODE_MASK':0x100000,
             'UVD_CGC_CTRL__VCPU_MODE_MASK':0x20000000,'UVD_LMI_CTRL2__STALL_ARB_UMC_MASK':0x100}
    assert all(defs[k]==v for k,v in symbols.items())
    names=['mmUVD_VCPU_CNTL','mmUVD_SOFT_RESET','mmUVD_STATUS','mmUVD_CGC_GATE','mmUVD_CGC_CTRL',
           'mmUVD_RB_ARB_CTRL','mmCC_UVD_HARVESTING','mmUVD_LMI_VCPU_CACHE_64BIT_BAR_LOW',
           'mmUVD_LMI_VCPU_CACHE_64BIT_BAR_HIGH','mmUVD_VCPU_CACHE_OFFSET0','mmUVD_VCPU_CACHE_SIZE0']
    off=texts['include/asic_reg/vcn/vcn_2_0_0_offset.h']; named=[]
    for name in names:
        match=re.search(r'^#define\s+'+name+r'\s+(0x[0-9a-f]+)\s*\n#define\s+'+name+r'_BASE_IDX\s+(\d+)',off,re.M)
        assert match,name
        named.append(dict(symbol=name,header_index=match.group(1),base_idx=int(match.group(2)),
                          absolute_address_computed=False,line=off.count('\n',0,match.start())+1))
    return dict(result='PASS',classification='PROVEN_STATICALLY',findings=findings,
                fields={k:hex(v) for k,v in symbols.items()},register_names=named,
                harvest_namespaces=[
                    {'name':'CC_UVD_HARVESTING reference register','bit0':'MMSCH_DISABLE','bit1':'UVD_DISABLE'},
                    {'name':'adev->vcn.harvest_config software bitmap','bit0':'VCN instance0','bit1':'VCN instance1'},
                    {'name':'adev->harvest_ip_mask software bitmap','bit0':'VCN IP','bit1':'JPEG IP'}],
                source_files=[dict(path='drivers/gpu/drm/amd/'+p,sha256=hashlib.sha256((base/p).read_bytes()).hexdigest()) for p in paths],
                limitations=['No actual mapping, read path, clock or gate state measured',
                             'Separate named fields do not specify independent physical power domains',
                             'Software-zero branch is a possibility conditional on the actual helper and state, not a diagnosis',
                             'Cache configuration symbols do not identify what an external cache-register report refers to',
                             'Software harvest table handling does not define CC register physical isolation or identify its writer',
                             'No physical addresses or acquisition commands generated'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['findings']),'provenance witnesses;',len(r['fields']),'clock/LMI fields')
