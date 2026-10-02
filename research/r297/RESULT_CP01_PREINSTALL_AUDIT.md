# R297 CP01 pre-install read-only audit

Date: 2026-10-02

Status: pre-install audit completed; direct install is blocked by /boot free space.

R297 package:
- initramfs SHA-256: 53915d3ab095c6824634e65cf574e569f8dec0782ae3846f9c57f94ef205533d
- signed module SHA-256: 967132a16903daaca4f4f2877fffab087b035ad5935091ec8bc5ec7521d35d6f

Current safe boot:
- 7.2.1-ogc4.1.fc44.x86_64

Research kernel:
- /boot/vmlinuz-7.2.3-r138
- SHA-256: c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6

/boot:
- free bytes: 67,756,032
- R297 image bytes: 257,088,213
- required with 50 MB margin: 307,088,213
- direct install space: NO

Installed R291:
- image size: 257,087,668
- inode link count: 1
- only one hardlink/path found
- HOME backup SHA-256: 03db7e3aca4d096be7d2abcc95a1adcb9becd9f6731e43866d5b4e8740960bbb
- estimated free space after retiring R291 image: 324,843,700
- space after R291 retire: YES

R291 BLS entries currently referencing the image:
- boot-entry-r291-debug.conf
- boot-entry-r291-pre-reset.conf
- boot-entry-r291-pstore.conf

R297 targets are currently absent.

Normal Bazzite entries remain present. R180 recovery entry remains present. grubenv reports boot_success=1.

Important audit limitation:
The unprivileged SHA command did not print hashes for root-readable-only initramfs files in /boot, so exact installed R180 and installed R291 image identities were not re-proven by this audit. A privileged read-only hash audit is required before retiring R291 or writing R297.

Audit log SHA-256:
d3aa83ea1859294d985b8192929af5625360aa5141531c473939e14f58caa37f

Next:
Perform a sudo read-only exact hash/policy audit, preserve the three R291 BLS entries and installed image identity to HOME, then retire only R291 and install R297 without changing boot selection.
