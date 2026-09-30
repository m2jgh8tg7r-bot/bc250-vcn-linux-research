# R282 persistent install result

Date: 2026-10-01

Persistent installation is directly proven.

Installed image:
- /boot/initramfs-7.2.3-r281-r274b.img
- SHA256 9765259d44bc1719c24318f3ac970fbbf74272b17e854aefb2b8380f12e7099c

Installed BLS entry:
- /boot/loader/entries/boot-entry-r282-r274b.conf
- SHA256 aac0ab07bf31082de8250e90ebda635242ff1ee59e442c4671336c9b37525551
- title BC-250 R282 R274-B direct provisioner (hardware start guards retained)
- version 0
- linux /vmlinuz-7.2.3-r138
- initrd /initramfs-7.2.3-r281-r274b.img

/boot/loader/entries and /boot/loader.1/entries are the same object and the entry views compare identical.

R180 recovery image remains exact:
b6ef569b85e24a5dedc81b076e4d4f977538bde400fb31c7d13d0674bb84c007

R180 BLS entry remains present.
Bazzite ostree-1 and ostree-2 entries remain present.

grubenv contains boot_success=1 and no next_entry.

Current /boot free bytes:
67764224

Result:
R282_PERSISTENT_INSTALL=PROVEN
R281_IMAGE_INSTALLED_EXACT=YES
R282_BLS_ENTRY_PRESENT=YES
R180_RECOVERY_PRESENT=YES
BAZZITE_ENTRIES_PRESENT=YES
PENDING_NEXT_ENTRY=NO
LIVE_BOOT=NOT_STARTED

Note: installed image link count is 2, likely because the first installer attempt left a hidden temporary hardlink after the pipeline-subshell cleanup bug. Audit this before first live boot.
