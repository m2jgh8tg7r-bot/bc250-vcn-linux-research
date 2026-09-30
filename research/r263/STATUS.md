# R263 — Historical lifecycle and test contracts

STAGE=R263
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=six pinned Linux source revisions
HARDWARE_ACCESS=none
HARDWARE_MUTATION=none
PROVEN=11 bounded invariants per revision; lifecycle variation recorded
UNPROVEN=whole-driver equivalence; original introducing commits; historical hardware behavior
NEXT=consolidate observation meanings and unresolved execution evidence

Across v5.4, v5.15, v6.6, v6.12, v7.2 and the current source pin, the normal stop requests UMC stall before a checked wait, then disables clock, asserts VCPU reset and clears status. The wrapper preserves bookkeeping on failure and has a same-state shortcut. The local conditional path from R262 is therefore not unique to the latest source sample.

Both decode and encode IB-test bodies map positive fence-wait returns to success and lack a completion-error query in all six samples. This does not re-prove every historical fence implementation or establish an actual false positive. R261's detailed fence chain remains tied to its current pin.

Important differences prevent transplanting the complete lifecycle:

| Sample | State storage | Submission count in begin-use | Idle worker has PG mutex | Legacy UVD DPM branch |
|---|---|---|---|---|
| v5.4 | device-wide VCN | absent | absent | present |
| v5.15, v6.6, v6.12 | device-wide VCN | present | absent | absent |
| v7.2 | per instance | present | present | absent |
| current | per instance | present | present | absent |

The current begin-use cancels delayed work on the first submission transition; sampled v7.2 cancels it on every begin-use. v5.4 uses a wait macro with an output argument, whereas later samples assign its return. These are source observations, not concurrency-bug diagnoses. The audit does not inspect all intervening commits or all historical macro/fence internals.

The script reuses the hash-pinned R254 sources and current manifest; it downloads nothing itself. Function hashes, starting lines, limited invariants and variations are recorded in `results.json`.
