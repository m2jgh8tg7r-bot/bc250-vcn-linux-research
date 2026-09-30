# R262 — Idle shutdown and partial-stop attribution

STAGE=R262
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=pinned Linux source
HARDWARE_ACCESS=none by audit; separate advisory Q36 GPU compute
HARDWARE_MUTATION=none
PROVEN=15 source witnesses; 13 ordered normal-stop phases
UNPROVEN=any physical stall or clock condition; occurrence of a failed stop; cause of the external report
NEXT=compare lifecycle and completion contracts across sampled releases

Normal idle shutdown intentionally clears the VCPU clock-enable request, asserts VCPU reset and writes status zero. A snapshot with those values can therefore follow earlier successful activity; it does not establish that startup never happened. The idle delay is nominally 1000ms converted to jiffies, not an exact shutdown time. The idle worker considers pending fences and submissions, requests gating under a lock, ignores that request's return and releases its profile reference.

The non-DPG stop sequence has three checked waits. It requests UMC stall before the third wait. If that wait returns an error, this function exits before clock-disable, reset and status-clear, without an explicit stall rollback on that return path. The power-state wrapper updates bookkeeping only on success. Thus, if bookkeeping was UNGATE beforehand and no other state change intervenes, a later UNGATE request can return zero through the same-state guard without invoking start (which contains an unstall request).

This is a conditional source-compatible partial-stop residue. It requires the preceding stop attempt and specified wait outcomes; it cannot explain an initial cold-start failure without those preconditions. Other callbacks or autonomous hardware behavior are outside this local path proof. No failed wait was induced and no actual stall was measured.

DPG stop follows a different branch. A zero VCN power-gating capability flag does not bypass the normal stop's clock-disable/reset/status writes: only the static power-off helper is conditional on that flag. Clock-gating helper behavior must also be read separately from its flags. These distinctions prevent treating software power bookkeeping as an execution trace.

The Q36 advisory review agreed with the bounded path ordering. Its broader phrase that DPG bypasses all stall operations is not adopted: only the normal-stop sequence is bypassed, and the DPG helper has its own implementation. Source witnesses and hashes are in `results.json`.
