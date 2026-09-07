# Reproducibility notes

This document records the exact identities used for the currently published BC-250 VCN findings. Hostnames, usernames, UUIDs, and unrelated machine-specific paths are intentionally omitted.

## Source provenance

- kernel: `7.2.1-ogc4.1.fc44.x86_64`
- OGC tag: `v7.2.1-ogc4`
- OGC commit: `14c028f83498b2900fecd0940a058a3ac0622afe`

Stock amdgpu identity:

- Build ID: `2da61adf20c29bf978a05facfb74130c81179faa`
- SHA-256: `744c135fd1a55e793034756664d23d2b7e6714729405446690e948aa216dad0e`

Exact `Module.symvers` used for ABI checking:

- SHA-256: `005560e7896f6da387ca45062cd7cb7377e266e69d1cc7aa06fd8562a93d6b05`

## VCN firmware candidate

- file: `vcn_2_0_3.bin`
- SHA-256: `a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5`
- size: 405952 bytes
- reported version fields: ENC 1.24 / DEC 8 / VEP 0 / revision 13

## Hardened live-test build

The final safety-hardened source patch used for the bounded NBIO transaction had:

- combined patch SHA-256: `6197af894ee930284f1d225dd92efbce8e73162707c441a929a966b92a6c9960`
- helper SHA-256: `3a5b882d2b96d8240a5659be7015f31f73b5623e091d9e087b52aac214301a29`
- superseded pre-hardening to hardened delta SHA-256: `7d37e84c8da5ab801ca11c238781580acb467137bbea68238a7e2aeb7453879b`

Built custom amdgpu:

- Build ID: `b0ca3ad4d1f157bf2a34b7e24fe221fff3a9a9b4`
- unstripped SHA-256: `d2a4d249a94cc4b2010b2e6d92a05167e876cf1f915e1f9d4e0eab4030592b97`
- stripped SHA-256: `cb3a6944a4c3861c7fe289a9ec1d4879cb6069c54300ffb526701521670fc0d6`
- symbol imports checked: 1146
- missing imports: 0
- vermagic matched the running stock kernel

Custom initramfs:

- SHA-256: `35a7152867fc60e92aad1b99708831ad9210991ea8d85b8221c489e15f6bf144`
- size: 251850195 bytes

The initramfs audit verified a single intended custom amdgpu, the exact firmware image, `modules.dep`, critical systemd/rootfs/btrfs/ostree modules, and `ostree-prepare-root`.

## Hardened manual boot artifact

Installed kernel image SHA-256:

- `2e78df5d9c802f04bdaa0dac81d155f8caf2737b4e04eb4fffe20de13116c9db`

The dedicated live-test BLS was manual-only and used a unique command-line token for post-boot identity verification. No `next_entry`, `saved_entry`, or default-entry change was used.

## Live transaction result

The physical-hardware transaction that matched exactly was:

```text
register          = 0x00000ef3
fresh old         = 0x00000000
target            = 0x00080c40
target readback   = 0x00080c40
restore           = 0x00000000
restore readback  = 0x00000000
```

The custom amdgpu Build ID and unique boot token were both verified after boot before this result was classified as a successful live experiment.

## Tested platform context

- AMD BC-250 / Cyan Skillfish
- BIOS P3.00
- SMU firmware reported as `0x00580600` (0.58.6.0)

This is a reproducibility anchor, not a claim that the same behavior is safe or identical on other BIOS/PMFW combinations.
