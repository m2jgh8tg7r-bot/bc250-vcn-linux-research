"""Launch the recorded rootless CPU-only experiment environment."""
from pathlib import Path
import argparse
import subprocess

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check-counters',action='store_true')
    args=parser.parse_args()
    out=Path(__file__).resolve().parent
    name='bc250-r247-counter-check' if args.check_counters else 'bc250-r247-matrix'
    script='verify_cpu_counters.py' if args.check_counters else 'run_matrix.py'
    cmd=['podman','run','--rm','--name',name,'--userns=keep-id',
        '--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges',
        '--security-opt=label=disable','--tmpfs','/tmp:rw,nosuid,nodev,size=64m',
        '--memory=2g','--pids-limit=128',
        '--mount',f'type=bind,src={out},dst=/out,rw=true',
        '--mount','type=bind,src=/usr/bin/ffmpeg,dst=/host-ffmpeg,ro=true',
        '--mount','type=bind,src=/usr/lib64,dst=/hostlib,ro=true',
        'localhost/q36-agent-runtime:fedora44','python3','/out/'+script]
    raise SystemExit(subprocess.run(cmd).returncode)
