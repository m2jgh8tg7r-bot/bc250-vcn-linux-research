# R297 CP03 full-module build-only PASS — 2026-10-02 JST

## Scope

This checkpoint records the formal **build-only PASS** for the current BC-250 / Cyan Skillfish R274B + CP03 full-amdgpu composition, **without advancing to package/install/boot/LIVE CP03**.

Current main path:

```
R274B direct VCN firmware provisioning
  -> P1/Cyan hw_init branch checkpoint (CP03)
  -> package/install/one-shot boot
  -> LIVE pstore proof
```

The older assumption that PSP type-13 enrollment must succeed first is no longer the Linux main path. CP02 already proved, in the real initial boot lifecycle, that the exact VCN firmware payload can be copied directly into the VCN BO with readback `equal=1`.

## Prior LIVE checkpoint: CP02

CP02 evidence already established:

- firmware payload bytes: `405696`
- source offset: `256`
- VCN BO destination offset: `0`
- readback: `equal=1`
- execution context: initial boot lifecycle, kernel `7.2.3+`
- persistence: EFI pstore
- CP02 panic intentionally occurred immediately after the successful R274B copy

CP02 does **not** prove entry into `vcn_v2_0_hw_init()` Cyan branch, helper execution, reset release, VCPU fetch/execution, VCN ready, rings, decode or encode.

## CP03 purpose

CP03 is deliberately narrower than P1.

It is intended to prove only that the actual initial boot lifecycle reaches the Cyan branch in `vcn_v2_0_hw_init()`.

Intended order:

```
BC250 R291P1 pre_reset: begin
  -> BC250 R297 CP03: panic after P1 begin before helper
  -> panic("BC250 R297 CP03 after P1 begin before helper")
  -> helper call would have been next, but must not execute in CP03
```

Therefore CP03 introduces no new VCN MMIO writes beyond reaching that branch.

## Exact inputs

Base tree:

```
~/bc250-research/r152-psp-boundary-src
```

R274B overlay:

```
~/bc250-research/r274b-native-layout-build-v2/amdgpu_vcn.c.candidate
SHA256 06e1595fe8f90503664bc242fefa2cc151d7b43f15f762998ad476e3160ddd67
```

CP03 overlay:

```
~/bc250-research/research/r297-checkpoint-panic/cp03-v3/vcn_v2_0-r297-cp03.c
SHA256 fc90416f8abb77012185343c5457b34d641dac8df0ee7bf47899c0e7906efa9b
```

Known clean R152 source hashes:

```
amdgpu_vcn.c       09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099
vcn_v2_0.c         eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
amdgpu_psp.c       d0513be4c77d71d72a21ab47764cad16f958e5d193ff21d26d7844ec3be54b1d
amdgpu_discovery.c 37202992e43a0d450b0b7e0d9c1e47ca97af95f8d1d02e6f22108aaf9d5302b5
amdgpu_device.c    cc9fe304c5e51434bb7a2bc4e04ecd3ce61c95e642ea2e9e8ec910d6eb66b679
```

## CP03 object checkpoint

The isolated `vcn_v2_0.o` CP03 build had already passed:

- candidate provenance: PASS
- `MAKE_RC=0`
- object SHA256: `a7eefa982174993332b65e5514d19643a156a23e27156ccbc720acd042be531a`
- CP03 markers retained
- undefined `U panic` retained
- `vcn_v2_0_hw_init` retained
- cold path disassembly showed `_dev_info -> _dev_emerg -> panic`
- R152 `vcn_v2_0.c` restored exactly afterward

## CP03 full-module composition — formal PASS

Build script:

```
~/bc250-research/research/r297-checkpoint-panic/build-cp03-fullmodule.sh
```

The full amdgpu module build itself succeeded:

```
MAKE_RC=0
```

Output identity:

```
CP03_FULLMODULE_SHA256=9a9bc4fd0bec05a38189ac80e0d0c9d6fadf83010143c62a61e095d5d482290b
BUILD_ID=94c0a230babde9b97af4a513b97ea45a2e1aec89
MODULE_SIZE=809041408
```

Required markers all passed:

```
BC250 R274B direct_copy:
BC250 R291P1 pre_reset: begin
BC250 R297 CP03: panic after P1 begin before helper
BC250 R297 CP03 after P1 begin before helper
BC250 R141 psp_vcn_enrollment: skipped (R79 guard)
```

Forbidden/obsolete markers were absent:

```
BC250 R297 CP01
BC250 R297 CP02
BC250 R141 vcn_hw_init: skipped
BC250 R274A
```

Lifecycle/panic symbol checks passed:

```
amdgpu_vcn_resume
vcn_v2_0_early_init
vcn_v2_0_sw_init
vcn_v2_0_hw_init
U panic
```

## Machine-code evidence present in the full module

The emitted `vcn_v2_0_hw_init.cold` disassembly visibly contains:

```
_dev_info
  -> _dev_emerg
  -> panic
```

and no helper call appears in the shown cold path.

Relevant relocation sequence:

```
R_X86_64_PLT32  _dev_info-0x4
R_X86_64_PLT32  _dev_emerg-0x4
R_X86_64_PLT32  panic-0x4
```

This is exactly the intended CP03 machine-code control flow.

## Automated machine-code audit — resolved

The first full-module build produced the correct module but the audit ended with exit 1 because it used an unconstrained string search for `panic`. That could match the pathname `r297-checkpoint-panic` before the actual relocation.

The audit was narrowed to `R_X86_64_PLT32` relocation targets and first validated against the already-generated disassembly:

