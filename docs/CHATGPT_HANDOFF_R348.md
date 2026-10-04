# R348 — Bounded management field04 alias review

STAGE=R348
RESULT=No unambiguous local store to the management-root field04 target is visible in the supplied consumer, init, and allocator windows; this does not establish a global writer set
STATIC_OR_LIVE=CONDITIONAL_STATIC_CONFIRMED from bounded saved-static instruction packet
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; all three analyzer attempts failed validation; model/reviewer address claims corrected by direct packet audit
PACKET_SHA256=30d5fb5dadf654306e5b77e5635c47f60e6848b07650360d25c533989193f78f

## Bounded observations

In the consumer window, `0x201c06` forms a root-derived address by adding `r11 << 2` to the value loaded from `[0x6054]`. `0x201c42: ldr r0,[r0,#4]` reads from that derived address; the loaded value is then written to a different structure by `0x201c48: str.w r0,[r2,#-4]`. The shown instruction is a read from a root-derived address, not a write back to it. The packet alone does not establish the complete table-entry indexing semantics, so this is not promoted to a global field04 producer conclusion.

Cold initialization at `0x203428` loads literal `0xb3408` into `r5`. It writes byte value 1 at `[r5]` (`0x20343e`), `r7` at `[0xb3408+0x58]` (`0x203444`), and `r6` at `[0xb3408+8]` (`0x20344a`). The supplied init window shows no store at `[0xb3408+4]`. It separately stores allocator base `0xb3000` through `[0x6050]` at `0x20342e` and initializes that allocator area at `0x203454` and `0x203460`.

The allocator body at `0x200c10` obtains its manager through `[0x6050]` and shows descriptor/count writes relative to that allocator base. The adjacent wrapper computes an indexed address from the root at `[0x6054]`; at `0x200d20` it writes a byte at offset `+3` from its computed address, not an identified field04 target. None of these bounded stores is an unambiguous write to the management-root field04 target. This is bounded-not-found only; other code, aliases, or indirect paths may write it.

Q36’s analyzer repeatedly failed required-output validation. Its suggested `0xb3408 + 4*index + 4` formula is not established by this packet. A reviewer’s `0x60` stride inference also is not adopted. No stride or complete index mapping is needed for the bounded statement above.

No BIOS, firmware, kernel, module, boot entry, or hardware state was changed. No `sudo` command or real-device test preparation was required.
