# R240 — signer metadata across retained VCN history

The 21 already-retained R184 Navi10 VCN versions (2019–2026) were rechecked with the original offline bounds/CRC/hash verifier. All 21 payloads are distinct, but the R233 signer metadata field is the same `c37290c310e64a62b027c56695492368` in every one. None matches the records in the ten saved KDB occurrences (two distinct KDB bodies). This broadens the metadata result beyond the two VCN versions previously tried live.

This does **not** prove that all 21 versions fail on hardware, that the live KDB equals the saved candidates, or that the signer is the only compatibility condition. It does show that selecting an older version from this particular retained path history does not change this signer field or produce a new saved-key membership result. No new candidate was installed or executed.

Official main `9b858e5bb58d7bf1fc4d8818cb9100aed6d46f6a` still reports identical SHA-256 and size for Navi10/12/14 VCN filenames, matching the retained latest file. This was checked using HEAD metadata only; no new firmware body was downloaded. The 21-version coverage is the saved R184 path history, not a new claim of exhaustive all-branch/all-vendor firmware coverage.

The VCN metadata layout is distinct from R237's control `$PS1` containers. The control parser was deliberately not applied to it; the successful checks here are whole-file/payload integrity and bounded metadata comparisons, not inner container signature validation.
