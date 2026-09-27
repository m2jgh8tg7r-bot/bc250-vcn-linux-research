# R233 — saved-image provenance and rejection-path checkpoint

Date: 2026-09-27. LATEST_STAGE=R233. Status: completed static checkpoint.

R233 consolidates the September 23 models, September 25 Q36-assisted reviews, and September 26 recovery notes. Completion means the bounded findings have been revalidated and their limits recorded; it does not mean VCN enablement or runtime attribution has been solved. The previous public baseline was R232 at `f4a7fec5b40f8ba9a3022ea1c5653af8544f18e1`.

## Findings and limits

- **PROVEN_STATICALLY:** all 14 existing CPU text-model suites pass again (8,191 cases), covering 2,061 distinct modeled instruction positions. Image/record consistency checks cover 6,618 TOS and 22,755 type28 instruction records. Four altered-image/record controls reject; nine interpreter guard controls and 252 arithmetic cases pass. These checks do not independently validate instruction decoding, signatures, or runtime execution.
- **PROVEN_STATICALLY:** metadata re-audit of five saved images and ten candidate KDBs finds no matching signer for the previously tested host VCN payload. The five inputs include two identical P3 captures; they are not five independent firmware implementations.
- **CONSISTENT_WITH:** with explicit backing and initialization assumptions, the saved candidate's no-matching-signer path returns `0xffff0008` and zero modeled placement. This occurs before later signature validation. It is a possible explanation for the historical response, not its proven cause.
- **PROVEN_STATICALLY:** in the saved Linux source, Cyan Skillfish2 with PSP 11.0.8 selects a function table containing five ring callbacks. `init_microcode` and bootloader KDB/SOS/sysdrv callbacks are absent; the microcode wrapper returns zero when its callback is absent. The same selection branch sets `autoload_supported=false`. Relevant excerpts match the source checkout's HEAD even where other portions of the files have local edits. This closes the ordinary function-table-mediated Linux loader hypothesis for that source version; it does not prove BIOS origin or exclude every alternative path.
- **UNPROVEN:** running TOS/service1/type28 identity, selected runtime KDB, the actual origin of the historical response, physical VCN power/isolation, firmware acceptance, VCPU execution, hardware rings, and VCN decode/encode.

## Error meanings remain conditional

| Saved candidate condition | Modeled result |
| --- | --- |
| No software backing | `0x80000203` |
| Failed initialization followed by a load request | `0xffff0007` |
| No matching signer | `0xffff0008` |
| Matching signer, wrong usage | `0x80000205` |
| Reserved usage | `0x80000206` |

These are path-specific results, not universal definitions of PSP status codes. Host command 6 maps to request 1007 in this model, not request 1002. Host `fw_type=13` and a BIOS directory type with the same number are separate namespaces.

## Incorporating the newer local work

The September 25 notes correctly separate host VCN staging-buffer equality from PSP service-image identity. They also distinguish saved loader virtual addresses from host-readable physical addresses and make placement branch-dependent. A saved type28 match cannot establish which branch the September 14 machine used. P3/Robin1/Robin3 share the candidate body, while Robin5 has a different outer body; model conclusions are not automatically transferable between them. The nested header is within an outer signed extent; an unsigned nested flag does not establish a signature bypass.

The September 26 notes leave management-field provenance, indirect aliases and allocator bounds unresolved. Their finite searches do not establish global absence, and service-slot count does not by itself bound allocation count. These later investigations are retained as unresolved source notes, not promoted into new verified producer or runtime claims. No new corruption-trigger or bypass investigation was performed for this closeout.

Q36 output was used as existing review material. Deterministic checks above are the evidence authority; no new Q36 session was needed.

## External progress checked September 27

The [community guide's September 26 update](https://github.com/katzzero/bc250-unofficial-community-guide/commit/ee8df9405daf50abd046530eab0dfcad232253c0) is newer than the initial handoff. Its PSP lead does not supply a version-matched standard-PSP acceptance trace. The [Shalasere research head](https://github.com/Shalasere/bc250-vcn-research/commit/edb222c65477b6ebc63834ef3562855009179539) remains September 20 and [daveconde's head](https://github.com/daveconde/bc250-vcn-enable/commit/7c511b725b135766c52a3e13776c1cd187e5015d) remains August 24.

Primary project documentation confirms the alternative processing distinction: [simpmix at the checked commit](https://github.com/simpmix/bc250-encoding-decoding-fix/blob/7d9c38bdfdc469505eeb94864a203c0b4ffee12c/README.md) describes CPU decoding and CPU/compute encoding, including an x264 default for H.264. The [Shalasere stopgap](https://github.com/Shalasere/bc250-vulkan-encode-stopgap/blob/732dfb57dda4e08c4b31d95039e99dc232d0a809/README.md) uses compute/CPU resources. VA-API exposure is not evidence of VCN execution. Their permanent-fuse assertions are not adopted as proof about this board.

A bounded default-branch Linux history check found no commits since the R232 baseline in the six recorded PSP/VCN/CCP paths. This is not an exhaustive survey of all branches, mailing lists or private research. No reviewed update resolves runtime image/KDB identity. The external progress therefore changes the comparison notes, not the static/live classification.

## Next discriminator and readiness

The highest-value missing evidence is a version-matched, independently obtained identity record for the running service image and selected KDB in the same boot as the load response. A firmware filename, host payload equality, status alone, or successful return from an absent Linux callback cannot provide that identity.

Next work can first compare additional already-saved boot records and documented platform identity interfaces, then assess whether any supported read-only interface exposes the required identity. No such usable interface is established here. No new live experiment is ready; repeating the previous response-only tests would not distinguish the candidate causes. Sudo/root/live access is not expected for the next two to three document/source-review steps.

## Stage record

```text
STAGE=R233
RESULT=COMPLETED_STATIC_CHECKPOINT
STATIC_OR_LIVE=PROVEN_STATICALLY, with explicit model assumptions
HARDWARE_ACCESS=NONE during closeout
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=bounded model replay, byte provenance, saved key metadata, saved Linux callback contract
REJECTED=saved signer absence proves live cause; VA-API proves VCN; missing callback return zero proves firmware load
UNPROVEN=runtime image/KDB identity, field producer and global alias bounds, live rejection cause, VCN operation
NEXT=version-matched runtime identity evidence through documented read-only or already-saved records
```

## Evidence

- [Verification summary, case counts and local evidence hashes](../research/r233/verification-summary.json)
- [Saved Linux source excerpts and hashes](../research/r233/host-source-audit.json)
- [External repository commits and bounded search scope](../research/r233/external-review.json)
- [Previous R232 handoff](CHATGPT_HANDOFF_R232.md)

Original local firmware, logs, models and September 26 notes remain preserved. This publication contains a reviewed summary and selected verification records, not the entire working directory. Historical `R233 unfinished` notices describe the earlier recovery state and are superseded by this closeout.
