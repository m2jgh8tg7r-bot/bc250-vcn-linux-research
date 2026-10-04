# R342 — SVC67 wrapper index guard

STAGE=R342
RESULT=The guarded wrapper path accepts indices 0–31 only when the indexed word at 0x69b0 is nonnegative; it does not establish one allocation per active slot
STATIC_OR_LIVE=PROVEN_STATICALLY from bounded saved-static instruction packet
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; analyzer and reviewer both misread the signed `blt` condition
PACKET_SHA256=025189c9e52a52ca2457c86b25650f528ac5a93334d25c005278e5a415c1625d

## Guard behavior

At `0x201724`, `cmp r0,#0x20` followed by unsigned `bcs 0x201732` rejects values at least 32 with return value `0x25`. For indices below 32, the literal at `0x20173c` supplies base address `0x69b0`, and `ldr.w r0,[r1,r0,lsl #3]` reads the indexed word at `0x69b0 + 8*index`. The following `cmp r0,#0` / `blt 0x201736` rejects only a signed negative word. Zero and positive words both fall through to `movs r0,#0`, the success return.

The wrapper at `0x200cbe` calls this guard and at `0x200cc2`–`0x200cc4` exits to `0x200d50` for a nonzero error. A zero return continues through `0x200cd2` and calls allocator core `0x200c10` at `0x200ce2`. In the supplied caller window, `0x204a26` zero-extends `r5` to the index argument before calling `0x200cb4` at `0x204a28`.

The bounded windows therefore prove an index range and a signed-value predicate for this wrapper path. They do not prove a zero-only free-slot test, because positive values pass. They also do not show a once-only allocation rule: the guard's role and indexed-word lifecycle are not established here, nor is the caller's `r5` proven to enumerate active slots. Nearby calls at `0x204a8e`, `0x204b82`, and `0x204c88` target `0x20351c`, `0x201f70`, and `0x2037ec`, respectively; they are not calls to `0x200cb4`. No global call-site or writer absence claim is made.

This index ceiling does not by itself cap the allocator descriptor count. R340 found that the count increments on split paths; repeated-call state and all paths that can change it remain outside this bounded result. Whether count 64 is reachable is still UNPROVEN.

## Q36 disposition

Q36 correctly identified the 32-entry index check and wrapper's early exit, but both its analyzer and reviewer interpreted `blt` after `cmp #0` as rejecting nonzero values. The branch condition rejects negative values only. The response is not evidence; the result above follows the saved instruction window.

No BIOS, firmware, kernel, module, boot entry, or hardware state was changed. No `sudo` command or real-test preparation was required.
