R291-P2C POST-BUILD FINAL AUDIT PASS (2026-10-01)

Built full amdgpu module SHA256: 2d792e86dd6ff276b1d7af21337684eb208579466de088ba0e9cb5e6b2e2a640
Build ID: 7ba93d2d4f750bc073ba8e11c5b29b0d162ab3ef
Vermagic: 7.2.3+ SMP preempt mod_unload

The same full module contains exact R274-B direct FW provisioning markers, exact R291-P1 pre-reset begin/returned markers, and the R79 PSP VCN enrollment skip marker. The obsolete R141 hw_init skip marker and R274-A marker are absent. P1 helper and hw_init symbols are retained.

Exact R152 critical source restoration passed for amdgpu_vcn.c, vcn_v2_0.c, amdgpu_psp.c, amdgpu_discovery.c, and amdgpu_device.c. No candidate-derived amdgpu.ko, vcn_v2_0.o, or amdgpu_vcn.o remained active in the source tree.

No module install/load, initramfs or boot change, hardware access, reset release, FILTER write, PowerUpVcn, or reboot occurred.

Result: R291_P2C_POSTBUILD_AUDIT=PASS
