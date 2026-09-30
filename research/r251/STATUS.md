# R251 — normal VCN2 VCPU start boundary

STAGE=R251
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=saved pinned upstream source
HARDWARE_ACCESS=GPU_COMPUTE for separate Q36 review only
HARDWARE_MUTATION=none for research target
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=28 source-ordered phases and 11 register-field definitions; separate normal/DPG contracts
REJECTED=equating VCPU_CNTL reset fields with UVD_SOFT_RESET.VCPU_SOFT_RESET; equating driver busy with ready
UNPROVEN=BC250 execution of this reference path; external RBC evidence; actual VCPU fetch/execution
NEXT=trace call/error propagation, cache provenance, and an offline observation contract

Pinned Linux commit: `551c722f40809618230001baccf219193e22fc5a`. The local R152 tree contains instrumentation and is not treated as clean upstream.

Normal `vcn_v2_0_start` enables the VCPU clock, configures memory/cache routing, releases VCPU reset, unstalls/releases LMI channels, and polls `status & 2` before final RBC and ring setup. Failure returns before that final setup. The busy report bit written by the driver is `0x4`; the readiness predicate tests `0x2`. `VCPU_REPORT` is a multi-bit field (`0xfe`), not a single synonym for either condition.

`UVD_VCPU_CNTL.CLK_EN` is `0x200`. Its PMB and RBBM soft-reset fields (`0x40`, `0x80`) are distinct from `UVD_SOFT_RESET.VCPU_SOFT_RESET` (`0x8`). The latter also differs from `UVD_SOFT_RESET.VCPU_VCLK_RESET_STATUS` (`0x80000`). These are source definitions, not proof that a reported BC250 register aperture implements every field identically.

Both normal and DPG start explicitly configure `RB_NO_FETCH=1` during RBC setup, with no same-function explicit zero assignment. Therefore a claim that Linux simply clears this bit as its final fetch-enable step is not supported by these functions. Firmware behavior and later activity require separate evidence. DPG returns through another path and does not contain the normal `status & 2` polling loop; indirect DPG also stages register data through PSP.

Cache window0 derives from PSP-returned TMR fields in the PSP loading branch, or from the driver firmware allocation in the other branch. Register accessibility does not establish valid backing bytes, authentication or instruction fetch. Readiness alone is also not a sufficient validity test: all-ones satisfies `status & 2`, and the source does not independently certify the origin of such a value.

The audit records source lines/hashes and semantic phase order in `results.json`; it does not execute a hardware sequence. `CC_UVD_HARVESTING` header names are MMSCH_DISABLE bit0 and UVD_DISABLE bit1. The header alone does not specify physical power isolation or identify a pre-ABL writer.

The added register-inventory.json indexes134 lexical register-access call sites across8 startup/helper/test functions, with source lines and expression hashes. Conditional alternatives, retry loops and DPG staging remain separate; these are not134 executed operations. Host queue-memory updates remain in the28-phase audit.
