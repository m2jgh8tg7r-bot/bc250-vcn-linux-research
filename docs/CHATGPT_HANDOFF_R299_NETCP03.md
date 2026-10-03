# R299 NETCP03 — network-first, receiver-gated CP03 control

Date: 2026-10-03 JST

STAGE=R299 NETCP03 STATIC / HOME PACKAGE
RESULT=PROVEN_STATICALLY package and gate checks; privileged preflight not executed; not installed or booted.
STATIC_OR_LIVE=PROVEN_STATICALLY
HARDWARE_ACCESS=NO new GPU/VCN access
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=Exact retained CP03 signed module identity, clean depmod, module dependency resolution, gzip validation and exact archive hash/mode/symlink round-trip; receiver gate mock tests 4/4.
REJECTED=R298 qualification proves GPU-stage or hang-time delivery; CP03 control proves VCN execution; this is a repeat of failed CP07.
UNPROVEN=Isolated CP03 boot reaches prior live boundary, GPU-stage netconsole delivery, recovery from this image, privileged installation and rollback behavior, VCN status read or execution.
NEXT=User-run privileged read-only preflight. After PASS, no-selection installation and exact final audit. Notify before manual-menu preparation and boot. No automatic boot.

## Design and discrimination

R298 NIC/PHY/netconsole sequence precedes any amdgpu loading. Ten unique R299 qualification markers are emitted. The RAM-only console then requires exact token `R299-CP03-RECEIVED`, entered only after Windows saves the completion marker. Wrong input, EOF, or pre-existing amdgpu holds without loading GPU. Valid input emits a confirmation marker, waits five seconds and emits AMDGPU_MODPROBE_BEGIN before explicitly loading the retained CP03 amdgpu module with dc=1. No udev/systemd/autoprobing or disk-root mount is included.

CP03 intentionally panics after the Cyan hw_init P1-begin marker and before the pre-reset helper. Saved linked disassembly has dev_info, dev_emerg and panic calls in that cold block with no helper/read/write call before panic. Earlier CP03 reached this boundary live in the original environment; the new RAM-only environment remains unproven. Prior amdgpu initialization still accesses GPU hardware and provisions firmware; this is not a no-hardware observation boot. No PGFSM_CONFIG write or PGFSM_STATUS read is introduced at the tested helper boundary.

The complete retained CP03 firmware set is copied unchanged to avoid an unvalidated reduced firmware list. Existing R274B/direct-copy and quarantine behavior remains in the unchanged module. The standalone boot changes userspace initialization and omits original root/OSTree and mitigations=off options; it is an observation control, not proof of exact failed-CP07 conditions.

Possible outcomes: qualification only narrows coverage to pre-GPU; modprobe-begin identifies the load launch but not driver entry; P1-begin plus CP03 emergency/panic markers establishes streaming at the intended pre-helper boundary. A missing later marker leaves transport/driver/panic ambiguity. Panic=10 acts only if panic handling proceeds. A normal panic reboot is expected but not guaranteed; manual physical recovery may be needed. Do not repeat an unchanged hanging control.

## Operation contract for future user-selected boot

Target: existing CP03 amdgpu initialization ending before the Cyan VCN pre-reset helper.
Transport: explicit modprobe after qualified netconsole and local receiver confirmation.
Before: installed artifact identity audited, normal/recovery entries retained, Windows file logging ready; no amdgpu loaded in standalone init.
After: externally visible CP03 checkpoint/panic, or classified incomplete coverage.
Rollback: panic timeout if operational, otherwise manual return to retained normal entry; CP07 files have verified local backups before retirement. Catchable installer failures restore retired files. Power-loss/uncatchable rollback is not guaranteed.
Persistence: new R299 BLS/image replaces archived CP07 BLS/image only; no GRUB selection mutation, disk-root mount, EFI pstore write or intended persistent device setting.
Cold-power recovery: contingency requiring physical action; unproven for this image.
Earlier proof: R298 network path and original CP03 checkpoint, separately; their combined path is UNPROVEN.

## Validation and install readiness

Image bytes: 168061706 (approximately 160.3 MiB). Current nonprivileged /boot free observation approximately 66 MiB; direct additive installation is insufficient. Prepared default read-only preflight verifies protected boot hashes, exact CP07 retirement identities, absent pending menu/selection, normal kernel/pstore policy and 50 MiB post-install margin. Installer archives and verifies CP07 before removing only its image/BLS; retains normal, R180, R298, kernel and GRUB files. It creates no selection and performs no module load/reboot. Python syntax and shell syntax passed; privileged execution and rollback remain UNPROVEN. Noninteractive sudo requires a password, so agent did not execute the protected preflight.

Mock gate checks: wrong token, EOF and already-present GPU all prevent mocked modprobe; valid token permits one mocked modprobe and records unexpected return without retry. Sysfs guard and commands were mocked; no module was loaded.

image_sha256: `a7099cfcf102cb8eb1ba61832e1456a886b104c893a7788376338eb21112df74`
bls_sha256: `aa393aaade9a9b0dc5970c894f2c03cdd03aff8b8f38bf334233d00b0fb3a0d3`
init_sha256: `d577454d3b42e9a3306a71923517473c836361db74f144ef1ba088f086e55b79`
cp03_signed_module_sha256: `43f177df38a8d4bef6572fcaca89c6d0f1f6165fd8983ee3ce62d019ec7c3d9a`


## Privileged read-only preflight PASS — 2026-10-03

User executed the default privileged preflight. Saved contract PASS was independently read; installer/package/image/BLS/init identities matched current HOME artifacts. Protected normal/R180/R298/kernel/GRUB identities and exact CP07 retirement identities passed. Free space was 68,395,008 bytes; planned new image 168,061,706 bytes; verified CP07 retirement permits the required 52,428,800-byte post-install margin. No boot write, selection change, GPU module load or reboot.

NEXT=User-run `install.py --install`: archive and verify CP07, replace only its image/BLS with R299, preserve protected identities, and save installed audit. Installation and combined LIVE control remain UNPROVEN.


## Installed and independently audited — 2026-10-03

User-run install returned PASS. Agent independently recomputed installed image/BLS and archived CP07 image/BLS hashes; all matched audited identities, and original CP07 paths are absent. Saved protected hashes match the preflight; privileged installer reports protected identity preservation. No selection, module load or reboot. Prepared manual-menu script rechecks all installed/protected hashes, normal kernel and absent pending selection, then sets only one-time 30-second menu timeout, with verified grubenv backup and catchable rollback. Script syntax passed; menu preparation is not yet executed.

NEXT=Receiver file logging ready; user runs arm-menu.py. After PASS, user manually reboots and selects R299. Confirm Windows saved R299 QUALIFICATION_COMPLETE before typing R299-CP03-RECEIVED at the BC-250 console. This initiates GPU initialization and an expected CP03 panic before the VCN helper; panic=10 may reboot if panic handling proceeds. If qualification is absent, do not enter the token; use reboot -f from the RAM shell and normal entry. Unexpected load return holds without retry. Combined live path and hang-time delivery remain UNPROVEN.
