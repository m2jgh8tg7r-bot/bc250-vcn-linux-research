# R291 P7B LIVE blackout / local observability result

Date: 2026-10-02

## Scope

This note records the first limited LIVE boot observations after P7A. It separates what was directly observed from what remains unknown.

## LIVE observations

- A manual boot of the R291 research entry reached the custom amdgpu VCN early-init instrumentation on screen.
- The following markers were visually observed before display loss:
  - `BC250 R141 early_init_begin ret=0`
  - `BC250 R141 early_init_end ret=0`
- The display then went black around the simple-framebuffer -> amdgpu DRM/KMS handoff.
- This does **not** prove that R274B direct-copy, VCN sw_init, R291P1 pre-reset, reset release, firmware first-fetch, or VCN execution occurred.
- The last visible console line must not be treated as the exact kernel stall point.

## Persistent-journal limitation

The R291 blackout boot did not leave a usable persistent journal boot record before forced recovery. Later `journalctl -b -1` entries were from an older normal 7.2.1 Bazzite boot, so absence of R291 markers there is not evidence that the R291 kernel never booted.

## Local-only EFI pstore validation on normal Bazzite

A local-only crash-recovery path was validated independently:

- `CONFIG_EFI_VARS_PSTORE=y` and `CONFIG_PSTORE=y` are present.
- Runtime `pstore_disable` can be changed from Y to N.
- After enabling it, the backend reports `efi_pstore`.
- Keyboard Magic SysRq HELP was observed on the normal kernel.
- A controlled SysRq crash produced a kernel panic and automatic reboot.
- After re-enabling efi_pstore on the next normal boot, 17 `dmesg-efi_pstore-*` records were recovered.
- The recovered dump contained `sysrq: Trigger a crash`, `Kernel panic - not syncing: sysrq triggered crash`, and the crash call trace.

This proves the board/firmware/kernel combination can persist panic dmesg through EFI pstore in a controlled normal-boot test.

## R291 PSTORE attempt

A dedicated R291 boot entry was prepared with:

- `efi_pstore.pstore_disable=N`
- `sysrq_always_enabled`
- `panic=10`

Old pstore records were cleared before the test.

After R291 blackout, `Alt+PrtSc(SysRq)+C` did **not** cause the expected panic/reboot. Recovery to normal Bazzite showed:

- efi_pstore can still be registered normally,
- `/sys/fs/pstore` contained zero new records,
- no matching `dump-type0-*` EFI variables were present.

Therefore this attempt does **not** localize the R291 stall. The important result is that an external keyboard-triggered panic is not a reliable observation mechanism after this blackout.

## Next observation strategy

Replace post-blackout keyboard SysRq with an internal checkpoint panic. The first checkpoint (R297 CP01) is placed immediately after the already-LIVE-proven `R141 early_init_end` marker. This adds no new VCN register sequence and should panic before VCN sw_init, R274B direct firmware provisioning, and R291P1 pre-reset programming.

## Evidence boundary

Proven LIVE:
- custom R291 amdgpu reaches VCN `early_init_begin/end ret=0` visually,
- EFI pstore controlled-panic persistence works on the normal Bazzite kernel,
- keyboard SysRq works on the normal Bazzite kernel.

Not proven LIVE:
- R274B direct-copy in the R291 blackout boot,
- R291P1 helper entry/return,
- any reset-release or VCN execution,
- that the blackout itself is a kernel hang rather than display loss followed by a later stall.
