# R338 — Serial observation feasibility and prerequisites

STAGE=R338
RESULT=Serial output is a possible distinct transport but existing package does not arm it; physical connectivity and fault coverage remain unqualified
STATIC_OR_LIVE=PROVEN_STATICALLY retained config/source; supplied boot UART enumeration separated
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=8250 console/polling/serial SysRq compiled; R329 console argument selects tty0; ordinary console write locks port while oops path uses trylock; serial code touches NMI watchdog
REJECTED=ttyS0 enumeration proves an accessible wired receiver; serial output is immune to all console/IO stalls
UNPROVEN=Physical connector/pinout/electrical levels, port ownership, configured receiver, reliable capture, sampling-to-UART fault independence
NEXT=Static observation-design preservation; no serial console enabling, physical wiring request or live trial this week

## Capability versus prepared route

Config enables SERIAL_8250_CONSOLE, SERIAL_CORE_CONSOLE, CONSOLE_POLL and MAGIC_SYSRQ_SERIAL. Supplied boot log enumerates ttyS0 at IO0x3f8/IRQ4 as a16550A. This is device enumeration, not proof that a physical header is exposed, safe voltage levels/pinout are known or an external receiver is connected. Do not infer them from the standard port address or board name. R329 entry selects console=tty0 only; no serial console activation was performed.

Serial8250's console-write path uses polled transmitter status and UART IO, so eventual transmit does not inherently require a transmit-completion interrupt. This could avoid NIC/UDP queue dependencies. It still needs the UART/CPU/interconnect and printk console path to function. The ordinary path acquires the UART port lock with IRQ saving; when oops_in_progress it instead tries the lock and may continue without acquiring it. This is a distinct dependency, not universal fault immunity. Adding it also changes timing and platform accesses.

wait_for_xmitr uses status polling and optional bounded flow-control loops. A bounded loop cannot guarantee return if an individual underlying port/register access stalls. The flow-control wait and console-write entry call touch_nmi_watchdog; thus extra serial output can interact with watchdog detection timing and must not be treated as an entirely passive sampler.

## What a future qualified route would require

Before proposing a changed live condition, establish actual physical availability, known electrical interface/ownership, external byte-preserving receive path, idle/normal-test capture, and whether the selected failure leaves this transport and panic/NMI console path functional. These are prerequisite categories, not instructions to wire unknown headers or start another test now. One must distinguish normal output qualification from NMI/fault output qualification. UART detection alone does neither.

A captured sampled RIP could distinguish printk, backend lock or IO boundaries if reliably associated with the affected CPU/boot; a second copy of BEGIN alone would still not prove PCI call entry. Serial adds another transport but does not by itself generate an independent program-counter sample.

No builds, images, boot-option changes, watchdog/pstore changes, hardware accesses or live trials. Current R329 remains installed; terminal CFG_AFTER_BEGIN and manual reset are the last live evidence. R335 holds the self-contained continuation summary, R336 watchdog limits, R337 persistent-path readiness and R338 serial feasibility. User's no-more-live-tests-this-week instruction persists; static continuation is authorized, quota not observable. Stage is published and remote content checked for interruption-safe continuation.
