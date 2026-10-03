# R297 CP06 progress checkpoint — single PGFSM_STATUS read candidate

Date: 2026-10-03 JST

Status: **PRE-LIVE CHAIN PASS / SELECT-WITNESS LIVE PASS / CP06 MAIN LIVE STILL NOT PROVEN**

## Scope

CP06 is the next checkpoint after the CP05 LIVE proof of the first intended VCN MMIO write path.

The CP06 design performs exactly:

1. the already-proven `PGFSM_CONFIG = 0x55555` write;
2. one `PGFSM_STATUS` read;
3. a raw-value log;
4. an intentional panic immediately after the read.

It intentionally does **not** execute a PGFSM wait loop or access `UVD_POWER_STATUS` before the panic.

## CP05 prerequisite

CP05 is already recorded separately as LIVE PASS in:

`research/r297/RESULT_CP05_LIVE.md`

The decisive CP05 LIVE sequence was:

```text
[    7.410959] amdgpu 0000:01:00.0: BC250 R291P1 pre_reset: begin
[    7.410961] amdgpu 0000:01:00.0: BC250 R297 CP05: helper_entry before guards
[    7.410963] amdgpu 0000:01:00.0: BC250 R297 CP05: guards_pass before PGFSM_CONFIG
[    7.410966] amdgpu 0000:01:00.0: BC250 R297 CP05: after PGFSM_CONFIG write before status wait
[    7.410969] Kernel panic - not syncing: BC250 R297 CP05 after PGFSM_CONFIG write before status wait
```

Therefore the first intended VCN MMIO write path executed and returned on the tested BC-250.

This does **not** independently prove register readback/electrical latch, PGFSM transition, VCPU execution, firmware-ready, rings, decode/encode, or VA-API.

## CP06 candidate identity

CP06 source:

```text
research/r297-checkpoint-panic/cp06-v1/vcn_v2_0-r297-cp06.c
SHA-256: 15ae7a736ae5cce2658cf5b304e59bb3895616c0298e15eb9b34ffad1ec85c4a
```

The intended core sequence is:

```c
WREG32_SOC15(VCN, 0, mmUVD_PGFSM_CONFIG, data);

dev_emerg(adev->dev,
          "BC250 R297 CP06: after PGFSM_CONFIG write before single status read\n");

tmp = RREG32_SOC15(VCN, 0, mmUVD_PGFSM_STATUS);

dev_emerg(adev->dev,
          "BC250 R297 CP06: PGFSM_STATUS raw=0x%08x after PGFSM_CONFIG write\n",
          tmp);

panic("BC250 R297 CP06 after single PGFSM_STATUS read");
```

## STATIC / OBJECT / FULLMODULE status

### STATIC

PASS.

Key contract before the deliberate panic:

```text
WREG32_SOC15_COUNT=1
RREG32_SOC15_COUNT=1
WAIT_COUNT=0
WREG32_P_COUNT=0
POWER_STATUS pre-panic references=0
```

Static audit log SHA-256:

`70f8640ee1c7d870e82c3bfab6050b0048458ef5909a002c861216d9a9ab08b`

### OBJECT BUILD-ONLY

PASS.

Object SHA-256:

`70fad7ffa22b5586faa986e06202d0104fe1b80e65701724d88c2a56d356dded`

Object machine audit V2 log SHA-256:

`a3171e02582c8ec20a37dda2823b925d027f5d4797a0d23c4e87de0b96c4ad09`

The machine audit established the WREG -> after-write log -> RREG -> raw-status log -> panic order, zero wait-on-rreg calls, and no executable post-panic wait/power block.

### FULLMODULE BUILD-ONLY

PASS.

```text
amdgpu-r297-cp06.ko.unstripped
SHA-256: c5d1a208256ec95bf79249ae5083d792c63c3d1112032028cb1e6c8f94142d4c

R297_CP06_FULLMODULE_BUILD_V1.log
SHA-256: d087b8ddd3ab93d44b9c9d85832e2318a805b2e0070455d601e5af235b3cbb35
```

### FULLMODULE MACHINE AUDIT V2

PASS.

The earlier V1 failure was a tooling false negative caused by searching the generic string `panic` in an objdump path containing `checkpoint-panic`, rather than locating the panic relocation/call.

V2 fixed this by parsing relocation-aware call records.

Decisive compiled addresses:

