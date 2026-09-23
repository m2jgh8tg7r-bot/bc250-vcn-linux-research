# R195–R197: live capability query and next firmware comparison

## R195 — measured normal-driver API state

On the tested BC-250 (PCI 1002:13fe), normal kernel 7.2.1-ogc4.1.fc44.x86_64, seven standard DRM_IOCTL_AMDGPU_INFO queries produced:

| Query | Observed result |
|---|---|
| ACCEL_WORKING | return 0, value 1 |
| GFX HW_IP_INFO | return 0, available_rings=1 |
| VCN decode / encode / JPEG HW_IP_INFO | return 0, available_rings=0, version fields=0 |
| VIDEO_CAPS decode / encode | return -1, errno=22 (EINVAL) for both |

**PROVEN_LIVE** applies to these API observations. Boot/module identity remained consistent across collection, with no intervening kernel-journal additions. Existing service-failure count and network connection state were unchanged. No ring job, video decode, firmware change, or register write was performed.

A successful HW_IP_INFO return alone does not establish an available ring. VIDEO_CAPS EINVAL does not distinguish the internal instance/harvest guard from the unsupported-version branch. This does not establish physical failure, PSP rejection cause, or every alternate userspace driver's behavior. R193's source evidence and this live observation remain distinct.

## R196 — external research integration

The five previously tracked public repositories were checked again, using saved HEAD/README/issues snapshots with retrieval timestamps and hashes. This was an independent public-source check; the separate ChatGPT monitoring notifications were not accessed.

The compute-encoder project merged [32-bit client support in PR9](https://github.com/simpmix/bc250-encoding-decoding-fix/pull/9). Its [fixed README](https://github.com/simpmix/bc250-encoding-decoding-fix/blob/eabbcb9cfc2bd9a6f0ef044df007ef3c3a87b6da/README.md) documents client/driver architecture matching and shared OpenMP library requirements. This is useful for a future isolated compute-encoder evaluation, not evidence of VCN execution. It was not installed or tested here.

The reviewed updates did not supply a matching standard-PSP acceptance profile. Claims under altered PSP conditions were not adopted as a standard-loader control; no bypass implementation was reproduced.

## R197 — prepared, not installed or booted

A single official predecessor, Navi10 VCN version 0x08118009, was selected for a **limited response comparison**, not because Cyan compatibility has been established. The question is whether that version changes the observed PSP response compared with 0x0811800d. No historical-version sweep is planned.

- Candidate official-file SHA256: `ac5f2182b0ddee7a2886bf1239a47b4027becd0c37a1b0b6cac1f335393302c9`.
- Candidate payload: 404288 bytes; original binary/header unchanged.
- All 5077 cpio records were compared. Only `usr/lib/firmware/amdgpu/vcn_2_0_3.bin` differs; the existing signed R180 module and all other member bytes/metadata remain identical.
- Existing VCN/JPEG execution guards remain in place. Firmware request transport and other firmware are unchanged.

The fixed observer compares host payload bytes only for the original 405696-byte size. The candidate is therefore expected to report `payload_checked=0` and `payload_equal=0`: **unchecked**, not unequal. The separate response-only parser does not claim candidate host-payload equality. Original parsers and evidence were preserved.

The parser checks version/size, full request ordering, matching response fields, completed fences, timeout, software guards, and non-VCN controls. Acceptance requires zero status and nonzero placement as well as completion. Eight test methods, including malformed-request subcases and synthetic acceptance/zero-placement cases, passed; six temporary-directory archive/recovery cases passed. Synthetic logs are not live evidence.

Privileged installed-image and boot-policy verification remains necessary. Candidate installation and manual boot have not occurred. Normal/recovery entries and R180 are retained in the prepared procedure. After a candidate boot, collect paired responses, verify controls, and return to the normal entry. Even a successful acceptance response would not prove VCN execution or diagnose signature/policy causes.
