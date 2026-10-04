# R344 — SVC67 per-invocation control flow

STAGE=R344
RESULT=The indexed direct CFG reaches saved SVC67 at most once per invocation; its only earlier backedge is before the SVC67 site
STATIC_OR_LIVE=CONDITIONAL_STATIC_CONFIRMED from bounded saved-static instruction packet
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; outputs conflicted and omitted a visible pre-SVC backedge
PACKET_SHA256=e1afd366373f40c114898553e0f29ad47216576b060c18f595e22b2250897aec

## Control-flow boundary

The packet shows `svc 0x64` at `0x211cc0` followed by `bne 0x211bf4` at `0x211cc4`. This is a real backedge, but it returns to code before the saved SVC67 at `0x211d5e`; it can repeat the earlier setup/SVC64 path without repeating SVC67, which has not yet run on that iteration.

After `svc 0x67` at `0x211d5e`, the shown direct branches do not return to that site or earlier setup. `0x211d62` branches on error to `0x211cba`, whose instruction is an unconditional branch to `0x212224`. `0x211daa` uses the same exit. `0x211db2` branches forward to `0x211e4c`; the later branches shown target `0x211e56`, `0x211e5a`, `0x211eba`, or `0x211fb8`, all after the SVC67 site. Thus the backward edge at `0x211cc4` must not be mistaken for a repeated SVC67 execution.

Under this direct CFG, one invocation reaches the SVC67 site at most once. The result does not cover indirect or exception-handler re-entry, or re-entry from callees whose bodies are outside this packet. Those possibilities remain UNPROVEN. This says nothing about SVC67 success or runtime service behavior.

## Q36 disposition

Q36 produced conflicting summaries: one claimed there was no backedge, while another said the packet began after the SVC. The packet includes `0x211d5e` and the pre-SVC branch at `0x211cc4`; neither summary is used as evidence. The conclusion above follows the saved instruction sequence and branch destinations.

No BIOS, firmware, kernel, module, boot entry, or hardware state was changed. No `sudo` command or real-test preparation was required.
