# R350 — no-PGFSM-write PCI-read control installed

STAGE=R350_MENU_ARMED_AWAITING_RECEIVER_AND_MANUAL_BOOT
RESULT=R350 image and BLS entry installed, independently verified, and one-time menu armed; no boot or reboot yet
STATIC/LIVE=PACKAGE_STATIC_CHECKS_PASS; INSTALLATION_LIVE_STATE_PASS
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
VCN_ACTIVATION=UNPROVEN

## Package and installation

R350 uses the previously audited R328 no-PGFSM_CONFIG-write control module. It performs the planned PCI identity reads, then reaches the named checkpoint panic path. It does not include the R329 PGFSM_CONFIG MMIO write. The read transactions can still hang, and ordinary GPU initialization performs hardware accesses.

Before installation, the user-run protected preflight passed: the normal kernel was still running, GRUB reported a successful normal boot with no pending override, the observed fixed-index default selected a protected normal entry, and all recorded protected file hashes matched. The R350 image and BLS entry matched the package audit. The /boot space check passed with the configured safety margin after retiring the exact R329 image and entry.

The separate install action passed. It backed up the exact R329 image and entry locally, installed R350, and verified the protected hashes. It did not change the boot selection, load a module, reboot, or access hardware. The normal boot entry remains the default.

## Observation and recovery limits

The running system has `nmi_watchdog=1`, but prior observation did not establish an NMI event. The normal kernel has EFI pstore disabled and the observed pstore directory was empty. R350's entry requests hardlockup panic and EFI pstore for that boot, but neither hardlockup capture nor post-reset pstore persistence is qualified. Its intentional panic uses `panic=0`, requiring manual reset. No unchanged R329 CONFIG-write retry is planned.

A local operator procedure is prepared for a fresh raw netconsole JSONL capture, independent installed-state verification, a one-time GRUB menu, manual R350 selection, receiver confirmation before GPU load, and manual recovery. The receiver is not yet confirmed running; the 30-second one-time menu is armed with no next-entry override; R350 is not booted.

## Next gate

The root-only read-only installed-state verifier and one-time menu preparation have both passed. Start and validate the independent receiver before rebooting, then select R350 manually. Wait for all qualification markers on the receiver before entering the local confirmation token. Preserve the entire raw capture.

Even successful PCI reads and the planned checkpoint do not prove VCN power, firmware execution, ring execution, or hardware video decode/encode.
