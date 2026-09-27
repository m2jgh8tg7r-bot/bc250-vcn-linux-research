# Diagnostic patch scope

The diff changes only the standalone test harness from simpmix/bc250-encoding-decoding-fix commit7d9c38bdfdc469505eeb94864a203c0b4ffee12c. It retains the upstream file's GPL-3.0-only license. It is a scoped CPU experiment, not a production-complete decoder patch. See STATUS.md for the untested picture-order cases.

Original source: https://github.com/simpmix/bc250-encoding-decoding-fix/blob/7d9c38bdfdc469505eeb94864a203c0b4ffee12c/approach1-compute-encoder/tools/h264dec.c

Saved-firmware scripts require the original retained research tree; firmware binaries are intentionally excluded. CPU harness scripts require a compiler-capable container image, the pinned public source and pinned Vulkan type-definition headers. No Vulkan runtime is linked to the CPU harness. Source and environment versions are recorded; the local image name is not a public image-distribution claim.
