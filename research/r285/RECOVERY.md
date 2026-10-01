# R285 recovery closure

Date: 2026-10-01

After collecting the full kernel journal from the successful R285 experimental boot, the system was rebooted manually back to the normal Bazzite entry.

Normal boot verification:

- uname -r:
  7.2.1-ogc4.1.fc44.x86_64
- cmdline points to the normal ostree deployment and normal 7.2.1 kernel
- grubenv contains:
  boot_success=1
- no next_entry is present

Full R285 experimental kernel journal was preserved before reboot:

- /home/kazuyuki/bc250-r285-kernel-full.log
- SHA256:
  0aa8e7b392e11c3f8f2df4f852f1cf9abca258d02fc25319ed8cfee71693d57c

Result:

R285_EXPERIMENTAL_BOOT_COMPLETE=YES
R285_FULL_KERNEL_LOG_PRESERVED=YES
NORMAL_BAZZITE_RECOVERY=PROVEN
NORMAL_KERNEL=7.2.1-ogc4.1.fc44.x86_64
PENDING_NEXT_ENTRY=NO
