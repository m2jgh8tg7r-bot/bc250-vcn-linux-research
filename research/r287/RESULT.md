# R287 call-path / EOPNOTSUPP static audit

Date: 2026-10-01

Source identities:
- vcn_v2_0.c: eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
- amdgpu_vcn.c: 09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099
- amdgpu_device.c: cc9fe304c5e51434bb7a2bc4e04ecd3ce61c95e642ea2e9e8ec910d6eb66b679

Static results:

1. vcn_v2_0_start() is quarantined on Cyan 2.0.3 and immediately returns -EOPNOTSUPP.
2. The normal start sequence calls vcn_v2_0_mc_resume(), then releases VCPU reset, enables LMI/UMC channels, polls UVD_STATUS bit 1 for VCPU response, and only later programs ring bases.
3. Therefore simply removing the mc_resume Cyan guard is insufficient: normal start never reaches mc_resume while the start guard remains.
4. Conversely, removing only the start guard while leaving mc_resume skipped would release VCPU reset without programming the normal VCPU cache/BAR windows; do not do this.
5. vcn_v2_0_set_pg_state() also quarantines Cyan: it forces cur_state=GATE and returns -EOPNOTSUPP for a requested ungate.
6. vcn_v2_0_reset() is quarantined with -EOPNOTSUPP.
7. vcn_v2_0_dec_ring_test_ring() is quarantined with -EOPNOTSUPP.
8. amdgpu_vcn_dec_ring_test_ib() and amdgpu_vcn_enc_ring_test_ib() both explicitly return -EOPNOTSUPP under the Cyan 2.0.3 quarantine before submitting any IB.
9. Therefore the R285 vcn_dec/vcn_enc IB failures with -95 are intentional software quarantine results, not evidence of hardware execution or firmware failure.
10. Other VCN test/reset helpers in amdgpu_vcn.c are likewise quarantined.

Important boundary:

R285 proved live direct firmware provisioning and immediate BO readback equality. R286/R287 now show that multiple independent software guards still prevent:
- VCPU memory-window programming through the normal start path,
- ungating,
- VCPU start/reset progression,
- ring tests and IB submission.

The next safe step should remain static/build-only: design a Cyan-specific staged path that can separate memory-window programming from power/clock/reset release, rather than removing the broad start guard.

R287 log SHA256:
7f8bf4294a7bc523ec629d8a6c1b0ce858cc387f28c3cad285d4c1e18dbe82b3