```text
SRIOV_WREG_ADDR=0xacb378
DEVICE_WREG_ADDR=0xacb389
AFTER_WRITE_LOG_ADDR=0xacb398
SRIOV_RREG_ADDR=0xacb3d2
DEVICE_RREG_ADDR=0xacb3de
RAW_STATUS_LOG_ADDR=0xacb3ef
PANIC_ADDR=0xacb3fb
```

Contract:

```text
WREG_BOTH_PATHS_REJOIN=YES
RREG_BOTH_PATHS_REJOIN=YES
PGFSM_CONFIG_VALUE_0x55555=YES
POST_PANIC_WAIT_POWER_LINES_ABSENT=YES
PGFSM_STATUS_WAIT_MACHINE_CODE_ABSENT=YES
R297_CP06_FULLMODULE_MACHINE_CODE_CONTRACT=PASS
R297_CP06_FULLMODULE_MACHINE_AUDIT_V2=PASS
```

Machine-audit V2 log SHA-256:

`38647e4183c788da39eab829cfaa491496daf6a705e4012baa723206acdfd61f`

## HOME package

CP06 HOME package V2 = PASS.

```text
package-cp06-home-v2.sh
SHA-256: 6677fb789ae834f61c9e9e5f1062219b1f2b64e7ae873d0d735bb5e547aa1753

amdgpu-r297-cp06-stripped.ko
SHA-256: e77c70a2a64110eb5f64045aeb2828120e394b7bcbed20331733c1aabb6f18c6

amdgpu-r297-cp06-signed.ko
SHA-256: 2944bb21c058e4561fa17d9f49a64d301a8665ab0b455bc49c12b5de30c6bbe8

initramfs-7.2.3-r297-cp06.img
SHA-256: 9bfac31bfa9bd0a1cf44d0afb009a332b8f3c6857312883041917ec6b7010927

R297_CP06_PACKAGE_AUDIT_V2.log
SHA-256: 51d8750862ebb6b757a99f1275649f663b3ae3f23d1d7020edd9ecf384ea64d6
```

The package audit established:

- module signature present and retained;
- signed module `.text` exact to the audited fullmodule;
- CP06 marker contract;
- signed CP06 machine-code contract;
- exact round-trip module and firmware identities;
- no /boot write, no module load, no VCN MMIO, no reboot.

VCN firmware identity remains:

`a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5`

## Privileged preflight

CP06 preflight V2 = PASS.

The V1 preflight stopped because two shell arithmetic blocks used malformed command-substitution syntax. This was tooling-only.

Corrected V2:

```text
preflight-cp06-install-v2.sh
SHA-256: 5067486f885c429491f23349df75d5b0b4d6f0c82f32cba31eead150a4fe9998

bc250-r297-cp06-preinstall-v2.log
SHA-256: db2dc6d7b668569e1abbfe7456923329f3b5d75f7d3d301c37f0755fd9edbb2f
```

Preflight confirmed:

- running known-safe normal kernel `7.2.1-ogc4.1.fc44.x86_64`;
- exact CP06 package identities;
- exact CP05 recovery material;
- exact protected boot artifacts;
- no pending `next_entry`;
- no pending one-shot menu;
- normal runtime EFI pstore policy `Y`;
- enough /boot capacity after retiring CP05.

CP06 BLS candidate SHA-256:

`63d6dc8b849c3e2652de20b37e58a7fdd124f9f53953c0c75df4b4453ecab8d0`

## INSTALL-NO-SELECT

PASS.

```text
install-cp06-no-select.sh
SHA-256: 87b8e5af575edb39f3e83bda2b63795372f553e36f1ab0348e7847a4b300a7b3

stable install log SHA-256:
468719ffb1c50977a9527639c21fff30995fc63e8c4615fca0f2ddd7139e819e
```

Installed identities:

```text
/boot/initramfs-7.2.3-r297-cp06.img
SHA-256: 9bfac31bfa9bd0a1cf44d0afb009a332b8f3c6857312883041917ec6b7010927

/boot/loader/entries/boot-entry-r297-cp06.conf
SHA-256: 63d6dc8b849c3e2652de20b37e58a7fdd124f9f53953c0c75df4b4453ecab8d0
```

The install retired CP05 only because /boot space required it, while preserving CP05 recovery material in HOME.

Boot selection was not changed.

## Installed final audit

PASS.

Installed-final-audit log SHA-256:

`d4c6a97996d50dbe245e62070a7198e94c18fe492d48dd726f561334e65f7277`

