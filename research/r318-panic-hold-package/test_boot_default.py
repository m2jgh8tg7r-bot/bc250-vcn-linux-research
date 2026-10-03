from pathlib import Path
from boot_default import check_default
import json
p=Path(__file__).resolve().parent
before={q.name:q.read_text() for q in Path('/boot/loader/entries').glob('*.conf')};after=dict(before);del after['boot-entry-r316-netext.conf'];after['boot-entry-r318-nethold.conf']=(p/'boot-entry-r318-nethold.conf').read_text()
cfg='load_env\nset default=1\nblscfg\n';env={'boot_success':'1'};rows=[]
def trial(name,e,c,b,a,allowed):
 try:result=check_default(e,c,b,a);passed=True
 except AssertionError:result=None;passed=False
 assert passed==allowed,(name,result)
 rows.append({'case':name,'expected_acceptance':allowed,'pass':True})
trial('observed_layout_fixed_1',env,cfg,before,after,True)
for name,c in [('changed_default',cfg.replace('default=1','default=2')),('multiple_defaults','set default=0\n'+cfg),('preceding_menu','menuentry extra {}\n'+cfg),('extra_config','source extra.cfg\n'+cfg),('multiple_bls',cfg+'blscfg\n')]:trial(name,env,c,before,after,False)
for key,value in [('next_entry','other'),('blsdir','elsewhere'),('saved_entry','boot-entry-r316-netext')]:trial(key,{**env,key:value},cfg,before,after,False)
a=dict(after);a['ostree-1.conf']+='\n# changed\n';trial('normal_content_changed',env,cfg,before,a,False)
a=dict(after);a['boot-entry-r318-nethold.conf']=a['boot-entry-r318-nethold.conf'].replace('version 0','version 3');trial('candidate_priority_changed',env,cfg,before,a,False)
a=dict(after);a['unexpected.conf']='title other\nversion 0\n';trial('unknown_entry',env,cfg,before,a,False)
trial('saved_normal_id',{'saved_entry':'ostree-1'},'set default="${saved_entry}"\nblscfg\n',before,after,True)
(p/'DEFAULT_CHECK_TEST.json').write_text(json.dumps({'result':'PASS','scope':'CPU fixtures using current readable BLS files; protected actual GRUB config remains user-supplied until preflight','cases':rows,'observed_layout_prediction':check_default(env,cfg,before,after)},indent=2)+'\n');print('PASS',len(rows),'cases; boot files unchanged')
