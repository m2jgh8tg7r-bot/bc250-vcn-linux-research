> **R329 installed, independent audit PASS:** Saved package/preflight/installed identities and HOME retirement backup match. Normal boot unchanged. Not booted; fresh receiver capture and manual menu next. Earlier uninstalled notices below are historical.

> **Protected preflight PASS:** User-run result independently matched package, installer, image/entry and checker hashes. Normal default preserved; exact R325 retirement meets space margin. Not installed or booted. Next: installation then independent audit. Earlier pending-preflight statements below are historical.

# R329 — PCI configuration completion HOME package

STAGE=R329
RESULT=HOME preparation complete; protected boot preflight requires user sudo authentication
STATIC_OR_LIVE=PROVEN_STATICALLY; CPU stub tests separated from live hardware
HARDWARE_ACCESS=NONE by agent
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Paired control/candidate builds; 1003 other objects match; guarded checkpoint call audit; 64 probe and 180 observer CPU conditions; signed executable sections equal; exact archive roundtrip; clean depmod; gate11/default13/include14 and receiver8 checks
REJECTED=R326 matching base alone proves physical VCN accessibility; PCI identity return proves VCN execution
UNPROVEN=Protected actual boot preflight, installed hashes, live PCI returns, physical VCN completion/power, VCPU execution, historical CP06/07 cause, R325 recovery method
NEXT=User-authenticated read-only install.py preflight; review concrete result before no-selection installation and independent audit

## Experiment

Use standard same-device PCI identity reads around one existing PGFSM CONFIG write (segment1 0x7e00, byte0x1f800, value0x55555). Bounded final-pointer/aperture verification, zero pg/cg, non-VF and no_hw_access guards remain. Pre-read failure or identity mismatch aborts without CONFIG write. The checkpoint ends at named R328 panic with panic=0; no helper STATUS read, reset release, firmware change or unknown SMU request is added. Earlier GPU initialization still performs hardware operations during an eventual boot.

A healthy post-read supplies conditional transport-ordering evidence under the retained Linux PCI contract. It does not certify internal VCN request completion, physical power or execution. Missing output cannot establish the stopped instruction. No software timeout is claimed to escape stalled bus access. A hang must not trigger an unchanged retry.

## Verified preparation

Isolated relocated-tree baseline rebuild preceded control/candidate builds. The candidate source was explicitly applied and forced to recompile; initial stale-timestamp no-op output was superseded before audit or packaging. Other 1003 AMD objects match within this new build baseline. Compiler helper outlining and cold-label changes are recorded; no whole VCN function-byte equality claim is made. The compiled candidate contains two PCI read calls and one normal CONFIG write, guarded by successful pre-read and final-base checks. The enclosing checkpoint terminates in panic before subsequent helper MMIO code.

Signed module preserves all six executable sections. R325-derived HOME archive changes init labels and amdgpu module; full file/mode/symlink roundtrip matches and depmod is clean. Image size is 168063182 bytes (about160.3MiB). Sender qualification/input gate11, boot-default13, GRUB include14, receiver parser8 and observer180/probe64 CPU checks passed. These checks do not replace privileged inspection of actual GRUB state.

HOME_PREPARATION_COMPLETE=YES
PROTECTED_BOOT_PREFLIGHT=PENDING_USER_SUDO_AUTHENTICATION
INSTALLED=NO
BOOTED=NO
LIVE_TEST_READY=NO until protected preflight, installation and independent installed audit pass

## Deployment and observation

Prepared installer defaults to read-only preflight. It retires only hash-matching R325 image/entry after verified HOME backup, protects normal boot artifacts/defaults and offers rollback. No installation or menu script has run. Current normal kernel remains7.2.1-ogc4.1.fc44.x86_64; sudo -n reports password required. Authentication was not bypassed.

Private OPERATOR.md contains exact commands and receiver sequence. Capture a fresh raw JSONL on the receiver, manually select R329 only after installed audit, require received QUALIFICATION_COMPLETE before local token, retain all pre/write/post/panic markers and report reset/cold-power-cycle/display recovery separately. Prior R325 recovery method can be confirmed from recollection; do not repeat R325 for it.

Detailed transaction/recovery contract: ../r327-posted-write-decision/RESULT.md. Compiled audit: ../r328-pci-config-checkpoint/COMPILED_REVIEW.md.
