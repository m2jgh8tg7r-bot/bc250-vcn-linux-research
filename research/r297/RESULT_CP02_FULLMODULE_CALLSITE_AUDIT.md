# R297 CP02 full-module callsite audit

Date: 2026-10-02
Status: PASS

Exact module:
- SHA-256: 1e40f5e6a81a6cb95445970876c7ceb9afd5ada328803945e930b448a76fa452
- Build ID: 640cca014583a8f2c807fb2d7a03ee2388b44621

Verified source/callsite:
- P1 source declares and calls vcn_v2_0_cyan_pre_reset_only
- P1 begin/returned markers bracket that call
- helper symbol vcn_v2_0_cyan_pre_reset_only is retained in the full module
- vcn_v2_0_hw_init.cold contains a direct call to vcn_v2_0_cyan_pre_reset_only

Verified module contract:
- P1 begin/returned markers present
- CP02 markers present
- panic reference retained

Conclusion:
The previous STOP was only an incorrect symbol-name expectation in the audit script. The exact full module is accepted for CP02 packaging without rebuild.

Callsite audit log SHA-256:
ec09beb6c95100690349ca3afb177dc672a1d0e369b425d95035361a8c67d274
