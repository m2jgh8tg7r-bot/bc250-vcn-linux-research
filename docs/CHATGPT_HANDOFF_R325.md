# R325 — Final-pointer checkpoint HOME preparation

STAGE=R325
RESULT=HOME image prepared and verified; protected boot preflight awaits user sudo authentication
STATIC_OR_LIVE=PROVEN_STATICALLY package/build checks and CPU fixtures; no live test
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=R324 instrumentation review closed, 1003 unchanged objects, signed executable-section identity, image roundtrip, depmod clean, gate11/default13/include14 CPU checks
REJECTED=R324 build-only status is still the latest preparation status
UNPROVEN=Protected actual boot configuration preflight, installed identity, final live pointer, VCN execution, old CP06/07 cause
NEXT=User-authenticated read-only install.py preflight, then reviewed installation audit and manual receiver-qualified boot

## Observation and its limits

This new checkpoint identifies whether the helper's selected VCN instance0 pointer belongs to a bounded discovery record and whether that record contains segment1. It logs matching die/count, number of instance0 records and conditional CONFIG/STATUS byte offsets. It adds no VCN register transaction and retains an unconditional named panic before helper VCN MMIO. Earlier GPU initialization still accesses hardware. Pointer values are never printed.
Expected matching base1 supports the software-address premise for this new boot. Unexpected bases or count0/1 revise it. No-match, malformed/conservatively rejected layout or missing logs remain inconclusive. Neither outcome proves VCPU execution or historical failure cause. Do not repeat unchanged CP06/07.

## Closed preparation gates

The compiler UBSan call is the guarded die_info[16] subscript check; ndies<=16 and die<ndies keep ordinary execution outside its failure path. __fentry__ is existing kernel function tracing instrumentation. These are documented accepted call relocations, not hardware operations. Guard and panic control flow are retained.
The incremental paired-build comparison keeps all 1003 other objects identical. Across 53 common VCN functions only vcn_v2_0_hw_init.cold changes bytes, and the software observer is added. This is pre-relocation evidence, not a proof of all linked data semantics or historical R318 equivalence.
Signing preserves all six executable module sections. The R318-derived image changes only init labels and amdgpu.ko; depmod reports no warnings and full extracted file/mode/symlink manifests match. The exact original R318 tree remains unchanged. Kernel image hash still matches the prior retained kernel audit.
CPU init-gate11, default-layout13 and include14 cases pass. The protected actual GRUB state is not read by those fixtures. Existing raw-receiver analyzer8 tests also pass.

## Remaining deployment gates

HOME_PREPARATION_COMPLETE=YES
PROTECTED_BOOT_PREFLIGHT=PENDING_USER_SUDO_AUTHENTICATION
INSTALLED=NO
BOOTED=NO
LIVE_TEST_READY=NO until protected preflight and installation identities are verified

The current normal kernel was read and remains 7.2.1-ogc4.1.fc44.x86_64. /boot has about 130MiB available, less than the roughly 160MiB new image. install.py therefore retires only the exact hash-matching R318 image/entry after verifying a HOME backup, installs the new image/entry without selection and has rollback. Existing normal entries, their referenced artifacts, the research kernel and retained R180/R298 artifacts are protected. It checks actual saved/fixed-index boot defaults and includes before any write. No installation or menu script was run.
The passwordless sudo probe reported authentication required. We did not bypass authentication. The read-only installer mode computes concrete protected hashes/default/space checks; only a later --install run writes boot files. Menu preparation is a distinct later action and performs no reboot.

## Operator sequence

1. Run the prepared install.py with sudo and WITHOUT --install; inspect PREFLIGHT_RESULT.json. Any rejection stops installation for review.
2. After the protected preflight succeeds and planned boot changes are communicated, execute --install and independently verify installed image/entry hashes and retained default artifacts. No automatic boot selection.
3. Start the existing R314 raw UDP capture on the receiver with a fresh private JSONL file for this boot. Receiver bound status alone is not sender qualification; verify R325 QUALIFICATION_COMPLETE is actually received before the sender gate token.
4. Only after installation/receiver checks, use the separate manual-menu preparation and explicitly select R325. The existing research confirmation token is retained. panic=0 requires manual reset after the named R324 final-pointer checkpoint. Do not type a different token or retry an unexpected modprobe return.
5. Preserve raw JSONL, analyze fragments and report explicit FINAL plus named panic/end markers and recovery separately. Do not use console excerpts to claim complete transport capture.

Detailed private operator commands are in OPERATOR.md in the local package directory. No raw init with machine network addresses, signing keys, module binaries or raw transcripts are published. This preparation supersedes R324's open compiler-audit/unsigned/unpackaged status while preserving its historical report.
