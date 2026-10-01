# R291-I result — Cyan runtime power provider audit

Date: 2026-10-01

Key findings:
- swSMU exposes smu_dpm_set_power_gate() as the power-gating callback provider.
- For AMD_IP_BLOCK_TYPE_VCN, smu_dpm_set_power_gate() calls smu_dpm_set_vcn_enable(smu, !gate, inst) and propagates its return code.
- amdgpu_smu.c assigns adev->powerplay.pp_funcs = &swsmu_pm_funcs.
- Cyan Skillfish initialization calls cyan_skillfish_set_ppt_funcs(smu), which assigns smu->ppt_funcs = &cyan_skillfish_ppt_funcs.
- cyan_skillfish_ppt.c contains no direct PowerUpVcn/PowerDownVcn token and no direct set_power_gate token in this audit.
- Therefore the remaining unresolved runtime step is smu_dpm_set_vcn_enable() -> Cyan ppt_funcs behavior.
- The generic "pp_funcs callback absent => false-success state update" risk exists in amdgpu_dpm_set_powergating_by_smu(), but R291-I shows that Cyan's swSMU provider itself does install set_powergating_by_smu; this generic risk should not be treated as proven active on Cyan without auditing smu_dpm_set_vcn_enable/ppt_funcs.

Result:
R291_I_CYAN_POWER_PROVIDER=PASS

Safety:
NO_LIVE_POWER_REQUEST=YES
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO
