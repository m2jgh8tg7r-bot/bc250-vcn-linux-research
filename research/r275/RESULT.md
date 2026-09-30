# R275 — artifact/provenance audit passed

Date: 2026-10-01

## Result

R275 artifact audit v2 passed completely.

### Exact input identities

```text
amdgpu.ko.unstripped
b1138dd396c0a0e31b3431b9da1a50ae1f564a0ef102864e63e4a75763576ef5

r274b-native-layout.patch
a46b83447bce8301f2516d561b270a25ddad84b8401652b04e7228c118421921

amdgpu_vcn.c.baseline
09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099

amdgpu_vcn.c.candidate
06e1595fe8f90503664bc242fefa2cc151d7b43f15f762998ad476e3160ddd67
```

All expected and actual hashes matched.

### Patch correspondence

A fresh `diff -u` generated from the retained exact baseline and exact candidate produced SHA256:

```text
a46b83447bce8301f2516d561b270a25ddad84b8401652b04e7228c118421921
```

which is exactly the retained R274-B patch SHA.

Therefore:

```text
baseline + retained patch -> exact candidate
```

is closed without relying on the unavailable `patch(1)` utility.

### Module identity

The retained build artifact is:

```text
ELF 64-bit LSB relocatable, x86-64
with debug_info, not stripped
BuildID reported by file(1):
df11540aa1aa8542efb46dbdfa12d3634d697da8
SHA256:
b1138dd396c0a0e31b3431b9da1a50ae1f564a0ef102864e63e4a75763576ef5
```

`modinfo` became readable when the same bytes were copied to a temporary `.ko` filename:

```text
license: GPL and additional rights
description: AMD GPU
author: AMD linux driver team
vermagic: 7.2.3+ SMP preempt mod_unload
MODINFO_READABLE=YES
```

The audit's separate `readelf` Build-ID extraction did not find a Build ID even though `file(1)` reported one. Treat the exact Build-ID extraction mechanism as unresolved, but this does not affect the SHA256 identity closure.

### Required markers

Present in the module:

```text
BC250 R141 psp_vcn_enrollment: skipped (R79 guard)
BC250 R141 vcn_hw_init: skipped
BC250 R274B direct_copy:
```

Absent:

```text
BC250 R274 direct_copy:
```

The R274-A marker is not present in the R274-B module.

### Added hardware-control token audit

```text
ADDED_HARDWARE_CONTROL_TOKENS=NONE
```

No new WREG/RREG/SMN/start/ring-init/LOAD_IP_FW/doorbell/soft-reset control token is introduced by the retained R274-B patch.

### Final audit status

```text
R275_ARTIFACT_AUDIT_V2=PASS
NO_MODULE_INSTALLED=YES
NO_BOOT_ARTIFACT_CHANGED=YES
```

## Evidence classification

Direct local filesystem/build proof:

- exact R274-B module identity;
- exact baseline/candidate/patch correspondence;
- module ELF readability;
- vermagic 7.2.3+;
- required quarantine/provisioning markers present;
- R274-A marker absent;
- no added hardware-control tokens in the source delta.

Still unproven:

- R274-B module loading on the user's BC-250;
- live VCN BO enlargement;
- live 405696-byte copy;
- live BO readback equality;
- absence of VCN PSP LOAD_IP_FW type13 in that boot;
- VCPU-visible bytes / first fetch / execution / ready;
- physical decode / encode.

## Next

R276 is not a live boot yet.

First close the live-artifact/recovery prerequisites using a read-only preflight:

- retained 7.2.3 kernel identity;
- retained R180 known-recovery boot artifact identity;
- boot-entry inventory;
- current default/normal environment observation;
- R274-B module identity;
- available disk space;
- signing/package inputs inventory.

Only after R276 preflight passes should a new one-shot boot artifact be constructed.
