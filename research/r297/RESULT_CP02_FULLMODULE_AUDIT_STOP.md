# R297 CP02 full-module audit stop

Date: 2026-10-02
Status: BUILD PASS, audit STOP

The composed CP02 + P1 full amdgpu module built successfully.

Module:
- SHA-256: 1e40f5e6a81a6cb95445970876c7ceb9afd5ada328803945e930b448a76fa452
- Build ID: 640cca014583a8f2c807fb2d7a03ee2388b44621

Required CP02, R274B, P1 begin/returned, and R79 markers are present. CP01, obsolete hw_init-skip, and R274A markers are absent. Lifecycle symbols early_init/sw_init/hw_init are present.

The script stopped only because an exact nm grep did not find a symbol named bc250_vcn_pre_reset_init. This is an audit/tooling stop, not a compile failure and not a hardware result. The next step is to inspect the exact symbol spelling/suffix or compiler transformation before deciding whether any rebuild is needed.
