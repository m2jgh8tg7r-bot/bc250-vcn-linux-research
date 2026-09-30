# R267 — Comparison preparation

STAGE=R267
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=CPU preparation plus passive cached kernel/device metadata; no register or DRM test
HARDWARE_ACCESS=cached sysfs metadata only; no register transactions
HARDWARE_MUTATION=none
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=normal-API preflight builds; saved-counter arithmetic verified against independent increment enumeration
REJECTED=preflight build means critical test ready; unknown wrap count chosen from requested frequency; missing input means zero
UNPROVEN=original GPCNT mapping/timing capture; safe matching acquisition path; current physical VCPU state
NEXT=continue source audit of fetch-observation boundaries; critical live acquisition remains not ready

PLAN.md specifies before/after evidence, A/B outcomes, stop/recovery limits and the missing acquisition evidence. The query binary is a standard-API preflight only, not a VCPU test. analyze_counter.py accepts saved values only; it does not access hardware. Inputs with missing provenance or ambiguous wrap count do not produce a unique rate. Distinct supplied counts can still be recorded without claiming a validated clock source. No original external GPCNT capture has been replayed.
