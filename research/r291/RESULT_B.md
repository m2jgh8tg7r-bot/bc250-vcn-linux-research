# R291-B result

R291-B memory layout contract passed.

Key facts:
- source WREG statements: 20
- runtime writes per branch: 17
- PSP cache0 uses VCN TMR
- native cache0 uses adev->vcn.inst->gpu_addr
- native cache0 uses AMDGPU_UVD_FIRMWARE_OFFSET >> 3
- native firmware copy destination is BO base, not BO+256
- all 14 common mapping writes are present
- mc_resume contains no start/reset/power/ring code
- direct-copy Cyan path therefore needs native cache0 layout
- guard removal alone is not acceptable
- next candidate is a Cyan memory-window-only helper

R291_B_MEMORY_LAYOUT_CONTRACT=PASS

Local log SHA256:
605a03cf0b3133d29175d230ab27c98b2690c6b3e0596fa29f4a6deb48461e4f
