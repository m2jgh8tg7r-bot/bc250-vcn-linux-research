# R347 — Function-like C boundary around 0x212dec

STAGE=R347
RESULT=The bounded body at 0x212dcc..0x212e3c contains one direct 0x211a04 call at 0x212dec with no visible local repetition
STATIC_OR_LIVE=CONDITIONAL_STATIC_CONFIRMED from bounded saved-static instruction packet
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; analyzer conclusion checked against packet; reviewer falsely disputed address subtraction
PACKET_SHA256=7f839d6d6a795affda9281dbd4ec69cc7cda7b5351c735c2a02b33d54795700b

## Visible body and call

The supplied body starts at `0x212dcc: push {r4,r5,r6,lr}` and returns at `0x212e3c: pop {r4,r5,r6,pc}`. Their address difference is `0x70` bytes. These are the exact visible prologue and epilogue boundaries in this packet; this does not establish an external caller or prove that no earlier entry aliases exist.

There is one direct call to `0x211a04`, at `0x212dec`. Immediately before it, `0x212de4` loads `r2` from `[r1,#0x28]`, `0x212de6` loads `r1` and `r6` from `[r1,#0x20]`, and `0x212dea` moves `r6` to `r0`. After the call, `0x212df2` branches to the epilogue on nonzero return. On the fallthrough path, the shown code reaches `0x212e2a: bne 0x212e3a` or proceeds to the SVC at `0x212e30` and then returns. No supplied branch returns to `0x212dec`; this body therefore shows at most one execution of that call per invocation. Runtime reachability, external callers, indirect entry, and origins of the input base register remain unproven.

No BIOS, firmware, kernel, module, boot entry, or hardware state was changed. No `sudo` command or real-device test preparation was required.
