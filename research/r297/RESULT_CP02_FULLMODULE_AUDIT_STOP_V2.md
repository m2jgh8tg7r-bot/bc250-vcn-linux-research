# R297 CP02 full-module build audit stop

Date: 2026-10-02
Status: BUILD PASS / AUDIT STOP

MAKE_RC=0.

Module SHA-256:
1e40f5e6a81a6cb95445970876c7ceb9afd5ada328803945e930b448a76fa452

Build ID:
640cca014583a8f2c807fb2d7a03ee2388b44621

Required CP02, R274B, P1 begin/returned and R79 markers are present.
CP01 and obsolete markers are absent.
Lifecycle symbols and amdgpu_vcn_resume are present.

The script stopped only because nm did not show the exact helper symbol bc250_vcn_pre_reset_init. This is an audit/symbol-retention issue, not a compile failure.

Script exit code: 30.
