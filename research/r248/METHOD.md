# R248 measurement contract

This stage extends the R245 CPU comparison to the existing R246 B-picture fixtures. It does not install a driver, change boot options or access a video GPU device.

## Inputs and variants

Four known-correct High-profile progressive8-bit420 libx264 clips cover720p/1080p and1/4 slices, maximum3 B pictures, GOP48,96 frames. Each complete elementary stream is repeated four times, including its IDR/SPS/PPS boundaries, to384 frames (12.8 seconds at nominal30fps). This adds duration, not unique visual content. Input hashes are checked against R246 before creating the longer file.

The custom executable is the unchanged R244 diagnostic standalone harness; its decoder core is unchanged from the pinned public source. Its type2 order patch does not establish general production correctness. These B inputs use POC type0. FFmpeg8.1.2 is explicitly forced to software H264 decoding. Both produce rawvideo to `/dev/null` for timing.

The custom worker settings1/4/8 are compared with FFmpeg decoder settings1/4/8; rawvideo output threads are fixed to1. The settings do not imply equal total thread counts or equal parallel algorithms. Custom setting1 disables its pool; settings>=2 create that many workers plus the caller.

## Environment and order

Reuse the R245 GPU-free rootless container recipe: network disabled, read-only root and input mounts, dropped capabilities, no-new-privileges,4GiB memory,128 PID limit, no CPU quota. Both programs inherit the same available logical CPU set. Record cpu.max, cgroup counters and executable hashes. Clocks/governor are not modified. Q36 and R247 timed trials finish before this matrix starts. Unrelated desktop load is not controlled.

Every one of the24 clip/engine/thread settings first matches its original96-frame saved FFmpeg raw-output hash and length. One excluded warm-up round then covers all24 long-input configurations. Three measured rounds shuffle their order with seed248:72 timed processes /27,648 frames. Each process must report384 completed pictures; all observations are kept.

Time includes executable startup, parsing, decoding, output packing/null writes and teardown. It excludes container launch, correctness hashing and the Python supervisor. User+system child CPU time is measured around each serial child; wall time uses a monotonic timer. Busy cores = CPU/wall. Any30/60fps estimates derived from CPU/frame are explicitly extrapolations; R245/R247 show that paced observations can differ.

After timing,12 extended-output checks (custom settings1/8 and FFmpeg1 for each clip) compare the complete384-frame output with four repetitions of the original96-frame reference. This validates ordering across repeated stream boundaries rather than only counting frames. Output hashes and measurements are distinct evidence.

## Limits

This is synthetic warm-cache throughput, not per-frame deadline validation, full media-player behavior, audio/video synchronization, energy efficiency, game concurrency or VCN execution. Reusing one clip per case gives no broad content distribution. Do not attribute differences from R245 exclusively to B pictures: GOP length, compressed bytes and reference structures also differ. No direct causal diagnosis of implementation speed differences is attempted. Report medians and observed ranges without significance claims from only three trials.

Reproduction requires the retained R244 binary/source and R246 fixtures; they are not distributed as public binaries or videos. Run launch.py --phase benchmark, then --phase verify_extended, then summarize.py. The local image tag is an environment identifier, not a public image URL.
