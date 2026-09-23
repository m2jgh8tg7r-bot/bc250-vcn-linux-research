# Safety boundaries

The BC-250 VCN bring-up work is intentionally staged so that each new hardware boundary is proven separately. This document records the rules used to prevent a software milestone from being misreported as a hardware milestone.

## Interpretation rules

Always preserve these distinctions:

```text
RING_SOFTWARE_REGISTRATION != RING_HARDWARE_EXECUTION
PSP_FIRMWARE_TRANSFER_OR_ENROLLMENT != VCN_VCPU_EXECUTION
NBIO_DOORBELL_ROUTING != VCN_WHOLE_BLOCK_POWER
SOFTWARE_POWER_BOOKKEEPING != HARDWARE_POWER_STATE
```

Until separately demonstrated:

```text
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
VCN_VCPU_EXECUTION=UNPROVEN
VCN_RING_HARDWARE_EXECUTION=UNPROVEN
```

Do not state that "VCN works" or that hardware decode/encode works until ring execution and normal userspace video APIs are confirmed.

## Parser/build/script failures are not hardware failures

A source matcher failure, shell quoting bug, parser error, build failure, artifact-install failure, or boot-selection failure must be classified at its actual layer. It is not evidence of VCN hardware failure.

## Live-write risk

The hardened NBIO experiment orders restoration immediately after target readback. This reduces the amount of code between the target write and restoration, but it cannot make a live write risk-free.

If the target `WREG32` itself stalls the GPU/SoC/CPU path, later restore instructions may never execute. Therefore static code ordering cannot guarantee rollback after a write-induced hard hang.

A hang during a future live write must never be automatically retried.

## Bounded NBIO transaction design

For logical register `0x00000ef3`, the final hardened transaction policy was:

1. fresh read in the same boot
2. require fresh old value `0x00000000`
3. otherwise stop with zero writes
4. perform exactly one target write `0x00080c40`
5. read target back once
6. immediately restore old value, with no logging between target readback and normal restore
7. read restored value once
8. if restoration mismatches, make emergency restore the first executable action in that branch
9. perform one final read after emergency restore
10. stop regardless of outcome

No target retry loop is permitted.

Normal maximum: 3 reads / 2 writes.
Failure maximum: 4 reads / 3 writes.

## Superseded pre-hardening artifact

An earlier experimental helper logged the target result before executing normal restore and also logged before the emergency restore path. That artifact was quarantined before any live write occurred under it and is considered **superseded / do not use**.

The later hardened helper moved restoration ahead of logging and was independently audited before build, install, and live boot.

## Quarantine scope

During the VCN software-init and NBIO work, the experiment deliberately avoided broad enablement actions such as:

- VCN core MMIO programming beyond the explicitly authorized boundary
- arbitrary SMU commands
- PSP VCN firmware execution
- VCN VCPU execution
- ring hardware tests
- VA-API claims

When a ring callback returned `-EOPNOTSUPP` under this configuration, it reflected the quarantine guard rather than a demonstrated hardware execution failure.

## External projects

External BC-250 projects may use more invasive techniques, including SMU firmware patching, exploit-based SRAM writes, PSP bypasses, direct firmware loading, or raw doorbell activity. Those techniques are valuable research references but are not automatically authorized for this project or considered locally reproduced.
