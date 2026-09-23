# R220 — External research audit changes the priority

STAGE=R220
RESULT=EXTERNAL_EVIDENCE_RECLASSIFIED
STATIC_OR_LIVE=EXTERNAL_REPORT_AUDIT
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=The external reports separate SMU-side power progress from the unresolved PSP/root clamp
REJECTED=Using `0xffff0008` alone to classify the VCN silicon as absent or dead
UNPROVEN=Independent reproduction, exact saved TOS correspondence, PSP gate bypass, VCN VCPU/ring execution
NEXT=Static comparison of fw_type-13/AUTOLOAD data and saved PSP type-2; prepare a discriminating read-only validation only if prerequisites are met

## New external evidence

The community guide updated through 14 September 2026 reports that VCN 2.0.3 is present in IP discovery and not harvested, while SMU-side clock/power sequencing and cold-reset toggling still leave the VCN MMIO clamped at `0xffffffff`. It reports that direct firmware loading can reach VCN initialization but historically hangs when the decoder ring is exercised. These are external reports, not this project's live evidence.

The same guide reports a newer hypothesis: the PSP AUTOLOAD path, rather than the ordinary `LOAD_IP_FW` path, registers operations from a `t02` firmware table; an op-id-8 path associated with `t28` is proposed to release the VCN clamp and write SMN `0x0900c004`. It also reports that BC-250 rejects fw_type 13 with an item-not-found result, so the release write is skipped. A proposed two-byte PSP gate patch was reported as unsuccessful by another tester. These claims require primary-artifact comparison before adoption.

The `daveconde/bc250-vcn-enable` repository documents a BIOS-3 / PMFW `0.58.6.0` SMU thunk path, a read-only `--verify` mode, a VCN power-register diagnostic, and a direct-load ring test. Its own safety notes describe cold-power-cycle-only wedge cases. We do not run these paths here.

## Effect on this research

R218's TOS service-1 route remains valid as a static transport finding, but it is no longer the highest-value next target. The external reports point to an earlier gate: PSP AUTOLOAD registration and root isolation release. The historical `0xffff0008` response is therefore consistent with a missing/disabled PSP firmware entry, but it does not prove that interpretation. The saved type-2 TOS body still has unproven runtime identity and must be compared with the reported t02/t28 artifacts.

## Sources

- [BC-250 unofficial community guide, BIOS and firmware](https://github.com/katzzero/bc250-unofficial-community-guide/blob/main/02-bios-and-firmware.md), especially the 24 August–14 September 2026 progress entries.
- [daveconde/bc250-vcn-enable](https://github.com/daveconde/bc250-vcn-enable), including the BIOS-3 target, read-only diagnostics, direct-load ring-test description, and safety constraints.
- [Phoronix report on BC-250 PSP Linux patches](https://www.phoronix.com/news/AMD-BC-250-Linux-PSP-Support), 21 September 2026. This confirms current upstream attention to PSP/CCP enablement, but does not claim VCN execution.

## Limits

No external claim is classified as `PROVEN_LIVE` for this board by this project. No firmware was changed, no SMU thunk was fired, no PSP gate was patched, and no direct-load ring test was run.