```
ORDER_DEV_INFO=487
ORDER_DEV_EMERG=792
ORDER_PANIC=987
HELPER_CALL_POS=-1
CP03_EXISTING_DISASM_AUDIT=PASS
```

The final build-only rerun then passed the same audit:

```
ORDER_DEV_INFO=487
ORDER_DEV_EMERG=792
ORDER_PANIC=987
HELPER_CALL_POS=-1
HW_INIT_COLD_DEV_INFO_THEN_DEV_EMERG_THEN_PANIC=YES
HW_INIT_COLD_HELPER_CALL_PRESENT=NO
CP03_MACHINE_CODE_CONTRACT=PASS
```

Final script and output identities:

```
BUILD_SCRIPT_SHA256=38dad21287f796a6675193c83f6614198fca54de64091395a4aa6dddce493b11
CP03_FULLMODULE_SHA256=9a9bc4fd0bec05a38189ac80e0d0c9d6fadf83010143c62a61e095d5d482290b
BUILD_ID=94c0a230babde9b97af4a513b97ea45a2e1aec89
R297_CP03_FULLMODULE_BUILD.log SHA256=0b486c08b3dfcc652cada22c92b72349cb01b7578ddb090032dbf11ada5393af
```

The module SHA256 and Build ID are identical to the earlier run, so the audit fix changed the tooling only and did not change the generated module.

Final result:

```
INPUT_CANDIDATES=PASS
R152_BASELINE=PASS
R274B_SOURCE_CONTRACT=PASS
CP03_SOURCE_CONTRACT=PASS
SOURCE_COMPOSITION=PASS
MAKE_RC=0
REQUIRED_MARKERS=PASS
FORBIDDEN_MARKERS_ABSENT=PASS
LIFECYCLE_SYMBOLS=PASS
PANIC_REFERENCE=PASS
CP03_MACHINE_CODE_CONTRACT=PASS
R152_SOURCE_RESTORATION=PASS
R297_CP03_FULLMODULE=PASS
CP03_FULLMODULE_SCRIPT_EXIT_CODE=0
TERMINAL_SURVIVED=YES
```

The detailed result is preserved in [research/r297/RESULT_CP03_FULLMODULE_PASS.md](../research/r297/RESULT_CP03_FULLMODULE_PASS.md).

## Safety boundary

No package/install/boot/LIVE CP03 action was performed as part of this checkpoint.

The full-module script explicitly recorded:

```
BOOT_WRITE=NO
MODULE_LOAD=NO
HARDWARE_ACCESS=NO
RESET_RELEASE=NO
FILTER_WRITE=NO
POWERUP_VCN=NO
REBOOT=NO
```

Do not infer any new VCN LIVE behavior from this build-only result.

## Exact uploaded-source provenance for this checkpoint

Conversation handoff Markdown:

```
SHA256 1e079b3e8ed694a496fb5d6964fc96897631b520b57b941930d5fef633fc992e
782 lines
```

Full-module script + terminal transcript:

```
SHA256 080c5393778338783fbc912a1b3edc31b5f2b6008a356bd15abd89aea2c02dce
621 lines
```


## CP03 HOME-only package — PASS

The exact full-module PASS was packaged in an isolated HOME-only initramfs tree and audited successfully without touching /boot.

Fixed identities:

```
SIGNED_MODULE_SHA256=43f177df38a8d4bef6572fcaca89c6d0f1f6165fd8983ee3ce62d019ec7c3d9a
IMAGE_SHA256=eb71ca03672e0d9070a5d6ecb3193ec175be70137ab212a802989456a4d31854
VCN_FW_SHA256=a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5
R297_CP03_HOME_PACKAGE=PASS
CP03_PACKAGE_SCRIPT_EXIT_CODE=0
```

Archive round-trip, signature metadata, CP03 marker contract and `U panic` retention all passed. Detailed result: [research/r297/RESULT_CP03_HOME_PACKAGE.md](../research/r297/RESULT_CP03_HOME_PACKAGE.md).

## CP03 installed-final audit — PASS

The installed CP03 image/BLS and the extracted amdgpu module/VCN firmware match the HOME package exactly. Signature metadata, marker contract, panic reference, installed machine-code order, protected recovery state and boot-selection state all passed.

Detailed result: [research/r297/RESULT_CP03_INSTALLED_FINAL_AUDIT.md](../research/r297/RESULT_CP03_INSTALLED_FINAL_AUDIT.md).

## Recommended next action — NOT executed here

The build-only gate is now complete. The next stage is to preserve exact CP03 module provenance through packaging and installation **without selecting or booting it yet**, then audit the initramfs/boot-entry path before any one-shot LIVE CP03 boot.

Required ordering:

```
1. package exact CP03 module
2. verify packaged module identity
3. install without selecting/booting
4. verify installed module identity and marker contract
5. build/audit the dedicated initramfs and boot entry
6. only then consider one-shot LIVE CP03
```

No helper execution, reset release, VCPU fetch, or other new VCN MMIO action should be introduced in CP03.

## Current scientific boundary

Already LIVE-proven:

```
VCN firmware direct provisioning into VCN BO with equal=1
```

Not yet LIVE-proven:

```
P1 hw_init Cyan branch reached
pre-reset helper entry/completion
reset release
first fetch
VCPU execution
VCN ready
RBC/ring bring-up
decode
encode
```

The next scientific milestone remains a LIVE CP03 pstore panic proving actual Cyan `vcn_v2_0_hw_init()` branch reach, but no such LIVE test has been performed at this checkpoint.
