# R282 — rollback correction: first attempt likely persisted

Date: 2026-10-01

The previous R282 note said the first attempt rolled back after printing PASS because the parent-shell EXIT trap still saw SUCCESS=0.

A second run of the corrected installer immediately stopped at:

```text
STOP: R282 image target already exists
```

This reveals an additional consequence of the same pipeline-subshell bug.

The variables:

- SUCCESS
- CREATED_IMAGE
- CREATED_ENTRY1
- CREATED_ENTRY2

were all mutated inside the pipeline subshell, while the parent EXIT trap retained their initial zero values.

Therefore the parent trap printed:

```text
ROLLBACK_COMPLETED=YES
```

but probably did **not** remove the persistent R282 image/BLS targets, because its CREATED_* flags were still 0.

The first R282 attempt had already proven during the subshell execution that:

- installed image SHA matched the R281 image;
- installed BLS matched the generated entry;
- boot policy hashes were unchanged;
- R180 and Bazzite recovery entries remained present.

The actual persistent post-command state now requires a read-only audit.

Updated classification:

```text
R282_TRANSIENT_INSTALL=PROVEN
R282_ROLLBACK_MESSAGE=PROVEN
R282_ROLLBACK_EFFECT=NOT_PROVEN
R282_PERSISTENT_INSTALL=LIKELY_BUT_MUST_BE_AUDITED
```

Do not rerun the installer again until persistent state is audited.
