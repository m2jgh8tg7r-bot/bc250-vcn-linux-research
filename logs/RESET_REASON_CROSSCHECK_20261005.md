# Reset-reason photo cross-check — 2026-10-05

## Source comparison

The GitHub photo-witness note `logs/R351_console_photo_witness_20261005.md` transcribes:

```text
x86/asm: Previous system reset reason (0x10000400): a parity error occurred
```

The R351 kernel build tree's `arch/x86/kernel/cpu/amd.c` contains the matching S5 reset-reason decoder. It prints the prefix `x86/amd`, labels array index 30 / `BIT(30)` as “a parity error occurred”, and prints the complete 32-bit register value using `%08x`. Thus parity corresponds to bit `0x40000000`; the transcribed value `0x10000400` does not contain that bit, and the prefix differs from the source string. The actual photo is not present in the GitHub commit, so the text may be a transcription/reading error or a different boot message. Do not normalize the mismatch by guessing; inspect the original image or obtain a raw console capture.

## Prior reset evidence

Older repository evidence (`research/r297/RESULT_CP06_PROGRESS.md` and `RESULT_CP06_LIVE.md`) records `0x40080402` and `0x40080400` after safe/manual resets. With the R351 source decoder, `0x40080402` includes parity bit 30, software-CF9 bit 19, and 4-second power-button bit 1; `0x40080400` includes parity bit 30 and software-CF9 bit 19. The same parity bit therefore occurred in prior recovery/reset scenarios and is not specific evidence for the current R351 attempt. The kernel's decoder writes the read value back to the status register to clear the reason bits.

## R351 attempt boundary

The photo's `clocksource: Switched to clocksource tsc` and Bash no-job-control text are consistent with the research initramfs console, but do not establish whether `R351-STATUS-READ` was accepted. No latest-attempt raw Windows receiver capture or `INPUT_RESULT` has been supplied here. Do not infer whether the single `PGFSM_STATUS` read ran. Preserve the photo as a visual witness only; request its original image and exact token/capture outcome before another LIVE status-read attempt.
