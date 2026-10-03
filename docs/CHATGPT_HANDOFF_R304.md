# R304 — checkpoint comparison and reduced experiment plan

Decision: defer the CP05 network repeat. Retain historical CP05 write-return/panic proof and R303 pre-MMIO receiver proof as separate observations. Their combination does not prove post-write network delivery in R303 conditions. This gap is acceptable for the present static research objective; it must be revisited if a future experiment specifically relies on post-write transport.

| Checkpoint | Reachable helper behavior before intentional panic | Saved live evidence | Remaining gap |
|---|---|---|---|
| CP04 / R303 | Guards, pre-MMIO marker; panic precedes helper MMIO | Receiver includes helper entry and guards_pass | Final panic/countdown delivery absent |
| Historical CP05 | Same guards, CONFIG write, post-write marker, panic | Ordered saved pstore includes write-return marker and Kernel panic | Physical power transition and current network delivery unproven |
| Historical CP06 | Same guards, CONFIG write, post-write marker, one STATUS read, value marker, panic | Blackout reported; no decisive persisted boundary | Instruction reached, returned value and cause unproven |
| Historical CP07 | Same guards, one STATUS read without CONFIG write, value marker, panic | Blackout reported; zero exposed pstore | Instruction reached, returned value and cause unproven |

Source inspection is scoped to vcn_v2_0_cyan_pre_reset_only. CP04/05/06 retain textual tails after unconditional panic; those tails are not evidence of reachable execution. Other register references elsewhere in each source are not helper transactions. This review supplements historical object/module audits and does not replace them with new binary attestation.

## What this changes

A CP05 repeat with network logging would qualify delivery after a previously observed write; it would not directly resolve physical power or STATUS-read behavior. A positive result retains the same unresolved cause candidates. A negative result introduces a new transport/boot-condition ambiguity rather than identifying the read. Therefore the repeat is useful only when post-write transport qualification becomes necessary for a specific next experiment, and is not mandatory now.

Do not infer that CP06/CP07 executed their reads from blackout or empty pstore. Do not label a single MMIO read safe because it has no write. A software polling timeout or panic timeout cannot guarantee recovery when the CPU is stalled inside a device access. Do not repeat the unchanged failed probes.

## Reduced next work

Continue saved-source analysis of register addressing and access dispatch for the exact retained CP05/06/07 variants. Compare direct/indirect paths and initialization preconditions against the fixed external baseline, using saved material. Record hypotheses separately from live facts. Prepare no image until a candidate answers a distinct question and has a concrete recovery and evidence plan.

Any future trial must state the hypothesis, changed variable, exact artifact identity, expected positive and negative observations, and interpretation of missing output. It must preserve normal/recovery entries and specify manual recovery. Notify the user before boot-option changes or reboot verification. No new trial is selected or authorized by this document.

STAGE=R304 static checkpoint decision
RESULT=CP05 network repeat deferred; saved-source comparison completed
STATIC_OR_LIVE=PROVEN_STATICALLY helper ordering; prior LIVE evidence retained separately
HARDWARE_ACCESS=Filesystem and Git only
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=No new observation
PROVEN=Source differences and existing evidence boundaries
REJECTED=Blackout/zero pstore proves STATUS-read execution or its causal responsibility
UNPROVEN=Post-write current network transport, STATUS response, physical power, VCPU/ring execution
NEXT=Saved-source address/access-dispatch comparison; no build, install or reboot
