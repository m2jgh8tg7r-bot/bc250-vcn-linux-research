# R269 — Separate write protection, disable state and first-fetch evidence

This update supersedes the fuse-semantic interpretation in R266, while preserving Shalasere's fixed original archive. Thomas's new statements are user-relayed external reports; original field definitions, extraction code and raw records have not been supplied. No new hardware operation was performed.

## Confirmed

The pinned Linux VCN 2.0 header defines `CC_UVD_HARVESTING.UVD_DISABLE` at bit 1. This establishes a name and mask in that register namespace. It does **not** define bit 1 at any of the three SMN locations.

Shalasere's fixed final documents report three equal values and infer a fuse connection using an externally supplied semantic identification plus the shared bit position. The inference is conditional. Neither equality nor matching bit numbers proves a hardware mirror or shared field meaning.

**Correction:** the three reported values remain attributed observations. Their interpretation as the board's actual UVD-disable fuse is **Strong hypothesis / unresolved fuse-field mapping**, never Confirmed. R266 already qualified the OTP interpretation, but its phrase “persistent disable-associated configuration” was too strong: the association itself has not been independently mapped.

## Strong evidence

The earlier externally reported GPCNT/RBC activity still weighs strongly against whole-domain inactivity. The new report separates a write-protection field from a disabled-state field. That distinction is logically important, but its BC-250 field mapping and reported values require primary verification.

A write-protection control can prevent modification of a disabled-state control without requiring that disabled-state control to be asserted. This is a logical possibility, not a verified BC-250 register specification. Conversely, reported disable=0 would not by itself establish effective VCPU enable, reset release or instruction issue.

## Still unknown: five separate namespaces

| Item | Current evidence | What remains unproven |
|---|---|---|
| `uvd_uvd_write_disable` | Thomas reports set and interprets it as write protection; OTP is his hypothesis | Exact source, bit extraction, silicon applicability, protected target, polarity, OTP origin |
| `uvd_uvd_disable` | Thomas reports 0, interpreted as enabled-side value | Exact source/mapping, whether same trial, relation to effective VCPU state |
| `CC_UVD_HARVESTING.UVD_DISABLE` | Linux VCN 2.0 names bit 1; live value 3 is externally reported | Physical source, causal effect, producer, any link to the two fields above |
| SMN `0x5d928/0x5d930/0x5d93c` | Shalasere reports each `0x10c6` | Whether mirrors; meaning of each bit; no automatic association with either Thomas field |
| IP discovery `harvest=0` | Exposed metadata documented separately in R265/R266 | No specification equating it to live harvesting, write protection, OTP or effective enable |

Treat these as separate observations until a mapping is established. That is not a claim that the underlying physical states are mutually independent. In particular, Thomas's update does **not** establish that bit 1 of Shalasere's SMN values is the write-disable field instead.

Exact-name web/GitHub searches and the retained Linux AMD headers did not locate primary definitions for the two `uvd_uvd_*` names. This bounded search failure leaves the mapping unknown; it does not disprove the names or Thomas's account. Original field-map provenance is the highest-value missing static input.

## VCPU start boundary: positive evidence by stage

This is an analytical decomposition, not a claimed hardware sequencing specification. The real microarchitecture can overlap stages, gate subtrees or stall between them.

| Boundary | Positive evidence currently available | Residual question |
|---|---|---|
| Clock | External GPCNT slope tracks two VCLK settings | Which clock node/tick source is measured? Is the VCPU leaf clock effective? |
| Core enable | Configuration/readback reported | No independent evidence that the core can issue instructions; no separately identified enable control is assumed |
| Reset release | VCPU soft-reset request/readback reportedly released | Effective internal reset/isolation state and epoch remain unknown |
| Bootstrap/vector selection | Program backing bytes and cache configuration reportedly readable | Selected first-fetch source/vector and visibility to core unknown |
| First fetch request | No attributable positive record supplied | A request may be absent, unobserved, stalled or followed by later failure |
| LMI/cache/fabric | RBC activity and host/cache-register access reported | VCPU instruction-master requests and responses not established |
| Backing memory | Firmware/program staging readback reported | Bytes returned to the VCPU and eventual retirement remain unproven |

The reported GPCNT clock-activity evidence and RBC positives must not be promoted to evidence that the VCPU core is instruction-issue capable.

