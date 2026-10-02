# R297 CP01 checkpoint result

Date: 2026-10-02

Purpose: replace the unreliable post-blackout keyboard SysRq observation method with an internal diagnostic checkpoint immediately after the last VCN point already observed LIVE: R141 early_init_end.

Evidence:
- R152 baseline vcn_v2_0.c SHA-256: eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
- P1 candidate SHA-256: 97e33967c54696540d621227e36b0e533007a5cc2d29121a9015dda76dfca38a
- R297 CP01 candidate SHA-256: f2f3708699024896310cdb766b9a9efc8bc2f84a7a0b3e3217e20fb0e4b04341
- Corrected Kbuild target: vcn_v2_0.o with M=drivers/gpu/drm/amd/amdgpu
- Corrected object build result: MAKE_RC=0 / PASS
- Object SHA-256: 79ffac3555799a020734c4ce94caea0f922e8b83cbac7acdea7325471ab61c63
- Required diagnostic strings are retained in the object.
- The kernel diagnostic-stop symbol reference is retained.
- vcn_v2_0_cyan_pre_reset_only, early_init, sw_init, and hw_init symbols are retained.
- R152 source restored exactly to baseline after build.
- Build log SHA-256: 504220e4dbb4bf04ccc800d70b888ea8fd518fca1a90ef1b0a09139e8911519e

The first object-build attempt failed only because the target path was specified incorrectly under M=...; it was a build invocation/tooling failure, not a research result.

Boundary:
This proves the CP01 source is object-build-valid. It does not yet prove full-module link, packaging, boot execution, or persistent logging from the research kernel.

Next:
Compose a full amdgpu module from the exact R152 safe baseline, exact R274B amdgpu_vcn.c, and exact R297 CP01 vcn_v2_0.c; then audit, sign, package, and only then perform one controlled boot.
