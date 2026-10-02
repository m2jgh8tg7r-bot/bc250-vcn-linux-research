# R297 CP01 LIVE result

Date: 2026-10-02

Status: PASS

EFI pstore preserved the CP01 event:
- R141 early_init begin/end returned 0
- R297 CP01 checkpoint message
- kernel panic from vcn_v2_0_early_init

The system rebooted back to normal Bazzite. The persistent checkpoint method is therefore validated for this research kernel.

Boundary: CP01 is before sw_init, direct-copy firmware provisioning, and P1 pre-reset.

Postmortem log SHA-256:
dc4e0d04eca6e50a617d6cf76d1c598d142af5441bfe44b1dce17d7c269cc45d

After recovery, next_entry was still present and should be cleared before any later reboot.
