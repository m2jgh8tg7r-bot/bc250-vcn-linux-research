# External research comparison

This document records how this project currently interprets several other public BC-250 efforts. External claims remain external until independently reproduced on the tested hardware.

## daveconde/bc250-vcn-enable

This project is the most directly relevant external comparison for real VCN bring-up.

It investigates, among other things:

- SMU/domain-6 behavior associated with VCN power and clocks,
- PMFW/SMU internal state and handlers,
- firmware-controlled power sequencing,
- direct VCN firmware placement/start paths,
- ring-execution-oriented proof techniques.

The tested environment described there overlaps meaningfully with the local test platform, including BIOS 3-era hardware and PMFW 0.58.6.0-class firmware.

However, its live techniques can include a much larger mutation surface than this project's bounded NBIO experiment, such as SMU firmware/SRAM modification, handler redirection, exploit-assisted writes, direct firmware loading, and other invasive operations.

Current policy: use it as high-priority static comparison material. Do not treat its reported success as local proof and do not automatically run its live tooling.

## simpmix/bc250-encoding-decoding-fix

This project explores a different route: using RDNA compute/Vulkan to provide VA-API-style video functionality without relying on the locked VCN silicon.

That makes it useful as a practical fallback route for applications such as streaming or recording, but it is conceptually separate from this project's goal:

```text
this project: real VCN -> power -> firmware/VCPU -> ring -> video APIs
compute workaround: GC/RDNA compute -> VA-API-compatible path
```

A compute-based encode/decode path must not be reported as proof that the physical VCN block has been enabled.

## leogx9r/ryzen_smu

`ryzen_smu` is useful as a reference implementation for Linux-side SMU/SMN transport concepts, including mailbox and SMN access patterns.

Cyan Skillfish / BC-250 is not treated here as a directly supported platform merely because a similar SMU family is supported elsewhere.

Current use: design/reference material for transport, timeout handling, and interface structure—not a blanket authorization to load or use it for VCN enablement.

## Comparison rule

For all external projects:

```text
EXTERNAL_REPORTED_SUCCESS != LOCAL_REPRODUCTION
```

Useful external findings may influence what this project audits or tests next, but local status markers change only when the corresponding boundary is reproduced on the local BC-250.
