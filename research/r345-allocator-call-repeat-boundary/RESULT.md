# R345 — Allocator-call repetition boundary

STAGE=R345
RESULT=One direct invocation of 0x2107bc reaches the 0x211a04 call site at most once in the supplied direct CFG
STATIC_OR_LIVE=CONDITIONAL_STATIC_CONFIRMED from bounded saved-static instruction packet
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; final analyzer/reviewer agreed and was checked against the packet
PACKET_SHA256=2c051575e5815e4ae9f42fd852e8185b90c2826af4fd1027bb367ed6f8e445a0

## Call and loop boundaries

The packet shows the parent calling `0x2107bc` at `0x2105b6`, returning to `0x2105ba`. Inside `0x2107bc`, `0x2107ce` calls `0x211a00`; this is a distinct call target from `0x211a04`. A bounded descriptor scan loops at `0x2107fa`–`0x21080a` before the target call. It advances `r6` until a free entry is found or the scan limit is reached. Exhaustion branches to the error cleanup at `0x2108e4`; finding an entry reaches the setup and single direct call `0x21085a: bl 0x211a04`.

After that call, a nonzero return reaches cleanup at `0x2108e4`, then `0x2108f0` branches to `0x2107de` and the return at `0x2107e0`. The success path continues through postprocessing. Its backward branch `0x210912 -> 0x2108ee` remains after the target call and then also reaches the return sequence; it does not revisit `0x21085a`. No shown branch after `0x21085a` targets the call site or the pre-call scan.

Therefore one direct invocation of `0x2107bc` reaches `0x211a04` at most once in this bounded direct CFG. This does not bound how often an outer caller may invoke `0x2107bc`, and it does not exclude re-entry through callees or indirect dispatch outside the packet. Runtime reachability remains unproven.

No BIOS, firmware, kernel, module, boot entry, or hardware state was changed. No `sudo` command or real-test preparation was required.
