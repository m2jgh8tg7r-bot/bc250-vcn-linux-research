# R291-P0 v5 result — boot init dispatch audit

Date: 2026-10-01

Classification: PROVEN STATIC

Confirmed:
- vcn_v2_0_sw_init order is amdgpu_vcn_sw_init -> amdgpu_vcn_setup_ucode -> amdgpu_vcn_resume -> amdgpu_ring_init.
- vcn_v2_0_sw_init has no Cyan early return; the initial firmware BO copy path is live for Cyan.
- vcn_v2_0_resume callback itself has a Cyan early return before its internal amdgpu_vcn_resume and hw_init calls.
- vcn_v2_0_hw_init Cyan guard is before hardware doorbell setup and ring tests.
- VCN ip funcs map sw_init, hw_init, and resume exactly once.
- Generic amdgpu_device_ip_init dispatches sw_init before HW-init phases.
- phase2 dispatches version->funcs->hw_init for eligible software-initialized IP blocks.

Derived static model:
vcn_v2_0_sw_init -> amdgpu_vcn_resume (initial FW BO copy) -> software ring setup -> generic HW init -> vcn_v2_0_hw_init Cyan branch.

Therefore the limited pre-reset callsite candidate remains:
`vcn_v2_0_hw_init()` Cyan branch, before hardware doorbell/ring tests.

Important wording:
- The software ring objects already exist by this point; call this a pre-hardware-ring / pre-doorbell / pre-ring-test boundary, not pre-software-ring.

Result:
R291_P0_V5_INIT_DISPATCH=PASS

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO
FILTER_WRITE=NO

Artifacts:
- audit script SHA256 2d1391ac2b0626169ad1f9e6a0f78115e2e7aa5acc185c6860bed8a7dc832a86
- log SHA256 50d54e1a54b0d852f58b9ee44bba0124d90116e0a4b0d3927259c4ce76f20204
