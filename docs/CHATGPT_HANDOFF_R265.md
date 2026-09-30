# R251–R265 — What the new VCN evidence excludes, and what remains unknown

The latest report changes the assessment: **the reported two-frequency GPCNT activity substantially demotes whole-domain VCLK absence, and working RBC activity opposes a completely disconnected VCN block.** FREE_COUNTER=0 does not restore either explanation. The exact VCPU failure remains unknown; no single cause is selected.

This handoff supersedes the earlier R260 external-evidence emphasis. It incorporates independent counterevidence review, pinned normal Linux sources, the user-supplied Thomas/PhishMaster report and a newly public, different-context September30 writeup. No new device experiment, firmware load, boot change or VCN execution was performed locally. Q36 activity was GPU compute for advisory review.

## Confirmed

The following are **source-confirmed**, not newly measured BC250 states:

| Interface | Verified source contract | Missing physical contract |
|---|---|---|
| `UVD_FREE_COUNTER_REG` | Separate named32-bit FREE_COUNTER field | Clock source, enable/reset behavior and meaning of zero |
| PG indirect index/data | Separate indirect interface; six-bit index field | VCN2.0 GPCNT0/index2 mapping and clock source |
| LMI perf monitor | STATE and event SEL fields; low32/high16 count components | Event meanings, initiator attribution and zero-count interpretation |
| VCPU trace PC / trace DATA | Distinct28-bit PC and32-bit DATA labels | Sampling, freshness and retirement semantics |
| VCPU PRID | Separate16-bit identity field | An expected nonzero value or execution-heartbeat meaning |

The pinned VCN2.0 headers do not define GPCNT0's reported index2 mapping. A separately pinned VCN4.0.5 header names GPCNT0 under `uvd_pg_indirect`; that corroborates the namespace, not its mapping or behavior on BC250. The exact source checks are in [counter-results.json](../research/r265/counter-results.json).

Normal VCN2 source distinguishes clock-enable requests, VCPU reset requests, status ready mask2 and host-written busy mask4. Normal ready polling precedes final RBC setup, while DPG follows another path. Successful normal idle shutdown clears clock enable, asserts VCPU reset and clears status. Thus phase matters. The detailed [R260 startup handoff](CHATGPT_HANDOFF_R260.md) and [extension findings](../research/r265/EXTENSION_FINDINGS.md) retain the source witnesses and conditional lifecycle/test-return findings.

CC harvesting register fields, software instance-harvest bits and whole-IP masks are different namespaces. In the VCN2.0 header, bit0 is MMSCH_DISABLE and bit1 is UVD_DISABLE, not VCN0/VCN1. Linux field names alone establish neither complete physical isolation nor a VCPU-specific fuse effect.

The saved September9 R155 cached-sysfs record contains one entry: instance0, version2.0.3, harvest display0. It supports the prior one-exposed-instance observation; it does not establish a universal physical instance count or independently verify Rukkus's particular capture. Current source derives ordinary VCN harvest display from an instance mask and can return zero in an early display path without device state. The latter is not retroactively assigned to the old capture. See [discovery-results.json](../research/r265/discovery-results.json).

