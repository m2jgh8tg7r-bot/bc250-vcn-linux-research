# R244 — saved firmware provenance, identity limits and CPU video control

Session: 2026-09-27, 19:04:52–20:24:52 JST (80-minute research window). R233 had already been completed; this session continues the R235 baseline through R244.

The new results narrow several evidence gaps, but **dedicated VCN operation and running PSP service/KDB identity remain unproven**. No PSP/VCN transaction, firmware installation, kernel change or reboot occurred. Q36 used authorized GPU compute for advisory reviews; video experiments used isolated CPU-only containers with no GPU device.

## Main findings

- **Official provenance (R236):** eight retained control files match official linux-firmware SHA-256, Git blob ID and size at two newer pinned revisions. Five graphics files differ from their initial 2021 versions, consistently with their 2022 update. The outer CRC discrepancy is present in the officially distributed bytes, not evidence by itself of local copying corruption. 24 file/ref comparisons and four malformed-metadata controls were checked.
- **Internal integrity (R237):** ten control container occurrences—including the two MEC jump tables—have matching body SHA-256 and exact bounded layouts. They represent eight distinct containers in seven distinct files. Five malformed-input controls are rejected. This is not public-key signature verification; the outer CRC convention remains unresolved.
- **Historical VCN candidates (R240):** all 21 retained, distinct 2019–2026 VCN payloads share the same signer metadata value, absent from the saved KDB candidates. Older versions in this particular set therefore do not provide signer-field diversity. This is not 21 live failures, a complete worldwide firmware survey, or proof that saved KDBs are active.
- **Identity and response interpretation (R238/R239):** platform CCP exposes register-backed bootloader/TEE versions, while TEE_IOC_VERSION returns implementation/capability constants. None establishes GPU service1/KDB byte identity. Ten historical controls have status 0; five also return a nonzero address. That five-control subset is a conservative observation filter, not a universal firmware acceptance ABI.
- **Current source support (R241/R242):** official Linux commit `fd179f8a05be3ccae366b9b96e176b51fbe54aab` still skips VCN2.0.3 registration and omits it from the codec query. The inspected community VA-API implementation uses CPU and Vulkan compute routes; GPU surface transfer does not establish VCN decoding. Its HEVC encoder does exist, contrary to an erroneous Q36 conclusion that was rejected.

## A useful CPU-only control and a harness correction

R244 built the pinned public H264 standalone harness and compared ordinary generated I/P clips against FFmpeg 8.1.2 software decoding. The original GOP12 matrix passed 18/18 clips. GOP32 initially failed ordered comparison in 18/18, but **every frame was pixel-identical to a reference frame**; only the sequence was permuted after a 16-frame number wrap.

The standalone harness's type2 picture-order calculation omits the wrap offset. An isolated diagnostic change to that harness alone made both matrices pass: **36/36 clips, 3456 frames**. The decoder core and original source were unchanged. The initial failures remain recorded. This is not a production-complete patch or a full conformance suite: B/non-reference pictures, MMCO5, field coding, gaps and changing parameter sets were not validated.

This establishes CPU reconstruction for the tested set without a GPU device. It does not establish VA-API integration, VCN execution, or a defect in the production VA-API decoder path. The VA path receives picture-order metadata from its caller, unlike the standalone parser.

## Evidence index

|Stage|Evidence|
|---|---|
|R236|[Official metadata and verification](../research/r236/STATUS.md)|
|R237|[Control container checksums](../research/r237/STATUS.md)|
|R238|[Platform identity interfaces](../research/r238/STATUS.md)|
|R239|[Response evidence contract](../research/r239/STATUS.md)|
|R240|[21-version signer metadata](../research/r240/STATUS.md)|
|R241|[Community implementation routes](../research/r241/STATUS.md)|
|R242|[Current upstream contract](../research/r242/STATUS.md)|
|R243|[Ten-claim evidence ledger](../research/r243/ledger.json)|
|R244|[CPU experiment, controls and limits](../research/r244/STATUS.md)|

Q36 reviews were advisory. One tool-enabled review drifted out of scope; another made false HEVC/GPU-only assertions. Those conclusions were discarded. Bounded wording suggestions were accepted only where consistent with source and measured results. Raw model output is not a primary source.

Next priority: target-specific supported firmware/identity evidence that discriminates the still-unmeasured running-image boundary. The historical signer result supplies no new reason for blind old-version trials. CPU workaround validation and dedicated VCN research remain separate tracks. No new live VCN experiment is prepared by this session.

Public artifacts contain selected scripts, sanitized metadata, hashes, source links and the explicitly scoped CPU harness diff. Firmware binaries, generated video/raw frames, executable binaries, unsanitized logs and personal machine identifiers are excluded.
