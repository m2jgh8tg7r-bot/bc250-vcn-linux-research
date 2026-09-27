# R247 experimental contract

Question: does the excess CPU cost seen during input-paced FFmpeg decoding depend on rawvideo output packing, and is the no-decode pacing path itself similarly expensive? This is a pipeline contrast, not an additive causal decomposition.

## Matrix

Two existing1080p High-profile8-bit420 one-slice H264 streams are reused: R244 I/P (GOP32) and R246 maximum3 B pictures (GOP48). Each complete96-frame stream is concatenated ten times to960 frames, nominal32seconds at30fps. SPS/PPS/IDR boundaries are retained. Hashes are verified against the saved source fixtures. Content repetition is explicit; these are not32seconds of unique scenes. GOP and reference structures differ, so an I/P-to-B difference is not attributed solely to B pictures.

For each input, compare compressed stream copy to null muxer, native H264 decode to wrapped_avframe/null muxer, and native H264 decode to rawvideo `/dev/null`. Decoder and output thread requests are1. Three rates are tested: unrestricted, readrate1, readrate2. No extra filter, display, audio, GPU or hardware decoder is used. Six unrestricted warm-ups (every input/mode pair) are excluded, then three seeded shuffled rounds cover18 configurations:54 measured processes. The result comprises34,560 decoded frames and17,280 copied compressed-picture units; copy-mode completions are not called decoded pictures.

## Timing

Measure each serial subprocess with monotonic wall time and before/after child-resource counters. Save user/system CPU seconds separately, voluntary/involuntary context switches and minor/major page faults. Busy-core equivalents = child CPU seconds / wall seconds. Per-frame cost = child CPU seconds /960. The supervisor and correctness hashing are outside child CPU time; process startup/teardown are included, container launch is excluded.

Both source clips have verified short-output reconstruction from earlier stages. This matrix checks completion counts and whole-pipeline resource use; it does not independently hash every960-frame timed output. The B-picture stage R248 separately validates concatenated output order and bytes.

Raw stream metadata display and nominal readrate are not accepted as actual timing: every process must report960 completions, and measured paced fps must lie within10% of the nominal30/60 target. Report exact measured rates and ranges, not that tolerance as a precision claim. FFmpeg's default initial burst and catch-up behavior remain enabled and are source-audited. No measured trials are trimmed.

## Isolation and limits

Rootless Podman: no network, no GPU device, read-only root, dropped capabilities, no-new-privileges,2GiB memory ceiling,128 PID limit, no CPU quota. Host FFmpeg binary/libraries are mounted read-only through the matching dynamic loader. Current container image, CPU affinity, cgroup limits/counters, executable hash and a governor observation are recorded. No clock-policy, firmware, driver or boot changes occur. Q36 finishes before timing; R248 starts after R247 finishes. Unrelated background desktop activity and clock frequency are not controlled.

Output modes differ in allocation, copying, scheduling and downstream handling. Subtraction cannot isolate pure decoding or a specific scheduler/memory cause. These measurements cannot establish display deadlines, audio synchronization, energy consumption, game impact or dedicated VCN execution. A low CPU load is not proof of hardware video acceleration.

Reproduction: use prepare_fixtures.py with the retained R244/R246 media and result manifests, then launch.py, then summarize.py. The local container tag is an environment identifier, not a public image distribution. Raw videos, raw process logs, binary files and downloaded source files are retained locally; public records contain selected scripts, measurements, hashes and source links.
