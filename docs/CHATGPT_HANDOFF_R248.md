# R248 — input-pacing cost and B-picture CPU performance

2026-09-27, approximately30-minute continuation from R246. The user requested advance notice if boot-option/reboot-style hardware validation is ready. No such test is prepared or performed. No boot options, firmware, driver or clock policy were changed. Dedicated VCN operation remains unproven.

The user also requested that time-limited long research be explained after completion, without Japanese progress explanations during processing; preserve that preference for future sessions.

## Findings

**The increased CPU cost under input pacing is not solely rawvideo packing.** R247 compares compressed copy/null, software decode/wrapped_avframe/null and software decode/rawvideo-to-null on I/P and B-picture inputs, with unrestricted/nominal30/60fps ingestion. All54 trials complete:34,560 decoded frames and17,280 copied compressed-picture units. For1080p I/P near30fps, the three median loads are0.0091,0.3047 and0.3291 busy-core equivalents. Even the decoded/null path is2.04 times its unpaced30fps extrapolation; the corresponding B-picture ratio is1.98. These whole-pipeline contrasts are not an additive causal decomposition.

**Timing interpretation is better supported.** Official FFmpeg8.1.2 source confirms rawvideo packing, frame wrapping, timestamp pacing and default initial-burst behavior. The actual runtime av_usleep helper calls nanosleep. An extra accounting check gives9.391561 wrapper CPU seconds versus9.213 FFmpeg-reported CPU seconds, within the preset0.25-second tolerance; the source shows FFmpeg's internal timer starts after input/output setup. Clock, cache and scheduling contributions remain unseparated. Input pacing does not establish presentation deadlines.

**FFmpeg remains the stronger tested CPU baseline with B pictures.** R248 runs24 configurations,24 excluded warm-ups and72 measured processes /27,648 frames. Across12 matched settings FFmpeg is faster and lower-cost, with median speed ratios2.55–6.67. For all four inputs, FFmpeg decoder setting1 also beats all tested custom settings in both throughput and CPU/frame.1080p one-slice: custom61.4 versus FFmpeg174.9fps at setting1;100.1 versus505.6 at setting4. Requested settings are not equal total OS thread counts.

**Output correctness is preserved.** All24 original B-picture output checks and12 longer384-frame checks match reference bytes and ordering. No new harness or decoder-core modification was needed. Custom8 workers do not universally improve performance over4. These remain synthetic, repeated, progressive8-bit420 clips rather than a broad media/player test.

## Evidence and scope

- [R247 pipeline controls](../research/r247/STATUS.md), [measurement method](../research/r247/METHOD.md), [source/runtime audit](../research/r247/SOURCE_AUDIT.md), [results](../research/r247/TABLE.md).
- [R248 B-picture throughput](../research/r248/STATUS.md), [measurement method](../research/r248/METHOD.md), [results](../research/r248/TABLE.md), [comparisons](../research/r248/comparison.json).
- Q36 ran one bounded advisory review before measurements. Its response repeated concerns and ended incompletely; no new conclusion was adopted. No Q36 inference overlaps timed CPU trials.

No VAAPI integration, VCN initialization/ring execution, complete-player smoothness, audio synchronization, game impact or energy saving is established. No upstream message/issue/PR was sent. Selected scripts, measurements, hashes and source links are public; videos, binaries, raw logs and downloaded source remain local.

Next: a representative full-player CPU baseline with frame-deadline/audio observations, kept separate from supported-firmware/identity research for dedicated VCN. Notify the user before continuing if boot-option/reboot-style validation becomes ready. No such boot test is prepared by this checkpoint.
