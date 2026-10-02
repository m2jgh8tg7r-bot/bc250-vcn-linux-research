# R297 CP01 privileged pre-install preflight PASS

Date: 2026-10-02

Status: PASS

The preflight was executed as a dedicated script so failures would not terminate the interactive terminal. Script exit code was 0 and the terminal survived.

Verified:
- current safe kernel: 7.2.1-ogc4.1.fc44.x86_64
- R297 image SHA-256: 53915d3ab095c6824634e65cf574e569f8dec0782ae3846f9c57f94ef205533d
- R297 signed module SHA-256: 967132a16903daaca4f4f2877fffab087b035ad5935091ec8bc5ec7521d35d6f
- research kernel SHA-256: c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6
- R180 recovery image SHA-256: b6ef569b85e24a5dedc81b076e4d4f977538bde400fb31c7d13d0674bb84c007
- R180 BLS SHA-256: 30e79f5193fe4488e7c194f4fae397c0f0f0d2f3ccd200405dec17fc01d423d2
- normal Bazzite BLS entries exact
- installed R291 image equals HOME backup exactly, SHA-256 03db7e3aca4d096be7d2abcc95a1adcb9becd9f6731e43866d5b4e8740960bbb
- R291 installed image link count is 1 and no alias/hardlink was found
- all three R291 BLS entries were snapshotted to HOME
- R297 BLS candidate passes title/version/kernel/initrd/pstore/panic/plymouth contract
- R297 /boot targets are absent
- grubenv has boot_success=1 and no next_entry
- space after retiring R291 is sufficient with 50 MB margin

R291 BLS snapshot hashes:
- debug: 0388befa640d85604bc84075be06cbf2ea2fd6277c56a68e40f2f0fb7fc1d9c0
- pre-reset: 0424f1f06e527de2f846a281ed9303b09646c8a2e7bfc4281f1d67e92555b762
- pstore: 7a8f19dad6ce89d4d8bc932815e4a8db9fa5a65f34ebde462e8f1909afba3d60

R297 BLS candidate SHA-256:
d05ce199ceadb76c62097a34f445ccbb37192f941a1372197739906cfd165b46

Space:
- free now: 67,756,032 bytes
- R291 reclaimable: 257,087,668 bytes
- R297 image: 257,088,213 bytes
- free after R291 retire estimate: 324,843,700 bytes
- required with 50 MB margin: 307,088,213 bytes

No /boot write, boot selection change, R291 removal, R297 install, module load, or reboot occurred.

Preflight log SHA-256:
28e333c5fe33f1c9a0c2df6e6f3fb480a39edce23d29245b5e19c0061435369e

Next: retire only the R291 image and its three BLS entries, install the exact R297 image and BLS entry, preserve R180/normal Bazzite/grub policy, and do not select a boot.
