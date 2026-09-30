"""Audit observation producers and side effects from source, without opening debugfs."""
import argparse,hashlib,json,re
from pathlib import Path

def audit(root):
 base=root/'drivers/gpu/drm/amd/amdgpu';common=(base/'amdgpu_vcn.c').read_text();v2=(base/'vcn_v2_0.c').read_text();findings=[]
 def check(file,label,pattern):
  t=common if file=='amdgpu_vcn.c' else v2;m=re.search(pattern,t,re.S);assert m,(file,label)
  findings.append({'claim':label,'path':'drivers/gpu/drm/amd/amdgpu/'+file,'line':t.count('\n',0,m.start())+1,'matched_source':m.group(0)})
 check('amdgpu_vcn.c','fwlog read requires enabled logging and shared memory',r'if \(!vcn->fw_shared.cpu_addr \|\| !amdgpu_vcnfw_log\)\s*return -EFAULT;')
 check('amdgpu_vcn.c','empty log returns zero on equal pointers',r'if \(!size \|\| \(read_pos == write_pos\)\)\s*return 0;')
 check('amdgpu_vcn.c','fwlog read advances shared read pointer',r'plog->rptr = read_pos;\s*\*pos \+= read_bytes;\s*return read_bytes;')
 check('amdgpu_vcn.c','fwlog file read permission is0444',r'debugfs_create_file_size\(name, S_IFREG \| 0444, root, vcn,')
 check('amdgpu_vcn.c','host initializes the log header and both pointers',r'log_buf->header_size = sizeof\(struct amdgpu_vcn_fwlog\);\s*log_buf->buffer_size = AMDGPU_VCNFW_LOG_SIZE;\s*log_buf->rptr = log_buf->header_size;\s*log_buf->wptr = log_buf->header_size;\s*log_buf->wrapped = 0;')
 check('vcn_v2_0.c','VCN2 software init conditionally enables logging',r'if \(amdgpu_vcnfw_log\)\s*amdgpu_vcn_fwlog_init\(adev->vcn.inst\);')
 check('amdgpu_vcn.c','dump storage is zero-initialized',r'adev->vcn.ip_dump = kcalloc\(adev->vcn.num_vcn_inst \* count,\s*sizeof\(uint32_t\), GFP_KERNEL\);')
 check('amdgpu_vcn.c','dump reads other registers only under source power predicate',r'if \(is_powered\)\s*for \(j = 1; j < adev->vcn.reg_count; j\+\+\)\s*adev->vcn.ip_dump\[inst_off \+ j\] =\s*RREG32\(SOC15_REG_ENTRY_OFFSET_INST\(adev->vcn.reg_list\[j\], i\)\);')
 start=common.index('void amdgpu_vcn_print_ip_state(');printed=common[start:];assert 'RREG32(' not in printed
 check('amdgpu_vcn.c','printed values come from saved dump storage',r'drm_printf\(p, "%-50s.*?adev->vcn.ip_dump\[inst_off \+ j\]\);')
 m=re.search(r'static const struct amdgpu_hwip_reg_entry vcn_reg_list_2_0\[\] = \{(.*?)\n};',v2,re.S);assert m
 names=re.findall(r'SOC15_REG_ENTRY_STR\(VCN, 0, (\w+)\)',m.group(1));assert names[0]=='mmUVD_POWER_STATUS'
 requested=['mmUVD_STATUS','mmUVD_VCPU_CNTL','mmUVD_SOFT_RESET','mmUVD_LMI_VCPU_CACHE_64BIT_BAR_LOW','mmUVD_LMI_VCPU_CACHE_64BIT_BAR_HIGH','mmUVD_VCPU_CACHE_OFFSET0','mmUVD_VCPU_CACHE_SIZE0','mmUVD_RBC_RB_CNTL']
 return {'result':'PASS','classification':'PROVEN_STATICALLY','sources':[{'path':'drivers/gpu/drm/amd/amdgpu/'+n,'sha256':hashlib.sha256((base/n).read_bytes()).hexdigest()} for n in ['amdgpu_vcn.c','vcn_v2_0.c']],'findings':findings,'vcn2_dump_register_count':len(names),'vcn2_dump_registers':names,'requested_coverage':{n:n in names for n in requested},'conclusions':['Read-only file permission does not make fwlog reads observationally side-effect-free','Host-initialized firmware-log header is not a VCPU heartbeat','Empty log output cannot establish that no instruction executed','print_ip_state reports saved values; Active is a power-status predicate label, not a VCPU execution measurement','Current VCN2 dump list does not provide the complete requested clock/reset/cache tuple'],'limits':['No debugfs read, MMIO, logging enable or recovery action performed','No external firmware logging capability established','No claim that any actual printed dump was uninitialized or stale','No universal physical interpretation of the tile-off predicate']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root);a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['findings']),'observation-source checks;',r['vcn2_dump_register_count'],'listed registers')
