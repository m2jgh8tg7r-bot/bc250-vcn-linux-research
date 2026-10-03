# R309 — Compiled discovery branch comparison

STAGE=R309
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=STATIC saved ELF inspection
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_NEW_TEST
PROVEN=Two retained function byte comparisons; branch shape; resolved string relocation differences
REJECTED=Inspected producer-function byte differences explain CP05/06/07 differences
UNPROVEN=Failed-boot flag values, loaded bytes, discovery data, stopping instruction, VCPU execution
NEXT=Prioritize runtime-data provenance over repeating these function comparisons

## Confirmed

Before relocation is applied, the retained CP05/06/07 ELF modules contain byte-identical amdgpu_discovery_set_ip_blocks functions (5599 bytes) and byte-identical amdgpu_discovery_reg_base_init functions (1786 bytes).

The selector's relocation lists also match. Its inspected compiled branch tests mask 0x40 at device-relative offset 0x690: clear branches to a call relocated to cyan_skillfish_reg_base_init; set falls through to amdgpu_discovery_reg_base_init. Retained amd_shared.h defines AMD_APU_IS_CYAN_SKILLFISH2 as 0x40. This confirms the compiled branch shape corresponding to R307; this stage does not independently attest the structure-field offset using DWARF or prove that this branch executed.

The parser's raw relocation lists differ. Every differing entry is among six selected references to diagnostic format strings in .rodata. Resolving these six references shows identical NUL-terminated string contents across all three modules; the remaining relocation records match. The audit retains both raw records and resolved strings, so it does not hide layout differences.

## Strong evidence

No inspected selector/parser function-code difference explains the checkpoint difference. The residual relocation-address differences are consistent with layout differences of identical diagnostic strings. This is bounded static evidence, not complete module or transitive-callee equivalence.

## Still unknown

Runtime apu_flags, the discovery blob used on a failed boot, reg_offset contents, loaded module bytes and the exact stopping instruction are still unproven. Matching retained code can behave differently with different input data or device state. Current normal-boot sysfs values from R308 cannot supply failed-boot runtime evidence.

## Hypothesis audit

| Hypothesis | Supporting evidence | Contradicting evidence | Unknown | Next discriminating evidence / if wrong |
|---|---|---|---|---|
| These producer function bytes changed between checkpoints | None | Both inspected functions have equal byte hashes; selector relocations match, parser differences resolve to equal strings | External targets and inputs | Do not repeat this comparison without changed artifacts; different runtime input can explain different outcomes despite equal code |
| A different discovery blob/base was used on a failed boot | No direct supporting saved observation | None; current normal-boot metadata is not a failed-boot contradiction | Exact failed-boot blob/base | A boot-attributed pre-access metadata record could support or reject a numerical base difference for that trial |
| A returned write implies subsequent read safety | CP05 post-write marker only proves CPU return | No direct contradiction established; the implication is unsupported | Read completion, power/isolation, operation reached | Existing write marker cannot discriminate these; preserve the unknown rather than repeat a hanging read |

## Best discriminating next work

Search retained boot-attributed discovery inputs/metadata within a bounded scope. If unavailable, record that gap. A future observation proposal should capture software state before the first VCN access; any live proposal needs a separate decision and must not silently add or repeat the failed read. This checkpoint supplies no new justification for hardware mutation.

Audit runs readelf/objdump and reads ELF bytes only; modules are never executed. Function hashes and relocation lists are in results.json. Module identities were previously checked in R306/R307. No new kernel build, install, reboot or hardware operation occurred.
