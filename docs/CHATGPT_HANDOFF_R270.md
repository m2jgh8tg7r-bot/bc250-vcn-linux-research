# R270 — Local standard-driver baseline before reproducing external VCN progress

Updated 2026-10-01. This checkpoint adds a new **local live baseline** on the user's BC-250 under the ordinary Bazzite/amdgpu environment. It does not claim VCN hardware execution, firmware acceptance, GPCNT activity, RBC execution, reset release, first fetch, or hardware video.

## New local live evidence

Environment captured in the successful baseline:

- Kernel: `7.2.1-ogc4.1.fc44.x86_64`
- Device: Cyan Skillfish / BC-250, PCI ID `1002:13fe`
- Driver: `amdgpu`
- Render node selected by sysfs vendor/device match: `/dev/dri/renderD128`
- R267 standard DRM query source SHA-256:
  `fcefedae17f358b4b762fc8faa732e1c3461a737bf8cc9c91e11ed45a78ab961`
- Query process completed with exit 0.

The standard DRM information queries returned:

```text
ACCEL_WORKING: ret=0 errno=0 value=1
GFX:          ret=0 errno=0 major=10 minor=0 available_rings=1 ip_discovery_version=655619
VCN_DEC:      ret=0 errno=0 major=0 minor=0 available_rings=0 ip_discovery_version=0
VCN_ENC:      ret=0 errno=0 major=0 minor=0 available_rings=0 ip_discovery_version=0
JPEG:         ret=0 errno=0 major=0 minor=0 available_rings=0 ip_discovery_version=0
VIDEO_CAPS DECODE: ret=-1 errno=22
VIDEO_CAPS ENCODE: ret=-1 errno=22
```

This proves that, in this ordinary-driver boot, the AMDGPU information path is functioning for the device and GFX is exposed, while VCN DEC/ENC/JPEG rings are not exposed through these standard API queries and the video-capability queries return EINVAL.

It does **not** prove that the VCN silicon is absent, physically disabled, unclocked, fused off, or incapable of execution.

## Same-boot kernel log observation

The same ordinary boot identifies Cyan Skillfish and lists detected IP blocks 0 through 7 as:

1. common
2. GMC
3. IH
4. PSP 11.0.8
5. SMU 11.0.0
6. display
7. GFX 10.0
8. SDMA 5.0

No VCN/UVD/JPEG IP block appears in that captured detected-IP-block list. PSP is present as `psp_v11_0_8`.

This is consistent with the standard DRM result above: the normal boot does not expose a VCN/JPEG userspace path. It remains a software-enumeration/exposure observation, not evidence of physical absence.

## Relation to prior local live work

Do not overwrite or weaken the earlier R173/R180/R182 findings.

Historical local experiments already crossed the ordinary exposure boundary by using guarded research driver paths:

- R173 proved a host VCN LOAD_IP_FW request with `ucode_id=57`, `command=6`, `fw_type=13`, `size=405696`, and an equal host payload comparison.
- R180 observed 11 paired LOAD_IP_FW transactions. Ten non-VCN requests returned status zero; VCN ID57/type13 returned `0xffff0008` with placement zero.
- R182 repeated the R180 condition after user-reported physical power removal for several minutes; the VCN response remained `0xffff0008` with placement zero.
- Those runs did not prove PSP-visible payload identity, VCN firmware acceptance, VCPU execution, hardware rings, or hardware video.

The new R270 baseline therefore establishes a clean ordinary-driver comparison point **before** those guarded experimental paths.

## External results remain external

R265–R269 external reports of:

- GPCNT rate following requested 800/1250 MHz settings,
- RBC packet fetch/execute,
- firmware acceptance/staging in another setup,
- domain-master/access changes,
- and VCPU soft-reset release readback,

remain strong attributed external observations, not local reproductions.

R270 does not promote any of them to local evidence.

## Current evidence ladder

```text
LOCAL ordinary amdgpu/GFX path                         PROVEN_LIVE
LOCAL standard VCN DEC/ENC/JPEG exposure               ABSENT_IN_CAPTURED_STANDARD_API
LOCAL standard VIDEO_CAPS                              EINVAL_IN_CAPTURED_STANDARD_API
LOCAL historical guarded VCN PSP request               PROVEN_LIVE (R173/R180)
LOCAL historical VCN PSP acceptance                    NOT MET in those runs
LOCAL GPCNT activity                                   UNPROVEN
LOCAL RBC packet fetch/execute                         UNPROVEN
LOCAL VCPU reset-release equivalent to external report UNPROVEN
LOCAL VCPU first-fetch                                 UNPROVEN
LOCAL VCPU execution/ready                             UNPROVEN
LOCAL hardware ring execution                          UNPROVEN
LOCAL hardware decode/encode                           UNPROVEN
```

## Next Codex objective

The user wants the local machine to reproduce, in order, the important externally reported milestones that have not yet been proven locally.

Work in a discriminating ladder:

1. Preserve this R270 ordinary-driver baseline.
2. Re-establish the reviewed historical guarded PSP boundary only with a version-matched, reviewable path and explicit rollback/recovery.
3. Identify a primary-source, known-working and target-matched acquisition method before attempting GPCNT/SMN/MMIO observation. Do not invent addresses/selectors from names alone.
4. Reproduce GPCNT activity locally with raw counts plus independent timestamps and documented selector/source semantics.
5. Reproduce RBC packet fetch/execute locally with an attributable effect, not register readback alone.
6. Reproduce effective VCPU reset-release evidence locally.
7. Only then move to the R269 first-request/first-fetch boundary, with a validated observer and positive control.

Keep request emission, fetch response, returned bytes, instruction consumption and retirement as separate milestones.

## Safety / stop rules

- No direct harvesting-clear trials.
- No speculative SMN/MMIO reader or selector programming without a known-working target-specific acquisition path.
- A process timeout is not recovery from a stalled bus.
- Do not repeat a hung write.
- Standard API absence is not physical VCN absence.
- Readback is not physical execution.
- Zero fault counts do not prove no fetch request without observer coverage.
- Any new live trial must state the exact variable, A/B interpretation, stop condition, normal-boot rollback and evidence capture before execution.

## Status

```text
STAGE=R270
RESULT=PROVEN_LIVE_BASELINE
STATIC_OR_LIVE=live standard DRM queries plus same-boot kernel-log observation
HARDWARE_MUTATION=none
VCN_STANDARD_API_EXPOSURE=absent in captured ordinary boot
VCN_PSP_ACCEPTANCE=unproven in current boot; historically failed acceptance conditions
VCN_VCPU_EXECUTION=unproven
VCN_HW_VIDEO=unproven
NEXT=prepare a version-matched local reproduction ladder for external GPCNT/RBC/reset-release evidence; first-fetch remains downstream
```
