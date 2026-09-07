# Research log

This is a condensed public milestone log. Stage numbers are preserved because they make cross-reference with private working notes easier, but parser/build/script failures are not represented as hardware failures.

## R73-R75 — stock Cyan VCN power-route closure

Static tracing showed that the stock Cyan path does not expose a proven whole-block VCN power-on route. A generic software power request can return success without establishing a hardware transition.

Public boundary retained:

```text
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
```

## R77 — real VCN software lifecycle

A quarantined custom amdgpu reached real VCN `early_init`, `sw_init`, and `sw_fini`. Firmware acquisition and software ring registration were allowed, while hardware callbacks remained guarded.

This established a controlled software bring-up point without claiming VCN execution.

## R79 — Cyan PSP VCN enrollment quarantine

Automatic Cyan VCN PSP firmware enrollment was suppressed. This separated VCN software initialization from PSP-mediated firmware transfer/execution and enabled later hardware-boundary work without silently starting the VCN VCPU.

## R84-R85 — live software-init confirmation / next boundary

The quarantined build was booted successfully and the expected VCN software lifecycle was observed live. The next hardware boundary was then defined rather than immediately allowing ring execution.

## R86-R89 — exact NBIO doorbell route

The VCN doorbell route was traced through the stock NBIO implementation to `BIF_MMSCH0_DOORBELL_RANGE`.

Important result:

```text
logical dword offset = 0x00000ef3
logical byte offset  = 0x00003bcc
```

The byte offset was explicitly distinguished from an absolute BAR physical address.

## R90-R96 — single-read probe construction and boot preparation

A function-scoped, kernel-controlled, single-read experiment was built and audited. The boot path used a manual-only experimental entry and avoided automatic selection.

## R97 — first live NBIO hardware observation

A single live read of `0x00000ef3` returned:

```text
0x00000000
```

No write, VCN-core MMIO, raw SMU command, VCPU execution, or ring execution occurred.

Classification:

```text
LIVE_SINGLE_NBIO_READ_PASS_ZERO_VALUE
```

## R99-R101 — bounded transaction design

A one-shot write/read/restore transaction was designed around the observed zero value. It required a fresh same-boot read and stopped with zero writes if the value was not zero.

The intended target encoding was `0x00080c40`.

## R100 — pre-hardening implementation, later superseded

An initial source implementation placed logging between target readback and restoration. No live write was ultimately executed with this artifact.

Later review determined that this ordering unnecessarily increased risk. The artifact was quarantined and marked **superseded / do not use**.

## R107 — immediate-rollback safety hardening

The helper was redesigned so that:

- normal restore follows target readback immediately,
- no logging occurs between target readback and normal restore,
- emergency restore is the first executable action in the mismatch branch,
- no target retry loop exists,
- outcome logging occurs only after restoration attempts.

This was audited statically before build or boot.

## R108-R109 — hardened build and independent artifact audit

The hardened module was built against the exact kernel ABI, checked for missing imports, embedded into a HOME-built initramfs, and independently audited for source identity, helper ordering, firmware identity, and initramfs composition.

## R110-R112 — manual boot artifact and boot-selection diagnosis

A manual-only hardened boot artifact was installed. Two intended live attempts returned to the stock entry without executing the probe.

This was classified as a boot-selection/resolution problem, not a hardware failure.

A read-only GRUB/BLS audit proved that the hardened BLS existed in the active loader path and that `blscfg` was active.

A harmless stock-kernel sentinel BLS with a unique command-line token was then created and manually selected. Its token reached `/proc/cmdline`, proving that manual BLS selection worked end-to-end.

## R112D — unambiguous R113 live-entry rearm

A new manual-only hardened BLS was created with a unique command-line token. Existing boot artifacts were kept byte-identical and automatic selection remained disabled.

## R113 — bounded live NBIO write/read/restore success

The dedicated hardened entry was confirmed after boot by both its unique command-line token and the expected custom amdgpu Build ID.

Physical-hardware result:

```text
fresh old       = 0x00000000
target write     = 0x00080c40
target readback  = 0x00080c40
restore           = 0x00000000
restore readback  = 0x00000000
```

The original value was restored exactly. Emergency restore was not required.

This proves the bounded NBIO register path is live and writable/readable on the tested BC-250.

It does not prove VCN power, VCPU execution, ring execution, or decode/encode functionality.

## R114A — live-entry quarantine

After the successful R113 experiment, the dedicated live BLS was removed and the boot environment returned to a non-live state. No additional NBIO/VCN/SMU operation occurred during quarantine.

## R114B — stock recovery closure

The system was rebooted through the ordinary stock Bazzite/OSTree entry. The R113-specific command-line token and experimental boot path were absent, and the loaded amdgpu GNU build ID matched the known stock module:

```text
2da61adf20c29bf978a05facfb74130c81179faa
```

Classification:

```text
R114B_RESULT=STOCK_RECOVERY_FULL_PASS
```

This closes the R113 live-test sequence without carrying the experimental amdgpu module into the next research stage.

## Current research direction

The next major problem is not the NBIO doorbell-range transaction itself. It is identifying and minimally proving the actual VCN power/liveness condition before authorizing firmware/VCPU or ring execution.

External SMU/domain-6 research is being used as static comparison material, but invasive external tooling is not treated as locally reproduced or automatically safe.
