# Competing VCPU hypotheses after the new positive measurements

No causal-likelihood ranking is assigned to A–F. Work priority is instruction-fetch boundary, VCPU-specific reset/isolation, bootstrap source, cache/LMI/AXI path, permission evidence, and the stock-BIOS control. Harvesting producer review is low-cost background work; direct-clear variants are outside the main line. Supporting observations indicate compatibility unless a direct causal measurement is explicitly identified. External outcomes remain attributed; lack of raw access does not erase their positive evidential weight. Each candidate includes a way it could be wrong. A/B outcomes below are discrimination criteria for existing records or controlled ordinary observations, not security-policy modification or firmware-bypass procedures.

## A. VCPU-specific reset or isolation remains active

- **Supporting evidence:** Reported RBC and GPCNT activity coexist with absent expected VCPU outputs. The normal Linux source distinguishes VCPU reset/clock controls from other controls.
- **Contradicting evidence:** Reported soft-reset release readback weakens the narrow claim that this observed request bit remains asserted. It does not establish the effective state of every internal reset/isolation signal.
- **Unknown:** Effective VCPU reset, leaf clock and isolation state; observation validity; whether an unseen control actually exists on this silicon.
- **Next discriminating evidence A/B:** A: independently attributable VCPU retirement evidence excludes a continuous reset or isolation condition that would prevent that retirement; other interface isolation remains possible. B: validated effective-state evidence showing reset/isolation active supports this candidate; request readback alone leaves it unresolved.
- **If wrong:** Fetch failure, wrong vector, execution before a stall, or invalid trace visibility explains the reported outputs.

## B. Instruction fetch path is blocked or misdirected

- **Supporting evidence:** Backing-memory/configuration readback and RBC transactions do not prove VCPU instruction-read completion. Missing bootstrap outputs are compatible with fetch failure.
- **Contradicting evidence:** No supplied VCPU-attributed successful fetch is established. Successful staging contradicts only “host could not stage these bytes,” not the fetch-path hypothesis.
- **Unknown:** Actual instruction addresses, cache source/translation, transaction initiator, response/error type, and data visible to the VCPU.
- **Next discriminating evidence A/B:** A: existing traces show a VCPU instruction read completing with expected bytes—reject a total fetch block at that address/time. B: validated VCPU-originated failed/stalled transactions localize the path, but do not alone distinguish policy, translation and physical transport.
- **If wrong:** A reset/isolation/leaf-clock condition could prevent requests entirely; alternatively execution could occur and stall before observable output.

## C. VCPU-specific permission/security restriction

- **Supporting evidence:** Different initiators can have different access outcomes; reported RBC activity is therefore compatible with a VCPU-only restriction. This is a possible mechanism, not positive evidence of a denial.
- **Contradicting evidence:** Reported domain-master enable, firmware acceptance and broader access improvements demote a simple “domain master enable is the sole remaining obstacle” explanation.
- **Unknown:** Whether there is a VCPU-specific restriction, its effective policy, and whether any observed error is attributable to permission rather than reset/translation/transport.
- **Next discriminating evidence A/B:** A: existing attributable VCPU reads succeed under the relevant policy—exclude total denial for that transaction class. B: a decoded existing permission-denial record names that initiator and transaction—support a specific restriction. Generic timeout/zero data does not choose this hypothesis.
- **If wrong:** Reset or fetch-address selection can yield the same absent-execution observations without any security denial.

## D. Reset vector or bootstrap source is wrong/uninitialized

- **Supporting evidence:** Expected first-store absence is compatible with execution entering another location; readable program bytes do not prove they are selected as the reset source.
- **Contradicting evidence:** No verified first-fetch address/source has been supplied to confirm or contradict this possibility. PC=0 does not establish a reset vector without trace validity.
- **Unknown:** BC-250 reset-vector contract, selected boot source, effective address and trace semantics.
- **Next discriminating evidence A/B:** A: existing first-fetch evidence matches the intended source and bytes—demote wrong-vector/source for that run. B: it consistently identifies another source—support a selection mismatch. No requests leaves reset/clock and fetch-path hypotheses open.
- **If wrong:** Correct vector with blocked access, reset or later firmware stall can explain the same negative markers.

