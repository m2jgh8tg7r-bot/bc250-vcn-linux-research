# R301 — bounded static review of new community intelligence

Date: 2026-10-03 JST. This is a supplemental external-intelligence review, not a replacement canonical handoff or a new live result. The user supplied the Discord claims through ChatGPT. Their original posts, firmware revisions and analysis artifacts were not supplied; attribution is preserved without treating the claims as facts.

The user authorized saved-file static analysis with a 100-minute ceiling and GitHub sharing after completion or after one hour of analysis. Work was interrupted and resumed; this bounded review finished before the ceiling. No sudo, hardware access, firmware execution, boot changes or live-test instructions were required.

## Existing live anchor remains unchanged

The user-provided canonical anchor is VCN LOAD_IP_FW with ucode_id 57, command 6, fw_type 13, payload length 405696, payload equality confirmed, response 0xffff0008 and zero placement. Same-boot non-VCN controls succeeded. This remains LIVE_CONFIRMED selective rejection. Saved-image authentication-path attribution remains STRONG_INFERENCE with respect to that live response; no new runtime identity evidence was acquired.

## What was independently rechecked

**STATIC_CONFIRMED metadata:** five saved ROM inputs contain ten top-level candidate key-store occurrences but only two distinct key-store bodies. The inputs have four distinct full-ROM hashes, which does not make them four independent firmware implementations. The retained VCN payload signer ID remains absent from both examined key-store types. The retained non-VCN control signer has a matching record in type51 and none in type50. These are record-membership observations, not cryptographic authentication, live database selection or proof of a private key.

**STATIC_CONFIRMED provenance:** 6,618 saved TOS instruction records and 22,755 saved type28 instruction records were checked against the retained image bytes, along with 253/977 literals and 363 type28 data entries. Altered-image and altered-instruction-record negative controls were rejected for both images. This establishes byte consistency of existing analysis records, not independent decoding, complete control-flow coverage or running-image identity. TOS was checked as a body; type28 as a complete container. An initial audit mistakenly used the type28 body for a container-hash contract and was corrected before the final PASS; that tooling error has no hardware implication.

**STATIC_CONFIRMED host-source distinction:** the pinned baseline non-DPG VCN start path orders firmware-window programming before VCPU reset release, then readiness checking, then RBC/ring programming. The retained R152 experimental working file has intentional Cyan guards in hw_init, mc_resume and start before the normal bodies. Thus absent host bring-up in that retained source is an experimental quarantine decision, not a newly discovered universal BC-250 defect. No claim is made that this source file identifies every later experiment's binary or the exact module from an external board.

## Community claims and disposition

| Attributed claim | Current classification | Boundary |
| --- | --- | --- |
| dan2wik/Rukkus: type checking, key-ID lookup and usage checking may be separable | UNPROVEN for their reported implementation | Preserve separate mechanisms; matching an ID does not establish permitted usage or valid signature |
| FJ60fan: a startup-derived PSP-local flag changes usage enforcement | UNPROVEN | Independent reproduction of bypass-enabling conditions was not performed; saved metadata does not establish this behavior |
| Rukkus: named firmware functions implement a validated type13 reset/power-release sequence | UNPROVEN for the exact external function interpretation | Existing saved type28 material is compatible with a type13-specific post-validation reset-related path, but external image/version identity and the claimed full sequence are not established |
| Rukkus: all five ERR_DETECT-related values are zero | UNPROVEN for this board | Host-source absence of detector programming cannot prove zero hardware state; names and header definitions alone cannot establish values |
| Rukkus: normal fetch-window/reset setup is missing | STATIC_CONFIRMED only for intentional guards in the retained local experimental source; otherwise UNPROVEN | Upstream architecture and deliberately omitted experimental operations must be distinguished from board capability and same-boot state |
| FJ60fan: the root key has been found | UNPROVEN / ambiguous | A key-store record or public key does not establish corresponding private signing-key possession |
| Rukkus: interposer availability limits some investigators | UNPROVEN contextual report | No execution recommendation follows |

The usage-gate claim remains the principal unverified external lead. This review does not locate, reproduce or publish authentication-bypass switches, patch targets, injection procedures or firmware modifications. It therefore must not be described as a completed reproduction of FJ60fan's claim.

No supplied community claim directly contradicts selective live PSP rejection. The fetch/reset discussion describes possible downstream blockers and does not replace that rejection. The narrower source result qualifies a broad reading of “BC-250 lacks host programming”: it can accurately describe a particular experimental code path without proving a silicon limitation.

## Priority after this review

1. Obtain or compare already-saved, version-attributed evidence for the running authentication/service image and selected key store. The saved signer contrast is useful but does not identify the live database.
2. Compare external normal authentication and bring-up descriptions with version-pinned material, keeping key-ID membership, usage authorization, signature verification, placement and execution separate. No bypass investigation is proposed.
3. Treat reset/fetch and detector-state claims as downstream questions requiring source/version attribution; no new MMIO or fault-witness experiment is ready from this review.
4. Keep R299 input rejection lower priority. R300's supplied exact-match result demonstrates that the token can be read in that diagnostic boot, not why the earlier boot rejected it.

This bounded review is complete; the broader external hypotheses are not resolved. No automatic continuation, test or reboot was launched.

## Evidence

- [Saved-file and source audit results](../research/r301/audit-results.json)
- [Prior saved-image scope and runtime-identity limitations](CHATGPT_HANDOFF_R233.md)
- [Prior positive signer controls](CHATGPT_HANDOFF_R235.md)
- [Fixed external baseline and evidence distinctions](CHATGPT_HANDOFF_R266.md)

STAGE=R301 supplemental external-intelligence static review
RESULT=Bounded metadata/provenance/source review complete; external usage-gate reproduction not performed
STATIC_OR_LIVE=STATIC_CONFIRMED for enumerated rechecks; LIVE_CONFIRMED refers to prior user-provided anchor only
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=No new hardware observation
PROVEN=Saved metadata identities, bounded instruction-byte consistency, baseline source order, deliberate local source guards
REJECTED=Public key means private key; downstream fetch issue replaces live PSP rejection; quarantine proves silicon incapability
UNPROVEN=External usage flag, exact external reset-function semantics, detector values, running image/KDB identity and live rejection cause
NEXT=Version-attributed saved evidence comparison; no live-test instructions
