# BC-250 VCN Linux research

Reverse-engineering and Linux enablement research for AMD BC-250 / Cyan Skillfish VCN 2.0.3.

This repository documents reproducible findings from a staged Linux/amdgpu bring-up effort. The project separates software registration, firmware enrollment, power state, VCPU execution, ring execution, and end-user VA-API functionality instead of treating them as one milestone.

## Current status

Confirmed on the tested BC-250:

- Cyan Skillfish exposes a VCN 2.x IP block and accepts the expected VCN 2.0.3 firmware image.
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

That last result proves the bounded NBIO register transaction path is live and writable/readable on this board. It does **not** prove VCN power, firmware execution, ring execution, or hardware video decode/encode.

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
- [Patch notes](patches/README.md)

## Safety

Some experiments involve live GPU register writes. A write that stalls the GPU/SoC can prevent rollback code from executing even when the source orders restoration immediately after readback. Do not treat the experimental procedures here as safe defaults for other cards, firmware versions, or kernels.

Raw personal logs are not published. Repository notes intentionally separate observed facts from hypotheses and omit usernames, UUIDs, host-specific paths, and unrelated machine identifiers.

## License

GPL-3.0. See [LICENSE](LICENSE).
