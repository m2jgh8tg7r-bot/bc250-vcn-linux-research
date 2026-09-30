# R279 — single-artifact retirement plan

R279 will be the first write-stage after the R274-B build/provenance work.

## Target

Preferred target:

```text
/boot/initramfs-7.2.3-r141-diagnostic.img
```

Expected SHA256:

```text
58fee6e04140062043fbc077fe6d1c5bf3b6c7c1687fa9ca60fa4cad252b10c3
```

Retained source copy:

```text
~/bc250-research/r141-swinit-diagnostic/initramfs-7.2.3-r141-diagnostic.img
```

## Required preconditions immediately before any write

1. /boot R141 still has the exact expected SHA256.
2. retained local R141 copy still has the same SHA256.
3. no bootloader reference to the R141 filename exists under the already-audited loader/grub/EFI locations.
4. R180 BLS entry still exists.
5. R180 /boot image still exists.
6. normal Bazzite entries still exist.
7. /boot free-space state is recorded.

## Intended mutation

Retire **only** the top-level R141 initramfs from /boot.

Do not:

- remove R157/R173/R180/R197;
- modify R180 entry;
- modify Bazzite entries;
- change default boot selection;
- reboot;
- build/install the R274-B live artifact in the same step.

## Postcondition

After the single retirement:

- re-read /boot free space;
- prove R180/Bazzite entries still present;
- prove R141 local retained copy still has expected SHA;
- record that the /boot R141 file is absent.

Only after R279 is independently closed should R280 construct a new R274-B initramfs in user space before any /boot installation.
