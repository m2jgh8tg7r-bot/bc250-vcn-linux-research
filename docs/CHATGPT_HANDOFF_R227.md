> **R232 correction — 2026-09-23:** The inherited initial-value0x16000 interpretation uses the wrong user-pointer/file mapping. R228/R232 retain the explicit startup0x280000 store and conditional table0x286000. [Evidence](CHATGPT_HANDOFF_R232.md). The original text below is historical.

# R227 — SVC 0x62 mapping call and the 0x280000 window

Date: 2026-09-22. Static analysis of the saved type-2 TOS body only; no hardware access or mutation.

## Static findings

At body offset `0x11608`, TOS initialization sets a context field at `+0x1c` from the value returned by SVC `0x73` plus `0x85000`. It later calls SVC `0x62` with `r0=0x280000`, `r1=context+0x1c`, `r2=0x51`, and `r3=0xc0000000`. It also makes SVC `0x62` calls for other ranges including `0x208000` and a range rooted at `0x200000`.

The TOS SVC dispatcher routes SVC `0x62` through address validation and, for addresses at or above `0x200000`, a page-table helper. The helper at body offset `0x2bb8` indexes a page-table entry by `address >> 20`, checks the entry's low permission/presence bits, invokes a lower-level mapping helper using the entry-derived base and address low bits, then performs a TLB invalidation and data synchronization barrier. Thus SVC `0x62` is involved in memory mapping/protection setup; its full ABI and the meaning of all flags still need confirmation.

The external guide's candidate table address `0x286000` shares the 1-MiB page-table index with the TOS's `0x280000` mapping request (`address >> 20 == 2`). This makes the external address geometrically compatible with the TOS mapping setup. It does not prove the mapping length covers `0x286000`, that its backing page is the F2 table, or that the external report and saved TOS are the same runtime image. The SVC `0x62` length operand is context-derived and not resolved to a concrete runtime value here.

R226's independent address arithmetic remains: context field `+0x18` is initialized to `0x16000`, and the F2 walker adds `0x6000` before indexing `0x5244` records. That yields candidate pre-mapping offset `0x1c000`. The mapping evidence does not establish a transformation from this offset to `0x286000`; the required bias/address translation remains unknown.

## Assessment and next step

The t02/F2 interpretation gains a real memory-mapping lead: `0x286000` sits in the same coarse page-table region as an explicit initialization request rooted at `0x280000`. Runtime address, concrete mapped range, table backing, 31-versus-32 count, and t28/clamp-release behavior remain unproven.

Next, decode the lower-level mapping helper and the context-derived length/flags passed to SVC `0x62`; then compare the resulting mapping arithmetic with the `0x16000 + 0x6000` table offset. Do not treat page-index compatibility alone as table identity.

## Reproduction artifacts

`r227-svc62-map-window/analyze.sh`, `map-functions.txt`, and `map-instructions.txt`; the executable is pinned by SHA-256 `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d`.