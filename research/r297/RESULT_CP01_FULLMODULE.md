# R297 CP01 full-module build result

Date: 2026-10-02

Status: PASS

Inputs:
- R152 amdgpu_vcn.c baseline: 09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099
- R152 vcn_v2_0.c baseline: eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
- R274B candidate: 06e1595fe8f90503664bc242fefa2cc151d7b43f15f762998ad476e3160ddd67
- R297 CP01 candidate: f2f3708699024896310cdb766b9a9efc8bc2f84a7a0b3e3217e20fb0e4b04341

Output:
- full amdgpu module build completed with MAKE_RC=0
- module SHA-256: 85932935276df18f8c1ede808a027b03404359760c012c06adf088e5b14684ec
- Build ID: c8bf2320b1f12c717e86acef28b670c07154234f
- expected R274B / R141 / R297 CP01 / R291P1 markers retained
- obsolete R141 hw_init-skip and R274A markers absent
- key VCN function symbols retained

R152 source restoration passed exactly after the build. Unchanged safety-source hashes:
- amdgpu_psp.c d0513be4c77d71d72a21ab47764cad16f958e5d193ff21d26d7844ec3be54b1d
- amdgpu_discovery.c 37202992e43a0d450b0b7e0d9c1e47ca97af95f8d1d02e6f22108aaf9d5302b5
- amdgpu_device.c cc9fe304c5e51434bb7a2bc4e04ecd3ce61c95e642ea2e9e8ec910d6eb66b679

Build log SHA-256:
a943c36d69dbb2f34ba322bfa750f272e0e8fe660e9900b456cf5f870bec2e0d

Boundary: this establishes full-module composition/link success only. Boot-time execution and persistent checkpoint capture remain to be tested.

Next: package/sign the exact module into a dedicated R297 CP01 boot artifact, verify archive provenance, then perform one controlled checkpoint boot.
