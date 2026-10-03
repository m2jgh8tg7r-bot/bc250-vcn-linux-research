# R297 CP07 — read-only PGFSM_STATUS control prepared

Date: 2026-10-03 JST

STAGE=R297 CP07 STATIC / BUILD-ONLY / HOME PACKAGE
RESULT=Read-only control candidate built, audited and installed without selection; not booted.
STATIC_OR_LIVE=PROVEN_STATICALLY
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=UNPROVEN
PROVEN=Source/helper, object, fullmodule, signed-module machine contracts; executable-section identity; archive round-trip. CP05 remains strongest saved PROVEN_LIVE boundary.
REJECTED=CP06 hang alone proves status-read execution or cause; unchanged CP06 retry.
UNPROVEN=CP07 LIVE execution/read value/safety, PGFSM transition, physical power, VCPU, hardware rings, VA-API, FFmpeg decode and stable playback.
NEXT=Manual-menu arm and user-selected CP07 boot, then normal-boot postmortem collection. No automatic LIVE launch.

## Experimental contrast

CP06: PGFSM_CONFIG write -> one PGFSM_STATUS read -> raw log -> panic.
CP07: guards -> one PGFSM_STATUS read without preceding config write -> raw log -> panic.

Only the pre-reset helper changes. The R274B direct-copy path and prior quarantine boundaries remain fixed. The helper retains zero pg_flags/cg_flags and non-VF guards. Its old unreachable tail is removed; no reset release, polling, POWER_STATUS access, SMU VCN power command or ring execution is introduced. This is a cold/normal-boot baseline control, not a readback of the prior failed boot. If a subsequent control returns, that does not by itself prove the CP06 read caused the hang or reveal post-write state.

The compiler inlines the smaller helper into vcn_v2_0_hw_init.cold. Object/fullmodule/signed audits inspect this actual region. Each binary has one device-rreg call site and one alternative SR-IOV-rreg call site, zero wreg/wait call sites, two emergency logs and one panic. These are alternative implementations of one read, not two sequential reads. The machine code uses SOC15 VCN segment base plus PGFSM_STATUS offset 0x1 (BASE_IDX=1). Saved disassembly verifies zero-flag/VF guards and read-return/raw-log/panic flow. Signature metadata and all six executable sections survive packaging unchanged.

The package is derived from the fixed CP06 image. Its round-trip manifest differs only at amdgpu.ko; depmod completed without warnings. No firmware change.

## New hardware operation contract (future LIVE, not executed)

Target: VCN0 mmUVD_PGFSM_STATUS, offset 0x0001, BASE_IDX=1.
Transport: existing RREG32_SOC15 -> amdgpu_device_rreg on guarded non-VF path. No selector or direct write is added.
Before: independently selected research boot, guards satisfied; register/physical island state unknown. No CP07 config write.
Expected after: either one returned raw value reaches its log and intentional panic, or failure to establish that boundary.
Success observation: same-boot CP07 guards marker, raw STATUS marker and CP07 panic, with installed artifact identity verified.
Failure observation: absent returned-value checkpoint, black-screen/hang or absent persistent trace. No trace leaves exact failing instruction UNPROVEN.
Rollback: return to retained normal Bazzite entry; install failure restores verified archived CP06 files. Retire CP07 entry/image only with matching installed identities.
Persistence: no intended register write and no intended persistent firmware change; actual physical effects of read/control boot remain UNPROVEN.
Cold power recovery: forced power or cold-power recovery is a contingency, not proven recovery for CP07. Do not repeat a hanging unchanged experiment.
Earlier proof: CP05 write-return is PROVEN_LIVE; CP07 read without write has never been proven live. CP06 read cause/execution remain UNPROVEN.
Panic: intentional panic follows returned raw-value logging; existing panic=10 applies. An MMIO fabric stall may prevent panic/pstore, as CP06 demonstrates operationally.

## Install preparation

sudo is needed for protected /boot files. Normal boot 7.2.1-ogc4.1.fc44.x86_64 was observed at preparation. Noninteractive sudo requires a password.

