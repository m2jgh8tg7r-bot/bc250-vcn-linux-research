"""Record syntax fields from ordinary generated clips using FFmpeg trace_headers."""
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parent
FIELDS=['pic_order_cnt_type','log2_max_pic_order_cnt_lsb_minus4',
        'log2_max_frame_num_minus4','frame_mbs_only_flag','chroma_format_idc',
        'bit_depth_luma_minus8','memory_management_control_operation',
        'nal_ref_idc','pic_order_cnt_lsb']

def main():
    rows=[]
    for clip in sorted((ROOT/'clips').glob('*.264')):
        log=clip.with_suffix('.headers.log')
        with log.open('w') as output:
            rc=subprocess.run(['ffmpeg','-hide_banner','-loglevel','info','-i',str(clip),
                '-c:v','copy','-bsf:v','trace_headers','-f','null','-'],
                stdout=output,stderr=subprocess.STDOUT,timeout=60).returncode
        assert rc==0
        text=log.read_text()
        fields={f:sorted({int(x) for x in re.findall(r'\b'+f+r'\b[^\n]*=\s*(\d+)',text)}) for f in FIELDS}
        rows.append(dict(case=clip.stem,fields=fields))
    (ROOT/'header-summary.json').write_text(json.dumps(dict(cases=rows),indent=2)+'\n')

if __name__=='__main__':
    main()
