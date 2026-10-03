# R318 — Panic-hold observation package

STAGE=R318
RESULT=Prepared locally; not installed or booted
STATIC_OR_LIVE=Offline artifact and package checks
HARDWARE_ACCESS=NONE during preparation
HARDWARE_MUTATION=NONE during preparation
HARDWARE_FAILURE=UNPROVEN
PROVEN=Kernel executable sections match extracted research image; compiled zero-timeout branch skips restart; package roundtrip exact; modules and firmware unchanged
REJECTED=This already proves a received panic or VCPU execution
UNPROVEN=Live final flush, actual R311 checkpoint, R316 reset cause
NEXT=Privileged read-only preflight, review, installation, fresh receiver and manual menu preparation

## Evidence and change

The retained research boot kernel hash is c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6. Its extracted ELF executable-flagged sections match retained vmlinux (KERNEL_AUDIT.json). In retained vpanic, a zero-timeout branch at 0xffffffff8120f331 skips emergency_restart at 0xffffffff8120f344 and reaches the path containing nbcon_atomic_flush_unsafe at 0xffffffff8120f36d. This closes the previously unverified executable-code correspondence for this artifact; it is not a new live control-flow observation.

R318 retains every R316 module/firmware byte. Inside initramfs only init changes, solely R316/NETEXT identification to R318/NETHOLD. The BLS options change only panic=10 to panic=0. Extended output, manual confirmation, firmware staging and R311 panic checkpoint remain unchanged. No new VCN register access or security-policy operation is added. The final unsafe flush is the kernel's existing path, not a removed safety flag.

Archive extraction matches the complete file/link/directory-mode manifest. Gate tests pass 11, normal-default tests 13, include tests 14. Original R316 tree remains unchanged. Installer preserves the normal boot selection and backs up the exact R316 entry/image before replacement; installation and menu preparation are separate from reboot.

## Experiment and recovery contract

Target: research-kernel panic timeout only, via the R318 BLS options. Expected before: panic=10. Expected after: panic=0 on this explicitly selected boot. The normal entry is not changed. This option persists only when the research entry is selected.

Success observation: receive R311 META plus the named intended panic; this proves only the checkpoint and reported software fields, not VCPU execution. A different panic identifies an alternative failure path. Another absent suffix is inconclusive and should end this line of repeated observation trials. Unexpected automatic reboot with panic=0 is a distinct observation to record, not immediate proof of hardware failure.

The kernel may remain stopped after panic; automatic recovery is deliberately disabled. Keep the receiver saving to a new file for this boot only. After the expected terminal logs, allow about 60 seconds for any delayed output; this is an observation interval, not a timeout guarantee. Preserve the receiver file, then use the physical reset control to return to the normal entry. If reset is unavailable or ineffective, power-cycle the machine. The research init does not mount the normal root filesystem. Cold-cycle behavior for this exact variant has not been proven. Do not keep repeating the test if the result remains ambiguous.

Rollback: normal entry remains the default; installer retains R316 backups. No autonomous reboot, module loading or new MMIO operation was performed while preparing this package. User authorized resuming hardware tests after the earlier pause.
