"""Reproduce the shared CPU-only container for timing or long-output checks.

Requires the retained R244 fixtures/binary, Podman, and host FFmpeg libraries.
The image name identifies a local runtime, not a publicly distributed image.
"""
import argparse
from pathlib import Path
import subprocess

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--phase',choices=['benchmark','verify_extended'],required=True)
    args=parser.parse_args()
    out=Path(__file__).resolve().parent
    data=out.parent/'r244-cpu-decode-reference-check'
    cmd=['podman','run','--rm','--name','bc250-r248-'+args.phase,
        '--userns=keep-id','--network=none','--read-only','--cap-drop=ALL',
        '--security-opt=no-new-privileges','--security-opt=label=disable',
        '--tmpfs','/tmp:rw,nosuid,nodev,size=2g','--memory=4g','--pids-limit=128',
        '--mount',f'type=bind,src={data},dst=/data,ro=true',
        '--mount',f'type=bind,src={out},dst=/out,rw=true',
        '--mount',f'type=bind,src={out.parent}/r246-cpu-b-picture-control,dst=/bdata,ro=true',
        '--mount','type=bind,src=/usr/bin/ffmpeg,dst=/host-ffmpeg,ro=true',
        '--mount','type=bind,src=/usr/lib64,dst=/hostlib,ro=true',
        'localhost/q36-agent-runtime:fedora44','python3',f'/out/{args.phase}.py']
    raise SystemExit(subprocess.run(cmd).returncode)

if __name__=='__main__':
    main()
