# R332 — Linked kernel PCI correspondence

STAGE=R332
RESULT=PCI wrapper/backend linked instructions correspond to retained extracted research-kernel text
STATIC_OR_LIVE=PROVEN_STATICALLY
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Retained vmlinux .text equals prior extracted kernel .text; linked PCI functions preserved
REJECTED=PCI_LOCKLESS_CONFIG alone removes backend pci_config_lock
UNPROVEN=Runtime bus-op pointer/lock ownership, stopped instruction and post-read hardware completion
NEXT=Trace CONFIG skip/virtualization conditions and netconsole delivery limits using saved artifacts only

## Correspondence closed

R331 object-only evidence is strengthened: all .text bytes from the retained R328 vmlinux and prior R318 extracted research kernel match SHA2561f2968332a5846ab3a4158a573b4680c405c7fbd84f0e7bba94c90fc5ee72b9d. R329 installed preflight preserved the research-kernel hash. This is artifact provenance, not a fresh privileged kernel read or proof of runtime alternatives/ftrace patch state.

Linked pci_read_config_dword, pci_bus_read_config_dword, raw_pci_read and pci_conf1_read instructions are preserved in LINKED_PCI_FUNCTIONS.disasm. The lockless bus wrapper indirectly dispatches bus ops. Conventional raw dispatch uses base ops for domain0/offset0. Type1 code retains its separate lock and CF8/CFC IO. The boot's type1 message is emitted directly before assigning raw_pci_ops to pci_direct_conf1 in retained init source; ACPI root creation selects pci_root_ops. This strengthens conventional type1 dispatch inference while leaving later override and runtime pointer unattested.

Live boundary remains R329 pre-read ret0 matching13fe1002, write-return, terminal post-read begin; manual reset confirmed. No post return/panic. No VCN execution claim, unchanged replay or new hardware test. User's ten-minute static session ends18:18:12UTC; more live tests this week remain forbidden. R331 remains the broader continuation contract; read any newer numbered handoff before resuming.
