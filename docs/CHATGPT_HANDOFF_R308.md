# R308 — Current normal-boot discovery base metadata

STAGE=R308
RESULT=PROVEN_LIVE (exported metadata only)
STATIC_OR_LIVE=LIVE_SYSFS_METADATA plus saved-source comparison
HARDWARE_ACCESS=NO_DIRECT_REGISTER_ACCESS
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NO_NEW_TEST
PROVEN=Current exported VCN entry and base array
REJECTED=Treating current metadata as failed-boot state
UNPROVEN=CP06/07 actual base array, stopping instruction, VCPU execution
NEXT=Resolve failed-boot provenance gaps from retained artifacts before any new live experiment

## Confirmed

At the timestamp in observation.json, the current normal kernel exported one VCN entry: HWID12, instance0, version2.0.3, harvest0, three base addresses. The values, in dword units under the retained source interpretation, are 0x7800, 0x7e00, 0x02403000.

The first two values numerically agree with the legacy UVD0_BASE initializer examined in R307. The third differs from the legacy zero slot. CONFIG/STATUS use segment1 in the previously inspected source, so this third-slot difference does not itself change that pair's arithmetic. Do not substitute the entire legacy table for discovery data.

This observation is a read of exported sysfs metadata only. No direct MMIO/SMN, module load, build, installation, firmware mutation, boot change or reboot occurred.

## Strong evidence

Current exported segment1 numerically supports the previously considered 0x7e00 base for this normal boot's metadata. R307's producer correction still stands: numeric equality does not mean the legacy initializer produced the value.

## Still unknown

The current normal-kernel implementation has not been attested by the retained research source. sysfs exposes a metadata representation, not an independent read of failed-boot reg_offset. CP05/06/07's actual array and executed accessor remain unknown. A single exposed entry does not prove a physical instance count. Harvest0 does not prove functional VCN.

## Hypothesis audit

| Hypothesis | Supporting evidence | Contradicting evidence | Unknown | Next discriminating evidence / if wrong |
|---|---|---|---|---|
| Segment1 should numerically be 0x7e00 for this board's metadata | Current sysfs value matches retained legacy value | None in this capture | Failed-boot values and firmware/kernel dependence | A retained boot-attributed array with a different value would limit generalization |
| All discovery slots equal the legacy table | First two slots agree | Third slot is 0x02403000, not zero | Other instances/boots | Do not use legacy table as a complete substitute; equality of the relevant slot can coexist with different producers |
| Wrong failed-boot base explains hang | No direct supporting observation | Current normal metadata is compatible with prior arithmetic, but is not a failed-boot contradiction | Address and operation actually reached | Exact failed-boot evidence would discriminate; absence does not establish wrong base |

## Best discriminating next work

Keep current metadata, historical September9 metadata, retained source, compiled modules and checkpoint live logs separately attributed. The September9 summary records a count of three bases but omits their values; it cannot retrospectively prove equality. Bounded searches of selected retained checkpoint/instance records did not locate a failed-boot array; this is not a claim that none exists anywhere.

Do not repeat CP06/07 unchanged. Any later live proposal must first name a new observable that distinguishes runtime address selection from a device-side response failure and provide a recovery plan.
