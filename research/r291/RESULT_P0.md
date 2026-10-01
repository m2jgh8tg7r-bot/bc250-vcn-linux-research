# R291-P0 result — callsite architecture audit (partial; one audit false positive)

Date: 2026-10-01

Classification: PARTIAL STATIC / AUDIT CORRECTION

Confirmed:
- vcn_v2_0_hw_init() has a Cyan 2.0.3 guard that logs and returns 0 before doorbell setup and ring tests.
- vcn_v2_0_start() itself has a separate Cyan guard returning -EOPNOTSUPP.
- In the normal vcn_v2_0_start() body, vcn_v2_0_mc_resume() precedes the first VCPU SOFT_RESET release.
- amdgpu_vcn_resume() performs firmware BO copy/clear work but has no WREG32, SOFT_RESET, or RBC operations in the audited body.
- vcn_v2_0_funcs assigns .hw_init = vcn_v2_0_hw_init exactly once.

Audit correction:
- The original P0 check used hw.find("vcn_v2_0_start"), which matched the substring vcn_v2_0_start_sriov() inside vcn_v2_0_hw_init().
- Therefore HW_INIT_START_CALL_POS and CYAN_GUARD_PRECEDES_START do NOT prove that normal vcn_v2_0_start() is called from hw_init().
- The normal start callsite must be located exactly before finalizing the live-callsite architecture.

Still-valid design observation:
- The Cyan branch of vcn_v2_0_hw_init() is before doorbell configuration and ring tests, so inserting pre_reset_only() there would keep those hw_init-side actions bypassed.
- This does not yet prove there is no earlier/later separate vcn_v2_0_start() invocation elsewhere in the IP-block lifecycle.

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO
FILTER_WRITE=NO
