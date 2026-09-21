# Current status

## Latest research — 2026-09-21

[R207: metrics record contract audit](CHATGPT_HANDOFF_R207.md) verifies the saved HEX and identifies conditional overlap between expanded average fields and unchanged timestamp/count storage, plus a 244-byte reset versus 284-byte export. This is a static combination audit, not evidence that the external machine ran that exact combination. Saved R125A also records 1111 as a normal policy target; the value alone does not establish a halt sentinel.

[R206: saved metrics producer trace](CHATGPT_HANDOFF_R206.md) confirms that the saved metrics-format patch moves the DCLK store from internal offset 76 to 96, supporting R205's layout-mismatch explanation. The original producer reads calculated clock-slot values; average and current fields are not independent physical-liveness observations. External patch/driver identity remains unproven. No hardware access or patch application occurred.

[R205: metrics layout mismatch qualification](CHATGPT_HANDOFF_R205.md) adds a conditional CPU model: an 8-core PMFW record decoded by a 6-core driver can place DCLK-derived data into the power field at offset 44 without changing the Linux ABI. Thus R204's field-name finding alone cannot disprove the external value's DCLK origin. The actual external producer/decoder pairing and physical clock state remain unproven.

[R204: saved metrics ABI audit](CHATGPT_HANDOFF_R204.md) finds that byte offset 44 is `average_soc_power`, not DCLK, in the verified local v2.2 format. The saved native R72 sample has 1111 there; external format/decoder provenance remains unresolved. [R203](CHATGPT_HANDOFF_R203.md) separates Domain6 power bookkeeping from physical state and reconstructs the cached-slot power policy. [R202](CHATGPT_HANDOFF_R202.md) connects feature lifecycle with callback registration. All work used saved files; no new hardware access.

[R201 static reconstruction and handoff](CHATGPT_HANDOFF_R201.md) preserves the initial candidate reconstruction. The fixed Robin1 image calls `0x1DB54(11)` and branches to `0x1EEB4`, correcting the external `0x1CB58`/`0x1EEB8` account for this image. The `0xCEE1` flag and descriptor 3/4 operations strongly support a GDDR6 clock SSC interpretation. This candidate is not established as a VCN power/isolation path.

Historical live baseline: R197 and R199 failed to meet VCN PSP acceptance conditions (`0xffff0008`, zero placement), followed by normal recovery. R197 is not an unbooted pending experiment. There was no new hardware access in R201.

Current policy: saved-image static/read-only analysis. No R197 reboot, firmware/initramfs/boot modification, unknown SMU/PSP/SVC calls, register writes, new broad BAR scans, or ring/VCPU execution. A future live proposal must establish six conditions: version-matched VCN relevance, prerequisites, exact target, discriminating observation, recovery, and more information value than R197.

The platform and earlier milestones below remain historical evidence.

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

R202–R204 add feature/callback lifecycle, conditional power-helper execution, automatic cached-slot policy, and a saved Linux metrics ABI audit. Next, seek existing external decoder/header provenance and continue version-matched static analysis. A function return, cached power flag, or clock field does not establish whole-block power, firmware placement, or execution.

## Remaining major milestones

These historical milestone categories describe unresolved work, not authorized live actions:

1. stock recovery / post-R113 closure and static comparison,
2. minimal VCN power/liveness probe design and audit,
3. physical power/liveness proof,
4. firmware/VCPU execution proof,
5. ring execution followed by normal VA-API / FFmpeg validation.
