# External research comparison

This document records how this project currently interprets several other public BC-250 efforts. External claims remain external until independently reproduced on the tested hardware.

## daveconde/bc250-vcn-enable

This project is the most directly relevant external comparison for real VCN bring-up.

Pinned comparison snapshot:

```text
repository: daveconde/bc250-vcn-enable
main: 7c511b725b135766c52a3e13776c1cd187e5015d
```

Its target platform is BC-250 BIOS 3 / Robin1 / PMFW 0.58.6.0. That matches the locally observed BIOS P3.00 and SMU firmware `0x00580600` (88.6.0 / 0.58.6.0), so the comparison is materially relevant.

### R115A static comparison

The external project identifies VCN as SMU power domain 6 and associates three clock slots with it:

```text
VCN slots: 0x16, 0x17, 0x18
```

Its BIOS-3 analysis also identifies a domain-6 sequencer block in the low SMN frame:

```text
cmd    = 0x0006d17c
rail   = 0x0006d184
status = 0x0006d190
ctrl   = 0x0006d0f8
```

The external project treats those values as an SMU-side power-state oracle. It further reports that host PCI-config reads of this block are live while direct host writes to the sequencer are ignored, with the firmware/debug-window path being the effective write vehicle.

This complements rather than contradicts the local R73-R113 work:

```text
local R113:
  NBIO BIF_MMSCH0_DOORBELL_RANGE transaction proven
  -> doorbell routing/configuration boundary

external domain-6 work:
  SMU sequencer / clock / rail state
  -> power-management boundary

NBIO_DOORBELL_TRANSACTION != VCN_POWER_PROOF
```

Accordingly, the successful R113 write/read/restore remains useful hardware evidence but does not change `OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN`.

### Transport distinction

The external BC-250 SMN transport is source-visible and uses root device `0000:00:00.0` PCI config space:

```text
write SMN index -> config 0xB8
read SMN data   -> config 0xBC
```

This is not automatically equivalent to Linux's generic `amd_smn_read()` path. Current upstream `amd_smn_read()` uses a different PCI config index/data pair (`0x60/0x64`) through the AMD node helper. Therefore this project did not substitute `amd_smn_read()` for the BC-250-specific `0xB8/0xBC` transport without a separate transport-identity proof.

That distinction is important because a transport mismatch could turn a nominally read-only experiment into a read from a different fabric/address space.

### R115 local transport reproduction

The external transport model has now been independently reproduced on the tested BC-250 at the transport layer.

Local preflight confirmed:

```text
0000:00:00.0 = AMD Ariel Root Complex [1022:13e0]
```

The installed `cyan-skillfish-governor-smu` v0.4.12 was also verified from exact upstream source to use the same `0xB8/0xBC` transport. It was temporarily quiesced before the active selector test to avoid index/data races.

A bounded local transaction then used two exact upstream queue-0 addresses:

```text
old B8 / Q0 response = 0x03b10a68
old BC               = 0x00000001
selected B8 / Q0 arg = 0x03b10a48
selected BC           = 0x00000000
restored B8           = 0x03b10a68
error                 = none
```

Only the index selector at PCI config `0xB8` was written. `0xBC` was read only. No SMU mailbox message, domain-6 write, or VCN-core access occurred.

This changes the local status of the transport boundary:

```text
BC250_ROOT_B8_BC_SMN_TRANSPORT=LOCALLY_PROVEN
```

It does not import any later external result automatically:

```text
LOCAL_SMN_TRANSPORT_PROOF != LOCAL_DOMAIN6_POWER_PROOF
LOCAL_SMN_TRANSPORT_PROOF != LOCAL_VCN_EXECUTION_PROOF
```

### Domain-6 status semantics and R116 local reproduction

The pinned external source documents:

```text
status @ 0x0006d190
bit 8  = up-ack
bit 12 = down-ack
```

