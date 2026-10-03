# R306 — Retained artifact identity and header-provenance boundary

The retained files match the recorded identities checked here. No artifact mismatch was found that explains the CP06/CP07 outcome. This is a static provenance result; it does not establish which instruction ran in a failed boot or the effective VCN state.

## Confirmed

The audit recomputed 26 recorded hashes: seven R305 access/base inputs, seven R304 comparison inputs and twelve CP07 build-manifest items. All 26 comparisons match; these are comparison rows, not 26 independent artifacts. This preserves the attribution of R304/R305 to those saved source files.

CP05 and CP06 signed package modules each exactly match their separately retained installed-module copies. CP07's retained signed module matches its package record; its retained image matches both the package image record and the historical installed-image record. The CP07 exact archive roundtrip remains a historical audited result, not a new extraction performed in R306. No current /boot file was read.

All three retained VCN objects use DWARF 5 with a filename table containing directory and name columns but no MD5 content column. None has a .debug_macro or .debug_macinfo section. These particular debug records do not provide a complete historical header-content or macro-expansion attestation.

## Strong evidence

The checked hashes and package/installed comparisons strengthen the continuity of the saved artifacts. They retain the prior distinction between CP05's observed post-write checkpoint and CP06/07's unresolved failed-boot execution. They do not supersede the original live classifications or imply that missing historical-header hashes invalidates CP05's observed markers.

## Still unknown

Complete transitive header/config/compiler-input identity at each historical build is not established by the inspected records. Current header hashes, debug filenames, a build log and a module Build ID are different evidence types. A source-restore guard in the retained CP07 build script covers its named source overlays; it is not a digest of every input. That script was read, not run.

Runtime base-table contents in the failed boots, the precise stopped instruction, device-side completion, power/clock/isolation state, VCPU execution and firmware ready remain unknown. Matching saved installation records is not proof of loaded bytes or runtime control flow in an unobserved failing boot.

## Contradicted / deprioritized hypotheses

| Hypothesis | Supporting evidence | Contradicting evidence | Unknown / if wrong | Next discriminator |
|---|---|---|---|---|
| A retained artifact mismatch explains the comparison | No mismatch identified | All checked hashes and the selected saved-module pairs match | Unchecked inputs or runtime selection remain separate; if wrong, equal artifacts can still encounter different hardware state | Inspect a concrete mismatching record if one appears; no rebuild or device retry follows from absent evidence |
| Current headers prove every historical build input | Current files match the R305 source manifest | No differing header content is demonstrated | The checked DWARF lacks content digests and macro records. Historical content can still have been identical; the proposed attestation is unsupported | A contemporaneous transitive input manifest, or a bounded compiled-code/table witness, can strengthen the specific claim |
| CP06/07 definitely stopped inside the STATUS read | Failure occurred in trials intended to include a read | No direct contradiction of a read stall is established | No returned-value or decisive same-boot boundary is established; the read may have stalled, but earlier failure or unobserved progress also fits | Attributable existing boundary evidence, not another unchanged failed read |

## Best next work

Inspect the retained compiled base-initialization table/code against the saved source, where available, to strengthen the bounded address-construction claim without asserting runtime execution. Then compare power/clock/isolation prerequisites against attributed saved external observations. Neither the matching artifacts nor the provenance gap justifies a new hardware trial.

For any future build already justified on other grounds, record transitive inputs before and after compilation and retain exact artifact/package identities. Do not rebuild solely to fill a historical record gap: a new build cannot retroactively attest to an old one.

`audit.py` replays only filesystem hashing and readelf over retained artifacts. It never invokes make, installs or loads a module, accesses device registers, or reads current boot files. `results.json` contains the checked identities and limits.

STAGE=R306
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=retained-file and ELF debug metadata audit
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=No new observation
PROVEN=26 recorded hashes match; CP05/06 saved installed modules match packages; CP07 saved image/module records agree
REJECTED=Current headers or DWARF filenames alone attest all historical inputs; saved artifact match establishes failed-boot control flow
UNPROVEN=Complete historical header provenance, failed-boot runtime state, precise stop location and VCPU execution
NEXT=Bounded compiled base-initialization witness and saved prerequisite comparison; no live trial

Counterevidence review: comparison-row counts are not independent-artifact counts; missing DWARF content hashes do not demonstrate differing headers; missing failed-boot markers do not refute a read stall. CP05 live evidence is preserved.
