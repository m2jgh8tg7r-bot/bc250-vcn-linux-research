# R352 pre-GPU netconsole target diagnostic

Status: correction required before the diagnostic is usable. The first R352-labelled boot loaded an initramfs whose embedded `/init` was still R351. This caused the received `R351 NETHOLD` output. The corrected local image is `~/bc250-research/research/r352-netconsole-target-diagnostic/initramfs-7.2.3-r352-netdiag.img` (159,057,810 bytes, SHA-256 `10fbbb6eb15b2d3d9fec7e36d67a8ee2a099f3b927e519cbe10577004b9c55cf`). Its embedded `/init` was inspected and begins with the R352 diagnostic banner. No corrected image has been installed or booted. The build initramfs tree is local because it contains the host-specific R138 kernel module set.

## Purpose

R351's init checked only whether `/sys/module/netconsole` existed. With `CONFIG_NETCONSOLE_DYNAMIC=y`, the module may load even when `netpoll_setup()` leaves a command-line target disabled. R352 explicitly attaches `cmdline0` to configfs and reads `enabled`, endpoint, device, extended-format, and transmit-error attributes before issuing ten UDP qualification markers.

## Safety boundary

Both image iterations were built from an initramfs tree with no `amdgpu.ko`. The initial package mistake was failing to copy R352's `/init` into that tree before archiving it. The corrected image now contains the correct R352 init script, which has no `modprobe amdgpu` call, no VCN MMIO access, and no automatic reboot. The submitted R351 output ends before its local confirmation gate; no token acceptance or VCN read is evidenced. Do not enter the R351 token. Manually reset to normal boot if still at that prompt.

## Interpretation

- `TARGET enabled=0` or a target setup failure localizes the issue to netconsole initialization/configuration before any GPU load.
- `TARGET enabled=1` with correct attributes and receiver-visible `QUALIFICATION` messages proves the early network path for this boot.
- Local `enabled=1` without receiver packets does not by itself prove UDP delivery; compare the Windows raw capture and `transmit_errors`.
- Missing receiver data before target diagnostics is not a VCN result.

## Deployment constraint

The initial image is currently installed under the R352 filename, and the exact original R351 files are retained under `r351-retirement-backup`. Do not boot the current image again. Once normal Bazzite is recovered, `update-corrected-image.py` performs a read-only preflight by default, requires exact hashes of the installed first R352 image and protected files, checks pstore is empty, confirms the normal GRUB environment, and verifies the 50 MiB post-replacement margin. Its explicit `--install` saves the current image to `r352-initial-bad-build-backup` before replacing it, with rollback on reported errors.

After returning to normal Bazzite, the next commands are the protected read-only preflight:

```sh
sudo sysctl -w kernel.nmi_watchdog=1
sudo python3 ~/bc250-research/research/r352-netconsole-target-diagnostic/update-corrected-image.py
```

Do not add `--install` until this correction preflight reports PASS and its result has been reviewed. The prior `MENU_RESULT.json` is retained; after corrected installation, verify it and use `arm-menu-retry.py` to make a new manual menu selection. Windows raw UDP capture must be running before reboot.

After a successful replacement, `verify_installed.py` performs the protected read-only check. `arm-menu.py` then creates a fresh GRUB environment backup and shows the menu for 30 seconds, requiring the operator to select R352 manually. It does not reboot or set `next_entry`. Start the Windows raw UDP receiver before arming/rebooting. At R352, inspect the local `TARGET` report and the Windows capture; do not expect a prompt/token and do not select another VCN experiment from this boot.
