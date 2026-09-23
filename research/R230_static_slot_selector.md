> **R232 correction — 2026-09-23:** SVC64 implementation was already saved and explained in R218. Its first-fit allocation1..31 for loader classes is reverified in R232; live occupancy remains unproven. [Evidence](../docs/CHATGPT_HANDOFF_R232.md). The original text below is historical.

# R230 — duplicate match and PSP slot assignment are separate paths

Date: 2026-09-22. Static saved-image analysis only; no hardware access or mutation.

## Finding

The apparent `0xff` out-of-range write was caused by reading the decompiler's control flow without the intervening service call. In `FUN_00211a04` (Ghidra `0x211a04`, body offset `0x11a04`), `FUN_0020fe08` first searches 32 rows for an existing `0x5244` item whose key bytes match the candidate's first 16 bytes against row+`0x20`. It skips a row when its first dword is zero and returns `0xff` after 32 misses.

On a duplicate, caller stores the matching index to its output byte and exits that path. On a miss, caller reaches SVC `0x64` at `0x211cc0`, passing `r0=r10` (the parsed item class/type in this path) and `r1=sp+0x60` (the slot-index output byte). If SVC `0x64` returns nonzero, caller exits with an error. If it returns zero, the caller reloads the output byte at `0x211cc6` and uses it to clear/write the row at base + index*`0x54` + `0x6000`. Therefore `0xff` is only the pre-call duplicate-search result; the miss path obtains a new index through SVC `0x64` before writing.

The successful writer then stores the item tag at row+8, marker `0xff` at row+`0x1e`, four metadata words at row+`0x20..0x2c`, 0x20 payload bytes at row+`0x32`, and invokes SVC `0x67`. It writes a payload base/size at row+0/4 and performs further mapping/loading. The saved code does not reveal SVC `0x64`'s implementation, its exact allocation policy, whether the output is always 0..31, or whether SVC `0x67` commits the record.

R228's F2 walker scans indices 31 down to 0, checks the same row tag `0x5244` at row+8, and reads row+`0x18` as a selector/command field. When that field equals 3 it takes a separate branch; otherwise it passes that value to SVC F2. This is evidence that the row+`0x18` field controls dispatch behavior, not evidence that a particular live slot executes.

## Interpretation and limits

R229's puzzle is resolved at the static control-flow level: duplicate detection and free/new slot assignment are distinct operations. The code establishes a 32-entry search domain and delegates new-slot selection to SVC `0x64`; it does not establish 31 populated rows, the allocator's exact range, runtime occupancy, or t28/clamp-release behavior. Preserve R228/R229's address result (`0x286000` under the observed startup setup) with the same limitation: this is computed by saved code, not a live memory capture.

## Reproduction

- `slot-functions.txt`: decompilation and call reference for `FUN_0020fe08`.
- `slot-instructions.txt`: disassembly for selector and helper.
- `r218-service-image-provenance/instructions.txt`: caller around `0x211be4` (duplicate search), `0x211cbc..0x211ce0` (SVC64 output and row clear), `0x211d02..0x211d5e` (row fields and SVC67), and F2 walker around `0x20fc9a..0x20fcd0`.
- All Ghidra addresses use artificial base `0x200000`; saved body SHA-256 is `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d`.

## Next

Recover SVC `0x64` semantics from other saved PSP/TOS code or a version-matched primary implementation; then map the row+`0x18` values to F2 branches and the associated metadata/payload interpretation. Do not infer live population or successful VCN execution from this static path.
