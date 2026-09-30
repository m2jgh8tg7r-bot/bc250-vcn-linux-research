# R273 — Direct-load compatibility closure

R273 establishes the **static compatibility basis** for trying a guarded driver-side VCN firmware load on the user's BC-250. It does not claim that direct-load has been executed locally.

## Evidence classes

### 1. Direct local proof already established before R273

R272 reproduced the historical local PSP boundary:

```text
VCN id=57
command=6
fw_type=13
payload size=405696
host request/payload conditions=PROVEN_LIVE
PSP response=0xffff0008
PSP firmware address=0
VCN PSP acceptance=UNPROVEN
```

Thus the ordinary local PSP path remains a reproducible rejection boundary.

### 2. Static/model proof established in R273

Historical and retained amdgpu source shows that VCN has a native non-PSP firmware path.

In older `amdgpu_vcn.c`, when:

```c
adev->firmware.load_type != AMDGPU_FW_LOAD_PSP
```

the driver copies VCN ucode directly into the VCN BO using the firmware header's ucode offset/size.

The VCN 2.0 memory-controller setup also contains a native split:

- PSP load: VCPU cache BAR points at the PSP-managed TMR address.
- non-PSP load: VCPU cache BAR points at `adev->vcn.inst->gpu_addr`.
- the firmware window uses `AMDGPU_UVD_FIRMWARE_OFFSET >> 3`.

This pattern is visible across retained source history including v5.4, v5.15, v6.6, v6.12 and v7.2.

Therefore the architectural idea "firmware in driver-managed BO, then VCPU cache window points at that BO" is not a BC-250-specific invention. It is an existing amdgpu/VCN load mode.

## Local source target identity

The retained R152 source target is Linux 7.2.3.

Recorded file identities:

```text
amdgpu_discovery.c
37202992e43a0d450b0b7e0d9c1e47ca97af95f8d1d02e6f22108aaf9d5302b5

amdgpu_vcn.c
09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099

vcn_v2_0.c
eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
```

## Local firmware identity

The retained local firmware candidate used by the historical PSP experiment is:

```text
file=vcn_2_0_3.bin
file_size=405952
payload_size=405696
header_size=256
sha256=a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5
```

The 405696-byte payload size matches the R272/R180 PSP request size.

## External Shalasere evidence

Primary external reference:

```text
repository=Shalasere/bc250-vcn-research
head=6c85b2fe382599ec80d6222b5ffe70eabb97457b
date=2026-09-30
```

That work reports a patched `amdgpu` path which:

1. enumerates VCN 2.0.3,
2. enlarges the VCN BO,
3. copies the 405696-byte VCN payload into the BO at `AMDGPU_UVD_FIRMWARE_OFFSET`,
4. skips VCN PSP autoload registration,
5. selects the driver's non-PSP VCPU cache BAR path,
6. can load amdgpu and expose DRM nodes under its guarded configuration.

This is **external live evidence**, not yet reproduced on the user's board.

The same external work explicitly states that this does not establish working VCN decode/encode and that attempts to proceed into VCN hardware/MMIO have separate power/isolation problems.

## What R273 proves

```text
native amdgpu non-PSP VCN firmware-copy architecture    STATIC_PROVEN
native VCN2 non-PSP cache-BAR architecture             STATIC_PROVEN
firmware offset convention at +256                     STATIC_PROVEN
local retained source target identity                  STATIC_PROVEN
local vcn_2_0_3.bin identity                           DIRECT_FILESYSTEM_EVIDENCE
compatibility of the direct-load design concept        STRONGLY_SUPPORTED
```

## What R273 does not prove

```text
local direct-load execution
local BO contents after a new patched boot
VCPU-visible firmware bytes
VCN register accessibility
VCN power/clock state
effective reset release
first instruction fetch
instruction retirement
VCN ready
RBC hardware execution
physical decode/encode
```

## Research consequence

The local PSP failure and the direct-load route are now distinct testable branches:

```text
existing local path:
vcn_2_0_3.bin
  -> amdgpu
  -> PSP LOAD_IP_FW type13
  -> 0xffff0008

candidate bypass:
vcn_2_0_3.bin
  -> driver-managed VCN BO
  -> [later, only after separate safety proof] VCPU cache BAR
  -> VCN
```

The first local direct-load experiment should **not** attempt VCN hardware bring-up.

R274 should stop after proving software-side BO allocation/copy and PSP-registration bypass while explicitly quarantining all VCN MMIO, ring registration and VCPU reset release.
