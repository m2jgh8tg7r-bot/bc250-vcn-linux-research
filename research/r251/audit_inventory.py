"""Index register-access call sites in pinned VCN2 startup functions.

This is a lexical source index, not a C evaluator or hardware trace. Branches,
retry loops and preprocessor alternatives are deliberately not flattened.
"""
import argparse,hashlib,json,re
from pathlib import Path
from audit_start import function

MACROS={'RREG32','WREG32','WREG32_P','RREG32_SOC15','WREG32_SOC15',
        'RREG32_SOC15_DPG_MODE','WREG32_SOC15_DPG_MODE','SOC15_WAIT_ON_RREG'}
FUNCTIONS={
 'vcn_v2_0_start':'normal entry with DPG early-return branch',
 'vcn_v2_0_mc_resume':'normal mapping helper with PSP/driver alternatives',
 'vcn_v2_0_disable_static_power_gating':'normal power helper with VF/policy branches',
 'vcn_v2_0_disable_clock_gating':'normal clock helper with VF/capability branches',
 'vcn_v2_0_start_dpg_mode':'DPG direct/indirect entry',
 'vcn_v2_0_mc_resume_dpg_mode':'DPG mapping helper with load-mode/indirect alternatives',
 'vcn_v2_0_clock_gating_dpg_mode':'DPG clock helper',
 'vcn_v2_0_dec_ring_test_ring':'specialized test with VF bypass'}

def mask_noncode(text):
    # Preserve line positions while excluding comments/string literals from token matching.
    pattern=r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    return re.sub(pattern,lambda m:''.join('\n' if c=='\n' else ' ' for c in m.group()),text,flags=re.S)

def inventory(root):
    path='drivers/gpu/drm/amd/amdgpu/vcn_v2_0.c';source=(root/path).read_text();rows=[]
    for name,scope in FUNCTIONS.items():
        body,line=function(source,name);code=mask_noncode(body);events=[]
        for match in re.finditer(r'\b([A-Za-z_]\w*)\s*\(',code):
            macro=match.group(1)
            if macro not in MACROS:continue
            start=code.index('(',match.start());pos=start+1;depth=1
            while depth:
                depth+=(code[pos]=='(')-(code[pos]==')');pos+=1
            args=code[start+1:pos-1];original=body[match.start():pos]
            registers=list(dict.fromkeys(re.findall(r'\b(?:mm|reg)UVD_[A-Z0-9_]+\b|\bmmCC_UVD_HARVESTING\b',args)))
            if not registers and 'scratch9' in args:registers=['symbolic external scratch9 mapping']
            assert registers,(name,macro,original)
            events.append({'source_order':len(events)+1,'line':line+body.count('\n',0,match.start()),
                           'macro':macro,'register_symbols':registers,
                           'source_expression_sha256':hashlib.sha256(original.encode()).hexdigest()})
        expected=sum(len(re.findall(r'\b'+re.escape(m)+r'\s*\(',code)) for m in MACROS)
        assert len(events)==expected and events,name
        rows.append({'function':name,'scope':scope,'function_line':line,'source_sha256':hashlib.sha256(body.encode()).hexdigest(),'call_sites':events})
    return {'result':'PASS','classification':'PROVEN_STATICALLY','source_path':path,
            'source_sha256':hashlib.sha256((root/path).read_bytes()).hexdigest(),
            'functions':rows,'lexical_call_site_count':sum(len(x['call_sites']) for x in rows),
            'distinct_register_symbols':sorted({r for x in rows for e in x['call_sites'] for r in e['register_symbols']}),
            'limitations':['Lexical call sites, not runtime operation counts',
                           'Branch alternatives and loops retain their original source context',
                           'DPG macro effect depends on its indirect argument',
                           'Host shared-memory queue updates and non-register helper calls are covered by the phase audit, not this register-call index',
                           'No physical addresses, device writes or observed transitions generated']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    r=inventory(a.source_root);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print('PASS',len(r['functions']),'functions;',r['lexical_call_site_count'],'lexical register call sites')
