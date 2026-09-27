"""Compare retained firmware metadata with saved KDBs and verified old logs.

No firmware execution, signature verification, hardware access or bypass.
The log parser is reused from R180; source files remain in the research tree.
"""
import argparse
import hashlib
import importlib.util
import json
import lzma
import struct
import sys
import zlib
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def metadata(data, require_crc=False):
    assert len(data) >= 256, 'short common header'
    total, header = struct.unpack_from('<II', data)
    size, offset, crc = struct.unpack_from('<III', data, 20)
    assert total == len(data) and 32 <= header <= offset, 'common header bounds'
    assert offset + size == len(data) and size >= 0x80, 'payload bounds'
    payload = data[offset:offset+size]
    crc_matches = zlib.crc32(payload) == crc
    if require_crc:
        assert crc_matches, 'payload CRC'
    return dict(file_sha256=sha(data), payload_sha256=sha(payload), size=size,
                offset=offset, signer=payload[0x38:0x48].hex(),
                header_7f=payload[0x7f], header_crc=hex(crc),
                whole_payload_zlib_crc=hex(zlib.crc32(payload)),
                whole_payload_crc_matches=crc_matches)


def run(root, captures):
    sys.path.insert(0, str(root/'r180-load-response-observation'))
    spec = importlib.util.spec_from_file_location('r180_collected', root/'r180-load-response-observation/analyze_collected.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    checked = []
    for i, path in enumerate(captures, 1):
        result = module.evaluate(path)
        assert result['module_and_boot_attributed'] and result['trace_structure_valid']
        assert result['trace_pair_count'] == 11 and result['accepted_control_count'] == 5
        assert result['observation_complete'] == 'PROVEN_LIVE'
        checked.append(dict(label=f'capture_{i}', capture_hashes_verified=result['capture_hashes_verified'],
                            journal_sha256=sha((path/'kernel-journal.txt').read_bytes()),
                            pairs=[dict(begin=x['begin'], end=x['end']) for x in result['trace_pairs']]))
    signature = lambda r: [(x['begin']['id'], x['begin']['fw_type'], x['begin']['size'],
                            x['end']['status'], x['end']['fw_addr_nonzero']) for x in r['pairs']]
    assert all(signature(x)==signature(checked[0]) for x in checked)
    # IDs and mapping are version-specific to the retained R180 source/headers.
    files = {1:('sdma',9), 2:('sdma1',10), 12:('ce',3), 13:('pfp',2),
             14:('me',1), 26:('mec',4), 28:('mec2',4), 50:('rlc',8)}
    base = root/'r180-load-response-observation/initramfs-tree/usr/lib/firmware/amdgpu'
    meta_path = root/'r233-service1-bootstrap-provenance/key-metadata-audit.json'
    dbs = json.loads(meta_path.read_text())['images']
    rows = []
    for ident, (suffix, fw_type) in files.items():
        filename = f'cyan_skillfish2_{suffix}.bin.xz'
        raw = (base/filename).read_bytes()
        second = root/'r173-request-observation/initramfs-tree/usr/lib/firmware/amdgpu'/filename
        assert raw == second.read_bytes(), 'Retained R173/R180 file mismatch'
        data = lzma.decompress(raw)
        m = metadata(data)
        size = m['size']
        if suffix in ('mec','mec2'):
            size -= struct.unpack_from('<I', data, 40)[0]*4
        pair = next(x for x in checked[0]['pairs'] if x['begin']['id']==ident)
        assert pair['begin']['fw_type'] == fw_type and pair['begin']['size'] == size
        assert pair['end']['status'] == 0
        matches = [dict(image=db['label'], directory_type=k['directory_type'], usage=r['usage'])
                   for db in dbs for k in db['kdbs'] for r in k['records'] if r['key_id_bytes']==m['signer']]
        assert len(matches)==5 and all(x['directory_type']=='0x51' and x['usage']==10 for x in matches)
        rows.append(dict(id=ident, fw_type=fw_type, file=filename, stored_sha256=sha(raw),
                         metadata=m, submitted_size=size, matches=matches,
                         second_saved_copy_identical=True,
                         historical_status='0x0', placement_nonzero=bool(pair['end']['fw_addr_nonzero'])))
    vcn_data = (base/'vcn_2_0_3.bin').read_bytes()
    vcn = metadata(vcn_data, require_crc=True)
    pair = next(x for x in checked[0]['pairs'] if x['begin']['id']==57)
    assert pair['begin']['size']==vcn['size'] and pair['end']['status']==0xffff0008
    assert all(r['key_id_bytes']!=vcn['signer'] for db in dbs for k in db['kdbs'] for r in k['records'])
    # Meaningful malformed-input controls: do not silently compare corrupt headers.
    bad = bytearray(vcn_data); bad[-1] ^= 1
    negative = []
    for label, candidate in [('truncated_payload', vcn_data[:-1]), ('changed_vcn_payload', bytes(bad)), ('short_header', vcn_data[:16])]:
        try:
            metadata(candidate, require_crc=True)
        except AssertionError:
            negative.append(label)
        else:
            raise AssertionError('Malformed metadata accepted: '+label)
    return dict(result='PASS', scope='Saved metadata and revalidated historical captures, not new hardware observations',
                captures=checked, control_files=rows, vcn=vcn,
                distinct_control_file_hashes=sorted({r['metadata']['file_sha256'] for r in rows}),
                distinct_kdb_body_hashes=sorted({k['body_sha256'] for db in dbs for k in db['kdbs']}),
                kdb_metadata_sha256=sha(meta_path.read_bytes()), negative_controls_rejected=negative,
                excluded_ids=[27,29], excluded_reason='MEC jump-table subpayloads; do not apply outer signer-header parsing to them',
                limits=['Same-log ID/type/size consistency does not prove retained file equals every PSP-visible historical byte',
                        'No claim of signature authentication, actual KDB selection or VCN failure root cause',
                        'Five saved images contain only two distinct KDB bodies; not ten independent KDBs',
                        'Control-file header CRC does not match zlib CRC over the whole declared payload; checksum convention/origin unresolved, files hash-pinned and identical in two retained trees',
                        'A matching public signer record is necessary only under the candidate lookup assumptions, not sufficient for acceptance'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--capture', type=Path, action='append', required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = run(a.root, a.capture)
    a.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(result=result['result'], captures=len(result['captures']),
                         control_files=len(result['control_files']), distinct_kdb_bodies=len(result['distinct_kdb_body_hashes']),
                         negative_controls=len(result['negative_controls_rejected']))))
