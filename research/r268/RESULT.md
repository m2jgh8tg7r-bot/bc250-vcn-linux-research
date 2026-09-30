# R268 — What ordinary driver observations cannot establish

This is a bounded clarification of R261/R262/R265, not another hardware discovery. Primary source is Linux commit `551c722f40809618230001baccf219193e22fc5a`; paths, line witnesses and whole-file hashes are in source-witnesses.json. No hardware transactions occurred.

## Confirmed

In vcn_v2_0.c, the normal interrupt callback dispatches three recognized source IDs to decoder/encoder fence processing. The default branch logs an unhandled source and data word. This callback does not validate the address, initiator or retirement of a VCPU first instruction.

The two UVD_LMI_STATUS references are stop-path waits. They use VCPU write-clean and aggregate read/write-clean masks, followed by UMC clean waits after an arbiter stall. Their use is a quiescence check; the source does not make these bits a historical instruction-read completion counter. A clean interface can be consistent both with completed work and with no work issued.

The VCN 2.0 header names PIF address-error and RBC register privilege-fault fields. A name and mask do not establish which address, transaction type, initiator, epoch or error propagation path produced a value. This driver does not use UVD_SYS_INT_STATUS or UVD_VCPU_INT_ACK. This bounded absence does not prove that firmware, another driver or hardware cannot observe those events.

## Strong evidence

The external GPCNT and RBC positive reports remain valuable and independent of these limitations. Ordinary fence dispatch and clean-bit names supply no independent corroboration of first instruction fetch. Existing external PC/PRID/marker negatives remain unresolved observations, rather than cause attribution.

## Still unknown

No instruction-fetch-specific transaction attribution or reset-vector specification was established from the audited source. In particular, PIF must not be expanded into an assumed VCPU instruction-fetch contract merely from its name. Read/ack side effects and a safe acquisition path were not established here.

## Contradicted / deprioritized hypotheses

| Proposed inference | Why insufficient | If the inference is wrong |
|---|---|---|
| Clean LMI proves firmware was fetched | Stop-path quiescence is not a historical read count | No instruction request was issued, or traffic completed elsewhere |
| An interrupt proves VCPU execution | Callback dispatches fence processing, without instruction attribution | A distinct source can generate a completion-related interrupt |
| PIF fault proves VCPU permission denial | Field lacks source/address/transaction attribution here | Other traffic or another error class produced the event |
| No logged fault excludes blocked fetch | Coverage, masking and propagation are unknown | The failure never reaches the observed reporting point |

These reject implications, not the existence of the underlying candidate causes.

## Best discriminating next experiments

Prefer analysis of an existing, independently validated trace over adding register reads whose semantics are unknown. A useful trace would establish boot/trial identity, the request initiator, transaction type, address range, request occurrence, and response/completion status. Instrumentation coverage must have a positive control.

- A validated VCPU instruction-read request at the expected firmware source would contradict inability to emit that request at that observed instant in the identified boot/reset epoch. It cannot exclude request absence during another failing startup interval. It would not prove completion or execution, and it would not exclude a later reset.
- A validated successful response would demote a complete upstream transport blockage for that request. Correct returned bytes, instruction-cache consumption and retirement remain separate boundaries.
- An attributable denied response would support a permission-path failure for that request. It would not identify which policy producer caused it.
- No request observed excludes nothing unless coverage and the start interval are independently established. Even with coverage, absent requests leave reset, bootstrap and local gating alternatives.

No direct fault, ACK, security-policy or counter programming sequence is proposed. The current critical acquisition remains unprepared; offline analysis and standard-API preflight are prepared in R267.

## Independent counterevidence review

Accepted three clarifications: constrain positive evidence to the matching trial/time/reset epoch; require a positive control for the actual fetch observer, not merely DRM preflight; distinguish the local VA-API staging rule from a universal logical prerequisite. No broader hypothesis elimination or new hardware sequence followed from this review.
