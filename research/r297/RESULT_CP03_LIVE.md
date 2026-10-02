# R297 CP03 LIVE result — 2026-10-02 JST

Status: LIVE PASS

EFI pstore captured after the CP03 boot contains:

- R274B direct provisioning readback:
  - bytes=405696
  - src_off=256
  - dst_off=0
  - bo=1069056
  - equal=1
- BC250 R291P1 pre_reset: begin
- BC250 R297 CP03: panic after P1 begin before helper
- Kernel panic - not syncing: BC250 R297 CP03 after P1 begin before helper

This proves that the actual initial boot lifecycle reached the Cyan VCN vcn_v2_0_hw_init() branch and executed the CP03 checkpoint placed immediately after the P1 begin marker and before the pre-reset helper.

Scientific boundary after CP03:
LIVE-proven:
- direct VCN firmware provisioning into VCN BO with readback equal=1
- sw_init path completion through the later hardware-init lifecycle
- entry into the Cyan vcn_v2_0_hw_init() branch
- CP03 checkpoint panic reached before helper execution point

Not LIVE-proven:
- pre-reset helper entry
- pre-reset helper completion
- helper MMIO effects
- reset release
- first VCPU fetch
- VCPU execution
- VCN ready
- RBC/ring bring-up
- decode
- encode

Postmortem capture:
- 17 EFI pstore files copied into HOME
- runtime pstore_disable restored to Y
- pstore was not cleared after capture

Important boot-state note:
After returning to the normal safe Bazzite kernel, grubenv still showed:
next_entry=boot-entry-r297-cp03

Therefore CP03 must be explicitly disarmed before any further reboot.