The installed initramfs round-trip established exact signed module and firmware identities.

Installed CP06 machine-code contract:

```text
amdgpu_device_wreg=1
amdgpu_sriov_wreg=1
amdgpu_device_rreg=1
amdgpu_sriov_rreg=1
amdgpu_device_wait_on_rreg=0
_dev_emerg=2
panic=1
PGFSM_CONFIG_0x55555_IMMEDIATE_COUNT=2
INSTALLED_CP06_PGFSM_CONFIG_WRITE_REGION=YES
INSTALLED_CP06_SINGLE_STATUS_READ_REGION=YES
INSTALLED_CP06_RAW_STATUS_LOG=YES
INSTALLED_CP06_PANIC_AFTER_RAW_STATUS_LOG=YES
INSTALLED_CP06_WAIT_MACHINE_CODE_ABSENT=YES
INSTALLED_CP06_MACHINE_CODE_CONTRACT=PASS
```

## First CP06 LIVE attempt: unresolved, not a CP06 result

A one-time manual-menu arm was prepared and passed its safety audit.

```text
arm-cp06-manual-menu-v1.sh
SHA-256: aac5de03054bde2f190f0045e11ec87f77b7ba64c308e7c117be33b9c50d39fe

bc250-r297-cp06-manual-menu-arm.log
SHA-256: 8675e4ebf83314978d086ca8a834b3d8703c5e01a11507675954b27c1230c1fd
```

The pstore baseline was cleared and the one-time 30-second menu was armed.

After the attempted boot, the postmortem found:

```text
MENU_SHOW_ONCE_CONSUMED=YES
NEXT_ENTRY_ABSENT=YES
PSTORE_FILE_COUNT=0
CP06_PSTORE_RESULT=NO_PERSISTED_RECORDS
```

Postmortem artifacts:

```text
collect-cp06-postmortem-v2.sh
SHA-256: 36914e6c54ad1e3f461575615f32ec2031165ff787130ecddb7f22c8921f4358

bc250-r297-cp06-live-postmortem-v2.log
SHA-256: aa7b81cbad6f9d210de5200247febec1abf03e8334c4b2c652d750f7edfc9f24
```

This does **not** prove CP06 executed and does **not** prove the `PGFSM_STATUS` read failed.

Scientific classification:

- CP06 STATIC = PASS
- CP06 OBJECT BUILD-ONLY = PASS
- CP06 OBJECT MACHINE AUDIT = PASS
- CP06 FULLMODULE BUILD-ONLY = PASS
- CP06 FULLMODULE MACHINE AUDIT V2 = PASS
- CP06 HOME PACKAGE V2 = PASS
- CP06 PRIVILEGED PREFLIGHT V2 = PASS
- CP06 INSTALL-NO-SELECT = PASS
- CP06 INSTALLED FINAL AUDIT = PASS
- CP06 LIVE = **NOT YET PROVEN / ATTEMPT 1 INCONCLUSIVE / ATTEMPT 2 HARD-HANG WITH NO PERSISTED TRACE**

## SELECT-WITNESS diagnostic

Because the first CP06 LIVE attempt produced no persisted pstore, the next diagnostic is a boot-selection witness, not another VCN experiment.

The witness:

- uses the same research kernel and CP06 initramfs;
- removes `amdgpu` from `rd.driver.pre`;
- adds:
  - `module_blacklist=amdgpu`
  - `rd.driver.blacklist=amdgpu`
  - `modprobe.blacklist=amdgpu`
  - `rd.break=pre-mount`
  - `bc250_cp06_select_witness=1`
- is intended only to prove that the intended BLS entry was selected;
- must not be interpreted as VCN hardware evidence.

An earlier HOME witness lacked `module_blacklist=amdgpu`; this mismatch was explicitly audited.

Conflict audit:

```text
audit-cp06-select-witness-conflict-v1.sh
SHA-256: 19578ca8b6fc5ccac387f3c4a343258690084390cf51461e6326057fd49a0d2e

R297_CP06_SELECT_WITNESS_CONFLICT_AUDIT_V1.log
SHA-256: 0edc8eb02cd706d0ead99473142a20f000ab4c08665cb467dbaff0b22ee98959
```

The old witness was preserved:

`4fc5b0d98c4612642463b39a9c0ad347abb88739d312458a32f702566fa9fe2a`

The stronger active HOME witness is:

`ad6fe52270cea2786e643c2cd126c045b7fdba275333e05cb12eebd84a90be3b`

Resolution artifacts:

```text
resolve-cp06-select-witness-v1.sh
SHA-256: f9918e9f0cbe3bd913e97ecc19019981c4e5204b31a54d8c8ba33fbf24c5184d

R297_CP06_SELECT_WITNESS_RESOLUTION_V1.log
SHA-256: 048b81a711e5a57b6565485da92db975459d4bfcf08398423eddbf085adc7127
```

The stronger witness was then installed as a BLS-only addition without selecting it:

```text
/boot/loader/entries/boot-entry-r297-cp06-select-witness.conf
SHA-256: ad6fe52270cea2786e643c2cd126c045b7fdba275333e05cb12eebd84a90be3b

install-cp06-select-witness-no-select-v1.sh
SHA-256: df12e5cb8ae12e2f1caf36fcee5f541ecb859aec4799a1bcdc053a38c1c99b7e

bc250-r297-cp06-select-witness-install-no-select.log
SHA-256: 2d824cd910c6374d5dcff37aca0c6ca9bc20658d946f435d6218e6669eb60ff0
```

The install audit established:

```text
BOOT_WRITE_SCOPE=BLS_ONLY
INITRAMFS_WRITE=NO
KERNEL_WRITE=NO
MAIN_CP06_BLS_WRITE=NO
BOOT_SELECTION_CHANGE=NO
NEXT_ENTRY_CHANGE=NO
MENU_SHOW_ONCE_CHANGE=NO
MODULE_LOAD=NO
HARDWARE_ACCESS=NO
VCN_MMIO_ACCESS=NO
REBOOT=NO
GRUBENV_BYTE_EXACT=YES
```

Current boot-selection state after witness installation remained:

```text
boot_success=1
next_entry absent
menu_show_once_timeout absent
pstore_disable=Y
```

## SELECT-WITNESS LIVE result

The installed `SELECT-WITNESS no-amdgpu` entry was manually selected and stopped at the intended `rd.break=pre-mount` boundary.

Observed from the dracut shell:

- `/proc/cmdline` contained:
  - `module_blacklist=amdgpu`
  - `rd.driver.blacklist=amdgpu`
  - `modprobe.blacklist=amdgpu`
  - `rd.break=pre-mount`
  - `bc250_cp06_select_witness=1`
- the kernel image was the research kernel path;
- `grep '^amdgpu ' /proc/modules` returned no match.

After forced return to normal Bazzite, the one-time menu state was consumed and the normal pstore runtime policy was restored.

Scientific classification:

- CP06 SELECT-WITNESS LIVE = **PASS**
- this proves the intended witness BLS can be manually selected and reaches its early dracut witness point;
- it does **not** prove any CP06 VCN MMIO execution.

## CP06 LIVE attempt 2: hard-hang observation, no persisted pstore

After the selection witness succeeded, a second main-CP06 manual-menu attempt was prepared with a clean pstore baseline.

Attempt-2 arm identities:

```text
arm-cp06-live-attempt2-menu-v1.sh
SHA-256: 1bb0ba3ee2ab5e33ab5f86c86bb17b3a5d9413db9ff841a791af5ce5ec8f8542

bc250-r297-cp06-attempt2-arm.log
SHA-256: 8f27716b4989497deceafbf76f0d1150b16d0d8a91dd9b59662430be4789fe21
```

The user manually selected the main CP06 entry. The display blacked out and the machine did not automatically recover; a forced power-button recovery was required.

Postmortem:

```text
MENU_SHOW_ONCE_CONSUMED=YES
NEXT_ENTRY_ABSENT=YES
PSTORE_FILE_COUNT=0

R274B_COUNT=0
P1_COUNT=0
HELPER_COUNT=0
GUARDS_COUNT=0
AFTER_WRITE_COUNT=0
RAW_STATUS_COUNT=0
CP06_PANIC_COUNT=0
KERNEL_PANIC_COUNT=0

CP06_ATTEMPT2_PSTORE_RESULT=NO_PERSISTED_RECORDS
```

Current-boot reset-reason evidence after recovery included:

```text
Previous system reset reason [0x40080402]: power button was pressed for 4 seconds
Previous system reset reason [0x40080402]: software wrote 0x6 to reset control register 0xCF9
Previous system reset reason [0x40080402]: a parity error occurred
```

Attempt-2 collection log SHA-256:

