"""Compare symbolic reset contracts across source generations; no hardware recipe."""
import argparse,hashlib,json,re
from pathlib import Path

def audit(p,current):
 specs=[('2.0','vcn_v2_0','vcn_2_0_0',current,current),('2.5','vcn_v2_5','vcn_2_5',current,p/'sources'),('3.0','vcn_v3_0','vcn_3_0_0',p/'sources',p/'sources'),('4.0','vcn_v4_0','vcn_4_0_0',p/'sources',p/'sources'),('5.0','vcn_v5_0_0','vcn_5_0_0',p/'sources',p/'sources')]
 rows=[]
 for gen,cn,hn,cr,hr in specs:
  cf=cr/'drivers/gpu/drm/amd/amdgpu'/(cn+'.c');hf=hr/'drivers/gpu/drm/amd/include/asic_reg/vcn'/(hn+'_sh_mask.h');c=cf.read_text();h=hf.read_text();defs={k:int(v,16) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+)L?\s*$',h,re.M)}
  suffix='UVD_SOFT_RESET__VCPU_SOFT_RESET_MASK' if gen=='2.0' else 'UVD_VCPU_CNTL__BLK_RST_MASK';register='UVD_SOFT_RESET' if gen=='2.0' else 'UVD_VCPU_CNTL'
  pattern=r'WREG32_P\(SOC15_REG_OFFSET\([^;]*?(?:mm|reg)'+register+r'\),\s*0,\s*~'+suffix+r'\);'
  m=re.search(pattern,c,re.S);assert m,(gen,pattern)
  fields=['UVD_VCPU_CNTL__CLK_EN_MASK','UVD_VCPU_CNTL__BLK_RST_MASK','UVD_VCPU_CNTL__CABAC_MB_ACC_MASK','UVD_SOFT_RESET__VCPU_SOFT_RESET_MASK','UVD_RB_ARB_CTRL__VCPU_DIS_MASK']
  rows.append({'generation':gen,'source':'drivers/gpu/drm/amd/amdgpu/'+cn+'.c','source_sha256':hashlib.sha256(cf.read_bytes()).hexdigest(),'header':'drivers/gpu/drm/amd/include/asic_reg/vcn/'+hn+'_sh_mask.h','header_sha256':hashlib.sha256(hf.read_bytes()).hexdigest(),'release_register':register,'release_field':suffix,'release_line':c.count('\n',0,m.start())+1,'release_source':m.group(0),'fields':{k:hex(defs[k]) if k in defs else None for k in fields},'vcpu_dis_source_references':c.count('UVD_RB_ARB_CTRL__VCPU_DIS_MASK')})
 assert rows[0]['fields']['UVD_VCPU_CNTL__BLK_RST_MASK'] is None
 assert rows[0]['fields']['UVD_VCPU_CNTL__CABAC_MB_ACC_MASK']=='0x10000000'
 assert rows[0]['vcpu_dis_source_references']==0
 assert all(x['fields']['UVD_VCPU_CNTL__BLK_RST_MASK']=='0x10000000' for x in rows[1:])
 assert all(x['fields']['UVD_VCPU_CNTL__CLK_EN_MASK']=='0x200' for x in rows)
 return {'result':'PASS','classification':'PROVEN_STATICALLY','generations':rows,'findings':['VCPU reset release changes register/field between the inspected2.0 and2.5+ reference drivers','The later BLK_RST bit value aliases the CABAC_MB_ACC name in the2.0 header; a matching register name or bit number does not establish semantics','VCPU_DIS exists in the2.0 header but is not referenced in the inspected vcn_v2_0.c; later source explicitly handles it','No generation transfer is justified by a field name alone'],'limitations':['Reference header2.0.0 is not an independently validated BC2502.0.3 silicon register specification','No inference about which reference the external suggestion used','No recommendation to write either bit or transplant a later startup sequence','Absence is bounded to the named source file, not firmware/UEFI or all software']}

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--current-source',type=Path,required=True);args=a.parse_args();p=Path(__file__).resolve().parent;r=audit(p,args.current_source);(p/'results.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['generations']),'generation contracts')