## E. Harvesting/fuse effect — low-priority static background

- **Supporting evidence:** Attributed CC_UVD_HARVESTING=3 before ABL0 and absent VCPU output are correlated observations. They make an early configuration question relevant but do not establish causality or fuse origin.
- **Contradicting evidence:** Reported RBC execution and GPCNT activity strongly oppose “the whole VCN block is physically disconnected.” IP-discovery harvest=0 is a distinct namespace; it cannot cancel the CC register by numerical comparison.
- **Unknown:** Silicon semantics, writable versus latched/fused provenance, affected sub-blocks, causal link to VCPU, and earliest producer. Linux names/masks are not a physical fuse specification.
- **Next discriminating evidence A/B:** A: a working compatible VCPU observation with the same validated CC value would refute “that value invariably disables VCPU.” B: a verified hardware/firmware specification connects the field to a VCPU-specific inhibit—support that mechanism. Mere correlation across nonmatched boards cannot isolate it.
- **If wrong:** The field could mirror another cause/state, or be an unrelated availability indication, while an independent reset/fetch problem explains VCPU symptoms. Causal, mirror and unrelated-display models remain parallel. Reported nonpersistent writes do not distinguish a mirror, restoration, lock or ineffective write path. Direct-clear variants are not pursued; shelve this branch if no new discriminator appears over days.

## F. Boot-time latch or PSP/SMU policy fixes VCPU enable state

- **Supporting evidence:** Attributed early harvesting state and unchanged VCPU outcomes despite later register changes are compatible with a boot-time decision.
- **Contradicting evidence:** Later ineffective writes do not positively establish a latch. Reported changes in exposure/abort behavior show some relevant state is changeable after the earlier stage, weakening an overly broad “nothing relevant can change later” model.
- **Unknown:** Existence, producer, lifetime and reset domain of any VCPU-specific latch; applicability of another SoC's reset labels/sequencing.
- **Next discriminating evidence A/B:** A: existing validated records show the relevant effective state changing after initialization—refute strict boot-only immutability for that state. B: source or specification identifies a sampled-once VCPU enable condition with matching provenance—support a concrete latch model. Ordinary failed startup does neither.
- **If wrong:** An ordinary runtime reset/fetch/configuration fault could persist across all the reported variants.

## G. MeiMeiV3 warm reset causes the VCPU failure

- **Supporting evidence:** The reported BIOS introduces a warm reset, providing a concrete confound worth controlling. No causal evidence has yet been supplied.
- **Contradicting evidence:** A matched stock-BIOS failure would weaken the claim that MeiMeiV3's additional warm reset is necessary for this failure. Results are pending; do not describe the hypothesis as already excluded.
- **Unknown:** Stock-control outcome, equivalent driver/firmware/configuration, cold/warm power history and sampling phase.
- **Next discriminating evidence A/B:** A: already planned matched stock and modified-BIOS captures show the same clock/RBC/VCPU result—demote the specific additional-warm-reset explanation. B: VCPU activity differs reproducibly—support a BIOS/history dependency, but not warm reset uniquely because the BIOS images differ in other respects.
- **If wrong:** A shared silicon configuration or common runtime startup/fetch condition explains both BIOS outcomes.

## Stop rules

Do not add another same-direction variant unless its two outcomes would remove or materially demote a named candidate. Lack of ready is not a cause. Readback is not physical execution. Counter names, field widths and selection namespaces remain distinct. Successful staging/authentication in one reported context cannot be projected onto an older failed local load; conversely an older local failure cannot invalidate the newer report without matching contexts.
