> **2026-09-22 R215:** Resource claims and grants are distinct; saved interrupt state is restored before return or scheduler transfer. A bounded instruction model passes 4096 cases. R216 is tracing outer dispatch. [Evidence and limits](CHATGPT_HANDOFF_R215.md).

> **2026-09-22 R214:** Directory/body checksums verify that the second same-version SMU entry is zero-filled except version words and a marker. Cyan Linux callbacks do not establish the BIOS load range. [Evidence and live-test readiness](CHATGPT_HANDOFF_R214.md).

> **2026-09-22 R213:** Saved SMU header and checksum delimit a 256-KiB body plus a retained 256-byte signature trailer. Actual loader/runtime extent remains unproven. [Evidence and limits](CHATGPT_HANDOFF_R213.md).

# Current status

## Latest research — 2026-09-21

[R212](CHATGPT_HANDOFF_R212.md) verifies full analysis-window byte identity in saved P3 BIOS captures and stored Robin1/Robin3 distributions. This establishes saved-image provenance, not loader extent or running SRAM identity.

[R211](CHATGPT_HANDOFF_R211.md) connects the SSC candidate to saved state-transition callbacks. [R210](CHATGPT_HANDOFF_R210.md) separates external BAR scan evidence from broader claims. [R209](CHATGPT_HANDOFF_R209.md) shows existing Domain6 status already satisfies the helper's request1 predicates. Earlier [metrics/observation findings](CHATGPT_HANDOFF_R208.md) remain qualified; none establishes physical VCN power or execution.

Historical live baseline: R197 and R199 returned VCN PSP response `0xffff0008` with zero placement, followed by normal recovery. R197 is not an unbooted pending experiment. R201–R212 performed no new hardware access.

Current policy: saved-image static/read-only analysis. No R197 reboot, firmware/initramfs/boot modification, unknown SMU/PSP/SVC calls, register writes, new broad BAR scans, or ring/VCPU execution. A future live proposal requires all six conditions: version-matched VCN relevance, prerequisites, exact target, discriminating observation, recovery, and more information value than R197.

Earlier platform details below are historical evidence.

## Platform

- AMD BC-250 / Cyan Skillfish
- Linux kernel source baseline: OGC `v7.2.1-ogc4`
- Source commit: `14c028f83498b2900fecd0940a058a3ac0622afe`
- Tested running kernel: `7.2.1-ogc4.1.fc44.x86_64`
- Tested board firmware: BIOS P3.00
- Observed SMU firmware: `0x00580600` (88.6.0 / 0.58.6.0)

## Confirmed software-side milestones

- VCN 2.x IP is enumerated on Cyan Skillfish.
- Candidate VCN 2.0.3 firmware is accepted by the driver and reports ENC 1.24 / DEC 8 / VEP 0 / revision 13.
- Quarantined custom amdgpu reached real VCN `early_init`, `sw_init`, and `sw_fini`.
- `vcn_dec`, `vcn_enc0`, and `vcn_enc1` software rings are registered.
- Cyan automatic PSP VCN firmware enrollment can be suppressed for controlled tests.
- Hardware IB callbacks remain intentionally guarded; `-95` from those guards is not evidence of a hardware execution failure.

## Confirmed stock power-route result

The stock Cyan path can report a successful VCN power request without exposing a concrete hardware route that proves the whole VCN block changed power state.

Therefore:

```text
STOCK_CYAN_VCN_POWER_REQUEST_RESULT=SUCCESS_NOOP
SOFTWARE_PWR_STATE_ON_EQUALS_HARDWARE_POWER_PROOF=NO
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
```

## Confirmed NBIO doorbell path

The stock-equivalent VCN NBIO doorbell-range register was identified as:

```text
logical dword register: 0x00000ef3
logical byte offset:    0x00003bcc
target value:           0x00080c40
OFFSET field:           0x310
SIZE field:             8
mutable mask:           0x001f0ffc
preserved mask:         0xffe0f003
```

The `0x3bcc` value is a register-file byte offset, not an absolute BAR physical address.

## Live hardware results

### Single read

A prior bounded live read of register `0x00000ef3` returned `0x00000000` without a hang.

### Bounded write/read/restore

A later hardened live transaction completed exactly:

```text
fresh old        = 0x00000000
target write     = 0x00080c40
target readback  = 0x00080c40
restore write    = 0x00000000
restore readback = 0x00000000
```

No retry loop was used. Emergency restore was not needed.

This proves the NBIO register transaction path is live and that the original value was restored. It does not prove VCN whole-block power or any VCN execution state.

### Post-live quarantine

After the successful live experiment, the dedicated R113 manual-only BLS entry was removed. The boot environment was left with no automatic experimental selection. No additional NBIO, VCN-core, SMU/PSP, ring, or VCPU operation occurred during this quarantine step.

## Still unproven

```text
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
VCN_VCPU_EXECUTION=UNPROVEN
VCN_RING_HARDWARE_EXECUTION=UNPROVEN
VAAPI_HARDWARE_DECODE=UNPROVEN
VAAPI_HARDWARE_ENCODE=UNPROVEN
```

## Current stage

R212 verifies saved-image provenance. R201–R211 reconstruct SSC/state callbacks, Domain6 bookkeeping and status predicates, metrics producer/decoder contracts, and external acquisition limits. Continue version-matched static analysis; the live-proposal gate remains unmet.

## Remaining major milestones

These historical milestone categories describe unresolved work, not authorized live actions:

1. stock recovery / post-R113 closure and static comparison,
2. minimal VCN power/liveness probe design and audit,
3. physical power/liveness proof,
4. firmware/VCPU execution proof,
5. ring execution followed by normal VA-API / FFmpeg validation.