and reports `0x01010101` as the persistent up-residue pattern for domains 0-6 on its tested matching platform, while a firmware-commanded-down domain 7 showed `0x01011010`.

A bounded local read has now independently reached the same low-frame domain-6 status address through the proven local transport and returned:

```text
0x0006d190 -> 0x01010101
```

The selector was then restored exactly and no SMU data write or mailbox command was performed.

This upgrades only the sequencer-status boundary:

```text
EXTERNAL_DOMAIN6_STATUS_SIGNATURE=LOCALLY_REPRODUCED
DOMAIN6_SEQUENCER_UP_RESIDUE=LOCALLY_OBSERVED
```

It does **not** yet justify `OUTER_WHOLE_BLOCK_VCN_POWER=PROVEN`. The same pinned external source explicitly records the unresolved contradiction that the domain-6 sequencer can look UP while VCN MMIO still appears CLOSED/all-ones, motivating a search for additional isolation/reset/state latches. Therefore this project keeps sequencer status, de-isolation, VCN register accessibility, VCPU execution, and ring execution as separate proof boundaries.

### VCN register-file warning

The external register-map work explicitly distinguishes VCN MMIO register-file offsets from SMN addresses. It reports that VCN MMIO reads can hang while the island is dead, and later can return uniform `0xffffffff` even after domain-6 clock/power work. This reinforces the local policy that direct VCN-core MMIO is not the next first-contact probe.

### PSP / firmware / ring comparison

The external project also explores a direct VCN firmware-load path that bypasses PSP/TEE and uses the driver's ring-test concept (`mmUVD_SCRATCH9` changing from `0xCAFEDEAD` to `0xDEADBEEF`) as execution proof.

This aligns conceptually with the local separation:

```text
PSP enrollment != VCN VCPU execution
software ring registration != ring hardware execution
```

But the external direct-load implementation, firmware choice, SMU exploit, handler redirection, and ring execution remain outside current local authorization.

### Current conclusion

The BC-250 `0xB8/0xBC` transport and the external domain-6 `0x01010101` status signature have both now been locally reproduced. The next boundary is to distinguish sequencer-up residue from a genuinely de-isolated/access-ready VCN block without jumping directly to risky VCN-core MMIO.

Current policy:

```text
BC250_ROOT_B8_BC_SMN_TRANSPORT=LOCALLY_PROVEN
EXTERNAL_DOMAIN6_STATUS_SIGNATURE=LOCALLY_REPRODUCED
DOMAIN6_SEQUENCER_UP_RESIDUE=LOCALLY_OBSERVED
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
RUN_EXTERNAL_ENABLE_TOOL=NO
RUN_DIRECT_LOAD=NO
RUN_SMU_HANDLER_REPOINT=NO
```

## simpmix/bc250-encoding-decoding-fix

This project explores a different route: using RDNA compute/Vulkan to provide VA-API-style video functionality without relying on the locked VCN silicon.

That makes it useful as a practical fallback route for applications such as streaming or recording, but it is conceptually separate from this project's goal:

```text
this project: real VCN -> power -> firmware/VCPU -> ring -> video APIs
compute workaround: GC/RDNA compute -> VA-API-compatible path
```

A compute-based encode/decode path must not be reported as proof that the physical VCN block has been enabled.

## leogx9r/ryzen_smu

`ryzen_smu` is useful as a reference implementation for Linux-side SMU/SMN transport concepts, including mailbox and SMN access patterns.

Cyan Skillfish / BC-250 is not treated here as a directly supported platform merely because a similar SMU family is supported elsewhere.

Current use: design/reference material for transport, timeout handling, and interface structure—not a blanket authorization to load or use it for VCN enablement.

## Comparison rule

For all external projects:

```text
EXTERNAL_REPORTED_SUCCESS != LOCAL_REPRODUCTION
```

Useful external findings may influence what this project audits or tests next, but local status markers change only when the corresponding boundary is reproduced on the local BC-250.
