from pathlib import Path
import json, os, pty, select, subprocess, time
out=Path(__file__).resolve().parent
fragment=(out/'input-diagnostic.bash').read_text()
fragment=fragment.replace('stty -a </dev/console','stty -a <&0 2>/dev/null || true')
script='marker() { printf "%s\\n" "$*"; };\n'+fragment
cases=[('exact',b'R299-CP03-RECEIVED\n','INPUT_EXACT_MATCH'),('space',b'R299-CP03-RECEIVED \n','INPUT_MISMATCH'),('carriage_return',b'R299-CP03-RECEIVED\r\n','INPUT_MISMATCH'),('empty_line',b'\n','INPUT_MISMATCH'),('eof',b'','INPUT_READ_FAILURE'),('partial_eof',b'R299-CP03-RECEIVED','INPUT_READ_FAILURE'),('unicode_dash','R299–CP03-RECEIVED\n'.encode(),'INPUT_MISMATCH'),('long_input',b'x'*200+b'\n','INPUT_MISMATCH')]
results=[]
for name,data,want in cases:
 p=subprocess.run(['bash','-c',script],input=data,capture_output=True,timeout=5)
 log=p.stdout.decode();assert p.returncode==0 and want in log,(name,log,p.stderr)
 assert 'modprobe' not in fragment
 results.append({'case':name,'pass':True,'output':log})
master,slave=pty.openpty()
p=subprocess.Popen(['bash','-c',script],stdin=slave,stdout=slave,stderr=slave);os.close(slave)
buf=b'';deadline=time.monotonic()+5
while b'INPUT_READY' not in buf:
 assert time.monotonic()<deadline
 if select.select([master],[],[],0.1)[0]:buf+=os.read(master,4096)
os.write(master,b'R299-CP03-RECEIVED\n')
while time.monotonic()<deadline:
 if select.select([master],[],[],0.1)[0]:
  try:buf+=os.read(master,4096)
  except OSError:break
 if p.poll() is not None:break
p.wait(timeout=2);os.close(master)
assert b'INPUT_EXACT_MATCH' in buf,buf
results.append({'case':'pty_exact','pass':True,'output':buf.decode()})
(out/'INPUT_TEST.json').write_text(json.dumps({'tests':results,'real_gpu_load':False,'live_console_test':False},indent=2)+'\n')
print(f'PASS {len(results)}/{len(results)}; CPU pipes and PTY only')
