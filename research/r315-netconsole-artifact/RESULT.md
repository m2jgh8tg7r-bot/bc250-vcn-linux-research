# R315 — Packaged netconsole extended-mode audit

STAGE=R315
RESULT=PROVEN_STATICALLY: packaged artifact contains extended-mode handling
STATIC_OR_LIVE=Retained ELF inspection only
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Staged/extracted netconsole bytes equal; all four executable sections equal retained build; explicit plus-prefix and extended writer present
REJECTED=Extended output necessarily requires rebuilding this module
UNPROVEN=Running artifact identity, actual extended capture, R312 terminal checkpoint
NEXT=Integrate reviewed receiver workflow and one-character logging change into a separately identified package before any boot

## Artifact evidence

AUDIT.json records full-module and executable-section hashes. Staged and roundtrip module hashes match. The retained build has a different full-file hash but equal .text, .init.text, .exit.text and .altinstr_replacement. This does not establish relocation/data equality or explain every whole-file difference.

Inspection of the packaged module's .init.text finds a compare with 0x2b ('+') at offset 0xa3, followed by a byte flag write and an input-pointer increment before checking optional 'r'. This matches retained alloc_param_target source. netconsole_write_ext at .text offset 0x2d20 passes true to netconsole_write; send_ext_msg_udp is present. register_console relocations are present in initialization. This supports compiled explicit extended capability; it does not prove live registration or delivery.

## Minimal local draft

A private draft changes only the existing netconsole argument from basic to explicit extended format by inserting '+'. Reverse substitution reproduces the original init byte-for-byte; bash -n passes. It is intentionally not packaged or installed and still has the old R312 stage label. It must receive a new stage identity when integrated. No driver, firmware, panic timeout, confirmation gate, or hardware access is changed in the draft. Local addresses remain private and the draft itself is excluded from publication.

## Hypotheses and limits

Supporting evidence for explicit extended support: packaged instruction pattern, wrapper and formatter symbols, executable-section correspondence and retained source.
Contradicting evidence: none found for compiled capability; the full-file difference prevents a blanket artifact-identity claim.
Unknown: receiver OS behavior, live sender mode, receipt of the final checkpoint, and reset mechanism.
If this interpretation is wrong, live qualification may remain basic or fail; the manual gate must then remain closed and GPU loading must not proceed.
Next discriminating observation: extended qualification records must parse before confirming the receiver. A received named checkpoint/panic distinguishes execution paths; another absent suffix is still inconclusive. No new VCN read is justified.
