# R257 — VCPU reset fields are generation-specific

STAGE=R257
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=five reference driver/header families at one pinned Linux commit
HARDWARE_ACCESS=none by audit
HARDWARE_MUTATION=none
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=different reset-release register contracts in VCN2.0 versus2.5/3.0/4.0/5.0
REJECTED=copying reset semantics based only on the VCPU_CNTL name or an equal bit number
UNPROVEN=exact BC2502.0.3 implementation of every reference field; cause of external VCPU nonresponse
NEXT=integrate version-specific field mapping into the offline evidence contract

The inspected VCN2.0 driver releases VCPU reset through `UVD_SOFT_RESET.VCPU_SOFT_RESET` (mask0x8). VCN2.5,3.0,4.0 and5.0 reference drivers instead use `UVD_VCPU_CNTL.BLK_RST` (mask0x10000000). In the2.0 register header, that same0x10000000 value is named `CABAC_MB_ACC`, and `BLK_RST` is absent. Clock-enable mask0x200 is shared across these samples, but a shared clock field does not make reset fields interchangeable.

This supports narrowing the external VCPU_CNTL suggestion by exact IP/header generation. It does not establish which source the external researcher used, nor prove that the2.0.0 header completely specifies BC2502.0.3 silicon. No later-generation bit write or startup transplant is proposed.

A second distinction: `UVD_RB_ARB_CTRL.VCPU_DIS` exists in the2.0 header (mask0x8) but is not referenced anywhere in the inspected `vcn_v2_0.c`. Later reference drivers explicitly handle it near reset release with a comment about VCPU register access. Its physical role and current value on BC250 remain unknown; bounded source absence is not proof that firmware or UEFI never handles it.

The source and header hashes, reset-release witnesses and five-family comparison are recorded in `results.json`. All files are pinned to `551c722f40809618230001baccf219193e22fc5a`.
