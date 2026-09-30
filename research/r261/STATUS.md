# R261 — Ring tests, fence completion and execution attribution

STAGE=R261
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=pinned test, submission, fence and debugfs source
HARDWARE_ACCESS=none by audit; separate advisory Q36 GPU compute
HARDWARE_MUTATION=none
PROVEN=18 source witnesses and bounded complete-function absence checks
UNPROVEN=an actual false-positive test; execution ownership of ring commands; VCPU or codec execution
NEXT=connect observation phase to the normal idle/stop lifecycle

The normal decode and encode IB tests create/destroy a session and map a positive fence-wait return to zero. Their complete bodies do not query fence completion error status. The inspected direct-submission path returns an AMDGPU fence; its operations do not install a custom wait. The default wait returns a positive value for an already-signaled fence with a nonnegative timeout, independently of the fence's completion-error field.

Consequently, an already-signaled error fence with a positive timeout is a source-level counterexample to equating test return0 with error-free completion. The driver has a separate software force-completion path that assigns errors and processes the latest sequence. This audit does not establish that it ran during any VCN test, reproduce a false positive, or classify the diagnostic limitation as an observed defect. The separate status-query API has different semantics from the wait API.

The decode IB test waits on the returned destroy-message fence; create submission does not return a caller fence. This is not a decoded-frame comparison or an explicit firmware-response validation. It also does not reveal which hardware/firmware agent owns each command's implementation. A source-backed test result is stronger evidence than a host pointer change, but its exact contract and completion provenance still matter.

Additional attribution details:

- The decode write-pointer getter returns CPU shadow memory in doorbell mode; it uses MMIO in the other branch.
- The VF scratch-test path returns0 without performing the test. The ring helper assigns scheduler readiness from that return, so readiness is not an independent measurement.
- Aggregate IB testing skips rings that are not ready or lack a test callback. An aggregate result alone does not show which VCN test ran. Actual failures of tested nonprimary rings are retained in the aggregate return; no contrary claim is made.
- Reading fence debug information invokes fence processing before printing. That can signal existing driver fence state; it is not an observationally inert read or independent proof of firmware execution.

No recovery, fault injection, device access, firmware request or diagnostic reproduction was performed. The examples are conditional source reasoning, not hardware trials. Source paths, hashes and witnesses are in `results.json`.
