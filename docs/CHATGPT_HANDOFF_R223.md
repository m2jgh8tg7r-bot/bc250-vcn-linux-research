# R223 — Disambiguate saved PSP directory type 0x13

STAGE=R223
RESULT=PROVEN_STATICALLY_DISAMBIGUATED
STATIC_OR_LIVE=STATIC
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=The saved type-0x13 body contains debug-unlock module strings; its body digest matches the PS1 header
REJECTED=Treating directory type 0x13 as the external VCN `fw_type 13` solely because the numbers match
UNPROVEN=Exact format mapping, runtime selection, VCN firmware identity, PSP AUTOLOAD registration, VCN execution
NEXT=Recover type-to-fw-type mapping from PSP directory/loader metadata and compare t02/t28 records

## Static result

The saved P3 ROM directory entry index 5 is type `0x13`, container offset `0x97f900`, size `0x2000`. Its PS1 header describes a signed, unencrypted, uncompressed body of `0x1e00` bytes, version `0x291c0001`. Body SHA-256 is `413fcd1f3e87a7afc3c6ce28f4be550d79d04d182d3fd376e9726382de876654`, and it exactly matches the digest stored at header offset `0xd0`.

The body contains the following printable strings:

```text
DBG_UNLOCK_MODULE::FAIL - Svc_GetDebugUnlockInfo Status =
DBG_UNLOCK_MODULE::Received UnlockMode =
DBG_UNLOCK_MODULE::FAIL - UnlockNegotiation with HdtError =
DBG_UNLOCK_MODULE::FAIL - SecureUnlock with HdtError =
DBG_UNLOCK_MODULE::Securely UNLOCKED
DBG_UNLOCK_MODULE::FAIL - Failed to Lock ASIC
```

The body begins with ARM code and is not a zero template. These strings make it a strong debug/secure-unlock candidate. They do not identify it as VCN firmware. The external reports' `fw_type 13` may use a separate PSP command enumeration, so the previous R222 numeric match is downgraded to a lead only.

No hardware access, firmware replacement, PSP patch, SMU thunk, or direct-load test was performed.

## Relation to external reports

R220 remains valid: external reports put priority on PSP AUTOLOAD/t02/t28 registration and root clamp release. R223 narrows the saved-image search by showing that the obvious directory type `0x13` is likely a debug-unlock payload rather than the VCN payload described externally. This is a correction of interpretation, not a rejection of the external reports.

## Sources

- [R220 external audit](../handoffs/BC250_VCN_handoff_CANONICAL_R220.md)
- [R222 type-0x13 candidate](../handoffs/BC250_VCN_handoff_CANONICAL_R222.md)
- [R218 TOS/load analysis](../handoffs/BC250_VCN_handoff_CANONICAL_R218.md)
