# R235 — positive signer controls narrow the saved KDB comparison

Date: 2026-09-27. LATEST_STAGE=R235. This is saved-file analysis, with historical live observations explicitly separated from new static comparisons.

R233 found that the previously tested VCN signer was absent from saved KDB candidates. R235 adds positive controls: eight retained non-VCN main-image files share a different signer, which matches a usage-10 record in directory-type51 and has no match in directory-type50. On the specific criterion of signer-ID membership, type51 matches these retained files and type50 does not. This does **not** identify the live selected KDB or prove the live VCN rejection cause.

## Historical response controls revalidated

The existing R180 offline verifier was rerun on the R180 and R182 captures. Each capture passes its 14-file content manifest and saved module/boot attribution checks. Each contains 11 paired requests with the same ID/type/size/status/placement pattern across the two boots:

| Group | Requests per capture | Historical response |
| --- | ---: | --- |
| CE, PFP, ME, MEC1, MEC2 main images | 5 | Status zero, nonzero placement, completed transport |
| SDMA0, SDMA1, RLC | 3 | Status zero, zero placement, completed transport |
| MEC1/MEC2 jump-table subpayloads | 2 | Status zero, zero placement; excluded from signer-header comparison |
| VCN | 1 | `0xffff0008`, zero placement |

Only the five nonzero-placement entries meet the existing parser's full control-acceptance predicate. All eight main-image files must not be described as independently proven accepted. Two boots repeat an observation; they are not two independent firmware implementations. R235 performed no new PSP load or firmware execution.

## Saved metadata comparison

- Eight retained control files have signer ID `30b8865125424499aeff3ac35ce621a6`. Each matches the type51 record with usage 10 in every inspected saved image, and none matches type50.
- Those eight filenames contain seven distinct decompressed file hashes: MEC1/MEC2 reuse identical file bytes. They are not eight independent signer observations.
- The retained VCN file has signer ID `c37290c310e64a62b027c56695492368`, absent from both types.
- The R173 and R180 retained compressed control files are byte-identical. Every control's ID/type/length agrees with the selected historical request. MEC main-image length excludes its 896-byte jump-table suffix according to the saved driver; the jump-table entries are not parsed as standalone signer headers.
- The ten KDB occurrences across five saved images have **only two distinct body hashes**, one per directory type. Thus KDB body hashes do not distinguish the inspected P3/Robin editions. The signer comparison adds a positive contrast, not ten independent negative observations.

These facts are PROVEN_STATICALLY for retained metadata. The connection from retained control files to the exact historical PSP-visible bytes remains UNPROVEN: source-address agreement and size/type agreement are weaker than a byte comparison. Key-ID agreement alone is not signature verification, appropriate-use enforcement, selection of that database, or firmware execution. A runtime database containing both the control signer and the VCN signer is not excluded by this evidence.

## Checksum limitation discovered during validation

For all eight control files, zlib CRC32 over the entire declared payload differs from the common header's CRC field. This discrepancy is recorded, not silently treated as a pass. VCN's whole-payload CRC matches. Control-file SHA-256 hashes, declared bounds and equality across two retained package trees are verified, but the control checksum coverage/origin is unresolved. Neither corruption nor cryptographic validity follows from these observations alone.

The first audit attempt incorrectly required the VCN CRC convention for all controls and stopped. The corrected audit reports that test independently; it does not claim the controls passed it. The saved generic Linux `amdgpu_ucode_validate` checks file length, not CRC, so a driver file-load success cannot resolve the discrepancy. This statement concerns that host helper, not PSP authentication. Three malformed-header/VCN-payload controls are rejected by the audit.

## What changes next

The strongest safe next provenance task is the origin/format of the retained control-file checksum discrepancy and any already-saved, version-matched evidence of KDB staging. Type51 should be investigated before repeating an undifferentiated search of ten duplicate KDB occurrences. It is not safe to turn the present comparison into a claim that type50 can never be selected.

No new VCN live test is ready. Repeating the old VCN-only load response cannot distinguish a signer miss from other candidate origins of the same status. The next saved-artifact/source steps do not require sudo or PSP/MMIO access.

## Local Q36 assistance

The user authorized Q36 as a local assistant. It was given only the bounded evidence argument for an adversarial wording review, with no research-tree mount and no network. Its output is advisory and cannot change an evidence class without deterministic support. The review uses Vulkan GPU compute, which is hardware access for inference; it is not a VCN/PSP experiment. A first invocation failed because its working directory prevented a shader asset from being found; this is a runtime configuration failure, not a hardware failure. The corrected attempt and disposition are recorded separately.

## Evidence

- [Metadata comparison and sanitized historical pairs](../research/r235/results.json)
- [Local audit script](../research/r235/audit_controls.py), reusing the retained R180 parser rather than inventing a new live-log interpretation
- [Source/provenance supplement](../research/r235/source-provenance.json)
- [Q36 review disposition](../research/r235/q36-review.md)
- [R234 interface audit](CHATGPT_HANDOFF_R234.md) and [R233 baseline](CHATGPT_HANDOFF_R233.md)

Raw journals, machine identifiers and firmware binaries remain local. Public outputs use anonymous capture labels and file hashes. The metadata comparison is reproducible with the retained research tree and captures; those private inputs are not distributed by this publication.

```text
STAGE=R235
RESULT=COMPLETED_STATIC_CONTROL_COMPARISON
STATIC_OR_LIVE=PROVEN_STATICALLY for metadata; PROVEN_LIVE refers only to revalidated historical capture observations
HARDWARE_ACCESS=GPU_COMPUTE for authorized local Q36 review; no VCN/PSP/MMIO observation
HARDWARE_MUTATION=NO research device/configuration mutation; ordinary inference submission only
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=retained control signer matches type51, VCN signer absent, two distinct saved KDB bodies, two old capture manifests verified
REJECTED=ten independent KDBs; all eight controls meet nonzero-placement acceptance; type51 is proven live
UNPROVEN=control checksum origin, exact PSP-visible control bytes, selected runtime KDB, VCN rejection cause and execution
NEXT=retained package provenance/checksum format and already-saved KDB staging evidence
```
