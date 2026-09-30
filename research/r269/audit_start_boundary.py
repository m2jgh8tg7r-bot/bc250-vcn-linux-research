"""Verify software-stage boundaries; no effective hardware-state claim."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
name='drivers/gpu/drm/amd/amdgpu/vcn_v2_0.c';f=a.source_root/name;s=f.read_text();start=s.index('static int vcn_v2_0_start(struct amdgpu_vcn_inst *vinst)\n{');end=s.index('\nstatic ',start+10);body=s[start:end]
anchors=['/* enable VCPU clock */','/* disable master interrupt */','vcn_v2_0_mc_resume(vinst);','/* release VCPU reset to boot */','/* enable LMI MC and UMC channels */','if (status & 2)','/* enable master interrupt */']
positions=[body.index(x) for x in anchors];assert positions==sorted(positions)
assert body.count('UVD_MASTINT_EN__VCPU_EN_MASK')==3
witnesses=[{'anchor':x,'line':s.count('\n',0,start+body.index(x))+1} for x in anchors]
a.output.write_text(json.dumps({'classification':'PROVEN_STATICALLY','source':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'commit':'551c722f40809618230001baccf219193e22fc5a','witnesses':witnesses,'scope':'Non-DPG start function; source order only','findings':['VCPU_EN in MASTINT_EN is used as master-interrupt control, disabled before the ready poll and enabled afterward','The source treats VCPU reset release as boot release, followed by channel/reset setup and ready polling','No source-order observation proves effective core enable or first instruction issue on BC250'],'hardware_access':False},indent=2)+'\n');print('PASS non-DPG start-boundary source order')
