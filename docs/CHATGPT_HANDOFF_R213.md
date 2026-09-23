# R213 — Separate SMU body from the retained signature trailer

2026-09-22. Saved regular files only; no hardware access or mutation.

R212 correctly established that the complete 262,400-byte analysis file occurs in saved BIOS. R213 resolves its static container boundary: the analysis file comprises a 262,144-byte body followed by a 256-byte trailer, interpreted as the signature by the pinned PSPTool parser. Do not treat its entire length as executable firmware or SRAM length.

The preceding 256-byte header starts at ROM offset `0x8ff000`. Its magic is `$PS1`; signed and uncompressed sizes are both `0x40000`, signed=1, signature type=0, encryption=0, compression=0, and container size=`0x40200`. Under [PSPTool's header parser at 6112e48](https://github.com/PSPReverse/PSPTool/blob/6112e48dc24d77fbeb2aa646d4a9ed3403fdd601/psptool/header_file.py), this describes a 256-byte header, 256-KiB body, and 256-byte signature trailer. This is a reverse-engineered format interpretation, not observation of loader execution.

Independent arithmetic and hashing confirm that SHA-256 of the first `0x40000` analysis bytes equals the 32 bytes at header offset `0xd0`. The full analysis-file hash does not equal that field. Both saved captures give identical structural results. The body hash is `5c805026581ace101ba43ef4d0f6b34354f4a61461a1c78d2fa6a335a53d9936`.

| Region | ROM start | ROM end, exclusive | Analysis offsets |
|---|---|---|---|
| Header | `0x8ff000` | `0x8ff100` | outside file |
| Body | `0x8ff100` | `0x93f100` | `[0, 0x40000)` |
| Signature trailer, parser interpretation | `0x93f100` | `0x93f200` | `[0x40000, 0x40100)` |

PROVEN_STATICALLY: saved header values, range arithmetic, and body checksum equality. STRONGLY_SUPPORTED: trailer classification under the pinned parser. Signature cryptographic verification, actual loader copy range, runtime SRAM identity/modification, and external experiment version identity remain UNPROVEN. The header load-address field is zero; it does not independently prove runtime placement.

The R201–R211 named targets (including `0x1edd4`, `0x1eeb8`, `0x1cb58`, `0x241ac`, and `0xcee1`) fall below `0x40000`; this boundary clarification does not by itself invalidate their interpretations. It does not revalidate all earlier disassembly. Future static xrefs or code findings in `[0x40000,0x40100)` must be excluded from body evidence or justified separately.

Next: distinguish the declared container/body extent from the loader's actual copy/verification path using saved loader evidence. Physical VCN power, de-isolation, PSP acceptance/placement, VCPU, rings, VA-API and video decode remain unproven. The six-condition gate remains unmet; no live operation follows from this result.

Reproduce with [file-only audit](../logs/R213_audit_extent.py), passing analysis-image and saved-ROM paths. [Sanitized output](../logs/R213_STATIC_EVIDENCE.json) contains no board ROM hash or raw contents.
