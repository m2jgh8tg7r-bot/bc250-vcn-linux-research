# R300 INPUTDIAG — R299 console rejection discrimination

Date: 2026-10-03 JST

STAGE=R300 INPUTDIAG HOME PACKAGE
RESULT=PROVEN_STATICALLY package round-trip and CPU input diagnostics; not installed/booted.
STATIC_OR_LIVE=PROVEN_STATICALLY; R299 excerpt remains user-reported LIVE
HARDWARE_ACCESS=NO new agent hardware access
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=R299 qualification 2/10–10/10, COMPLETE and token rejection received; failure hold requires manual return. R300 input tests 9/9; exact archive hash/mode/symlink round-trip; no amdgpu module included.
REJECTED=R299 attempt demonstrates CP03 panic failure or VCN failure; mocked/PTY checks prove actual boot-console behavior.
UNPROVEN=Exact cause of R299 rejection; installed R300 identity; actual console read result; CP03/GPU-stage delivery; VCN execution.
NEXT=User-run privileged read-only preflight, audit result, install without selection, audit result, then notify before menu preparation/manual boot.

## Evidence and chosen change

R299 user reports entering the correct token, but receiver excerpt ends with FAIL receiver confirmation token mismatch at 65.842606. Existing init does not record read status or consumed bytes. Wrong input and EOF share the same message. No RECEIVER_CONFIRMED or AMDGPU_MODPROBE_BEGIN is supplied. The failure path explicitly holds in a RAM shell without automatic reboot; user reboot -f follows that path. Current normal kernel was observed after return. Token bytes, EOF/read error, queued input and console state remain unresolved; do not attribute this to user mistyping.

R300 retains R298 network-only modules and qualification sequence, and uses the SAME R299-CP03-RECEIVED token to avoid introducing a different input string. It logs stdin TTY status, read return code, byte length in LC_ALL=C and shell-escaped first 64 bytes. Terminal settings are displayed locally via read-only stty -a; no stty setting is changed and no input is drained or normalized. Exact match, mismatch and failed read have separate markers. Even an exact match ends in a RAM shell. No GPU module is included; no CP03 trigger or panic is expected. Input may be logged: type only the specified public token.

The byte log describes Bash's consumed string, not a raw keyboard byte capture: newline is consumed, terminal line discipline can transform characters, and Bash read can ignore NUL. The failed-read marker deliberately covers both EOF and other read errors; return status does not alone identify which occurred.

Tests: exact LF token, trailing space, CRLF via pipe, empty line, EOF, exact token without newline, Unicode dash, 200-byte mismatch, exact token via PTY. All 9 passed on CPU; no real GPU load. PTY test proves one userspace terminal case, not /dev/console on the research boot.

## Package and operation contract

Approximately 10 MiB additive image. Read-only /boot space observation was 146,366,464 bytes; privileged preflight must recheck at least image size plus 50 MiB margin. Installer preserves hashes of all existing BLS entries and their referenced images, normal kernel, R180/R298/R299, research kernel and GRUB. No retirement, automatic selection, module load or reboot. Catchable install exceptions remove only newly created R300 files; power-loss rollback is not guaranteed. Default invocation is read-only and saves a preflight result.

Target/transport: standalone RAM init using prior NIC/PHY/netconsole path, then console read. Before: normal Bazzite, saved receiver file, exact package/boot identity audit. After: INPUT_RESULT plus one classification marker, shell hold. Success observation: INPUT_EXACT_MATCH and normal manual return. Failure observation: INPUT_MISMATCH/INPUT_READ_FAILURE, missing qualification or missing input result. Rollback: reboot -f at shell and select normal entry; physical recovery only if console cannot return. Persistence: additive image/BLS and optional one-time menu timeout; no disk-root mount or GPU device setting. Cold-power recovery for R300 is UNPROVEN. Network-only path inherited from R298; input diagnostics are new.

## User sequence

1. Run `sudo python3 /var/home/kazuyuki/bc250-research/research/r300-console-input-diagnostic/install.py` and share PASS output for independent audit.
2. After audit, run the same script with `--install`; share installed PASS output.
3. After installed audit and boot-change notification, prepare the menu using arm-menu.py, manually reboot and choose R300.
4. Wait until Windows saves R300 QUALIFICATION_COMPLETE, then type R299-CP03-RECEIVED at the BC-250 console and press Enter once.
5. Save INPUT_READY, INPUT_RESULT and classification. This diagnostic will not automatically reboot. At the shell use reboot -f and select the normal entry.

No privileged commands were run successfully by the agent: sudo -n requires authentication. No boot preparation or reboot was performed.

## Identity

image_sha256: `9ed01bc61374a1b4468320e9c2555ec8cde13883a5ccfa06db0a4f354868ba65`
image_size: `10449032`
bls_sha256: `b4cab77aa08eb1cc8eb7fd82c1ae024038e8c01baee30ceec0ac550b682f3c39`
init_sha256: `f967502045c8599f9218d70dd1e5f5450b3311b8375e6b3dce710662ea2fd16c`
research_kernel_sha256: `c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6`
