# R288 result — D_Ogi parser compatibility

Date: 2026-10-01

The retained local VCN firmware file was checked directly.

File:
- path: /home/kazuyuki/bc250-research/r136-boot-artifact/vcn_2_0_3.bin
- SHA256: a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5
- actual file size: 405952

Common firmware header:
- size_bytes: 405952
- header_size_bytes: 32
- header_version: 1.0
- ip_version: 2.0
- ucode_version: 135364621
- ucode_size_bytes: 405696
- ucode_array_offset_bytes: 256
- crc32: 0xc52dcf97

Checks:
- file_size_matches_header=YES
- header_before_payload=YES
- payload_nonzero=YES
- payload_in_file=YES
- expected_file_size=YES
- expected_payload_offset=YES
- expected_payload_size=YES
- D_OGI_COMMON_PARSER_COMPAT=YES

Interpretation:

D-Ogi's current E10-style common-header parser logic is structurally sufficient for this VCN firmware. No VCN-specific container parser is required merely to locate the payload. The cross-OS PSP probe can therefore use:

- source offset 256
- payload size 405696
- fw_type GFX_FW_TYPE_VCN (13)

with the existing generic PSP LOAD_IP_FW path.

This does not prove that the Windows PSP will accept VCN type 13. It only proves that the local VCN firmware payload can be represented by D-Ogi's existing parser/model without changing the firmware container parsing model.

Local log SHA256:
d01df7995053286fcd2e8403825c2de5e688b31e91c4f452f6b20eb5967ea82f
