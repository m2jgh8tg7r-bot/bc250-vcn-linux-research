# External BC-250 VCN research update — 2026-09-21

This is an **external research input**, not an adopted conclusion. It supplements `EXTERNAL_UPDATE_2026-09-14_SHALASERE.md`. Before acting on it, use the repository's current handoff (R197 is the latest checked-in handoff as of this update) and preserve all existing proof boundaries.

## Evidence classes

- **EXTERNAL_PRIMARY_STATIC**: code/disassembly/diff published by the external researcher; useful evidence, but not independently reproduced locally.
- **EXTERNAL_PRIMARY_CODE**: source-code change in another project.
- **EXTERNAL_REPORTED**: interpretation/claim in external documentation that exceeds the directly demonstrated evidence.
- **LOCAL_STATUS**: state of this repository, not an external claim.

## 1. Shalasere: PSP_BL/APCB path found a real alignment bug, but the current chain stops at DoS / impractical escalation

Primary commits:
- 2026-09-18 `29cd973336c0175d19ab30cd95a7fcf93304e32b`
  https://github.com/Shalasere/bc250-vcn-research/commit/29cd973336c0175d19ab30cd95a7fcf93304e32b
- 2026-09-18 final correction/resolution `769471cb427a7f3f80ea8416ec57faa4b920c096`
  https://github.com/Shalasere/bc250-vcn-research/commit/769471cb427a7f3f80ea8416ec57faa4b920c096

**EXTERNAL_PRIMARY_STATIC:** Their published chain is:
`APCB -> FUN_066A0 -> FUN_07014 -> FUN_062F8 -> 0x01704 -> 0x05F0 -> 0x0BF4 -> 0x0CFC -> 0x0D50 -> CCP descriptor LENGTH`.
For selected encrypted APCB types, an aligned length can exceed the raw length by up to 15 bytes. The external analysis says CCP then performs in-place AES processing across those adjacent bytes. The non-encrypted path contains checks/adjustment absent from the encrypted path.

**EXTERNAL_PRIMARY_STATIC:** The final follow-up narrows exploitability substantially:
- adjacent bytes are the next APCB token header;
- AES mode is reported as AES-128-CBC with fuse key slot 9;
- the corrupted output is not attacker-predictable without the fuse key;
- no fallback-to-insecure boot path was found;
- a previously reported `0x7644` arbitrary SRAM read was **retracted**: the dereference uses fixed `0x9A44`, not an attacker-controlled pointer;
- current demonstrated impact is DoS; code-execution escalation would need an additional condition such as useful `SizeOfType` corruption/oracle behavior and is not demonstrated.

**Direction impact:** This weakens the value of treating PSP_BL/APCB exploitation as the near-term VCN unlock path. It does **not** falsify the SEC_GASKET/fabric-ACL model, the normal SMU/PMFW path, or local firmware-response work.

### Safe Codex application

1. Do not attempt exploit construction, fuse-key recovery, SPI-flash mutation, or live fault injection.
2. Static/read-only only: independently inspect the external call chain and especially the claimed differential between the encrypted and non-encrypted paths around `FUN_07014`.
3. Treat the external ledger as candidate-function prioritization, not ground truth. The important methodological lesson is that the earlier automated/heuristic SAFE sweep missed a real alignment defect; manually re-check security-relevant functions before adopting a negative conclusion.
4. Record the `0x7644` arbitrary-read claim as **retracted externally** so it is not propagated into local hypotheses.
5. Confirmation criterion: local static reconstruction independently reaches the same CCP LENGTH data flow and proves the missing bound/adjustment. Falsification criterion: argument/data-flow reconstruction shows the aligned value cannot reach the CCP descriptor as claimed.

## 2. Shalasere SMU/VCN power-path result remains a high-value independent comparison target

Primary commits already observed after the previous 2026-09-14 update:
- `e68af4ae63456074f0cae46f315f13a9bb4888c0`
  https://github.com/Shalasere/bc250-vcn-research/commit/e68af4ae63456074f0cae46f315f13a9bb4888c0
- `820297d2f292fcbd7f6b51ce11798dfc9c361f28`
  https://github.com/Shalasere/bc250-vcn-research/commit/820297d2f292fcbd7f6b51ce11798dfc9c361f28

**EXTERNAL_PRIMARY_STATIC + external live read-only observations:** The external work corrected the previously cited `0x1EE90` address: the claimed caller entry is `0x1EDD4`. It reports calls into shared routine `0x241AC` with arguments 3 and 4, guarded by two preconditions: a status-check subcall (`0x1cb58`, arg 11) and SRAM byte `0xCEE1`. Both failure paths reportedly converge on early exit `0x1eeb8`. `0xCEE1` was externally read as `0x01`.

This should not be renamed locally as `PowerUpVcn` or `power_gate_tile` without independent semantic proof. The structural call path is the useful evidence.

### Safe Codex application

