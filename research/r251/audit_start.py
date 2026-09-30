"""Offline audit of pinned normal VCN2 source. Never reads a device or writes registers."""
from pathlib import Path
import argparse,hashlib,json,re,sys

def sha(b):return hashlib.sha256(b).hexdigest()
def function(text,name):
 pattern=re.compile(r'^(?:static\s+)?(?:inline\s+)?[\w\s*]+\b'+re.escape(name)+r'\s*\([^;]*?\)\s*\{',re.M)
 ms=list(pattern.finditer(text));assert len(ms)==1,(name,len(ms));m=ms[0];a=text.index('{',m.start());n=1;b=a+1
 while n:
  n+=(text[b]=='{')-(text[b]=='}');b+=1
 start=m.start()
 while text[start]=='\n':start+=1
 return text[start:b],text.count('\n',0,start)+1

def audit(root):
 base=root/'drivers/gpu/drm/amd';cf=base/'amdgpu/vcn_v2_0.c';hf=base/'include/asic_reg/vcn/vcn_2_0_0_sh_mask.h'
 c=cf.read_text();h=hf.read_text();defs={k:int(v,16) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+)L?\s*$',h,re.M)}
 expected={'UVD_VCPU_CNTL__CLK_EN_MASK':0x200,'UVD_VCPU_CNTL__PMB_SOFT_RESET_MASK':0x40,'UVD_VCPU_CNTL__RBBM_SOFT_RESET_MASK':0x80,'UVD_SOFT_RESET__VCPU_SOFT_RESET_MASK':8,'UVD_SOFT_RESET__RBC_SOFT_RESET_MASK':1,'UVD_SOFT_RESET__VCPU_VCLK_RESET_STATUS_MASK':0x80000,'UVD_STATUS__VCPU_REPORT_MASK':0xfe,'UVD_STATUS__VCPU_REPORT__SHIFT':1,'UVD_RBC_RB_CNTL__RB_NO_FETCH_MASK':0x10000,'CC_UVD_HARVESTING__MMSCH_DISABLE_MASK':1,'CC_UVD_HARVESTING__UVD_DISABLE_MASK':2}
 for k,v in expected.items():assert defs[k]==v,(k,defs[k])
 assert 'UVD_VCPU_CNTL__VCPU_SOFT_RESET_MASK' not in defs
 names=['vcn_v2_0_start','vcn_v2_0_start_dpg_mode','vcn_v2_0_mc_resume','vcn_v2_0_mc_resume_dpg_mode','vcn_v2_0_disable_static_power_gating','vcn_v2_0_disable_clock_gating','vcn_v2_0_set_pg_state','vcn_v2_0_dec_ring_test_ring','vcn_v2_0_hw_init']
 funcs={n:function(c,n) for n in names};s,line=funcs['vcn_v2_0_start']
 steps=[('DPM request when enabled','amdgpu_dpm_enable_vcn(adev, true, 0)'),('DPG early-return branch','return vcn_v2_0_start_dpg_mode'),('static power gate helper','vcn_v2_0_disable_static_power_gating(vinst)'),('mark busy','UVD_STATUS__UVD_BUSY'),('disable clock gating','vcn_v2_0_disable_clock_gating(vinst)'),('enable VCPU clock','UVD_VCPU_CNTL__CLK_EN_MASK'),('disable master interrupt','/* disable master interrupt */'),('LMI coherence setup','/* setup mmUVD_LMI_CTRL */'),('MPC setup','/* setup mmUVD_MPC_CNTL */'),('cache mappings','vcn_v2_0_mc_resume(vinst)'),('release VCPU reset','/* release VCPU reset to boot */'),('unstall LMI channel','/* enable LMI MC and UMC channels */'),('release LMI reset fields','tmp &= ~UVD_SOFT_RESET__LMI_SOFT_RESET_MASK'),('byte-swap setup','/* disable byte swapping */'),('bounded readiness retry','for (i = 0; i < 10; ++i)'),('readiness test','if (status & 2)'),('failure exit','if (r) {'),('enable master interrupt','/* enable master interrupt */'),('clear busy report bit','~(2 << UVD_STATUS__VCPU_REPORT__SHIFT)'),('RBC VMID','mmUVD_LMI_RBC_RB_VMID'),('RBC idle configuration','/* force RBC into idle state */'),('decode queue reset','decode_queue_mode |= FW_QUEUE_RING_RESET'),('decode buffer base','/* program the RB_BASE for ring buffer */'),('decode ring pointers','/* Initialize the ring buffer'),('decode queue reset cleared','decode_queue_mode &= ~FW_QUEUE_RING_RESET'),('encode general queue','encode_generalpurpose_queue_mode |= FW_QUEUE_RING_RESET'),('encode low-latency queue','encode_lowlatency_queue_mode |= FW_QUEUE_RING_RESET'),('completion readback','/* Keeping one read-back')]
 positions=[]
 for label,needle in steps:
  off=s.index(needle);positions.append({'phase':label,'line':line+s.count('\n',0,off),'needle':needle,'offset':off})
 assert [x['offset'] for x in positions]==sorted(x['offset'] for x in positions)
 d,dl=funcs['vcn_v2_0_start_dpg_mode'];assert 'if (status & 2)' not in d;assert 'amdgpu_vcn_psp_update_sram' in d
 assert s.count('RB_NO_FETCH, 1')==1 and 'RB_NO_FETCH, 0' not in s
 assert d.count('RB_NO_FETCH, 1')==1 and 'RB_NO_FETCH, 0' not in d
 cache,cl=funcs['vcn_v2_0_mc_resume'];assert 'fw->size + 4' in cache and 'tmr_mc_addr_lo' in cache and 'AMDGPU_UVD_FIRMWARE_OFFSET >> 3' in cache
 test,tl=funcs['vcn_v2_0_dec_ring_test_ring'];assert 'VCN_DEC_CMD_PACKET_START' in test and '0xCAFEDEAD' in test and '0xDEADBEEF' in test
 fields=[{'symbol':k,'value':hex(v),'line':next(i for i,l in enumerate(h.splitlines(),1) if re.match(r'#define\s+'+k+r'\s',l))} for k,v in expected.items()]
 return {'result':'PASS','classification':'PROVEN_STATICALLY','scope':'Pinned source structure and field definitions; no runtime or silicon equivalence claim','source_files':[{'path':str(f.relative_to(root)),'sha256':sha(f.read_bytes())} for f in [cf,hf]],'normal_path_phases':positions,'fields':fields,'functions':[{'name':n,'line':ln,'sha256':sha(t.encode())} for n,(t,ln) in funcs.items()],'readiness_test_mask':2,'driver_busy_mask':2<<defs['UVD_STATUS__VCPU_REPORT__SHIFT'],'readiness_truth_table':[{'status':hex(v),'passes_status_and_2':bool(v&2),'clears_busy_to':hex(v&~4),'valid_device_read_established':False} for v in [0,1,2,3,4,6,0xffffffff]],'findings':['Normal path polls readiness before final RBC setup; DPG path has a different contract','PMB/RBBM resets in VCPU_CNTL are not the VCPU_SOFT_RESET field in UVD_SOFT_RESET','VCPU_REPORT is a field; readiness mask2 and busy mask4 are distinct bits','Both start paths set RB_NO_FETCH=1 with no explicit same-function clear; missing clear is not by itself a defect','Cache source is conditional on PSP versus driver loading; register access alone does not validate its backing bytes','Readiness polling accepts any value containing bit1, including all-ones; source predicate alone cannot establish read validity'],'limitations':['Normal VCN2 reference does not prove BC250 executes the same path','DPG and virtualization must not be merged with the normal path','This is not a manual register-write procedure','No VCPU instruction, ring operation, decoding or clock physical state observed']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root);a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['normal_path_phases']),'ordered source phases;',len(r['fields']),'field definitions')
