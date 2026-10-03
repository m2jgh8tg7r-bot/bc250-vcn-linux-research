# R302 — network-first CP03 control with live-proven input diagnostics

Date: 2026-10-03 JST. Prepared in HOME only; not installed or booted.

The user selected the R300 input-diagnostic approach for the next CP03 control. R300's supplied receiver excerpt reports stdin_tty=YES, read_rc=0, 18 bytes and INPUT_EXACT_MATCH for the public token R299-CP03-RECEIVED. This is LIVE_CONFIRMED for that diagnostic boot; it does not identify why the earlier R299 boot rejected input.

## Result

R302 preserves the R299 NIC/netconsole qualification sequence and exact signed CP03 module. Its archive tree differs from R299 only at /init. The new init retains R300's locale, TTY/read diagnostics and escaped consumed-string logging, then requires both successful read status and exact token equality before the GPU-presence guard, five-second pause and CP03 module load. Failed reads and mismatches hold separately without GPU load or normalization. Unexpected module-load return also holds without retry. The token remains R299-CP03-RECEIVED because that exact string was successful under R300; stage markers are R302.

The read log describes Bash's consumed string, not raw keyboard bytes. Newline is consumed and terminal discipline may transform input. Type only the public token because input is logged. R302 is a separate package, not a modification of the installed R299 or R300 images.

CPU pipe/PTY gate checks pass 11/11: exact token, trailing space, CRLF, empty line, EOF, exact token without newline, Unicode dash, long input, already-present GPU, queued wrong first line, and PTY exact input. The real gate fragment is exercised with command stubs. All rejection cases issue zero mock GPU loads; accepted input issues one in the expected marker order. This does not prove actual boot-console behavior, real GPU initialization or panic delivery.

Build checks pass: shell/Python syntax, warning-free depmod, module dependency closure, gzip integrity, exact hash/mode/symlink archive round-trip, fixed signed-module hash, and independent R299/R302 tree comparison. No actual modprobe, boot write, pstore change or reboot was performed.

## Experimental boundary

After qualification and confirmation, the unchanged R297 CP03 module is expected to initialize the existing GPU path and reach the P1/Cyan hw_init branch checkpoint. It intentionally panics before the helper. No new VCN MMIO read/write or reset release is added. Existing firmware provisioning and GPU initialization are real hardware operations during a future user-run boot; this is not an observation-only R300 image. An expected CP03 panic may reboot under panic=10, while an earlier hard stall can still require manual recovery. GPU/fabric hang-time netconsole delivery remains UNPROVEN.

The useful observation is the ordered same-boot sequence: R302 qualification, successful input result, INPUT_EXACT_MATCH, RECEIVER_CONFIRMED, AMDGPU_MODPROBE_BEGIN, then existing CP03 checkpoint/panic markers. A final pre-load marker with no later marker only bounds observable progress; it cannot uniquely identify the stalled instruction or distinguish delivery loss. Missing qualification 1/10 in prior excerpts is not repaired by this package.

## Installation contract and next action

Prepared installer defaults to a privileged read-only preflight. It requires the normal kernel, successful normal boot, no pending selection/menu state, unchanged package identities, exact installed R299 hashes and normal pstore policy. It hashes all retained BLS entries and their referenced images, normal kernel, R180/R298/R300, research kernel and GRUB. Local capacity observation was 135,909,376 bytes; R302 is 168,064,369 bytes. It therefore prepares verified retirement of R299 only, with a flushed HOME backup before deletion and at least 50 MiB remaining. R300 and recovery artifacts are retained. Catchable installation failure restores R299; power-loss recovery is not guaranteed.

Default preflight does not retire, install, select or reboot. The next user action is:

```sh
sudo python3 /var/home/kazuyuki/bc250-research/research/r302-netconsole-cp03-inputdiag/install.py
```

Share its PASS output for independent audit before installation. The installer with --install and the manual-menu helper are prepared locally, but their execution is not the current next step. Menu preparation would require a prior installed audit and boot-change notification. No automatic hardware launch is scheduled.

## Identities

- image SHA-256: 1f35c5bde8e15b22a05526f7b62d45cd7493e23135763e52eb592899bfddd522
- image size: 168064369 bytes
- BLS SHA-256: 0cdf7754f224c0bfad5ddc52f7a5ca6b9fa132e8bd27746202315254b9a753ca
- init SHA-256: 26268fd93b80c47fe113c2f75e095866941eae353e2bb14edc1f93a1f9ec1aed
- unchanged signed CP03 module SHA-256: 43f177df38a8d4bef6572fcaca89c6d0f1f6165fd8983ee3ce62d019ec7c3d9a

## Evidence taxonomy

STAGE=R302 HOME preparation
RESULT=STATIC_CONFIRMED package/input-gate contracts; privileged preflight pending
STATIC_OR_LIVE=STATIC_CONFIRMED new preparation; LIVE_CONFIRMED prior R300 user-supplied input result only
HARDWARE_ACCESS=No new agent device operation; source/package filesystem inspection only
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=No new hardware observation
PROVEN=11 CPU/PTY gate cases, exact archive round-trip, unchanged CP03 module/network sequence, only init differs
REJECTED=R300 proves R299 rejection cause; mocked gate proves CP03 or panic delivery
UNPROVEN=R302 installation/boot, real gate behavior, GPU-stage transport, CP03 boundary and VCN execution
NEXT=User-run privileged read-only preflight, then independent audit

Private network configuration and raw machine logs remain local. [Package audit](../research/r302/PACKAGE_AUDIT.json), [independent tree comparison](../research/r302/INDEPENDENT_PACKAGE_AUDIT.json), [CPU/PTY gate results](../research/r302/GATE_TEST.json).

## Privileged read-only preflight verified

The user-run preflight returned PASS. The saved result was independently checked against current HOME package/image/BLS/init/installer hashes, exact installed R299 retirement hashes, prior protected records and R300 identities. Nine protected files were directly readable and matched; four require privileged reads and are supported by the user-run preflight record, not a new independent privileged read. Estimated post-replacement capacity is 135,906,713 bytes, above the 52,428,800-byte margin. Normal kernel confirmed; no boot write, selection change, module load or reboot.

NEXT=User-run the same install.py with --install. This archives and verifies R299 before replacement, installs R302 without selection, preserves R300/normal/recovery artifacts, and saves an installed audit. Audit that result before menu preparation or manual boot. Installation and R302 LIVE remain UNPROVEN.
