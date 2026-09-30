# Latest September 30 report: independent re-evaluation

This review supersedes the earlier session's external-report emphasis. The new positive GPCNT and RBC observations materially change hypothesis priority. They are not treated as absent merely because the raw data have not yet been retrieved. Equally, reported outcomes are not relabeled as locally reproduced measurements.

## Evidence ledger

| Item | Evidence available here | Assessment |
|---|---|---|
| GPCNT rate follows both 800 and 1250 MHz requests | User's attributed Thomas report; exact raw count/time code not located | Strong reported positive activity; substantially demotes whole-domain VCLK absence |
| FREE_COUNTER stays zero in earlier trials | User's attributed earlier outcome; separate Linux register definition verified | Does not negate another counter's activity; no clock-source equivalence established |
| RBC packet fetch/execute works | User's attributed report; exact command/effect trace not supplied | Strong reported activity for that path, not automatically VCPU-master activity |
| Firmware accepted/staged and program bytes read back | Attributed external outcome in its modified experimental context | Demotes simple missing-host-staging or universally impossible acceptance explanations; does not prove VCPU-visible instruction bytes |
| Domain AXI-master enable reached; exposure/abort behavior improved; no ready | Attributed PhishMaster outcome; original RESULT/log/code not located | Demotes that one domain enable being the sole remaining barrier; effects require same-trial attribution |
| VCPU reset release readback | Attributed result | Weakens “that observed request bit remains asserted”; not all internal reset/isolation state |
| Status4, PC0, PRID0, absent marker/bootstrap store | Attributed negative observations; source labels and host status4 write verified | Missing expected outputs, not unique cause or proof of zero retired instructions |
| Harvesting3 before ABL0, discovery harvest0 | Attributed boot observation; separate namespaces verified in source | Early producer and physical scope remain unknown; numerical mismatch is not a contradiction by itself |
| Stock BIOS comparison | Planned external control, no outcome supplied | Cannot yet exclude the added-warm-reset hypothesis |
| Steam Deck ISP domain names/order | Attributed SmuV13Dxe analysis; image/hash/disassembly not supplied | Structural analogy only; BC250 mapping and order equivalence unverified |

An optional request for original public URLs was made. Bounded web searches for the exact GPCNT/PhishMaster/RSMU/SmuV13Dxe combinations did not locate the requested primary experiments. This is a search limitation, not evidence against the observations or proof that no public record exists.

## Counter meanings

`counter-results.json` verifies ten field definitions and nine distinct interfaces in the pinned VCN2.0 source. FREE_COUNTER is a separate 32-bit named field. PG indirect access has its own index/data pair; the reported GPCNT0/index2 association is not defined in those VCN2.0 headers. LMI monitoring includes STATE and event SEL fields with low/high count components; the event map and initiator specificity are not established here. Trace PC, trace DATA and PRID are separate fields, not interchangeable execution counters.

A newly pinned VCN4.0.5 header names GPCNT0 under `uvd_pg_indirect`. It is useful naming provenance, not permission to import its indices or behavior into BC250. In particular, field declaration order does not establish index2 or a VCLK clock source.

If independently timed fresh counter slopes track both requested frequencies, the associated clocked circuitry is active. That contradicts a model of complete clock absence for those captures. It does not independently establish delivery to the VCPU leaf, effective reset release, instruction fetch or retirement. FREE_COUNTER=0 cannot rescue the broader absent-clock model without a proven counter relationship.

Re-analysis of the existing measurements should retain raw counts and independent timestamps, declared counter width, sampling interval and any reset/wrap behavior. A displayed MHz value computed from the requested frequency would not be an independent measurement; this is a review criterion, not an allegation about Thomas's code. For a declared 32-bit counter, a full wrap is approximately5.37s at800MHz or3.44s at1.25GHz. Choosing an unknown number of wraps from the requested frequency would be circular. Those arithmetic values are not claims about the undocumented counter's actual width or divider.

## Reinterpreting the domain-master trial