/boot currently has about 76MiB available; the new image is about 235MiB. The prepared install retires the fixed CP06 image and its main/select-witness BLS entries only after verified copies are retained locally. It preserves normal Bazzite entries, R180 recovery image/entry, research kernel, grub.cfg and grubenv. It makes no selection change and performs no reboot. The first required user command runs read-only preflight, not the install script. Preflight records protected hashes and stops on stale identities, pending selection, wrong kernel or inadequate post-retirement margin. Install rechecks that snapshot and rolls back on failure. The privileged scripts are syntax checked but have not been executed; their operational behavior remains UNPROVEN.

A package V1 check incorrectly expected a separate .text.unlikely section in the linked fullmodule. Kbuild merges cold code into .text. This tooling assertion was corrected; the V1 log is retained. No hardware failure inference.

## Identities

source SHA-256: `a2aebdfa5bc65e26dd812351da72046ef476cf617cde5914ba0059595683243e`

object SHA-256: `cfda2f5a4372fb7f639b9474ac335f70570b4d7c5150c749aa8dc15deacdaf32`

fullmodule SHA-256: `010d8bfe57ab24e6d7655e8d73313070c0de6c01659993b6361eb4b65cd1c83d`

signed_module_sha256: `fbb5849df514077e75d41a8a3eb46c7f85e62aa7f6f9c82e549c8e3c64bb8ce3`

image_sha256: `a8160d963b7b8b21cf7d9078f157895259944050611abedee2576d670c9ca93b`

bls_sha256: `719e0bfb6f522bfbf3861c1100802e1b4d55d1c70165c72ed2db897ea0fbb501`


## CP07 privileged preflight — 2026-10-03

The user executed the prepared privileged read-only preflight. The saved result was independently read and its script/package hashes matched. Classification: PROVEN_STATICALLY for protected-file identities and capacity checks; no VCN access, boot write, selection change or reboot.

The normal boot, normal pstore policy and absence of pending one-shot selection passed. Free boot space: 78,823,424 bytes. New image: 246,028,802 bytes. Retiring the verified CP06 image plus its main/witness entries allows the 52,428,800-byte margin while retaining the normal and R180 recovery entries.

NEXT=Execute prepared install-no-select via sudo; revalidate all preflight identities, flush verified CP06 backups before deletion, install CP07, verify installed hashes and protected policy. Install has not been executed; CP07 LIVE remains UNPROVEN. The installer now flushes backups before retirement and handles catchable interruption with rollback. Syntax check passed; these recovery paths are not live-proven.

## CP07 installed, not yet LIVE — 2026-10-03

The user executed install-no-select. Saved installed-final-audit is PASS. The installed image and main BLS hashes were independently recomputed and matched the audited package. Three CP06 recovery artifacts were retained in a verified local backup before retirement. Normal entries, R180 recovery, research kernel, grub.cfg and grubenv remained unchanged. Remaining /boot capacity is 78,823,424 bytes. No module load, VCN access, boot selection change or reboot occurred.

Classification: PROVEN_STATICALLY for installed artifact identity. CP07 LIVE remains UNPROVEN.

Manual-menu arm and postmortem collection tools are prepared. Arm rechecks installed/protected hashes and verified CP06 backups, archives and verifies every exposed pstore record before clearing, restores normal pstore policy, then sets only menu_show_once_timeout=30. It never sets next_entry or reboots. On catchable failure it restores the byte-exact grubenv snapshot and normal pstore policy. These privileged recovery paths remain UNPROVEN until executed; source syntax is checked.

The postmortem collector requires return to normal Bazzite. It does not clear pstore or access VCN. It restores the original pstore policy unconditionally and retains raw records locally. Classification requires one record containing ordered helper/guards/raw-value/CP07-panic markers. Six CPU cases passed, including reversed order, missing panic, old-stage markers, no record, and split-record negatives. Split records remain UNPROVEN pending manual correlation; zero pstore does not establish the instruction that stalled.

NEXT=Run manual-menu arm; after its PASS, manually reboot and select the CP07 read-only checkpoint. A returned read should log its raw value and intentionally panic with panic=10. Return to normal Bazzite before collection. A persistent hard hang may still require manual power recovery; CP07 recovery and read safety are not yet proven. Do not repeat an unchanged hanging test. No autonomous reboot or live test has been launched.
