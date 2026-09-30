# R274 — Guarded minimal direct-load port plan

R274 is the first local implementation stage after R273.

## Goal

Prove only the software provisioning branch:

```text
VCN 2.0.3 software enumeration
 -> request/parse vcn_2_0_3.bin
 -> allocate VCN BO large enough for ucode + stack/context/fw_shared
 -> copy exactly the header-declared 405696-byte payload at offset 256
 -> verify CPU-visible equality
 -> do not register VCN with PSP LOAD_IP_FW
 -> finish GPU init with all VCN hardware activity quarantined
```

## Explicit non-goals for the first live stage

The first R274 live artifact must not perform:

```text
VCN MMIO reads
VCN MMIO writes
vcn_v2_0_mc_resume register programming
vcn_v2_0_start
VCPU reset release
VCN/JPEG hw_init
VCN ring hardware setup / IB tests
undocumented SMN accesses
power/clock/reset experiments
```

## Why this is narrower than Shalasere vcn_direct

Shalasere's external implementation proves that a broader direct-load path can load amdgpu under guarded variants.

Our local source already contains R171/R141-derived quarantine work and has separately reproduced the PSP boundary in R272.

Therefore R274 should not transplant the whole external patch. It should make the smallest source delta required to prove local BO provisioning and PSP-registration bypass while retaining the already-audited local hardware guards.

## Required exact-source preflight

Before generating a patch, capture the exact current R152/R171-derived function bodies for:

- amdgpu_vcn_sw_init
- amdgpu_vcn_setup_ucode
- vcn_v2_0_sw_init
- vcn_v2_0_hw_init
- vcn_v2_0_mc_resume
- the IP_VERSION(2,0,3) discovery case
- the device hw-init quarantine call site / markers

Also record SHA256 for the relevant source files.

The repository script `research/r274/r152_exact_source_preflight.sh` performs only reads and writes a text log.

## Candidate minimal delta after preflight

Expected logical changes, subject to exact-source confirmation:

1. keep global firmware load type as PSP for all normal firmware;
2. enlarge only the VCN BO by the VCN ucode payload allocation amount;
3. copy the VCN ucode into the VCN BO at `AMDGPU_UVD_FIRMWARE_OFFSET`;
4. skip only VCN's PSP ucode-list enrollment;
5. preserve existing VCN/JPEG hardware-init quarantine;
6. avoid the non-PSP `mc_resume` register path in the first live stage;
7. add explicit R274 log markers and CPU-side byte-equality verification.

The first live stage intentionally does not point VCPU cache BARs at the BO.

## Proof target

A successful first R274 live run would establish:

```text
local firmware request/parse             PROVEN_LIVE
local VCN BO allocation                  PROVEN_LIVE
local CPU-side ucode copy                PROVEN_LIVE
local copied payload equality            PROVEN_LIVE
VCN PSP enrollment absent                PROVEN_LIVE
VCN PSP LOAD_IP_FW type13 absent         PROVEN_LIVE
normal GPU/display/network recovery      PROVEN_LIVE
```

It would not establish VCPU visibility, fetch, execution, ready, RBC execution, decode or encode.
