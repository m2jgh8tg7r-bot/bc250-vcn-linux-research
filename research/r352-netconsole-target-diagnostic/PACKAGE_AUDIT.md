Offline artifact audit, 2026-10-05:

- Local image: `/var/home/kazuyuki/bc250-research/research/r352-netconsole-target-diagnostic/initramfs-7.2.3-r352-netdiag.img`
- SHA-256: `d99c23db4d248f1e90aa190b8195749b5dad3aa58c5becee7e4dd6beb37773d9`
- Size: 159,058,834 bytes
- R352 init SHA-256: `8f21b65fd15841bb8e2aa6a795ba54308d7121d276d83b322c1e38a759a62f96`
- BLS entry SHA-256: `05c27370357cc3a99f7e13fe17fe1e7b55d506f55203103f529526086adb08b5`
- Kernel config: `NETCONSOLE=m`, `NETCONSOLE_DYNAMIC=y`, `CONFIGFS_FS=y`, `DRM_AMDGPU=m`.
- The R352 module directory has no `amdgpu.ko`; the init script has no amdgpu load path.
- Artifact is prepared but not installed. A guarded in-place replacement and exact R351 backup/rollback procedure remain to be prepared before asking the operator to run any privileged command.
