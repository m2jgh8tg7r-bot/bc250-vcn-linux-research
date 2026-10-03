> Latest R297 CP07: [Attempted boot: blackout reported, postmortem zero pstore; execution boundary UNPROVEN](docs/CHATGPT_HANDOFF_R297_CP07.md). [Observation coverage audit](docs/R297_CP07_OBSERVABILITY_AUDIT.md). Do not repeat unchanged CP07; CP05 remains strongest saved LIVE checkpoint.

# BC-250 VCN Linux research

## Latest — R297 CP03 LIVE PASS, 2026-10-02 JST

[CP03 full-module handoff](docs/CHATGPT_HANDOFF_R297_CP03.md) · [formal result](research/r297/RESULT_CP03_FULLMODULE_PASS.md): the R274B + CP03 full-amdgpu composition now passes the corrected relocation-target audit with `MAKE_RC=0`, `CP03_MACHINE_CODE_CONTRACT=PASS`, source restoration PASS, and final script exit 0. The full module is unchanged from the earlier build (`SHA256 9a9bc4fd…`, Build ID `94c0a230…`), confirming the prior exit 1 was audit-tooling only. The exact CP03 module has also passed HOME-only packaging and initramfs round-trip (`SIGNED_MODULE_SHA256 43f177df…`, `IMAGE_SHA256 eb71ca03…`) without any `/boot` write or boot selection change. LIVE proof now includes entry into the Cyan `vcn_v2_0_hw_init()` branch at `BC250 R291P1 pre_reset: begin`, followed by the intentional CP03 panic before helper execution.

### Previous — R269, 2026-10-01 JST

[Write-disable versus disable; first-request boundary](docs/CHATGPT_HANDOFF_R269.md): explicitly downgrades the SMN-to-UVD-disable fuse interpretation to an unresolved field-mapping hypothesis. CC bit definitions, SMN words, Thomas's named fields and discovery metadata remain separate. Fault silence is not proof of absent fetch. The fixed original Shalasere archive is unchanged. [R267–R268 preparation](docs/CHATGPT_HANDOFF_R268.md) adds saved-counter analysis and ordinary-API preflight; critical new acquisition is not ready and no VCN device test was performed.

### Previous — R266, 2026-10-01 JST

[Fixed Shalasere external baseline](docs/CHATGPT_HANDOFF_R266.md): pins final commit6c85b2fe and parentb09ef6ff, prioritizes corrections, records board-specific provisioning/prerequisite/fuse evidence, and compares Thomas observations without assuming identical hardware state. Includes negative-result reuse boundaries and discriminating cross-board outcomes. Source/raw measurement confidence is kept separate; no hardware experiment performed.

### Previous — R265, 2026-10-01 JST

[R251–R265 VCPU execution-boundary handoff](docs/CHATGPT_HANDOFF_R265.md) separates source-confirmed facts, strong reported GPCNT/RBC activity, unresolved VCPU fetch/reset/bootstrap candidates, and demoted hypotheses. Whole-domain VCLK absence and direct harvesting-clear variants are deprioritized; the cause remains unknown. Includes counter/instance distinctions, lifecycle and completion audits, a rebuttal matrix and public offline replay. No new live VCN activation is claimed. R249 remains a separate CPU checkpoint and R250 remains unfinished advisory work.

### Previous — R248, 2026-09-27

[R247–R248 handoff](docs/CHATGPT_HANDOFF_R248.md) adds input-pacing pipeline controls and B-picture CPU throughput measurements. Rawvideo output packing is not the sole explanation for the higher paced CPU cost. The compared FFmpeg paths use software decoding; no boot-option change, firmware operation or dedicated VCN execution is involved.

### Previous — R246, 2026-09-27

[R245–R246 handoff](docs/CHATGPT_HANDOFF_R246.md) adds a controlled CPU throughput comparison, input-paced CPU-load controls, and24 exact B-picture output checks. FFmpeg software decode is faster and lower-cost than the custom CPU harness in this synthetic I/P matrix. Paced CPU measurements exceed simple unpaced estimates. These results do not establish dedicated VCN or complete-player performance.

