# R242 — upstream support contract refreshed

Official torvalds/linux HEAD was resolved to `fd179f8a05be3ccae366b9b96e176b51fbe54aab` (2026-09-26T18:14:35Z) and six source files were fetched as text. This refresh is current to this check, not a claim about later commits.

The VCN2.0.3 registration case still adds no VCN/JPEG block. `nv_query_video_codecs` still has cases2.0.0/2.0.2 but no2.0.3, with default `-EINVAL`. Both nv.c and amdgpu_kms.c are byte-for-byte identical to the earlier R193 upstream copies, so that old interpretation was independently refreshed rather than silently assumed current.

Cyan PSP11.0.8 still selects the five ring-only callbacks, with autoload_supported and boot_time_tmr false in that branch. Both Cyan GPU PCI variants remain marked AMD_IS_APU. These are software support/registration facts; no inference of permanent physical fusing, actual loaded TOS/KDB identity or VCN execution follows.

Evidence and permanent source links are in `results.json` and `source-manifest.json`. No kernel was built, installed or run; no research hardware was accessed.
