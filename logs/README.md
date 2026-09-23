# Log publication policy

Raw personal terminal logs are intentionally not published by default.

The project instead publishes sanitized result summaries that preserve the technically relevant evidence while removing unrelated or identifying material such as:

- usernames
- hostnames
- filesystem home paths
- UUIDs
- unrelated device identifiers
- network details
- incidental application/service noise

## What should be published

For meaningful hardware stages, the public record should preserve:

- exact kernel/source identity
- exact custom-module identity
- exact firmware identity when relevant
- the authorized operation scope
- observed register values
- whether a write actually occurred
- readback values
- restoration results
- whether emergency rollback was required
- whether a hang/fault occurred
- the interpretation boundary

## What should not be inferred

A log line showing software ring registration, PSP transfer, a successful return code, or a bounded NBIO transaction must not be silently upgraded into a claim of VCN power, VCPU execution, ring execution, or video acceleration.

## R113 sanitized hardware result

The core evidence from the successful bounded live transaction is:

```text
custom amdgpu Build ID = b0ca3ad4d1f157bf2a34b7e24fe221fff3a9a9b4
fresh reg 0x00000ef3 = 0x00000000
target write           = 0x00080c40
target readback        = 0x00080c40
restore                = 0x00000000
restore readback       = 0x00000000
emergency restore      = not required
```

Retained interpretation:

```text
NBIO_DOORBELL_REGISTER_PATH=PROVEN_LIVE_WRITABLE
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
VCN_VCPU_EXECUTION=UNPROVEN
VCN_RING_HARDWARE_EXECUTION=UNPROVEN
```
