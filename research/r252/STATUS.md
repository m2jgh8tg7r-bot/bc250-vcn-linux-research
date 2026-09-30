# R252 — source applicability and startup return contracts

STAGE=R252
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=pinned source and retained diagnostic source
HARDWARE_ACCESS=separate Q36 GPU_COMPUTE only
HARDWARE_MUTATION=none for research target
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=14 source contracts; upstream/reference/local diagnostic paths distinguished
REJECTED=ring allocation success implies VCPU startup; missing callback success implies physical power transition
UNPROVEN=external active kernel/boot path and actual VCPU state
NEXT=offline external-observation contract and cross-version source comparison

Linux `551c722f40809618230001baccf219193e22fc5a` leaves the VCN2.0.3 registration branch empty. The normal VCN2 sequence is therefore a reference for nearby supported IP versions, not a claim that unmodified upstream starts BC250 VCN. NV initialization sets both clock- and power-gating flags to zero for GC10.1.3/10.1.4; the global pg mask ANDs existing flags and cannot add DPG support. An external modified configuration needs its own evidence.

The normal test chain is hardware initialization → ring-test helper → specialized VCN2 decode ring test → ring allocation → VCN begin-use → set_pg_state → start. `begin_use` is void and does not propagate `set_pg_state`'s error. Ring allocation may consequently return zero despite an unsuccessful startup; the later test observation and logs remain necessary. The state setter updates its software state only when start/stop succeeds.

The VCN2 specialized ring test includes a packet-start command followed by an expected scratch-register change; it is not identical to the generic VCN scratch test. A sourced test result must identify which implementation ran. Such a register effect is still distinct from decoded-frame correctness.

The DPM enable helper returns void after logging failures. The SMU VCN helper can also return zero when the VCN path is absent or its enable callback is missing. Cyan's complete static PPT callback initializer contains no `dpm_set_vcn_enable` member. This bounds what a software-success observation means; it does not prove the block is physically off or incapable of operating.

The retained R152 working source separately returns `-EOPNOTSUPP` from Cyan start and skips Cyan hardware initialization with a diagnostic message. Its source hash is recorded. This is deliberately limited to the retained source, not an assertion about the currently loaded module or an external researcher's kernel.

`audit_calls.py` records exact source witnesses in `results.json`. No kernel changes or test boot were performed.

Prior evidence: R143 already established the underlying power/return and saved-file geometry facts. This stage refreshes and connects them to the current pinned source and the new external-report question; it is not a first discovery of those facts.

Cyan initialization also has two source-provenance branches: one uses discovery tables, while the other assigns IP versions statically, including UVD/VCN2.0.3. A reported driver IP version is not automatically an independent silicon-discovery measurement. Which branch an external configuration used remains unproven.
