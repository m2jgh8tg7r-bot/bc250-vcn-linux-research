> **2026-09-22 R225:** saved TOS matches the external t02 0x5244/SVC-F2 pattern, while runtime address and 31-versus-32 entry interpretation remain open [Evidence and limits](docs/CHATGPT_HANDOFF_R225.md).

> **2026-09-22 R224:** saved type-2 TOS confirms the static t02 SVC-F2 path; Linux source confirms command fw_type 13 is VCN, distinct from BIOS directory type 0x13 [Evidence and limits](docs/CHATGPT_HANDOFF_R224.md).

> **2026-09-22 R223:** Disambiguate saved PSP type 0x13 as debug-unlock candidate; downgrade VCN fw_type numeric match. [Evidence and limits](docs/CHATGPT_HANDOFF_R223.md).

> **2026-09-22 R222:** Saved PSP directory type 0x13 candidate found and checksum verified; semantic identity remains unproven. [Evidence and limits](docs/CHATGPT_HANDOFF_R222.md).

> **2026-09-22 R221:** Update reusable packet with R220 external PSP findings [Evidence and limits](docs/CHATGPT_HANDOFF_R221.md).

> **2026-09-22 R220:** External evidence audit PSP AUTOLOAD fw_type 13 root clamp priority no hardware mutation [Evidence and limits](docs/CHATGPT_HANDOFF_R220.md).

> **2026-09-22 R219:** Reusable R218 continuation packet for ChatGPT review and next-week direction setting. [Evidence and limits](docs/CHATGPT_HANDOFF_R219.md).

> **2026-09-22 R218:** Service-1 bootstrap traced to SVC-derived mapped input; user-section mapping and kernel source-base chain checked. [Evidence and limits](docs/CHATGPT_HANDOFF_R218.md).

> **2026-09-22 R217:** Saved PSP TOS command-6 status transport and mutable service routing verified; rejection producer remains unknown. [Evidence and limits](docs/CHATGPT_HANDOFF_R217.md).

> **2026-09-22 R216:** The saved setter enters priority6 and the walker priority4. A queue-backed witness explains gate consumption before setter entry without requiring mid-handler preemption; historical timing remains unproven. R217 continues PSP analysis. [Evidence and limits](docs/CHATGPT_HANDOFF_R216.md).

> **2026-09-22 R215:** Resource claims and grants are distinct; saved interrupt state is restored before return or scheduler transfer. A bounded instruction model passes 4096 cases. R216 is tracing outer dispatch. [Evidence and limits](docs/CHATGPT_HANDOFF_R215.md).

> **2026-09-22 R214:** Directory/body checksums verify that the second same-version SMU entry is zero-filled except version words and a marker. Cyan Linux callbacks do not establish the BIOS load range. [Evidence and live-test readiness](docs/CHATGPT_HANDOFF_R214.md).

> **2026-09-22 R213:** Saved SMU header and checksum delimit a 256-KiB body plus a retained 256-byte signature trailer. Actual loader/runtime extent remains unproven. [Evidence and limits](docs/CHATGPT_HANDOFF_R213.md).

# BC-250 VCN Linux research

Reverse-engineering and Linux enablement research for AMD BC-250 / Cyan Skillfish VCN 2.0.3.

This repository documents reproducible findings from a staged Linux/amdgpu bring-up effort. The project separates software registration, firmware enrollment, power state, VCPU execution, ring execution, and end-user VA-API functionality instead of treating them as one milestone.

## Latest handoff — 2026-09-21

[R212: saved BIOS image identity](docs/CHATGPT_HANDOFF_R212.md) verifies the complete analysis window in both saved P3 captures and stored Robin1/Robin3 distributions. Running SRAM identity remains unproven.

[R211: SSC caller lifecycle](docs/CHATGPT_HANDOFF_R211.md) connects the original `0xCEE1` candidate to state-transition callbacks, strengthening the SSC interpretation. [R210](docs/CHATGPT_HANDOFF_R210.md) audits Session15 BAR evidence and acquisition limits. Research remains saved-file static/read-only; physical VCN power and execution are unproven.

Recent evidence:

- Candidate, feature lifecycle, and bookkeeping: [R201](docs/CHATGPT_HANDOFF_R201.md), [R202](docs/CHATGPT_HANDOFF_R202.md), [R203](docs/CHATGPT_HANDOFF_R203.md).
- Metrics ABI, producer, and record boundaries: [R204](docs/CHATGPT_HANDOFF_R204.md), [R205](docs/CHATGPT_HANDOFF_R205.md), [R206](docs/CHATGPT_HANDOFF_R206.md), [R207](docs/CHATGPT_HANDOFF_R207.md).
- Observation/feature interpretation and saved Domain6 status: [R208](docs/CHATGPT_HANDOFF_R208.md), [R209](docs/CHATGPT_HANDOFF_R209.md).

