# Hardware findings

This document contains findings that were observed on physical AMD BC-250 / Cyan Skillfish hardware or that directly constrain interpretation of physical-hardware tests.

## 1. VCN block presence and firmware candidate

The tested BC-250 exposes a VCN 2.x IP block through amdgpu. The firmware candidate used throughout the controlled bring-up work is:

- file: `vcn_2_0_3.bin`
- SHA-256: `a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5`
- size: 405952 bytes
- firmware-reported VCN fields: ENC 1.24, DEC 8, VEP 0, revision 13

Firmware acquisition or software registration does not prove firmware execution.

## 2. VCN software lifecycle

A quarantined custom amdgpu build reached the real VCN lifecycle:

- `early_init`
- `sw_init`
- `sw_fini`

Software ring objects were registered for:

- `vcn_dec`
- `vcn_enc0`
- `vcn_enc1`

Hardware ring execution remained deliberately blocked. Therefore:

```text
RING_SOFTWARE_REGISTRATION != RING_HARDWARE_EXECUTION
```

## 3. PSP enrollment quarantine

Cyan Skillfish automatic VCN PSP firmware enrollment was deliberately suppressed in the controlled test build. This allowed software initialization and later NBIO experiments to be separated from PSP-mediated VCN firmware execution.

```text
PSP_FIRMWARE_ENROLLMENT != VCN_VCPU_EXECUTION
```

## 4. Stock Cyan power-route result

Static tracing of the stock Cyan VCN power route showed that a generic power-state request can return success without proving a hardware transition of the whole VCN block.

Observed classification:

```text
STOCK_CYAN_VCN_POWER_ROUTE_EXPOSED=NO
STOCK_CYAN_VCN_POWER_REQUEST_RESULT=SUCCESS_NOOP
SOFTWARE_PWR_STATE_ON_EQUALS_HARDWARE_POWER_PROOF=NO
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
```

## 5. NBIO VCN doorbell-range register

The stock NBIO v2.3 route for the VCN MMSCH0 doorbell range was traced to:

- logical register: `BIF_MMSCH0_DOORBELL_RANGE`
- logical dword register offset: `0x00000ef3`
- logical byte register offset: `0x00003bcc`

`0x3bcc` is a logical byte offset in the register-access model, not an absolute physical BAR address.

For the stock-equivalent configuration studied here:

- OFFSET field: `0x310`
- SIZE field: `8`
- encoded target value: `0x00080c40`
- mutable mask: `0x001f0ffc`
- preserved mask: `0xffe0f003`

## 6. First live NBIO read

A bounded kernel-controlled live read of logical register `0x00000ef3` returned:

```text
0x00000000
```

The read completed without a hang. No NBIO write, VCN-core MMIO access, raw SMU command, VCPU execution, or ring execution was performed.

This proves the read path worked at that observation point. It does not prove VCN power state.

## 7. Bounded live NBIO write/read/restore

A later safety-hardened experiment performed exactly one bounded target write on a fresh value of zero.

Verified physical-hardware sequence:

```text
fresh old       = 0x00000000
target write     = 0x00080c40
target readback  = 0x00080c40
restore           = 0x00000000
restore readback  = 0x00000000
```

The target readback matched exactly, and the original value was restored exactly. Emergency restore was not needed.

This is the strongest hardware result in the project so far. It proves that this bounded NBIO register path is live and writable/readable on the tested BC-250.

It does **not** prove any of the following:

```text
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
VCN_VCPU_EXECUTION=UNPROVEN
VCN_RING_HARDWARE_EXECUTION=UNPROVEN
VAAPI_HARDWARE_DECODE=UNPROVEN
VAAPI_HARDWARE_ENCODE=UNPROVEN
```

## 8. Ring-test errors under quarantine

The custom build later reports `-95` / `-EOPNOTSUPP` for VCN IB tests. These results come from deliberate quarantine guards and must not be represented as evidence that VCN hardware execution failed.

## 9. Current tested platform context

- hardware: AMD BC-250 / Cyan Skillfish
- BIOS: P3.00
- PMFW observed by amdgpu: `0x00580600` (0.58.6.0)
- kernel: `7.2.1-ogc4.1.fc44.x86_64`

These details are useful for comparison with other BC-250 research, but reported behavior on other boards or firmware versions remains external until reproduced here.
