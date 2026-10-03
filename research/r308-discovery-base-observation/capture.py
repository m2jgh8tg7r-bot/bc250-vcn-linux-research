"""Read exported IP metadata only; no direct register or device-memory access."""
from pathlib import Path
import datetime,json,platform
rows=[]
for p in Path('/sys/class/drm').glob('card*/device/ip_discovery/die/*/12/*'):
 vals={n:(p/n).read_text().strip() for n in ['hw_id','num_instance','major','minor','revision','harvest','num_base_addresses','base_addr'] if (p/n).exists()}
 rows.append({'values':vals,'base_dwords':[int(x,16) for x in vals.get('base_addr','').split()]})
v={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kernel_release':platform.release(),'scope':'Current normal-boot sysfs IP metadata, not CP05/06/07 failed-boot runtime state','classification':'PROVEN_LIVE','classification_limit':'Exported metadata was observed; physical VCN activity is not established','entries':rows,'direct_hardware_access':False,'hardware_mutation':False,'limitations':['Current kernel implementation not attested by the retained research source','sysfs array is not a direct dump of failed-boot adev->reg_offset','One exposed entry is not proof of physical instance count']}
Path(__file__).with_name('observation.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps(v,indent=2))
