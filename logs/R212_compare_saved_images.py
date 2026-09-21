"""File-only comparison. No device access; no ROM contents or ROM hashes printed."""
import argparse, hashlib, json
from pathlib import Path
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('analysis'); p.add_argument('capture_a'); p.add_argument('capture_b')
a = p.parse_args()
paths = [Path(x) for x in (a.analysis, a.capture_a, a.capture_b)]
if not all(x.is_file() and not str(x.resolve()).startswith(('/dev/', '/sys/', '/proc/')) for x in paths):
    raise SystemExit('Regular saved files required')
fw, left, right = [x.read_bytes() for x in paths]
expected = '8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675'
if hashlib.sha256(fw).hexdigest() != expected:
    raise SystemExit('Analysis image hash mismatch')
def offsets(blob):
    result, start = [], 0
    while (pos := blob.find(fw, start)) >= 0:
        result.append(hex(pos)); start = pos + 1
    return result
result = dict(analysis_sha256=expected, analysis_size=len(fw),
              captures_equal=left == right, capture_sizes=[len(left),len(right)],
              match_offsets=[offsets(left),offsets(right)], hardware_access=False)
print(json.dumps(result, indent=2))
if left != right or result['match_offsets'] != [['0x8ff100'], ['0x8ff100']]:
    raise SystemExit('Saved comparison differs from R212')
