# R290-A result — isolated VCN probe architecture

Date: 2026-10-01

Source provenance matched the R289 pinned D-Ogi snapshot:
- psp_h SHA256 6d864ce2227308031625a01f40e31523ea042551ac9e490ca866eff7a4631389
- psp_c SHA256 3d6ecccffbf559cca6eb86e923268f5b1968b6f2e0983f877e935457feb25136
- kmd psp.c SHA256 81b8e30a551524aa356a183c8fd9bf3f1e7d930aabd4925fb7920547fe948ca1
- escape header SHA256 ef69e07fb04cd0c073c34c23320b1642315e4583c8f54ddbe28fb27a0a5c54da

Architecture checks:
- CURRENT_FW_COUNT_DRIVES_LAYOUT=YES
- COMMAND_COUNT_DERIVED_FROM_FW_COUNT=YES
- LOAD_EXECUTES_COMMAND_COUNT=YES
- LOADED_REQUIRES_ALL_COMMANDS=YES
- GENERIC_LOAD_IP_FW_EXISTS=YES
- VCN_NOT_IN_NORMAL_FW_ENUM=YES
- VCN_NOT_IN_NORMAL_FILE_ENUM=YES
- PSP_OP_PLAN/LOAD/UNLOAD all exist

Design consequence:
- ADDING_VCN_TO_BC250_FW_COUNT_WOULD_CHANGE_STANDARD_LOAD=YES
- KEEP_STANDARD_E10_BASELINE_UNCHANGED=YES
- ISOLATED_EXPLICIT_VCN_PROBE_PREFERRED=YES

Proposed probe contract:
- requires normal PSP loaded
- reuses existing PSP ring and TMR
- exactly one PSP LOAD_IP_FW submission
- fw_type 13
- VCN file size 405952
- payload offset 256
- payload size 405696
- staging offset 0x162000
- aligned allocation 0x64000
- staging end 0x1c6000 <= 0x200000

Safety contract:
- no VCN MMIO writes
- no VCN power changes
- no VCN clock changes
- no VCN reset changes
- no VCN ring init
- PSP-only design

R290_A_STATIC_ARCHITECTURE=PASS

Local log SHA256:
5bbf407dd3abc4bbd13e68bbf3717cfd719988180825bca16cd25b6690b2973c
