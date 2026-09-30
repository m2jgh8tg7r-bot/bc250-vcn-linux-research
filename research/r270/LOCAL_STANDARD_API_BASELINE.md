# R270 local standard API evidence

This file records only sanitized derived observations from the user's 2026-10-01 ordinary Bazzite boot. It intentionally excludes usernames, boot IDs, host identifiers and raw machine-specific addresses that are not needed for replay.

## DRM query

Source: `research/r267/query.c`

Source SHA-256:

```text
fcefedae17f358b4b762fc8faa732e1c3461a737bf8cc9c91e11ed45a78ab961
```

Result:

```json
{"query":"ACCEL_WORKING","ret":0,"errno":0,"value":1}
{"query":"HW_IP_INFO","type":"GFX","ret":0,"errno":0,"major":10,"minor":0,"available_rings":1,"ip_discovery_version":655619}
{"query":"HW_IP_INFO","type":"VCN_DEC","ret":0,"errno":0,"major":0,"minor":0,"available_rings":0,"ip_discovery_version":0}
{"query":"HW_IP_INFO","type":"VCN_ENC","ret":0,"errno":0,"major":0,"minor":0,"available_rings":0,"ip_discovery_version":0}
{"query":"HW_IP_INFO","type":"JPEG","ret":0,"errno":0,"major":0,"minor":0,"available_rings":0,"ip_discovery_version":0}
{"query":"VIDEO_CAPS","type":"DECODE","ret":-1,"errno":22}
{"query":"VIDEO_CAPS","type":"ENCODE","ret":-1,"errno":22}
```

Process exit: 0.

## Captured detected IP blocks

The ordinary boot identified Cyan Skillfish and reported the following detected IP-block sequence:

```text
0 common_v1_0_0 / nv_common
1 gmc_v10_0_0 / gmc_v10_0
2 ih_v5_0_0 / navi10_ih
3 psp_v11_0_8 / psp
4 smu_v11_0_0 / smu
5 dce_v1_0_0 / dm
6 gfx_v10_0_0 / gfx_v10_0
7 sdma_v5_0_0 / sdma_v5_0
```

No VCN/UVD/JPEG block appears in the captured detected-IP-block list.

## Interpretation boundary

Allowed:

- ordinary amdgpu acceleration and GFX exposure are functioning in this capture;
- standard VCN DEC/ENC/JPEG exposure is absent in this capture;
- standard video-capability queries reject with EINVAL;
- PSP is enumerated in the ordinary boot.

Not allowed:

- VCN silicon absent;
- VCN physically fused off;
- VCN unclocked;
- VCPU cannot fetch;
- firmware can never be accepted;
- external GPCNT/RBC/reset-release reports have been reproduced locally.

Those remain separate questions.
