# R341 — Allocator split destination and table-boundary check

STAGE=R341
RESULT=With 64 pre-split descriptors, a split requires descriptor index 64 at 0xb3408; the saved split/copy path overlaps that root boundary
STATIC_OR_LIVE=CONDITIONAL_STATIC_CONFIRMED from bounded saved-static instruction packet and recorded host-normalized layout
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; its reviewer corrected the destination offset but missed the destination write on the last-slot path
PACKET_SHA256=6a56dcb71c0d1a511dc21b6f52054bf6b34f4a6d5682322620995095fad02dc4

## Argument and range

Let `B` be the allocator base (0xb3000), `n` the pre-split descriptor count loaded from `B+4`, and `i` the current descriptor index in `r4`. From `0x200c54`–`0x200c68`, the call at `0x200c6a` passes:

```text
destination = B + 0x28 + 0x10*i
source      = B + 0x18 + 0x10*i
length      = 0x10*(n - i - 1)
```

The code forms the destination at `0x200c5e` and `0x200c68`, the source at `0x200c62`, and the length at `0x200c5a`, `0x200c5c`, and `0x200c66`. These are half-open copy ranges; the routine copies from the end when destination is 16 bytes above source and the length exceeds that gap (`0x2005e8`–`0x200664`). For `n=64, i=0`, the source is `[0xb3018, 0xb3408)` and destination is `[0xb3028, 0xb3418)`. The 16-byte destination tail overlaps the recorded management-table root at 0xb3408.

The 64 descriptor records begin at `B+8` and have 0x10 stride; 64 records end exactly at `B+8+64*0x10 = 0xb3408`. This is the off-by-one boundary: splitting a table already holding 64 records requires record index 64.

The end cases agree with that result. At `i=62`, a 16-byte copy has source `[0xb33f8,0xb3408)` and destination `[0xb3408,0xb3418)`. At `i=63`, `0x200c56` branches around the copy, but the subsequent record initialization stores fields at `B+63*0x10+0x18` and following offsets, beginning at 0xb3408. Skipping the shift therefore does not avoid the boundary collision.

## Evidence limits and Q36 review

Q36's final reviewer correctly rejected its analyzer's destination `+0x40`; the instruction sequence gives `+0x28`. Its no-overlap conclusion for `i=63` is not correct for the requested conditional case: it treats the skipped copy as no write and omits the record initialization after the branch. The address calculations above follow the saved packet and the recorded layout; neither Q36 response is evidence.

This establishes only the conditional static overlap if a split is attempted with a pre-split count of 64 and the recorded layout applies. Whether saved-static control flow can reach that count, whether the table root is active at that moment, and any resulting runtime effect remain UNPROVEN. No hardware operation, build, installation, or privileged preparation occurred.
