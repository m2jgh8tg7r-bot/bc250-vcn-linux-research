# Current status

## Platform

- AMD BC-250 / Cyan Skillfish
- Linux kernel source baseline: OGC `v7.2.1-ogc4`
- Source commit: `14c028f83498b2900fecd0940a058a3ac0622afe`
- Tested running kernel: `7.2.1-ogc4.1.fc44.x86_64`
- Tested board firmware: BIOS P3.00
- Observed SMU firmware: `0x00580600` (88.6.0)

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
fresh old       = 0x00000000
target write    = 0x00080c40
target readback = 0x00080c40
restore write   = 0x00000000
restore readback= 0x00000000
```

No retry loop was used. Emergency restore was not needed.

This proves the NBIO register transaction path is live and that the original value was restored. It does not prove VCN whole-block power or any VCN execution state.

## Still unproven

```text
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
VCN_VCPU_EXECUTION=UNPROVEN
VCN_RING_HARDWARE_EXECUTION=UNPROVEN
VAAPI_HARDWARE_DECODE=UNPROVEN
VAAPI_HARDWARE_ENCODE=UNPROVEN
```

## Next research direction

The next useful boundary is VCN power/liveness rather than broader register experimentation. External BC-250 work on SMU domain-6 and direct VCN bring-up is being treated as static comparison material before any live adoption.
