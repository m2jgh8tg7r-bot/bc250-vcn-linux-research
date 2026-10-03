# R324 — Final-pointer checkpoint preparation

Question: At the existing pre-MMIO helper checkpoint, does the selected instance-0 VCN base pointer match a bounded discovery record, and does that record contain segment 1?

The candidate walks only device-owned discovery heap memory. It checks allocation, binary/table/header bounds, die IDs, record extents and conservative monotonic die layout. It compares pointers without printing addresses, and reads native segment1 via memcpy only from a fully bounded matching record. Ambiguous/missing records or malformed layout produce an inconclusive marker. count0/1 produce segment1_absent. Earlier GPU initialization still accesses hardware.

The candidate preserves guards and an unconditional named panic before helper VCN MMIO. No VCN read, write, reset release, ring execution or power message is added. panic=0 and extended netconsole should be retained for any future package. A raw UDP receiver must be recording before the existing local input gate accepts GPU loading. Manual reset is required after the intended panic.

Interpretation: matching expected base supports this boot's final software address premise. An unexpected value or short record revises it. No-match, malformed layout or missing logs are inconclusive. Matching metadata does not prove device accessibility or explain historical CP06/07. It is not a license to repeat their unchanged reads.

Preparation gates: CPU boundary/mismatch/duplicate/wide-format tests; actual kernel object build; final linked checkpoint audit; paired rebuilt baseline and candidate comparison; signing and executable-section equality; image roundtrip and dependencies; installed-file/default-boot audits. Installation and a manual live trial are not performed by this preparation.

At this draft stage there is no completed boot package and no test-ready claim. The isolated copy rebuild may touch broad dependencies; historical module equivalence is not assumed.
