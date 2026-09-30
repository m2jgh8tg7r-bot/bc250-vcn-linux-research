# R266 — Shalasere fixed external baseline

Shalasere/bc250-vcn-research is registered as a fixed, board-specific comparison baseline, not a feed to monitor routinely. Researcher departure is user-supplied context, not independently verified. New Thomas/PhishMaster/Rukkus observations are compared against the recorded Shalasere configuration, not judged by whether they preserve its conclusions.

Pinned final commit: [6c85b2fe382599ec80d6222b5ffe70eabb97457b](https://github.com/Shalasere/bc250-vcn-research/commit/6c85b2fe382599ec80d6222b5ffe70eabb97457b). Its immediate parent is independently confirmed as [b09ef6ffd1730832066e7582ce7f36c25709f2b0](https://github.com/Shalasere/bc250-vcn-research/commit/b09ef6ffd1730832066e7582ce7f36c25709f2b0). Nine selected original documents across these revisions, commit metadata and tree inventories are preserved locally with hashes. Original documents are not republished wholesale; implementation files are indexed by immutable Git blob identities, not installed, modified or executed.

Precedence: [CORRECTIONS](https://github.com/Shalasere/bc250-vcn-research/blob/6c85b2fe382599ec80d6222b5ffe70eabb97457b/research/CORRECTIONS_2026_09_30.md) overrides conflicting text in the [September30 summary](https://github.com/Shalasere/bc250-vcn-research/blob/6c85b2fe382599ec80d6222b5ffe70eabb97457b/research/SESSION_SUMMARY_2026_09_30.md) and [README](https://github.com/Shalasere/bc250-vcn-research/blob/6c85b2fe382599ec80d6222b5ffe70eabb97457b/README.md). Even after correction, causal claims are evaluated separately from reported measurements.

## 1. Findings incorporated and their evidence level

- **Independently source-confirmed:** the normal driver naming fallback yields `vcn_2_0_3.bin` for VCN2.0.3. The Cyan GC/SDMA legacy names do not supply a VCN legacy name. `cyan_skillfish2_vcn.bin` is the superseded name.
- **Confirmed as a pinned external result, not locally reproduced:** Shalasere reports driver-managed firmware provisioning and amdgpu reaching device-node availability without the VCN PSP load request. This is retained as an existing host-provisioning implementation/reference asset. PSP loading must not be treated as the only source path.
- **Boundary of that result:** host provisioning, configuration code and `/dev/dri` availability do not prove VCPU instruction fetch, accepted executable bytes at the VCPU, successful live cache programming in every variant, or codec operation. The summary itself distinguishes restricted working configurations from later access hangs. Do not merge all variant outcomes into one successful full initialization trace.
- **Strong external handler evidence:** IDs reported as PowerUpVcn produce prerequisite rejection rather than unknown-command responses on that board. The baseline records recognized/prerequisite-rejected PowerUpVcn behavior. Exact handler-body identity and the rejecting predicate were not independently traced here; generic pre-dispatch checks are not excluded solely by response codes.
- **Correction adopted:** transports and address pairs are not interchangeable merely because community labels use Q0/Q3. The observed response subset strongly suggests shared handler space; complete dispatch-table identity or physical mailbox aliasing is not independently established.
- **Firmware provenance:** Shalasere reports an unowned manually placed file in its specific package environment. Canonical origin remains unknown. File size/header consistency is not authenticity verification; do not repeat the original implication that header appearance proves a genuine signed image or claim package absence for every distribution/version.
- **Reference recognition:** the pinned README explicitly lists our repository as “Linux enablement side — firmware/ring/doorbell staging.” This confirms external citation/recognition, not independent reproduction or validation of all our findings.

## 2. Findings restricted to Shalasere's board/configuration

The reported prerequisite responses, access hangs, three equal mirror-like values, unsuccessful writes and extensive negative trials belong to the observed board, firmware, BIOS and transports. They are not impossibility proofs for all BC250 devices.

The three reported values `0x10C6` and CC harvesting3 provide strong board-specific evidence of a persistent disable-associated configuration. Shalasere interprets it as UVD_DISABLE/fuse evidence. We preserve that interpretation as a strong external board-specific hypothesis, while distinguishing it from independently proven OTP fuse identity: the SMN locations' semantic identification comes from an external tip, and equal bit positions across unrelated registers do not establish equal meaning. Identical values likewise do not by themselves prove a hardware mirror relationship.

Possible prerequisites remain parallel: BIOS-init policy, fuse/configuration state, internal SMU state, early boot configuration and security policy. Neither the response nor readback establishes that one BIOS flag is sufficient, or that the decision is necessarily boot-only.

## 3. Agreement with our existing work

R255 already separates normal PSP placement from driver-backed cache allocation. The external provisioning result adds a board-reported implementation outcome to that source distinction; it does not replace the historical local failed PSP response. Firmware name/geometry agrees with our saved-file/source analysis (file405952 bytes, payload405696, offset256); matching geometry alone does not establish identical firmware hashes.

R143/R252 identified missing Cyan power callbacks and success/no-op boundaries. R155/R192/R259 distinguish instance metadata, CC field names and power/execution. R265 separates clocks, counters, ring effects and VCPU output. The new baseline is compatible with these boundaries.

R265's caution about inferring a particular handler or boot-only policy from a prerequisite code is refined, not erased: we now explicitly retain the corrected board-reported recognized-handler evidence, while keeping exact dispatch identity and causal prerequisite unproven. Original R265 is a historical checkpoint; this R266 baseline controls future Shalasere references.

## 4. Cross-board comparison and tensions

Thomas entries below come from the user's attributed reports, not independently retrieved raw captures. `unknown` means the selected evidence does not establish the value; it is not zero or failure. Rows aggregate reports across dates and must not be read as a simultaneous same-boot capture.

| Observation | Shalasere fixed baseline | Thomas latest attributed report |
|---|---|---|
| CC_UVD_HARVESTING | 3 reported | 3 reported |
| SMN0x5d928 | 0x10C6 reported | unknown |
| SMN0x5d930 | 0x10C6 reported | unknown |
| SMN0x5d93C | 0x10C6 reported | unknown |
| PowerUpVcn0x2A/0x2B | 0xFD prerequisite rejection reported | unknown |
| PGFSM | Control value2 reported; successful matched power-up outcome unknown | Power-up reported; exact matched scalar record unknown |
| Physical VCLK | Counter-based rate evidence unknown; mailbox frequency replies are not such evidence | GPCNT rates reportedly track800/1250MHz |
| RBC packet execution | Independent successful packet effect unknown in selected final records | Packet fetch/execute reported |
| VCPU PC / PRID | Exact paired numeric values unknown in selected final records; VCPU described as silent | Both0 reported |
| VCPU firmware/custom-program execution | No successful execution reported | Expected marker/bootstrap stores not observed |
| Stock / modified BIOS | README describes P3 with cores unlocked; final trial-specific image/hash/reset history unknown | MeiMeiV3 reported; stock comparison planned, outcome unknown |
| Direct-load host provisioning | Successful restricted driver configuration reported; no VCPU execution proof | Same implementation/path use unknown |
| VCPU cache/register access | Configuration implementation/provisioning reported; simultaneous successful access tuple unknown | Access/readback reported |
| Firmware provenance | Manually placed vcn_2_0_3.bin; canonical origin unknown | Exact matching file/hash/origin unknown |

The tension is between broad interpretations of Shalasere's inactivity and Thomas's positive sub-block activity, not necessarily between incompatible raw observations. Board variation, BIOS/reset history, firmware, access method, operating phase or observation validity could explain differences. Physical per-board fuse variation is possible, not established merely by comparing these reports.

## 5. Negative-result registry: avoid equivalent retries

These categories are archived as failed/limited in Shalasere's reported campaign. They are not global impossibility proofs or validated causal mechanisms. This record does not reproduce exploit, security-bypass or undocumented-request procedures.

| Category | Reuse decision / boundary |
|---|---|
| Runtime TOCTOU, CCP host visibility, PSP SRAM access | Do not reopen equivalent exploitation paths; preserve historical negative scope only |
| APCB overflow-related constraints | Preserve as negative provenance; no reproduction or refinement |
| Direct harvesting clear | Outside the main research line; repeated nonpersistent writes do not identify a producer |
| Simple feature enabling or arbitrary PowerUpVcn arguments | No equivalent sweeps; rejected outcomes do not identify the prerequisite |
| Simple PGFSM host writes | No equivalent blind retries; unchanged readback is not a complete physical model |
| PSP firmware loading alone implies VCN starts | Reject sufficiency inference; acceptance/provisioning and execution are separate |
| Earlier universal software-exhaustion conclusions | Historical claims superseded in scope by later results; not mathematical proofs |

Reopening an ordinary non-exploit diagnostic question requires materially changed context or a new observation that discriminates named alternatives. Another identical failure is not new discrimination. Harvesting producer review remains low-cost background work; cause, mirror of another policy/state, partial/sub-block disable, per-board configuration and unrelated availability indication remain distinct alternatives.

## 6. Minimal cross-board comparison and outcomes

First seek existing saved read-only observations of the three named SMN locations on Thomas's board, retaining provenance, BIOS/reset history, firmware and phase alongside GPCNT/RBC/VCPU outputs. If new observation becomes appropriate, use an already validated acquisition path; no write, clear, request sweep or boot change is part of this import. Read-only is not a guarantee of harmless access: the fixed archive also reports read-related hangs, so arbitrary address-access commands are not supplied here.

- **Thomas differs with bit1 clear:** supports a configuration difference at those locations. If Thomas's VCPU remains inactive, it weakens bit1-set being a necessary explanation of all VCPU failures. It does not by itself prove different OTP fuse states; semantics, policy and transport still require attribution.
- **Thomas has the same values/bit1 set while GPCNT/RBC work:** opposes whole-domain inactivity tied invariably to that bit. **It does not refute VCPU-specific disable if both boards still lack VCPU execution.** That requires a working VCPU under the same validated state or independent semantic evidence.
- **Thomas VCPU executes with the same validated bit state:** rejects that state invariably preventing VCPU execution in those conditions.
- **Invalid, inaccessible or mismatched observation:** inconclusive; never convert missing/zero data to a fuse conclusion.

These criteria avoid equating a useful cross-board discriminator with a guaranteed fuse diagnosis. They also avoid attributing stock-versus-modified BIOS differences uniquely to warm reset without controlling other image differences.

## 7. Most important unresolved boundary

On configurations with reported power, physical clock activity and RBC operation, the missing expected VCPU outputs remain unexplained. First-fetch address/completion, VCPU-specific reset/isolation, bootstrap source, memory-path visibility and permission evidence remain the priority. “No expected output observed” is still not a proven absence of every instruction fetch or retirement.

The archived Shalasere baseline prevents rediscovering old paths and preserves a useful provisioning asset. It neither dictates the cause on Thomas's board nor collapses all boards into one theory. Further active work follows new Thomas/PhishMaster/Rukkus and local evidence. No hardware action was performed for R266.
