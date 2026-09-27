# R247 — input-pacing CPU cost controls

STAGE=R247
RESULT=PASS:18 configurations /54 timed processes
STATIC_OR_LIVE=PROVEN_LIVE CPU pipeline measurements; PROVEN_STATICALLY sleep/source checks
HARDWARE_ACCESS=ordinary CPU; separate authorized Q36 GPU review before timing
HARDWARE_MUTATION=no boot options, reboot, firmware, driver or clock-policy changes
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=all54 processes complete960 picture units; paced rates observed near30/60fps; higher CPU cost persists without rawvideo serialization
REJECTED=rawvideo packing as the sole explanation for higher paced cost; treating default pacing as exact whole-run frame rate; intentional busy-spin interpretation of the inspected sleep helper
UNPROVEN=complete causal attribution; display/audio deadlines; game impact; energy use; dedicated VCN
NEXT=B-picture throughput R248; counter-report agreement check; full-player baseline remains a future task

## What changed in our understanding

R245 found more CPU consumption under input-paced decoding than a simple unpaced CPU/frame estimate predicted. R247 repeats that comparison with longer32-second nominal inputs and three output modes, on I/P and I/P/B clips. The full54-process matrix includes34,560 decoded frames and17,280 copied compressed-picture units; it does not count streamcopy as decoding.

For1080p I/P input near30fps, measured median busy-core equivalents are:

| Pipeline | Busy-core equivalents |
|---|---:|
| Compressed stream copy to null muxer |0.0091|
| Software decode to wrapped_avframe/null muxer |0.3047|
| Software decode to rawvideo `/dev/null` |0.3291|

The decoded/null path still uses2.04 times the unpaced-derived30fps estimate. On the B-picture input that ratio is1.98. Therefore, rawvideo packing is not the sole source of the paced/unpaced discrepancy. The no-decode paced path is low-cost in absolute terms. These are whole-pipeline observations; subtracting them is not a precise isolated decoder-cost measurement.

At near60fps, I/P decoded/null consumes0.4767 busy-core equivalents and rawvideo output0.5150. B-picture decoded/null consumes0.4630 and rawvideo0.4798. B/I/P clips also differ in GOP and reference structure; these figures do not isolate a B-picture effect. None includes display or audio.

## Source and runtime corroboration

The matching upstream release source shows rawvideo plane packing versus AVFrame wrapping/null output, timestamp-based pacing, a default0.5-second initial burst, and catch-up behavior. A local disassembly of the actual libavutil file corroborates that av_usleep calls nanosleep. The runtime library hash matches the prior R245 dependency manifest. This rules out describing that inspected helper as an intentional busy-spin implementation, but does not isolate scheduler, clock, cache or other reasons for the increased decoding CPU cost.

Measured paced rates are approximately30.3–30.4 and60.2–60.6fps across the aggregate rows, not exactly the nominal target. The initial-burst/default pacing rules and process boundaries matter; no display-deadline claim follows from them.

## Evidence and limits

See [full results](TABLE.md), [machine-readable summary](summary.json), [measurement contract](METHOD.md), and [source/runtime audit](SOURCE_AUDIT.md). All three trials per configuration are retained, with six separate unpaced warm-ups excluded. Both source inputs are known-correct fixtures repeated ten times; this is explicit content repetition, not32seconds of diverse footage.

No hardware-video device is exposed to the container. No boot-option or system-policy change is needed. Q36's bounded review repeated concerns and ended incompletely; no new conclusion was adopted from it. Its run ended before timing. Boot-option/reboot-style tests remain unprepared; the user's requirement to be told before such work is preserved.

An additional counter cross-check completed960 frames: wrapper9.391561 CPU seconds versus FFmpeg9.213 seconds, with different documented lifetime boundaries. The preset0.25-second tolerance passed. This one validation run is separate from the54-run matrix. See counter-cross-check.json and SOURCE_AUDIT.md.
