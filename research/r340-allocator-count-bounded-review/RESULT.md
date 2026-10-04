# R340 — Bounded allocator-count write review

STAGE=R340
RESULT=The supplied saved-static windows contain one allocator-count increment on the block-split path; no 63/64 saturation check is visible there
STATIC_OR_LIVE=PROVEN_STATICALLY from bounded saved-static instruction packet
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; independent packet review corrected its loop-path summary
PACKET_SHA256=ea4a474ada100621cc63a380344f56050d93ed9868bad2022e98915864b263c2

## Finding

In the `0x200c10` window, the manager pointer is loaded from the saved global at `0x6050` (`0x200c2c`–`0x200c30`). The descriptor count is loaded from manager offset `+4` at `0x200c3a` and used to bound the descriptor scan: `r4` starts at zero (`0x200c3c`), advances at `0x200ca6`, and the `bhi 0x200c40` at `0x200caa` repeats while the index remains below the loaded count.

The request size is held in `r6`; the total-size check at `0x200c32` is against that request, not an `n<=63` count check. For a matching free descriptor, `0x200c4a`–`0x200c52` compares its size against the request. A descriptor no larger than the request branches to `0x200c8e` without changing the count. A larger descriptor takes the split path (`0x200c54`–`0x200c6a`), then loads the manager count and increments/stores it at `0x200c86`–`0x200c8c` (`adds r1,r1,#1`; `str r1,[r0,#4]`). Thus the visible increment applies when the descriptor is split to create another descriptor, not to every successful allocation.

The `0x200cb4` wrapper calls the core at `0x200ce2`; it has no direct count-field store in the supplied window. The supplied `0x203422` setup window likewise shows no direct store to that field. Within these windows there is no visible decrement, reset, saturation, or 63/64 count guard. This is a bounded conclusion, not a global search for every writer or proof of the allocator's maximum count.

## Review disposition

Q36 analyzer/reviewer output was advisory. The packet itself confirms the increment and includes the scan back-edge at `0x200ca6`–`0x200caa`; the Q36 reviewer's claim that this back-edge was missing is incorrect. The analyzer's statement that the scan iterates on the requested index is also inaccurate: `r4` scans the stored descriptor count, while `r6` carries the requested size. The deterministic conclusion above comes from the saved-static packet, not either Q36 response.

No BIOS, firmware, kernel, module, boot entry, or hardware state was changed. This R340 allocator result is a separate saved-static continuation and does not change R339's requirement for an independently qualified sampled RIP or authorize a live retry.
