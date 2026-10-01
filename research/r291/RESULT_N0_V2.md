# R291-N0 v2 result — R291-C helper semantic audit

Date: 2026-10-01

Classification: PROVEN STATIC / SOURCE ARTIFACT REUSE

Source hashes:
- baseline vcn_v2_0.c: eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
- R291-C candidate: 8d99fbb07c155353622e680d7d26be412d748f74da88f0a390ed5d73105b677d

Confirmed:
- R291-C helper name occurrences = 1; callsites = 0.
- Helper contains exactly 17 WREG32_SOC15 writes.
- Helper contains no register reads, no WREG32_P, no waits.
- All 17 expected native VCN memory-window registers appear exactly once.
- No executable SOFT_RESET, DPM enable, PowerUpVcn/PowerDownVcn, UVD_REG_FILTER_EN, MMSCH, RBC/ring, doorbell, wait, or mdelay tokens.
- Previous N0 doorbell hit was comment-only and is resolved.

Result:
R291C_MEMORY_HELPER_SAFE_TO_REUSE_AS_SOURCE_ARTIFACT=YES
R291_N0_V2_R291C_HELPER_AUDIT=PASS

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO
FILTER_WRITE=NO

Artifacts:
- audit script SHA256 a3af14fa323b63e4e5f2af71d5ddc932ac3493d63f12c79753d00468a48f6d96
- log SHA256 536128b6da27ff67bafd4e0387a08f668a9129ccd12c6d1180165a7e37319fdf
