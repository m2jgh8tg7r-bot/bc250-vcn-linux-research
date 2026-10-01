# R291-N v2 result — Cyan pre-reset candidate final static audit

Date: 2026-10-01

Classification: PROVEN STATIC / CANDIDATE DEFINITION ONLY

Source hashes:
- R291-C source: 8d99fbb07c155353622e680d7d26be412d748f74da88f0a390ed5d73105b677d
- R291-N candidate: 119644d465022cde52a32bf9ca28e5563e2e58e64b88f0117ef5f7298f98a81e

Confirmed:
- vcn_v2_0_cyan_pre_reset_only is defined exactly once and has zero callsites.
- The R291-C memory helper is byte-identical and has one internal callsite from the new pre-reset helper.
- Direct pre-reset operation counts: 13 WREG32_SOC15, 2 WREG32_P, 9 RREG32_SOC15, 1 SOC15_WAIT_ON_RREG.
- Order is PGFSM_CONFIG -> PGFSM_STATUS wait -> POWER_STATUS -> STATUS -> CGC -> SUVD CGC -> VCPU clock -> MASTINT disabled -> LMI -> MPC -> existing R291-C memory helper.
- Runtime guards for zero pg/cg flags and SR-IOV are present.
- No SOFT_RESET, UVD_REG_FILTER_EN, PowerUpVcn/PowerDownVcn, amdgpu_dpm_enable_vcn, MMSCH, RBC/ring, doorbell code appears in the helper.
- Existing vcn_v2_0_start, disable_static_power_gating, disable_clock_gating, and mc_resume functions are byte-identical to R291-C.
- Therefore runtime behavior remains unchanged because the helper is uncalled.

Safety:
HARDWARE_ACCESS=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
REBOOT=NO
RESET_RELEASE_PRESENT=NO
FILTER_WRITE_PRESENT=NO

Result:
R291_N_V2_FINAL_STATIC_AUDIT=PASS

Artifacts:
- audit script SHA256 a18e94b79439f0286bc4cf925d54d66f71058c66cbab8c38175f43a4429db82d
- candidate SHA256 119644d465022cde52a32bf9ca28e5563e2e58e64b88f0117ef5f7298f98a81e
- log SHA256 4fb49155e211c566d6aa4a3765c32fd5aa6ea07d29e32aeed6cd3d4b5791e126
