import base64
import unittest
from analyze import analyze


def row(payload, session='synthetic-one-boot'):
    return {'session': session, 'payload_b64': base64.b64encode(payload).decode()}


class CaptureTests(unittest.TestCase):
    def test_reordered_duplicate_and_gap(self):
        a = row(b'6,12,120,-;last')
        r = analyze([a, row(b'6,10,100,-;first'), a])
        self.assertEqual(r['interior_missing_sequence_ranges'], [[11, 11]])
        self.assertEqual(r['records'][1]['duplicate_datagrams'], 1)
        self.assertEqual(r['suffix_completeness'], 'UNKNOWN')

    def test_fragments_reordered(self):
        r = analyze([row(b'0,5,50,-,ncfrag=3/6;def'), row(b'0,5,50,-,ncfrag=0/6;abc')])
        self.assertEqual(r['records'][0]['text'], 'abcdef')

    def test_hole_not_execution(self):
        r = analyze([row(b'0,5,50,-,ncfrag=3/6;def')])
        self.assertFalse(r['records'][0]['complete'])
        self.assertIsNone(r['records'][0]['text'])

    def test_overlap_conflict(self):
        r = analyze([row(b'0,5,50,-,ncfrag=0/4;abc'), row(b'0,5,50,-,ncfrag=2/4;Xd')])
        self.assertTrue(r['records'][0]['conflict'])

    def test_sequence_reuse_conflict(self):
        r = analyze([row(b'0,5,50,-;abc'), row(b'0,5,1,-;abc')])
        self.assertTrue(r['records'][0]['conflict'])

    def test_mixed_sessions_rejected(self):
        with self.assertRaises(ValueError):
            analyze([row(b'0,5,50,-;abc'), row(b'0,6,60,-;def', 'other')])

    def test_bad_inputs(self):
        r = analyze([row(b'[1.0] old basic log'), row(b'0,1,1,-,ncfrag=0/999999999;abc'), row(b'0,1,1,-,ncfrag=x/3;abc')])
        self.assertEqual(len(r['invalid_rows']), 3)
        self.assertEqual(r['records'], [])

    def test_valid_overlap(self):
        r = analyze([row(b'0,5,50,-,ncfrag=0/4;abc'), row(b'0,5,50,-,ncfrag=2/4;cd')])
        self.assertEqual(r['records'][0]['text'], 'abcd')


if __name__ == '__main__':
    unittest.main()
