# R350 — no-PGFSM-write PCI-read control installed

STAGE=R350_LIVE_GATE_REACHED_RECEIVER_CAPTURE_FAILED
RESULT=User reports R350 reached local receiver-confirmation prompt; token typed but input remained waiting; normal Bazzite restored
STATIC/LIVE=PACKAGE_STATIC_CHECKS_PASS; USER_REPORTED_LOCAL_GATE_PROMPT; receiver delivery/token acceptance unverified
HARDWARE_ACCESS=AMDGPU_LOAD_NOT_PROVEN; gate precedes modprobe
HARDWARE_MUTATION=NONE_PROVEN
VCN_ACTIVATION=UNPROVEN

## Package and installation

R350 uses the previously audited R328 no-PGFSM_CONFIG-write control module. It performs the planned PCI identity reads, then reaches the named checkpoint panic path. It does not include the R329 PGFSM_CONFIG MMIO write. The read transactions can still hang, and ordinary GPU initialization performs hardware accesses.

Before installation, the user-run protected preflight passed: the normal kernel was still running, GRUB reported a successful normal boot with no pending override, the observed fixed-index default selected a protected normal entry, and all recorded protected file hashes matched. The R350 image and BLS entry matched the package audit. The /boot space check passed with the configured safety margin after retiring the exact R329 image and entry.

The separate install action passed. It backed up the exact R329 image and entry locally, installed R350, and verified the protected hashes. It did not change the boot selection, load a module, reboot, or access hardware. A later user-reported R350 boot reached the local receiver-confirmation prompt; after the user typed the token, the display remained at input wait. The user then returned to normal Bazzite. A subsequent user-run read-only GRUB environment check returned only `boot_success=1`; no pending one-shot menu timeout or next-entry override remained.

## Observation and recovery limits

The running system has `nmi_watchdog=1`, but prior observation did not establish an NMI event. The normal kernel initially had EFI pstore disabled. After the reported trial, EFI pstore was enabled at runtime and the pstore directory remained empty; the normal setting was then restored. No recoverable panic record was found. R350's entry requests hardlockup panic and EFI pstore for that boot, but hardlockup capture remains unqualified. Its intentional panic uses `panic=0`, requiring manual reset. No unchanged R329 CONFIG-write retry is planned.

The local operator procedure requires a fresh raw netconsole capture and receiver confirmation before GPU load. The receiver capture failed due to a reported router problem. The local prompt implies the init passed wired-link setup, netconsole module load and its ten-iteration qualification loop, but does not prove datagram receipt. Token acceptance is unverified. The init calls amdgpu modprobe only after an exact line and a five-second delay, so GPU load, PCI reads and checkpoint panic remain unproven. Do not repeat R350 unchanged until an independent receiver path and console input behavior are understood.

## Next gate

The attempted run is inconclusive. Requalify an independent receiver and console input path before another boot. Preserve raw datagrams and require the receiver's complete qualification sequence before any token is entered. Preserve the entire raw capture.

Even successful PCI reads and the planned checkpoint do not prove VCN power, firmware execution, ring execution, or hardware video decode/encode.