`e2b63cfc392f3d915ebe8e4545e589ba5759d21cd02c31f0e8caceb2e6baec31`

Classification:

- CP06 attempt 2 = **LIVE hard-hang observation / NO PERSISTED TRACE**
- this is stronger than the first attempt operationally because manual BLS selection had already been independently validated;
- however, absence of pstore means the exact executed boundary is still unproven;
- do **not** claim that the single `PGFSM_STATUS` read executed, returned, or caused the hang.

The direct single-read candidate is therefore no longer worth rerunning unchanged. The next diagnostic should add an independently recoverable witness around the read, for example by moving the MMIO read to a worker context while another CPU retains a timeout/panic path. That design must first be STATIC/BUILD-ONLY audited before any new LIVE run.

## Current scientific boundary

The strongest direct VCN-path LIVE statement remains CP05:

> the first intended VCN MMIO write path executed and returned.

CP06 adds a completely audited and installed single-status-read candidate, but there is not yet LIVE evidence that its read executed or returned.

Therefore do **not** claim any value for `PGFSM_STATUS` yet.

Also still unproven:

- PGFSM transition;
- UVD power-island state;
- `UVD_POWER_STATUS`;
- reset release attributable to this path;
- VCPU firmware execution;
- firmware-ready;
- rings;
- decode/encode;
- VA-API.

## Next safe direction

The manual BLS-selection mechanism is now independently proven by the SELECT-WITNESS LIVE PASS, and the unchanged main CP06 candidate has subsequently hard-hung twice without a persisted pstore trace.

Do **not** repeat the unchanged direct-read CP06 boot.

The next stage should remain STATIC/READ-ONLY first:

1. verify the research kernel was built with hard-lockup/NMI watchdog support and confirm the relevant kernel parameters are available;
2. if supported, prepare a BLS-only diagnostic variant that keeps the exact same CP06 initramfs/module but adds bounded hard-lockup panic parameters;
3. audit that BLS variant without selecting it;
4. only after that audit consider one LIVE diagnostic run.

If the watchdog diagnostic can panic and persist a stack while the status read is stalled, it can distinguish a CPU-local MMIO stall from a wider fabric/system hang without yet changing the CP06 machine-code body.


## 2026-10-03 update — SELECT-WITNESS LIVE proved; CP06 attempt 2 still no pstore

The manual-selection witness was executed successfully before the second main CP06 retry.

At the dracut `rd.break=pre-mount` emergency shell, the selected kernel command line visibly contained:

```text
module_blacklist=amdgpu
rd.driver.blacklist=amdgpu
modprobe.blacklist=amdgpu
rd.break=pre-mount
bc250_cp06_select_witness=1
```

and an explicit initramfs check reported no loaded amdgpu module.

Therefore:

```text
CP06 SELECT-WITNESS LIVE = PASS
```

This proves the manual GRUB/BLS selection mechanism can reach the intended research entry. It is selection-path evidence only and is not VCN hardware evidence.

A second main CP06 LIVE attempt was then prepared with a clean EFI pstore baseline and the main CP06 BLS. The postmortem collection again found:

```text
PSTORE_FILE_COUNT=0
R274B_COUNT=0
P1_COUNT=0
HELPER_COUNT=0
GUARDS_COUNT=0
AFTER_WRITE_COUNT=0
RAW_STATUS_COUNT=0
CP06_PANIC_COUNT=0
KERNEL_PANIC_COUNT=0
CP06_ATTEMPT2_PSTORE_RESULT=NO_PERSISTED_RECORDS
```

The following normal boot reported previous reset reason `0x40080402`, including:

```text
power button was pressed for 4 seconds
software wrote 0x6 to reset control register 0xCF9
a parity error occurred
```

Attempt-2 collection log:

```text
bc250-r297-cp06-attempt2-live-collect.log
```

The second attempt therefore remains **LIVE INCONCLUSIVE**. It does not establish a `PGFSM_STATUS` value and does not independently prove that the status read executed. However, because SELECT-WITNESS LIVE independently proved the manual-selection path, simple menu/BLS-selection failure is now a weaker explanation than before.

A useful next discriminating control is a new read-only checkpoint that performs exactly one `PGFSM_STATUS` read **without** the preceding `PGFSM_CONFIG` write, then logs the raw value and panics. This can distinguish a read-path problem from a write-then-read interaction. It must first pass STATIC / BUILD-ONLY / package / install audit before any LIVE use.
