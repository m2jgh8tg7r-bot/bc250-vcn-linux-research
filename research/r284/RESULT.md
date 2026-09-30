# R284 — verified hardlink cleanup result

Date: 2026-10-01

R284 completed successfully.

## Precheck

Installed image and hidden temporary name were the same inode:

- image inode: 34
- hidden image inode: 34

Installed BLS entry and hidden temporary name were the same inode:

- entry inode: 35
- hidden entry inode: 35

Persistent artifact identities before cleanup:

- image SHA256:
  9765259d44bc1719c24318f3ac970fbbf74272b17e854aefb2b8380f12e7099c
- entry SHA256:
  aac0ab07bf31082de8250e90ebda635242ff1ee59e442c4671336c9b37525551

## Mutation

Removed only:

- /boot/.r282-image.t08aIiuT
- /boot/loader/entries/.r282-entry.wlYCa9tl

These were extra hardlink names left by the first R282 installer attempt.

## Postcheck

Persistent targets remained:

- /boot/initramfs-7.2.3-r281-r274b.img
  - inode 34
  - link count 1
  - size 257088089
- /boot/loader/entries/boot-entry-r282-r274b.conf
  - inode 35
  - link count 1
  - size 549

Recovery state remained intact:

- R180 recovery image present
- R180 BLS entry present
- Bazzite ostree-1 present
- Bazzite ostree-2 present

No boot selection and no reboot occurred.

## Result

R284_HARDLINK_CLEANUP=PASS
MAIN_IMAGE_PRESERVED=YES
MAIN_ENTRY_PRESERVED=YES
R180_RECOVERY_PRESERVED=YES
BAZZITE_ENTRIES_PRESERVED=YES
NO_BOOT_SELECTION=YES
NO_REBOOT=YES

Log SHA256:
561aa540d1c7cd536a42a206e60ad25b862697e93a19b2132e9288129a4259ac
