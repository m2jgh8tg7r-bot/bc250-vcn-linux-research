# R272 — Historical R180 replay reproduced live on 2026-10-01

This checkpoint records a successful one-shot replay of the historical R180 PSP LOAD_IP_FW response-observation experiment on the user's BC-250, followed by return to the normal Bazzite kernel.

R272 is a **live reproduction checkpoint**. It does not prove VCN firmware acceptance, VCPU execution, first fetch, RBC execution, or hardware video.

## Experiment identity and boot attribution

The R180 boot was selected manually through a restored BLS entry.

Live boot identity:

```text
kernel_release=7.2.3+
BOOT_IMAGE=/vmlinuz-7.2.3-r138
ostree=/ostree/boot.1/default/b25f8196b82ddc29b0b7050f121f97dea399215bd21874762f29f4f11b6dfb19/0
```

The same-boot collector recorded:

```text
same_boot_for_log_and_identity=true
r180_metadata_correspondence=true
result=PROVEN_LIVE
observation_complete=PROVEN_LIVE
selective_response_pattern=PROVEN_LIVE
trace_issues=[]
```

The analyzer verified 14 capture hashes.

Loaded amdgpu GNU Build ID:

```text
9e4870cde4dfbec0c4dab01a3a7667bd1c153223
```

Expected R180 Build ID:

```text
9e4870cde4dfbec0c4dab01a3a7667bd1c153223
```

Thus the live module/boot attribution for this capture is established.

## Host VCN request reproduced

The R173 host-side observer embedded in R180 again reported:

```text
id=57
command=6
fw_type=13
size=405696
source_aligned=1
source_matches=1
bo_present=1
map_present=1
iomem=0
map_matches=1
bounds_ok=1
header_ok=1
payload_checked=1
payload_equal=1
```

This re-proves host-side request formation and CPU-visible payload equality for the replay.

It still does **not** prove PSP-visible byte identity.

## Same-boot PSP response comparison reproduced

Eleven paired existing LOAD_IP_FW traces were observed:

```text
id  fw_type  size    status       fw_addr_nonzero
1   9        33536   0x0          0
2   10       33536   0x0          0
12  3        263040  0x0          1
13  2        263168  0x0          1
14  1        263168  0x0          1
26  4        267440  0x0          1
27  5        896     0x0          0
28  4        267440  0x0          1
29  6        896     0x0          0
50  8        25088   0x0          0
57  13       405696  0xffff0008   0
```

Every trace had:

- `ret=0`
- `submitted=1`
- `response_valid=1`
- matching expected/observed fence
- timeout remaining
- `ras_intr=0`

Five non-VCN controls (12,13,14,26,28) additionally returned a nonzero firmware address.

VCN ID57/type13 again returned:

```text
status=0xffff0008
fw_addr_nonzero=0
```

The analyzer classified:

```text
trace_pair_count=11
trace_structure_valid=true
accepted_control_count=5
accepted_control_ids=[12,13,14,26,28]
selective_response_conditions_met=true
selective_response_pattern=PROVEN_LIVE
observation_complete=PROVEN_LIVE
root_cause=UNPROVEN
host_request_result=PROVEN_LIVE
```

## Why enrollment_log_conditions_met=false

This field does not indicate missing R180 attribution or an incomplete trace.

The lifecycle had:

```text
exact_event_order=true
valid_event_fields=true
size_and_fence_correspondence=true
```

but:

```text
acceptance_log_conditions_met=false
```

because the VCN PSP response was nonzero (`0xffff0008`) and the returned firmware address was zero.

Therefore:

```text
host request validity          PROVEN_LIVE
transport completion           PROVEN_LIVE
PSP acceptance                 UNPROVEN / acceptance conditions not met
VCN execution                  UNPROVEN
```

## Software lifecycle observations

The R171/R141-derived software diagnostic sequence was complete and ordered.

Notable results:

```text
gpu_initialized=true
diagnostic_sequence_complete=true
vcn_hw_init=skipped
jpeg_hw_init=skipped
```

Delayed VCN IB tests returned `-95` for:

- vcn_dec
- vcn_enc0
- vcn_enc1

The existing analyzer classified these as consistent with the retained R141 quarantine guards, not as hardware-execution results.

## Network / boot health during R180

Captured network state:

```text
enp4s0:ethernet:connected
lo:loopback:connected (externally)
```

