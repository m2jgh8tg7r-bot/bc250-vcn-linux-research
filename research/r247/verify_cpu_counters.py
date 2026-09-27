"""Compare wrapper child accounting with FFmpeg's own benchmark report."""
import re
import run_matrix as m

original=m.command

def command(c,verbose=False):
    args=original(c,True)
    return args[:4]+['-benchmark']+args[4:]

def main():
    m.command=command
    row=m.measure(dict(clip='ip',mode='decode_null',readrate=1),'counter-cross-check',True)
    text=(m.OUT/'logs/counter-cross-check.log').read_text()
    match=re.search(r'bench: utime=([\d.]+)s stime=([\d.]+)s rtime=([\d.]+)s',text)
    assert match,text[-2000:]
    user,system,wall=map(float,match.groups())
    row.update(ffmpeg_user_seconds=user,ffmpeg_system_seconds=system,ffmpeg_wall_seconds=wall,
        child_minus_ffmpeg_cpu_seconds=row['cpu_seconds']-user-system,
        wrapper_minus_ffmpeg_wall_seconds=row['wall_seconds']-wall,
        scope='Two reporters of OS process accounting, not independent hardware counters')
    row['agreement_within_0_25_seconds']=abs(row['child_minus_ffmpeg_cpu_seconds'])<0.25
    m.save('counter-cross-check.json',row)
    print('Counter agreement',row['agreement_within_0_25_seconds'],row['child_minus_ffmpeg_cpu_seconds'])

if __name__=='__main__':main()
