R291-P2B SAFE BASE CLOSURE PASS (2026-10-01)

Exact R152 source provenance passed for amdgpu_vcn.c, vcn_v2_0.c, amdgpu_psp.c, amdgpu_discovery.c, and amdgpu_device.c. Exact R274-B amdgpu_vcn.c and exact R291-P1 vcn_v2_0.c inputs also matched expected SHA256 values.

The safe composition model is fixed as: base tree r152-psp-boundary-src; overlay exact R274-B amdgpu_vcn.c; overlay exact R291-P1 vcn_v2_0.c; no other relevant base files changed.

Confirmed preserved: PSP VCN enrollment skip, common VCN ring/test quarantine, normal start quarantine, reset quarantine, and mc_resume guard. Added by composition: R274-B direct FW provisioning and P1 limited pre-reset hw_init call. No SOFT_RESET release, FILTER write, PowerUpVcn, or RBC/ring hardware setup was added.

No source modification, build, module link/install, initramfs or boot change, hardware access, or reboot occurred.

Result: R291_P2B_SAFE_BASE_CLOSURE=PASS
