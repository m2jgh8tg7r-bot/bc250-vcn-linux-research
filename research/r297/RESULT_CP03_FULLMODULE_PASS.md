# R297 CP03 full-module build-only PASS — 2026-10-02 JST

## Result

The R297 CP03 full-amdgpu build-only composition is now a formal PASS.

No package, install, initramfs selection, module load, reboot, or LIVE hardware action was performed in this result.

## Inputs

R274B overlay:

```
SHA256 06e1595fe8f90503664bc242fefa2cc151d7b43f15f762998ad476e3160ddd67
```

CP03 overlay:

```
SHA256 fc90416f8abb77012185343c5457b34d641dac8df0ee7bf47899c0e7906efa9b
```

Final build script:

```
~/bc250-research/research/r297-checkpoint-panic/build-cp03-fullmodule.sh
SHA256 38dad21287f796a6675193c83f6614198fca54de64091395a4aa6dddce493b11
```

## Build result

```
MAKE_RC=0
CP03_FULLMODULE_SHA256=9a9bc4fd0bec05a38189ac80e0d0c9d6fadf83010143c62a61e095d5d482290b
BUILD_ID=94c0a230babde9b97af4a513b97ea45a2e1aec89
MODULE_SIZE=809041408
```

The module SHA256 and Build ID are identical to the earlier full-module build that ended with an audit-only exit 1. The audit fix therefore did not change the generated amdgpu module.

## Contract results

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

Required markers included:

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

## Machine-code audit

The previous audit bug used an unconstrained string search for `panic`, which could match the pathname `r297-checkpoint-panic` before the actual relocation.

The fixed audit matches `R_X86_64_PLT32` relocation targets.

Final observed order:

```
ORDER_DEV_INFO=487
ORDER_DEV_EMERG=792
ORDER_PANIC=987
HELPER_CALL_POS=-1
HW_INIT_COLD_DEV_INFO_THEN_DEV_EMERG_THEN_PANIC=YES
HW_INIT_COLD_HELPER_CALL_PRESENT=NO
CP03_MACHINE_CODE_CONTRACT=PASS
```

Relevant relocation sequence:

```
R_X86_64_PLT32  _dev_info-0x4
R_X86_64_PLT32  _dev_emerg-0x4
R_X86_64_PLT32  panic-0x4
```

The nearby objdump display label on the unresolved call instruction is not treated as the final call target; the relocation identifies `panic`.

## Dead-code observation

```
P1_RETURNED_MARKER_PRESENT=YES
P1_HELPER_SYMBOL_PRESENT=NO
```

This is acceptable for CP03 because `panic()` is noreturn and code after the CP03 stop may be eliminated by the compiler. CP03 is intentionally designed to stop before the helper executes.

## Source restoration

After the build:

```
RESTORED_AMDGPU_VCN_SHA256=09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099
RESTORED_VCN_V2_0_SHA256=eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075
R152_SOURCE_RESTORATION=PASS
```

## Safety boundary

The run recorded:

```
BOOT_WRITE=NO
MODULE_LOAD=NO
HARDWARE_ACCESS=NO
RESET_RELEASE=NO
FILTER_WRITE=NO
POWERUP_VCN=NO
REBOOT=NO
```

Therefore this result proves only the build/module/code-shape contract. It does not prove LIVE entry into the Cyan `vcn_v2_0_hw_init()` branch.

## Build log identity

```
R297_CP03_FULLMODULE_BUILD.log
SHA256 0b486c08b3dfcc652cada22c92b72349cb01b7578ddb090032dbf11ada5393af
```

## Scientific boundary

Already LIVE-proven by CP02:

```
VCN firmware direct provisioning into VCN BO with equal=1
```

Now build-proven:

```
R274B + CP03 full-module composition
Cyan hw_init CP03 machine-code stop:
_dev_info -> _dev_emerg -> panic
helper absent before stop
```

Still not LIVE-proven:

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

## Next stage

The next scientific milestone remains a one-shot LIVE CP03 boot whose EFI pstore evidence proves that the real initial boot lifecycle reached:

```
BC250 R291P1 pre_reset: begin
BC250 R297 CP03: panic after P1 begin before helper
```

Before that LIVE boot, package/install/initramfs/boot-entry provenance should be audited and fixed to the exact CP03 module.
