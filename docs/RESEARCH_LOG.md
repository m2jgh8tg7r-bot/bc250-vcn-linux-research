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

## R115A-R115B — BC-250 SMN transport preflight

Static comparison with public BC-250 SMU tooling identified the board-specific SMN transport as the root-complex PCI configuration pair `0xB8/0xBC`, rather than assuming equivalence with a generic AMD SMN helper.

The local `0000:00:00.0` function was confirmed as the AMD Ariel Root Complex. Passive reads then showed known BC-250 SMU mailbox addresses left in config dword `0xB8`, including queue-0 argument and response addresses.

Because the installed `cyan-skillfish-governor-smu` v0.4.12 uses the same `0xB8/0xBC` transport, it was temporarily stopped before an active selector test. With the governor inactive, the passive pair remained stable for five one-second samples:

```text
B8 = 0x03b10a68
BC = 0x00000001
```

No domain-6, VCN-core, or SMU mailbox command was issued during this preflight.

## R115C — bounded local SMN transport proof

A single locked selector/read/restore transaction was performed on the stock system using two known queue-0 SMU addresses:

```text
old selector          = 0x03b10a68   # Q0 response
old data              = 0x00000001
selected target       = 0x03b10a48   # Q0 argument
selector readback     = 0x03b10a48
target data           = 0x00000000
restored selector     = 0x03b10a68
error                 = none
```

Only PCI config `0xB8` was written. PCI config `0xBC` was read only; no SMU data register was written and no mailbox message was sent.

The selector-dependent data change, exact selector readback, and exact restore establish the local BC-250 `0000:00:00.0` `0xB8/0xBC` SMN index/data path as live.

Classification:

```text
R115C_RESULT=BOUNDED_LOCAL_BC250_SMN_TRANSPORT_PROOF_FULL_PASS
```

This is a transport result only:

```text
SMN_TRANSPORT_PROVEN != DOMAIN6_POWER_PROVEN
SMN_TRANSPORT_PROVEN != VCN_VCPU_EXECUTION
SMN_TRANSPORT_PROVEN != VCN_RING_EXECUTION
```

## R116B — first local domain-6 status observation

Using the locally proven `0xB8/0xBC` transport, one bounded selector/read/restore transaction targeted only the externally documented domain-6 status register:

```text
target SMN            = 0x0006d190
selector readback     = 0x0006d190
raw status            = 0x01010101
restored selector     = 0x03b10a68
restored prior data   = 0x00000001
error                 = none
```

No `0xBC` write, SMU mailbox command, domain-6 write, VCN-core MMIO access, firmware load, or ring execution occurred.

The raw value exactly matches the `0x01010101` domain-6 up-residue signature reported by the pinned matching-platform external research. This locally reproduces the **sequencer status signature**, not yet the complete VCN power state.

Classification:

```text
R116B_RESULT=LOCAL_DOMAIN6_STATUS_UP_RESIDUE_MATCH_PASS
DOMAIN6_SEQUENCER_UP_RESIDUE=LOCALLY_OBSERVED
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
```

The whole-block power marker remains unproven because the external work itself documents a later state where the domain-6 sequencer reports the up-residue pattern while the VCN register block still appears closed, leaving isolation/reset/liveness as separate boundaries.

## R117B — low-vs-high domain-6 frame discriminator

A second bounded read targeted only the alternate full-width spelling of the same domain-6 status offset. The governor was temporarily quiesced, the SMN selector was confirmed stable, and the original selector was restored before the governor was restarted.

Observed pair:

```text
low-frame  0x0006d190 -> 0x01010101
high-frame 0x0116d190 -> 0x00000000
```

The high-frame transaction itself returned:

```text
old selector          = 0x03b10a68
second old read       = 0x03b10a68
selected target       = 0x0116d190
raw data              = 0x00000000
restored selector     = 0x03b10a68
error                 = none
governor after test   = active
```

This locally reproduces the pinned external low-frame discriminator and establishes the live domain-6 sequencer spelling on this card as the low SMN frame.

Classification:

```text
R117B_RESULT=HIGH_FRAME_DEAD_ZERO_DISCRIMINATOR_FULL_PASS
DOMAIN6_LOW_FRAME_SPELLING=LOCALLY_PROVEN
```

This remains a mapping/reachability result. It does not establish VCN de-isolation, register-file accessibility, VCPU execution, or ring execution.

## Current research direction

The low-frame domain-6 sequencer path is now locally reproduced at both the status-value and frame-discriminator levels. The next safe boundary is to investigate whether any independently readable SMN responder corresponds to the externally suspected isolation/reset family, while keeping speculative unknown-register writes and direct VCN-core MMIO out of scope.

External SMU/domain-6 research remains comparison material for those later boundaries. Invasive external enable tooling is not treated as locally reproduced or automatically safe.
