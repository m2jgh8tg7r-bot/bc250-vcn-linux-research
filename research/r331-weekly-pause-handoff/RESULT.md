# R331 — PCI access dispatch and low-quota continuation handoff

STAGE=R331
RESULT=Static transport/locking audit completed; this week's additional live tests prohibited by user
STATIC_OR_LIVE=PROVEN_STATICALLY retained exact build sources; R330 live transcript remains separate
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Build CONFIG_PCI_LOCKLESS_CONFIG=y; generic PCI wrapper omits pci_lock; conventional domain0/offset0 dispatch prioritizes raw_pci_ops; type1 access has a distinct lock and CF8/CFC IO
REJECTED=Generic pci_lock wait is required by this built wrapper; CONFIG write-return proves request completion
UNPROVEN=Actual boot bus->ops/raw_pci_ops identity, type1 lock ownership, entered/stopped instruction, bus completion, physical VCN power/execution
NEXT=Saved-source/compiled analysis only this week; resume from this handoff without another live trial

## Current live result (R330)

R329 input accepted; final pointer die0/count3/one instance0 record, base1=0x7e00. Pre PCI identity read ret0, expected and actual0x13fe1002. CONFIG write0x55555 reports return. Actual terminal receiver line is CFG_AFTER_BEGIN at50.744106s; operator confirms no suffix and manual reset recovery. No post-read return or named panic received. Current normal kernel was read after the trial. No proof of full recovered health, VCN execution or cause. Do not replay this sequence unchanged. R325 transcript preceding it belongs to another boot.

Receiver command used in supplied transcript is display-only UTF8 decoding, not raw JSONL capture. Existing screen evidence establishes listed markers but not complete byte/sequence capture. Do not demand a repeat merely to obtain a file.

## New static finding

Exact retained .config enables PCI_LOCKLESS_CONFIG, PCI_DIRECT and PCI_MMCONFIG. drivers/pci/access.c:26–54 therefore omits generic pci_lock on pci_bus_read_config_dword. pci_read_config_dword at580–587 first checks disconnected state, then invokes that wrapper; alignment0 is valid. A diagnosis of waiting on the generic pci_lock for this call is inconsistent with this configuration.

For conventional x86 bus ops, arch/x86/pci/common.c:40–47 prioritizes raw_pci_ops for domain0 and offset below256, even when extended MMCONFIG is available. The supplied boot has domain0000, identity offset0 and reports configuration type1 base access. Type1 is therefore strongly supported conditional on conventional bus ops, not independently attested runtime dispatch. arch/x86/pci/direct.c:21–49 takes distinct pci_config_lock with IRQ saving, emits outl(CF8), then inl(CFC), unlocks and returns0. Lock wait and platform IO completion remain distinct possible boundaries; the generic lockless option does not eliminate this backend lock. No timeout breaks either operation. Merely assuming MMCONFIG from its enabled config or ECAM boot message is insufficient.

amdgpu_reg_access.c:494–514 first checks skip_hw_access; an in-aperture non-SRIOV normal access uses writel then a trace hook. The checkpoint guards and reported byte0x1f800/aperture524288 support that branch. A WRITE_RETURN records function/control return, not device internal acknowledgement; an internal skip possibility is not independently instrumented. No readback was added and no physical power conclusion follows.

CF8/CFC IO, a backend lock, missing printk delivery and instruction execution are not differentiated by the receiver tail. No stack/NMI trace or runtime ops pointer was captured for the failed interval. Software evidence cannot select one as the established cause.

## User constraints and restart instructions

User reports weekly budget2%; agent cannot inspect remaining quota or guarantee a checkpoint at exactly0%. No additional live test this week. This prohibition persists across new turns; resuming analysis is not permission to boot/install/arm hardware again. Do not reuse expired hardware permissions.

Repository is the independent continuation record: docs/CHATGPT_HANDOFF_R331.md, R330 live handoff, R329 preparation and r327 transaction contract. R329 remains installed; normal boot default preserved. No new package/install/menu/reboot is requested. Do not run install.py again (its preconditions intentionally require uninstalled state). Existing raw/private addresses, keys, full kernel trees and source baselines stay local.

Next authorized static work: inspect retained compiled pci_read_config_dword/pci_bus_read_config_dword/raw_pci_read/type1 backend and their actual section/call correspondence; examine saved WRITE_RETURN trace-hook path; compare pre/post probe instructions and logging context. Resolve the inherited inaccurate init phrase panic before helper VCN MMIO in a future distinct package only (R329 does write CONFIG). Keep lock, IO/bus, logging and internal power hypotheses separate. Plan a future discriminator only after these gaps are clear and renewed user authorization permits a live test; no arbitrary register/SMU changes and no unchanged hang replay.

If quota interrupts work, read this document and any newer canonical/results first, inspect Git status/history, preserve originals and add a new numbered result. Do not claim VCN works until firmware init, ring execution, VA-API, FFmpeg hardware decode and stable playback are actually proven live.

## Compiled access follow-up

Retained direct.o pci_conf1_read contains pci_config_lock and _raw_spin_lock_irqsave plus a 32-bit port input instruction. Retained access.o pci_bus_read_config_dword contains an indirect bus-op call and no generic spin-lock call/reference. This independently supports the configuration-dependent static distinction; object correspondence to the installed kernel and runtime bus-op target are not newly attested. COMPILED_ACCESS.disasm preserves the exact selected functions. No runtime failure cause is established.
