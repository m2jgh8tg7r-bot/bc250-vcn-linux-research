# ChatGPT handoff — R297 CP06 checkpoint

Date: 2026-10-03 JST

## Current headline

The R297 checkpoint sequence has advanced from CP05 LIVE proof of the first intended VCN MMIO write to a fully audited CP06 candidate that adds exactly one `PGFSM_STATUS` read.

**CP05 LIVE = PASS.**

**CP06 pre-LIVE chain = PASS through installed-final-audit.**

**CP06 LIVE = not yet proven.**

The first CP06 boot attempt produced no persisted EFI pstore records, so it must not be classified as either a CP06 hardware PASS or a PGFSM read failure.

The stronger `SELECT-WITNESS no-amdgpu` BLS diagnostic has now been selected successfully and reached its intended early dracut witness point. A subsequent main-CP06 attempt blacked out/hard-hung and required forced power-button recovery, but produced no persisted pstore.

## Exact current classifications

```text
CP04 LIVE                            = PASS
CP05 LIVE                            = PASS
CP06 STATIC                          = PASS
CP06 OBJECT BUILD-ONLY               = PASS
CP06 OBJECT MACHINE AUDIT            = PASS
CP06 FULLMODULE BUILD-ONLY           = PASS
CP06 FULLMODULE MACHINE AUDIT V2     = PASS
CP06 HOME PACKAGE V2                 = PASS
CP06 PRIVILEGED PREFLIGHT V2         = PASS
CP06 INSTALL-NO-SELECT               = PASS
CP06 INSTALLED FINAL AUDIT           = PASS
CP06 FIRST LIVE ATTEMPT              = INCONCLUSIVE
CP06 SELECT-WITNESS HOME             = PASS
CP06 SELECT-WITNESS BLS INSTALL      = PASS
CP06 SELECT-WITNESS LIVE             = PASS
CP06 SECOND MAIN LIVE ATTEMPT         = HARD-HANG OBSERVED / NO PSTORE
```

## Strongest LIVE result

The strongest verified hardware-path boundary is still CP05.

```text
BC250 R291P1 pre_reset: begin
BC250 R297 CP05: helper_entry before guards
BC250 R297 CP05: guards_pass before PGFSM_CONFIG
BC250 R297 CP05: after PGFSM_CONFIG write before status wait
Kernel panic - not syncing: BC250 R297 CP05 after PGFSM_CONFIG write before status wait
```

Interpretation:

- first intended VCN MMIO write path executed;
- WREG returned;
- post-write checkpoint reached.

Do not strengthen this into proof of register latch/readback, PGFSM transition, VCN power-up, VCPU, firmware-ready, rings, decode/encode, or VA-API.

## CP06 design

The CP06 candidate performs:

```text
PGFSM_CONFIG write 0x55555
-> after-write log
-> exactly one PGFSM_STATUS read
-> raw status log
-> panic
```

No wait-on-rreg survives in the audited machine code, and no pre-panic `UVD_POWER_STATUS` path is part of the candidate.

Source SHA-256:

`15ae7a736ae5cce2658cf5b304e59bb3895616c0298e15eb9b34ffad1ec85c4a`

Fullmodule SHA-256:

`c5d1a208256ec95bf79249ae5083d792c63c3d1112032028cb1e6c8f94142d4c`

Fullmodule machine-audit V2 log SHA-256:

`38647e4183c788da39eab829cfaa491496daf6a705e4012baa723206acdfd61f`

## CP06 installed artifacts

Signed module:

`2944bb21c058e4561fa17d9f49a64d301a8665ab0b455bc49c12b5de30c6bbe8`

Installed initramfs:

`9bfac31bfa9bd0a1cf44d0afb009a332b8f3c6857312883041917ec6b7010927`

Installed main BLS:

`63d6dc8b849c3e2652de20b37e58a7fdd124f9f53953c0c75df4b4453ecab8d0`

Installed-final-audit log:

`d4c6a97996d50dbe245e62070a7198e94c18fe492d48dd726f561334e65f7277`

Research kernel:

`c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6`

VCN firmware:

`a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5`

## First CP06 LIVE attempt

Manual-menu arm was prepared correctly and the pstore baseline was cleared.

After the attempted selection/reboot, postmortem showed:

```text
MENU_SHOW_ONCE_CONSUMED=YES
NEXT_ENTRY_ABSENT=YES
PSTORE_FILE_COUNT=0
CP06_PSTORE_RESULT=NO_PERSISTED_RECORDS
```

Postmortem log SHA-256:

`aa7b81cbad6f9d210de5200247febec1abf03e8334c4b2c652d750f7edfc9f24`

