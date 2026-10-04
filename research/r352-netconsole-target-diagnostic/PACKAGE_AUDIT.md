Offline artifact audit, 2026-10-05:

- Local image: `/var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic/initramfs-7.2.3-r352-netdiag.img`
- Corrected SHA-256: `10fbbb6eb15b2d3d9fec7e36d67a8ee2a099f3b927e519cbe10577004b9c55cf`
- Corrected size: 159,057,810 bytes
- Corrected newc archive SHA-256: `eb0ae2b7bfd894ca691a7041b1dec7a36548087042ade9ae5da988bda0a25c9b`
- R352 init SHA-256: `8f21b65fd15841bb8e2aa6a795ba54308d7121d276d83b322c1e38a759a62f96`
- BLS entry SHA-256: `05c27370357cc3a99f7e13fe17fe1e7b55d506f55203103f529526086adb08b5`
- Kernel config: `NETCONSOLE=m`, `NETCONSOLE_DYNAMIC=y`, `CONFIGFS_FS=y`, `DRM_AMDGPU=m`.
- The R352 module directory has no `amdgpu.ko`; the init script has no amdgpu load path.
- The first image was incorrectly assembled with the R351 `/init` despite the R352 standalone script. It was installed and selected once; receiver output correctly exposed the mismatch. That first image has no `amdgpu.ko`, and its R351 load gate was not confirmed by the submitted log. Never select that image again.
- The corrected archive has been inspected directly: its embedded `init` starts with the R352 diagnostic banner, and no `amdgpu.ko` path is present. It is not installed yet. `update-corrected-image.py` provides a separate read-only preflight followed by an explicit `--install`, backing up the current image before replacing it.
- No corrected-image installation or new hardware test has occurred.
