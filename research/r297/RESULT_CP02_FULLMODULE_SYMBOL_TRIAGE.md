# R297 CP02 full-module symbol triage

Date: 2026-10-02
Status: PASS / prior audit condition corrected

The prior full-module audit stopped because it searched for a non-existent expected helper name:
bc250_vcn_pre_reset_init

The built module actually retains the P1 helper as:
vcn_v2_0_cyan_pre_reset_only

Evidence from nm/readelf:
- vcn_v2_0_cyan_pre_reset_only is present as a local function
- vcn_v2_0_hw_init is present
- amdgpu_vcn_resume is present
- P1 begin/returned strings are present
- R152 source restoration hashes are exact

Full module identity:
- SHA-256: 1e40f5e6a81a6cb95445970876c7ceb9afd5ada328803945e930b448a76fa452
- Build ID: 640cca014583a8f2c807fb2d7a03ee2388b44621

Conclusion:
The prior STOP was an audit-script symbol-name error, not a build or scientific failure. No rebuild is required solely for that STOP. A final focused callsite/disassembly audit should verify that the Cyan hw_init cold path calls vcn_v2_0_cyan_pre_reset_only, after which this exact module can be accepted for packaging.
