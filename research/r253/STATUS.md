# R253 — offline VCPU/RBC evidence contract

STAGE=R253
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=source-derived input interpretation and synthetic controls
HARDWARE_ACCESS=none by interpreter; separate Q36 GPU_COMPUTE review
HARDWARE_MUTATION=none for research target
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=30 named ambiguity/schema controls and all 256 status-field inputs checked
REJECTED=missing value equals zero; ready-bit input proves execution; cache access proves firmware fetch; harvest3 proves whole-block isolation
UNPROVEN=authenticity of external observations; VCPU instruction execution and physical failure cause
NEXT=apply contract to attributable existing captures if supplied; compare historical reference source

`CONTRACT.md` distinguishes register access, ring pointer state, independent ring effects, VCPU-ready convention, session completion and codec output. “No ready report” does not prove that no instruction ever executed.

`interpret_capture.py` accepts only a saved JSON object. It decodes named masks and documents missing provenance, without reading devices or issuing commands. It never declares execution or hardware failure proven. The empty template preserves missing values as unknown; it is not a machine snapshot. DPG indirect table placeholders are explicitly separated from final live mappings.

The 30 named tests cover absent values, busy/ready separation, reset request/status distinction, DPG placeholders, ambiguous harvest-plus-ready values, malformed numeric/schema data and 64-bit BAR composition. The 256-value status sweep validates field decoding only, not 256 hardware cases. All pass in `verification.json`.

All masks derive from the pinned R251 register header. Absolute physical register addresses are intentionally not inferred: source register indices and BASE_IDX require the matching ASIC mapping. User-supplied observations still need that mapping provenance.

R257 integration: explicit later-generation maps are rejected; the2.0 CABAC_MB_ACC and RB_ARB_CTRL.VCPU_DIS fields remain named scalar observations only. Six additional controls verify generation handling and malformed modes.

R259 integration: separate clock/LMI named fields were added without physical-state inference. All24 decoder masks pass a reference-header consistency audit in source-field-verification.json; four additional controls keep RBC/VCPU fields separate.

The paired-capture comparator passes14 additional synthetic controls. It withholds differences across mismatched/missing context labels, preserves unknown values and never upgrades a delta to chronology, execution or hardware-failure proof. Module/firmware identity fields are supplied provenance, not resident-byte verification.
