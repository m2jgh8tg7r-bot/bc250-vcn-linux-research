# R246 — CPU video practicality and B-picture controls

2026-09-27 continuation of R244, requested approximately20 minutes. Dedicated VCN operation remains unproven. No firmware, kernel, driver or clock-policy changes were made. CPU video tests used GPU-free rootless containers. Q36 was used for two bounded advisory reviews, outside timed CPU measurements; its numerical and interpretation errors were rejected.

## Results that matter

**FFmpeg software decoding is the stronger CPU performance baseline in the tested matrix.** R245 compares four synthetic720p/1080p High-profile I/P inputs,1/4 slices, four requested thread settings, both implementations. After32 warm-ups,160 shuffled trials complete61,440 frames. In all16 matched settings FFmpeg is faster and uses fewer CPU seconds/frame; median speed ratios2.40–5.63.1080p one-slice, setting1: custom69.3fps vs FFmpeg192.1fps; setting4:110.8 vs526.5fps. These are warm-cache full-process timings to null rawvideo output, not displayed-playback guarantees.

**More workers are not always better.** On720p four-slice input the custom setting8 is slower than4 (305.2 vs327.8fps) and costs more CPU per frame. At1080p four-slice the small speed difference has overlapping ranges. This does not establish a universally optimal setting.

**Unpaced CPU-load extrapolation understates the separate input-paced observation.** Twelve additional FFmpeg controls restrict input ingestion to nominal30/60fps and measure CPU time directly. All four conditions consume more busy-core equivalents than the unpaced estimate. The cause is not isolated. Use [paced measurements](../research/r245/paced-summary.json), not the unpaced estimate, when discussing this particular paced CPU workload; neither represents complete-player/display/audio/game/power behavior.

**B-picture correctness coverage is now positive for a bounded set.** R246 adds eight normal libx264 High-profile progressive8-bit420 clips at720p/1080p,1/4 slices, maximum2/3 B pictures, GOP48. They contain16 I,292 P and460 B pictures. The unchanged diagnostic decoder matches FFmpeg output bytes and order at worker settings1,2,8:24 matches /2,304 frames. Header traces show POC type0 and no MMCO5. This updates the earlier blanket absence of B-picture tests, but does not validate every H264 mode or every type2 ordering case.

## Evidence and interpretation

- [R245 throughput, CPU load and limits](../research/r245/STATUS.md), [method](../research/r245/METHOD.md), [full table](../research/r245/TABLE.md).
-32 original-output hash checks and12 long-output checks pass before performance interpretation. The long expected output is four repetitions of the saved original FFmpeg reference, not merely an equal frame count.
- [R246 B-picture controls](../research/r246/STATUS.md), including exact output hashes, syntax summaries and reproducible generation/replay scripts.
- [Q36 disposition](../research/r245/q36-disposition.json): both reviews gave some useful clarity suggestions, but incorrect load formulas, approximate ratios and a mistaken objection to the real-time limitation were rejected. Model output supplies no new primary evidence.

No VCN initialization, hardware video ring, VAAPI integration, complete-player smoothness, game concurrency or power improvement is established. No upstream issue/PR/message was sent. Generated media, executable binaries, raw logs and personal host data remain local; selected scripts, hashes, measurements and source links are public.

Next: use ordinary FFmpeg CPU decoding as the full-player baseline with representative media and frame-deadline/audio observations. Keep CPU workaround evaluation separate from supported-firmware/identity evidence for dedicated VCN. No new VCN hardware experiment is prepared by this stage.
