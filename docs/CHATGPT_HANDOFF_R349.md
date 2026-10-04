# R349 — SVC64 management-entry and local slot relation

STAGE=R349
RESULT=The bounded management path reads entry state and a four-bit occupancy mask; it does not establish one SVC67 allocation per active management slot
STATIC_OR_LIVE=CONDITIONAL_STATIC_CONFIRMED from bounded saved-static instruction packet
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; run rejected for attempted tool activity; packet reviewed directly
PACKET_SHA256=77cc9fbe1cdbdd290b5a70a5d442304aef18679e815a16db9eb18189c7cb4244

## Entry fields and local allocation constraint

In the `0x2049ba` window, code reads a byte at object offset `0x4b`, computes the indexed offset with `7*i + 16*i = 23*i` then scales it by four, and reads a byte through the `lr`-based table pointer. It compares that byte with `1` (`0x2049ce–0x2049d0`). On the shown matching path it reads a word at object offset `+4` (`0x2049d2`), calls `0x20158c`, then calls `0x20180c` after loading a word from `[r8] + 4` (`0x2049de–0x2049e8`). This path does not itself show a call to `0x200cb4` or SVC67. A nearby separate branch calls the allocation wrapper at `0x204a28`; the packet does not prove that the two branches share a per-slot allocation limit.

The `0x201ab8` path maps a request type through the table at `0x8430` and reads candidate index from object offset `0x4b`. For the shown type-3 path, it computes entry offset `0x5c * index` from the root loaded through `[0x6054]`, then requires the entry byte to equal `1` (`0x201af6–0x201b04`). It reads an occupancy byte at entry offset `+0x34` (`0x201b24–0x201b28`), scans bits 0 through 3, and returns error `0x31` if all four are already set (`0x201b2c–0x201b52`). The later shown code sets the selected bit in that byte (`0x201c18–0x201c22`). Thus this bounded path chooses at most one free bit per invocation and exposes four local occupancy positions per indexed entry; it does not show a one-allocation-per-entry rule.

The separate state table at `0x69b0` is read by the guard at `0x201724` and updated by `0x20180c`. Those accesses do not establish that one SVC67 allocation corresponds to one active slot. The nearby direct call `0x204a28: bl 0x200cb4` confirms an allocation-wrapper site in a dispatch branch, but no global caller/re-entry or one-load-per-slot constraint follows from these bounded windows. Runtime behavior and caller frequency remain unproven.

No BIOS, firmware, kernel, module, boot entry, or hardware state was changed. No `sudo` command or real-device test preparation was required.
