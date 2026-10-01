# R291-P0 v4 result — exact lifecycle audit

Date: 2026-10-01

Classification: PROVEN STATIC, with an important lifecycle nuance

Confirmed:
- Source provenance matched expected vcn_v2_0.c.
- Forward declarations and real definitions were separated correctly.
- vcn_v2_0_reset has one prototype and one definition.
- vcn_v2_0_set_pg_state has one prototype and one definition.
- Exact normal vcn_v2_0_start callsites are fully classified: one in reset and one in set_pg_state.
- Both are blocked by Cyan-specific guards before reaching vcn_v2_0_start.
- vcn_v2_0_hw_init has no normal vcn_v2_0_start call and its Cyan return occurs before doorbell setup and ring tests.
- Function table assignments for hw_init and resume are unique.

Important nuance:
- vcn_v2_0_resume itself also has a Cyan early return before amdgpu_vcn_resume() and vcn_v2_0_hw_init().
- Therefore the statement `RESUME_COPY_BEFORE_HW_INIT=YES` describes ordering inside the non-Cyan body, not the live Cyan execution path.
- A separate audit is required to locate the actual generic boot-time caller of .hw_init on Cyan before inserting the limited pre-reset callsite.

Result:
R291_P0_V4_EXACT_LIFECYCLE=PASS

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO
FILTER_WRITE=NO
