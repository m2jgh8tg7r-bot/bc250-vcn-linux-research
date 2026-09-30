# R285 live result

Date: 2026-10-01

Live boot reached kernel 7.2.3+ on BC-250 with the experimental amdgpu module loaded.

Key live lines:

- VCN firmware found: ENC 1.24 DEC 8 VEP 0 Revision 13
- BC250 R141 psp_vcn_enrollment: skipped (R79 guard)
- BC250 R274B direct_copy: bytes=405696 src_off=256 dst_off=0 bo=1069056 equal=1
- BC250 R152 psp_vcn_slot index=57 id=0 fw_present=0 size=0
- BC250 R152 psp_vcn_skip_decision skip=1
- BC250 R141 vcn_hw_init: skipped
- vcn_dec / vcn_enc0 / vcn_enc1 software rings were registered
- their IB tests returned -95
- DRM initialized and /dev/dri/card1 plus renderD128 were present

Collector summary:

- R274B_DIRECT_COPY_MARKER=YES
- R274B_DIRECT_COPY_EQUAL_1=YES
- PSP_VCN_ENROLLMENT_GUARD_LIVE=YES
- VCN_HW_INIT_GUARD_LIVE=YES

Evidence boundary:

This proves live host-side VCN BO provisioning and immediate readback equality while the VCN PSP slot is not enrolled in the instrumented PSP scan and VCN hardware init remains skipped.

It does not prove VCPU visibility, first fetch, VCPU execution/ready, functional VCN ring execution, VA-API, decode, or encode.

Log SHA256:
22b1ee120e406235b54c128c1d94b638f587c8cca1b59f1b80ee686fb99d647a
