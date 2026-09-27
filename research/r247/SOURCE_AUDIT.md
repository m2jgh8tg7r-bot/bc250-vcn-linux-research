# FFmpeg pipeline and pacing interpretation

Primary source: official FFmpeg release tag `n8.1.2`, pinned commit `38b88335f99e76ed89ff3c93f877fdefce736c13`. Eight files were retrieved and SHA256-recorded in source-provenance.json. This identifies inspected upstream source, not a proof that the distribution executable is an unmodified build of that tree. Executable and runtime library identity are separately recorded.

## Output modes

- `copy_null`: the executed stream mapping confirms compressed-packet copy. Demuxing, probing and parsing still exist; this is not a zero-work baseline. It has no full video reconstruction/output frame packing stage.
- `decode_null`: stream mapping confirms native H264 to wrapped_avframe. The null muxer defaults to that wrapper and its write_packet returns without file output. The wrapper clones/references an AVFrame and packages frame metadata instead of calling the rawvideo plane-packing routine. This is not a claim of zero allocations or unconditional zero-copy: av_frame_ref explicitly copies data when the source lacks reference-counted buffers.
- `decode_raw`: stream mapping confirms native H264 to rawvideo. raw_encode obtains a packed image buffer and invokes av_image_copy_to_buffer; that helper copies active plane rows. Sending the resulting bytes to `/dev/null` avoids persistent file writes but does not remove the preceding packing/copying work.

References: [null muxer](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/libavformat/nullenc.c), [wrapper](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/libavcodec/wrapped_avframe.c#L42), [raw encoder](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/libavcodec/rawenc.c#L49), [image packing](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/libavutil/imgutils.c#L501), [frame references](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/libavutil/frame.c#L300).

These whole-pipeline contrasts do not yield an additive decomposition of decoder, scheduler and memory costs. They change work, buffering and scheduling together. No claim is made that subtracting copy_null gives a precise isolated decoder cost.

## Input pacing

ffmpeg_demux.c updates an estimated decoding timestamp using packet DTS when present, otherwise frame-rate or packet-duration information. readrate_sleep compares that stream time with elapsed wall time and sleeps when ahead. The inspected defaults include an initial0.5-second burst and a catch-up rate1.05 times the requested rate. No initial-burst or catch-up override is supplied by this experiment. This helps explain why average frame counts divided by entire short-process duration need not be exactly30 or60; it is not a measured attribution of every timing difference.

On a build with nanosleep support, av_usleep uses nanosleep. The inspected path is not an intentional CPU busy-spin loop, but this source fact alone does not isolate the cause of additional CPU seconds during paced decoding. Scheduling, clock behavior, memory/cache effects and pipeline overhead remain unseparated.

The raw H264 probe display includes25fps/60tbr while decoded output is30fps. That display is not used as the pacing acceptance criterion. Every completed process reports960 pictures; actual elapsed-time rates are checked directly for paced modes. The source's estimated timestamp path and the measured copy-mode pacing avoid treating missing container timestamps as automatic failure. This is input-ingestion timing, not presentation deadlines.

References: [timestamp estimation](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/fftools/ffmpeg_demux.c#L312), [readrate_sleep](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/fftools/ffmpeg_demux.c#L507), [defaults](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/fftools/ffmpeg_demux.c#L2142), [sleep implementation](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/libavutil/time.c#L84).

No boot-option changes, reboot, firmware operation, GPU video access or system policy change is required or performed. The `perf` executable is unavailable; no profiler installation or counter-based frequency attribution was attempted.

## Matching runtime sleep helper

The measured libavutil.so.60 SHA256 matches the R245 dependency manifest. Local disassembly of its exported av_usleep function contains a call to nanosleep, corroborating the source sleep implementation in the actual shared-library file. This is static binary evidence, not a runtime syscall trace or a measured explanation for the excess CPU cost. See binary-sleep-check.json; raw disassembly remains local.

## CPU-accounting cross-check

One additional960-frame I/P decoded/null readrate1 run reports9.391561 child CPU seconds in the wrapper versus9.213 seconds in FFmpeg internal benchmarking; wall times are31.653888 and31.473 seconds. The differences are0.178561 CPU seconds and0.180888 wall seconds. The predeclared0.25-second accounting tolerance passes. These are two views of OS process accounting, not independent hardware counters. Matching upstream fftools/ffmpeg.c starts its internal benchmark after option parsing and opening inputs/outputs, whereas the wrapper includes the complete child lifetime. The difference is consistent with those wider boundaries, not proof that every microsecond was attributed. The result confirms that the large paced CPU total is also present in FFmpeg reporting; it does not explain the paced/unpaced cost gap. [Benchmark boundaries](https://github.com/FFmpeg/FFmpeg/blob/38b88335f99e76ed89ff3c93f877fdefce736c13/fftools/ffmpeg.c#L1009).
