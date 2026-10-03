# R314 — Sequence-aware capture and offline analysis

STAGE=R314
RESULT=PROVEN_STATICALLY: eight synthetic parser tests pass
STATIC_OR_LIVE=Offline software validation only
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Reassembly, duplicate handling, conflict detection and interior gap reporting on synthetic fixtures
REJECTED=Sequence continuity proves a complete suffix or VCPU execution
UNPROVEN=Live receiver compatibility, loaded netconsole extended-mode behavior, R312 panic cause
NEXT=Review receiver workflow and verify retained netconsole artifact before proposing a boot change

## Artifacts

- capture.py: Python standard-library UDP receiver, explicit local bind and expected sender required, exclusive creation of a private output file. Saves original datagram bytes as base64 and wall/monotonic arrival timestamps. Displays escaped byte representations; never sends confirmation or controls a boot. Not launched during R314.
- analyze.py: offline JSONL reader for the documented basic extended header (without release prefix). Reassembles ncfrag by byte offset, detects conflicting overlaps/metadata, deduplicates identical datagrams and reports missing sequence ranges between received anchors. Malformed records are reported. A record is capped at 1 MiB. This is not a hostile-input service or a full kernel log validator.
- test_analyze.py: eight synthetic cases covering reordered data, duplicates, gaps, reordered fragments, missing fragments, conflicting overlaps, sequence reuse, mixed sessions, malformed headers/oversize extents, and consistent overlaps.

## Receiver workflow (prepared, not a request to boot)

Stop the previous listener before binding the same port. Run capture.py on the receiver with --bind, --sender and --output filled locally. The output must be a new private file for exactly one boot. A bound socket is not sender qualification: the existing manual gate still requires the operator to observe the current boot's qualification-complete message. Stop capture after that boot; do not append subsequent boots.

Analyze the resulting private file with `python analyze.py CAPTURE.jsonl`. Basic legacy netconsole lines are rejected, not silently treated as extended records. R312 still uses basic format; no existing entry/image was modified. Explicit extended-mode selection is a future separate boot-package change.

Raw payloads and decoded reports can contain private identifiers. Do not publish either automatically; publish only reviewed, sanitized findings. Sender-address filtering is not authentication. No firewall or network setting is changed by these scripts. Receiver output is line-flushed but not fsync-durable; host failure can still lose buffered data. Live throughput, OS UDP buffer behavior and Windows console behavior are untested.

## Inference limits

Interior gaps identify absent sequence numbers in the supplied capture, subject to header validity and one-boot isolation. They do not locate loss at sender/network/receiver, prove execution of a missing marker, or count an entirely missing suffix. Prefix/suffix completeness always remains UNKNOWN. Session UUIDs identify capture processes, not kernel boots: a user can still accidentally mix boots in one process. Incompatible sequence reuse is flagged, but not every mixed-boot capture can be detected.

Supporting evidence for useful observability: retained netconsole documentation describes sequence and ncfrag metadata; synthetic reconstruction passes.
Contradicting evidence: none established for parser cases; live feasibility is untested.
Unknown: the R312 reset mechanism and missing terminal records remain unchanged.
Next discriminating observation: received named R311 panic versus a different panic; a missing suffix remains inconclusive. No repeated VCN MMIO trial is justified by this work.
