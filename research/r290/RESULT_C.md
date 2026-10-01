# R290-C result — PSP response/state preservation audit

Date: 2026-10-01

Candidate psp.c SHA256:
1362359681f2a128ad655c8493793a01db6fe8cf513471888fce63a588e38e26

Audit script SHA256:
b9785149dcd92a61a74cd281d58b4355184d82e20170321870486d261bc6bdaa

Audit log SHA256:
b2e364434120e1fc79d19d9cb0c6a2c5284a5c3887c6fa26ebc51e9458bba50c

Key static proofs:
- generic PSP response is copied before nonzero status rejection
- nonzero PSP status returns -EINVAL
- bc250_psp_load_ip_fw copies response to caller even on error
- no early return loses the response
- isolated VCN probe records PspStatus and TmrAddress after the call
- CommandsDone is set to 1
- result is propagated after diagnostics are recorded
- failed VCN probe does not clear Loaded, RingUp or TmrUp
- failed VCN probe does not unload TMR or stop PSP ring
- normal E10 LOAD remains byte-identical
- existing Loaded assignments remain unchanged
- VCN file is freed and staging mapping is unmapped
- overall escape status remains REFUSED on nonzero result while detailed response fields remain available

Expected modeled 0xffff0008 semantics:
- fence completes
- PSP response status = 0xffff0008
- generic return = -EINVAL
- probe PspStatus preserved
- probe TmrAddress preserved
- CommandsDone = 1
- overall escape status = REFUSED
- normal PSP loaded state retained

R290_C_RESPONSE_PATH=PASS
NO_BUILD=YES
NO_HARDWARE_ACCESS=YES
NO_WINDOWS_REQUIRED=YES
