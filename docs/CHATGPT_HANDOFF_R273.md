# R273 handoff — direct-load compatibility established, local execution not yet attempted

## Current strongest local live baseline

R272 is the current live hardware baseline.

The user's BC-250 reproduced:

```text
VCN id=57 / command=6 / fw_type=13 / size=405696
host request conditions valid
host CPU-visible payload equality valid
PSP response status=0xffff0008
firmware address=0
```

Eleven paired PSP LOAD_IP_FW observations and five status-zero/nonzero-address controls were reproduced. Root cause of `0xffff0008` remains unproven.

## R273 static result

R273 examined retained amdgpu source history and the current Shalasere direct-load implementation.

The important result is that driver-side VCN direct loading is based on an existing amdgpu architecture:

```text
non-PSP load
  -> allocate sufficiently large VCN BO
  -> copy firmware ucode from header-described offset
  -> place it at AMDGPU_UVD_FIRMWARE_OFFSET
  -> VCN 2.0 non-PSP mc_resume path uses adev->vcn.inst->gpu_addr
```

This pattern exists independently of the BC-250 patch.

## Local firmware identity

```text
vcn_2_0_3.bin
size=405952
ucode payload=405696
header=256
sha256=a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5
```

## External primary source

```text
Shalasere/bc250-vcn-research
HEAD 2026-09-30:
6c85b2fe382599ec80d6222b5ffe70eabb97457b
```

External live claims include VCN enumeration, direct BO copy, PSP VCN registration bypass and successful amdgpu/DRM-node emergence under guarded settings.

Treat these as external evidence until locally reproduced.

## Safety boundary for R274

Do **not** begin with the external full `vcn_direct=1`/hardware-start behavior.

First local stage must prohibit:

```text
VCN MMIO read/write
vcn_v2_0_mc_resume register programming
vcn_v2_0_start
VCPU soft-reset release
VCN/JPEG hw_init
VCN ring amdgpu_ring_init
hardware IB tests
undocumented SMN access
```

The first target is software-only:

```text
enumerate the VCN 2.0.3 software block
request/parse vcn_2_0_3.bin
allocate VCN BO sized for payload + stack/context
copy exactly 405696 bytes to BO + 256
verify CPU mapping equality
ensure VCN is not enrolled into PSP LOAD_IP_FW
return without touching VCN hardware
```

## Evidence interpretation

If that first guarded stage succeeds, it proves only:

```text
local direct-load software provisioning path
local BO allocation
local CPU-side firmware placement
local PSP-registration bypass
```

It still does not prove PSP acceptance (not used), VCPU-visible bytes, first fetch, execution or decode.

## Next objective

R274: implement and statically audit the minimal guarded port against the retained 7.2.3 source tree before any live boot.