- Compare the external `0x1EDD4 -> 0x241AC(3/4)` structure against the local Robin1 88.6.0 image/disassembly.
- Trace writers/readers of `0xCEE1` statically and identify the semantics of `0x1cb58(arg=11)` before any live invocation.
- Compare this path with the local R124-era dynamic-policy/callback map rather than assuming they are the same mechanism.
- Confirmation criterion: independent local disassembly reproduces entry, branch targets, argument values, and common early exit. Falsification criterion: image/version mismatch or corrected decode changes those targets/arguments.
- No unknown SMU call, no write to `0xCEE1`, and no VCN-core MMIO write is requested by this update.

## 3. simpmix compute VA-API: useful control path; its physical-VCN conclusions are not ground truth

Relevant commits:
- 2026-09-20 `f2eb143ee5bd7ac1009b813d8d6aaa7cc68aef26`
  https://github.com/simpmix/bc250-encoding-decoding-fix/commit/f2eb143ee5bd7ac1009b813d8d6aaa7cc68aef26
- 2026-09-20 `9b85e36ba096f6675f19381405b4be18d264a6a2`
  https://github.com/simpmix/bc250-encoding-decoding-fix/commit/9b85e36ba096f6675f19381405b4be18d264a6a2
- 2026-09-20 `106ea01910e7745d8b92344e7c30287d60bc1a56`
  https://github.com/simpmix/bc250-encoding-decoding-fix/commit/106ea01910e7745d8b92344e7c30287d60bc1a56

**EXTERNAL_PRIMARY_CODE:** The compute encoder continues to advance independently of physical VCN. Recent changes add Vulkan subgroup arithmetic for H.264 motion-estimation reduction and GPU ME / reciprocal-division optimizations for HEVC. This remains a CU/Vulkan compute VA-API implementation, **not VCN VCPU/ring execution**.

**EXTERNAL_REPORTED / caution:** `f2eb143e` rewrites the project's hardware notes around VCN 2.0.3, SEC_GASKET/fabric ACL, `0x1f81c`, and `0x1f820`, but also makes stronger claims such as physical VCN being definitively impossible to unlock and all exploit vectors being closed. Those conclusions should not be imported as proof. In particular, Shalasere's later 2026-09-18 manual review found a real APCB alignment vulnerability after an earlier broad negative sweep, then narrowed it to DoS/currently impractical escalation. Therefore preserve separate labels for measured/static mechanism versus broad impossibility claims.

### Safe Codex application

- Keep simpmix as a **control/alternative userspace path** only.
- If future local VCN execution succeeds, compare normal VCN VA-API/FFmpeg behavior and resource usage against this compute path.
- Do not use simpmix documentation as evidence that SEC_GASKET, harvesting, firmware acceptance, or physical impossibility has been locally proven.

## 4. Other monitored sources

As of the 2026-09-21 check, no newer result from `cachenetics/project-ariel`, `bc250-collective/amd_smu_reverse_engineering`, `AMD-BC-250/documentation`, `elektricM/amd-bc250-docs`, `Keshas-dev/AMD-BC-250-Windows-Driver`, or `PSPReverse/PSPTool` was found that supersedes the above for physical VCN power/reset, VCLK/DCLK, firmware/VCPU, ring execution, or normal VCN VA-API/FFmpeg decode. Project Ariel's recent musl ioctl fix is unrelated to VCN.

The unofficial community guide contains consolidated VCN claims, but it is secondary material and may preserve stale naming/interpretations. Use primary commits/disassembly/live logs instead.

## 5. External use/reference of this repository

Shalasere's repository has already added `m2jgh8tg7r-bot/bc250-vcn-linux-research` to its community references and describes it as the Linux enablement / firmware-ring-doorbell staging line. This is credible evidence that the external researcher is aware of and references this research line. It is **not** by itself proof that a distinctive R-series result has been independently reproduced.

Do not claim external validation of R-series findings unless a later primary source explicitly reproduces a distinctive measurement, mapping, script result, or methodology.

## 6. Recommended next research ordering

This update does **not** justify abandoning R197's carefully separated firmware-response experiment. It does change the relative value of side branches:

1. Preserve R197 firmware-response work as its own proof boundary.
2. In parallel, perform a static-only independent reconstruction of `0x1EDD4`, `0x1cb58(arg=11)`, `0xCEE1`, `0x1eeb8`, and `0x241AC(3/4)` in the exact local Robin1/SMU 88.6.0 image.
3. Trace `0xCEE1` writers and the status predicate backward to initialization/policy inputs; compare with local Domain6/profile/callback evidence.
4. Treat PSP_BL/APCB exploitation as a lower-priority static research branch unless a new controllable primitive appears. Preserve the alignment-bug result and the retraction of the arbitrary-read claim.
5. Keep SEC_GASKET/fabric ACL, Domain6 sequencer state, VCN register-file accessibility, PSP firmware acceptance, VCPU execution, hardware ring execution, and VA-API/FFmpeg as separate proof boundaries.

## Requested handoff behavior

After independently checking the useful external inputs above, create a new handoff only for results that are actually reproduced or materially change the local evidence graph. Label external-only facts explicitly and do not promote them to PROVEN_LOCAL without local evidence.