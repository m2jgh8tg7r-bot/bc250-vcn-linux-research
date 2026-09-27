"""Build the pinned public CPU decoder harness in a device-free container."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

FILES = ['tools/h264dec.c', 'src/decoder_h264.c', 'src/h264_mb_cabac.c',
         'src/h264_mb_cavlc.c', 'src/h264_cavlc_dec.c', 'src/h264_mb_motion.c',
         'src/h264_recon_mb.c', 'src/h264_recon.c', 'src/h264_pred.c',
         'src/h264_mc.c', 'src/h264_deblock.c', 'src/h264_threads.c',
         'src/h264_dec_tables.c', 'src/cabac.c']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--headers', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--image', default='localhost/q36-agent-runtime:fedora44')
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(exist_ok=True, parents=True)
    cmd = ['podman','run','--rm','--name','bc250-r244-cpu-build',
        '--userns=keep-id', f'--user={os.getuid()}:{os.getgid()}',
        '--network=none','--read-only','--cap-drop=ALL',
        '--security-opt=no-new-privileges','--security-opt=label=disable',
        '--tmpfs','/tmp:rw,nosuid,nodev,size=256m','--memory=2g','--cpus=2',
        '--pids-limit=128','--mount',f'type=bind,src={args.source.resolve()},dst=/source,ro=true',
        '--mount',f'type=bind,src={args.headers.resolve()},dst=/headers,ro=true',
        '--mount',f'type=bind,src={out},dst=/out,rw=true',args.image,
        'gcc','-O2','-g','-Wall','-Wextra','-std=gnu11','-I/source/src',
        '-I/source/include','-I/headers','-o','/out/h264dec']
    cmd += ['/source/'+name for name in FILES] + ['-pthread','-lm']
    start = time.monotonic()
    with (out/'build-with-headers.log').open('w') as stream:
        result = subprocess.run(cmd, stdout=stream, stderr=subprocess.STDOUT, timeout=180)
    record = dict(returncode=result.returncode, seconds=time.monotonic()-start,
        source_files=[dict(path=f, sha256=hashlib.sha256((args.source/f).read_bytes()).hexdigest()) for f in FILES],
        gpu_device_exposed=False, network='none', container_image=args.image,
        source_read_only=True, only_writable_host_mount_is_output=True, temporary_tmpfs_writable=True)
    if result.returncode == 0:
        record['binary_sha256'] = hashlib.sha256((out/'h264dec').read_bytes()).hexdigest()
    (out/'build-with-headers.json').write_text(json.dumps(record, indent=2)+'\n')
    print('CPU harness build return code', result.returncode)
    raise SystemExit(result.returncode)