R197 was subsequently booted on 2026-09-14: VCN response remained `0xffff0008` with zero placement. Normal recovery and later R198/R199 results are preserved in the R201 handoff; the prepared-stage note below is historical.

[R195–R197 live API results and prepared firmware comparison](docs/CHATGPT_HANDOFF_R197.md) records measured zero VCN/JPEG available rings and VIDEO_CAPS EINVAL in the normal environment, the external compute-driver update, and a single official predecessor response-only experiment. That note records preparation; the subsequent boot and recovery are summarized in R201.

[R191–R194 additional evidence checks / 最新引き継ぎ](docs/CHATGPT_HANDOFF_R194.md) adds upstream evidence for separating return codes, PSP responses, harvest metadata, codec lists, and actual VCN execution. Source versions are kept distinct; current early-sysfs behavior is not assigned to older live captures. No new VCN experiment or image was made, and no better-supported alternate firmware candidate emerged.

[R186–R190 support evidence and upstream history](docs/CHATGPT_HANDOFF_R190.md) preserves the AMD product-support statement, standard-PSP default history, firmware catalogue, and five-project claim audit.

[Previous R182 results and R183–R185 audit](docs/CHATGPT_HANDOFF_R185.md) preserves the live response baseline, normal recovery, and 21-version firmware audit.

[Previous R182 pre-boot handoff](docs/CHATGPT_HANDOFF_R182.md) remains available as history.

[Previous R180 pre-boot handoff](docs/CHATGPT_HANDOFF_R180.md) remains available as history.

[Previous R169 handoff](docs/CHATGPT_HANDOFF_R169.md) remains available as history.

## Historical status

Confirmed on the tested BC-250:

- Cyan Skillfish exposes a VCN 2.x IP block, and the host driver can acquire and parse the selected firmware image. This is not PSP acceptance: R171/R173 returned a nonzero PSP status and zero placement.
- Real VCN software lifecycle (`early_init`, `sw_init`, `sw_fini`) can run under a quarantined custom amdgpu.
- VCN software rings (`vcn_dec`, `vcn_enc0`, `vcn_enc1`) are registered, but hardware IB execution remains deliberately blocked.
- Automatic Cyan PSP VCN firmware enrollment can be suppressed for controlled experiments.
- The stock Cyan VCN power request path does not provide proof that the VCN whole block is powered.
- The VCN NBIO doorbell-range register path was identified at logical register `0x00000ef3`.
- A bounded live transaction on that register was completed successfully:
  - fresh value `0x00000000`
  - target write `0x00080c40`
  - exact target readback `0x00080c40`
  - immediate restore to `0x00000000`
  - exact restore readback `0x00000000`
- The dedicated live-test boot entry was removed after the successful transaction so the experiment cannot be accidentally re-run.

That live result proves the bounded NBIO register transaction path is live and writable/readable on this board. It does **not** prove VCN power, firmware execution, ring execution, or hardware video decode/encode.

## Unproven boundaries

These remain intentionally open:

```text
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
VCN_VCPU_EXECUTION=UNPROVEN
VCN_RING_HARDWARE_EXECUTION=UNPROVEN
VAAPI_HARDWARE_DECODE=UNPROVEN
VAAPI_HARDWARE_ENCODE=UNPROVEN
```

## Documentation

- [Current status](docs/STATUS.md)
- [Hardware findings](docs/HARDWARE_FINDINGS.md)
- [Safety boundaries](docs/SAFETY_BOUNDARIES.md)
- [Reproducibility](docs/REPRODUCIBILITY.md)
- [Research log](docs/RESEARCH_LOG.md)
- [External research comparison](docs/EXTERNAL_COMPARISON.md)
- [R124 dynamic Domain6 policy trace](docs/R124_DYNAMIC_POLICY_TRACE.md)
- [Patch notes](patches/README.md)
- [Sanitized log publication policy](logs/README.md)

## Safety

Some experiments involve live GPU register writes. A write that stalls the GPU/SoC can prevent rollback code from executing even when the source orders restoration immediately after readback. Do not treat the experimental procedures here as safe defaults for other cards, firmware versions, or kernels.

Raw personal logs are not published. Repository notes intentionally separate observed facts from hypotheses and omit usernames, UUIDs, host-specific paths, and unrelated machine identifiers.

## Collaboration

The purpose of publication is to make the work reusable by the wider BC-250 and Linux/AMD community. Independent reproduction, corrections, safer test designs, comparisons with related work, and mirroring into more appropriate public research venues are welcome.

## License

GPL-3.0. See [LICENSE](LICENSE).

