# R297 CP06 LIVE attempt — postmortem result

Date: 2026-10-02/03 JST

## Classification

- CP06 STATIC: PASS
- CP06 OBJECT BUILD-ONLY: PASS
- CP06 OBJECT MACHINE AUDIT: PASS
- CP06 FULLMODULE BUILD-ONLY: PASS
- CP06 FULLMODULE MACHINE AUDIT V2: PASS
- CP06 HOME PACKAGE V2: PASS
- CP06 PRIVILEGED PREFLIGHT V2: PASS
- CP06 INSTALL-NO-SELECT: PASS
- CP06 INSTALLED FINAL AUDIT: PASS
- CP06 LIVE ATTEMPT: EXECUTED
- CP06 LIVE PSTORE: NO PERSISTED RECORDS
- CP06 PGFSM_STATUS raw value: NOT OBSERVED
- CP06 panic-after-read: NOT OBSERVED
- Hard hang at/around the first PGFSM_STATUS read: SUSPECTED, NOT PROVEN

## Intended CP06 boundary

The installed machine-code contract was audited as:

1. one PGFSM_CONFIG write region with value 0x55555
2. after-write emergency log
3. one PGFSM_STATUS read region
4. raw-status emergency log
5. panic
6. no wait_on_rreg machine code before panic
7. no POWER_STATUS access before panic

Installed module machine-code audit:

- amdgpu_device_wreg=1
- amdgpu_sriov_wreg=1
- amdgpu_device_rreg=1
- amdgpu_sriov_rreg=1
- amdgpu_device_wait_on_rreg=0
- _dev_emerg=2
- panic=1
- PGFSM_CONFIG immediate 0x55555 count=2
- machine-code contract=PASS

## Fixed artifact identities

- CP06 source SHA256:
  `15ae7a736ae5cce2658cf5b304e59bb3895616c0298e15eb9b34ffad1ec85c4a`
- CP06 fullmodule SHA256:
  `c5d1a208256ec95bf79249ae5083d792c63c3d1112032028cb1e6c8f94142d4c`
- CP06 signed module SHA256:
  `2944bb21c058e4561fa17d9f49a64d301a8665ab0b455bc49c12b5de30c6bbe8`
- CP06 initramfs SHA256:
  `9bfac31bfa9bd0a1cf44d0afb009a332b8f3c6857312883041917ec6b7010927`
- CP06 BLS SHA256:
  `63d6dc8b849c3e2652de20b37e58a7fdd124f9f53953c0c75df4b4453ecab8d0`
- VCN firmware SHA256:
  `a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5`
- Installed final-audit log SHA256:
  `d4c6a97996d50dbe245e62070a7198e94c18fe492d48dd726f561334e65f7277`
- Manual-menu arm log SHA256:
  `8675e4ebf83314978d086ca8a834b3d8703c5e01a11507675954b27c1230c1fd`
- LIVE collection V1 script SHA256:
  `01f1346cc6e449d525e2ab5dbb856fef05b4ae1c48646dafb357f8457acc87b7`
- LIVE collection V1 log SHA256:
  `a12cc0a881af49d90032be3546220416d58a82b00d152ec7ff05ac837e6c4a01`
- Postmortem V2 script SHA256:
  `36914e6c54ad1e3f461575615f32ec2031165ff787130ecddb7f22c8921f4358`
- Postmortem V2 log SHA256:
  `aa7b81cbad6f9d210de5200247febec1abf03e8334c4b2c652d750f7edfc9f24`

## LIVE observation

The one-time 30-second GRUB menu was armed successfully with no `next_entry`.
The user manually selected CP06.

Observed behavior:

- display blacked out
- system did not proceed to the expected visible panic/reboot behavior
- after waiting well beyond the intended panic timeout, manual recovery/reset was required
- the machine returned to the known-safe Bazzite kernel

After recovery:

- `menu_show_once_timeout` was consumed
- `next_entry` was absent
- CP06 installed image/BLS identities remained exact
- EFI pstore was exposed and contained zero files

Postmortem machine classification:

```text
CP06_HELPER_COUNT=0
CP06_GUARDS_COUNT=0
CP06_AFTER_WRITE_COUNT=0
CP06_RAW_STATUS_COUNT=0
CP06_CP06_PANIC_COUNT=0
CP06_KERNEL_PANIC_COUNT=0
CP06_PSTORE_RESULT=NO_PERSISTED_RECORDS
```

Therefore there is no persisted evidence that the CP06 helper-entry, guards-pass,
after-write, raw-status, or panic checkpoints reached durable storage during this boot.

## Reset-reason note

The subsequent safe boot reported:

```text
Previous system reset reason [0x40080400]:
  software wrote 0x6 to reset control register 0xCF9
  a parity error occurred
```

The same reset-reason text is also present on earlier normal/safe boots, so it is
**not CP06-specific evidence** and must not be used to localize the failure.

## Scientific interpretation

CP05 previously proved that the first intended VCN MMIO PGFSM_CONFIG write path
executed and returned, with a durable pstore panic checkpoint immediately after
that write.

CP06 added a single PGFSM_STATUS read after the same intended write, followed by
a raw-value log and panic. The user-observed hard stop plus the complete absence
of a CP06 panic/pstore record is consistent with a hard hang at or around that
read. However, because no CP06 checkpoint was durably recorded, the exact fault
boundary is not proven.

Do **not** claim:

- PGFSM_STATUS value was read
- PGFSM_STATUS read definitely caused the hang
- VCN power island woke
- VCPU executed
- firmware became ready
- rings worked
- decode/encode worked
- VA-API worked

## Recommended next experiment

Do not simply repeat CP06.

Use a paired control design that keeps helper structure/layout as similar as
practical:

- control variant: same path through PGFSM_CONFIG write and after-write log,
  then panic immediately before any PGFSM_STATUS read
- read variant: same control structure plus exactly one PGFSM_STATUS read,
  raw-status log, then panic

Prefer explicit noinline/helper-shape control so the comparison is not confounded
by CP05/CP06 inlining differences.

Run STATIC and BUILD-ONLY audits for both variants before any further LIVE test.
