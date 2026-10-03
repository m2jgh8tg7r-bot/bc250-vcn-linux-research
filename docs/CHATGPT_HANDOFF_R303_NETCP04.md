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


## User-reported R303 boot and normal return (2026-10-03)

User reports booting R303, entering input according to the procedure, then rebooting and returning to the normal entry. Agent read-only inspection confirms the current normal kernel `7.2.1-ogc4.1.fc44.x86_64`; current command line points to the normal deployment. Receiver output has not yet been supplied for this attempt. This report does not independently establish token acceptance, GPU load, CP04 helper entry/guards/panic, or automatic panic-driven restart.

STAGE=R303 user-reported boot / normal return
RESULT=User reports procedure completed and normal entry restored; receiver evidence pending
STATIC_OR_LIVE=PROVEN_LIVE current normal kernel; user-reported R303 attempt
HARDWARE_ACCESS=Agent read-only procfs inspection; user-performed boot/input/reboot
HARDWARE_MUTATION=No new agent hardware mutation
HARDWARE_FAILURE=NO_EVIDENCE in the current report
PROVEN=Current normal kernel; user-reported return to normal entry
REJECTED=Normal return alone proves CP04 checkpoint delivery or VCN operation
UNPROVEN=R303 token acceptance, CP04 receipt, final panic/countdown, automatic restart, VCN execution
NEXT=Inspect R303 receiver output from QUALIFICATION_COMPLETE through final received lines; classify checkpoint before choosing next comparison


## R303 receiver evidence — CP04 guards reached live

The user-supplied cumulative receiver text contains separate historical R298/R299/R300/R302 boots followed by R303. R303 includes all qualification markers 1/10–10/10, completion at 15.372569, input read_rc=0 and bytes=18 at 45.845515, exact-match acceptance, receiver confirmation and GPU load beginning at 50.847807. Firmware direct-copy reports 405696 bytes and equal=1; software initialization completes. At 56.266818 P1 begins, at 56.266827 CP04 helper_entry is received, and at 56.266834 CP04 guards_pass before first VCN MMIO is received. These last two lines belong to R303, not the earlier R302 CP03 boot.

This establishes network delivery through the helper guard boundary. The retained CP04 source places intentional panic after this marker and before the helper's first VCN MMIO; the supplied text ends at guards_pass. No final Kernel panic line or restart countdown is present. Automatic restart and complete panic delivery remain UNPROVEN. The init prefix retains NETCP03, but its R303 stage and CP04 expected/actual markers identify this comparison. Display IRQ warnings precede continued P1/helper progress and do not by themselves establish the termination cause. The early previous-reset parity flag describes previous-reset status; it does not prove a new R303 parity fault.

STAGE=R303 CP04 receiver qualification
RESULT=PROVEN_LIVE receipt through helper entry and guards_pass before first helper VCN MMIO
STATIC_OR_LIVE=User-supplied LIVE receiver evidence plus retained static CP04 boundary
HARDWARE_ACCESS=User-run R303 boot; no new agent device transaction
HARDWARE_MUTATION=No new agent hardware mutation
HARDWARE_FAILURE=NO_EVIDENCE of an unintended failure in the supplied ending
PROVEN=Qualification 1/10–10/10 receipt, exact token acceptance, GPU software initialization/direct-copy markers, P1, helper entry, guard passage; normal return recorded separately
REJECTED=This proves VCN firmware execution or makes historical CP05 write-return evidence invalid
UNPROVEN=Final panic/countdown delivery, automatic restart, arbitrary hang-time transport, VCN physical power/VCPU/ring execution
NEXT=Use CP04 as the qualified pre-MMIO network boundary; statically review a discriminating next comparison using historical CP05 and failed CP06/CP07 evidence, without repeating an unchanged failing read
