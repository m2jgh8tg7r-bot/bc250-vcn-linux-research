# R336 — NMI watchdog discrimination and output limits

STAGE=R336
RESULT=Hardlockup detector can potentially sample an IRQ-stalled CPU; default is warning, not automatic panic; silence is not a negative proof
STATIC_OR_LIVE=PROVEN_STATICALLY retained build config/source; no live watchdog test
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Perf callback receives pt_regs; hardlockup predicate checks unchanged timer interrupt count; default hardlockup_panic false; console hostile takeover restricted to panic priority
REJECTED=Enabled NMI watchdog implies automatic panic/pstore capture; no received watchdog output rules out backend lock or bus stall
UNPROVEN=R329 watchdog event coverage/NMI delivery, elapsed wait, captured PC, output delivery, stop cause
NEXT=Static review of independent observation paths and prerequisites; no new live test this week

## Detector and sampled state

watchdog_perf.c:102–119 receives pt_regs in its perf overflow callback, skips checking during existing panic and when timestamp validation fails, and calls watchdog_hardlockup_check for the current CPU. watchdog.c:183–197 detects unchanged per-CPU timer interrupt count across qualified checks; touch/reset and already-warned logic can defer/suppress a report. On a detected local hardlockup with regs, the report calls show_regs(regs), making a sampled RIP a potential independent discriminator if captured. Config alone or the early enabled message is not actual sample coverage.

Type1 pci_config_lock acquisition uses raw_spin_lock_irqsave; following CF8/CFC IO occurs with local IRQs disabled. If NMI delivery and the detector remain functional, a sufficiently prolonged wait here can stop timer increments and produce a sampled location. A normal IRQ-enabled scheduling wait or deferred console delivery does not necessarily meet the same hardlockup predicate. An actual IO/fabric stall may also prevent NMI progress; all are conditional, not guarantees.

The default watchdog_thresh is10 but sample scheduling/timestamp checks are separate from a fixed guaranteed10-second report. Operator gave no measured delay before manual reset. Do not infer the trial waited long enough or that it failed the detector's timing condition.

## Warning does not imply persistent panic evidence

Retained config leaves CONFIG_BOOTPARAM_HARDLOCKUP_PANIC unset; hardlockup_panic initializes to false. R329 init does not set that watchdog policy. Detected lockup ordinarily reports and shows regs rather than obligatorily calling nmi_panic. panic=0 controls restart after a panic, not whether hardlockup triggers a panic. Thus an absent pstore panic record is not a useful negative about this boundary. Runtime policy is not freshly attested.

Watchdog report prints its first emerg message before acquiring printk_cpu_sync for subsequent details; that design avoids making the first warning depend on that serialization lock, but does not bypass every console/network dependency. printk severity alone does not imply NBCON panic priority. nbcon_context_try_acquire_hostile requires explicit allowance and panic priority; a warning path cannot be assumed to take over a console whose current owner is unsafe. Netconsole itself enters unsafe while sending, and queued/drop/output paths remain as in R333. Independent sample generation and independent durable delivery are separate requirements.

## Future-plan prerequisites, no execution requested

Any later NMI-based observation proposal must qualify event coverage, sufficient measured time, actual panic/warning policy, sampled-register capture and a delivery/persistence route surviving the candidate fault. It must not infer readiness from enabled config, reuse the same netconsole path as proof of independent observation, or retry R329 unchanged simply to wait longer. A backend-lock sample would not itself prove lock owner's cause; an IO sample would not prove VCN power/fuse status.

User resumed static analysis after the ten-minute session; the former18:18:12UTC deadline is historical and not a new timed grant. Further live tests this week remain explicitly prohibited. No new image/build/install/boot option, watchdog setting, hardware access or reboot was performed. Latest live remains R330 terminal post-read begin/manual reset. R335 is the broader self-contained continuation summary; R336 adds detector limitations. Quota0% cannot be detected by agent. Results are published and remotely checked so interruption does not lose the restart point.
