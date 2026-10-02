# R297 CP01 install-no-select PASS

Date: 2026-10-02

Status: PASS

The R297 CP01 boot artifact was installed without changing boot selection.

Preconditions:
- safe running kernel: 7.2.1-ogc4.1.fc44.x86_64
- R297 image SHA-256: 53915d3ab095c6824634e65cf574e569f8dec0782ae3846f9c57f94ef205533d
- R297 BLS SHA-256: d05ce199ceadb76c62097a34f445ccbb37192f941a1372197739906cfd165b46
- R291 recovery material exact
- installed R291 precheck exact
- R180 / normal Bazzite / research kernel protected identities exact
- no pending next_entry

Actions:
- retired only the R291 image and three R291 BLS entries
- installed R297 image atomically
- installed R297 BLS atomically
- did not change grub selection
- did not load the module or reboot

Installed R297:
- /boot/initramfs-7.2.3-r297-cp01.img
  SHA-256: 53915d3ab095c6824634e65cf574e569f8dec0782ae3846f9c57f94ef205533d
- /boot/loader/entries/boot-entry-r297-cp01.conf
  SHA-256: d05ce199ceadb76c62097a34f445ccbb37192f941a1372197739906cfd165b46

Protected state after installation:
- grub.cfg unchanged
- grubenv unchanged
- ostree-1.conf unchanged
- ostree-2.conf unchanged
- R180 BLS unchanged
- R180 recovery image unchanged
- research kernel unchanged
- boot_success=1
- no pending next_entry

R291 retired state:
- boot-entry-r291-debug.conf absent
- boot-entry-r291-pre-reset.conf absent
- boot-entry-r291-pstore.conf absent
- initramfs-7.2.3-r291-pre-reset.img absent

No module load, VCN register access, reset release, FILTER write, PowerUpVcn, boot selection change, or reboot occurred.

Install log SHA-256:
8281a6019faa101b1e75a28f8e62b245fc6681766d1b61a068f8e670ccb43a45

Next:
perform a read-only installed-final audit by extracting the exact amdgpu module and VCN firmware from the installed R297 initramfs and verifying hashes, signature metadata, markers, recovery state, and boot policy. Only after that should a one-shot CP01 boot be armed.
