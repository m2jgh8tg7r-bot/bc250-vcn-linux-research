#!/usr/bin/env python3
"""Offline extended-netconsole analysis. Input: one explicitly isolated boot/session."""
import argparse
import base64
import json
import re
from collections import defaultdict
from pathlib import Path

HEADER = re.compile(rb'^(\d+),(\d+),(\d+),([^,;]+)((?:,[^;]+)*);', re.S)
FRAG = re.compile(rb'ncfrag=(\d+)/(\d+)$')
MAX_RECORD = 1024 * 1024


def parse(data):
    m = HEADER.match(data)
    if not m:
        raise ValueError('not supported basic extended header (release prefix unsupported)')
    level, seq, stamp = map(int, m.group(1, 2, 3))
    if level > 191 or seq >= 2**64 or stamp >= 2**64:
        raise ValueError('header value outside supported range')
    body = data[m.end():]
    offset, total = 0, len(body)
    fragments = []
    for field in m.group(5).split(b',')[1:]:
        if field.startswith(b'ncfrag='):
            f = FRAG.fullmatch(field)
            if not f:
                raise ValueError('malformed ncfrag')
            fragments.append(tuple(map(int, f.groups())))
    if len(fragments) > 1:
        raise ValueError('duplicate ncfrag header')
    if fragments:
        offset, total = fragments[0]
    if total > MAX_RECORD or offset + len(body) > total or total < 1:
        raise ValueError('invalid fragment extent or record too large')
    return seq, (level, stamp, m.group(4), total), offset, body


def analyze(rows):
    groups = defaultdict(list)
    errors = []
    sessions = set()
    for i, row in enumerate(rows):
        sessions.add(row.get('session'))
        try:
            data = base64.b64decode(row['payload_b64'], validate=True)
            seq, metadata, offset, body = parse(data)
            groups[seq].append((metadata, offset, body))
        except (ValueError, KeyError, TypeError) as exc:
            errors.append({'row': i, 'reason': str(exc)})
    if len(sessions) != 1 or None in sessions:
        raise ValueError('exactly one explicit capture session required; never merge boots')
    records = []
    for seq, parts in sorted(groups.items()):
        metas = {p[0] for p in parts}
        conflict = len(metas) != 1
        total = parts[0][0][3]
        buf, seen = bytearray(total), bytearray(total)
        unique = set()
        duplicates = 0
        for meta, offset, body in parts:
            key = (meta, offset, body)
            if key in unique:
                duplicates += 1
            unique.add(key)
            if meta != parts[0][0]:
                continue
            for n, byte in enumerate(body, offset):
                if seen[n] and buf[n] != byte:
                    conflict = True
                seen[n], buf[n] = 1, byte
        complete = all(seen) and not conflict
        records.append({'sequence': seq, 'complete': complete, 'conflict': conflict,
                        'missing_bytes': total - sum(seen), 'duplicate_datagrams': duplicates,
                        'text': buf.decode('utf-8', errors='replace') if complete else None})
    seqs = sorted(groups)
    gaps = [[a + 1, b - 1] for a, b in zip(seqs, seqs[1:]) if b > a + 1]
    return {'session': next(iter(sessions)), 'records': records,
            'interior_missing_sequence_ranges': gaps, 'invalid_rows': errors,
            'prefix_completeness': 'UNKNOWN', 'suffix_completeness': 'UNKNOWN',
            'boot_identity': 'operator isolation required; session ID is not a boot ID',
            'loss_location': 'UNKNOWN', 'hardware_execution': 'NOT_INFERRED'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('capture', type=Path)
    args = ap.parse_args()
    print(json.dumps(analyze(json.loads(line) for line in args.capture.read_text().splitlines() if line), indent=2))
