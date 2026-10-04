# R343 — Saved slot-state lifecycle

STAGE=R343
RESULT=The table writer claims a nonnegative slot by setting bit 31; visible readers distinguish that marker, but no clear/reuse transition appears in the supplied windows
STATIC_OR_LIVE=PROVEN_STATICALLY from bounded saved-static instruction packet
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; its analyzer invented labels and its reviewer misread visible instruction addresses
PACKET_SHA256=60e09052d8c92e447dda9048f70a5414590844074ed6c38ee0854e8ae0875a5b

## Slot state

The literal at `0x20180e` supplies base `0x69b0`. The routine scans entries using stride 8 from index 1 (`0x201816`–`0x20181a`), skips entries whose first word is signed negative (`0x20181c`–`0x20181e`), and advances until index 32 (`0x20187e`–`0x201884`). On its successful assignment paths it ORs bit 31 into the requested state at `0x201834`, stores a tag in the entry's second word (`0x201838`), merges/stores the marked first word (`0x20183a`–`0x201842`), and returns success. The special `r0==1` path initializes entry zero to `0x80000001` and writes `0x4505` in its second word (`0x201854`–`0x20185c`). This is evidence for a sign-bit claimed/in-use marker; exact low-nibble status names are not established here.

The guard at `0x201724` rejects indices >=32, then rejects a negative first word at `0x69b0+8*index`; nonnegative words return success. The wrapper `0x200cb4` aborts on a nonzero guard result and otherwise calls `0x200c10`. Thus the wrapper blocks a repeat for the same index while its entry remains marked negative. The `0x201ae0` reader tests bit 7 of the first word's low byte (`lsls #24`, then `bpl` to error); the packet does not establish that this is the same marker as bit 31. The `0x203c2e` reader masks the first word to its low nibble and dispatches values 5, 4, and 6 along separate paths; their semantic names are not proven by this packet. The `0x201c54` sequence reads the entry's second word and merges it into another structure; it does not change the table entry.

These windows show no instruction that clears bit 31 or makes a claimed entry reusable. They support a one-at-a-time rule for the guarded same-index path while the marker persists, but do not establish the full call chain connecting every slot assignment to every wrapper use, concurrent behavior, a deactivation/reset path elsewhere, or that slot count bounds allocator descriptor count. In particular, 32 legal indices do not cap the descriptor count at 32; R341's conditional count-64 boundary result remains, while reachability of count 64 is still UNPROVEN.

## Corrections and limits

R342's interpretation of `0x201724`'s signed branch was correct. Its note that the table's lifecycle was outside that narrower packet is now refined by this additional window. Q36's R343 analyzer inferred unsupported status names and misreported some displayed addresses; its reviewer then incorrectly claimed the packet omitted `0x203c34`–`0x203c3c`, which are present. The conclusions above use the verbatim packet instructions.

No BIOS, firmware, kernel, module, boot entry, or hardware state was changed. No `sudo` command or real-test preparation was required.
