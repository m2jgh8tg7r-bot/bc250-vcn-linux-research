# R298 NETOBS1 — pre-GPU network observation qualification prepared

Date: 2026-10-03 JST

STAGE=R298 NETOBS1 STATIC / HOME PACKAGE
RESULT=Standalone observation-only initramfs prepared; not installed or booted. Normal-boot netconsole external receipt is proven; research-kernel early-boot coverage is not.
STATIC_OR_LIVE=PROVEN_STATICALLY (package); PROVEN_LIVE (prior normal-boot transport)
HARDWARE_ACCESS=NO during preparation
HARDWARE_MUTATION=NO during preparation
HARDWARE_FAILURE=UNPROVEN
PROVEN=Shell/Python syntax, module vermagic/signatures and dependency resolution, warning-free depmod after modules.order correction, compressed archive validation and exact hash/mode/symlink round-trip. amdgpu absent from archive; saved kernel config makes amdgpu modular.
REJECTED=Prior delayed Windows display establishes netconsole failure; source-side tcpdump absence proves no netpoll delivery; replayed early timestamps prove early live coverage.
UNPROVEN=This image boots, research-kernel NIC/netpoll operation, link/receiver readiness, keyboard recovery, next VCN-read boundary and hang-time log delivery.
NEXT=Privileged read-only preflight, then no-selection install after PASS. Receiver file logging and manual-menu preparation before any user-selected observation boot. No automatic hardware launch.

## Prior receiver evidence and correction

Windows displayed netconsole marker triplets from the first and second normal-boot attempts after Esc released the console state. Initial no-display reports are superseded. Terminal selection pause is consistent with the sequence, not independently inspected. Verbosity increase is not proven necessary for emergency markers. The large received normal-kernel dump is buffered replay; it does not indicate a new boot. Raw messages contain machine identifiers and remain local.

## Independent observation-only design

The image has its own /init shell, no systemd or udev startup, no automatic module probing and no amdgpu module. It uses the retained research kernel. Early built-in kernel/simpledrm initialization still runs. The init mounts only proc/sysfs/devtmpfs, loads Realtek PHY and wired NIC modules, finds the known wired PCI device, brings it up with the locally configured fixed sender address, and waits up to 30 seconds for carrier. It then loads netconsole with the locally configured receiver address/MAC and emits ten unique R298 NETOBS1 QUALIFICATION markers plus a completion marker. Failures hold at a recovery shell; successful acquisition also holds. No disk root mount, VCN firmware provisioning, VCN MMIO, panic, automatic GPU load or automatic reboot is introduced.

Addresses/MACs are kept in local configuration and omitted from publication. DHCP changes require revalidation and rebuilding. User manually returns to normal Bazzite. Actual recovery remains unproven until the qualification boot.

Image is approximately 9.9 MiB; current nonprivileged capacity observation was approximately 76 MiB. Privileged preflight enforces a 50 MiB remaining margin with no retirement of existing images. Installation adds only a new image and new BLS, preserves normal/recovery/CP07 artifacts and GRUB policy, and makes no selection. Menu preparation sets only a transient 30-second manual menu, never next_entry, and does not archive/clear pstore. Removal checks exact installed identities. Prepared catchable-failure rollback is source-reviewed, not live-proven.

## Future operation contract

Target: normal research-kernel boot, existing wired NIC/PHY and netconsole/netpoll; no amdgpu/VCN module path.
Transport: kernel module initialization, standard ip link/address, and module netconsole parameter; same external UDP receiver proven under normal kernel.
Before: normal Bazzite, installed-file hashes verified, receiver listening without terminal pause, wired cable connected; research-kernel network coverage unknown.
Expected after: externally received unique R298 markers while amdgpu remains absent; local shell waits.
Success observation: receiver-file R298 markers identify research kernel and amdgpu absence; current test is distinct from prior buffered normal-kernel messages.
Failure observation: local explicit FAIL or no qualified external markers; absence does not identify a failing instruction.
Rollback: manual reboot from RAM-only shell to retained normal entry; no persistent root change. Remove only exact R298 artifact identities after return.
Persistence: optional BLS/image installation only; IP/module state volatile; EFI pstore stays disabled; no automatic firmware-variable writes requested by the test.
Cold-power recovery: manual power recovery is contingency, not demonstrated for this image. Do not repeat unchanged failed/hanging boot.
Earlier proof: NIC and netconsole externally proven under normal kernel; this standalone research-initramfs sequence never live-proven.

