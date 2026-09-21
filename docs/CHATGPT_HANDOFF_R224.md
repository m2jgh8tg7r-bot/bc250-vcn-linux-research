# R224 — saved type-2 TOS confirms the t02 SVC-F2 path

Date: 2026-09-22  
Result: static corroboration against the locally saved BIOS TOS body. No hardware access or mutation.

## Finding

The external report's two `t02` candidate addresses correspond to code in the locally extracted PSP type-2 Trusted OS body when interpreted as body offsets: `0x115b6` and `0xfc50`. The analysis project uses artificial base `0x200000`, so the Ghidra addresses are `0x2115b6` and `0x20fc50`; subtracting the base gives the body offsets. The analyzed body SHA-256 is `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d`, matching the saved type-2 image recorded in R218/R219.

At body offset `0xfc50`, static disassembly shows a loop over 32 entries, tests the tag `0x5244`, and invokes SVC `0xf2` for matching records (with a separate branch when a record field equals 3). The loop includes status-dependent iteration. This corroborates that SVC F2 participates in processing a TOS-internal table in this saved body. It does not establish what SVC F2 means outside this body or prove the table is the external report's `0x286000` runtime table.

At body offset `0x115b6`, the routine checks a byte argument. A nonzero value returns `0x0d`; otherwise it copies fields into locations reached through globals, sets a byte flag, and executes SVC `0x5c` followed by SVC `0x5a`. This routine is distinct from the F2 loop. The constant 13 here is not evidence that the routine loads VCN firmware.

## Interpretation correction

R222/R223 investigated a saved BIOS PSP directory entry whose numeric entry type is `0x13`; its 0x1e00-byte body has SHA-256 `413fcd1f3e87a7afc3c6ce28f4be550d79d04d182d3fd376e9726382de876654` and contains debug-unlock strings. That is a directory-entry namespace and is not the Linux PSP command's `fw_type` namespace.

In the saved Linux source snapshot `bc250-vcn-r40-worktree` at commit `0bb924b042ab85b8f529aed6e4f3e24750584276`, `psp_gfx_if.h` defines `GFX_FW_TYPE_VCN = 13` for `GFX_CMD_ID_LOAD_IP_FW`; `amdgpu_psp.c` maps `AMDGPU_UCODE_ID_VCN` to `GFX_FW_TYPE_VCN`. Thus the external command argument `fw_type 13` does mean VCN in that Linux/PSP-command context. Equal numeric values do not identify the BIOS directory entry with the VCN command type. This resolves the ambiguity left open in R223 and retains R223's rejection of numeric equality as identity proof.

## Limits and next work

- The TOS body is a saved image; executing identity and runtime addresses are not observed.
- The static code supports an SVC-F2 table-processing path in this image, but does not map that table to address `0x286000` without a proven runtime base or relocation map.
- SVC semantics, service payload identity, AUTOLOAD `t28`, firmware registration outcome, VCN firmware transfer, and VCN execution remain unproven.
- No live readiness or hardware trial is claimed. Continue static work by resolving the TOS data/global base and relating table records to saved PSP directory/container metadata.

## Reproduction artifacts

Local disassembly/decompilation artifacts: `r217-tos-load-response/t02-candidate-functions.txt` and `r217-tos-load-response/t02-candidate-instructions.txt`. The analysis project uses base `0x200000`; the executable body hash is embedded in the function export. Primary Linux source locations: `bc250-vcn-r40-worktree/drivers/gpu/drm/amd/amdgpu/psp_gfx_if.h` and `amdgpu_psp.c`.
