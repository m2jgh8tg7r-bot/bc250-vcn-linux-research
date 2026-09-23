"""Verify saved text/data against an independently supplied existing TOS body.

No instruction decoding, network calls, firmware execution, or device access.
--source-root optionally checks original exports and their recorded hashes.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct

ROOT = Path(__file__).parent
BODY_SHA = "19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("body", type=Path, help="Existing independently supplied TOS body; never downloaded")
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    body = args.body.read_bytes()
    require(hashlib.sha256(body).hexdigest() == BODY_SHA, "Wrong body hash")
    require(len(body) == 82256, "Wrong body length")
    index = json.loads((ROOT / "saved-instruction-index.json").read_text())
    manifest = json.loads((ROOT / "evidence-manifest.json").read_text())
    source_lines = {}
    if args.source_root:
        for entry in manifest["sources"]:
            data = (args.source_root / entry["path"]).read_bytes()
            require(hashlib.sha256(data).hexdigest() == entry["sha256"], "Export hash mismatch: " + entry["path"])
            require(len(data) == entry["bytes"], "Export size mismatch")
            source_lines[entry["path"]] = data.decode().splitlines()
    compared = 0
    text_only = 0
    for addr, entry in index["instructions"].items():
        offset = int(addr, 16) - 0x200000
        require(offset == int(entry["body_offset"], 16), "Coordinate mismatch")
        if entry["bytes"]:
            expected = bytes.fromhex(entry["bytes"])
            require(body[offset:offset + len(expected)] == expected, "Instruction-byte mismatch: " + addr)
            compared += 1
        else:
            text_only += 1
        if source_lines:
            for source in entry["sources"]:
                line = source_lines[source["path"]][source["line"] - 1]
                require(line.startswith("INS=" + entry["address"] + " "), "Source address mismatch")
                rest = line.split(" ", 1)[1]
                first, sep, remaining = rest.partition(" ")
                if re.fullmatch(r"(?:[0-9a-fA-F]{2}){2,8}", first):
                    require(first.lower() == entry["bytes"], "Source byte mismatch")
                    rest = remaining
                require(rest == entry["asm"], "Source assembly-text mismatch: " + addr)
    for addr, value in index["literals"].items():
        offset = int(addr, 16) - 0x200000
        require(struct.unpack_from("<I", body, offset)[0] == int(value, 16), "Literal mismatch: " + addr)
    dispatch = json.loads((ROOT / "dispatch-table-verification.json").read_text())
    for svc, entry in dispatch["svc_targets"].items():
        offset = 0x45E4 + 4 * (int(svc, 16) - 0x51)
        relative = struct.unpack_from("<I", body, offset)[0]
        require(offset == int(entry["table_body_offset"], 16), "Dispatch index mismatch")
        require(body[offset:offset + 4].hex() == entry["raw_le"], "Dispatch byte mismatch")
        require(0x45E4 + relative == int(entry["target_body_offset"], 16), "Dispatch target mismatch")
    require(body[0xFE8C:0xFE9C] == b"amd.dr.driverID\0", "Property key mismatch")
    require(0x10582 + 2 * body[0x10582 + 8] == 0x1064E, "Host command-8 TBB target mismatch")
    require(index["instructions"]["0x21065a"]["asm"] == "bl 0x0020f18c", "Host command-8 wrapper mismatch")
    for literal_offset, body_target in ((0xE040, 0x11608), (0x11770, 0x122C4)):
        user_pointer = struct.unpack_from("<I", body, literal_offset)[0]
        require((user_pointer & ~1) - 0x200000 + 0xE000 == body_target,
                "User-section pointer-pair mismatch")
    for entry in json.loads((ROOT / "coordinate-recheck.json").read_text())["coordinate_pairs"]:
        require(int(entry["candidate_body_offset"], 16) == int(entry["user_va"], 16) - 0x200000 + 0xE000,
                "Candidate user coordinate mismatch")
        for offset_key, value_key in (("candidate_body_offset", "candidate_saved_u32"),
                                      ("wrong_uniform_base_offset", "wrong_offset_saved_u32")):
            require(struct.unpack_from("<I", body, int(entry[offset_key], 16))[0] == int(entry[value_key], 16),
                    "Coordinate comparison data mismatch")
    result = {"result": "PASS", "classification": "PROVEN_STATICALLY", "body_sha256": BODY_SHA,
              "instruction_byte_matches": compared, "text_only_instructions": text_only,
              "literal_matches": len(index["literals"]), "source_files_checked": len(source_lines),
              "dispatch_entries_checked": len(dispatch["svc_targets"]), "hardware_access": False,
              "method": "Byte and source-text equality; no fresh disassembly"}
    (ROOT / "evidence-audit-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
