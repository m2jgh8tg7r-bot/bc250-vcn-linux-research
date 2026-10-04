# R352 initramfs correction

The first R352-labelled initramfs was assembled from the R351 tree without copying the standalone R352 `init` into `initramfs-tree/init`. The BLS entry and kernel image were correct, but the initramfs executed the stale R351 NETHOLD script. The Windows capture `R351 QUALIFICATION 6/10–10/10` and `INPUT_READY` exposed the discrepancy.

The submitted data shows no later R351 `INPUT_RESULT` or `AMDGPU_MODPROBE_BEGIN`. The initramfs module tree had no `amdgpu.ko`, and the kernel configuration has `CONFIG_DRM_AMDGPU=m`; no VCN read is evidenced. Do not enter the R351 token. If still at that prompt, manually reset to normal Bazzite.

The corrected tree now includes the R352 `/init`. The corrected gzip image is 159,057,810 bytes with SHA-256 `10fbbb6eb15b2d3d9fec7e36d67a8ee2a099f3b927e519cbe10577004b9c55cf`. Direct extraction showed the R352 banner; an archive listing found no `amdgpu.ko`.

The current `/boot` still has the first, incorrect image. After recovering to the normal kernel, run the read-only correction preflight:

```sh
sudo sysctl -w kernel.nmi_watchdog=1
sudo python3 /var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic/update-corrected-image.py
```

Only if that reports PASS should the operator review it and run the same script with `--install`. Then rerun `verify_installed.py`, start Windows capture, and use `arm-menu-retry.py` before manually selecting R352. The first menu result is historical and does not validate the corrected image.
