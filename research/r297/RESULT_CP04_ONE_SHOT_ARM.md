# R297 CP04 one-shot arm PASS

Date: 2026-10-02 JST

Status: PASS

Pre-arm:
- safe Bazzite kernel
- installed CP04 identities exact
- installed-final-audit chain exact
- CP04 BLS contract PASS
- boot_success=1
- no pending next_entry
- runtime pstore_disable=Y

Arm result:
- next_entry=boot-entry-r297-cp04
- exactly one next_entry entry
- boot_success remained 1
- runtime pstore_disable remained Y
- no reboot performed by the arm stage

Final:
- R297_CP04_ONE_SHOT_ARM=PASS
- CP04_ONE_SHOT_ARM_EXIT_CODE=0
- TERMINAL_SURVIVED=YES

Stable artifacts:
- arm script: c417192a2591b60772d5ad2ebafb5e13f6e2ababeec6119c66f7cbdb26bda3ba
- arm log: 0ab7dfd5b2894d6de645062c43d965e8cbf43917fc3d374159deff4c68a2278a

Current grubenv:
- boot_success=1
- next_entry=boot-entry-r297-cp04
