# R327 — Posted-write completion boundary and next candidate

STAGE=R327
RESULT=Choose standard PCI configuration pre/post control after the previously observed PGFSM write; do not read VCN STATUS
STATIC_OR_LIVE=Saved-source documentation review with inherited CP05/R325 live evidence separated
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Saved Linux posted-write documentation; standard PCI read API dispatch; Cyan power callback no-op boundary
REJECTED=Matching R325 bases makes STATUS-read retry informative; CONFIG write-return proves VCN power-on
UNPROVEN=Physical VCN power/clock, historical read execution, bus/device completion in candidate, VCPU execution
NEXT=Build and verify a guarded CONFIG-write plus PCI identity-read checkpoint; no STATUS transaction

## Why this is a new question

R325/R326 closes the final-base premise for its boot. Historical CP05 provides a saved write-return marker followed by its named panic. CP06/CP07 did not provide decisive read execution/return evidence. Do not repeat those reads unchanged.
The saved kernel Documentation/driver-api/device-io.rst:68–104 states PCI writes are posted and documents a same-device read as completion ordering, with config-space reads recommended when the device read may fail. This is the Linux driver contract, not a promise that every platform fault is recoverable or that internal VCN commands complete.
The Cyan startup's DPM request path still lacks a real VCN enable callback; software success cannot supply a missing physical prerequisite. The ordinary zero-pg startup uses CONFIG then STATUS before software clock programming, so merely moving clock accesses earlier would introduce unqualified VCN reads/writes. Unknown SMU messages and arbitrary clock-register changes are not selected.

## Candidate transaction contract

- Hypothesis: the previously observed CONFIG write can be followed by a returning standard same-device PCI configuration read; this supplies a transport-side boundary distinct from inaccessible VCN STATUS.
- Target/transport: PCI_VENDOR_ID offset0, 4 bytes via pci_read_config_dword, before and after one PGFSM CONFIG write. No PCI configuration write. The single MMIO write uses the established macro to VCN instance0 segment1 CONFIG, dword0x7e00 / byte0x1f800, value0x55555.
- Before state: physical PGFSM/power unknown; fresh bounded final-pointer verification must match segment1=0x7e00, count>1, aperture>=0x1f804, zero pg/cg, non-VF, no_hw_access=0. Pre-read must return success and match the device's enumerated vendor/device identity.
- Changed variable relative to a paired compile control: insertion of the single established CONFIG write between identical standard PCI reads. New network markers describe before-write, write-return, pre/post PCI read results. Do not require an additional control boot automatically; pre-read is the within-boot control.
- Expected after state: reported config read return and identity, not an asserted physical power-on state. Healthy post-read is conditional transport-completion evidence under documented ordering, not VCN command/status acknowledgement.
- Positive: pre/post return success with expected identity, ordered write-return marker and named planned panic/end. Negative: explicit API error or identity mismatch; pre-read failure aborts without CONFIG write. Missing output remains inconclusive about stopped instruction and cause.
- Rollback/recovery: no state-restoring blind write; keep panic=0/manual reset and normal boot. Retain old image/entry HOME backups before any deployment. Old successful CP05 recovery is provenance; candidate config-read sequence and cold-power-cycle recovery remain untested. No software timeout is claimed to break a stalled bus access.
- Persistence: CONFIG is a runtime request, not flash/OTP programming. Exact warm/cold persistence and device internal transition remain unproven, so recovery observation is recorded separately.
- Prior proof: CP05 saved after-write marker and named panic at7.410966/7.410969s. The post-write PCI-read ordering sequence has not yet been proven live.

## Outcomes and limits

A healthy post-read would justify stronger transport provenance and qualify post-write network delivery for later experiments, reopening the specific infrastructure purpose that R304 deferred. It does not justify releasing reset, executing a ring or trying STATUS without a separately justified discriminator.
Failure after a healthy pre-read would narrow the observation to the new write/read sequence, but would not identify power, policy, device internals or a specific failing instruction. Never retry that sequence unchanged after a hang. No bypass, new firmware, policy modification or unknown SMU transaction is involved.

No new image, installation or hardware transaction was performed for this decision.
