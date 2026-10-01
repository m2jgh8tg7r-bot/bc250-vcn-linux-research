R291-P2A provenance result (2026-10-01)

The R291-D worktree amdgpu_vcn.c SHA256 is 1437aff7a1df69d33406e39266764b88f7995c8eb5c54a9f1aa0562eb3e22f36. It is not the R152/R274-B baseline (09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099) and not R274-B (06e1595fe8f90503664bc242fefa2cc151d7b43f15f762998ad476e3160ddd67).

The same 1437 SHA is present in source-R137, r135-kernel-src, the saved v7.2 source history, and other upstream-era trees. Diffing against R152 shows that 1437 lacks the later BC-250/Cyan quarantine additions in amdgpu_vcn.c, including the PSP VCN enrollment skip and common VCN ring/test quarantine guards.

Conclusion: r291d-worktree is suitable for isolated vcn_v2_0 object builds but must not be used as the base for the live composed full module. The composed module must instead use the exact R152 safe baseline and overlay only exact R274-B amdgpu_vcn.c plus exact R291-P1 vcn_v2_0.c.

No source modification, build, module link/install, boot change, hardware access, or reboot occurred in P2A.
