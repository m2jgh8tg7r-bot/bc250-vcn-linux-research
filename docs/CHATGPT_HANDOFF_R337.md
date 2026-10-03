# R337 — Persistent observation readiness audit

STAGE=R337
RESULT=Existing R329 package does not qualify an independent durable failure-observation route; new live trial remains unprepared and prohibited this week
STATIC_OR_LIVE=PROVEN_STATICALLY retained boot entry/init plus pstore source
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=EFI pstore disabled in entry; no crashkernel argument/load step or ramoops setup in init; nonblocking pstore dump may skip on lock contention
REJECTED=Kernel PSTORE/CRASH_DUMP capability means independent failure evidence was armed
UNPROVEN=Persistence under reset, NMI sample/output coverage, post-read return, stop cause and VCN execution
NEXT=Static route qualification design only; no changes or new live attempt this week

## Existing artifact readiness

OBSERVATION_MATRIX.json separates compiled capabilities from prepared/observed paths. R329 entry explicitly sets efi_pstore.pstore_disable=Y and panic=0, with tty0 and SysRq enabled. It contains no crashkernel argument. Its minimal init mounts proc/sys/dev, loads LAN/netconsole and later amdgpu; it does not initialize ramoops, reserve a persistent region or load a crash kernel. The retained user tools do not add a kexec load step. These are scoped package observations, not a claim about every possible unseen platform reservation/backend.

Therefore merely waiting for a watchdog or receiving no pstore log cannot establish the CPU location. R336 establishes default warning policy and potential sampled regs, not a guaranteed persistent dump trigger. A normal hardlockup warning is not inherently kmsg_dump panic, and EFI pstore was deliberately disabled.

fs/pstore/platform.c:150–167 classifies NMI/panic/emergency dump contexts as unable to block; dump code at291–298 uses raw_spin_trylock_irqsave and skips if the buffer lock is busy. This avoids one blocking risk but sacrifices capture under that condition. Backend-specific writing and memory retention remain additional prerequisites. Enabling a backend in a future candidate is not evidence it works during this stall or after manual reset; no enabling is requested.

SysRq availability alone says nothing about input interrupts surviving an IRQ-disabled stall or its output escaping an unsafe console/network path. Crash-dump config alone lacks reserved/loaded capture-kernel evidence. No route in the current package independently distinguishes logging-call completion, PCI call entry, backend lock wait, IO instruction completion and missing return datagram.

## Decision

Do not build/arm another R329 replay or flip watchdog/pstore flags merely because these features exist. Future work must choose and qualify an observation route with independent fault coverage, durable collection, recovery and minimal changed variables. Existing print-only receiver limitation is retained, but it is not grounds to repeat this achieved/failed sequence. Source/binary analysis can continue now; live qualification waits for the user lifting this week's prohibition.

Latest live remains R330 terminal CFG_AFTER_BEGIN/manual reset, not a proven read stall. R335 is the self-contained restart summary, R336 watchdog prerequisites and R337 package readiness. All current stages are published with content verification. No new build, package, install, boot selection, hardware access or reboot. Prior ten-minute limit is historical; the user has resumed static continuation, quota not observable, further live tests this week forbidden.
