# R291-K2 result — GFX 10.1.3 platform flags

Date: 2026-10-01

Classification: PROVEN STATIC (source-path contract)

Key findings:
- Cyan Skillfish discovery assigns GC_HWIP = IP_VERSION(10, 1, 3) and UVD_HWIP = IP_VERSION(2, 0, 3) on the non-Skillfish2 fallback path.
- IP_VERSION(10, 1, 3) is classified in the AMDGPU_FAMILY_NV group.
- In nv.c, the IP_VERSION(10, 1, 3) / 10,1,4 case explicitly sets:
  - adev->cg_flags = 0
  - adev->pg_flags = 0
- Therefore this source contract does not advertise AMD_PG_SUPPORT_VCN or AMD_PG_SUPPORT_VCN_DPG for GFX 10.1.3.
- The nearby VCN/VCN_DPG flag assignments belong to other IP-version cases and must not be attributed to GFX 10.1.3.

Implications:
- For this source path, the normal vcn_v2_0_start() DPG selection condition based on AMD_PG_SUPPORT_VCN_DPG is false when fed the GFX10.1.3 platform flags.
- Removing only the Cyan start guard would therefore not automatically select the DPG path because of pg_flags.
- However the VCN power-enable call still needs separate treatment: R291-J v2 showed Cyan's swSMU VCN enable callback is absent and can return success as a no-op.
- Physical VCN power state remains unproven.

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO

R291_K2_GFX1013_PLATFORM_FLAGS=PASS
