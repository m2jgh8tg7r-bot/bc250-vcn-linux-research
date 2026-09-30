# R274-B — native-layout build-only result

Date: 2026-10-01

The commit-pinned R274-B helper completed successfully on the user's retained Linux 7.2.3 source tree.

## Source identity preflight

All guarded source identities matched before mutation:

- amdgpu_vcn.c: 09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099
- amdgpu_psp.c: d0513be4c77d71d72a21ab47764cad16f958e5d193ff21d26d7844ec3be54b1d
- vcn_v2_0.c: eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
- amdgpu_discovery.c: 37202992e43a0d450b0b7e0d9c1e47ca97af95f8d1d02e6f22108aaf9d5302b5
- amdgpu_device.c: cc9fe304c5e51434bb7a2bc4e04ecd3ce61c95e642ea2e9e8ec910d6eb66b679

## Candidate identity

`amdgpu_vcn.c` candidate SHA256:

`06e1595fe8f90503664bc242fefa2cc151d7b43f15f762998ad476e3160ddd67`

## Source delta

R274-B adds only software-side provisioning behavior for Cyan Skillfish VCN 2.0.3:

- enlarge the VCN BO by the existing native non-PSP aligned firmware-region amount;
- validate source firmware bounds;
- validate BO bounds;
- copy the ucode payload from firmware-file offset 256 to VCN BO offset 0;
- zero the remaining BO tail;
- read back the copied 405696 bytes through the CPU mapping;
- compare them to the firmware source and fail on mismatch.

This follows the native amdgpu non-PSP VCN layout more closely than R274-A.

The helper's added-token check returned:

`ADDED_HARDWARE_CONTROL_TOKENS=NONE`

No new VCN MMIO, SMN, VCPU reset-release, ring submission, PSP command, doorbell, or hardware-start calls were added by the R274-B delta.

## Build

Kbuild completed:

```text
CC [M]  amdgpu_vcn.o
LD [M]  amdgpu.o
MODPOST Module.symvers
LD [M]  amdgpu.ko
```

This clean R274-B pass rebuilt only `amdgpu_vcn.o` among the directly observed source objects; `amdgpu_psp.o` was not rebuilt.

Generated module SHA256:

`b1138dd396c0a0e31b3431b9da1a50ae1f564a0ef102864e63e4a75763576ef5`

After the build, `amdgpu_vcn.c` was restored exactly to the known baseline SHA256:

`09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099`

The helper reported:

```text
R274B_BUILD_ONLY_COMPLETE=YES
NO_MODULE_INSTALLED=YES
NO_BOOT_ARTIFACT_CHANGED=YES
```

## Evidence classification

Proven by this build-only run:

- exact guarded source preflight: PROVEN_FILESYSTEM
- R274-B source transform: PROVEN_BUILD
- no added hardware-control tokens: PROVEN_STATICALLY
- amdgpu_vcn.o compilation: PROVEN_BUILD
- amdgpu module link: PROVEN_BUILD
- module artifact identity: PROVEN_BUILD
- baseline source restoration: PROVEN_BUILD
- no module installation or boot mutation by the helper path: PROVEN_BY_SCRIPT_PATH

Still unproven:

- R274-B module boot/load on the user's BC-250
- live VCN BO enlargement
- live 405696-byte copy
- live BO readback equal=1
- absence of PSP LOAD_IP_FW type13 in that boot
- VCPU-visible BO bytes
- VCN cache BAR programming
- first fetch/execution/ready
- physical decode/encode

## Next

Advance to R275 artifact/provenance audit only. Do not boot the module yet.
