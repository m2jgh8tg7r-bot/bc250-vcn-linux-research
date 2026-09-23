> **R232 correction — 2026-09-23:** The separate 12-byte SVC74 writer interpretation is corrected: the preceding factor7 makes the stride0x54. Runtime occupancy remains unproven. [Evidence](CHATGPT_HANDOFF_R232.md). The original text below is historical.

# R225 — t02 table shape: saved-image audit of the external claim

Date: 2026-09-22. Scope: static comparison only; no hardware access or mutation.

## Result

The community guide reports a `t02` firmware table at runtime address `0x286000`, magic `0x5244`, 31 entries, with an AUTOLOAD registration chain. These remain third-party claims, not local runtime observations: https://github.com/katzzero/bc250-unofficial-community-guide/blob/main/02-bios-and-firmware.md (updated September 2026).

The saved type-2 TOS body (SHA-256 `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d`) independently contains a loop at body offset `0xfc50` which walks indices 31 down to 0 (32 possible slots), tests a `0x5244` tag at slot+8, and invokes SVC F2 for matching records except a field-3 branch that has a separate SVC F2 path. This is a strong static match for the *record family and processing pattern*. It does not confirm a runtime address of `0x286000`.

A distinct code path around body offset `0x121de` uses a 12-byte stride from a context-derived base plus `0x6000`, writes at record+`0x18`, and then calls SVC 74. The candidate TOS loop instead uses a 0x54-byte stride from a context-derived base plus `0x6000`. The initialized 32-bit value at body offset `0x6080` is `0x16000`, but it may be runtime-mutated or interpreted through a TOS mapping. Raw file bytes at body `0x6000..0x607f` are mostly zero; this is not a captured runtime table. The different strides and unknown context lifecycle prevent treating the two code paths as a single table or claiming that the raw on-disk region encodes 31 entries.

The external function naming sequence `FUN_000115b6→FUN_0000fc50` should also be read as an analysis narrative, not necessarily a direct call: local xrefs show the `0xfc50` function is called from body offset `0x1174c`, whereas the `0x115b6` helper itself performs SVC `0x5c`/`0x5a` on one branch and returns `0x0d` on another.

## Interpretation

R224 confirms the external `t02` candidate body offsets exist and that `0xfc50` processes `0x5244` records using SVC F2. R225 narrows the structural match and identifies the remaining gaps: 32 slots scanned versus 31 reported entries; unknown runtime base/relocation; distinct observed record strides; and non-direct relation between the two named functions.

The Linux PSP command mapping remains separately established: `AMDGPU_UCODE_ID_VCN` maps to `GFX_FW_TYPE_VCN = 13`. This command argument namespace is distinct from the saved BIOS directory-entry type `0x13` (R224).

## Next static step

Trace all reads/writes and SVC context updates affecting the pointer stored at body offset `0x6080` / context `0x206080`, especially initialization around body offsets `0x1174c`, `0x121de`, and `0x12600`. Determine whether the `0x6000` area is dynamic memory relocated by SVC, and whether the two record layouts refer to alternate phases/contexts. Until then, keep runtime address, entry count, and AUTOLOAD registration linkage unproven.
