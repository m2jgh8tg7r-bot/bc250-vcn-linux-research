# Patch notes

This directory documents patch identities and safety status. It does not imply that every historical experimental patch should be run.

## R79 — real software init with Cyan PSP VCN enrollment suppressed

Purpose:

- allow the real VCN software lifecycle,
- acquire the VCN firmware,
- register software rings,
- suppress automatic Cyan PSP VCN firmware enrollment,
- keep hardware execution quarantined.

Known patch SHA-256:

`a421b533579c43c6d3e0dd25a75b43843c66702cb66217a2d6b38b22ee1bda5a`

This stage is important because it created a controlled separation between software initialization and firmware/VCPU execution.

## R100 — pre-hardening transient NBIO RMW

**Status: SUPERSEDED / DO NOT USE FOR LIVE TESTING.**

The initial helper placed logging between target readback and normal restoration, and also logged before the emergency restore path. The issue was discovered before a live write was executed with this artifact.

Its boot entry was quarantined and must not be restored for live use.

## R107 — safety-hardened immediate-rollback source

The R107 helper fixed the R100 ordering problem:

- fresh read before any write,
- zero-write stop when the fresh value is unexpected,
- one target write only,
- one target readback,
- immediate normal restore with no logging in between,
- emergency restore as the first executable statement in the mismatch branch,
- no target retry loop,
- logging only after restoration attempts.

Identities:

- combined patch SHA-256: `6197af894ee930284f1d225dd92efbce8e73162707c441a929a966b92a6c9960`
- helper SHA-256: `3a5b882d2b96d8240a5659be7015f31f73b5623e091d9e087b52aac214301a29`
- R100 -> R107 delta SHA-256: `7d37e84c8da5ab801ca11c238781580acb467137bbea68238a7e2aeb7453879b`

Built custom amdgpu identity used for the successful bounded live transaction:

- Build ID: `b0ca3ad4d1f157bf2a34b7e24fe221fff3a9a9b4`
- stripped module SHA-256: `cb3a6944a4c3861c7fe289a9ec1d4879cb6069c54300ffb526701521670fc0d6`

## Safety warning

Even the hardened ordering cannot guarantee restoration after a write-induced hard stall. If the hardware stops executing instructions at the target write, the later restore instruction cannot run.

For this reason, a future live write that hangs must not be automatically retried.

## Publication policy

Historical patch identities and safety-relevant deltas are worth publishing even when the patch itself is not suitable for reuse. This helps other researchers distinguish a proven design from an obsolete or dangerous intermediate artifact.
