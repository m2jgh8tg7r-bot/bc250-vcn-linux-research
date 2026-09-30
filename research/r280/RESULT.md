# R280 — packaging recipe audit result

Date: 2026-10-01

R280 completed read-only and closed the historical packaging recipe sufficiently for a home-only R274-B live-artifact build.

## Current state confirmed

- /boot free: 324861952 bytes
- R141 /boot image absent
- R180 image and BLS entry present
- normal Bazzite entries present
- R274-B unstripped module SHA256:
  b1138dd396c0a0e31b3431b9da1a50ae1f564a0ef102864e63e4a75763576ef5
- R274-B vermagic:
  7.2.3+ SMP preempt mod_unload

## Historical R180 packaging recipe

Exact retained `pack.sh` SHA256:

```text
bf7b36082485379bf8f93834ca3d4ebdf4b091e75fc6325324da7f54c77c2615
```

Its module/image sequence was:

1. install the unstripped amdgpu module into the initramfs tree;
2. `strip --strip-debug`;
3. sign the stripped module using Linux `scripts/sign-file`, SHA-512, retained private key and X.509 certificate;
4. run `depmod -b ... -e -E Module.symvers 7.2.3+`;
5. require empty depmod log;
6. create a sorted newc cpio archive with root ownership;
7. compress with `gzip -1`.

R180 depmod log was empty and the historical signature verification recorded cryptographic validity.

## Exact retained signing inputs

```text
signing_key.pem
904b7b14a8fbd11de3f73e699ecfa3c1a95da3616915fe4ed490049f559a6f4c

signing_key.x509
6f425bc02a1f554b7169d61ad8f6d22ab691981829f7cb59a05e1201c1a4e92f

scripts/sign-file
36264b18a597d20c0235be6a233ba13be3428e7fc50f2a26287e11a97c83d62b
```

Firmware input:

```text
vcn_2_0_3.bin
a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5
```

All required packaging tools were available.

## Important correction: reuse pack logic, not historical install logic

The historical R180 `install.sh` and `prepare_live.sh` are now stale relative to the current /boot layout.

In particular, historical `install.sh` requires exact R141 and R157 boot entries/images to still be present. R279 intentionally retired the R141 /boot image and current BLS inventory contains only R180 plus normal Bazzite entries.

Therefore:

```text
R180 pack recipe semantics        REUSABLE
R180 install.sh                   DO_NOT_REUSE
R180 prepare_live.sh              DO_NOT_REUSE
```

A new install stage must be written against the current R279/R280 state and must preserve R180 plus Bazzite entries.

## Next

R281 is home-only:

- verify exact R274-B module and signing-input identities;
- clone the retained R180 initramfs tree into a new directory;
- replace only amdgpu.ko;
- strip and sign using the historical recipe;
- depmod and require no diagnostics;
- build sorted cpio + gzip image;
- verify the module and firmware bytes inside the archive;
- do not touch /boot;
- do not reboot.
