# R323/R324 — Bounded discovery reader and final-pointer checkpoint draft

STAGE=R323/R324
RESULT=Offline reader tested; software checkpoint candidate and paired modules built; final call audit remains open
STATIC_OR_LIVE=PROVEN_STATICALLY and CPU synthetic tests; no live trial
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Offline reader 12 tests; exact observer CPU harness 180 cases; isolated baseline/candidate module builds
REJECTED=Successful build alone means a live test is ready
UNPROVEN=Live final pointer, VCN execution, prior blackouts, complete module equivalence
NEXT=Review instrumented bounds branch and paired module changes, then signing/executable correspondence and package gates

R323 adds an explicit-format offline reader with bounded header/table/die/record traversal. It distinguishes original wide wire data from post-parser native-u32 entries, inventories duplicate VCN records and reports the last record per instance. It does not validate original checksums or attest the driver pointer. It is intended for well-formed supported discovery captures; syntactic last-record reporting does not replicate all driver validation and hardware-IP mappings.

R324 is a private next-test draft. At the existing helper checkpoint it walks device-owned discovery memory with allocation/table/record bounds, matches the selected VCN instance0 pointer without printing pointers, and reads segment1 only from a matching record whose count permits it. Missing/ambiguous/unsupported layouts are inconclusive. It preserves guards and a named unconditional panic before helper VCN MMIO. No register accessor or power operation was added. Earlier initialization still accesses hardware.

The exact observer was compiled in a CPU harness using structure definitions extracted from the retained kernel header. All 180 cases passed, including each prefix truncation, pointer mismatch, count0/1, same/cross-die duplicates, post-parser wide format, header v2 and 64-bit address arithmetic. Ordinary -Wall -Wextra -Werror compilation passed. Userspace UBSan linking was unavailable because the system runtime library is missing; no userspace sanitizer success is claimed.

An isolated reflink build-tree copy produced baseline and candidate amdgpu modules. Compilation rebuilt broad dependencies; equivalence to historical R318 is not presumed. Linked observer relocation review found _dev_emerg plus compiler __fentry__ and __ubsan_handle_out_of_bounds calls. The unexpected instrumentation invalidated the initial logging-only call allowlist; review is open, not PASS. This is a verification issue, not a hardware failure. No signing, boot image, installation or reboot was completed. Do not run this draft.

This checkpoint records the requested maximum-ten-minute session. No ongoing build or experiment is left running. Test readiness has not been reached. Further work must close the instrumentation review and paired-module comparison before packaging and validating a panic=0 extended-netconsole/manual-recovery image. The raw receiver must save datagrams by boot, and outcomes apply to that new boot only. No unchanged CP06/07 trial is proposed.