## Limits

A successful qualification only proves this research-kernel streaming path before GPU initialization. It does not prove a later GPU/fabric stall will permit packet emission. No CP07 retry is embedded. Future VCN experiment needs separately reviewed code/order, a new unique marker and artifact identity.

## Package identities

image_sha256: `a9092017ac2a0952531c608cf61f1788aa3dd874e6f74836cc638f163253eb6e`

image_size: `10422780`

bls_sha256: `fda55fab50c51cf0704732519217b46c3ab3eff502cfe9f6f5acd6f99372ce37`

init_sha256: `3dda67d141788c1e08530c320e12a0306e12dcba35f5c13e00977f10eafbf388`

research_kernel_sha256: `c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6`



## R298 NETOBS1 live result — 2026-10-03 (supersedes preparation status)

STAGE=R298 NETOBS1 LIVE QUALIFICATION
RESULT=PROVEN_LIVE research-kernel pre-GPU external marker receipt; user reports normal reboot after observation.
STATIC_OR_LIVE=PROVEN_LIVE (user-supplied Windows receiver excerpt); current normal kernel independently read as 7.2.1-ogc4.1.fc44.x86_64.
HARDWARE_ACCESS=User ran observation boot; agent performed only post-return uname and filesystem/Git inspection.
HARDWARE_MUTATION=NIC/netconsole initialization during user-run boot; no VCN access in reviewed init; no new agent hardware mutation.
HARDWARE_FAILURE=NO_EVIDENCE in supplied excerpt.
PROVEN=Unique QUALIFICATION 2/10 through 10/10 received at 6.454454 through 14.478145 seconds, each reporting kernel=7.2.3+ amdgpu_absent=YES no_VCN_access; QUALIFICATION_COMPLETE at 15.480975 seconds. Successful return reported by user, with normal kernel confirmed locally.
REJECTED=Research-kernel network transport categorically unavailable; early timestamps alone prove immediate early-boot delivery; this excerpt proves lossless logging.
UNPROVEN=QUALIFICATION 1/10 receipt, complete kernel log receipt, packet-loss cause, receiver file durability, loaded-image live hash attestation, GPU/fabric hang-time packet delivery, VCN read completion and VCN execution.
NEXT=Review a fresh instrumentation boundary with unique immediately-before/after markers and an external receiver acknowledgement before any VCN experiment. No unchanged CP07 retry or automatic boot.

The excerpt includes the receiver-ready line, early kernel messages through approximately 0.242737 seconds, then QUALIFICATION 2/10 onward. QUALIFICATION 1/10 and the intervening kernel messages are absent from the supplied excerpt. This is a coverage gap, not evidence identifying packet loss, terminal clipping, or any particular failing instruction. The early messages can be buffered replay after netconsole registration; the unique periodic R298 markers establish the live post-registration path. The /vmlinuz-7.2.3-r138 command-line name is consistent with the retained research kernel, while R298 identifies the independent initramfs test.

Next-test constraints: retain the qualified NIC path; establish external receipt before experimental access; use a new stage/attempt identifier and bounded pre-access pause; emit emergency-priority markers immediately before and after the single access. A received before marker without after marker narrows the last observable boundary but cannot distinguish an access stall from subsequent netpoll/receiver failure. CPU heartbeat and local console observations, if added, require a separate static review. The qualification does not make a GPU/fabric hang observable by itself. No new boot selection, installation, VCN read/write, or reboot was performed in this result review.
