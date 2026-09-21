"""Read a saved kernel source tree and report Cyan SMU firmware callback wiring."""
import argparse, hashlib, json, re
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('kernel_source');a=p.parse_args()
r=Path(a.kernel_source)
base='drivers/gpu/drm/amd/'
paths=[base+'pm/swsmu/'+x for x in ['amdgpu_smu.c','smu_internal.h','smu11/cyan_skillfish_ppt.c','smu11/smu_v11_0.c']]+[base+'amdgpu/amdgpu_psp.c']
s={x:(r/x).read_text() for x in paths}
cyan=s[paths[2]]; table=cyan.split('static const struct pptable_funcs cyan_skillfish_ppt_funcs = {',1)[1].split('};',1)[0]
assignments=dict(re.findall(r'\.(\w+)\s*=\s*(\w+)',table))
assert 'init_microcode' not in assignments and 'load_microcode' not in assignments
assert assignments['check_fw_status']=='smu_v11_0_check_fw_status'
assert re.search(r'case IP_VERSION\(11, 0, 8\):\s*cyan_skillfish_set_ppt_funcs\(smu\)',s[paths[0]])
assert 'smu->is_apu = true;' in cyan
out=dict(hardware_access=False,files=[dict(path=x,sha256=hashlib.sha256((r/x).read_bytes()).hexdigest()) for x in paths],
         ip='11.0.8',ppt_setter='cyan_skillfish_set_ppt_funcs',is_apu=True,
         callbacks=assignments,init_microcode_callback_present=False,load_microcode_callback_present=False,
         runtime_image_identity_proven=False)
print(json.dumps(out,indent=2))
