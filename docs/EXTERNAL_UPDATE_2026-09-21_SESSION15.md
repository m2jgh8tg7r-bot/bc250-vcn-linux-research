# External VCN research delta — 2026-09-21 Session 15

Status: external research input only. Do not adopt external interpretations as local proof.

## New primary-source result

Shalasere/bc250-vcn-research commit edb222c65477b6ebc63834ef3562855009179539 (2026-09-20 20:36 UTC; 2026-09-21 JST) reports Session 15 TOCTOU analysis.

Fresh board measurement reported by that project:
- Full 1 MiB PSP BAR2 scan found only about 15 live regions / roughly 100 bytes total, described as PSP mailbox/status areas.
- The expected CCP region 0x0000-0x6000 read as 0xffffffff throughout.
- This is direct negative evidence against the specific hypothesis that the host can manipulate CCP queues through BAR2 to race a permission-table window.

External static/interpretive conclusion:
- The project classifies six runtime VCN gates as unavailable to runtime software and says the permission-table TOCTOU candidate was closed through CCP MEMTYPE_LOCAL, host-to-PSP-SRAM, and known-CVE avenues.
- Treat this broad "all runtime paths dead" statement as EXTERNAL_REPORTED / interpretation, not as a locally proven universal result.
- The commit is co-authored with Claude Opus 4.6, so retain code/measurement evidence separately from generated interpretation.

Source:
https://github.com/Shalasere/bc250-vcn-research/commit/edb222c65477b6ebc63834ef3562855009179539

## Relationship to current local research

Do not regress to R153/R197 assumptions blindly. First inspect the newest local handoff/stage before using this note.

This result does NOT falsify the local SMU/PMFW investigation around:
- corrected external candidate 0x1EDD4
- status-check call 0x1cb58(arg=11)
- SRAM gate byte 0xCEE1
- shared early exit 0x1eeb8
- candidate callee 0x241AC with arguments 3/4

It instead reduces the priority of searching for a host-runtime PSP/CCP TOCTOU shortcut.

Keep proof boundaries separate:
1. outer whole-block power
2. VCN de-isolation / register-file accessibility
3. firmware acceptance/placement
4. VCN VCPU execution
5. hardware ring execution
6. VA-API / FFmpeg hardware decode/encode

## Safe Codex application

1. Read the latest local handoff before analysis; preserve any work newer than R197.
2. Fetch/diff Shalasere edb222c only as external evidence. Do not import its global conclusion as ground truth.
3. Compare the reported BAR2 map with any existing local PSP BAR/window documentation. Prefer static or read-only evidence.
4. Record whether local evidence independently supports or contradicts the claim that CCP 0x0000-0x6000 is host-invisible on this platform.
5. Continue independent static reconstruction of the Robin1/SMU path around 0x1EDD4, 0x1cb58(arg=11), 0xCEE1, 0x1eeb8 and 0x241AC. Determine actual callees/register effects before assigning semantic names such as PowerUpVcn or power_gate_tile.
6. Trace writers/readers of 0xCEE1 and the predicate implemented by 0x1cb58(arg=11), and compare them with the already-established Domain6 policy/callback machinery.
7. Do not perform unknown register writes, unknown SVC calls, firmware bypasses, APCB flashing, fault injection, or speculative live SMU calls as a consequence of this external report.
8. Classify any result as PROVEN_LOCAL, PROVEN_STATIC, EXTERNAL_VERIFIED, EXTERNAL_REPORTED, WEAKENED, DISPROVED, or UNRESOLVED.

## Confirm / falsify value

Supports current direction if static analysis connects the 0x1EDD4 preconditions to a legitimate Cyan power/de-isolation policy while the host PSP shortcut remains inaccessible.

Weakens current direction if 0x1EDD4/0x241AC proves unrelated to VCN or if its predicates cannot affect VCN power/reset/register accessibility.

A local read-only contradiction to the external BAR2 result should reopen only that specific TOCTOU premise, not automatically the broader PSP path.
