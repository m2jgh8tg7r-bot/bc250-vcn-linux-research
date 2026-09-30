# R259 — Register observation provenance and clock fields

STAGE=R259
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=pinned upstream register helpers, clock helper and headers
HARDWARE_ACCESS=none
HARDWARE_MUTATION=none
PROVEN=12 source witnesses; 6 clock/LMI masks; 11 symbolic register index entries
UNPROVEN=actual read path, physical addresses, clock state or cache-interface identity in the external report
NEXT=consolidate externally comparable evidence without converting source fields into physical diagnoses

The reference clock helper handles separate RBC and VCPU gate and mode fields. It explicitly clears dynamic-clock mode when the corresponding capability is absent. This adds clock-controller context beyond VCPU_CNTL.CLK_EN, but separate named bits do not define independent physical power domains or prove a measured clock.

SOC15 register indices depend on an instance-specific base and BASE_IDX. The lower-level direct MMIO helper converts dword indices to byte offsets. UVD and VCN HWIP identifiers alias in this source, while the actual SOC15 read dispatch still depends on a configured RLC helper. No physical register address is inferred from a header index alone.

The generic amdgpu_device_rreg helper can return software zero before a bus read when its skip-access predicate holds. This is an acquisition-provenance condition, not a diagnosis of any supplied capture. A numeric value alone cannot establish which read branch ran.

The phrase “VCPU cache register” remains ambiguous: cache mapping configuration and a cache-content access interface are different observations. The report needs its exact symbolic name and mapping provenance before these source definitions can be compared. No new device collection is implemented or requested by this artifact.

Three harvest namespaces are now explicitly separated: reference CC_UVD_HARVESTING bits0/1 name MMSCH_DISABLE/UVD_DISABLE; the software VCN harvest_config bits0/1 mean instance0/instance1; the software harvest_ip_mask bits0/1 mean VCN/JPEG IPs. Discovery table handling maps instance numbers to software masks. It does not define the physical effect or pre-ABL writer of the CC register. Equal numeric values across these namespaces are not interchangeable evidence.
