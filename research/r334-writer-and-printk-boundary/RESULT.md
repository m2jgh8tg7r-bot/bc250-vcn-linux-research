# R334 — Candidate writer and printk boundary

STAGE=R334
RESULT=Compiled writer alternatives and log-call/PCI-call separation preserved
STATIC_OR_LIVE=PROVEN_STATICALLY exact candidate module; inherited live markers separated
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Writer skip boolean precedes outlined write path; direct store versus independent runtime-bit/trylock KIQ branch; printk ring storage precedes console flush and function return
REJECTED=KERN_EMERG text level guarantees NBCON emergency-context priority; receiving BEGIN proves dev_emerg has returned
UNPROVEN=Actual runtime virtualization/skip state, printk flush method, exact stalled PC, post-read return and VCN power/execution
NEXT=Preserve future discriminator requirements; no additional live test this week

## Exact module writer

WRITER_FUNCTIONS.disasm contains the candidate module's writer, outlined part and skip predicate. Entry calls skip_hw_access and returns early if true. Its other branch enters amdgpu_device_wreg.part.0. The outlined body checks aperture, then tests independent SRIOV RUNTIME bit0x10; if clear, a direct 32-bit store occurs at0x8da0. If set, down_read_trylock can select KIQ; failed trylock returns to direct store. Non-VF alone does not decide this bit, as corrected in R333. These paths add no unconditional register readback or GPU command acknowledgement.

Writer function return is before the probe emits WRITE_RETURN, so a still-stuck writer or its trace callbacks cannot directly explain a later genuinely received CFG_AFTER_BEGIN on that same probe invocation. This does not determine whether the store was skipped, posted, internally accepted or electrically completed. Runtime code patching/trace state remain unobserved.

## BEGIN record is inside a logging call

The audited candidate orders _dev_emerg(CFG_AFTER_BEGIN), pci_read_config_dword, then _dev_emerg(CFG_AFTER_RETURN). _dev_emerg in drivers/base/core.c returns void and supplies no receiver acknowledgement. vprintk_emit stores into the printk ring before console flushing, waking print threads, optional legacy console handling and return. Therefore its record can already be received while the emitter is still inside the logging call; scheduling between that call and PCI read is another unobserved boundary.

kernel/printk/internal.h:194 onward chooses direct/offloaded flushing using context and running-console threads. nbcon_get_default_prio in nbcon.c:1442 checks panic CPU and emergency nesting state; it does not choose emergency context merely from KERN_EMERG text severity. The helper's dev_emerg strings therefore do not prove an emergency atomic flush. Earlier display warnings do not attest current emergency nesting at this later call. R329's runtime flush type was not logged.

The last receiver marker provides ordering of record creation through write return, not a program-counter snapshot. A genuine PCI backend stall remains consistent with terminal BEGIN/manual reset, but selecting it over logging/scheduling/local-record-without-UDP hypotheses requires independent evidence. A future experiment must distinguish log-call return, actual PCI entry/backend entry and missing transmission; adding more network BEGIN markers alone cannot close that gap. A timeout around the caller cannot interrupt a non-returning bus instruction.

No new image, install, menu operation, register transaction or reboot. R331 contains low-quota restart rules; R332 linked-kernel correspondence; R333 source transport limits. User's current ten-minute window ends18:18:12UTC and this week's live prohibition persists.