### Previous — R244, 2026-09-27

[R236–R244 research handoff](docs/CHATGPT_HANDOFF_R244.md) adds official control-file provenance, ten verified container checksums, 21-version VCN signer metadata and current source/interface checks. Running PSP/KDB identity and dedicated VCN operation remain unproven.

A GPU-free CPU video control exposed a standalone harness frame-ordering defect: the original short-GOP matrix passed 18/18; an isolated ordering variant passed both matrices 36/36. This is CPU-only evidence, not VCN activation or a production-complete patch. Q36 assistance was independently checked and its incorrect conclusions rejected.

### Previous — R235, 2026-09-27

[R235 signer controls](docs/CHATGPT_HANDOFF_R235.md) add a positive contrast: retained non-VCN main-image signer IDs match saved type51 KDB records; the VCN signer does not. Two historical captures were revalidated. Ten saved KDB occurrences reduce to two distinct bodies. Runtime KDB identity and VCN rejection cause remain unproven; control-file whole-payload CRC discrepancies are explicitly unresolved.

[R234 interface audit](docs/CHATGPT_HANDOFF_R234.md) shows that SOS version displays share driver fields and that the saved firmware-attestation interface excludes Cyan APUs. These interfaces do not establish runtime byte identity. Local Q36 reviewed the bounded argument using authorized GPU compute; no new PSP/VCN experiment or system configuration change occurred.

### Previous R233 checkpoint

[R233 handoff](docs/CHATGPT_HANDOFF_R233.md) completes the saved-image checkpoint: 14 CPU model suites (8,191 cases), byte-provenance controls, saved signer metadata, and the Cyan PSP host-loader callback contract were revalidated. The saved no-signer rejection is consistent with the historical response; runtime service-image/KDB identity and VCN execution remain unproven. September 25–26 local progress and fresh external updates are incorporated.

No hardware access or mutation occurred during closeout. No new live experiment is ready. Next: version-matched image/KDB identity evidence.

### Previous R232 checkpoint

[R232 handoff](docs/CHATGPT_HANDOFF_R232.md) restores the already-saved R218 SVC64 allocator evidence, corrects the row writer to stride0x54, and separates user pointers from file offsets. Driver-selector acquisition, registration, cleanup and the mode-dependent F2 walker are checked in 9,563 CPU-model cases. These are static results: running-image identity, live occupancy and VCN execution remain unproven.

[Transport comparison](docs/R232_TRANSPORT_CONTRACT.md) · [External evidence questions](docs/R232_EXTERNAL_EVIDENCE_QUESTIONS.md) · [Earlier external review](docs/R232_PLAN_EXTERNAL_REVIEW_20260923.md).

The requested one-hour research session is complete. No hardware access or mutation occurred. No new hardware test is ready or needed to establish these static corrections; the next step is service-image provenance.

<details>
<summary>Historical update notices (superseded where R232 corrects them)</summary>

> **2026-09-23 External review complete; R232 plan decided:** New VA-API decoding is CPU-based; platform-mailbox support does not establish VCN execution. Next: version-matched PSP registration/dispatch evidence. R228–R230 supersede the historical table-base uncertainty below: saved code computes 0x286000, while live occupancy remains unproven; SVC64 is corrected in R232. [Review and plan](docs/R232_PLAN_EXTERNAL_REVIEW_20260923.md).

> **2026-09-22 R226:** TOS initialization calls the saved 0x5244/SVC-F2 walker; 0x286000 alignment requires an unproven runtime load bias [Evidence and limits](docs/CHATGPT_HANDOFF_R226.md).

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

</details>


Reverse-engineering and Linux enablement research for AMD BC-250 / Cyan Skillfish VCN 2.0.3.

This repository documents reproducible findings from a staged Linux/amdgpu bring-up effort. The project separates software registration, firmware enrollment, power state, VCPU execution, ring execution, and end-user VA-API functionality instead of treating them as one milestone.

## Earlier milestones — through 2026-09-21

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

