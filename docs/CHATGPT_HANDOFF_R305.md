# R305 — saved register addressing and access dispatch

Static review finds no CONFIG-versus-STATUS base-index mismatch in the saved source. Both use VCN instance0 segment1; Cyan maps VCN to UVD0. CONFIG and STATUS are neighboring dword offsets in the same mapped segment. With the R303-reported 524288-byte register aperture, both calculated offsets are within the direct MMIO range. This is a conditional static result, not attestation of the failed CP06/07 runtime base table.

SOC15 macros can dispatch through SR-IOV/RLC, but the checkpoint helper rejects VF before its accesses. Under that non-VF condition, amdgpu_device_rreg/wreg are selected. Those functions first check skip_hw_access, then choose in-aperture access or indirect PCIe access. The in-aperture KIQ branch additionally requires SR-IOV runtime. The normal non-VF in-aperture path uses readl/writel. Finding both SR-IOV and device calls in object code does not prove both branches executed.

A returned writel and post-write marker do not establish device-side command completion or a physical power transition. A following read requires a response and may have different completion behavior. This is a possible distinction, not a diagnosis of the reported blackout. Existing read-return traces are absent. The software guard tests establish flag/VF eligibility, not physical power, clock, isolation or successful device response.

No source-level addressing difference found here justifies a new trial. Preserve CP05 as prior write-return proof, CP04 as current pre-MMIO transport proof, and CP06/07 cause as UNPROVEN. Next static work: reconcile exact retained build/header provenance and inspect power/clock/isolation prerequisites against saved external material before proposing a hardware change.

Sources inspected: soc15_common.h, amdgpu.h, amdgpu_reg_access.c, cyan_skillfish_reg_init.c, cyan_skillfish_ip_offset.h, vcn_2_0_0_offset.h, amdgpu_device.c and retained checkpoint helper sources. No new binary attestation or live register access.

STAGE=R305 saved-source register access review
RESULT=Shared base segment and conditional direct-MMIO dispatch established statically
STATIC_OR_LIVE=PROVEN_STATICALLY source logic; runtime failed-boot path UNPROVEN
HARDWARE_ACCESS=NONE; filesystem only
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=No new observation
PROVEN=Saved macro/base/accessor relationships
REJECTED=Write return proves physical power or read safety; object branch presence proves execution
UNPROVEN=Failed-boot runtime addresses, exact stopped instruction, device response and VCN execution
NEXT=Exact build/header provenance and saved prerequisite review; no live trial
