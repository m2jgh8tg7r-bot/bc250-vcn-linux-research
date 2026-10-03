# R333 — Post-write observation limits and skipped-write premise

STAGE=R333
RESULT=Post-write UDP delivery proves an observed transport event, not PCI post-read outcome or VCN command completion
STATIC_OR_LIVE=Saved-source audit; inherited R330 live markers separated
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Writer skip predicate checks no_hw_access; netpoll can enqueue while returning success; nbcon can decline ownership
REJECTED=Post-write marker receive establishes synchronous completion of its printk call; non-VF macro logically implies runtime-bit clear
UNPROVEN=Actual skipped/write branch, concurrent state changes, trace hook state, terminal CPU location, final datagram completeness
NEXT=Audit exact candidate writer instructions and scheduling/logging relationship; no live retry

## Writer narrowing

amdgpu_device_skip_hw_access in amdgpu_device.c:834–860 returns true only on no_hw_access. Optional CONFIG_LOCKDEP trylock is diagnostic and returns no alternate skip result; this build has no enabled CONFIG_LOCKDEP. Thus R331's unspecified skip possibility narrows to a change of no_hw_access between probe check and writer invocation. R329 logged no_hw=0 and checked that field before the pre-read. This strongly supports an actual write along the ordinary initialization path, but no atomic sampling of that field inside the writer was captured.

SRIOV IS_VF and RUNTIME are separate virt.caps bits. The enclosing non-VF guard is not a logical proof that RUNTIME is clear. Cyan is absent from the supported detect_asic cases and default reg=0; runtime setters examined in amdgpu_virt.c are associated with virtualization callbacks. This supports the normal direct-writel path for bare hardware, but the exact runtime caps byte was not captured. Preserve that qualification rather than mechanically replacing one bit test with another.

## Logging and delivery

netconsole_write at2153–2177 can skip a target, or return when nbcon_enter_unsafe fails. send_udp at1909–1924 classifies drop/allocation errors for optional counters; the dev_emerg caller does not obtain a per-message receiver acknowledgement. netpoll's __netpoll_send_skb at273–332 can queue an skb and schedule delayed work after immediate transmit attempts fail, yet return NETDEV_TX_OK. This is accepted-for-send, not proof of remote receive or physical GPU ordering.

R329's WRITE_RETURN and CFG_AFTER_BEGIN were actually received, strengthening that code/log creation crossed the write-return boundary. A received last marker does not imply the emitting printk call finished: a different CPU or deferred console thread can deliver it, and the producer can still be in logging code, tracing or later execution. Conversely a post-read return record could exist locally without UDP delivery. The code ordering still makes actual execution of the PCI call a candidate, not a proof.

The normal RTL8169 transmit/netpoll callbacks examined use NIC register access and queues. Two PCI configuration read sites found in r8169_main.c belong to configuration/open paths, not evidence that every UDP packet invokes GPU PCI config read. No global fabric health follows from a successful NIC datagram: NIC and GPU are different endpoints. A prior successful pre-read controls basic API functionality in that boot, not every post-write device/bus state.

Terminal receiver line and manual reset are confirmed. R329 has no post-read return or intended panic evidence; logging loss, backend lock wait, PCI IO completion and other CPU contexts remain separate hypotheses. No unchanged test replay or new hardware operation. R332 closes retained linked-kernel text correspondence; R331 holds broader restart constraints. Session deadline18:18:12UTC, user prohibits more live trials this week. Raw receiver file remains unavailable from the displayed print-only command.