## Normal-driver boundary witness

The non-DPG `vcn_v2_0_start` source calls its VCPU reset transition a boot release. Memory/cache setup precedes it; further LMI channel/reset setup and the ready poll follow. This supplies the ordinary software expectation, not a silicon contract that one bit guarantees fetch.

A particularly relevant name trap is `UVD_MASTINT_EN.VCPU_EN`: the source explicitly disables it as master-interrupt control before boot/ready polling, then enables it after the ready check. It must not be relabeled as the missing generic VCPU-core enable solely because its field name contains VCPU_EN. This source path expects startup status without that interrupt enable being asserted. It does not establish every BC-250 effective enable dependency.

`start-boundary-source.json` records pinned line witnesses and source hash; `audit_start_boundary.py` verifies the bounded source order. The initial lexical-count expectation was corrected from four to three references after inspecting one disable mask and the enable value/mask pair; this was an audit-script correction, not a hardware finding. No register trial follows from it.

## Fault observation and competing interpretations

Thomas reports no increments at known VCN fault observation points. Exact addresses, event definitions, enable/mask state, reset behavior, acquisition code and same-trial timing remain unknown. The result is a negative observation. It cannot yet distinguish no request from a request that stalls, succeeds, is dropped, is not covered, or fails without reaching those counters.

| Hypothesis | Supporting evidence | Contradicting evidence | Unknown | Next discriminating evidence; if wrong |
|---|---|---|---|---|
| No first request emitted during the relevant start interval | Missing attributed execution outputs and no observed fault are compatible | No positive first-request witness supplied; none established as contradiction | Observer coverage, effective core/reset/bootstrap state | A matched attributable request contradicts absence at that instant. If absent with validated, complete coverage of request emission itself throughout the target start epoch, localize before request emission without choosing reset versus bootstrap; fault-monitor coverage alone is insufficient. If wrong, invisible/stalled/later-failing requests explain negatives. |
| Request emitted but fetch path fails | Staging/RBC do not prove instruction-master response | No fault increment is weakly adverse only if that fault path is known to cover the failure class | Request identity, response class, event visibility | A matched failed response supports the relevant path. A successful read demotes a total block for that request, not later failures. If wrong, no request or a later execution stall explains outputs. |
| Actual UVD-disable fuse is asserted on Shalasere's board | External interpretation of persistent values and inactivity | No direct contradictory observation on Shalasere's board is established; Thomas's other-board value is not one | Actual disable/write-disable maps, per-board applicability and semantic meaning of the shared bit position | A validated read-only field decode distinguishes asserted disable from asserted write protection. If wrong, the observed words can represent another configuration while an independent start failure remains. |

**Priority:** investigate the conditions for first-request emission before adding more downstream fault or harvesting variants. This is a work-order decision. Without fault-detector coverage/sensitivity, no quantitative or categorical likelihood ordering between “no request” and “unobserved request failure” follows from zero faults alone.

## Contradicted / deprioritized hypotheses

- Write-disable set implies UVD itself disabled: unsupported implication.
- Bit 1 in the CC register defines bit 1 in the SMN words: unsupported namespace substitution.
- Equal words prove mirrors or OTP: unsupported inference.
- VCLK running implies VCPU instruction issue: unsupported implication.
- Zero faults proves no fetch requests: unsupported without coverage.

## Best discriminating next evidence

1. Original definition/extraction source for both `uvd_uvd_*` fields: exact revision, target SoC, container register/structure, bit range and meaning. Compare definitions before comparing values. No new writes are needed.
2. Existing same-trial values for both named fields and the three separate SMN locations, retaining provenance. Different values identify a recorded state difference before they identify a fuse difference.
3. Fault-observer definition and a positive-control record proving detection of the relevant instruction-fetch failure class. Without this, keep the zero result as a visibility-limited observation.
4. Existing attributable first-request trace in the matching reset/start epoch. Request, response with intended bytes, instruction consumption and retirement are separate milestones.

Direct harvesting-clear trials remain outside the main line. This update does not prepare a new fuse access or boot modification.

## Counterevidence review disposition

Accepted: unmapped fields are an evidence gap, not direct contradiction; another board's disable value does not refute Shalasere's board state. GPCNT evidence does not establish a shared VCPU clock. Only validated coverage of request emission itself, not fault coverage, can support localization before request emission from an absent request.
