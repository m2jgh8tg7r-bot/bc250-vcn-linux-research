"""Recheck named harvest namespaces and a saved cached-metadata record."""
import argparse,hashlib,json,re
from pathlib import Path

def audit(root,saved):
    rel='drivers/gpu/drm/amd/amdgpu/amdgpu_discovery.c';text=(root/rel).read_text()
    header='drivers/gpu/drm/amd/include/asic_reg/vcn/vcn_2_0_0_sh_mask.h';h=(root/header).read_text();rows=[]
    checks=[('early_no_device_returns_zero',r'/\* In early init mode \(adev == NULL\), harvest info is not available \*/\s*if \(!adev\)\s*return 0;'),
            ('normal_vcn_harvest_uses_instance_mask',r'case VCN_HWID:\s*/\* VCN vs UVD\+VCE \*/\s*if \(!amdgpu_ip_version\(adev, VCE_HWIP, 0\)\)\s*harvest = \(\(1 << inst\) & adev->vcn.inst_mask\) == 0;'),
            ('table_entry_increments_count_and_instance_bit',r'adev->vcn.num_vcn_inst\+\+;\s*adev->vcn.inst_mask \|=\s*\(1U << ip->instance_number\);'),
            ('revision_capability_bits_saved_separately',r'vcn_config =\s*ip->revision & 0xc0;'),
            ('revision_display_strips_capability_bits',r'ip->revision &= ~0xc0;')]
    for label,pattern in checks:
        m=re.search(pattern,text,re.S);assert m,label
        rows.append({'claim':label,'path':rel,'line':text.count('\n',0,m.start())+1,'matched_source':m.group()})
    masks={}
    for name,expected in [('CC_UVD_HARVESTING__MMSCH_DISABLE_MASK',1),('CC_UVD_HARVESTING__UVD_DISABLE_MASK',2)]:
        m=re.search(r'^#define\s+'+name+r'\s+(0x[0-9a-fA-F]+)L?\s*$',h,re.M);assert m and int(m.group(1),16)==expected
        masks[name]=hex(expected)
    data=json.loads(saved.read_text());assert data['scope']=='Cached sysfs IP metadata only'
    instances=data['instances'];assert len(instances)==1 and instances[0]['num_instance']=='0'
    return {'result':'PASS','classification':'PROVEN_STATICALLY','source_witnesses':rows,'cc_register_masks':masks,
            'saved_record':{'sha256':hashlib.sha256(saved.read_bytes()).hexdigest(),'captured_at':data['captured_at'],'scope':data['scope'],
                            'recorded_entries':len(instances),'recorded_instances':[x['num_instance'] for x in instances],
                            'version':'.'.join(instances[0][k] for k in ['major','minor','revision']),'harvest_display':instances[0]['harvest'],
                            'physical_instance_count_proven':False},
            'source_files':[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in [rel,header]],
            'conclusions':['The saved September9 record lists instance0 only; it corroborates a prior one-exposed-instance observation, not a universal physical count',
                           'CC register bits0/1 are MMSCH_DISABLE/UVD_DISABLE, not VCN0/VCN1',
                           'Displayed harvest0 and live CC3 need not be contradictory because their provenance and semantics differ',
                           'Current early-mode zero fallback cannot be retroactively assigned to the saved capture without matching its implementation',
                           'Reported nonpersistent writes are compatible with mirror/restore/lock behavior but do not identify a producer'],
            'priority':'Low-cost static producer/source review only; direct clear variants excluded from the main line',
            'hypotheses_remaining':['causal VCPU-specific effect','mirror of another cause/state','unrelated availability indication'],
            'producer_identified':False,'hardware_access':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--saved-metadata',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=audit(a.source_root,a.saved_metadata)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(r['source_witnesses']),'source witnesses; saved record contains',r['saved_record']['recorded_entries'],'instance entry')
