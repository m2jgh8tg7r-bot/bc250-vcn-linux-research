# R291-D result — build-only Cyan memory helper

Date: 2026-10-01

Kernel source HEAD:
0bb924b042ab85b8f529aed6e4f3e24750584276

Config:
r152-psp-boundary-src/.config

Candidate source SHA256:
8d99fbb07c155353622e680d7d26be412d748f74da88f0a390ed5d73105b677d

Built object:
drivers/gpu/drm/amd/amdgpu/vcn_v2_0.o

Object SHA256:
606a764f88419e677731f2a25f270b593ea89d2c1ac3772980cba6bb0a9275ba

Build log SHA256:
d8ad61cbc371d633cbfe9415adf8bf20c0f6fe491071b75fc8786795afab1d04

Result:
- R291_D_KERNEL_OBJECT_BUILD=PASS
- HELPER_NAME_OCCURRENCES=1
- HELPER_CALLSITES=0
- HARDWARE_ACCESS=NO
- AMDGPU_MODULE_LINK=NO
- MODULE_INSTALL=NO
- INITRAMFS_CHANGE=NO
- BOOT_CHANGE=NO
- REBOOT=NO
- RESET_RELEASE=NO
- R291_D_BUILD_ONLY=PASS

Interpretation:
The R291-C Cyan memory-window-only helper is accepted by the actual 7.2.3 kernel Kbuild environment and compiles into vcn_v2_0.o. It is still definition-only and cannot execute because there is no callsite.

Important ordering correction:
Normal vcn_v2_0_start() performs VCN power/clock/LMI preparation before vcn_v2_0_mc_resume(), and reset handling follows mc_resume(). Therefore future live testing must not assume memory-window writes are safe or meaningful before the normal pre-mc_resume prerequisites are satisfied. R291-E should audit those prerequisites statically before any callsite is introduced.
