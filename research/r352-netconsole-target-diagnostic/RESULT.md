# R352 pre-GPU netconsole target diagnostic

Status: offline image prepared, not installed. No boot files were changed and no device test was run. Image: `~/bc250-research/research/r352-netconsole-target-diagnostic/initramfs-7.2.3-r352-netdiag.img` (159,058,834 bytes, SHA-256 `d99c23db4d248f1e90aa190b8195749b5dad3aa58c5becee7e4dd6beb37773d9`). The build initramfs tree is local because it contains the host-specific R138 kernel module set.

## Purpose

R351's init checked only whether `/sys/module/netconsole` existed. With `CONFIG_NETCONSOLE_DYNAMIC=y`, the module may load even when `netpoll_setup()` leaves a command-line target disabled. R352 explicitly attaches `cmdline0` to configfs and reads `enabled`, endpoint, device, extended-format, and transmit-error attributes before issuing ten UDP qualification markers.

## Safety boundary

The local R352 initramfs was built from the R351 initramfs tree with the out-of-tree `amdgpu.ko` removed. Its module directory contains no `amdgpu.ko`. The init script contains no `modprobe amdgpu` call, no VCN MMIO access, and no reboot. It holds in the initramfs after reporting the diagnostic result. This experiment diagnoses only NIC/netconsole setup and delivery.

## Interpretation

- `TARGET enabled=0` or a target setup failure localizes the issue to netconsole initialization/configuration before any GPU load.
- `TARGET enabled=1` with correct attributes and receiver-visible `QUALIFICATION` messages proves the early network path for this boot.
- Local `enabled=1` without receiver packets does not by itself prove UDP delivery; compare the Windows raw capture and `transmit_errors`.
- Missing receiver data before target diagnostics is not a VCN result.

## Deployment constraint

The existing `/boot` partition has limited free space and currently has R351 installed. R352 must replace R351 in place while preserving R351's exact image and BLS entry in the user home directory; do not install a second research image alongside it. Installation requires an explicit privileged command by the operator. A guarded in-place replacement, exact R351 backup, and rollback preflight still need to be prepared before any deployment request.