Sources are pinned to [Linux551c722](https://github.com/torvalds/linux/commit/551c722f40809618230001baccf219193e22fc5a), with six release samples and five reset-generation comparisons. The manifests identify reference files, not a currently loaded external module.

## Strong evidence

These are **strong attributed external observations**, pending access to their original code/raw captures; their positive evidential weight is retained:

- GPCNT increment rate reportedly follows800MHz and1.25GHz requests. Valid fresh counts measured against an independent time base contradict complete inactivity of the associated clocked circuitry. They do not alone establish the VCPU leaf clock, effective reset or instruction fetch.
- Reported RBC packet fetch/execute establishes activity in the tested path, much stronger than host pointer or register readback. It does not automatically identify the VCPU as the executing agent or validate its separate instruction path.
- Reported firmware acceptance, staging, enabled domain-master state, improved exposure/abort behavior and power-up materially weaken broad missing-provisioning or whole-domain-inaccessible explanations. Successful host staging/readback still differs from VCPU-visible executable bytes.
- Reported soft-reset-release readback weakens the narrow claim that that observed request bit remains asserted. It does not measure all internal reset or isolation signals.

The new semantic attribution for the earlier domain-master trial is useful: the enabled state reportedly coexists with no expected VCPU output. Therefore treating that one enable as the sole remaining obstacle is no longer a productive default. Possible VCPU-specific permission issues require their own evidence; no positive permission-denial record has been supplied.

The [latest external review](../research/r265/LATEST_EXTERNAL_REVIEW.md) separates each reported experiment from source facts and explains why older local failed loads cannot disprove newer acceptance under different conditions. A new public Shalasere writeup was inspected at commit6c85b2f; it concerns a different setup and is not the Thomas GPCNT capture. Its stronger causal claims from hangs/prerequisite responses are not adopted.

## Still unknown

**The physical cause is currently indeterminate.** Expected VCPU outputs have not been observed through the reported interfaces. That is narrower and more defensible than claiming no instruction was ever fetched or retired: zero PC/PRID and absent stores require valid sampling, source selection and memory visibility before supporting that stronger conclusion.

The candidates remain unranked by causal confidence. Work priority follows the user's instruction: fetch boundary, VCPU-specific reset/isolation, bootstrap source, cache/LMI/AXI path, permission evidence, stock-BIOS control, then low-cost harvesting producer review. Direct harvesting-clear trials are outside the main line. The candidates are:

| Candidate | Current limit |
|---|---|
| A. VCPU-specific reset/isolation | No validated effective internal-state observation |
| B. Instruction fetch path | No attributed VCPU first-read address/completion/visible bytes |
| C. VCPU-specific permission | No decoded VCPU-specific denial; domain enable alone is insufficient |
| D. Reset vector/bootstrap selection | Effective first-fetch source not established |
| E. Harvesting-related effect | Low-priority static work; causal effect, mirror of another state and unrelated availability indication all remain possible |
| F. Boot-time latch/PSP/SMU policy | A concrete sampled-once state and its producer have not been identified |
| G. MeiMeiV3 added warm-reset effect | Matched stock-BIOS control result is pending |

The [hypothesis matrix](../research/r265/HYPOTHESES.md) separately records **Supporting evidence, Contradicting evidence, Unknown, Next discriminating evidence A/B, and how the observations would be explained if the hypothesis were wrong**, for every candidate.

The reported Steam Deck ISP sequence is PGFSM configuration/status confirmation followed by hard- and cold-reset deassertion. Its proposed domain-relative names are a structural clue. The exact BIOS/SoC/disassembly and a complete ordered BC250 same-boot trace are missing, so BC250 semantic equivalence and sequence equivalence are unknown. The type13 loader's reported write can be interpreted as cold-reset deassertion only conditionally on the mapping/polarity.

Reported writes that do not persist are compatible with a mirror or restoration mechanism, but also with other write-path/lock behavior. They do not identify the source of truth. No direct-clear variants were run. If this static branch produces no new discriminator over days, it should be shelved instead of delaying VCPU work.

The pre-ABL harvesting producer is still unknown. An already-set value at ABL0 entry does not identify Boot ROM, PSP BL, SMU, a fuse load or a particular earlier function. No new producer was established in this interval.

## Contradicted / deprioritized hypotheses

| Hypothesis or inference | Revised assessment |
|---|---|
| Physical VCLK is absent throughout the domain | **Substantially deprioritized now; contradicted for validated independently timed GPCNT captures** |
| FREE_COUNTER=0 proves no VCLK | Unsupported counter equivalence; reject the inference |
| VCN is completely physically disconnected/inactive | Strongly opposed by reported RBC and GPCNT activity in those configurations |
| The one domain-wide AXI-master enable is the sole remaining obstacle | Substantially weakened by enabled readback/access progress without VCPU outputs |
| Firmware can never be accepted, based on an older failed local load | Not portable across contexts; newer reported acceptance requires revising the universal claim |
| Readback proves physical activity or instruction fetch | Reject the inference |
| Status4, PC0 or missing marker identifies one cause | Reject the inference; multiple mechanisms and observation failures remain compatible |
| A generic prerequisite response proves a particular fuse/security gate or boot-only latch | Not established without matching implementation evidence |
| MeiMeiV3 warm reset is already excluded | Premature; stock control is pending |

The remaining leaf-clock/reset/fetch candidates are not a way to preserve the disproven broad clock model. They are narrower, separately testable possibilities and should receive no causal status without new discriminating evidence.

## Best discriminating next experiments

Prefer re-analysis of existing records and the already planned ordinary stock-BIOS control. These are **outcome criteria, not device-write or bypass procedures**:

1. **Attribute already-recorded instruction transactions or validated execution observations.** A: a VCPU-originated read completes with expected bytes—exclude total fetch blockage for that address/time; a validated retirement observation excludes continuous reset over that interval. B: an attributable error identifies a narrower transaction class; absent requests alone still leaves reset, leaf clock, vector and observation validity open.
2. **Reconstruct the two GPCNT rates from original code and counts/timestamps.** A: independent slopes track both settings with valid counter identity/wrap handling—exclude whole-domain clock absence for those runs. B: the rates cannot be independently reconstructed—keep the result attributed; do not conclude that the clock is absent. Neither outcome establishes the VCPU leaf clock.
3. **Compare matched stock and MeiMeiV3 observations.** Preserve source/module/firmware, reset history and phase, and compare GPCNT, status, PC/PRID, RBC effect, outer reset/domain-master fields, PGFSM and CC harvesting. A: same failure pattern without the additional reset—demote its necessity as a cause. B: reproducible VCPU difference—establish BIOS/history dependence, not uniquely warm reset because other BIOS changes remain confounders.
4. **Compare existing ordered reset records and domain-name provenance.** A: the same validated semantic sequence is already present—deprioritize a simple missing outer-reset step. B: a genuine difference is found—record a candidate mismatch, not a cause, until a matched ordinary control discriminates it.
5. **Low-priority static check of harvesting against existing compatible working records or authoritative semantic evidence.** A: VCPU works with the same validated CC value—reject “that value invariably disables VCPU.” B: a specification or matching implementation explicitly connects it to a VCPU inhibit—support that narrower mechanism. Cross-board correlation alone does not isolate it. Do not perform direct-clear variants or delay fetch-boundary work for this branch.

Do not add another same-direction variant unless its A/B outcomes remove or materially demote a named hypothesis. A further “not ready” result without a new discriminator has low value.

Research progressed through **R251–R265**. [Public replay](../research/r265/REPLAY.md) reproduces pinned source and offline checks, including the counter distinction. The source/synthetic counts overlap and do not represent hardware trials. R249 remains a separate CPU checkpoint and R250 remains unfinished advisory work. No live VCN success is claimed.
