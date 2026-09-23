# R212 — Saved BIOS contains the complete analysis window

2026-09-21. Saved regular files only; no new hardware access.

The two saved P3 BIOS captures are byte-identical (16 MiB each). Each contains exactly one complete copy of the 262,400-byte Robin1 analysis file, at ROM offset `0x8ff100` through `0x93f200` (exclusive). The analysis SHA-256 is `8c29cf0b1c5ea713f1f8ae95ed4c1dc547d00c530530c131950cfd5eb08c6675`. Existing stage5 records also match the saved capture hashes. These are two captures from the same board, not independent boards.

The stored Robin1.00 and Robin3.00 distribution ZIP members contain the same complete analysis window at the same offset. This strengthens the version provenance used by R201–R211 beyond a matching 88.6.0 version word. It does not independently validate every interpretation of those bytes.

This proves ROM-contained analysis-window identity. The firmware loader's declared extent, complete running SRAM identity, runtime modifications, and the exact image used in external experiments remain unproven. The earlier stage5 candidate window is shorter than this full match and must not be treated as a loader-length determination. Physical VCN power, de-isolation, PSP acceptance/placement, VCPU, rings, and VA-API remain separate unproven boundaries.

[Sanitized evidence](../logs/R212_STATIC_EVIDENCE.txt) includes distribution archive hashes. [File-only comparator](../logs/R212_compare_saved_images.py) accepts analysis-image, saved-capture-A, saved-capture-B paths. It checks the fixed analysis hash and compares complete byte sequences without printing board ROM hashes or contents. No raw board ROM, NVRAM, or personal metadata is published.

Continue static analysis against this verified saved window. The six-condition gate for any future live proposal remains unmet. R197 is historical (booted, nonzero PSP response and zero placement); no reboot or hardware action is authorized by this result.
