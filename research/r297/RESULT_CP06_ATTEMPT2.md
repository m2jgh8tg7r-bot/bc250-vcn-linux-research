# R297 CP06 LIVE attempt 2 — no persisted pstore, exact MMIO boundary unresolved

Date: 2026-10-03 JST

Status: **LIVE ATTEMPT / INCONCLUSIVE**

## Context

CP06 is the minimal checkpoint after CP05.

CP05 already proved on BC-250 LIVE hardware that the first intended VCN MMIO write path executed and returned:

```text
BC250 R291P1 pre_reset: begin
BC250 R297 CP05: helper_entry before guards
BC250 R297 CP05: guards_pass before PGFSM_CONFIG
BC250 R297 CP05: after PGFSM_CONFIG write before status wait
Kernel panic - not syncing: BC250 R297 CP05 after PGFSM_CONFIG write before status wait
```

CP06 changes the body only by adding one `PGFSM_STATUS` read after the already-proven
`PGFSM_CONFIG = 0x55555` write, logging the raw value, and panicking immediately.

The installed CP06 machine-code audit established:

```text
amdgpu_device_wreg=1
amdgpu_sriov_wreg=1
amdgpu_device_rreg=1
amdgpu_sriov_rreg=1
amdgpu_device_wait_on_rreg=0
_dev_emerg=2
panic=1
PGFSM_CONFIG_0x55555_IMMEDIATE_COUNT=2
INSTALLED_CP06_MACHINE_CODE_CONTRACT=PASS
```

## Selection-path control

Before attempt 2, a separate SELECT-WITNESS entry was used to remove the earlier
manual-selection ambiguity.

The witness used:

```text
module_blacklist=amdgpu
rd.driver.blacklist=amdgpu
modprobe.blacklist=amdgpu
rd.break=pre-mount
bc250_cp06_select_witness=1
```

and reached the intended early dracut witness point.

Scientific classification:

```text
CP06 SELECT-WITNESS LIVE = PASS
```

This is boot-selection evidence only, not VCN execution evidence.

## Attempt-2 preparation

The main CP06 BLS was then armed again with a clean EFI pstore baseline.

Arm script SHA-256:

`1bb0ba3ee2ab5e33ab5f86c86bb17b3a5d9413db9ff841a791af5ce5ec8f8542`

Arm log SHA-256:

`8f27716b4989497deceafbf76f0d1150b16d0d8a91dd9b59662430be4789fe21`

Installed CP06 artifacts remained fixed:

```text
initramfs SHA-256:
9bfac31bfa9bd0a1cf44d0afb009a332b8f3c6857312883041917ec6b7010927

BLS SHA-256:
63d6dc8b849c3e2652de20b37e58a7fdd124f9f53953c0c75df4b4453ecab8d0

research kernel SHA-256:
c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6

installed-final-audit SHA-256:
d4c6a97996d50dbe245e62070a7198e94c18fe492d48dd726f561334e65f7277
```

## LIVE observation

The main CP06 entry was manually selected.

Observed behavior:

- display blacked out;
- no automatic panic/reboot was observed;
- forced recovery was required.

After returning to the normal Bazzite kernel, the one-time menu state had been consumed:

```text
boot_success=1
MENU_SHOW_ONCE_CONSUMED=YES
NEXT_ENTRY_ABSENT=YES
```

EFI pstore was exposed and contained zero persisted records:

```text
PSTORE_FILE_COUNT=0
```

The machine classification therefore had no CP06 markers:

```text
R274B_COUNT=0
P1_COUNT=0
HELPER_COUNT=0
GUARDS_COUNT=0
AFTER_WRITE_COUNT=0
RAW_STATUS_COUNT=0
CP06_PANIC_COUNT=0
KERNEL_PANIC_COUNT=0

CP06_ATTEMPT2_PSTORE_RESULT=NO_PERSISTED_RECORDS
CP06_ATTEMPT2_MACHINE_CLASSIFICATION=PASS
```

The following normal boot reported previous reset reason `0x40080402`, including:

```text
power button was pressed for 4 seconds
software wrote 0x6 to reset control register 0xCF9
a parity error occurred
```

Attempt-2 collection log SHA-256:

`e2b63cfc392f3d915ebe8e4545e589ba5759d21cd02c31f0e8caceb2e6baec31`

## Scientific interpretation

What is proven:

- the second main CP06 attempt was made after the manual BLS-selection path had
  independently been witnessed;
- the attempt resulted operationally in a black-screen/hard-hang state requiring
  forced recovery;
- no EFI pstore record from that attempt persisted.

What is **not** proven:

- that execution reached the CP06 helper;
- that the CP06 `PGFSM_CONFIG` write executed in attempt 2;
- that the single `PGFSM_STATUS` read executed;
- that the read returned;
- that the read itself caused the hang;
- any raw `PGFSM_STATUS` value;
- PGFSM transition;
- VCN power-island state;
- VCPU execution;
- firmware-ready;
- rings;
- decode/encode;
- VA-API.

Therefore the exact classification is:

```text
CP06 LIVE ATTEMPT 2 = INCONCLUSIVE
OBSERVED BEHAVIOR    = HARD-HANG / BLACKOUT
PERSISTED TRACE      = NONE
PGFSM_STATUS VALUE   = NOT PROVEN
```

## Next discriminating checkpoint

Do not rerun the unchanged CP06 direct write-then-read experiment.

The next minimal diagnostic should be staged STATIC / BUILD-ONLY first and separate
the two operations:

```text
single PGFSM_STATUS read
without preceding PGFSM_CONFIG write
-> raw-value log
-> intentional panic
```

This read-only control can discriminate a basic status-read-path problem from a
write-then-read interaction. It must not be promoted to LIVE until source/object/
fullmodule/package/install audits pass.
