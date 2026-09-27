"""Fetch only public GitLab HEAD headers; never download firmware bodies.

This optional fetcher is separate from the offline verification script.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import lzma
import urllib.parse
import urllib.request
from pathlib import Path

API = 'https://gitlab.com/api/v4/projects/kernel-firmware%2Flinux-firmware/repository/files/'
REFS = ['f704766b41b9324e3d679156e0ad5ff9428d7146',
        'd371ae3b6888b260e4c37b327a020401cfaaaefd',
        '9b858e5bb58d7bf1fc4d8818cb9100aed6d46f6a']
SUFFIXES = ['ce', 'me', 'mec', 'mec2', 'pfp', 'rlc', 'sdma', 'sdma1']


def fetch(base, ref, suffix):
    name = f'cyan_skillfish2_{suffix}.bin'
    data = lzma.decompress((base/(name+'.xz')).read_bytes())
    sha = hashlib.sha256(data).hexdigest()
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    url = API + urllib.parse.quote('amdgpu/'+name, safe='') + '?ref=' + ref
    request = urllib.request.Request(url, method='HEAD', headers={'User-Agent':'BC250-provenance-audit'})
    with urllib.request.urlopen(request, timeout=45) as response:
        metadata = {k: response.headers['X-Gitlab-'+k] for k in
            ['blob-id','commit-id','content-sha256','file-path','last-commit-id','size']}
    if any(v is None for v in metadata.values()):
        raise ValueError('Missing metadata header')
    return dict(ref=ref, file=name, url=url, method='HEAD', metadata=metadata,
        local_sha256=sha, local_git_blob_sha1=blob,
        sha256_matches=sha==metadata['content-sha256'], blob_matches=blob==metadata['blob-id'],
        size_matches=len(data)==int(metadata['size']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--firmware-directory', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetch, args.firmware_directory, ref, suffix)
                   for ref in REFS for suffix in SUFFIXES]
        rows = [f.result() for f in futures]
    args.output.write_text(json.dumps(dict(
        checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scope='Official file metadata only; no firmware payload downloaded', results=rows), indent=2)+'\n')
    print('Fetched', len(rows), 'HEAD metadata records')
