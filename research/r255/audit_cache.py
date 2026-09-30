"""Reference cache geometry for an existing saved firmware file; no loading or execution."""
from pathlib import Path
import argparse,hashlib,json,re,struct

def audit(source,firmware):
 base=source/'drivers/gpu/drm/amd/amdgpu';rows=[]
 def witness(file,label,pattern):
  p=base/file;t=p.read_text();m=re.search(pattern,t,re.S);assert m,(file,label)
  rows.append({'claim':label,'path':'drivers/gpu/drm/amd/amdgpu/'+file,'line':t.count('\n',0,m.start())+1,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'matched_source':m.group(0)})
 witness('vcn_v2_0.c','reference cache span uses full firmware file size plus4',r'uint32_t size = AMDGPU_GPU_PAGE_ALIGN\(adev->vcn.inst\[0\].fw->size \+ 4\);')
 witness('vcn_v2_0.c','PSP cache base takes TMR response bookkeeping',r'if \(adev->firmware.load_type == AMDGPU_FW_LOAD_PSP\) \{\s*WREG32_SOC15\(UVD, 0, mmUVD_LMI_VCPU_CACHE_64BIT_BAR_LOW,.*?offset = 0;')
 witness('vcn_v2_0.c','driver branch cache offset uses firmware offset divided by8',r'AMDGPU_UVD_FIRMWARE_OFFSET >> 3\);')
 witness('amdgpu_vcn.c','driver-loaded allocation reserves payload plus8 aligned',r'if \(adev->firmware.load_type != AMDGPU_FW_LOAD_PSP\)\s*bo_size \+= AMDGPU_GPU_PAGE_ALIGN\(le32_to_cpu\(hdr->ucode_size_bytes\) \+ 8\);')
 witness('amdgpu_vcn.c','driver resume copies declared payload only in nonPSP branch',r'if \(adev->firmware.load_type != AMDGPU_FW_LOAD_PSP\) \{\s*offset = le32_to_cpu\(hdr->ucode_array_offset_bytes\);.*?le32_to_cpu\(hdr->ucode_size_bytes\)\);')
 witness('amdgpu_psp.c','response address copied into ucode bookkeeping',r'if \(ucode\) \{\s*ucode->tmr_mc_addr_lo = psp->cmd_buf_mem->resp.fw_addr_lo;\s*ucode->tmr_mc_addr_hi = psp->cmd_buf_mem->resp.fw_addr_hi;\s*}')
 witness('amdgpu_gart.h','GPU page size4096',r'#define AMDGPU_GPU_PAGE_SIZE 4096')
 witness('amdgpu_uvd.h','UVD firmware offset256',r'#define AMDGPU_UVD_FIRMWARE_OFFSET\s+256')
 witness('amdgpu_vcn.h','stack/context sizes',r'#define AMDGPU_VCN_STACK_SIZE\s+\(128\*1024\)\s*#define AMDGPU_VCN_CONTEXT_SIZE\s+\(512\*1024\)')
 witness('psp_gfx_if.h','VCN type13 decimal',r'GFX_FW_TYPE_VCN\s*= 13,')
 witness('psp_gfx_if.h','MMSCH type19 decimal',r'GFX_FW_TYPE_MMSCH\s*= 19,')
 witness('vcn_v2_0.c','MMSCH startup is reached from SRIOV startup in this source',r'return vcn_v2_0_start_mmsch\(adev, &adev->virt.mm_table\);')
 b=firmware.read_bytes();total,header=struct.unpack_from('<II',b);size,offset=struct.unpack_from('<II',b,20)
 assert total==len(b)==405952 and size==405696 and offset==256 and offset+size==len(b)
 align=lambda n:(n+4095)&~4095
 span=align(len(b)+4);reserved=align(size+8);assert span==reserved==409600
 return {'result':'PASS','classification':'PROVEN_STATICALLY','scope':'Normal reference-source formulas applied to one already-saved firmware file; no submitted or resident bytes measured','witnesses':rows,'saved_firmware':{'file_sha256':hashlib.sha256(b).hexdigest(),'payload_sha256':hashlib.sha256(b[offset:]).hexdigest(),'file_size':len(b),'payload_size':size,'common_header_offset':offset},'conditional_geometry':{'cache_size0':span,'driver_payload_reservation':reserved,'stack_size':131072,'context_size':524288,'psp_cache_offset0':0,'driver_cache_offset0_encoded':32,'psp_stack_relative_to_vcpu_bo':0,'driver_stack_relative_to_vcpu_bo':span,'psp_context_relative_to_vcpu_bo':131072,'driver_context_relative_to_vcpu_bo':span+131072,'noncache_base':'separate fw_shared.gpu_addr','base_addresses':'not measured; symbolic only'},'conclusions':['For this retained file, the two distinct size formulas align to the same409600-byte span','PSP returned placement fields feed the reference firmware cache base; a readable cache register is not backing-memory provenance','R252 retained diagnostic source skips startup, so historical zero placement is not evidence that a live zero cache BAR was programmed','External RBC/cache-access reports do not alone establish acceptance of the historically rejected VCN payload','MMSCH19 and VCN13 are distinct; the inspected MMSCH startup belongs to the SRIOV path'],'limitations':['No argument that every possible firmware size has the same alignment result','No signature validation, authentication bypass, firmware loading or memory fetch performed','No proposed switch of loading mode or firmware command type','No claim about another BIOS, external boot conditions or physical power']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--saved-firmware',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root,a.saved_firmware);a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['witnesses']),'source witnesses; saved-file cache span',r['conditional_geometry']['cache_size0'])
