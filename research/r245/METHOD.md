# Measurement contract

The measured object is CPU-only process throughput, not dedicated VCN operation or full video playback.

## Inputs and implementations

Reuse the R244 diagnostic ordering variant, whose decoder core is unchanged from simpmix/bc250-encoding-decoding-fix commit `7d9c38bdfdc469505eeb94864a203c0b4ffee12c`. The custom executable was built with GCC 16.2.1, `-O2 -g -Wall -Wextra -std=gnu11`, without explicit native-ISA flags. Compare FFmpeg 8.1.2 software H264. Executable and resolved host library SHA256 values are recorded.

Four existing High-profile, progressive 8-bit 4:2:0 I/P clips cover 1280x720 / 1920x1080 and 1 / 4 slices, GOP32, 96 frames, generated testsrc2 at 30fps with x264 core165. Each complete elementary stream is concatenated four times, including sequence headers and IDR boundaries: 384 frames per timed process, nominally 12.8 seconds at 30fps. No claim of four times as much unique visual content is made. The original stream hashes are checked before concatenation.

## Isolation and scheduling

Both executables run inside the same rootless Podman container: no network, no `/dev/dri`, read-only root and source, writable output directory and temporary tmpfs, dropped capabilities, no-new-privileges, 4GiB memory ceiling, 128 PID limit. No CPU quota is set; `cpu.max` and cgroup throttling counters are saved. Both inherit the same allowed logical CPU set. The OS reports 16 logical CPUs for AMD BC-250; this is an OS topology observation, not a physical fuse assertion. The existing CPU governor is `performance`; clocks, thermal state and unrelated desktop workload are not controlled. Q36 inference ends before timing starts.

FFmpeg and its host `/usr/lib64` are mounted read-only and launched through the matching host dynamic loader. The explicit library search path includes the host Jack, PulseAudio and Samba subdirectories. Two preliminary loader failures were missing search paths, not decoder failures; no video was decoded in those failed probes.

Custom `BC250_H264_THREADS` settings are 1,2,4,8. Source `h264_threads.c` disables the worker pool below2; at higher values it creates that many pool workers in addition to the caller. FFmpeg `-threads` sets the decoder's requested parallelism; the rawvideo output encoder is fixed to one thread. These settings do not imply identical parallel algorithms or identical total OS thread counts.

## Timing and validation

Every decoder/clip/thread setting first reproduces the saved R244 reference YUV SHA256 and byte count for the original 96-frame clip (32 checks). Longer concatenated inputs are separately checked against four copies of the original reference output. Hashing and correctness output are outside timed performance trials.

One warm-up round covers all32 exact long-input configurations. Five measured rounds shuffle the configurations with fixed seed245. Preserve all160 measurements, with no outlier trimming. Each timed process consumes384 frames and writes rawvideo to `/dev/null`; candidate picture counts and FFmpeg progress counts must both report384. No container launch is timed. Executable process launch, input parsing, decoding, output preparation, null writes and process teardown ARE timed. Candidate internal slice/end-picture timing is retained separately and is not the headline comparison.

Wall time is `perf_counter` around the child process. CPU time is the serial before/after delta of `getrusage(RUSAGE_CHILDREN)` user+system time, including decoder worker threads. No unrelated child process overlaps this delta. The Python wrapper and correctness hashing are not included in child CPU time.

Throughput = frames / wall seconds. Average busy-core equivalents during the unpaced run = CPU seconds / wall seconds. Estimated demand at30fps = CPU seconds / frames *30, and likewise *60 at60fps. This is a compute-demand extrapolation, NOT a measured paced-playback load or percentage of all available cores. Median, minimum and maximum over all five trials are reported. Averages above30/60fps do not establish per-frame deadlines, audio synchronization, smooth playback, display integration, game concurrency or power consumption.

## Reproduction

Use `launch.py --phase benchmark`, then `launch.py --phase verify_extended`, then `summarize.py` with the retained R244 fixtures/source build. The local image tag identifies an existing runtime, not a public distribution. The public record intentionally excludes generated videos, raw YUV, executable binaries and unrelated host data.

## Separate input-paced control

`launch.py --phase paced_control` uses the same FFmpeg software path and1080p one-slice concatenated input, adding input `-readrate 1` or `2`. Settings1/4 each have three shuffled trials. These12 additional runs are not part of the160 unpaced measurements. Actual output fps and measured CPU/wall ratios are retained; nominal rate is not a proof of exact frame deadlines. No display or audio is involved. Differences from unpaced extrapolation are observed but not causally attributed.
