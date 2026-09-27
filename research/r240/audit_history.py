"""Offline metadata comparison of already-retained R184 VCN versions.

No firmware execution, disassembly, signature validation, mutation or download.
VCN is not passed to R237's distinct $PS1 control-container parser.
"""
import argparse
import hashlib
import importlib.util
import json
import struct
from pathlib import Path


def audit(root):
    verifier = root/'r184-firmware-history/verify.py'
    spec = importlib.util.spec_from_file_location('r184_verify', verifier)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    old = module.verify()
    metadata_path = root/'r233-service1-bootstrap-provenance/key-metadata-audit.json'
    databases = json.loads(metadata_path.read_text())['images']
    rows = []
    for item in old['versions']:
        path = root/'r184-firmware-history/blobs'/(item['commit']+'.bin')
        data = path.read_bytes()
        size, offset = struct.unpack_from('<II', data, 20)
        payload = data[offset:offset+size]
        if len(payload) < 0x80:
            raise ValueError('short retained metadata')
        # Fixed saved VCN metadata field established in R233, not a generic parser.
        signer = payload[0x38:0x48].hex()
        hits = [dict(image=db['label'], directory_type=k['directory_type'], usage=record['usage'])
                for db in databases for k in db['kdbs'] for record in k['records']
                if record['key_id_bytes'] == signer]
        rows.append(dict(commit=item['commit'], date=item['date'],
            file_sha256=item['sha256'], payload_sha256=item['payload_sha256'],
            ucode_version=item['ucode_version'], payload_size=size,
            bounds_and_outer_crc_verified=True,
            signer_metadata=signer, saved_key_metadata_matches=hits,
            signature_verified=False, live_acceptance='UNPROVEN'))
    assert len(rows) == 21 and len({x['payload_sha256'] for x in rows}) == 21
    assert {x['signer_metadata'] for x in rows} == {'c37290c310e64a62b027c56695492368'}
    assert all(not x['saved_key_metadata_matches'] for x in rows)
    return dict(result='PASS', source='existing R184 saved 21-version path history',
        verifier_sha256=hashlib.sha256(verifier.read_bytes()).hexdigest(),
        key_metadata_sha256=hashlib.sha256(metadata_path.read_bytes()).hexdigest(),
        versions=rows, distinct_signer_metadata=1, distinct_payloads=21,
        kdb_occurrences=sum(len(x['kdbs']) for x in databases),
        distinct_kdb_bodies=len({k['body_sha256'] for x in databases for k in x['kdbs']}),
        limitations=['Only this saved path history; not all firmware in existence',
            'No cryptographic signature verification', 'No running KDB identity',
            'No proof of all historical versions failing live',
            'No inference that signer metadata is the sole compatibility requirement'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.root)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print('PASS: 21 distinct payloads, one signer metadata value, zero saved-key matches')
