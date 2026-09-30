# R255 — cache configuration versus backing-image evidence

STAGE=R255
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=reference source and one retained firmware file
HARDWARE_ACCESS=none by audit; separate Q36 GPU_COMPUTE review
HARDWARE_MUTATION=none for research target
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=12 source witnesses and conditional saved-file memory geometry
REJECTED=cache register access establishes accepted firmware or instruction fetch; VCN13 equals MMSCH19
UNPROVEN=external firmware backing; physical fetch; connection to historical response
NEXT=complete helper-level clock/power contract and audit observation overclaims

The reference PSP branch configures cache window0 from `ucode[].tmr_mc_addr_lo/hi`, which are populated from PSP response address fields. The driver-loaded branch uses a separate buffer and firmware offset. Stack, context and shared-memory windows are distinct mappings. This source chain does not prove that a readable or writable cache register points at authenticated, resident, executable bytes.

For the retained 405952-byte file with 405696-byte payload, the reference cache-span formula `align(file_size+4)` and non-PSP allocation formula `align(payload_size+8)` both give409600 bytes with4096-byte GPU pages. This is a file-specific static calculation, not an assertion for arbitrary firmware. Stack/context sizes are131072/524288 bytes; window placement depends on the loading branch. No physical addresses are inferred or programmed.

Historical VCN placement0 is not evidence that a live cache BAR was programmed to0: R252 shows that the retained diagnostic source skips Cyan startup. Conversely, external cache-register access does not establish that the previously rejected payload was accepted. Both observations need same-boot attribution before connecting them.

The source enum distinguishes VCN firmware type13 decimal from MMSCH19 decimal. The inspected VCN2 MMSCH startup is reached through the SRIOV path; its existence does not justify changing the normal VCN request type or infer a missing BC250 boot operation.

`audit_cache.py` and `results.json` retain the source and saved-file hashes. No signature verification, firmware loading, reset release, or instruction fetch was performed.

Prior evidence: R143 already established the underlying power/return and saved-file geometry facts. This stage refreshes and connects them to the current pinned source and the new external-report question; it is not a first discovery of those facts.
