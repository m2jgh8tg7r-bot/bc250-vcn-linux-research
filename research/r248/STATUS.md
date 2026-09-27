# R248 — B-picture CPU throughput

STAGE=R248
RESULT=PASS:24 configurations /72 measured runs;24 original and12 extended exact-output checks
STATIC_OR_LIVE=PROVEN_LIVE CPU-only execution
HARDWARE_ACCESS=ordinary CPU processing; no video GPU device
HARDWARE_MUTATION=no boot options, reboot, firmware, driver or clock-policy changes
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=27,648 timed decoded frames; FFmpeg faster/lower CPU cost in all12 matched settings;4 cross-setting contrasts agree
REJECTED=assuming more custom workers always improve speed or efficiency; treating average throughput as frame-deadline proof
UNPROVEN=full-player smoothness; audio synchronization; power; game concurrency; dedicated VCN
NEXT=representative full-player CPU baseline; advance notice before any boot-option/reboot-style hardware test

## Main result

The unchanged R244 diagnostic custom decoder and FFmpeg8.1.2 software H264 were tested on four previously validated R246 B-picture clips:720p/1080p,1/4 slices, maximum3 B pictures, High-profile8-bit420, GOP48. Each96-frame input is repeated four times. Both programs output rawvideo to `/dev/null`, with explicit requested decoder settings1/4/8 and FFmpeg rawvideo output threads1.

Across all12 matched clip/thread settings, FFmpeg has higher median throughput and lower CPU seconds/frame. Speed ratios span2.55–6.67. More strongly, for every one of these four inputs, FFmpeg decoder setting1 is faster and uses fewer CPU seconds/frame than every tested custom setting. The setting number does not imply equal total OS threads or equal parallel algorithms.

For1080p one-slice input:

| Requested decoder setting | Custom median fps | FFmpeg median fps |
|---:|---:|---:|
|1|61.4|174.9|
|4|100.1|505.6|
|8|103.0|687.0|

Custom setting1 has little average throughput margin over60fps in this synthetic case; no actual60fps presentation guarantee follows. At720p four-slice input, setting4 reaches291.3fps (291.1–311.0) while8 reaches282.5fps (279.0–285.5) with higher CPU cost. At1080p four-slice input, medians131.6 and127.6 have overlapping observed ranges, so no strong statistical separation is claimed.

## Validation

Twenty-four original96-frame output comparisons match the saved FFmpeg YUV SHA256 and length. After timing, twelve384-frame output comparisons match four repetitions of the original reference (custom1/8 and FFmpeg1 for every clip). All24 warm-ups and72 measured runs report384 pictures, with no refused candidate slices. All three measured repetitions are retained; no outlier trimming. Correctness checks and hashing are outside the performance timer.

CPU video containers expose no GPU device or network and set no CPU quota. R247 and Q36 finish before R248 timing starts. The decoder core, harness binary, system drivers and boot state are unchanged. Executable process startup/output handling are included; container launch is excluded.

See [full table](TABLE.md), [summary](summary.json), [matched and cross-setting comparisons](comparison.json), [method](METHOD.md), and output-check records. R247 demonstrates why unpaced CPU/frame estimates must not be called measured playback load. These B clips also differ from R245 I/P clips in GOP/reference structure, so do not attribute a cross-stage difference exclusively to B pictures. Complete-player behavior, other formats and dedicated VCN remain unproven.
