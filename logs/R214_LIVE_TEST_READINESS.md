# R214 live-test readiness — 2026-09-22

Status: UNPROVEN prerequisites; no live test executable prepared or run.

User scope: continue research; prepare and report a live validation if needed. Existing adopted constraints retain static analysis as the current mode. This assessment identifies what would make a test useful; it is not a request to perform a speculative operation.

| Required element | Current evidence | Missing element |
|---|---|---|
| Version-matched VCN-related path | Type 0x08 body and R201–R211 static paths fixed by hash | Loaded-image identity and physical meaning of the path |
| Preconditions | Historical normal recovery R199; no new live baseline in R214 | Baseline contemporaneous with a proposed experiment |
| Exact operation and transport | Saved image/directory fields known | A proven readable live identity/selection location; no assumed SRAM address |
| Discriminating observations | Type 0x12 is almost all zero; both version fields agree | An observable distinguishing executable-image identity or actual copy range, with a positive control |
| Recovery | Prior experiments have their own saved recovery procedures | Recovery applicable to the exact new transport, including selector restoration if relevant |
| More information than R197 | A new identity observable could narrow the static/runtime gap | Such an observable has not yet been established |

Candidate assessments:

- Version-only observation: insufficient. Both headers and both body prefixes carry 0x00580600. It is not an image hash.
- Repeating R197 firmware load: insufficient for image-selection/copy-range provenance; previous nonzero response and zero placement remain the baseline.
- Reading a supposed SRAM/selection register: not ready. Neither an exact proven path nor valid-value/positive-control contract is established; zero or all-ones alone would be ambiguous.
- Reading existing saved logs and comparing BIOS distribution bodies: completed offline; no reboot required.

Before preparing an executable live collector, establish the exact path from saved source/instructions, its read side effects, bounded access range, expected contrasting values and invalid-read control. If it requires B8/Q2, include stable original selector capture, necessary governor coordination, unconditional restoration, exact restoration verification and governor restoration. Do not reuse an old experiment's recovery claim for a different operation.

A future collector must separate transport success from meaningful data and loaded-image identity from VCN execution. This remains a preparation boundary, not a diagnosis of hardware failure.
