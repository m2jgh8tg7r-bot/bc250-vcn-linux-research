# R274-A build-only audit

Date: 2026-10-01

## User-supplied artifacts

The user supplied:

- build.log
- amdgpu.ko.unstripped.sha256
- r274-minimal-direct-load.patch
- amdgpu_vcn.c.candidate
- amdgpu_vcn.c.baseline

Independent artifact checks:

```text
baseline amdgpu_vcn.c
09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099

candidate amdgpu_vcn.c
9848d3586d1091c840d1b90f35f687148025ca93f5c62752f4228f7e77b53084

built amdgpu.ko
f596ec30cd0ad7bd63e8afa4ea0ac020c9f10fd8d27ea640e3e4d3510750b58e
```

The uploaded patch exactly reproduces the uploaded baseline -> candidate textual diff.

Kbuild completed through:

```text
CC [M] amdgpu_psp.o
CC [M] amdgpu_vcn.o
LD [M] amdgpu.o
MODPOST Module.symvers
LD [M] amdgpu.ko
```

The source restoration hash returned exactly to the known baseline:

```text
09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099
```

Therefore:

```text
R274-A source transform reproducible      PROVEN_STATICALLY
R274-A compile/link                       PROVEN_BUILD
source restoration                        PROVEN_BUILD
module installation                       NOT_PERFORMED
boot artifact mutation                    NOT_PERFORMED
R274-A live execution                     UNPROVEN
```

## No new VCN register transaction in R274-A delta

The source delta adds:

- one include for kvmalloc/kvfree support;
- one include for the UVD firmware offset constant;
- Cyan 2.0.3-specific BO sizing;
- Cyan 2.0.3-specific BO memset/copy/readback/compare;
- diagnostic logging and error returns.

The added lines do not contain VCN register access, WREG/RREG, SMN access, VCPU reset release, ring submission, PSP command submission, or other hardware-control primitives.

The BO readback uses the already-mapped driver-managed VCN BO. This is not a VCN register read.

## Important correction: R274-A placement should not be used live

R274-A copied the 405696-byte payload to:

```text
BO + AMDGPU_UVD_FIRMWARE_OFFSET
BO + 256
```

A re-check against the actual native amdgpu non-PSP VCN path shows that upstream/local `amdgpu_vcn_resume()` copies the ucode payload to the **BO base**, not to BO+256.

Separately, `vcn_v2_0_mc_resume()` programs:

```text
BAR = BO gpu_addr
VCPU_CACHE_OFFSET0 = AMDGPU_UVD_FIRMWARE_OFFSET >> 3
```

Thus `AMDGPU_UVD_FIRMWARE_OFFSET` belongs to the VCPU cache mapping semantics, while the native software copy places payload bytes at physical BO offset 0.

The following sizes also converge exactly:

```text
ucode_size = 405696
firmware file size = 405952
header/source offset = 256
page = 4096

ALIGN(ucode_size + 8) = 409600
ALIGN(firmware_file_size + 4) = 409600
```

This is the firmware-region size used by the native BO allocation / VCN2 memory-controller layout.

R274-A therefore remains useful as a build proof but is **not approved for live use**.

## External-source correction

Shalasere commit:

```text
6c85b2fe382599ec80d6222b5ffe70eabb97457b
```

copies firmware during `amdgpu_vcn_sw_init()` to BO+256 and logs `VCN-DIRECT: fw copy complete`.

However its published `vcn_v2_0_sw_init()` then calls `amdgpu_vcn_resume()`. With global firmware load type still PSP and `saved_bo == NULL` on initial initialization, the published `amdgpu_vcn_resume()` takes the PSP branch and executes:

```c
memset_io(ptr, 0, size);
```

over the full VCN BO.

Therefore the public source/log combination proves that the copy was attempted and completed at that point, but does **not** prove that the copied payload remained in the BO after `amdgpu_vcn_resume()`.

This does not disprove every external live observation, because the exact live-built artifact could have differed from the published source. It does mean post-resume direct-load persistence must be treated as **UNPROVEN externally from the currently published source**.

## Additional build provenance item

R274-A Kbuild also rebuilt `amdgpu_psp.o` because of tree/object state, even though the R274 source delta did not change `amdgpu_psp.c`.

Before producing a live artifact, the next build helper must assert the known restored PSP baseline:

```text
amdgpu_psp.c
2087292def28e46fec9f4df25b152429eabb411e7be748e4121b7232f9f753a2
```

and the known R152/R157 guard-source identities before invoking Kbuild.

## Next

R274-B:

- copy ucode to BO offset 0, matching the native non-PSP path;
- zero the remaining BO tail;
- verify source firmware bounds;
- verify BO bounds;
- read back and compare the copied 405696 bytes;
- assert the exact amdgpu_psp.c, amdgpu_vcn.c, vcn_v2_0.c, amdgpu_discovery.c and amdgpu_device.c source hashes;
- build only;
- restore amdgpu_vcn.c automatically;
- no module install, no initramfs creation, no boot.
