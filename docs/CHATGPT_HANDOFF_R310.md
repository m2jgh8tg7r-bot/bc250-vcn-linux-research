# R310 — Pre-access software metadata experiment

Status: DEFERRED AFTER REVIEW; not a runnable or validated test. Not installed or booted. Source and package validation do not establish live success.

Question: in a new CP04-derived boot, do the in-memory VCN base, aperture and no_hw_access flag support the previous conditional address calculation?

Changed variable: add software-memory metadata logging immediately before the existing unconditional CP04 panic. Existing guards stay unchanged. No new VCN read/write, SMU command, reset release or firmware change is added. Whole driver initialization before this helper still touches hardware as in R303; this is not a hardware-free boot.

Outcomes:
- A: base and arithmetic match, aperture checks true, no_hw_access false. Supports the address calculation for this new boot only; does not prove physical response or eliminate power/isolation/fetch candidates.
- B: missing base, unexpected base, out-of-aperture calculation or no_hw_access true. Revisit the affected software premise before any register probe; does not establish historical CP06/07 state or root cause.
- C: metadata missing or incomplete. Trial is inconclusive; network/panic delivery and execution boundary remain ambiguous. Do not infer a VCN fault or repeat the hanging read.

Supporting evidence: R303 delivered guard markers at the pre-VCN-MMIO boundary; R308 exported normal-boot base1 0x7e00; R309 bounds retained compiled producer differences.
Contradicting evidence: none currently establishes a numerical mismatch.
Unknown evidence: new runtime metadata is not acquired; historical CP06/07 lack decisive traces.
Unknown: failed-boot runtime values, operation reached, actual hardware activity, automatic panic restart reliability.
If the address hypothesis is wrong: values can match while device state or another execution boundary explains failure.

Recovery: preserve normal/recovery entries; retain old R303 package and verified backup before replacement. Installation must not select an entry or reboot. Save network receiver output before manually selecting the new research entry. Existing public confirmation gate remains required before GPU load. Expect deliberate panic; if automatic restart fails, manually restart to the normal entry. Do not repeat on missing metadata without reviewing evidence.

Privacy: public result contains stage, relative artifact identities and scalar metadata only. Do not publish machine network configuration, raw init, keys, binaries, host paths or raw receiver logs.

The source computes address candidates only and never dereferences rmmio. no_hw_access is a field observation, not a call to the accessor and not a proof of all dispatch conditions. Logging values from a new boot cannot retroactively attest CP06/07.

## Preparation outcome and release gates

An isolated reflink working copy was made; the retained R152 source was not edited. A full-module build was started and deliberately terminated after review, with exit143. This is an interrupted preparation, not a compiler failure or hardware result. No bootable R310 package was produced or installed. No build process is intended to remain running.

Review found:
1. A non-null reg_offset pointer does not establish that the desired array index is valid. The draft must not be released as-is.
2. Candidate byte-start checks are not full 32-bit access bounds checks, and 64-bit arithmetic does not reproduce every actual accessor overflow behavior.
3. The copied build tree triggered broad recompilation. A future package must record and audit the wider binary changes instead of claiming only a logging change in the final module.

A better bounded observation point is the discovery parser while the entry's num_base_address is known: emit only indices validated against that count, record assignment identity, and separately record scalar accessor conditions at the existing pre-access checkpoint. This is a design direction, not a validated implementation. It also requires confirming that later code does not replace the base pointer. No new VCN access is warranted by this preparation result.

STAGE=R310
RESULT=DEFERRED_AFTER_REVIEW
STATIC_OR_LIVE=STATIC preparation only
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_NEW_TEST
PROVEN=Draft review limits; isolated build interruption
REJECTED=Draft is ready for a live boot; non-null proves array bounds
UNPROVEN=New runtime metadata, failed-boot cause, VCPU execution
NEXT=Count-bounded observation design and artifact comparison before packaging
