# R276 — live artifact and recovery preflight

R276 prepares the *conditions* for a later R274-B live boot. It does not install a module, create an initramfs, modify /boot, or reboot.

## Why this stage exists

R274-B and R275 close source/build/provenance, but a live module test changes the kernel/module boot path. Before that, the recovery path must be fixed from current local evidence rather than assumed from historical state.

## Read-only goals

Collect:

1. current running kernel;
2. retained 7.2.3 kernel files and SHA256;
3. retained R180 initramfs files and SHA256;
4. loader/BLS entries referring to 7.2.3 / R180;
5. current /boot filesystem free space;
6. exact R274-B module SHA256 and vermagic;
7. retained signing/package inputs if present;
8. current source baseline hashes.

## Safety boundary

R276 preflight must not:

- use sudo;
- write under /boot or /usr/lib/modules;
- run depmod/dracut;
- sign or strip the module;
- load/unload amdgpu;
- modify bootloader configuration;
- access VCN MMIO/SMN;
- reboot.

## Pass condition

Enough current evidence must exist to define a new one-shot entry while leaving at least one independently verified existing recovery entry untouched.

If the historical R180 artifact or kernel identity is missing or changed, live packaging pauses until recovery is re-established.
