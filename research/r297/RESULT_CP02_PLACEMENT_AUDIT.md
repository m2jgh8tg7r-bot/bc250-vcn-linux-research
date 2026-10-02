# R297 CP02 placement audit

Date: 2026-10-02
Status: PASS

Exact R274B source SHA-256:
06e1595fe8f90503664bc242fefa2cc151d7b43f15f762998ad476e3160ddd67

amdgpu_vcn_resume is lines 374..467 in the audited source.

Cyan Skillfish direct-copy success path:
- firmware source/BO bounds are checked
- BO copy and readback are performed
- equality is computed with memcmp
- the result is logged by the R274B direct_copy marker
- if equal is false, the function returns -EIO

Therefore the CP02 checkpoint must be inserted after the `if (!equal) return -EIO;` guard and before the following non-Cyan `else if` branch. Reaching CP02 will then prove that the Cyan Skillfish direct-copy/readback path completed with equal=true in the live boot lifecycle.

No source modification, build, boot write, module load, or reboot occurred in this placement audit.
