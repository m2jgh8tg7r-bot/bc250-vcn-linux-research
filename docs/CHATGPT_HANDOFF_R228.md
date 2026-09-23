> **R232 correction — 2026-09-23:** The table expression0x286000 remains supported. The parenthetical body0x6068/body0x6080 mapping and claimed initial0x16000 user-context value are corrected using R218's separate user-section coordinates. [Evidence](CHATGPT_HANDOFF_R232.md). The original text below is historical.

# R228 — saved TOS computes the external t02 table address

Date: 2026-09-22. Static analysis of the saved PSP type-2 TOS body only; no hardware access or mutation.

## Finding and correction

The saved TOS code itself computes the external report's candidate address `0x286000` before entering the SVC-F2 walker. This resolves the load-bias/address uncertainty in R225–R227 and corrects R226's assumption that the saved `0x16000` value remains in use.

The verified body SHA-256 is `19f091ded7bea3ee3c61adc3b6a7e1d2a48c8a7817f885bdb43b9c1f2b6bc43d`. The analysis uses artificial Ghidra base `0x200000`, so subtract that base from exported addresses to obtain body offsets.

- The startup function at body offset `0x11608` uses context address `0x206068` (body offset `0x6068`). The context field at `+0x18` is at body offset `0x6080`, whose initial saved value is `0x16000`.
- After issuing SVC `0x62` with `r0=0x280000` and passing the error branch, the startup code executes `str r7,[r6,#0x18]` at body offset `0x116f4`; `r7` still contains `0x280000`. Thus the context field `+0x18` is overwritten with `0x280000` before the walker call at body offset `0x1174c`.
- The walker at body offset `0xfc50` follows that context field, adds `0x6000`, then indexes records with stride `0x54`; it tests the `0x5244` tag at each row+8. Its table base expression at the call is therefore `0x280000 + 0x6000 = 0x286000`.

This is direct static evidence of the address expression in this saved TOS image, not a capture of live RAM contents. SVC `0x62` mapping length/backing, execution of this path on the BC-250, exact live entry count, and whether the external guide analyzed the identical runtime image remain unproven.

## Entry-count distinction

The walker iterates indices `31` down through `0`, so its capacity is 32 slots. It filters by the `0x5244` tag; empty/unmatched slots are not processed. The community report's “31 entries” can therefore be compatible with 31 populated rows plus one unused slot, but the saved static code alone does not prove that runtime occupancy.

The community guide reports `t02` at `0x286000`, magic `0x5244`, and 31 entries, and describes SVC-F2 processing and AUTOLOAD/t28 registration. The local address and record-family match are now strong; t28 registration and clamp-release effects remain external claims pending artifact/version-matched corroboration. Source: https://github.com/katzzero/bc250-unofficial-community-guide/blob/main/02-bios-and-firmware.md

## Next static step

Follow the F2 walker outputs and the `0x5244` row fields into the registration path, then compare the row parser with a version-matched t02 artifact if available. Preserve the distinction between static address calculation, runtime mapping, successful registration, PSP firmware acceptance, and VCN hardware execution.

## Reproduction artifacts

`r226-context-pointer/context-instructions.txt` records the context overwrite and caller; `r217-tos-load-response/t02-candidate-functions.txt` and `t02-candidate-instructions.txt` record the walker. Fresh lower-level mapping helper analysis is in `r228-map-helper/map-helper-functions.txt` and `map-helper-instructions.txt`.