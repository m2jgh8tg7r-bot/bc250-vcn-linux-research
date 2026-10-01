# R291-F result — pre-mc dependency audit

Date: 2026-10-01

Source SHA256:
eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075

Key findings:
- Cyan start guard is present and returns -EOPNOTSUPP before all normal pre-mc work.
- pre-mc control flow has two returns: Cyan quarantine and DPG-mode diversion.
- pre-mc start body performs 3 direct hardware reads and has no wait/delay primitive itself.
- pre-mc calls:
  - amdgpu_dpm_enable_vcn()
  - vcn_v2_0_disable_static_power_gating()
  - vcn_v2_0_disable_clock_gating()
- static-power-gating helper has its own Cyan guard and currently returns immediately on Cyan.
- static-power-gating helper contains 3 writes, 1 register read and 2 SOC15_WAIT_ON_RREG polls on the normal path.
- clock-gating helper has its own Cyan guard and currently returns immediately on Cyan.
- clock-gating helper contains 5 writes and 5 reads on the normal path, no wait/delay primitive.
- first post-mc write is UVD_SOFT_RESET; there are zero post-mc writes before that reset boundary.

Result:
PRE_MC_HAS_HARDWARE_READS=YES
PRE_MC_HAS_WAIT_OR_DELAY=NO
PRE_MC_DEPENDENCIES_INVENTORIED=YES
RESET_BOUNDARY_RETAINED=YES
R291_F_PRE_MC_DEPENDENCY_AUDIT=PASS

Important interpretation:
A future Cyan pre-mc candidate cannot simply call the existing PG/CG helpers, because both are explicitly quarantined on Cyan. Nor is it sufficient to copy only their write statements: the PG path includes status polling that is part of the normal sequencing contract. The DPG diversion and DPM power-enable path also need separate audit before any live callsite is introduced.

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO

Artifacts:
- audit script SHA256 a561c06fd99770fe2cf4f66ab8f163d52626cdbad17d1fd72c89a0d34de02791
- log SHA256 798ec05e77b83c74d2887ede0149d828f0d93ef6dc79f9f3c27700c1c7e2929c
