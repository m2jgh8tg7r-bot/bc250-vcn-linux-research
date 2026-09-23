> **R232 correction — 2026-09-23:** The body0x6080/user VA0x206080 identification is not valid under the R218 user-section mapping. The saved startup explicitly stores0x280000; R228/R232 establish the conditional0x286000 expression. [Evidence](CHATGPT_HANDOFF_R232.md). The original text below is historical.

# R226 — TOS context initialization and candidate t02 runtime base

Date: 2026-09-22. Static saved-image analysis only; no hardware access or mutation.

## Evidence

The analyzed type-2 TOS body SHA-256 is `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d`. At artificial Ghidra base `0x200000`, function `0x211608` (body offset `0x11608`) loads a context pointer whose image-relative value is `0x206068` (body offset `0x6068`). The context field at `+0x18`, body offset `0x6080`, is initialized to `0x16000` in the saved body.

The function then performs setup involving SVC `0x8d`, SVC `0x62` with arguments including `0x208000`/`0x4f000`, SVC `0x73`, repeated SVC `0x5d`, SVC `0x80`, and additional SVC `0x62` calls. It enters a loop polling SVC `0x60`; when the byte at context `+0x8d` is nonzero, it calls the `0xfc50` F2 walker at body offset `0x1174c`. This establishes a local caller relationship for the t02 candidate processing path.

The F2 walker obtains the `+0x18` value by following a context-relative global, then adds `0x6000` and indexes records at stride `0x54`; the field/tag `0x5244` is at each record+8. From saved initialization bytes, the *candidate offset* is therefore `0x16000 + 0x6000 = 0x1c000` before any runtime load/mapping bias. A bias of `0x26a000` would yield `0x286000`, the address claimed for the t02 table by the community guide. This arithmetic is a hypothesis only: no evidence yet establishes that load bias, and the saved type-2 container header does not supply a directly identified load address in the inspected fields.

The other function named by the external report, body offset `0x115b6`, is not the direct caller of `0xfc50` in this saved image. Its own path returns `0x0d` on one branch or uses SVC `0x5c` and `0x5a` on another. Local xrefs show `0xfc50` called from `0x1174c`.

## Assessment

R224/R225's structural match is strengthened: the saved body has a context-driven caller that invokes the `0x5244`/SVC-F2 walker after TOS memory/service initialization. It does not prove that this local image has the same runtime load bias or table address as the external t02 artifact. The reported 31 live entries versus 32 loop slots remains unresolved; no live memory table was captured.

## Next static target

Identify the PSP loader's destination/load-bias for this exact type-2 container or an equivalent version-matched TOS image. Separately trace the context field at body `0x6080` through SVC mapping setup and determine whether it is modified before the loop. Until then, do not label `0x286000` as locally confirmed.

## Reproduction

Decompilation and instruction exports: `r226-context-pointer/context-functions.txt`, `context-instructions.txt`, and `analyze.sh`. The script is pinned by executable SHA-256 in `BC250TosFunctions.java` and was run against the saved R217 Ghidra program. Primary container/body identity is recorded in `r217-tos-load-response/image-identity.json`.
