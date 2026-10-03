from pathlib import Path
import json
from boot_includes import validate_include,inspect_sources,SOURCES
rows=[]
def case(name,fn,accept):
 try:fn();ok=True
 except AssertionError:ok=False
 assert ok==accept,name
 rows.append({'case':name,'accepted':ok,'pass':True})
for n in ['bootuuid.cfg','console.cfg','user.cfg']:case('absent_'+n,lambda n=n:validate_include(n,None),True)
case('uuid_assignment',lambda:validate_include('bootuuid.cfg','set BOOT_UUID="01234567-abcd"'),True)
case('console_commands',lambda:validate_include('console.cfg','terminal_input console\nterminal_output console\nset gfxmode=auto'),True)
case('password_assignment',lambda:validate_include('user.cfg','GRUB2_PASSWORD=grub.pbkdf2.sha512.1.AA.BB'),True)
for n in ['bootuuid.cfg','console.cfg','user.cfg']:
 case('reject_default_'+n,lambda n=n:validate_include(n,'set default=3'),False)
case('reject_nested_source',lambda:validate_include('console.cfg','source another.cfg'),False)
cfg='\n'.join(SOURCES)+'\nset default=1\nblscfg\n'
case('three_observed_absent_sources',lambda:inspect_sources(cfg,{n:None for n in SOURCES.values()}),True)
case('missing_observation',lambda:inspect_sources(cfg,{}),False)
case('unknown_source',lambda:inspect_sources('source other.cfg\nblscfg',{}),False)
case('preceding_menu',lambda:inspect_sources('menuentry example {}\nblscfg',{}),False)
Path(__file__).with_name('INCLUDE_CHECK_TEST.json').write_text(json.dumps({'result':'PASS','cases':rows,'hardware_access':False},indent=2)+'\n');print('PASS',len(rows),'include cases; boot files unchanged')
