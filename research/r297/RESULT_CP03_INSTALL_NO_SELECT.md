# R297 CP03 install-no-select PASS — 2026-10-02 JST

Status: PASS

The exact CP03 image/BLS pair was installed to /boot after retiring only the exact installed CP02 pair. Boot selection was not changed and no reboot/module load/hardware access occurred.

CP03 source identities:
- image SHA-256: eb71ca03672e0d9070a5d6ecb3193ec175be70137ab212a802989456a4d31854
- BLS SHA-256: 1819a92c492e7da53b84e361da51c247206192d0d449d35e158d54e9664b707b
- source identity: PASS

CP02 recovery:
- HOME recovery material: PASS
- installed CP02 precheck: PASS
- CP02 retired: YES
- final CP02 retired state: PASS

Space check before mutation:
- free now: 67,764,224 bytes
- CP02 reclaimable: 257,087,851 bytes
- estimated free after retirement: 324,852,075 bytes
- CP03 plus 50 MiB required: 309,517,645 bytes
- PASS

Installed CP03:
- image installed: YES
- BLS installed: YES
- installed contract: PASS

Protected boot policy:
- boot_success=1 before mutation
- protected precheck: PASS
- protected post-install boot policy unchanged: YES
- no pending next_entry before or after
- boot selection change: NO

Safety boundary:
- module load: NO
- hardware access: NO
- reset release: NO
- FILTER write: NO
- PowerUpVcn: NO
- reboot: NO

Final:
- R297_CP03_INSTALL_NO_SELECT=PASS
- CP03_INSTALL_SCRIPT_EXIT_CODE=0
- TERMINAL_SURVIVED=YES

The install log printed SHA-256 d2559f45d511ed30d9c826f176ce81532427c66d63692b04c98717303e3ecf4c from inside its tee-backed stream; treat that value as provenance-only rather than a stable post-run log identity.

Next: perform a read-only installed-final audit by verifying the installed CP03 image/BLS hashes, extracting the installed initramfs, and proving the embedded amdgpu module/VCN firmware identities, signature metadata, CP03 marker contract and panic reference. Do not set next_entry or reboot until that audit passes.
