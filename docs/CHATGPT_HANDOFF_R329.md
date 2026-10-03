# R327–R329 — Next PCI configuration completion checkpoint (preparation in progress)

R326 remains the latest live result. It confirms final software-address provenance for its own boot, not physical VCN access or execution.

R327 selects a new discriminator: read same-device PCI identity using the standard API before and after one previously observed PGFSM CONFIG write. There is no VCN STATUS read. Successful pre-read is mandatory; invalid identity or API error aborts without that write. A returning post-read is transport-side ordering evidence under the retained Linux contract, not VCN power-on or command acknowledgement. No unchanged CP06/07 replay is planned.

[R327 transaction/recovery contract](../research/r327-posted-write-decision/RESULT.md) records target, transport, expected observations, recovery and unproven persistence. R328 draft implements the sequence behind bounded final-pointer, aperture, zero-pg/cg, non-VF and no-hardware-access checks. CPU probe stubs passed 32 write and 32 no-write conditions, including failed pre-reads and mismatched identities.

At this interim publication, isolated paired module builds are running. Compiled call/control-flow review, signing and R329 HOME image roundtrip are not yet closed. Prepared deployment scripts are drafts and have not been executed. HOME_PREPARATION_COMPLETE=NO; INSTALLED=NO; BOOTED=NO; LIVE_TEST_READY=NO. No agent hardware access, boot-file change or reboot has occurred. Protected preflight will require user sudo authentication after HOME validation.

The recovery method of the earlier R325 live trial remains unconfirmed; answer it from operator recollection, without repeating the achieved observation. Raw receiver completeness remains separate from the received final/panic markers.

Next: close paired build and call audit; package and validate HOME image; publish the completed status; then protected read-only preflight before deployment.
