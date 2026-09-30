# R254 — sampled VCN2 source history

STAGE=R254
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=six pinned Linux source revisions
HARDWARE_ACCESS=none by comparison; separate Q36 GPU_COMPUTE review
HARDWARE_MUTATION=none for research target
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=60 source contract checks and 11 unchanged field definitions per revision
REJECTED=assuming the full queue protocol is identical across versions
UNPROVEN=external driver's exact revision; firmware implementation; BC250 physical behavior
NEXT=cache backing/provenance boundary and adversarial validation of observation rules

Pinned releases v5.4, v5.15, v6.6, v6.12, v7.2 and current Linux `551c722f40809618230001baccf219193e22fc5a` share the checked clock/reset masks, readiness mask2 versus busy mask4, normal ready-before-final-RBC ordering, NO_FETCH initialization and specialized VCN2 packet-start scratch test. Every sample contains the normal VCPU reset field and cache setup before its reset-release point. The normal ready polling loop is absent from the DPG start function in all samples.

The source-level shared decode-queue reset is absent in v5.4 and present in the sampled v5.15 and later code. This is a concrete reason to preserve the driver/firmware version and queue mode when comparing reports; it is not a claim about the exact introducing commit or all intervening releases.

A bounded same-function absence of an explicit RB_NO_FETCH zero assignment is not a global absence claim and does not diagnose a missing enable operation. These are reference-source comparisons, not six hardware experiments.

`source-manifest.json` binds each downloaded release to a resolved commit and file hashes. `compare_history.py` produces `results.json`. Raw upstream files remain local; published evidence can be reproduced from the pinned URLs.
