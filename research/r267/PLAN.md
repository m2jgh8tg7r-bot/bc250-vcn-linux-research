# R267 — Concrete comparison preparation and readiness boundary

The user requests preparation now and continued research until interruption. This package separates a ready normal-API preflight from the unresolved acquisition path for the actual discriminating VCPU/counter/mirror comparison. Building a preflight does not make the critical hardware experiment ready.

## Experiment priority and outcomes

1. Existing GPCNT raw-data reanalysis: independent counter slopes following800/1250MHz demote whole-domain clock absence; unreconstructable timing is inconclusive, not evidence of clock absence. Original counter configuration/index provenance and timestamp code remain needed.
2. Matched VCPU-output/first-fetch evidence: a VCPU-originated completed instruction read excludes total read blockage for that transaction; absent unvalidated trace/marker output does not identify a cause. No custom firmware or security manipulation is prepared.
3. Cross-board saved mirror values: different values support configuration differences, not necessarily OTP differences. Same values with working RBC/VCLK oppose whole-domain disable but do not exclude VCPU-specific disable while both VCPUs remain inactive.
4. Planned stock-versus-MeiMeiV3 control: same symptom weakens the necessity of its additional warm reset; different outcome identifies BIOS/history dependence, not warm reset uniquely. No BIOS installation is prepared here.

## Ready component: standard-API preflight

`query.c` retains R195's seven standard DRM information queries, with an explicit render-node argument instead of a hardcoded node. It has been compiled with warnings as errors. It checks acceleration and GFX as controls, then records VCN/JPEG available-ring and video-capability fields. It submits no video jobs, firmware requests or register accesses. The revised binary has not been run on the device in this stage.

Before using it, bind the render node to the intended AMD device through cached sysfs metadata and record kernel/module identity and an opaque boot-context label. Do not choose a node by number alone. A failed GFX control stops the sequence; zero VCN rings or EINVAL video capabilities records API exposure only. It cannot identify a fuse, firmware failure or physical VCPU state.

The file-descriptor lifecycle requires no persistent rollback. If unexpected driver errors/hangs appear, stop; do not retry. Existing R195 established normal-query behavior in its older environment, not universal safety of all device queries on every kernel. New boot/image conditions require their own attribution. For this environment, the standing local operating rule defers VA-API/FFmpeg diagnostics until ring execution is established. This is an operational restriction, not a universal evidentiary ordering: on another validated setup, an ordinary API job can itself supply ring-execution evidence. This information-query preflight alone does not validate such a job path.

## Critical measurement acquisition: NOT READY

No verified BC250 acquisition implementation for the new GPCNT or three SMN mirror observations has been supplied in this session. The existing archives include read-related hangs. The package therefore contains no direct SMN/MMIO reader, selector manipulation, undocumented request sweep, trace enable, reset write, harvest clear, BIOS patch or PSP bypass. A process timeout is not treated as recovery from a stalled bus or kernel.

Required before a new device acquisition can be marked ready:

- Exact known-working acquisition code/path and matching target/map, including selector or read-side effects and concurrency assumptions.
- Evidence tying that path to the intended board/firmware/source configuration; another board's success is not identical safety evidence.
- Before/after fields and A/B interpretation fixed in advance, with unknown/invalid reads retained as unknown. For a fetch observation, define initiator classification and retain a positive-control record proving that the observer can detect the intended event in its covered interval. A standard DRM information query is not that positive control.
- Recovery behavior and stop condition supported by the chosen existing path; no unverified promise that a reboot/power cycle restores all state.
- If a boot-option or reboot test becomes concrete, notify the user before proceeding, as requested earlier.

This is a missing-evidence boundary, not a request for permission to perform an unspecified experiment. Continue useful source analysis and prepare saved-data interpretation while the acquisition evidence remains unavailable.

## Capture contract

Keep board alias, boot-context alias, source/module/firmware identities, BIOS identity, reset history, capture phase, register-map provenance, counter configuration, acquisition method and read validity. Preserve original logs privately; publish sanitized derived records. Do not combine Shalasere observations across dates or PhishMaster observations with Thomas's into one synthetic board state.

Counters must carry declared width, a justified unsigned modulo up-counter model and independent monotonic timestamps. The analyzer reports increments/second; conversion to clock cycles/second needs a separate tick-to-cycle contract. Saturating, down-counting or unidentified counters do not satisfy this model. Known reset/reconfiguration intervals cannot be differenced. Without a justified independent rate bound, modulo arithmetic can leave multiple wrap counts possible. The requested frequency must not be used to choose the number of wraps and then presented as measured confirmation of itself.

For mirror data, record the three separate symbolic fields and validity of each. Missing is not zero; all-ones is ambiguous. Readback consistency does not identify OTP, mirror wiring or physical operation. Stock/modified comparisons require matched software/configuration and phase, while documenting BIOS as the intended changed variable plus reset-history confound.
