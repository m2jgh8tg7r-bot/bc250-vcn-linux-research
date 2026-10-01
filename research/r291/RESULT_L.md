# R291-L result — start path with GFX10.1.3 zero platform flags

Date: 2026-10-01

Classification: PROVEN STATIC

Key findings:
- vcn_v2_0_start() still begins with the Cyan 2.0.3 quarantine returning -EOPNOTSUPP.
- If that top-level guard is conceptually removed, the function first calls amdgpu_dpm_enable_vcn() when DPM is enabled.
- The DPG branch is conditional on AMD_PG_SUPPORT_VCN_DPG.
- GFX 10.1.3 / 10.1.4 platform initialization sets:
  - adev->cg_flags = 0
  - adev->pg_flags = 0
- Therefore AMD_PG_SUPPORT_VCN_DPG is not set and the DPG branch is not selected by these platform flags.
- The normal non-DPG path is therefore the platform-selected branch after the Cyan guard.
- That path then calls the static-PG helper, status/clock/LMI/MPC setup, vcn_v2_0_mc_resume(), and only after mc_resume crosses the VCPU reset-release boundary.

Checks:
GFX1013_CG_FLAGS_ZERO=YES
GFX1013_PG_FLAGS_ZERO=YES
START_HAS_DPG_BRANCH=YES
START_CALLS_DPM_ENABLE=YES
START_CALLS_MC_RESUME=YES
PG_HELPER_USES_PG_FLAG=YES
CG_HELPER_USES_CG_FLAG=YES

Derived:
GFX1013_VCN_DPG_FLAG_SET=NO
GFX1013_VCN_PG_FLAG_SET=NO
DPG_BRANCH_TAKEN_WITH_PLATFORM_FLAGS=NO
DPM_ENABLE_CALL_STILL_REACHED_AFTER_CYAN_GUARD_REMOVAL=YES
NON_DPG_START_PATH_IS_PLATFORM_SELECTED=YES

Important limits:
- This does not prove physical VCN power state.
- R291-J v2 showed Cyan's swSMU dpm_set_vcn_enable callback is absent and can return success as a no-op.
- Existing Cyan guards on the PG/CG helpers still prevent those helpers from executing on Cyan.
- No reset release or live hardware access was performed.

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO

Artifacts:
- audit script SHA256 6852c59591dc41ee4d412e6b810362ecf0438e95a01b545a27a65f60041e9b65
- log SHA256 9fa995f7aa3fb63494712ca1a5e900bc60084a7834ed4c7a25602a86a8e5c41b

R291_L_START_ZERO_FLAGS=PASS
