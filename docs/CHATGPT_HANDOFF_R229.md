> **R232 correction — 2026-09-23:** Use one dereference at user VA0x206080 for the context base; do not equate it with body0x6080. SVC64 allocation1..31 for loader classes is already in R218 and reverified in R232. [Evidence](CHATGPT_HANDOFF_R232.md). The original text below is historical.

# R229 — TOS image loader populates the same 0x5244 table

Date: 2026-09-22. Static saved-image analysis only; no hardware access or mutation.

## Finding

R218's previously exported image-loader function provides the writer-side half of the R228 table address match. In the saved type-2 TOS body (SHA-256 `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d`), `FUN_00211a04` at body offset `0x11a04` accepts container/item tags `0x4154` and `0x5244`. For a `0x5244` item it parses metadata, obtains a slot index, clears a `0x54`-byte row, writes the tag at row+8, sets a marker byte at row+0x1e, writes metadata words at row+0x20..0x2c, copies 0x20 bytes to row+0x32, and calls SVC `0x67`.

The writer forms its row at `*(*(u32 *)0x206080) + slot*0x54 + 0x6000`. The pointer field at body offset `0x6080` is the same context `+0x18` field overwritten with `0x280000` during startup (R228). Thus the writer's table base is `0x286000` in that initialized code path. R228's F2 walker reads the same `0x54` stride and checks tag `0x5244` at row+8 before invoking SVC F2.

This gives a paired static result: the saved image loader constructs `0x5244` rows at the computed base, and the saved startup walker later scans records of the same stride/tag and dispatches their row fields through SVC F2. It strongly corroborates the external guide's `t02` table interpretation and address. It still does not prove that this branch executed on the BC-250 or that external t28/clamp-release claims are correct.

## Capacity and remaining boundaries

The walker iterates 32 indices (31 down through 0) and filters by the row tag. The loader uses a slot-selection helper; the exact helper bound and runtime occupancy have not yet been exported here. The external guide's 31-entry description could be 31 populated rows among 32 available slots, but that remains a hypothesis until the slot selector or a version-matched table dump confirms it.

Unproven: exact runtime image identity; live table contents; loader/walker execution; slot occupancy; `t28` registration and clamp release; PSP VCN firmware acceptance; VCN VCPU/ring execution.

## Next static step

Recover the slot-selection helper used by `FUN_00211a04`, verify its search bound and empty-row predicate, and trace the row fields passed by the F2 walker. Compare against a version-matched external `t02` binary if available.

## Reproduction

Writer-side export: `r218-service-image-provenance/image-loader.txt` (source pointer references around Ghidra addresses `0x211b28`–`0x211c00`, artificial base `0x200000`). Reader-side export: `r217-tos-load-response/t02-candidate-functions.txt` and `t02-candidate-instructions.txt`. Startup overwrite and caller: `r226-context-pointer/context-instructions.txt`.