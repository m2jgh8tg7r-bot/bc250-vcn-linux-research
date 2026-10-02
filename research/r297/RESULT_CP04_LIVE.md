# R297 CP04 LIVE PASS — helper entry and both software guards passed before first VCN MMIO

Date: 2026-10-02 JST

Status: LIVE PASS

## Scope

CP04 was designed to answer one narrow question:

> Does the Cyan Skillfish VCN 2.0.3 path actually enter the pre-reset helper and pass its software-only pg/cg and SR-IOV guards on real BC-250 hardware?

The checkpoint intentionally panics before the helper's first VCN MMIO access.

This result is therefore LIVE software/control-flow evidence, not VCN hardware-activation evidence.

## Pre-LIVE artifact chain

Installed CP04 final audit had already established:

- initramfs SHA-256:
  `888676eab4a586250f2fce213eb1deaeea569e70f64c1722b1b9b17af2733f35`
- installed BLS SHA-256:
  `0efd19c1a7d784a6b4399aa146e25cf6062bd45c0a1ab3bda46b5dd9697bde53`
- signed amdgpu.ko SHA-256:
  `2b154c25d7de1bef4fcdc127edf10df3b6388897760cc0da55b52242fae2bdf9`
- VCN firmware SHA-256:
  `a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5`
- research kernel SHA-256:
  `c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6`

Installed machine-code audit established:

- standalone helper symbol absent because the helper prefix was inlined into `vcn_v2_0_hw_init.cold`
- three `_dev_info` relocations
- one `_dev_emerg` relocation
- one `panic` relocation
- relocation order: P1 begin -> helper-entry -> guard-return log -> guards-pass -> panic
- zero executable instructions after the panic call in the cold symbol
- no executable VCN MMIO sequence survives after the CP04 panic checkpoint

Installed-final-audit script SHA-256:
`7136a85bce26309a488884418950e081360dc6509c5e6f8e4a97d7376da94775`

Installed-final-audit log SHA-256:
`f77f958fad46f50f6e81eb4bf6ea5e181f655f42b4d848a81b726184647ad1cc`

## LIVE pstore evidence

The CP04 crash record group is `1790934789`.

The decisive record is:

```text
[    7.423970] amdgpu 0000:01:00.0: BC250 R291P1 pre_reset: begin
[    7.423973] amdgpu 0000:01:00.0: BC250 R297 CP04: helper_entry before guards
[    7.423975] amdgpu 0000:01:00.0: BC250 R297 CP04: guards_pass before first VCN MMIO
[    7.423978] Kernel panic - not syncing: BC250 R297 CP04 guards_pass before first VCN MMIO
```

Individual record:
`dmesg-efi_pstore-179093478903001`

Individual record SHA-256:
`128b6bbed9a1dfc5bcac6183a1fa54dabc37b69b12c15dd7661dd357333a2edd`

Group hashes:

- ascending raw:
  `d7eb300a79fc9bd5e0921f7287ed0f0bae24184d8571f2879ec609cada01cd66`
- descending raw:
  `066817b68d7a0e2ec7f9004759342aff4d4036d7a988c8e5980cf85096863373`

## LIVE lifecycle context in the same CP04 pstore group

The same crash group also preserves the expected earlier path:

```text
BC250 R141 early_init_begin ret=0
BC250 R141 early_init_end ret=0
BC250 R141 sw_init_begin ret=0
BC250 R141 common_sw_init_begin ret=0
[VCN instance 0] Found VCN firmware Version ENC: 1.24 DEC: 8 VEP: 0 Revision: 13
BC250 R141 common_sw_init_end ret=0
BC250 R141 psp_vcn_enrollment: skipped (R79 guard)
BC250 R141 buffer_resume_begin ret=0
BC250 R274B direct_copy: bytes=405696 src_off=256 dst_off=0 bo=1069056 equal=1
BC250 R141 buffer_resume_end ret=0
BC250 R141 sw_init_end ret=0
BC250 R141 ucode_bo_begin ret=0
BC250 R141 ucode_bo_end ret=0
BC250 R141 hw_phase1_begin ret=0
BC250 R141 hw_phase1_end ret=0
BC250 R141 device_fw_loading_begin ret=0
BC250 R152 psp_scan_begin max_ucodes=73
BC250 R152 psp_vcn_slot index=57 id=0 fw_present=0 size=0
BC250 R152 psp_vcn_skip_decision skip=1
BC250 R141 device_fw_loading_end ret=0
BC250 R141 hw_phase2_begin ret=0
BC250 R291P1 pre_reset: begin
BC250 R297 CP04: helper_entry before guards
BC250 R297 CP04: guards_pass before first VCN MMIO
Kernel panic - not syncing: BC250 R297 CP04 guards_pass before first VCN MMIO
```

## What CP04 LIVE proves

CP04 LIVE proves, on the tested BC-250:

1. execution reaches the R291P1 `pre_reset: begin` checkpoint;
2. execution enters the Cyan pre-reset helper body far enough to execute the helper-entry marker;
3. the pg/cg early-return guard does not return;
4. the SR-IOV early-return guard does not return;
5. therefore the path reaches the explicit guards-pass checkpoint;
6. the deliberate panic executes before the first VCN MMIO operation according to the independently audited installed machine code.

For the tested execution, the guard outcome implies:

```c
(adev->pg_flags || adev->cg_flags) == 0
amdgpu_sriov_vf(adev) == false
```

This is the first LIVE proof in this checkpoint sequence that the software path reaches the boundary immediately before the helper's first VCN MMIO.

## What CP04 LIVE does NOT prove

CP04 does **not** prove any of the following:

- any VCN MMIO read or write occurred;
- PGFSM state changed;
- VCN power became active;
- reset state changed;
- FILTER registers were written;
- PowerUpVcn occurred;
- the VCPU executed firmware;
- VCN became ready;
- decode/encode rings became operational;
- a ring test passed;
- hardware decode or encode worked;
- VA-API worked.

Do not describe CP04 as a VCN activation result.

## Comparison with CP03

The older CP03 group is `1790929230` and stops earlier:

```text
BC250 R291P1 pre_reset: begin
BC250 R297 CP03: panic after P1 begin before helper
Kernel panic - not syncing: BC250 R297 CP03 after P1 begin before helper
```

CP03 group hashes:

- ascending raw:
  `f925675831fa6132ce51d692a316750819ea787930f1a75ee6eab85536159c61`
- descending raw:
  `75d794d8cb9397fbffcfbaa62b9580bdff57c00bbac5eda9a32a154522d69766`

The CP03 -> CP04 progression therefore moves the LIVE boundary from immediately before helper entry to immediately before the helper's first VCN MMIO.

## pstore recovery note

After returning to the normal Bazzite boot, `systemd-pstore.service` saw an empty `/sys/fs/pstore` because the normal policy had `efi_pstore.pstore_disable=Y`.

Temporarily setting the runtime parameter to `N` surfaced 34 EFI pstore records, including both CP03 and CP04 groups. The records were copied to HOME and hashed, then the normal policy was restored to:

```text
PSTORE_DISABLE=Y
```

This recovery procedure did not itself execute the research kernel or perform VCN MMIO.

## Scientific classification

- source/object/package/installed artifact evidence: BUILD-ONLY / static-forensic chain
- pstore checkpoint evidence above: LIVE
- hardware-access evidence at CP04: NONE by design

## Next checkpoint direction

The next experiment should remain narrower than the full P1 helper.

A suitable CP05 design is:

1. preserve the same entry/guard chain;
2. execute only the first intended PGFSM_CONFIG write;
3. checkpoint immediately after that write;
4. separately capture/read or wait on PGFSM_STATUS in a later checkpoint;
5. panic before later POWER_STATUS, clock-gating, reset/VCPU, ring, or decode/encode operations.

That progression would test the first actual VCN hardware transition without conflating it with reset release, VCPU start, or ring bring-up.
