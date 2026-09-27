# R245 — CPU decode throughput and resource cost

STAGE=R245
RESULT=PASS, scoped CPU throughput comparison
STATIC_OR_LIVE=PROVEN_LIVE CPU-only execution
HARDWARE_ACCESS=ordinary CPU processing; separate authorized Q36 GPU review
HARDWARE_MUTATION=no firmware, kernel, clock policy, or VCN changes
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=32 original-output checks and12 extended-output checks match;160 measured trials complete; FFmpeg faster and lower CPU/frame in all16 paired settings
REJECTED=R244 quota-limited timings as benchmarks; more workers always means faster or more efficient; throughput as smooth-playback proof
UNPROVEN=dedicated VCN; full playback deadlines; game concurrency; power; universal codec performance
NEXT=ordinary B-picture correctness controls, then real-player integration as a separate future task

## Findings

On the tested BC-250 environment, FFmpeg8.1.2 software H264 is faster and consumes fewer CPU seconds per frame than the pinned custom CPU harness for every matched clip/thread setting in this matrix. Median throughput ratios range2.40–5.63, but these are synthetic warm-cache I/P results, not a universal codec ranking. Requested thread settings also do not represent identical thread architectures.

For1080p, one-slice input, custom thread setting1 achieves69.3fps (68.6–69.4 across five runs); FFmpeg setting1 achieves192.1fps (190.9–193.2). At setting4 the respective medians are110.8 and526.5fps. These are full process timings including launch, parsing and rawvideo output preparation to `/dev/null`, with container launch excluded.

Estimated compute demand for30fps on that one-slice1080p input is0.431 core equivalents for custom setting1 versus0.181 for FFmpeg setting1. The estimate comes from measured CPU seconds per frame times30, not a percent of all16 available logical CPUs. It is not measured paced-playback load. At custom setting8 demand rises to0.703 equivalents while throughput reaches116.5fps: speed and CPU efficiency are different objectives.

For720p four-slice input, custom setting4 reaches327.8fps (319.5–333.8), while setting8 reaches305.2fps (303.1–307.5) and consumes more CPU per frame. For1080p four-slice input the corresponding medians140.9 and139.4fps have overlapping ranges; no strong separation claim is made there.

## Evidence and scope

- [Measurement contract](METHOD.md), [all32 aggregate rows](TABLE.md), [summary](summary.json).
- One warm-up plus five seeded shuffled rounds:32 warm-ups and160 measured runs,61,440 measured frames. No discarded measured trials. Both programs report384 pictures per run.
-32 original96-frame output comparisons match the saved R244 SHA256 and byte count. Twelve extended384-frame comparisons match the hash of four repeated reference sequences (custom settings1/8 and FFmpeg1 for all four clips):4,608 additional correctness frames.
- Both programs use the same GPU-free, network-free rootless container and allowed CPU set. `cpu.max=max 100000`; cgroup counters record zero throttled periods. Host FFmpeg libraries are read-only and hash-recorded. Governor remains `performance`; dynamic clocks and unrelated background desktop activity are uncontrolled.
- Original R244 diagnostic ordering variant and decoder core are unchanged. The timed matrix contains no B pictures. Output hashes and timing cannot prove VAAPI integration, VCN use, display deadlines, audio synchronization, game concurrency, energy consumption or broad H264 conformance.
- Q36 reviews are advisory and run outside timed measurements. Useful clarity suggestions were adopted; incorrect launch-boundary and CPU-conversion objections were rejected. See the disposition record.

Practical implication: the custom CPU path does not demonstrate a speed advantage over established FFmpeg software decoding in these conditions. A future complete-player test should include FFmpeg software decoding as its baseline. This result does not assess the project's compute encoder or any GPU-accelerated path.

## Input-paced follow-up

For the same1080p one-slice384-frame input, FFmpeg settings1/4 were each measured three times with input read rates1/2 (nominal30/60fps), null rawvideo output, no GPU, no Q36 overlap. Twelve trials /4,608 frames completed. Process launch is included; no separate paced warm-up is excluded. The clock governs input ingestion, not display presentation.

| FFmpeg thread setting | Nominal input fps | Observed output fps median | Measured busy-core equivalents | Unpaced estimate |
|---:|---:|---:|---:|---:|
| 1 | 30 | 30.8 | 0.335 | 0.181 |
| 1 | 60 | 60.6 | 0.523 | 0.363 |
| 4 | 30 | 30.8 | 0.351 | 0.198 |
| 4 | 60 | 60.5 | 0.600 | 0.397 |

Measured input-paced CPU demand exceeds the unpaced extrapolation in all four conditions. Its cause is unproven; pacing overhead, scheduling, cache and clock behavior have not been separated. Do not use the unpaced estimate as measured playback load. Neither test includes display/audio/game concurrency or energy measurement. See paced-control.json and paced-summary.json.
