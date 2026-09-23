# R214 — SMU directory entries, zero-filled second body, and Linux loading boundary

2026-09-22. Saved-file analysis only. No device access, service change, firmware installation, or reboot.

The saved P3 BIOS directory corroborates R213's container boundaries. Its type `0x08` entry points to the analyzed SMU container at `0x8ff000`, size `0x40200`. Type `0x12` points to a different container at `0x93f700`, also size `0x40200` and version `0x00580600`. However, the second body is a zero-filled template, not a byte-identical backup of the analyzed executable body.

## Verified structure

The `$PSP` directory at `0x8e0000` has 19 entries. Its Fletcher-32 checksum matches, its address mode is zero, and the selected physical-address entries map into the saved 16-MiB ROM. Entry sizes agree with both SMU headers. Each 256-KiB body independently hashes to its own header SHA-256 field.

| Entry type | Container start | Body start | Body SHA-256 | Nonzero body bytes |
|---|---|---|---|---:|
| `0x08` | `0x8ff000` | `0x8ff100` | `5c805026581ace101ba43ef4d0f6b34354f4a61461a1c78d2fa6a335a53d9936` | 144782 |
| `0x12` | `0x93f700` | `0x93f800` | `f22e2815c99e9bf4a4fbdcc8d6498d3eee59181dd46185f83a0130ff73190b06` | 8 |

Type `0x12` has the word `0x00580600` at offsets 0 and 4, zeros throughout `[0x8,0x3fffc)`, and `0x11223344` at `0x3fffc`. Thus the repeated version alone is not executable-image identity. An initial observation that the bodies differ must not be inflated into evidence of two alternate executable builds. A placeholder interpretation is CONSISTENT_WITH these bytes; its intended boot role is UNPROVEN.

These structural results match both saved board captures and both stored Robin1.00/Robin3.00 distribution members. The captures are from one board, not independent boards. Deliberate in-memory changes to a directory entry and each body were rejected by the checksum checks. No altered image was written or used on hardware.

## Why Linux does not resolve the boot selection

Saved kernel commit `0bb924b042ab85b8f529aed6e4f3e24750584276` selects `cyan_skillfish_set_ppt_funcs` for MP1 11.0.8. Its table provides `check_fw_status`, but no `init_microcode` or `load_microcode` callback. The wrapper returns zero when the init callback is absent; the non-PSP load wrapper conditionally invokes a load callback and then checks status. The generic `smu_v11_0_load_microcode` SRAM-copy loop therefore cannot be treated as the Cyan boot loader merely because it exists in the tree. The PSP SMU-load helper also returns before loading when its firmware pointer is absent.

`smu_v11_0_check_fw_status` checks the interrupts-enabled flag. This static wiring does not identify loaded bytes or prove VCN operation. The inspected source files are clean relative to the saved commit; no new claim about the currently running module is made.

The directory also locates type `0x01` at `0x8e0400`, size `0xa800`. The inspected entry lacks `$PS1` at header offset `0x10`; this observation alone does not prove encryption. A matching plaintext loader and its copy/verification path have not been established. Addresses from an external plaintext/internal-BIOS loader must not be imported without version and address mapping evidence.

## Classification and next work

PROVEN_STATICALLY: directory checksum and selected entries; SMU body hashes and sizes; exact zero-filled structure of type `0x12`; scoped Linux callback wiring. REJECTED: type `0x12` is a byte-identical copy of type `0x08`; generic Linux SMU loader code proves Cyan's boot copy range. UNPROVEN: selected boot image and copy extent, runtime modifications/SRAM identity, signature verification, VCN physical power/de-isolation, PSP acceptance/placement, VCPU, rings and video decode.

The type `0x08` analysis remains the useful static executable candidate. The zero-filled second entry removes one apparent alternate-code hypothesis; it does not turn ROM evidence into runtime proof. Next static work should trace a version-matched loader or find a discriminating identity observable through an already-established read path.

## Live-test readiness

The user's instruction is to prepare a useful live test when needed and report it. [The readiness assessment](../logs/R214_LIVE_TEST_READINESS.md) is saved. No executable live test is ready: a verified image-selection/runtime-identity read target and transport remain missing. Repeating the version read cannot distinguish these containers; repeating R197 does not resolve the new boundary. The six-condition proposal gate remains unmet. No BIOS swap, SRAM scan, unknown mailbox request, or additional reboot is proposed.

Evidence: [directory/body audit](../logs/R214_DIRECTORY_EVIDENCE.json), [reproduction script](../logs/R214_audit_directory.py), [kernel excerpts](../logs/R214_KERNEL_EVIDENCE.txt), [kernel source hashes and callbacks](../logs/R214_KERNEL_AUDIT.json), [kernel audit script](../logs/R214_audit_kernel.py).

Format interpretation uses pinned [PSPTool directory code](https://github.com/PSPReverse/PSPTool/blob/6112e48dc24d77fbeb2aa646d4a9ed3403fdd601/psptool/directory.py), [entry code](https://github.com/PSPReverse/PSPTool/blob/6112e48dc24d77fbeb2aa646d4a9ed3403fdd601/psptool/entry.py), and [header code](https://github.com/PSPReverse/PSPTool/blob/6112e48dc24d77fbeb2aa646d4a9ed3403fdd601/psptool/header_file.py). These describe static formats, not observed loader execution.
