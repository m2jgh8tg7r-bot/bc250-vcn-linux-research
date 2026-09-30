# Offline VCPU/RBC observation contract

This contract interprets already-collected observations. It contains no acquisition commands or hardware-write procedure. The September30 Discord summary is an attributed report; no raw capture was supplied.

## Keep the observations separate

1. Register access: a read returns a value, or a readback agrees with a write. Identify the actual symbolic register and address-mapping provenance. “Cache register” may mean configuration, aperture/data, or another interface; these are not interchangeable.
2. Ring state: pointer values change. Establish who can write each value; host-initialized equality or a changed host write pointer is not autonomous consumption.
3. Ring effect: a submitted, identified normal driver test causes its expected independent effect. Distinguish the VCN2 packet-start scratch test from the generic scratch test. Record what excludes a direct host write or stale result.
4. VCPU readiness: the normal driver observes status mask0x2, with read validity and initialization history established. This is a firmware-ready convention used by source, not a program-counter trace or proof of all codecs.
5. Service execution: a normal session message completes with attributable status/fence evidence.
6. Codec output: hardware-attributed decode yields validated frames. CPU or Vulkan results belong to different paths.

These are dimensions of evidence, not an automatic proof ladder. One observation does not certify all preceding or following layers.

## Bind a comparison to its conditions

Capture provenance should identify a single boot/session using a local opaque label, source revision and modifications, module and firmware identity evidence, VCN/IP mapping, load mode (PSP or driver), power mode (normal, DPG direct, DPG indirect or virtualization), acquisition method and phase/time. Do not publish machine identifiers. A differing kernel, firmware payload, mode or boot sequence invalidates a naive before/after comparison. Identity fields are supplied labels, not a verification of resident bytes; describe whether a hash identifies only a saved file.

Useful already-collected values include VCPU control, soft-reset request/status, VCN status, firmware cache BAR/OFFSET/SIZE, RBC control and pointers, LMI stall state, and relevant power state. Values must retain width and read-validity provenance. All-ones is a warning about ambiguous reads, not an automatic determination of bus failure; all-zero also needs context.

## Conservative interpretation

- The interpreter supports the `vcn_2_0_0` reference map only. An omitted map is an explicit assumption and missing provenance; an explicitly different map is rejected. BC2502.0.3 applicability is still a separate question. R257 establishes that bit0x10000000 in VCPU_CNTL is `CABAC_MB_ACC` in this map but `BLK_RST` in later families; these meanings must not be mixed.
- `UVD_RB_ARB_CTRL.VCPU_DIS` is reported as a named bit only. The inspected VCN2.0 driver does not reference it; later drivers' comments do not prove its BC250 physical behavior.
- `VCPU_CNTL.CLK_EN` records a requested enable bit, not a physical clock measurement.
- `SOFT_RESET.VCPU_SOFT_RESET` and `VCPU_VCLK_RESET_STATUS` differ. PMB/RBBM reset fields in VCPU_CNTL are not substitutes.
- Status readiness mask0x2 differs from busy mask0x4. Busy may have been set by the driver itself. A stale value or all-ones can satisfy a simple mask predicate.
- Cache register accessibility does not validate its backing memory, accepted firmware placement, mapping units, executable image or instruction fetch. PSP-returned addresses and driver allocations are distinct source branches.
- DPG indirect cache zeros in a staged table can be placeholders. Do not apply a normal live-register rule to the table contents.
- `RB_NO_FETCH=1` is explicitly used during both reference start paths. Its isolated value does not prove a broken final sequence or identify which agent owns the next transition.
- Harvesting value3 decodes named MMSCH_DISABLE and UVD_DISABLE fields in the reference header. The header does not define complete-block isolation or identify who set them before ABL0.

## What is currently missing

The report does not yet distinguish direct register access from an independent ring-command effect, nor attribute its conditions to a pinned normal/modified kernel and firmware path. The most valuable additional evidence is an existing, sanitized, same-boot record that binds those observations to mode, mapping provenance and VCPU-ready/reset/cache state. No fresh hardware operation is prescribed here.

A valid RBC effect alongside no VCPU-ready observation would narrow the boundary, but would not uniquely select reset, clock, firmware backing, bus access, memory routing, authentication or early firmware execution as the cause. “VCPU never executed any instruction” is stronger than “no ready report was observed.”

## Comparing two existing captures

`compare_captures.py left.json right.json --output comparison.json` compares saved scalar inputs only. It withholds differences when required context labels are missing or disagree. Phase labels may differ, but their chronology is not verified. Missing values stay unknown; different numeric notation for the same value is not a delta. Even compatible labels and a ready/pointer delta do not prove autonomous execution. Fourteen synthetic controls cover cross-boot/source/module/firmware/mapping/read/load/mode mistakes, missing values, generation mismatch and ambiguous reads.
