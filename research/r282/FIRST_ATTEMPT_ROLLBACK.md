# R282 — first install attempt rolled back by shell-pipeline cleanup bug

Date: 2026-10-01

## What happened

The R282 install itself completed and all install/post-install checks passed:

- R281 image identity matched before install.
- 7.2.3 kernel identity matched.
- R180 recovery image/entry and Bazzite entries passed precheck.
- loader and loader.1 entries were the same underlying directory.
- no pending next_entry existed.
- space check passed.
- installed /boot image hash matched the R281 image exactly.
- installed BLS entry matched the local generated entry.
- grub.cfg, grubenv, Bazzite entries and R180 entry hashes were unchanged.
- R180 recovery and Bazzite entries remained present.
- the script printed R282_INSTALL=PASS.

Immediately after that, the EXIT trap printed:

```text
=== ROLLBACK OF R282-CREATED FILES ===
ROLLBACK_COMPLETED=YES
```

## Root cause

The main body was executed as the left side of:

```sh
{ ... } 2>&1 | tee "$OUT"
```

In Bash, the left pipeline component runs in a subshell in the normal configuration. Therefore `SUCCESS=1` was assigned in that subshell, while the parent shell's `SUCCESS` remained 0.

When the parent shell exited, its EXIT trap saw `SUCCESS=0` and removed the R282-created image and BLS entry.

This is an installer-script control-flow bug, not an artifact failure or boot-policy failure.

## Evidence classification

Transient install before rollback:

```text
R282_TRANSIENT_INSTALL=PROVEN
INSTALLED_IMAGE_HASH_MATCH=PROVEN
INSTALLED_ENTRY_MATCH=PROVEN
BOOT_POLICY_UNCHANGED_DURING_INSTALL=PROVEN
R180_RECOVERY_PRESERVED_DURING_INSTALL=PROVEN
BAZZITE_ENTRIES_PRESERVED_DURING_INSTALL=PROVEN
```

Persistent post-command installation:

```text
R282_PERSISTENT_INSTALL=NOT_PROVEN
EXPECTED_STATE=ROLLED_BACK
```

No boot selection, module load, or reboot occurred.

## Correction

Do not use a pipeline around the stateful installer body.

A corrected installer should attach tee with process substitution, for example:

```sh
exec > >(tee "$OUT") 2>&1
```

so SUCCESS and CREATED_* state remain in the same shell that owns the EXIT trap.

Before retrying, perform a read-only check that the R282 image/BLS entry are absent and that R180/Bazzite recovery state remains intact.
