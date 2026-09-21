# R216 — Priority-queue path can consume the policy gate before setter entry

2026-09-22. Saved Robin1 bytes and synthetic CPU work only; no hardware access.

R215's direct-mask result has now been connected to the ordinary saved dispatcher and worker path. The policy setter is queued at priority 6, while the periodic walker is queued at priority 4. The saved queue favors the smaller number. Therefore callback-before-target behavior does not require preemption inside the setter: it can occur before the setter starts, when both callbacks await selection.

## Fixed-image route

In the saved R1 image, channels 3 and 4 share table `0x7464`. Entry `0x1d` points to `0x2e6c8` with metadata word `0x6`: priority 6, permission mask zero, direct-call flag clear. This is table interpretation, not authorization or evidence of host accessibility.

Dispatcher `0xebc` checks bounds, handler presence and permissions. With the direct-call bit clear, instructions `0xf40..0xf4d` pass the handler, metadata priority and channel argument to `0x26b4`. There is no resource acquire/release call in this dispatcher. Earlier candidate wrappers `0x1070/0x10d0` describe a different mailbox transaction; they must not be substituted for the setter's table route.

Timer callback `0x1024`, when its pending condition permits submission, passes `0x1b154` with priority 4 to the same queue helper (`0x1034..0x1041`). This reuses R146/R169's established timer/worker connection; the new result is its composition with the setter's exact R1 metadata and R215's resource semantics.

The worker obtains a queued item through `0x1fc4 -> 0x27f8`; on successful acquisition, `0x1fc4` copies the queued priority into task fields `+0x29/+0x2a` and restores PS before returning (`0x202f`). The worker then calls the copied callback at `0x1e90` or `0x1e96`, and calls completion at `0x1e99`. No extra resource-acquire wrapper appears in these checked bodies. R215's completion guard requires zero remaining claims after the previous callback. Initial task state and indirect/global context are not exhaustively proven.

## Queue-backed ordering witness

The unchanged R165 enqueue interpreter and R169 dequeue interpreter were used on synthetic RAM with context inhibition during insertion and threshold 7 during extraction. Both arrival orders were tested:

| Arrival order while neither has been extracted | Observed dequeue order in the bounded interpreter |
|---|---|
| setter(6), walker(4) | walker(4), setter(6) |
| walker(4), setter(6) | walker(4), setter(6) |

The callback layer is an explicitly abstract selector/target model. Starting from A=1, B=0, target=old=0, the walker first applies the old target and makes A=B=0. The setter then stores target=1250; its direct applicator sees equal selectors and skips. Final state is target=1250, old=0, A=B=0, consistent with the saved software-field observation. The no-walker control and an assumed FIFO-order control instead yield old=1250.

The queue portion follows saved instructions; the callback abstraction does not simulate floating-point clock conversion or hardware writes. The fixtures assume the callback is registered, pending permits submission, both items coexist before extraction, and no intervening profile/reset operation changes the fields. Actual R125B arrival, extraction and execution times remain UNPROVEN. A setter already extracted cannot be reordered by this particular witness.

## Consequence for measurement design

Gate readback followed by a later successful setter response does not establish that the gate was unequal at setter entry. Host submission order is also insufficient to infer callback execution order across this queue. To distinguish this mechanism, evidence would need to bracket queue insertion/extraction or applicator entry together with selectors and target values; aggregate queue counts and non-atomic readback do not supply that history.

No such safe live observation transport is established yet. R217 continues static work on the saved PSP trusted-OS load-response path, which is a separate boundary from SMU clock policy. There is no repeat gate write, firmware swap or reboot.

PROVEN_STATICALLY: exact routing metadata, checked wrapper instructions, priority-queue witness. CONSISTENT_WITH: this ordering explains the saved selector/target/old fields under stated assumptions. UNPROVEN: historical ordering and VCN operation.

[Route and model results](../logs/R216_ROUTE_RESULTS.json), [verified instruction bytes](../logs/R216_INSTRUCTIONS.tsv), [saved dispatch evidence](../logs/R216_DISPATCH.txt), [reproducer](../logs/R216_verify_route.py). The reproducer requires the prior R165/R169 artifacts named and hashed in its results; it is not a standalone hardware test.
