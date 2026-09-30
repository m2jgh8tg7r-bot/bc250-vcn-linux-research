# R278 — retirement-candidate audit result

Date: 2026-10-01

R278 completed as a root-assisted **read-only** audit.

## Bootloader references

Search scope:

- `/boot/loader`
- `/boot/loader.1`
- `/boot/grub2`
- `/boot/efi`

Only the R180 research initramfs was referenced:

```text
/boot/loader/entries/boot-entry-r180-observation.conf
  initrd /initramfs-7.2.3-r180-observation.img

/boot/loader.1/entries/boot-entry-r180-observation.conf
  initrd /initramfs-7.2.3-r180-observation.img
```

No reference to the R138, R141, R157, R173, or R197 research initramfs filenames was found in the searched bootloader locations.

## Exact /boot vs retained-copy comparisons

### R138

```text
local:
  size   246875557
  sha256 c13534428c86b1ea268aaebe655f09c9306965561c92f064eed1fc22d10e6929

/boot:
  size   256958804
  sha256 33e7b04bbf6617cf721216c68f37a67c98345919aca1582c82d83882349ddc19

LOCAL_BOOT_HASH_MATCH=NO
```

R138 is **not** a retirement candidate from current evidence. The retained local file is not the exact installed /boot image.

### R141

```text
size   257089093
sha256 58fee6e04140062043fbc077fe6d1c5bf3b6c7c1687fa9ca60fa4cad252b10c3
LOCAL_BOOT_HASH_MATCH=YES
bootloader reference found=NO
```

### R157

```text
size   257089361
sha256 b0ad5c63356e92d9d6101ba32a0fe11f6cf52eb914e24e09ac8911a9d481d540
LOCAL_BOOT_HASH_MATCH=YES
bootloader reference found=NO
```

### R173

```text
size   257087863
sha256 5998a6cb7000ae76fd6c95dd5f729fff77fcb686e660abcf1aac22a6a8b5bd61
LOCAL_BOOT_HASH_MATCH=YES
bootloader reference found=NO
```

### R180

```text
size   257087698
sha256 b6ef569b85e24a5dedc81b076e4d4f977538bde400fb31c7d13d0674bb84c007
LOCAL_BOOT_HASH_MATCH=YES
bootloader reference found=YES
```

R180 is explicitly retained as the current research recovery/reference entry.

### R197

```text
size   256087382
sha256 80ea74fa41f605700a57a66cfed3e024ea43985c36d9d4df396d55093f0d5414
LOCAL_BOOT_HASH_MATCH=YES
bootloader reference found=NO
```

## Current BLS inventory

Both loader trees currently contain only:

- R180 research entry
- Bazzite ostree:1
- Bazzite ostree:0

No R141/R157/R173/R197 BLS entry is present.

## Safety result

The audit reported:

```text
R278_READ_ONLY=YES
NO_FILES_MOVED=YES
NO_FILES_DELETED=YES
NO_BOOT_CONFIG_CHANGED=YES
```

Audit log SHA256:

```text
5e76dfeb1e44f83521c0e6f882f48b91699a0caf14e4fd8384c302a2cf10c5ee
```

## Retirement candidates

Directly proven safe-to-consider for retirement from /boot, subject to a separate write-stage verification:

1. R141
2. R157
3. R173
4. R197

Not candidates:

- R180 — actively referenced recovery/reference entry
- R138 — local retained copy does not match installed /boot image

## Preferred first retirement candidate

Prefer **R141**.

Reason:

- exact retained-copy SHA match;
- no current bootloader reference;
- older diagnostic stage than R157/R173/R180/R197;
- removing only R141 is enough to solve the current capacity blocker;
- preserves R173 and R180, the most valuable direct-live provenance baselines in this branch of the research.

Current /boot free bytes:

```text
67,772,416
```

R141 installed image bytes:

```text
257,089,093
```

Projected free bytes after retiring only R141:

```text
324,861,509
```

That is enough for one new initramfs of approximately the same size class while leaving the other research images untouched.

## Evidence boundary

R278 proves redundancy/reconstructability conditions for the named /boot image bytes and absence of references in the searched bootloader locations.

It does **not** yet perform or prove:

- deletion/retirement;
- post-retirement free-space state;
- new R274-B initramfs construction;
- new BLS installation;
- live R274-B boot.
