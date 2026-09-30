# R271 historical artifact integrity evidence

Sanitized derived evidence from the user's 2026-10-01 read-only audit.

## Initramfs integrity

```text
R173
local SHA256 = 5998a6cb7000ae76fd6c95dd5f729fff77fcb686e660abcf1aac22a6a8b5bd61
/boot SHA256 = 5998a6cb7000ae76fd6c95dd5f729fff77fcb686e660abcf1aac22a6a8b5bd61
LOCAL_BOOT_MATCH=YES

R180
local SHA256 = b6ef569b85e24a5dedc81b076e4d4f977538bde400fb31c7d13d0674bb84c007
/boot SHA256 = b6ef569b85e24a5dedc81b076e4d4f977538bde400fb31c7d13d0674bb84c007
LOCAL_BOOT_MATCH=YES
```

## Extracted amdgpu module identities

```text
R173
size=46855689
sha256=27f3d114330876c54fb40d730529d440a31ebbe5f1794c31ce200dc726197bf4
build_id=90c4d49de3e79d30f63c61f595245d57b7d1e3e9

R180
size=46857713
sha256=5185df438a65ae63cd4619e10e4ead2fd8fe8483538743d81b7acdb48c8de78a
build_id=9e4870cde4dfbec0c4dab01a3a7667bd1c153223

R173_R180_AMDGPU_IDENTICAL=NO
```

## Historical initramfs build characteristics

Both R173 and R180 were built with:

```text
--kver 7.2.3+
--kmoddir .../r137-modules-root/lib/modules/7.2.3+
--add-drivers amdgpu
--include .../vcn_2_0_3.bin /usr/lib/firmware/amdgpu/vcn_2_0_3.bin
```

Both images contain:

```text
usr/lib/firmware/amdgpu/vcn_2_0_3.bin size=405952
usr/lib/modules/7.2.3+
```

## Current-vs-historical environment gap

Current installed module tree observed:

```text
7.2.1-ogc4.1.fc44.x86_64
```

Historical retained kernel images identify themselves as version:

```text
7.2.3+
```

No R173/R180/7.2.3 reference was returned from the captured scan of `/boot/loader/entries`.

## Interpretation

This evidence supports integrity and provenance reconstruction.

It does not establish replay safety, present PSP response behavior, firmware acceptance, GPCNT, RBC, reset release, first fetch, VCPU execution, or hardware video.
