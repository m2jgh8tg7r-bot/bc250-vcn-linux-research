# R353 gated status-read trial design

## Current R351 attempt result (2026-10-05)

The operator returned to the normal Bazzite kernel (`7.2.1-ogc4.1.fc44.x86_64`). The pstore directory was empty, the Windows UDP receiver recorded no R351 messages, and the operator confirms that `R351-STATUS-READ` was not entered. The R351 token gate therefore did not open; this attempt provides no VCN STATUS-read observation. An empty pstore is not evidence that no panic occurred.

## Change for R353

R353 combines the proven R352 early-boot UDP/configfs diagnostic with the guarded R351 module and its existing manual token boundary. Before a token is presented, initramfs checks that:

* the expected research kernel is running and `amdgpu` is absent;
* wired PCI device `0000:04:00.0` is present and has carrier;
* the netconsole configfs command-line target is enabled and reports the expected interface, sender `192.168.128.130:6665`, receiver `192.168.128.189:6666`, and receiver MAC `8c:1d:55:1b:af:44`;
* ten qualification messages are emitted while the GPU module remains absent.

Any failed assertion holds in the initramfs shell and does not load the GPU module. Only exact local input `R353-STATUS-READ` allows the existing R351 module to run. That module performs the guarded PCI identity checks and one read of `mmUVD_PGFSM_STATUS`; it does not write CONFIG or poll/wait for VCN. Its existing checkpoint panic remains in place to preserve early-boot evidence.

## Receiver interpretation

Do not type the token unless both the local screen identifies R353 and the Windows listener has recorded `QUALIFICATION_COMPLETE` plus `INPUT_READY`. Preserve the complete receiver output. The useful ordering is `TARGET`, ten `QUALIFICATION` records, `INPUT_READY`, exact `INPUT_RESULT`, `AMDGPU_MODPROBE_BEGIN`, and the R351 `STATUS_READ_BEGIN` / `STATUS_READ_RETURN` or `ABORT` markers. A panic message alone does not prove a STATUS read.

This design and package are being prepared offline. The preflight/install scripts do not select a boot entry, reboot, load a module, or access GPU hardware. The image remains a local artifact and its SHA-256 and byte size are recorded in `PACKAGE_AUDIT.json`.
