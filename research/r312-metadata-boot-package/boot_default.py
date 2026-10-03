"""Fail-closed check for this machine's saved-ID or fixed-index BLS layout."""
import re
from boot_includes import inspect_sources

def check_default(environment, config, before, after, includes=None):
    # before/after map BLS filenames to text. No filesystem or boot mutations.
    def fields(text):
        result={}
        for line in text.splitlines():
            p=line.split(None,1)
            if len(p)==2 and not p[0].startswith('#'):
                assert p[0] not in result, 'Duplicate BLS field; review required'
                result[p[0]]=p[1]
        return result
    def layout(entries):
        normal=[]; research=[]
        for name,text in entries.items():
            f=fields(text)
            assert not any(k in f for k in ['sort-key','machine-id','id','grub_arg','grub_args']), 'Nonstandard ordering/identity metadata'
            m=re.fullmatch(r'ostree-([1-9][0-9]*)\.conf',name)
            if m:
                assert f.get('version')==m[1], 'OSTree version/name mismatch'
                normal.append((int(m[1]),name))
            else:
                assert re.fullmatch(r'boot-entry-r[0-9]+-[a-z0-9-]+\.conf',name) and f.get('version')=='0', 'Unrecognized BLS ordering'
                research.append(name)
        assert len(normal)>=2, 'Need two protected normal entries ahead of research entries'
        return [n for _,n in sorted(normal,reverse=True)],research
    oldnormal,oldresearch=layout(before);newnormal,newresearch=layout(after)
    assert oldnormal==newnormal and all(before[n]==after[n] for n in oldnormal), 'Normal entries changed'
    lines=[x.strip() for x in config.splitlines() if x.strip() and not x.lstrip().startswith('#')]
    assignments=[x for x in lines if re.match(r'set\s+default\s*=',x)]
    saved=environment.get('saved_entry')
    if saved:
        assert saved+'.conf' in oldnormal, 'Saved entry is not protected normal ID'
        # Do not guess precedence between a saved ID and a literal config default.
        assert assignments in [['set default="${saved_entry}"'],['set default=${saved_entry}']], 'Unreviewed default assignment'
        return {'mode':'saved_normal_id','selected_entry':saved+'.conf'}
    assert assignments==['set default=1'], 'Only observed fixed default=1 is supported'
    assert lines.count('blscfg')==1 and lines.index('set default=1')<lines.index('blscfg'), 'Unexpected BLS/default control flow'
    include_check=inspect_sources(config,includes or {})
    assert not any(k in environment for k in ['next_entry','blsdir']), 'Unreviewed environment override'
    return {'include_check':include_check,'mode':'fixed_index_1_no_saved_entry','normal_bls_prefix':oldnormal,'selected_entry':oldnormal[1],'research_count_before':len(oldresearch),'research_count_after':len(newresearch),'normal_prefix_unchanged':True,'scope':'Observed conventional Fedora BLS names and matching numeric versions; not a general GRUB parser'}
