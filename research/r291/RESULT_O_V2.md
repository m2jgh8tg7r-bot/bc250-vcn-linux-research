# R291-O v2 result — Cyan pre-reset candidate object build

Date: 2026-10-01

Classification: PROVEN BUILD

Candidate:
- R291-N source SHA256: 119644d465022cde52a32bf9ca28e5563e2e58e64b88f0117ef5f7298f98a81e

Build result:
- Kbuild configuration was prepared successfully from the known source config.
- The kernel build reached and successfully compiled:
  CC [M] drivers/gpu/drm/amd/amdgpu/vcn_v2_0.o
- Produced object SHA256:
  cf6b02cf7583c10c6791dd8f691a6506242d376b8f7a7f803256b763d72743e8
- Source remained unchanged during the build.
- Worktree source was restored after the build to the R291-C SHA:
  8d99fbb07c155353622e680d7d26be412d748f74da88f0a390ed5d73105b677d

Safety:
AMDGPU_MODULE_LINK=NO
MODULE_INSTALL=NO
INITRAMFS_CHANGE=NO
BOOT_CHANGE=NO
HARDWARE_ACCESS=NO
RESET_RELEASE=NO
FILTER_WRITE=NO
REBOOT=NO

Result:
R291_O_V2_OBJECT_BUILD=PASS

Nuance:
- nm produced no matching helper symbols. Because both helpers are static and the pre-reset helper has zero callsites, the compiler may optimize them out of the final object.
- This does not invalidate compile-time syntax/type/macro validation of the function bodies, but it does mean this build does not prove the helper machine code is retained in the object.
- A later build-only candidate with an explicit, still-uninstalled callsite should verify retained code before any live boot.

Artifacts:
- build script SHA256 c3a450c9e1d07f273a287c44e265f5fdeeab8d0b76a3a9d91b247ed776e5f517
- object SHA256 cf6b02cf7583c10c6791dd8f691a6506242d376b8f7a7f803256b763d72743e8
- build log SHA256 c9131ef8b96268472b7805ca1ec7bc29d99ef7dfaf718aded51dd0ba8871a1eb
