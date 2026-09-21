"""Read saved files only. Never imports hardware libraries or applies patches."""
import argparse
import hashlib
import json
from pathlib import Path


def audit(image, ihex):
    assert hashlib.sha256(image).hexdigest() == "8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675"
    assert hashlib.sha256(ihex).hexdigest() == "89a53429c6467c9a20dd00215801a49059633d258c494355a56b41535f21501e"
    memory, base, records, ended = {}, 0, 0, False
    for line in ihex.decode().splitlines():
        if not line.strip():
            continue
        assert not ended and line.startswith(":")
        b = bytes.fromhex(line[1:])
        assert len(b) == b[0] + 5 and sum(b) % 256 == 0
        addr, kind, data = int.from_bytes(b[1:3], "big"), b[3], b[4:-1]
        if kind == 0:
            records += 1
            for i, value in enumerate(data):
                assert base + addr + i not in memory
                memory[base + addr + i] = value
        elif kind == 2:
            assert len(data) == 2
            base = int.from_bytes(data, "big") << 4
        elif kind == 4:
            assert len(data) == 2
            base = int.from_bytes(data, "big") << 16
        elif kind in (3, 5):
            assert len(data) == 4  # entrypoint metadata, not a memory write
        elif kind == 1:
            assert not data
            ended = True
        else:
            raise ValueError("Unknown Intel HEX record type")
    assert ended
    unchanged = [(0x29804, 32), (0x17F24, 4), (0x29AF8, 3),
                 (0x29B11, 3), (0x29B20, 3), (0x29AD6, 3),
                 (0x29AE1, 3), (0x29CCD, 3)]
    for addr, length in unchanged:
        assert all(addr + i not in memory for i in range(length))
    checks = []
    for addr, offset, width in [(0x29B71, 0x60, 2), (0x298CB, 0xE8, 2),
                                (0x298E8, 0xEA, 2), (0x2991D, 0xEC, 4)]:
        old = image[addr:addr + 3]
        new = bytes(memory[addr + i] for i in range(3))
        # Compare operand prefix to the independently disassembled original.
        assert old[:2] == new[:2] and new[2] * width == offset
        checks.append({"site": hex(addr), "old": old.hex(), "new": new.hex(),
                       "offset": hex(offset)})
    return {"hardware_access": False, "patch_applied": False,
            "data_records": records, "checksums_valid": True,
            "unchanged_ranges": [[hex(a), n] for a, n in unchanged],
            "encoded_offset_checks": checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("saved_hex", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.image.read_bytes(), args.saved_hex.read_bytes()), indent=2))
