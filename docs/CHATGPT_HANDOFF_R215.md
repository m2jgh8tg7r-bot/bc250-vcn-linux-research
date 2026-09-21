# R215 — Resource claims, granted bits, and restored interrupt state

2026-09-22. Static saved Robin1 analysis and bounded CPU models; no hardware access.

R147 identified different resource masks in the periodic walker and policy setter. R215 now resolves the shared state aliases, the acquire/release boundary, and the meaning of a waiting task's mask. This is not proof of historical callback interleaving. R216 continues outward into mailbox dispatch; a caller may hold additional resources.

## Shared state and acquisition

Saved literals are `0xd00 -> 0xae80`, `0xd20 -> 0xae84`, and `0xcfc -> 0xaec0`. Therefore acquire's `base+0x40` and release's `base+0x3c` are the same current-task pointer at `0xaec0`. Their `+0x68` and `+0x64` accesses likewise name one global granted-resource mask at `0xaee8`.

`0x2268(mask)` raises the processor interrupt level with `rsil 2` during bookkeeping. It rejects overlap with the current task's `+0x2c` mask through fatal handler `0x1b78(1,3,mask,...)`. Otherwise it adds the request to that task mask **before** testing global availability.

- When none of the requested global bits is already set, it adds the bits globally and restores the saved PS at `0x229c` before returning.
- On conflict it sets task state 2, saves the requested mask at `task+0x30`, updates priorities of active overlapping tasks, restores PS at `0x22df`, and reaches context-switch entry `0x2de8`.

Thus `task+0x2c` is a claim mask containing granted bits plus a blocked request, not always a mask of resources already acquired. State, wait mask and global granted bits must be considered together. On a pre-switch waiting path, normal return has not been established.

## Release and completion

`0x231c(mask)` rejects release of bits absent from the current task claim (fatal arguments begin `1,10,mask`). It removes valid bits from the global and task masks. It scans five task records for state-2 waiters whose requested bits are free, favors the numerically smallest priority, grants the selected task's claims, changes it to state 1 and clears its wait mask. Equal-priority selection keeps the first table candidate. It can admit multiple compatible waiters in one release operation.

The releaser's base priority is restored, with another inheritance check if it retains claims. A scheduler transition may follow; PS is restored on both the normal-return and transition paths. The actual context switch remains outside the CPU model.

At worker completion, `0x2040` checks that the current task's claim mask is zero before clearing its task state; a nonzero mask reaches fatal handler arguments `1,1,0,...`. Queue-item removal, callback completion and resource release therefore remain distinct milestones.

## Relation to the policy observation

The setter `0x2e6c8` stores the target before acquiring `0x40000`, calls the applicator, then releases that mask. The periodic walker `0x1b154` obtains mask 1 before invoking slots. A synthetic case with another task holding only mask 1 allows `0x40000` to be acquired normally; requesting mask 1 instead reaches the context-switch boundary. In both cases PS has already been restored at the checked boundary.

This rejects the claim that those two direct masks alone serialize the paths, or that the acquire helper necessarily leaves interrupts raised for the whole caller operation. It does not prove that callbacks can run at an arbitrary instruction: outer locks, initial PS, task priority, registration, context nesting and live state still matter. R147/R202's callback-before-target model remains CONSISTENT_WITH the saved result, not its established cause.

## Verification and limits

The exported 306 instruction byte sequences match the fixed analysis image SHA-256 `8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675`. The important `movi.n a11,0xff` at `0x2347` has signed immediate -1, so the release mask inversion is 32-bit; treating the printed `ff` as positive 255 would be wrong.

A bounded interpreter and a separate state-transition reference agree on 4,096 acquire/release cases, including high-bit masks, conflicts, reentrant claims, release errors and priority changes. Counts: acquire returned 536 / reached context boundary 1,303 / fatal 209; release returned 1,114 / reached context boundary 115 / fatal 819. Two directed mask cases and a completion-guard case also pass. The actual small task-state setter is interpreted in its own supplied register window; fatal and scheduler targets are stopping boundaries. These are synthetic sequential fixtures, not full Xtensa emulation or a concurrency proof.

PROVEN_STATICALLY: aliases, checked instructions, scoped state transitions and CPU results. UNPROVEN: outer dispatch serialization, live task/PS/claim values, historical timing, VCN operation. R216 proceeds with outer mailbox dispatch instead of stopping because a live test is not ready.

[Model results](../logs/R215_MODEL_RESULTS.json), [reproducer](../logs/R215_check_resources.py), [verified instruction export](../logs/R215_INSTRUCTIONS.tsv), [function evidence](../logs/R215_FUNCTIONS.txt). Run the reproducer with the saved analysis image, exported instruction file, and an output JSON path. No device access.
