# R274 exact-source preflight result

The user ran the repository's read-only preflight against:

```text
~/bc250-research/r152-psp-boundary-src
```

Generated log:

```text
~/bc250-r274-r152-exact-source-preflight.log
sha256=16310e67547c4786144649ef5c9ceeb416acc7f058b80bfbd65ded77b0a6c4c8
size≈36 KiB
```

## Exact source identity

```text
kernel=7.2.3

amdgpu_discovery.c
37202992e43a0d450b0b7e0d9c1e47ca97af95f8d1d02e6f22108aaf9d5302b5

amdgpu_vcn.c
09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099

vcn_v2_0.c
eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075

amdgpu_device.c
cc9fe304c5e51434bb7a2bc4e04ecd3ce61c95e642ea2e9e8ec910d6eb66b679
```

## Important finding: most of the R274 quarantine is already present

### Discovery already registers VCN 2.0.3

The exact tree already contains:

```c
case IP_VERSION(2, 0, 3):
    amdgpu_device_ip_block_add(adev, &vcn_v2_0_ip_block);
    if (!amdgpu_sriov_vf(adev))
        amdgpu_device_ip_block_add(adev, &jpeg_v2_0_ip_block);
    break;
```

Cyan Skillfish manually receives:

```c
adev->ip_versions[UVD_HWIP][0] = IP_VERSION(2, 0, 3);
```

No R274 discovery change is required.

### PSP VCN enrollment is already quarantined

`amdgpu_vcn_setup_ucode()` already contains the local R79/R141 Cyan Skillfish guard:

```c
if (adev->asic_type == CHIP_CYAN_SKILLFISH) {
    dev_info(... "BC250 R141 psp_vcn_enrollment: skipped (R79 guard)");
    return;
}
```

Therefore the first R274 candidate does not need to alter PSP code or `amdgpu_vcn_setup_ucode()`.

### VCN hardware init is already quarantined

`vcn_v2_0_hw_init()` returns immediately for Cyan VCN 2.0.3.

Thus the first R274 candidate will not boot the VCPU or perform the normal VCN ring hardware tests.

### VCN mc_resume is already quarantined

`vcn_v2_0_mc_resume()` also returns immediately for Cyan VCN 2.0.3.

Thus adding the BO payload does not cause VCPU cache BAR programming in this stage.

This is critical: the initial R274 local experiment can provision the firmware BO while retaining the existing proven hardware boundary.

## Existing software path

`vcn_v2_0_sw_init()` currently performs:

```text
amdgpu_vcn_sw_init
 -> amdgpu_vcn_setup_ucode
 -> amdgpu_vcn_resume
 -> software ring registration
```

The ring-registration behavior is unchanged from the local R141/R171 guarded line and has historical live evidence. R274 does not need to adopt Shalasere's broader experimental ring changes for the first stage.

## The one missing piece

Because the global firmware load type remains PSP:

```c
bo_size = STACK + CONTEXT;
if (load_type != PSP)
    bo_size += aligned_ucode;
```

the current Cyan BO has no dedicated direct-firmware region.

Also, `amdgpu_vcn_resume()` copies firmware only when global `load_type != PSP`; on the Cyan PSP-global path it clears the BO instead.

Therefore R274 needs a narrowly scoped Cyan 2.0.3 software provisioning branch:

1. enlarge the VCN BO by `AMDGPU_GPU_PAGE_ALIGN(ucode_size + 8)`;
2. keep global PSP mode unchanged for all other firmware;
3. clear the VCN BO exactly as before;
4. copy the VCN payload into the dedicated firmware area at `AMDGPU_UVD_FIRMWARE_OFFSET` (256);
5. read back through the CPU mapping and compare to the source payload;
6. fail the init if bounds or equality verification fails;
7. retain the existing PSP enrollment, mc_resume and hw_init guards unchanged.

## Evidence classification

### Newly established

```text
exact local source identity                 PROVEN_LIVE_FILESYSTEM
VCN 2.0.3 discovery already present        STATIC_PROVEN
Cyan PSP enrollment guard already present  STATIC_PROVEN
Cyan VCN hw_init guard already present      STATIC_PROVEN
Cyan VCN mc_resume guard already present    STATIC_PROVEN
one-file R274 design feasibility            STRONGLY_SUPPORTED
```

### Still unproven

```text
R274 candidate compilation
local direct BO allocation with extra region
local 405696-byte payload copy/readback
absence of type13 PSP request in an R274 live boot
VCPU visibility/fetch/execution
physical decode/encode
```

## Next

Build a one-file source candidate with **no install and no live module load**. The build helper must restore the original source automatically even on failure.
