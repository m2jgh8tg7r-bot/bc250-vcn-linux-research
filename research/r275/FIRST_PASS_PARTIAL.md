# R275 first-pass artifact audit — partial

Date: 2026-10-01

The first R275 artifact audit was informative but not complete.

Observed artifact identities:

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

Required module markers were present:

- BC250 R141 psp_vcn_enrollment: skipped (R79 guard)
- BC250 R141 vcn_hw_init: skipped
- BC250 R274B direct_copy:

The R274-A marker was absent.

The added-control-token scan returned NONE.

Two checks were not valid:

1. patch reconstruction did not happen because the host lacks the `patch` utility. The reported reconstructed hash was therefore just the untouched baseline and must not be interpreted as a failed patch/candidate correspondence.
2. `modinfo` failed on the filename `amdgpu.ko.unstripped`. Since the same file exists and hashes correctly, this is an audit-tool/path/suffix issue until proven otherwise, not evidence that the module is invalid.

R275 remains PARTIAL until a dependency-free second-pass audit closes these two items.