The newly reported name `RSMU_SEC_AXI_MASTER_ENABLE_UVD` gives the earlier domain-master trial a more specific proposed meaning. Reaching its enabled readback, improved register exposure and removal of a reported target abort are compatible with a changed access path. They do not prove that every VCPU-originated instruction transaction is permitted or completes. Concurrent policy/power changes must not be silently attributed to a single field.

Most importantly, the reported enabled state coexists with no expected VCPU output. The hypothesis “this one domain-wide enable is the only remaining obstacle” is therefore substantially weakened. Repeating equivalent enable variants without a new discriminating observable has low value. A VCPU-specific permission hypothesis remains possible but has no supplied positive denial evidence; it should not become the default explanation simply because the broad enable explanation weakened.

## Steam Deck versus BC250 sequence

| Aspect | Steam Deck ISP report | BC250 report available here | Conclusion |
|---|---|---|---|
| Domain-relative naming | Cold reset, hard reset and PGFSM control/status identified by a debug printer | Same relative layout proposed for the VCN domain | Analogy; not an independently verified BC250 register contract |
| Order | PGFSM control, status poll, hard-reset deassert, cold-reset deassert | Power-up, external reset-related writes and later VCPU reset trials reported | No complete ordered same-boot trace supplied; sequence equality is unknown |
| Type13 loader reset-related write | Not the same loader/SoC | A write of1 to the proposed cold-reset field is reported | Conditional cold-reset-deassert interpretation if mapping/polarity are correct |
| Remaining core state | ISP example concerns another domain | VCPU-specific output remains absent | Outer-domain bring-up does not establish internal VCPU reset/fetch state |

Neither a missing reported step nor a naming analogy is proof of the cause. The exact BIOS image/SoC, debug-string association and matching disassembly would strengthen the semantic mapping. No domain-security or boot-patching procedure was derived or run.

## Newly public but different experiment

During the session, [Shalasere's September30 summary](https://github.com/Shalasere/bc250-vcn-research/blob/6c85b2fe382599ec80d6222b5ffe70eabb97457b/research/SESSION_SUMMARY_2026_09_30.md) and [corrections](https://github.com/Shalasere/bc250-vcn-research/blob/6c85b2fe382599ec80d6222b5ffe70eabb97457b/research/CORRECTIONS_2026_09_30.md) appeared at a new HEAD. They report host provisioning, a stable restricted driver configuration, failed VCN activity and corrected mailbox terminology. The summary itself contains quoted logs and interpretation; it is not the Thomas/PhishMaster GPCNT capture.

We do not accept its stronger claim that a prerequisite response identifies a particular secure policy, fuse or boot-only unlocking requirement. Nor does a hang establish a physical clock condition. Host copy/driver initialization does not demonstrate VCPU execution. These observations are useful in their own context and do not overturn the newer reported positive GPCNT/RBC activity on another setup. Procedures for bypassing security or probing undocumented requests were not reproduced or included in this checkpoint.

## Earlier local evidence

Older local nonzero PSP responses and guarded-out startup remain valid historical observations for those runs. They do not refute newer external acceptance in a different configuration. Conversely, newer acceptance does not retroactively change the old response or prove that the same saved file/path is now accepted locally. No additional live firmware request, boot change or register experiment was made.

## Harvesting priority update

Later user steering explicitly removes direct CC-clear variants from the main line. Reported writes from multiple contexts either fail to persist or revert; a mirror is compatible with this but is not proven. A causal VCPU-specific effect, a mirror of another state and unrelated availability metadata remain separate possibilities. Producer/source tracing stays low-cost and is shelved if it stops producing discriminating evidence.

The older R155 saved cached-sysfs record was rechecked: it lists instance0 only, version2.0.3 and harvest0. This corroborates a historical one-exposed-instance observation, not a universal physical absence of instance1 or an independent verification of Rukkus's record. The CC register's bits name MMSCH_DISABLE/UVD_DISABLE, not instance0/instance1. Current source can derive harvest display from software instance masks; an early standalone path can also return0 when state is unavailable. Exact display provenance is required before explaining a specific observation.
