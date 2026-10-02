# R297 CP04 privileged preflight PASS

Date: 2026-10-02 JST

Status: PASS

Key identities:
- CP04 image: 888676eab4a586250f2fce213eb1deaeea569e70f64c1722b1b9b17af2733f35
- CP04 signed module: 2b154c25d7de1bef4fcdc127edf10df3b6388897760cc0da55b52242fae2bdf9
- CP04 package script: 59e0de6199e77aa1c4a5fcc2c668259aeea8b7881be01d61595d8ddecee14668
- CP04 package log: 7d9cb07a98e188ebcd315bb9f6ecc62b571873a9925ce3b6cfce35b9ad23e171
- CP04 BLS candidate: 0efd19c1a7d784a6b4399aa146e25cf6062bd45c0a1ab3bda46b5dd9697bde53

Recovery:
- installed CP03 image/BLS exact
- CP03 HOME recovery exact
- CP03 BLS snapshot exact

Protected state:
- research kernel exact
- R180 image/BLS exact
- grub.cfg exact
- OSTree entries exact
- boot_success=1
- no next_entry
- runtime efi_pstore pstore_disable=Y

Capacity:
- free now: 67764224
- reclaimable from CP03: 257089424
- free after CP03 retirement: 324853648
- CP04 image: 257087825
- CP04 + BLS + 50 MiB margin required: 309517205
- CP03 retirement required for space: YES

Final:
R297_CP04_PRIVILEGED_PREFLIGHT=PASS
CP04_PREFLIGHT_V3_EXIT_CODE=0

No boot write, install, selection change, module load, hardware access, or reboot occurred.
