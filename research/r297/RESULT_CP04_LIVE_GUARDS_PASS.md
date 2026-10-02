# R297 CP04 LIVE result: guards pass before first VCN MMIO

Date: 2026-10-02 JST

Evidence class: LIVE

Result: PASS

Recovered EFI pstore generation:
- 1790934789: CP04
- 1790929230: earlier CP03

CP04 LIVE sequence:
- BC250 R274B direct_copy: bytes=405696 src_off=256 dst_off=0 bo=1069056 equal=1
- BC250 R291P1 pre_reset: begin
- BC250 R297 CP04: helper_entry before guards
- BC250 R297 CP04: guards_pass before first VCN MMIO
- Kernel panic - not syncing: BC250 R297 CP04 guards_pass before first VCN MMIO

What this proves:
1. The CP04 boot reached the Cyan hw_init branch after the R274B direct-copy path.
2. Execution entered the inlined pre-reset helper body.
3. The software guard `adev->pg_flags || adev->cg_flags` did not return.
4. The software guard `amdgpu_sriov_vf(adev)` did not return.
5. Execution reached the checkpoint immediately before the first VCN MMIO.
6. The installed machine-code audit independently proved panic terminates the cold path with zero executable instructions after panic, so this CP04 run did not perform the first VCN MMIO.

What this does NOT prove:
- no PGFSM write occurred
- no VCN power-state transition occurred
- no VCN reset release occurred
- no VCPU execution/ready state
- no VCN ring functionality
- no decode/encode functionality

This result closes the software-guard uncertainty for the current CP04 environment and supports a next checkpoint that isolates the first PGFSM_CONFIG write and observes its status before any later helper operations.