Five failed systemd units were present in the R180 boot:

```text
proc-sys-fs-binfmt_misc.mount
var-lib-nfs-rpc_pipefs.mount
bc250-tdp.service
mcelog.service
systemd-binfmt.service
```

No claim is made here that these are caused by R180.

## Return to normal Bazzite

After the R180 capture, the user manually returned to the normal Bazzite entry.

Live recovery output:

```text
kernel_release=7.2.1-ogc4.1.fc44.x86_64
BOOT_IMAGE=.../vmlinuz-7.2.1-ogc4.1.fc44.x86_64
enp4s0=UP
wlp0s16f0u2i2=UP
```

On the normal boot, the reported failed-unit list contained only:

```text
bc250-tdp.service
```

This establishes successful return from the one-shot R180 replay to the ordinary kernel and active network state.

## What R272 newly proves

```text
historical R180 boot replay                     PROVEN_LIVE
R180 amdgpu Build ID attribution                 PROVEN_LIVE
same-boot capture/module attribution             PROVEN_LIVE
14 capture hashes                                VERIFIED
R173 host VCN request conditions in replay       PROVEN_LIVE
11 paired existing LOAD_IP_FW traces             PROVEN_LIVE
non-VCN status-zero controls                     PROVEN_LIVE
five placement/nonzero-address controls          PROVEN_LIVE
VCN ID57/type13 status 0xffff0008                PROVEN_LIVE
selective PSP response pattern reproducibility   PROVEN_LIVE
return to normal 7.2.1 kernel                    PROVEN_LIVE
normal-boot wired interface up                   PROVEN_LIVE
```

## Still not proven

```text
PSP-visible payload identity
meaning/root cause of 0xffff0008
KDB/signer/key/policy diagnosis
VCN firmware acceptance
local GPCNT reproduction
local RBC execution
effective VCPU reset release
VCPU first fetch
VCPU instruction execution
VCPU ready
physical decode/encode
VA-API hardware video
```

## Research consequence

The historical PSP rejection boundary is no longer merely archival evidence. It is reproducible on the present system.

This narrows the next work to explaining or bypassing the specific VCN acceptance boundary and independently reproducing the externally reported post-acceptance milestones.

Do not interpret this as evidence that:

- PSP itself is globally broken,
- the LOAD_IP_FW transport is globally broken,
- VCN silicon is absent or dead,
- `0xffff0008` has a proven symbolic meaning.

Same-boot non-VCN status-zero responses, including five nonzero firmware-address responses, argue against a global PSP/transport failure but do not identify the VCN-specific root cause.

## Recommended next Codex objective

1. Preserve R272 as the current local live baseline.
2. Do not repeat R180 without a specific discriminating reason.
3. Compare the reproducible `0xffff0008` boundary with primary-source external firmware-acceptance work.
4. Identify the exact change(s) between:
   - local R272: valid host request → PSP status `0xffff0008`
   - external reported state: VCN firmware accepted/staged.
5. Prioritize evidence around KDB/signer/key/policy selection and the `0x6007` branch only when exact primary-source provenance exists.
6. In parallel, find a target-matched, known-working, safe acquisition path for externally reported GPCNT/RBC/reset-release observations.
7. Do not invent direct SMN/MMIO access or undocumented selectors.
8. Keep first-fetch/request-emission validation as the post-acceptance frontier.

## Status

```text
STAGE=R272
RESULT=PROVEN_LIVE_R180_REPRODUCTION_AND_NORMAL_RECOVERY
DATE=2026-10-01
R180_REPLAY=proven_live
R180_MODULE_ATTRIBUTION=proven_live
TRACE_PAIRS=11
ACCEPTED_CONTROL_COUNT=5
VCN_ID=57
VCN_FW_TYPE=13
VCN_SIZE=405696
VCN_STATUS=0xffff0008
VCN_FW_ADDR_NONZERO=0
SELECTIVE_RESPONSE_PATTERN=proven_live
ROOT_CAUSE=unproven
VCN_PSP_ACCEPTANCE=unproven
VCN_EXECUTION=unproven
NORMAL_RECOVERY_KERNEL=7.2.1-ogc4.1.fc44.x86_64
NORMAL_RECOVERY_NETWORK=enp4s0_up
NEXT=diff reproducible local rejection boundary against primary-source external acceptance path; then advance toward safe local reproduction of GPCNT/RBC/reset-release
```
