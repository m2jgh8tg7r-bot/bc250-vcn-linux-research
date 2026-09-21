# BC-250 VCN Linux research

Reverse-engineering and Linux enablement research for AMD BC-250 / Cyan Skillfish VCN 2.0.3.

This repository documents reproducible findings from a staged Linux/amdgpu bring-up effort. The project separates software registration, firmware enrollment, power state, VCPU execution, ring execution, and end-user VA-API functionality instead of treating them as one milestone.

## Latest handoff — 2026-09-21

[R206: saved metrics producer trace](docs/CHATGPT_HANDOFF_R206.md) confirms that the saved metrics-format patch moves the DCLK store from internal offset 76 to 96, supporting R205's layout-mismatch explanation. The original producer reads calculated clock-slot values; average and current fields are not independent physical-liveness observations. External patch/driver identity remains unproven. No hardware access or patch application occurred.

[R205: metrics layout mismatch qualification](docs/CHATGPT_HANDOFF_R205.md) adds a conditional CPU model: an 8-core PMFW record decoded by a 6-core driver can place DCLK-derived data into the power field at offset 44 without changing the Linux ABI. Thus R204's field-name finding alone cannot disprove the external value's DCLK origin. The actual external producer/decoder pairing and physical clock state remain unproven.

[R204: saved metrics ABI audit](docs/CHATGPT_HANDOFF_R204.md) finds that byte offset 44 is `average_soc_power`, not DCLK, in the verified local v2.2 format. The saved native R72 sample has 1111 there; external format/decoder provenance remains unresolved. [R203](docs/CHATGPT_HANDOFF_R203.md) separates Domain6 power bookkeeping from physical state and reconstructs the cached-slot power policy. [R202](docs/CHATGPT_HANDOFF_R202.md) connects feature lifecycle with callback registration. All work used saved files; no new hardware access.

[R201: independent Robin1 control-flow reconstruction](docs/CHATGPT_HANDOFF_R201.md) corrects the external call/branch targets in the fixed local image. The candidate is strongly consistent with GDDR6 clock spread-spectrum configuration, not an established VCN power-up route. Sanitized instruction evidence and a CPU-only checker are included. Research remains static/read-only.

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

