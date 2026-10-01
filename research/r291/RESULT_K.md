# R291-K result — Cyan platform contract (partial)

Date: 2026-10-01

Classification: PARTIAL / STATIC SEARCH

Confirmed:
- PCI ID 1002:13FE is classified as CHIP_CYAN_SKILLFISH | AMD_IS_APU.
- SMU IP version 11.0.8 selects cyan_skillfish_set_ppt_funcs().
- cyan_skillfish_ppt_funcs still has no VCN power callback.
- is_vcn_enabled() does not observe physical VCN power. It only scans VCN/JPEG IP blocks and returns false when one is present but status.valid is false; otherwise true.
- Therefore is_vcn_enabled() is not a hardware power-good check and does not invalidate the R291-J no-op-success finding.

Not yet resolved:
- The actual runtime adev->pg_flags / adev->cg_flags for Cyan Skillfish.
- The R291-K grep output showed several soc15.c AMD_PG_SUPPORT_VCN_DPG assignments, but those were generic IP_VERSION cases and were not tied to CHIP_CYAN_SKILLFISH by this audit.
- SOC15/NV direct CHIP_CYAN_SKILLFISH context was empty, so the platform flags must be traced through the actual IP-version/initialization path rather than inferred from nearby DPG references.

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO
