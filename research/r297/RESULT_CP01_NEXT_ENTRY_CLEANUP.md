# R297 CP01 stale next_entry cleared

Date: 2026-10-02

After the successful CP01 LIVE/pstore run, grubenv still contained:
- boot_success=1
- next_entry=boot-entry-r297-cp01

The post-CP01 grubenv was saved to HOME with SHA-256:
e65c9fe33b62ef7147de17656d52d85d659690b9813ba851df91c46e780e1b75

Then next_entry was explicitly unset and grubenv was verified to contain only:
- boot_success=1

No reboot was performed during this cleanup.
