# R286 static frontier result

Date: 2026-10-01

Exact source identities:
- vcn_v2_0.c: eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
- amdgpu_device.c: cc9fe304c5e51434bb7a2bc4e04ecd3ce61c95e642ea2e9e8ec910d6eb66b679

Static proof:
- Cyan Skillfish VCN 2.0.3 returns immediately from vcn_v2_0_mc_resume before any cache/BAR programming.
- Cyan Skillfish VCN 2.0.3 returns immediately from vcn_v2_0_hw_init.
- Normal vcn_v2_0_mc_resume programs VCPU cache window 0 for firmware, cache windows 1/2 for stack/context, a non-cache fw_shared window, and GFX10 address config.
- The normal PSP branch uses the PSP VCN TMR address and cache offset 0.
- The normal non-PSP branch uses the VCN BO gpu_addr and AMDGPU_UVD_FIRMWARE_OFFSET >> 3, then places stack/context after the firmware region.
- vcn_v2_0_hw_init performs doorbell setup and ring tests; it does not contain the mc_resume programming.
- Static grep shows Cyan-specific -EOPNOTSUPP returns in vcn_v2_0.c, so R285 ring-test -95 needs exact call-path attribution before being interpreted as hardware failure.

Implication:
R285 proved live direct BO provisioning, but R286 proves the normal VCPU memory-window connection is still skipped on Cyan 2.0.3. The next step is static-only attribution of the mc_resume caller/start sequence and the exact -EOPNOTSUPP source before any live register-write experiment.

Log SHA256:
42b9a53668b916df20ee64b0aa97d99f9fd2d375c8bc5dc6e5b5d4fac3a38eb1
