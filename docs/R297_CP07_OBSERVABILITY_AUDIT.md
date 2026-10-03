# R297 CP07 postmortem and observation coverage audit

Date: 2026-10-03 JST

STAGE=R297 CP07 POSTMORTEM / STATIC OBSERVATION AUDIT
RESULT=User reports CP07 selection, persistent blackout, manual reboot. Salvage succeeded with zero exposed pstore records. EFI pstore does not continuously preserve pre-read printk messages in the audited configuration.
STATIC_OR_LIVE=PROVEN_STATICALLY (logging mechanism); UNPROVEN (CP07 execution boundary)
HARDWARE_ACCESS=NO new VCN access
HARDWARE_MUTATION=NO new hardware or boot changes
HARDWARE_FAILURE=UNPROVEN
PROVEN=Saved collection reports no records, no deletion, restored pstore policy Y and normal-kernel return. Source identifies a panic-dependent dump path and DMESG-only EFI backend. CP05 remains the strongest saved LIVE write-return checkpoint.
REJECTED=Zero pstore proves the status read stalled; absent ARM_RESULT proves hardware failure; enabling pstore after reboot reconstructs unpersisted logs.
UNPROVEN=CP07 kernel/module entry, helper/guards/read-return/panic, exact failing instruction, physical power, VCPU/rings and decode.
NEXT=Prepare an independently validated streaming observation transport before any further read experiment; do not retry unchanged CP07.

## What was observed

The user selected CP07, saw sustained blackout and rebooted. No ARM_RESULT or preboot baseline exists. Collection on normal kernel 7.2.1-ogc4.1.fc44.x86_64 returned records=[] and persisted_trace=NONE. No GRUB next_entry was present in the saved environment. Collection did not delete pstore. Current normal boot logs show EFI pstore registration/unregistration during collection. Normal boot's systemd-pstore service was skipped for an empty directory; its local archive directory was also empty at inspection. This excludes an existing archive at that inspection, not every possible failed-boot logging outcome.

## Static chain and limits

Audited saved build-tree sources:

- vcn_v2_0-r297-cp07.c: Cyan hw_init enters helper; helper logs entry, checks flags/VF, emits emergency guards marker, performs one status read, emits raw-value marker, then calls panic.
- drivers/firmware/efi/efi-pstore.c: backend flags are PSTORE_FLAGS_DMESG. Initialization requires EFI write support and enabled policy; allocation/registration can also fail. EFI record write can return EBUSY or firmware error.
- kernel/panic.c: kmsg_dump_desc(KMSG_DUMP_PANIC, ...) occurs after crash handling, other-CPU shutdown and panic notifiers. Even entering panic is not a guarantee that persistent writing completes.
- fs/pstore/platform.c: the dump callback takes a buffer lock; nonblocking paths may skip on contention. It consumes a kmsg dump rather than streaming every dev_emerg message into EFI.
- Saved .config: EFI pstore=y, default disabled=y, PSTORE_CONSOLE/PMSG/FTRACE disabled; RAM backend=m; netconsole=m; serial console=y; lockup detectors enabled.
- Prepared BLS enables efi_pstore.pstore_disable=N and panic=10 and preloads NIC/amdgpu. The panic timeout applies after panic, not to arbitrary stalled MMIO. Lack of arm did not remove this BLS parameter; arm mainly establishes a clean baseline and one-shot menu. Runtime CP07 parameter application remains unobserved.

These are saved-source/config conclusions, not proof that the failed boot executed those binaries or enabled the backend. CP05 previously persisted ordered write-return/panic markers. That supports the prior mechanism under CP05 conditions, not guaranteed capture for CP07.

## Candidate observation methods

| Method | What it could establish | Prerequisites and limits |
| --- | --- | --- |
| Initramfs netconsole before amdgpu | External receipt of entry/guards/raw markers without waiting for panic | A separate receiver and demonstrated NIC/netpoll readiness; load and validate before amdgpu. UDP loss and whole-fabric stalls remain possible. Current BLS preloads amdgpu, so simply appending netconsole is insufficient to prove ordering. |
| Independent serial console | External streaming logs before the attempted read | Confirm actual UART hardware, wiring and receiver; saved serial-console config alone proves none of these. |
| Console-enabled reserved RAM backend | Continuous logs surviving a supported warm reset | Current CONFIG_PSTORE_CONSOLE is disabled. Requires kernel/config change and safely reserved memory with demonstrated retention; cold power loss may erase it. Do not invent a physical address. |
| CPU watchdog panic | Possible timeout-derived dump | Detector configuration is not live coverage. Fabric stalls, NMI delivery and panic completion remain unproven; it cannot be treated as a reliable escape. |

Preferred next design is an observation-only initramfs netconsole qualification that does not enter the unproven VCN read path. It must demonstrate receiver delivery before GPU initialization and use a separate test entry. Receiver availability is currently unknown; no boot artifact or privileged install was made. Another status-read test is not ready.

The purpose is to recover a pre-read witness and distinguish boot non-entry from helper entry; receipt of guards alone would still not prove the following MMIO instruction completed. A missing packet alone remains negative evidence with incomplete coverage.
