# R307 — Correct register-base producer applicability

STAGE=R307
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=STATIC
HARDWARE_ACCESS=NO
HARDWARE_MUTATION=NO
HARDWARE_FAILURE=NO_NEW_TEST
PROVEN=Compiled legacy table equality; retained source branch selection
REJECTED=Using legacy table equality alone as a BC-250 runtime base witness
UNPROVEN=Failed-boot actual reg_offset values and stopping instruction
NEXT=Locate saved discovery-derived base evidence with boot provenance

## Confirmed

The 120-byte UVD0_BASE data symbol in retained CP05, CP06 and CP07 signed modules matches the retained header initializer exactly. Each compiled cyan_skillfish_reg_base_init has a relocation referencing that symbol. Six storage slots are not six physical VCN instances.

**Correction to R305 applicability:** cyan_skillfish_reg_base_init is the non-Skillfish2 fallback. For AMD_IS_APU devices classified as CHIP_CYAN_SKILLFISH, retained amdgpu_device_init_apu_flags marks PCI 13FE/143F as Skillfish2 before IP early initialization. For that flag, amdgpu_discovery_set_ip_blocks calls amdgpu_discovery_reg_base_init instead. The latter assigns reg_offset from parsed IP discovery base arrays. The legacy table is therefore not sufficient evidence of this board's runtime base values.

CONFIG/STATUS sharing a relative base index remains a source fact. The numerical base and aperture/access-branch conclusion must remain conditional on the actual discovery-derived runtime values. This correction does not establish an incorrect address or a hardware cause.

## Strong evidence

Previously recorded normal-boot PCI identity is 13FE, consistent with the discovery branch. That earlier record is not failed-boot state attestation. CP05 live evidence of the post-write boundary remains unchanged; CPU write return is not device completion.

## Still unknown

Actual failed-boot reg_offset contents, exact execution boundary in CP06/07, device response, and VCPU instruction execution remain unproven. Static relocation presence does not prove a function ran or attest that each retained binary contains the source branch predicate shown here. No new hardware operation or build occurred.

## Hypothesis audit

| Hypothesis | Supporting evidence | Contradicting evidence | Unknown | Next discriminating evidence / if wrong |
|---|---|---|---|---|
| Legacy table differences explain checkpoint differences | None in inspected symbol | All three tables byte-identical; source selects another producer for Skillfish2 | Other binary/runtime differences | The inspected legacy symbol difference is already excluded; discovery-derived runtime differences are a separate unresolved question |
| Legacy table proves actual BC-250 bases | Compiled table and reference exist | Retained branch predicate routes Skillfish2 through discovery | Failed-boot branch and values | A boot-attributed discovery array would test numeric agreement; agreement would not make the legacy initializer the producer |
| An address/access-state difference contributes to failure | Possible runtime state is not preserved completely | No direct contradiction; missing markers are not evidence against or for it | Actual failed-boot address and operation reached | Prefer existing boot-attributed logs; absent those, report unknown rather than repeat hangs |

## Best discriminating next work

Search retained discovery records for the actual VCN instance/base array and establish which boot produced each record. Matching values would support numerical agreement for that captured boot only. A mismatch would invalidate transferring legacy arithmetic to that record; neither outcome alone proves CP06/07's cause. Do not rerun the unchanged hanging trials.

Evidence: audit.py, results.json, branch-evidence.json. Public excerpts are source-only and contain no raw machine logs.
