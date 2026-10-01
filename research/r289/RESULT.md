# R289 result — D_Ogi VCN probe static audit

Date: 2026-10-01

Pinned upstream:
- D-Ogi/amdgpu-wddm
- commit bf4d102f41efce376a1a3f0d0503451f33d27dd7

## Proven static facts

- GFX_FW_TYPE_VCN = 13 exists in imported psp_gfx_if.h.
- Generic bc250_psp_load_ip_fw(ctx, type, mc_addr, size, resp) exists.
- Current E10 firmware inventory contains 10 images across 8 files.
- Current E10 integration does not include VCN.
- BC250_PSP_MAX_COMMANDS = 16.
- Current E10 command count = 11.
- With one VCN command = 12.
- COMMAND_CAPACITY_FITS=YES.

VCN firmware:
- SHA256 a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5
- file size 405952
- payload offset 256
- payload size 405696
- 4 KiB aligned payload allocation 409600 (0x64000)

E10 staging:
- capacity 0x200000
- current used 0x162000
- with VCN 0x1c6000
- remaining 0x3a000
- STAGING_CAPACITY_FITS=YES.

## Patch surface identified

Likely minimal integration surface:
- driver/shim/include/bc250_psp.h
- driver/shim/bc250_psp.c
- driver/kmd/psp.c

No change is required to the imported PSP protocol definition merely to represent VCN type 13.

## Result

R289_STATIC_AUDIT=PASS
VCN_HEADER_COMPAT=YES
PSP_GENERIC_TYPE13_AVAILABLE=YES
CURRENT_E10_VCN_INTEGRATION=NO
COMMAND_CAPACITY_FITS=YES
STAGING_CAPACITY_FITS=YES
NO_BUILD=YES
NO_HARDWARE_ACCESS=YES
NO_BOOT_CHANGE=YES
NO_REBOOT=YES

Local log SHA256:
708e45f2e9c1ebd9f26efa1ba24ded462121cb7fcccfe8bf839222eaccd6b3d7

## Interpretation

The pinned D-Ogi E10 PSP framework already has enough command capacity, staging space and generic PSP protocol support for one VCN type-13 probe. The next step can remain Linux-only and static/build-only: generate and audit a minimal patch without installing Windows or executing hardware commands.
