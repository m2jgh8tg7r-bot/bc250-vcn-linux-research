# R351/R352-era console photo evidence — 2026-10-05

## Purpose

Alternative evidence captured from the physical console because the normal log collection produced no usable log file. This record is based on the user-provided photograph IMG_0414.jpeg.

## Evidence classification

- Evidence type: physical-console photograph / visual boot trace
- Collection method: photograph of the display
- Normal log capture: **FAILED / no usable log obtained**
- This is **not** a claim of VCN activation, VCN execution, or firmware acceptance.
- Treat the photograph as an auxiliary witness for boot/reset state only.

## Visible boot/reset information

The upper portion of the screen visibly contains:

- x86/asm: Previous system reset reason (0x10000400): a parity error occurred
- microcode: Current revision ...
- mtrr ...
- registered taskstats version 1
- X.509 / kernel-key / EFI-related initialization
- multiple ima: / integrity initialization messages
- cgroup: initializing ... 
- Freeing unused kernel image ...
- USB/HID initialization for Logitech Wireless Receiver / mouse

Near the bottom of the photograph:

- bash: cannot set terminal process group (-1): Inappropriate ioctl for device
- bash: no job control in this shell
- a clocksource calibration line reporting approximately 3194.029 MHz
- clocksource: tsc: ...
- clocksource: Switched to clocksource tsc

## Interpretation boundary

The strongest directly visible finding is the recorded **previous reset reason: parity error (0x10000400)**.

The photograph does **not** establish where the parity error originated. It must not be attributed to VCN, PSP, SMU, memory, PCIe, or any particular block without additional evidence.

The visible boot sequence progresses at least through TSC clocksource selection. The photograph does not show a VCN firmware load/authentication result.

## Research handling

This should be retained as an auxiliary witness for the R351-era boot/reset investigation because ordinary log capture was unavailable.

Recommended status wording:

> PHOTO WITNESS ONLY — previous reset reason reports parity error 0x10000400; no VCN conclusion.

Do not promote this photograph to a PASS/FAIL result for VCN bring-up.

## Source

User-provided console photograph in the 2026-10-05 research conversation: IMG_0414.jpeg.
