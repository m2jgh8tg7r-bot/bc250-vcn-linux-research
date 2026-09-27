"""Offline container integrity checks; not signature verification or execution."""
import argparse
import hashlib
import json
import lzma
import struct
import zlib
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def u32(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


def container(data):
    # Only the uncompressed, unencrypted, type-0 control format in this set.
    if len(data) < 512 or data[16:20] != b'$PS1':
        raise ValueError('container header')
    if u32(data, 0x18) != 0 or u32(data, 0x48) != 0:
        raise ValueError('unsupported encoded body')
    if u32(data, 0x30) != 1 or u32(data, 0x34) != 0:
        raise ValueError('unsupported signature layout')
    size = u32(data, 0x14)
    if size + 512 != len(data) or u32(data, 0x6c) != len(data):
        raise ValueError('container bounds')
    flags = struct.unpack_from('>I', data, 0x58)[0]
    if not flags & 1:
        raise ValueError('SHA256 flag absent')
    body = data[256:256+size]
    if hashlib.sha256(body).digest() != data[0xd0:0xf0]:
        raise ValueError('body SHA256 mismatch')
    return dict(container_sha256=digest(data), container_size=len(data),
                body_size=size, body_sha256=digest(body),
                signer=data[0x38:0x48].hex(), signature_bytes=256,
                checksum_flags_be=hex(flags), body_hash_matches=True,
                signature_verified=False)


def audit(root):
    base = root/'r180-load-response-observation/initramfs-tree/usr/lib/firmware/amdgpu'
    rows, first = [], None
    for suffix in ('ce', 'me', 'mec', 'mec2', 'pfp', 'rlc', 'sdma', 'sdma1'):
        name = f'cyan_skillfish2_{suffix}.bin.xz'
        data = lzma.decompress((base/name).read_bytes())
        total, header = struct.unpack_from('<II', data)
        size, offset, crc = struct.unpack_from('<III', data, 20)
        if total != len(data) or not 32 <= header <= offset or offset+size != total:
            raise ValueError('common header bounds')
        payload = data[offset:]
        spans = [('main', 0, size)]
        if suffix in ('mec', 'mec2'):
            jt_offset, jt_size = u32(data, 36)*4, u32(data, 40)*4
            if jt_offset + jt_size != size:
                raise ValueError('JT partition bounds')
            spans = [('main', 0, jt_offset), ('jump_table', jt_offset, jt_size)]
        for role, start, length in spans:
            part = payload[start:start+length]
            result = container(part)
            rows.append(dict(file=name, file_sha256=digest(data), role=role,
                             relative_payload_offset=start, **result,
                             outer_header_crc=hex(crc),
                             outer_full_payload_crc=hex(zlib.crc32(payload)),
                             outer_full_payload_crc_matches=zlib.crc32(payload)==crc))
            if first is None:
                first = part
    negatives = []
    for label, off in [('changed_body', 256), ('changed_magic', 16),
                       ('changed_body_size', 0x14), ('changed_stored_hash', 0xd0)]:
        bad = bytearray(first)
        bad[off] ^= 1
        try:
            container(bytes(bad))
        except ValueError as exc:
            negatives.append(dict(case=label, rejected=True, reason=str(exc)))
        else:
            raise AssertionError(label)
    try:
        container(first[:-1])
    except ValueError as exc:
        negatives.append(dict(case='truncated_container', rejected=True, reason=str(exc)))
    else:
        raise AssertionError('truncated_container')
    assert len(rows) == 10
    assert len({r['signer'] for r in rows}) == 1
    return dict(result='PASS', scope='saved control container integrity only',
                containers=rows, container_occurrences=len(rows),
                distinct_containers=len({r['container_sha256'] for r in rows}),
                distinct_files=len({r['file_sha256'] for r in rows}),
                negative_controls=negatives,
                limitations=['No public-key signature verification',
                            'No running firmware identity or acceptance inference',
                            'Outer CRC mismatch convention unresolved'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.root)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('result', 'container_occurrences',
                                           'distinct_containers', 'distinct_files')}))
