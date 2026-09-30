"""Separate counter/interface definitions and bounded cross-generation names."""
import argparse,hashlib,json,re
from pathlib import Path

def audit(root):
    base='drivers/gpu/drm/amd/include/asic_reg/vcn/'
    paths=[base+'vcn_2_0_0_offset.h',base+'vcn_2_0_0_sh_mask.h',base+'vcn_4_0_5_sh_mask.h']
    offset,old,new=[(root/p).read_text() for p in paths]
    wanted=['UVD_FREE_COUNTER_REG__FREE_COUNTER_MASK','UVD_PG_IND_INDEX__INDEX_MASK','UVD_PG_IND_DATA__DATA_MASK',
            'UVD_LMI_PERFMON_CTRL__PERFMON_STATE_MASK','UVD_LMI_PERFMON_CTRL__PERFMON_SEL_MASK',
            'UVD_LMI_PERFMON_COUNT_LO__PERFMON_COUNT_MASK','UVD_LMI_PERFMON_COUNT_HI__PERFMON_COUNT_MASK',
            'UVD_VCPU_PRID__PRID_MASK','UVD_VCPU_TRCE__PC_MASK','UVD_VCPU_TRCE_RD__DATA_MASK']
    rows=[]
    for name in wanted:
        m=re.search(r'^#define\s+'+name+r'\s+(0x[0-9a-fA-F]+)L?\s*$',old,re.M);assert m,name
        rows.append({'symbol':name,'value':hex(int(m.group(1),16)),'line':old.count('\n',0,m.start())+1})
    symbols=['mmUVD_FREE_COUNTER_REG','mmUVD_PG_IND_INDEX','mmUVD_PG_IND_DATA','mmUVD_LMI_PERFMON_CTRL','mmUVD_LMI_PERFMON_COUNT_LO','mmUVD_LMI_PERFMON_COUNT_HI','mmUVD_VCPU_PRID','mmUVD_VCPU_TRCE','mmUVD_VCPU_TRCE_RD']
    offsets=[]
    for name in symbols:
        m=re.search(r'^#define\s+'+name+r'\s+(0x[0-9a-fA-F]+)\s*$',offset,re.M);assert m,name
        offsets.append({'symbol':name,'relative_dword_offset':hex(int(m.group(1),16)),'line':offset.count('\n',0,m.start())+1})
    assert len({x['relative_dword_offset'] for x in offsets})==len(offsets)
    assert 'UVD_GPCNT0_STATUS_LOWER' not in old and 'UVD_GPCNT0_STATUS_LOWER' not in offset
    heading=new.index('// addressBlock: uvd_pg_indirect');name='UVD_GPCNT0_STATUS_LOWER__COUNT__SHIFT'
    m=re.search(r'^#define\s+'+name+r'\s+(0x[0-9a-fA-F]+)\s*$',new,re.M);assert m and m.start()>heading
    return {'result':'PASS','classification':'PROVEN_STATICALLY','fields':rows,'distinct_interfaces':offsets,
            'newer_header_name_witness':{'map':'vcn_4_0_5','address_block':'uvd_pg_indirect','symbol':name,'line':new.count('\n',0,m.start())+1},
            'source_files':[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in paths],
            'confirmed':['FREE_COUNTER, indirect PG access, selected LMI perf monitoring, PRID and trace are distinct named interfaces',
                         'The VCN2.0 reference headers do not establish the reported GPCNT0 indirect index0x02 mapping',
                         'The newer4.0.5 header supports the GPCNT0 name in an indirect-PG block, not its BC250 index or clock source'],
            'conditional_evaluation':{'reported_two_frequency_tracking':'Strong positive evidence against whole-domain VCLK absence if independently timed fresh counts track both settings',
                                      'free_counter_zero':'Does not contradict activity of a different counter and does not rescue whole-domain clock absence',
                                      'remaining_unknown':'VCPU leaf clock, reset/isolation, instruction-master path, vector and visibility of execution evidence'},
            'raw_external_measurement_verified':False,'hardware_access':False,
            'limits':['No cross-generation address transplantation','No named-field equivalence to physical activity',
                      'No LMI event map or trace sampling specification established','No counter rate was measured locally']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['fields']),'field definitions;',len(r['distinct_interfaces']),'distinct interfaces; newer-header name only')
