# R258 — Startup observation preconditions

STAGE=R258
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=pinned reference source and conditional scalar examples
HARDWARE_ACCESS=none
HARDWARE_MUTATION=none
PROVEN=9 source witnesses covering readiness freshness, power-helper errors and observation interfaces
UNPROVEN=actual stale status, PGFSM timeout, physical clock/power, or VCPU execution
NEXT=combine generation and phase provenance in the evidence contract

The normal startup readiness predicate tests a bit, not a transition. Its earlier busy expression preserves other input bits at the C expression level. A pre-existing ready bit is a conditional counterexample to treating the predicate alone as proof of a fresh start; hardware power/reset side effects are not modeled. The normal stop path explicitly clears status, so this is not evidence of a demonstrated stale-status defect.

The static power helper writes PGFSM configuration in both policy branches and discards the wait result. Therefore zero power-management capability flags do not mean zero power-state requests, and reaching a later source line does not prove the wait succeeded. No actual timeout was observed.

The sysfs `vcn_reset_mask` interface reports supported software reset methods, not live reset assertion. An indirect DPG write macro stages offset/value pairs in host storage; its name alone does not prove a target register transaction. The later PSP SRAM update uses the VCN RAM firmware identities, distinct from the regular VCN image and MMSCH identities.

The five scalar examples are logical illustrations only. R163 already modeled readiness-loop outcomes more extensively; R258 adds provenance/helper context and does not count these examples as new hardware trials.

The power-state wrapper has VF and same-software-state success returns before start/stop. A successful wrapper call does not even prove that a new start attempt occurred; cur_state is bookkeeping, not a measured physical state.
