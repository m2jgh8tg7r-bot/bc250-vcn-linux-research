# External research update — Shalasere / 2026-09-14

## Purpose

This note records a public external research update for comparison against the current local BC-250 VCN work. It is **input evidence for independent verification**, not a statement that the external interpretation is correct.

Current local handoff observed before adding this note: `docs/CHATGPT_HANDOFF_R197.md` (R195–R197). Therefore this document must be evaluated against **R197 or later**, not against the older R125/R153 state.

## External source

Primary public repository under review:

- `Shalasere/bc250-vcn-research`
- Reported relevant update date: 2026-09-14
- Commit previously identified during public monitoring: `4499a7c9fc4fd340c1fda82631b9a0b5f34d611e`
- URL: https://github.com/Shalasere/bc250-vcn-research/commit/4499a7c9fc4fd340c1fda82631b9a0b5f34d611e

Before relying on any conclusion below, fetch and inspect the commit, referenced raw logs/scripts, and surrounding history directly.

## Reported observations worth checking

The public report states that a broad set of SMU-authority writes targeting candidate VCN-related registers did not produce the expected VCN clock/activity transition. Candidates reportedly included:

- `CC_UVD_HARVESTING` at `0x0001f81c`
- prior candidate `0x0900c004`
- multiple Van Gogh-derived `0x0900xxxx` addresses

The report says DCLK sentinel `1111` remained unchanged and no VCN activity appeared across the tested set.

Treat this as **externally reported live evidence pending local audit**. Do not equate it with local reproduction.

## Van Gogh comparison claim

The same external work reports that a Van Gogh SMU firmware comparison exposed a VCN-related table/region around:

- `0x16be0..0x17000`

and candidate referenced addresses including:

- `0x0900c1d0`
- `0x0900c224`
- `0x0900b018`
- `0x0116f200`
- `0x0116ee00`
- `0x00050d6c`
- `0x000511b4`

The external report further claims that the older `0x0900c004 = VCN cold reset` interpretation is weakened because the corresponding Van Gogh SMU path does not appear to reference that address while other `0x0900cxxx` registers do.

This is potentially important, but **the semantic names are not trusted until call sites, control flow, and register effects are independently reconstructed**.

## What this does NOT prove

Do not promote any of the following to PROVEN_LOCAL based on this note alone:

- that `0x0900c004` has no role on Cyan Skillfish
- that the Van Gogh table has identical semantics on BC-250
- that SMU-authority access is sufficient to remove VCN isolation
- that `CC_UVD_HARVESTING` is the decisive outer gate
- that PSP boot-loader code permanently clamps VCN
- that any particular SVC owns the missing de-isolation/reset sequence
- that VCN MMIO, VCPU execution, hardware ring execution, VA-API decode, or encode is now functional

External summaries may contain inferred or AI-assisted naming. Prefer raw code, disassembly, scripts, logs, and reproducible observations.

## Relation to current local work

R197 currently focuses on a controlled standard-PSP response comparison using predecessor Navi10 VCN firmware. That experiment should remain logically separate from this external SMU/PSP power-path evidence.

This external update is most useful for the **next static-analysis branch** rather than as justification for speculative live writes.

## Recommended Codex application

### 1. Reproduce the Van Gogh-vs-Cyan static comparison

Independently obtain/identify the exact Van Gogh SMU image used by the external work, then verify whether a table/function region corresponding to `0x16be0..0x17000` exists and reconstruct its consumers.

For each candidate address (`0x0900c1d0`, `0x0900c224`, `0x0900b018`, `0x0116f200`, `0x0116ee00`, `0x00050d6c`, `0x000511b4`):

- find every static reference in the compared firmware images;
- identify the containing function(s);
- reconstruct argument flow and write/read ordering;
- identify prerequisite branches and polling loops;
- compare with Cyan/Robin1 equivalents by structure, not by guessed function name.

**Confirming result:** a coherent Van Gogh VCN-specific control path is independently reconstructed and Cyan either lacks it or routes to a structurally different primitive.

**Falsifying result:** the reported addresses are not actually consumed by a VCN-specific path, or Cyan contains an equivalent path missed by the external report.

### 2. Re-test the `0x0900c004` hypothesis statically before any live use

Search all relevant Cyan and comparison firmware for `0x0900c004` references and nearby address-family accesses. Determine whether its control-flow context is actually reset/power related.

Do not retain the label `VCN cold reset` without evidence from callers and side effects.

### 3. Cross-check against local policy/callback work

Compare the reconstructed Van Gogh VCN path against the local Robin1 dynamic-policy/callback chain, including the previously identified function-pointer/policy machinery. Look for convergence on the same lower-level primitive rather than matching names.

A meaningful convergence would be stronger evidence than either analysis alone.

### 4. Audit the external SMU-authority write experiment before reproducing it

Inspect the exact external scripts/logs and answer:

- what authority/path actually performed each write;
- whether every write had readback;
- whether values were restored;
- what clocks/status/registers were sampled before and after;
- whether the tested state was clean boot or already modified;
- whether failure to change DCLK can distinguish isolation from wrong-register/wrong-prerequisite cases.

Until that audit is complete, treat duplicate live writes as low priority.

### 5. PSP/SVC work remains static-first

If external evidence points toward PSP/ABL ownership of the missing gate, enumerate and compare candidate SVC handlers and their callees statically. Prefer proving the call path and register effects before invoking unknown services on hardware.

## Evidence classification

- **PROVEN_LOCAL:** none added by this document.
- **EXTERNAL_REPORTED_LIVE:** broad candidate-register SMU-authority write sweep with no reported DCLK/activity transition; `CC_UVD_HARVESTING` write attempt behavior.
- **EXTERNAL_STATIC_CLAIM:** Van Gogh region/table around `0x16be0..0x17000` and the candidate register references listed above.
- **WEAKENED_HYPOTHESIS:** `0x0900c004` as a simple standalone VCN cold-reset control.
- **UNRESOLVED:** the actual outer de-isolation/reset/power primitive and its owning firmware/service path.

## Safety / research discipline

- Do not copy external semantic labels without independent reconstruction.
- Do not turn this note into a new live-write plan automatically.
- Preserve separation between firmware acceptance, sequencer/domain status, de-isolation/register accessibility, VCPU execution, ring execution, and userspace codec availability.
- Any new live experiment should have a bounded scope, explicit controls, restoration procedure, and independent safety review.
