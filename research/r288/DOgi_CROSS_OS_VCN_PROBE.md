# R288 — D_Ogi cross-OS VCN PSP probe design

Date: 2026-10-01

## External baseline

D-Ogi/amdgpu-wddm E10 has a BC-250 Windows PSP implementation that has already proven on hardware:

- GART enabled before PSP load.
- PSP GPCOM ring creation succeeds.
- SETUP_TMR succeeds.
- Ten normal Cyan Skillfish firmware LOAD_IP_FW commands succeed with status 0.
- The implementation imports AMD psp_v11_0_8 ring functions and psp_gfx_if.h.
- Its generic loader accepts an arbitrary psp_gfx_fw_type, aligned MC source address and byte size.
- The imported enum already defines GFX_FW_TYPE_VCN = 13.

The current E10 firmware list mirrors the normal Linux Cyan Skillfish PSP list:
SDMA0, SDMA1, CE, PFP, ME, MEC1, MEC1 JT, MEC2, MEC2 JT, RLC.
VCN is not currently included.

Therefore D-Ogi does not already prove VCN on Windows, but their existing PSP/TMR/GART path is a strong independent positive-control environment for one VCN type-13 request.

## Local proven VCN request identity

Our Linux live/static work has established:

- VCN file: vcn_2_0_3.bin
- file size: 405952 bytes
- source offset: 256 bytes
- payload size: 405696 bytes
- PSP fw_type: 13
- Linux PSP result in R173/R180: status 0xffff0008, placement 0
- R285 direct host provisioning: the same 405696-byte payload copied from source offset 256 to driver VCN BO offset 0 with equal=1.

## Proposed discriminating experiment

Do not port a Windows VCN driver.

Instead add a narrow E10-derived operation that:

1. establishes the already-proven E10 GART + PSP ring + TMR baseline;
2. requires all known-good control LOAD_IP_FW commands to have succeeded first;
3. stages only the VCN payload (file offset 256, length 405696) at a page-aligned staging MC address;
4. submits exactly one generic GFX_CMD_ID_LOAD_IP_FW with fw_type GFX_FW_TYPE_VCN (13);
5. records fence completion, resp.status and resp.fw_addr/placement;
6. performs no VCN MMIO, power, reset, clock or ring programming.

A PLAN-only/host-model check should precede any hardware run.

## Interpretation matrix

Windows status 0xffff0008 + addr 0:
- strongly supports the blocker being independent of Linux amdgpu and reproducible in a second OS/driver;
- increases confidence in a VCN-specific PSP authentication/policy/signing issue.

Windows status 0 with placement:
- strongly indicates that some prerequisite/state differs between the Windows E10 environment and our Linux VCN request;
- compare TMR/GART/source placement/ring state and exact command payload before any VCN MMIO work.

Different nonzero error:
- compare exact request bytes and firmware payload identity first; do not infer the failing PSP layer from the code alone.

No fence / hang:
- does not diagnose authentication; treat as transport/state failure and stop.

## Safety boundary

The first cross-OS experiment should stop at the PSP response. It must not:
- touch VCN/UVD MMIO;
- send undocumented SMU messages;
- ungate VCN;
- release VCPU reset;
- run VCN ring tests.

This keeps the experiment comparable to R180 and avoids mixing PSP acceptance with the power/start problem.

## Immediate local next check

Verify that the retained local vcn_2_0_3.bin common header reports exactly:
- file 405952
- ucode/source offset 256
- ucode size 405696

and determine whether D-Ogi's current common-header parser can accept the file without a VCN-specific parser.
