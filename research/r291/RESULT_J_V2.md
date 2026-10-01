# R291-J v2 result — Cyan VCN power-enable dispatch

Date: 2026-10-01

Source provenance:
- amdgpu_smu.c SHA256: 4d4489ba57df6017414546fc9862cf40927fbc8a45482576fcfce3c1cf8a1d26
- cyan_skillfish_ppt.c SHA256: 9259ad3ff6f660fe97ca7ea68f9b7e5f5d185982f0d3341180bd880442f030f1

Static findings:
- smu_dpm_set_vcn_enable() checks is_vcn_enabled().
- If smu->ppt_funcs->dpm_set_vcn_enable is absent, it returns 0.
- Cyan Skillfish's cyan_skillfish_ppt_funcs contains no dpm_set_vcn_enable assignment.
- cyan_skillfish_ppt.c contains no PowerUpVcn / PowerDownVcn / SMU_MSG_PowerUpVcn / SMU_MSG_PowerDownVcn tokens.
- Therefore, for the Cyan pptable, the generic smu_dpm_set_vcn_enable path can return success without invoking a VCN power callback.
- Combined with R291-H, amdgpu_dpm_set_powergating_by_smu() can then treat ret==0 as success and update software pwr_state even though no Cyan VCN power callback was invoked.

Checks:
- SMU_CALLBACK_GUARD_PRESENT=YES
- SMU_CALLBACK_CALL_PRESENT=YES
- MISSING_CALLBACK_RETURN=0
- CYAN_DPM_SET_VCN_ENABLE_ASSIGNMENTS=0
- CALLBACK_GUARD_PRESENT=YES
- CALLBACK_CALL_PRESENT=YES
- CYAN_CALLBACK_ABSENT=YES
- CYAN_DIRECT_POWER_MESSAGE_ABSENT=YES
- MISSING_CALLBACK_IS_SUCCESS_RETURN=YES
- CYAN_GENERIC_VCN_ENABLE_CAN_NOOP_SUCCESS=YES
- CYAN_PPT_VCN_POWER_CALLBACK_PRESENT=NO
- CYAN_DIRECT_POWERUPVCN_IMPLEMENTATION_PRESENT=NO

Classification:
PROVEN STATIC only. Not yet proven live that a runtime power-up call on the BC-250 emits no SMU message or that physical VCN power remains off.

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO

R291_J_V2_VCN_ENABLE_DISPATCH=PASS

Artifacts:
- audit script SHA256 544ae25b67cff917e2c682a11def42e92da069e26807f84c096cd89bfddeee40
- log SHA256 7a869536bfa2fb1639a10656ebc96aaed1a3fa7799c38206be0397374d7cbb53
