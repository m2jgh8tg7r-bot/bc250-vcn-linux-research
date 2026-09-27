# R244 — GPU-free CPU decode and a standalone harness ordering defect

A pinned public simpmix H264 **standalone CPU test harness** was built in a rootless, network-disabled container. No GPU device was exposed; the harness receives a NULL GPU context and would abort if it attempted the upload stub. The initial build lacked Vulkan type-definition headers; pinned Khronos headers were supplied in the research directory only. No system package, video driver, firmware or kernel was installed or modified.

We generated ordinary 8-bit progressive I/P H264 clips with FFmpeg8.1.2/libx264: 640x360,1280x720,1920x1080; Baseline/Main/High; one/four slices;96 frames per clip. Reference output is FFmpeg's software decoding of each **compressed clip**, not the pre-compression test pattern.

|Variant|Clips|Frames|Ordered byte-identical output|
|---|---:|---:|---:|
|Original harness, GOP32|18|1728|0/18|
|Original harness, GOP12 control|18|1728|18/18|
|Isolated ordering variant, both GOPs|36|3456|36/36|

The initial GOP32 mismatch was **not a pixel-reconstruction failure**: every complete frame matched a reference frame byte-for-byte, and every clip followed the same permutation (0,16,1,17,… within each32-frame GOP). All fixtures use picture-order-count type2 and MaxFrameNum16. The original harness computes type2 POC from frame_num alone, then sorts by POC. It omits the wrap offset, so different pictures acquire equal POC after frame_num wraps. GOP12 avoids that wrap before the next IDR and passes unchanged.

A separately copied CPU harness added frame-number wrap accounting; the decoder core and original source were unchanged. The variant passed both matrices against the already-recorded reference hashes. This is a diagnostic experiment, **not a production-complete fix**: B pictures, non-reference pictures, MMCO5, frame-number gaps, field coding and parameter changes are not validated here. The original failures are preserved and are not relabeled as passes.

The [H264 standard,8.2.1.3](https://www.itu.int/rec/dologin_pub.asp?id=T-REC-H.264-202408-I%21%21PDF-E&lang=e&type=items) and [FFmpeg's POC implementation](https://github.com/FFmpeg/FFmpeg/blob/n8.1.2/libavcodec/h264_parse.c#L287) corroborate the missing wrap term. This finding concerns the standalone harness. It does not establish a defect in the VA-API driver, whose caller supplies picture-order metadata through another path. It also does not refute or independently reproduce the project's separate conformance corpus.

The experiment positively demonstrates CPU frame reconstruction on this generated set without a GPU device. It demonstrates **no dedicated VCN execution**, no VA-API surface integration and no physical fuse state. Cgroup-limited execution timings are not performance benchmarks. No message or issue was sent to external maintainers.

Reproduction inputs and hashes: `summary.json`, the two original results files, `frame-order-analysis.json`, `all-fixture-header-summary.json`, `type2-wrap-variant/variant.json`, the explicit CPU-only patch, build/run scripts and environment versions. Public copies exclude generated video/raw frames, binary executables, personal paths and raw logs.

The public `frame-order-summary.json` condenses the locally retained full per-frame hashes in `frame-order-analysis.json`. Both CPU binaries link only libm and libc; the sandbox device/link check is recorded separately.

Final Q36 methods review: a tool-enabled pass was stopped after repeated context loss; a bounded text pass agreed with the counts but attempted one unavailable file read and made an inaccurate permutation paraphrase. Those parts were rejected. The result rests on the recorded hashes and source comparison, not AI agreement.
