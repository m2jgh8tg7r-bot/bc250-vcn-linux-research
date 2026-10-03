"""Offline discovery inventory. Never opens hardware paths or assumes raw encoding."""
import argparse, json, struct
from pathlib import Path

class InvalidDiscovery(ValueError):
    pass

def inspect(data, encoding):
    if encoding not in ('wire', 'post-parser-le32'):
        raise InvalidDiscovery('explicit encoding required')
    def bound(off, length, limit=None):
        end = len(data) if limit is None else limit
        if off < 0 or length < 0 or off > end or length > end - off:
            raise InvalidDiscovery('out of bounds')
    def u16(off):
        bound(off, 2)
        return struct.unpack_from('<H', data, off)[0]
    def u32(off):
        bound(off, 4)
        return struct.unpack_from('<I', data, off)[0]
    bound(0, 12)
    if u32(0) != 0x28211407:
        raise InvalidDiscovery('binary signature')
    version, total = u16(4), u16(10)
    bound(0, total)
    if total < 12:
        raise InvalidDiscovery('binary size')
    if version in (0, 1):
        table = 12
    elif version == 2:
        bound(12, 4, total)
        if u16(12) < 1:
            raise InvalidDiscovery('no tables')
        table = 16
        bound(table, u16(12) * 8, total)
    else:
        raise InvalidDiscovery('binary version')
    bound(table, 8, total)
    start, table_size = u16(table), u16(table + 4)
    bound(start, table_size, total)
    bound(start, 80, start + table_size)
    if u32(start) != 0x53445049:
        raise InvalidDiscovery('IP signature')
    ip_version, size, ndies = u16(start + 4), u16(start + 6), u16(start + 12)
    if ip_version not in (1, 2, 3, 4) or ndies > 16 or size < 80 or size > table_size:
        raise InvalidDiscovery('IP header')
    end = start + size
    wide = bool(data[start + 78] & 1) if ip_version == 4 else False
    records, spans = [], []
    for die in range(ndies):
        off = u16(start + 14 + die * 4 + 2)
        if off < start + 80:
            raise InvalidDiscovery('die overlaps header')
        bound(off, 4, end)
        if u16(off) != die:
            raise InvalidDiscovery('die ID')
        count, cur = u16(off + 2), off + 4
        spans.append((off, off + 4))
        for ordinal in range(count):
            bound(cur, 8, end)
            hw, instance, nbase = u16(cur), data[cur + 2], data[cur + 3]
            extent = 8 + nbase * (8 if wide else 4)
            bound(cur, extent, end)
            spans.append((cur, cur + extent))
            if wide and encoding == 'wire':
                bases = [struct.unpack_from('<Q', data, cur + 8 + k * 8)[0] for k in range(nbase)]
                selected = [(x & 0xffffffff) & 0x3fffffff for x in bases]
            else:
                bases = [u32(cur + 8 + k * 4) for k in range(nbase)]
                selected = bases
            records.append({'die': die, 'ordinal': ordinal, 'record_offset': cur,
                            'hw_id': hw, 'instance': instance, 'count': nbase,
                            'bases': bases, 'converted_bases': selected})
            cur += extent
    spans.sort()
    if any(b[0] < a[1] for a, b in zip(spans, spans[1:])):
        raise InvalidDiscovery('overlapping records/dies')
    vcn = [r for r in records if r['hw_id'] == 12]
    grouped = {}
    for r in vcn:
        grouped.setdefault(str(r['instance']), []).append(r)
    return {'encoding': encoding, 'binary_version': version, 'ip_version': ip_version,
            'base_addr_64_bit': wide, 'record_count': len(records), 'vcn_records': vcn,
            'last_vcn_record_by_instance': {k: v[-1] for k, v in grouped.items()},
            'duplicate_vcn_instances': {k: len(v) for k, v in grouped.items() if len(v) > 1},
            'checksum_status': 'NOT_VALIDATED: post-parser mutation may invalidate wire checksums',
            'limit': 'Offline record inventory; not final live pointer or VCPU evidence'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('capture', type=Path)
    p.add_argument('--encoding', required=True, choices=('wire', 'post-parser-le32'))
    args = p.parse_args()
    print(json.dumps(inspect(args.capture.read_bytes(), args.encoding), indent=2))
