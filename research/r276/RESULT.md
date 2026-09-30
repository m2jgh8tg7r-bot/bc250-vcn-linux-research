# R276 — live-artifact/recovery preflight result

Date: 2026-10-01

R276 preflight is sufficient to establish the current recovery baseline, but it also found a packaging blocker.

## Proven current state

- R274-B module still matches SHA256 `b1138dd396c0a0e31b3431b9da1a50ae1f564a0ef102864e63e4a75763576ef5`.
- retained Linux 7.2.3 kernel copies match the historical SHA256 `c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6`.
- retained user-owned R180 initramfs matches `b6ef569b85e24a5dedc81b076e4d4f977538bde400fb31c7d13d0674bb84c007`.
- /boot contains the R180 BLS entry referencing `/vmlinuz-7.2.3-r138` and `/initramfs-7.2.3-r180-observation.img`.
- normal Bazzite ostree entries remain present.
- all five guarded source baseline hashes remain unchanged.
- signing material and historical packaging scripts are retained locally.

## Important limitation

The root-owned /boot R180 initramfs exists but is mode 0600, so the non-root preflight could not re-hash that copy. Historical deep-integrity evidence previously proved the installed R180 copy matched the retained user copy. Current existence is proven; current byte identity of the root-only copy remains un-rechecked in R276.

## Packaging blocker

Current /boot space:

```text
2.0G total
1.8G used
65M free
97% used
```

The retained R180 image is about 246 MiB. Therefore a new similarly-sized initramfs cannot be added while preserving the existing R180 recovery artifact.

Do not overwrite or remove R180.

Historical R180 preparation solved a similar space problem by retiring a specifically verified older R140 artifact, but the current BLS inventory no longer shows R140. Therefore that historical removal procedure must not be replayed blindly.

## Result

```text
R276_RECOVERY_BASELINE=PASS
R276_LIVE_PACKAGING=BLOCKED_BY_BOOT_SPACE
R180_RECOVERY_ENTRY=PRESENT
R180_RETAINED_USER_COPY_HASH=VERIFIED
NORMAL_BAZZITE_ENTRIES=PRESENT
LIVE_BOOT=NOT_STARTED
```

## Next

R277: read-only /boot occupancy and orphan-artifact inventory. Identify exact files consuming space and classify only files that can be proven redundant against retained copies. No deletion or move in R277.
