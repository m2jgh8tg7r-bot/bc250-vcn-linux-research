# R234 — runtime identity interfaces in the saved Cyan driver

Date: 2026-09-27. Classification: PROVEN_STATICALLY. No live API invocation.

R233 left runtime service-image and KDB identity unresolved. R234 checks whether the existing host interfaces can discriminate those identities before considering another hardware observation.

## Results

| Interface in the saved source | What it reports | Consequence for this investigation |
| --- | --- | --- |
| `AMDGPU_INFO_FW_SOS` | Driver fields `psp.sos.fw_version` and `feature_version` | Not a runtime image digest or KDB identity |
| `amdgpu_firmware_info` SOS line | The same firmware-info helper | Not an independent second observation |
| `fw_version/sos_fw_version` | The same cached firmware version | A zero value hides the attribute at group creation; absence does not prove absent SOS |
| PSP SOS line in a device coredump | The same two driver fields | A coredump does not independently identify the service image |
| Firmware attestation debugfs | A PSP request followed by record reads, on supported devices | The saved support predicate excludes APUs; Cyan PCI entries set `AMD_IS_APU` |

The saved attestation record contains firmware IDs, version, source, validity and TA/VF fields, not an image digest or KDB contents. Its read operation submits a PSP command; a file read is not necessarily a passive cached-data read. R234 does not invoke it, remove its support gate or propose a direct request.

The bounded UAPI scan enumerates 28 `AMDGPU_INFO_FW_*` definitions, including the query selector itself; none is a KDB or service1 identity selector. This is not proof that no other interface can exist.

R233 already established that Cyan PSP 11.0.8 lacks ordinary SOS/KDB loader callbacks. R234 connects that fact to the consumers of SOS version metadata. On other ASICs, the PSP 13 implementation does populate SOS version from a register: the cached-reader conclusion must not be generalized into “all reported SOS versions come only from files.” Even a hardware-origin version would not establish complete byte identity.

## Historical observation

Saved Stage30Q text line 4450 records `SOS feature version: 0, firmware version: 0x00000000`. The current source audit explains how an unpopulated driver field can produce that display. The old text is not a new measurement and is not newly attributed to the September 14 R173/R180 boot. It does not show that PSP was absent or nonfunctional.

## Evidence and reproducibility

[Evidence JSON](../research/r234/results.json) contains 15 hash-pinned source excerpts, the UAPI selector list and the historical text hash. [Extraction script](../research/r234/audit_interfaces.py) operates on saved ordinary files only:

```sh
python3 audit_interfaces.py --source SAVED_KERNEL_TREE --history SAVED_STAGE30Q_TEXT --output results.json
```

The inspected source tree is based on commit `0bb924b042ab85b8f529aed6e4f3e24750584276`; files are individually hash-pinned. The public kernel [debugfs documentation](https://docs.kernel.org/gpu/amdgpu/debugfs.html) describes the interface but does not establish Cyan support. The support predicate in the version-matched source is decisive here.

```text
STAGE=R234
RESULT=COMPLETED_STATIC_INTERFACE_AUDIT
STATIC_OR_LIVE=PROVEN_STATICALLY; historical text retained separately
HARDWARE_ACCESS=NONE for this audit
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=cached reader relation, zero-value sysfs visibility rule, saved APU attestation exclusion
REJECTED=multiple version displays independently establish image identity; absent SOS attribute proves absent running SOS
UNPROVEN=runtime service/KDB identity and existence of another usable supported interface
NEXT=compare existing non-VCN response controls with saved signer metadata (R235)
```
