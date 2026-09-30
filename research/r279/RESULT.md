# R279 — R141 single-artifact retirement result

Date: 2026-10-01

R279 completed successfully.

## Preconditions re-verified immediately before mutation

Retained local R141 image:

```text
path:
~/bc250-research/r141-swinit-diagnostic/initramfs-7.2.3-r141-diagnostic.img

size:
257089093

sha256:
58fee6e04140062043fbc077fe6d1c5bf3b6c7c1687fa9ca60fa4cad252b10c3
```

Installed /boot R141 image had the exact same size and SHA256.

No bootloader reference to `initramfs-7.2.3-r141-diagnostic.img` was found.

Before mutation, all of the following were present:

- /boot/initramfs-7.2.3-r180-observation.img
- /boot/loader/entries/boot-entry-r180-observation.conf
- /boot/loader.1/entries/boot-entry-r180-observation.conf
- Bazzite ostree-1 entry
- Bazzite ostree-2 entry

The R180 BLS entry still referenced:

```text
linux /vmlinuz-7.2.3-r138
initrd /initramfs-7.2.3-r180-observation.img
```

## Mutation

Only:

```text
/boot/initramfs-7.2.3-r141-diagnostic.img
```

was removed.

No reboot was performed.

## Postconditions

R141 /boot image:

```text
R141_BOOT_IMAGE_PRESENT=NO
```

Retained user-space copy remained byte-identical:

```text
58fee6e04140062043fbc077fe6d1c5bf3b6c7c1687fa9ca60fa4cad252b10c3
```

Recovery paths remained present:

```text
R180_RECOVERY_STILL_PRESENT=YES
BAZZITE_ENTRIES_STILL_PRESENT=YES
```

## Space

Before:

```text
67,772,416 bytes free
```

After:

```text
324,861,952 bytes free
```

Observed gain:

```text
257,089,536 bytes
```

## Result

```text
R279_R141_RETIREMENT=PASS
ONLY_R141_REMOVED=YES
RETAINED_LOCAL_COPY_VERIFIED=YES
R180_RECOVERY_PRESERVED=YES
BAZZITE_ENTRIES_PRESERVED=YES
NO_REBOOT_PERFORMED=YES
```

Log SHA256:

```text
afb1fb60726f66f0f03125598f0587681820e5a9dad0e5b689246be9e03506e6
```

R279 closes the /boot capacity blocker for one new ~257 MiB initramfs while retaining R180 and normal Bazzite recovery paths.
