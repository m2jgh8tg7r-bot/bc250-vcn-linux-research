# R303 — network-first CP04 pre-MMIO boundary

R302 user-supplied receiver excerpt confirms qualification 2/10–10/10 and completion, successful read status and exact 18-byte token, receiver confirmation, amdgpu load, firmware software initialization/direct copy, P1 begin, then the CP03 intentional-panic checkpoint marker at 58.526934 seconds. User reports return to the normal environment with normal operation. Current agent observation confirms the normal kernel. The excerpt does not show the final Kernel panic line or countdown; automatic restart, complete packet delivery and arbitrary hang-time transport remain unproven. Display IRQ warnings were followed by later P1/CP03 markers and cannot alone explain termination.

Next comparison reuses the retained signed CP04 module. Source shows helper entry, zero pg/cg flags and non-VF guards, then unconditional panic before the helper's first VCN MMIO. The historical CP05 write-return evidence remains valid; CP04 is a qualification of this newly established network transport at a closer boundary, not a claim that CP05 evidence disappeared. No unchanged CP06/CP07 read experiment is proposed.

R303 retains R302's exact public token R299-CP03-RECEIVED and network/input sequence. Only stage/expected-checkpoint text and the amdgpu module change. CPU gate tests and archive validation do not prove hardware execution. A future boot performs existing GPU initialization and intentionally panics; it can require manual recovery. VCN execution remains UNPROVEN.

Installer defaults to privileged read-only preflight; installation replaces only R302 after verified HOME backup because boot capacity cannot retain both. R300, normal and recovery entries are protected. No selection or reboot is performed by installation. Installation requires a matching prior preflight; manual-menu preparation follows independent installed audit and advance notification.

STAGE=R303 HOME preparation
RESULT=Prepared CP04 network comparison; not installed or booted
STATIC_OR_LIVE=PROVEN_LIVE prior R302 user-reported receipt/recovery; PROVEN_STATICALLY CP04 source boundary and package checks
HARDWARE_ACCESS=No new agent device transaction
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=No new hardware failure observation
PROVEN=R302 CP03 checkpoint receipt and user-reported normal return
UNPROVEN=R303 live boundary, final panic transport, VCN power/VCPU/ring execution
NEXT=Privileged read-only R303 preflight followed by independent audit

Validation: 11/11 CPU/PTY gate cases PASS; dependency closure, warning-free depmod, gzip and exact archive round-trip PASS. Independent comparison against R302 finds only init and amdgpu.ko changed. Image size 168064077 bytes; image SHA-256 f100c7aebe64bec65a452646360a9a198dc183bafe056c00c280b7c4b4ad9b8c.

## Installed and independently audited

User-run installation PASS. Installed R303 image/BLS and both R302 retirement backups independently match. Retired R302 paths are absent. Protected hash records equal preflight: nine accessible protected files independently checked, four rely on the privileged installer record. No selection, module load or reboot occurred.

Next: save receiver output to a file, then user-run arm-menu.py. This backs up grubenv and sets only a transient 30-second manual menu timeout; it does not select an entry, change pstore or reboot. Audit its PASS output before manual R303 boot. Confirm same-boot R303 QUALIFICATION_COMPLETE on receiver before entering the retained public token R299-CP03-RECEIVED. Expected CP04 helper-entry/guards-pass/panic occurs before first helper VCN MMIO. R303 LIVE remains UNPROVEN.
