import struct, unittest
from inspect_discovery import inspect, InvalidDiscovery

def capture(dies, wide=False, version=1, post=False):
    start = 64
    data = bytearray(start + 80)
    struct.pack_into('<IHHHH', data, 0, 0x28211407, version, 0, 0, 0)
    table = 16 if version == 2 else 12
    if version == 2:
        struct.pack_into('<HH', data, 12, 1, 0)
    struct.pack_into('<IHHIH', data, start, 0x53445049, 4 if wide else 3, 0, 0, len(dies))
    data[start + 78] = int(wide)
    for die, records in enumerate(dies):
        struct.pack_into('<HH', data, start + 14 + die * 4, die, len(data))
        data.extend(struct.pack('<HH', die, len(records)))
        for hw, inst, bases in records:
            data.extend(struct.pack('<HBBBBBB', hw, inst, len(bases), 2, 0, 3, 0))
            if wide and post:
                data.extend(b''.join(struct.pack('<I', x) for x in bases) + b'\0' * (4 * len(bases)))
            else:
                data.extend(b''.join(struct.pack('<Q' if wide else '<I', x) for x in bases))
    struct.pack_into('<H', data, 10, len(data))
    struct.pack_into('<HHH', data, table, start, 0, len(data) - start)
    struct.pack_into('<H', data, start + 6, len(data) - start)
    return data

class ReaderTests(unittest.TestCase):
    def test_triplet(self):
        r=inspect(capture([[(12,0,[0x7800,0x7e00,0x2403000])]]),'wire')
        self.assertEqual(r['vcn_records'][0]['converted_bases'][1],0x7e00)
    def test_same_die_duplicate(self):
        r=inspect(capture([[(12,0,[1,2]),(12,0,[3])]]),'wire')
        self.assertEqual(r['duplicate_vcn_instances'],{'0':2})
        self.assertEqual(r['last_vcn_record_by_instance']['0']['count'],1)
    def test_cross_die_duplicate(self):
        r=inspect(capture([[(12,0,[1])],[(12,0,[2])]]),'wire')
        self.assertEqual(r['last_vcn_record_by_instance']['0']['die'],1)
    def test_zero_count(self):
        self.assertEqual(inspect(capture([[(12,0,[])]]),'wire')['vcn_records'][0]['bases'],[])
    def test_wide_wire(self):
        r=inspect(capture([[(12,0,[0xabcdef0040007800,0x1234000000007e00])]],wide=True),'wire')
        self.assertEqual(r['vcn_records'][0]['converted_bases'],[0x7800,0x7e00])
    def test_wide_post_parser(self):
        b=capture([[(12,0,[0x7800,0x7e00,0x2403000])]],wide=True,post=True)
        self.assertEqual(inspect(b,'post-parser-le32')['vcn_records'][0]['bases'],[0x7800,0x7e00,0x2403000])
        self.assertNotEqual(inspect(b,'wire')['vcn_records'][0]['converted_bases'],[0x7800,0x7e00,0x2403000])
    def test_v2(self):
        self.assertEqual(inspect(capture([[(12,0,[1])]],version=2),'wire')['binary_version'],2)
    def test_every_truncation(self):
        b=capture([[(12,0,[1,2,3])]])
        for n in range(len(b)):
            with self.assertRaises(InvalidDiscovery): inspect(b[:n],'wire')
    def test_bad_die_offset(self):
        b=capture([[(12,0,[1])]]);struct.pack_into('<H',b,80,65535)
        with self.assertRaises(InvalidDiscovery):inspect(b,'wire')
    def test_overlapping_dies(self):
        b=capture([[(12,0,[1])],[(12,0,[2])]])
        struct.pack_into('<H',b,84,struct.unpack_from('<H',b,80)[0])
        with self.assertRaises(InvalidDiscovery):inspect(b,'wire')
    def test_bad_count(self):
        b=capture([[(12,0,[1])]]);b[151]=255
        with self.assertRaises(InvalidDiscovery):inspect(b,'wire')
    def test_explicit_encoding(self):
        with self.assertRaises(InvalidDiscovery):inspect(b'',None)

if __name__=='__main__':unittest.main()