This is selection/boot ambiguity, not evidence that the CP06 status read returned any specific value.

## SELECT-WITNESS state

The current diagnostic BLS is designed only to prove manual selection.

Installed witness:

`/boot/loader/entries/boot-entry-r297-cp06-select-witness.conf`

SHA-256:

`ad6fe52270cea2786e643c2cd126c045b7fdba275333e05cb12eebd84a90be3b`

Its important option changes are:

```text
rd.driver.pre=realtek,r8169
module_blacklist=amdgpu
rd.driver.blacklist=amdgpu
modprobe.blacklist=amdgpu
rd.break=pre-mount
bc250_cp06_select_witness=1
```

The previous weaker HOME witness lacked `module_blacklist=amdgpu`; it was preserved at SHA-256:

`4fc5b0d98c4612642463b39a9c0ad347abb88739d312458a32f702566fa9fe2a`

Resolution log SHA-256:

`048b81a711e5a57b6565485da92db975459d4bfcf08398423eddbf085adc7127`

Witness install log SHA-256:

`2d824cd910c6374d5dcff37aca0c6ca9bc20658d946f435d6218e6669eb60ff0`

The witness was installed BLS-only with:

```text
BOOT_SELECTION_CHANGE=NO
NEXT_ENTRY_CHANGE=NO
MENU_SHOW_ONCE_CHANGE=NO
GRUBENV_BYTE_EXACT=YES
```

## SELECT-WITNESS LIVE result

The witness was manually selected successfully.

At the `rd.break=pre-mount` dracut shell:

- the command line contained the select-witness marker and all three amdgpu blacklist forms;
- `amdgpu` was not present in `/proc/modules`;
- the one-time menu state was later consumed cleanly after returning to normal Bazzite.

Therefore:

```text
CP06 SELECT-WITNESS LIVE = PASS
```

This is boot-selection evidence only, not VCN execution evidence.

## Main CP06 attempt 2

After the selection mechanism had been independently witnessed, the main CP06 BLS was retried with a clean pstore baseline.

Observed behavior:

- user manually selected the main CP06 entry;
- display blacked out;
- no automatic panic/reboot was observed;
- forced 4-second power-button recovery was required;
- the one-time menu state was consumed;
- postmortem found zero persisted pstore files and zero CP06 markers.

Classification:

```text
CP06 main attempt 2 = LIVE hard-hang observation
persisted pstore     = NONE
exact hang boundary  = UNPROVEN
```

Do not state that `PGFSM_STATUS` read is proven to be the cause. The CP05 -> CP06 delta makes that read a strong suspect, but the current evidence is still an inference.

Attempt-2 collection log SHA-256:

`e2b63cfc392f3d915ebe8e4545e589ba5759d21cd02c31f0e8caceb2e6baec31`

## Required next-step discipline

Do not repeat the unchanged direct-read CP06 LIVE attempt. Two main attempts have produced no persisted pstore, and attempt 2 was an observed hard hang after boot-selection ambiguity had already been removed.

The next experiment should first be designed and audited as STATIC/BUILD-ONLY. A preferred direction is to execute the single status read in a worker context while a separate CPU retains a bounded timeout/panic path. This can distinguish: read returns; one CPU stalls while the system remains recoverable; or the read stalls the wider fabric/system. No new LIVE run should occur before that design has passed source/object/fullmodule machine-code audit.

## Important tooling lessons retained

1. Do not search generic `panic` text in objdump output when the path itself contains `checkpoint-panic`; parse the relocation/call record.
2. Do not use destructive/ambiguous objcopy forms against the signed input module; extract `.text` to an explicit output file and confirm the signed ELF hash/signature is unchanged.
3. Under `set -o pipefail`, avoid `strings ... | grep -q` for large files because upstream SIGPIPE can produce false failure; materialize strings first.
4. Shell arithmetic must use `$(( ... ))`, not command substitution around a parenthesized expression.
5. Do not place a bare `exit` directly into the interactive shell. Any `exit` belongs inside a generated script; invoke it from an outer `set +e` shell and always print terminal-survival status.

## Evidence-class boundary

- source/object/fullmodule/package/installed audits: STATIC / BUILD-ONLY / INSTALL evidence
- CP05 pstore checkpoint: LIVE
- CP06 first attempt: LIVE attempt, scientifically INCONCLUSIVE
- SELECT-WITNESS preparation/install: STATIC / INSTALL
- SELECT-WITNESS execution: LIVE PASS
- CP06 main attempt 2: LIVE hard-hang observation, no persisted trace, exact MMIO boundary unresolved

Full detailed checkpoint:

`research/r297/RESULT_CP06_PROGRESS.md`
