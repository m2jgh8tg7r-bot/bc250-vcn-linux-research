# R297 CP03 privileged pre-install preflight PASS — 2026-10-02 JST

Status: PASS

Preflight script:
- SHA-256: db9404997e04041d72485bcd3901b11d1cbae51265c3719c0f5feab71d379b50

CP03 HOME package:
- image SHA-256: eb71ca03672e0d9070a5d6ecb3193ec175be70137ab212a802989456a4d31854
- signed module SHA-256: 43f177df38a8d4bef6572fcaca89c6d0f1f6165fd8983ee3ce62d019ec7c3d9a
- package script SHA-256: c68c1bc364f212ae5e7741cccbd98d92b78766b5e5968084e11daf4558009cda
- package completed-log SHA-256: 059894cf29cb1fdabb4f0305485244471c7f7991e640f468d27de5b225748850
- semantic package log contract: PASS

Installed CP02:
- image SHA-256: 6a20504c1e59543d285e6dd5dbd5068b1f290d67ab38861f1cf35da2c78d5c31
- BLS SHA-256: f85ced260e4c16763a42797cce2cd1e1794e21a096db5b98a60d2eeb37a86f45
- installed identity: PASS
- HOME recovery material: PASS
- BLS snapshot to HOME: PASS

CP03 BLS candidate:
- SHA-256: 1819a92c492e7da53b84e361da51c247206192d0d449d35e158d54e9664b707b
- title: BC-250 R297 CP03 hw_init branch checkpoint
- kernel: /vmlinuz-7.2.3-r138
- initrd: /initramfs-7.2.3-r297-cp03.img
- pstore/panic/no-plymouth options retained
- contract: PASS

Protected identities:
- research kernel: c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6
- R180 image: b6ef569b85e24a5dedc81b076e4d4f977538bde400fb31c7d13d0674bb84c007
- R180 BLS: 30e79f5193fe4488e7c194f4fae397c0f0f0d2f3ccd200405dec17fc01d423d2
- grub.cfg: 4ce37c9435a99e716d02a842715ee6e74eb596cff9da45f56a4e3cf541a5aa56
- ostree-1.conf: eeffb2867a8e0479b6f3dd63bc2b7e5d5614b9bea4c214c48b0b7e146686bba7
- ostree-2.conf: 4de8416b08bdd0e805d463529228c7d2615ebc0f78f840e2c842e4abf46d0145
- protected identities: PASS

GRUB semantic state:
- boot_success=1
- no pending next_entry
- PASS

Retired state:
- R291 artifacts absent
- CP01 artifacts absent
- CP03 install targets absent

/boot accounting:
- free now: 67,764,224 bytes
- CP02 reclaimable: 257,087,851 bytes
- CP03 image: 257,088,845 bytes
- estimated free after CP02 retirement: 324,852,075 bytes
- required CP03 plus 50 MiB margin: 309,517,645 bytes
- space check: PASS

Safety boundary:
- no /boot write
- CP02 not deleted
- CP03 not installed
- no boot selection change
- no module load
- no hardware access
- no reset/filter/power action
- no reboot

Final:
- R297_CP03_PRIVILEGED_PREFLIGHT=PASS
- CP03_PREFLIGHT_EXIT_CODE=0
- TERMINAL_SURVIVED=YES

Next: retire only the exact CP02 image/BLS pair and install the exact CP03 image/BLS pair without selecting a boot or rebooting.
