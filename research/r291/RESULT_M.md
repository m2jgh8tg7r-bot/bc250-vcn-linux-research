# R291-M result — Cyan VCN sequence-gap audit

Date: 2026-10-01

Classification: PROVEN STATIC

Source hashes:
- vcn_v2_0.c: eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
- nv.c: 2caff07352a311acc0f960504fc954a525109fad70880a4497cce1255f2ae646

Confirmed:
- GFX 10.1.3/10.1.4 sets adev->cg_flags = 0 and adev->pg_flags = 0.
- Cyan guards exist independently in start, static-PG helper, clock-gating helper, and mc_resume.
- The zero-flag normal PG path contains PGFSM_CONFIG write, PGFSM_STATUS wait for zero, POWER_STATUS read/clear/write.
- The zero-flag normal CG path contains CGC_CTRL/CGC_GATE/SUVD_CGC_GATE/SUVD_CGC_CTRL programming.
- Normal pre-reset order is DPM -> DPG check -> PG -> STATUS -> CG -> VCPU clock -> LMI -> MPC -> mc_resume -> reset.
- FILTER/security/FW-version registers are not referenced by the normal VCN2 start+PG+CG+mc_resume path in this source.
- Therefore the FILTER hypothesis can be kept as an independent later A/B rather than mixed into the first pre-reset reconstruction.

Derived:
GFX1013_SELECTS_DPG=NO
ZERO_FLAG_PG_SEQUENCE_EXISTS=YES
ZERO_FLAG_CG_SEQUENCE_EXISTS=YES
CYAN_GUARD_BLOCKS_PG_SEQUENCE=YES
CYAN_GUARD_BLOCKS_CG_SEQUENCE=YES
MEMORY_MAPPING_PRECEDES_RESET=YES
FILTER_IS_NOT_PART_OF_NORMAL_VCN2_START_SEQUENCE=YES

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO
FILTER_WRITE=NO

R291_M_SEQUENCE_GAP_AUDIT=PASS
