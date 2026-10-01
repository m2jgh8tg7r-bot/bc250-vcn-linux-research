# R291-J v2 — Cyan VCN power dispatch gap

Date: 2026-10-01

Artifacts:
- audit script SHA256: 544ae25b67cff917e2c682a11def42e92da069e26807f84c096cd89bfddeee40
- log SHA256: 7a869536bfa2fb1639a10656ebc96aaed1a3fa7799c38206be0397374d7cbb53
- amdgpu_smu.c SHA256: 4d4489ba57df6017414546fc9862cf40927fbc8a45482576fcfce3c1cf8a1d26
- cyan_skillfish_ppt.c SHA256: 9259ad3ff6f660fe97ca7ea68f9b7e5f5d185982f0d3341180bd880442f030f1

Static proof:
- smu_dpm_set_vcn_enable() checks is_vcn_enabled().
- If smu->ppt_funcs->dpm_set_vcn_enable is NULL, it returns 0.
- Cyan Skillfish pptable has no dpm_set_vcn_enable assignment.
- Cyan Skillfish source has no direct PowerUpVcn/PowerDownVcn token.
- Therefore the normal swSMU VCN power-enable dispatch for Cyan can terminate successfully without issuing a Cyan ppt VCN power callback.

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
- R291_J_V2_VCN_ENABLE_DISPATCH=PASS

Interpretation:
This is a concrete Linux-side software gap in the normal VCN power-up path for Cyan Skillfish. It does NOT prove the physical VCN block is powered off, nor that no other firmware/boot path has powered it. It proves only that this normal swSMU path has no Cyan VCN power callback and reports success on callback absence.

Safety:
- HARDWARE_ACCESS=NO
- SOURCE_MODIFICATION=NO
- MODULE_BUILD=NO
- BOOT_CHANGE=NO
- RESET_RELEASE=NO
