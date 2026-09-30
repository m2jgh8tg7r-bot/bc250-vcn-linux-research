"""Verify every decoder mask against the reference header, without a device."""
import argparse,json,re
from pathlib import Path
from interpret_capture import FIELDS
NAMES={
 'UVD_VCPU_CNTL':['CLK_EN','PMB_SOFT_RESET','RBBM_SOFT_RESET','CABAC_MB_ACC'],
 'UVD_SOFT_RESET':['VCPU_SOFT_RESET','RBC_SOFT_RESET','VCPU_VCLK_RESET_STATUS','LMI_SOFT_RESET','LMI_UMC_SOFT_RESET'],
 'UVD_STATUS':['VCPU_REPORT_READY','DRIVER_BUSY','RBC_BUSY'],
 'UVD_RBC_RB_CNTL':['RB_NO_FETCH','RB_NO_UPDATE','RB_RPTR_WR_EN'],
 'CC_UVD_HARVESTING':['MMSCH_DISABLE','UVD_DISABLE'],
 'UVD_RB_ARB_CTRL':['VCPU_DIS'],
 'UVD_CGC_GATE':['RBC','VCPU'],
 'UVD_CGC_CTRL':['DYN_CLOCK_MODE','RBC_MODE','VCPU_MODE'],
 'UVD_LMI_CTRL2':['STALL_ARB_UMC']}
def verify(header):
 defs={k:int(v,16) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+)L?\s*$',header.read_text(),re.M)}
 checked=[]
 for reg,fields in FIELDS.items():
  assert len(fields)==len(NAMES[reg])
  for (label,value),symbol in zip(fields.items(),NAMES[reg]):
   if reg=='UVD_STATUS':
    # Driver conventions within/adjacent to VCPU_REPORT; not three header fields.
    expected={'VCPU_REPORT_READY':1<<defs['UVD_STATUS__VCPU_REPORT__SHIFT'],
              'DRIVER_BUSY':2<<defs['UVD_STATUS__VCPU_REPORT__SHIFT'],
              'RBC_BUSY':defs['UVD_STATUS__RBC_BUSY_MASK']}[symbol]
   else:expected=defs[reg+'__'+symbol+'_MASK']
   assert value==expected,(reg,label,value,expected)
   checked.append({'register':reg,'label':label,'mask':hex(value)})
 return {'result':'PASS','verified_masks':checked,'scope':'Header definitions and explicitly labeled driver conventions; no hardware validation'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('header',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=verify(a.header)
 a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['verified_masks']),'decoder masks')
