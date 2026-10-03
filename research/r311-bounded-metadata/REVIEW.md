# R311 — Count-bounded discovery observation

R310 draft is superseded. Its unbounded pre-panic reg_offset dereference is removed. The replacement logs at most the first three slots inside the existing parser loop guarded by k < num_base_address, after the existing conversion/read. It adds no unconditional index1 access. If count is 0, this loop emits no record; missing output cannot distinguish count0 from other causes. A received count1 record explicitly supplies evidence that index1 was not present in that parsed entry. Existing parser input validation is assumed; this is not a complete malformed-discovery parser audit.

At CP04's existing pre-access boundary, only scalar fields are logged: apu_flags, pg_flags, cg_flags, no_hw_access and rmmio_size. No base pointer dereference or new register read/write occurs there. The existing guards and unconditional panic are retained. Driver initialization before this point still accesses hardware.

The two observation times are distinct: discovery parsing versus the later helper checkpoint. These logs will NOT establish that reg_offset is unchanged between them. Runtime mutation/corruption remains unknown without further evidence. Die/instance identity and duplicate entries or later assignments must be kept separate; a parsed value is not necessarily the final selected value. Scalar no_hw_access does not attest the entire accessor dispatch or its later execution.

Outcomes:
- Expected parsed base plus compatible later scalar conditions: supports this new boot's parsed metadata and scalar conditions, not historical failed-boot values or physical response.
- Missing index1 because entry count is too small, unexpected base, or incompatible scalar condition: revises the relevant software premise for this boot.
- Missing records: inconclusive, not evidence of a hardware fault. No unchanged failed-read retry.

The paired baseline and candidate are built in the same isolated tree/toolchain. Broad rebuilding is explicit; equivalence to historical CP04 is not presumed. Object and module comparison must precede packaging or installation.

Supporting evidence: previous pre-access marker delivery and current normal-boot metadata.
Contradicting evidence: no live R311 observation yet contradicts any runtime hypothesis.
Unknown: pointer lifetime between observations, loaded bytes, device state, failed-boot stop, VCPU execution.
If address reasoning is wrong: even matching metadata may coexist with later pointer changes or device-side failure.
Next discriminating work: audit compiled logging/panic boundaries and paired module differences. No new boot or hardware operation is authorized by this document alone.
