# R246 — ordinary H264 B-picture CPU controls

STAGE=R246
RESULT=PASS:8 clips across3 worker settings,24 exact output matches
STATIC_OR_LIVE=PROVEN_LIVE CPU-only execution
HARDWARE_ACCESS=ordinary CPU processing in GPU-free containers
HARDWARE_MUTATION=no firmware, driver, kernel or clock changes
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=24 comparisons /2,304 decoded frames match FFmpeg reference bytes and SHA256
REJECTED=describing all B-picture inputs as still wholly untested after this stage
UNPROVEN=full H264 conformance; type2 non-reference/MMCO5 handling; field coding; VAAPI; VCN; B-picture performance
NEXT=complete-player CPU baseline and representative workload selection, separately from dedicated VCN research

## New coverage

Generate eight ordinary libx264 medium-preset High-profile progressive8-bit4:2:0 clips using testsrc2,96 frames at30fps, GOP48, no scene-cut insertion, ref3. Matrix:1280x720 /1920x1080,1 /4 slices, maximum2 /3 consecutive B pictures. FFprobe confirms each clip actually contains B pictures. The unique set contains16 I,292 P and460 B pictures (768 total).

Use the unchanged R244 diagnostic executable and its unchanged decoder core. Initial worker setting2 matches all eight FFmpeg8.1.2 software reference outputs, including presentation order and byte count. Replays at settings1 and8 also match:24 configurations and2,304 output frames. Matching raw output files were deleted after hashing; compressed inputs and logs remain local.

Header traces establish picture-order type0, six-bit POC LSB, four-bit frame number, progressive4:2:0/8-bit syntax, reference and non-reference NALs, and observed memory-management operations0/1. No MMCO5 is observed. These B-picture controls extend R244's prior I/P-only coverage; they do NOT validate its type2 wrap patch for every non-reference case or turn that diagnostic patch into a production-complete fix.

The standalone source header comment says decode order, but the executed source contains a POC-sorting drain. Claims here rely on exact FFmpeg output comparisons rather than that outdated comment. No additional harness or decoder changes were necessary.

This is a correctness stage under a2-CPU quota, not a B-picture performance benchmark. Q36 may overlap correctness-only work, never R245 timed performance measurements. No GPU device is exposed to the video containers; no VAAPI application or dedicated VCN path is tested.

Evidence: [primary matrix](results.json), [thread replays](thread-replay.json), [header fields](header-summary.json), [summary](summary.json). Generation and replay scripts are included. This is a small synthetic positive-control set, not a full conformance suite or evidence about arbitrary media.
