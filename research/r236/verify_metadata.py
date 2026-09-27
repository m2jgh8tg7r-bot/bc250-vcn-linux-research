"""Offline verification of saved official HEAD metadata against retained files."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path


def verify(root, metadata):
    obj = json.loads(metadata.read_text())
    base = root/'r180-load-response-observation/initramfs-tree/usr/lib/firmware/amdgpu'
    expected_refs = {'f704766b41b9324e3d679156e0ad5ff9428d7146',
                     'd371ae3b6888b260e4c37b327a020401cfaaaefd',
                     '9b858e5bb58d7bf1fc4d8818cb9100aed6d46f6a'}
    expected_files = {f'cyan_skillfish2_{s}.bin' for s in
                      ('ce','me','mec','mec2','pfp','rlc','sdma','sdma1')}
    pairs = [(row['ref'], row['file']) for row in obj['results']]
    assert len(pairs) == len(set(pairs)) == 24, 'duplicate or missing file/ref pair'
    assert set(pairs) == {(ref, name) for ref in expected_refs for name in expected_files}, 'coverage'
    groups = {}
    for row in obj['results']:
        data = lzma.decompress((base/(row['file']+'.xz')).read_bytes())
        sha = hashlib.sha256(data).hexdigest()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        m = row['metadata']
        assert m['commit-id'] == row['ref']
        assert m['file-path'] == 'amdgpu/'+row['file']
        assert row['method'] == 'HEAD'
        checks = [sha == m['content-sha256'], blob == m['blob-id'], len(data) == int(m['size'])]
        assert checks == [row['sha256_matches'], row['blob_matches'], row['size_matches']]
        assert sha == row['local_sha256'] and blob == row['local_git_blob_sha1']
        groups.setdefault(row['ref'], []).append(dict(file=row['file'], matches=all(checks),
            sha256_matches=checks[0], git_blob_matches=checks[1], size_matches=checks[2],
            last_commit=m['last-commit-id']))
    assert len(obj['results']) == 24 and all(len(v)==8 for v in groups.values())
    counts = {k: sum(x['matches'] for x in v) for k,v in groups.items()}
    assert sorted(counts.values()) == [3, 8, 8]
    return dict(result='PASS', metadata_sha256=hashlib.sha256(metadata.read_bytes()).hexdigest(),
        observations=24, matching=19, by_ref=groups,
        scope='Decompressed file provenance; no signature validation or live identity',
        caveat='HEAD metadata is an HTTPS server claim, not a locally cloned Git object or signed attestation')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--metadata', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r = verify(a.root, a.metadata)
    a.output.write_text(json.dumps(r, indent=2)+'\n')
    print(r['result'], r['matching'], '/', r['observations'])
