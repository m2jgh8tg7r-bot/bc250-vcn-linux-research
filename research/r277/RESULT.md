# R277 — /boot space inventory result

Date: 2026-10-01

## Current /boot usage

```text
total: 2,040,373,248 bytes
used:  1,848,451,072 bytes
free:     67,772,416 bytes
usage: 97%
```

Large top-level research initramfs files:

```text
257089361 /boot/initramfs-7.2.3-r157-psp-control.img
257089093 /boot/initramfs-7.2.3-r141-diagnostic.img
257087863 /boot/initramfs-7.2.3-r173-observation.img
257087698 /boot/initramfs-7.2.3-r180-observation.img
256958804 /boot/initramfs-7.2.3-r138.img
256087382 /boot/initramfs-7.2.3-r197-firmware.img
```

Current BLS entries visible under /boot/loader/entries reference:

- R180 research entry only;
- two normal Bazzite ostree entries.

The visible R180 entry references only:

```text
/vmlinuz-7.2.3-r138
/initramfs-7.2.3-r180-observation.img
```

The top-level R141, R157, R173, R138-initramfs and R197 images are not referenced by the currently visible BLS entries.

## Important limit

No deletion is justified yet.

A file can be absent from /boot/loader/entries but still be referenced by another loader directory, GRUB configuration, or retained recovery procedure. Also, most /boot research initramfs files are root-only, so current byte identity has not yet been re-proven against retained user-space copies.

## Local retained-copy evidence

Prior asset inventory records retained local initramfs copies for:

- r138-boot-repair/initramfs-7.2.3-r138.img
- r141-swinit-diagnostic/initramfs-7.2.3-r141-diagnostic.img
- r157-psp-observation-control/initramfs-7.2.3-r157-psp-control.img
- r173-request-observation/initramfs-7.2.3-r173-observation.img
- r180-load-response-observation/initramfs-7.2.3-r180-observation.img
- r197-firmware-response-comparison/initramfs-7.2.3-r197-firmware.img

R173 and R180 were previously directly proven to match their /boot copies. Current R277 only re-confirmed presence/size, not root-only hashes.

## Next

R278 performs a read-only root-assisted reference/hash audit.

Pass criteria for a retirement candidate:

1. exact /boot image exists;
2. exact retained user-space copy exists;
3. SHA256 of /boot image equals retained copy;
4. no current bootloader configuration references the image;
5. candidate is not R180;
6. no write/delete/move occurs during R278.

Only after one candidate satisfies all six should a separate, explicit retirement operation be designed.
