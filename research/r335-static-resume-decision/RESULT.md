# R335 — Static continuation decision and independent restart entry

STAGE=R335
RESULT=Conventional backend inference strengthened; pre-read retained-lock self-deadlock unsupported; next discriminator requirements preserved
STATIC_OR_LIVE=PROVEN_STATICALLY saved-source/compiled analysis; R330 user-supplied live evidence separated
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Pre-read type1 successful return path unlocks backend lock; child bus normally inherits parent ops; examined ASPM override is Intel-specific
REJECTED=Successful pre-read necessarily leaves its backend lock held until post-read; AMD endpoint automatically uses examined Intel ASPM quirk
UNPROVEN=Other-CPU backend lock holder, runtime overrides, IO completion, exact stalled PC, physical power and VCPU execution
NEXT=Static preservation of alternate-boundary evidence; no live trial this week or unchanged hanging sequence replay

## Single-thread retained-lock hypothesis

R329 pre-read explicitly returned ret0 with identity13fe1002. Under conventional type1 dispatch, its compiled successful path unlocks pci_config_lock before returning0. Probe does not manually acquire that lock. Its intervening direct-writer normal path does not acquire it. Therefore merely chaining pre-read/write/post-read does not structurally retain this lock on the same thread. This rejects the simple retained-pre-read-lock explanation, not all backend-lock waits: another CPU or unexpected callback/state can still hold it, and no lock-owner/stack evidence was captured.

The source defines backend-lock users in type1/type2 access and additional platform/32-bit paths. This build is X86_64; mmconfig_32 is not a reason to assert a second active path. No active lock-holder census is inferred from source references.

PCI root creation passes root ops; pci_alloc_child_bus uses host child_ops if supplied, otherwise parent ops. Scoped pci_bus_set_ops callers include x86 ASPM quirks and AER injection. Examined ASPM override registrations target Intel ports, whereas the reported R329 GPU upstream port is AMD1022:13e5. AER injection is buildable as a module, but reported loaded modules contain no aer_inject. These observations strengthen conventional dispatch inference; they are not direct proof of runtime pointers or a global absence of all overrides. pci_bus_set_ops itself still uses generic pci_lock even under lockless read config; do not confuse that setter with the read wrapper.

## Current state sufficient to resume independently

Latest live test is R329, analyzed as R330: final base0x7e00, pre PCI ret0/ID13fe1002, CONFIG write-return, terminal CFG_AFTER_BEGIN50.744106s. Operator confirms no suffix, no automatic reboot, manual reset recovery. No post return/panic observed. Normal7.2.1 kernel was read; full health/display recovery is not inferred. R329 remains installed and normal default was preserved at independent install audit. Do not rerun its installer or menu automatically.

R331: generic PCI lock excluded; backend lock/port IO retained, low-quota restart contract.
R332: retained extracted research-kernel and vmlinux .text match; linked PCI instructions archived.
R333: skip condition narrowed to no_hw_access; independent VF/runtime bits; netconsole/queued-send and receive limitations.
R334: exact module writer alternatives and printk call/return boundary; dev_emerg level does not imply emergency-context flush.
R335: pre-read cannot simply retain the backend lock on its normal successful path; bus-op inheritance/known override qualifications.

User requested ten minutes from18:08:12 to18:18:12UTC (03:08:12–03:18:12JST), reports roughly2% weekly quota and explicitly prohibits more live tests this week. Any quota interruption can be resumed from this document and newer canonical/raw evidence. No quota measurement API is available; do not claim exact remaining percentage or0% reached. Q36 local AI is allowed if useful, but not used in this session; deterministic saved-code inspection resolved the current questions.

No agent hardware transaction, new build, package, installation, boot selection or reboot during this ten-minute session. Every meaningful stage is pushed and remote content checked; publication metadata remains local. Shared archive and session state preserve newest completed checkpoint. Do not send transcripts/keys/identifying data publicly.

## Next work and future discriminator requirements

The independent question is no longer base arithmetic. Separate (1) log-call not returned/scheduling, (2) standard PCI API entered, (3) backend-lock wait, (4) CF8/CFC operation not completing, (5) successful return but message missing. Network marker insertion alone cannot provide a PC snapshot or receiver acknowledgement. A caller timeout cannot preempt a non-returning bus instruction. Physical VCN request acceptance remains separate from transport completion even if future PCI read succeeds.

Next authorized steps are static: assess independent observation mechanisms and their actual prerequisites using retained kernel config/code, without arming or executing them; preserve a one-variable future design only if it discriminates these states better than another identical replay. Any future live test must wait for user lifting this week's prohibition and have documented recovery/observation boundaries. Do not change clock/reset/firmware/unknown SMU policy to guess a cause. Prior VCN ring, VA-API, hardware decode and stable playback remain unproven.

## Final observation-mechanism preflight (static only)

Saved config enables HARDLOCKUP_DETECTOR_PERF, SOFTLOCKUP_DETECTOR, MAGIC_SYSRQ, PSTORE and CRASH_DUMP. This is compiled capability, not proof of delivered NMI, captured stack, configured crash kernel or persistent evidence from R329. The saved boot reports NMI watchdog enabled; watchdog source starts watchdog_thresh at10, but actual wait time before manual reset was not provided. No diagnostic silence conclusion is justified. Hardware/fabric or delivery failure can prevent useful independent output. Kexec/crash dump needs its actual reservation/loaded-kernel prerequisites checked; pstore needs a writing event and backend; USB SysRq requires functional input delivery. None was armed or executed. A future plan must verify the entire independent observation path, without assuming config alone makes a stalled bus recoverable.

Session close: ten-minute static work only; no continuing background research/build/receiver processes were started. All numbered stages pushed and remotely checked. Further live tests this week remain prohibited. This is the latest self-contained entry unless newer evidence is present. Remaining quota and0% status are not observable to the agent.
