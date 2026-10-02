# R297 CP01 LIVE boot observation

Date: 2026-10-02

Status: partial LIVE success; persistent capture pending.

User-observed LIVE behavior:
- R297 CP01 one-shot boot was attempted.
- The system reached a kernel panic.
- After the panic, the machine automatically rebooted.

Interpretation boundary:
- Because the CP01 candidate intentionally calls panic immediately after the R141 early_init_end checkpoint, this is LIVE evidence that execution reached the CP01 checkpoint.
- The automatic reboot is LIVE evidence that the panic/reboot path with panic=10 was serviced in this research boot.
- Persistent EFI pstore capture has not yet been checked, so persistence is not yet proven.

Next:
collect pstore, grubenv, current kernel identity, and any previous-boot journal evidence before changing anything else.
