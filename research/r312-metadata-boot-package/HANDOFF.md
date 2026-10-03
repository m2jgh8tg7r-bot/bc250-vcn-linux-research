# R311/R312 — Bounded metadata candidate and HOME boot package

STAGE=R312
RESULT=PREPARED_HOME; privileged read-only preflight pending
STATIC_OR_LIVE=STATIC build/package checks only
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_NEW_TEST
PROVEN=Paired builds, scoped final checkpoint call audit, signed executable equality, image roundtrip, mock input gates
REJECTED=This proves a live R312 result or historical failed-boot state
UNPROVEN=Live receipt, runtime data, loaded-byte identity, VCPU execution
NEXT=User-run privileged read-only preflight; review output before installation or boot preparation

## Confirmed preparation results

R310's unbounded helper base-array dereference was removed. R311 logs at most three slots inside the existing discovery parser's count-bounded loop. The later CP04-derived helper logs scalar software fields only, then reaches the existing intentional panic boundary. No new VCN register access is added. Earlier driver initialization still touches hardware.

Baseline and candidate objects and full modules both build in one isolated tree/toolchain. VCN object byte changes are confined to hw_init.cold. Five discovery function symbols change bytes: three have equal instruction text after symbolizing direct targets, while parser main/cold code changes with logging. This is not whole-program semantic equivalence. Final linked checkpoint call relocations include logging and panic only; the audit does not establish all transitive behavior or historical module equivalence.

R312 reuses the R303 network-first environment with the new signed module and stage text. Executable sections match before/after stripping/signing. Archive extraction matches the staged file/link/mode manifest exactly. Mock CPU/PTY gate tests pass 11/11. No installation or boot occurred.

## Interpretation limits

Parser output and the later scalar checkpoint are different observation times. Parsed entries may be superseded by duplicate entries or later pointer changes. Missing parser output cannot distinguish count0 from missing delivery. Metadata and readback do not prove physical VCN activity. A future matching observation supports this new boot only, not CP06/07 retrospectively.

The retained public token R299-CP03-RECEIVED is intentionally unchanged. It is an operator confirmation string, not a secret or automatic proof that this boot's receiver is ready. The user must see and save **R312 QUALIFICATION_COMPLETE** before entering it. Mock tests do not prove actual console/network/panic delivery.

## Hypotheses and discriminating outcomes

Supporting evidence: R303 pre-access marker receipt; R308 normal-boot base metadata; R309 compiled producer comparison.
Contradicting evidence: no R312 live observation yet.
Unknown: failed-boot inputs, final selected pointer, device state, stopped instruction, VCPU execution.
If the address explanation is wrong: parsed values may match while later state or device-side response differs.
Next experiment: expected parsed values plus compatible scalar conditions support only the new boot's software premises; unexpected values revise those premises; absent/incomplete output is inconclusive and does not justify a repeated hanging read.

## Release and recovery

The installer defaults to privileged read-only boot inspection and writes only its local report. It checks protected normal/recovery identities, old R303 identity, package hashes, pending boot selection and space. Saved default must explicitly identify a protected normal entry, otherwise stop for review. sudo required a password in this session, so no privileged preflight was performed.

Do not add --install until the report is reviewed. Installation, if later selected, backs up and replaces only R303, preserves protected entries, does not write grubenv/select a boot/reboot, and verifies copied hashes. Rollback covers caught exceptions; power loss, SIGKILL and recovery-copy failures are not guaranteed recoverable by the script. Manual normal-entry recovery must remain available.

No boot choice or reboot instruction is issued by this checkpoint. The eventual observation boot intentionally panics and may require manual restart. Do not assume automatic restart or repeat CP06/07.

Public evidence excludes raw init/network configuration, private keys, binary images and raw local logs.
