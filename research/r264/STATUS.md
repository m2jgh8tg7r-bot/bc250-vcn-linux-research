# R264 — Cache access and trace labels

STAGE=R264
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=pinned public headers and two normal driver files
HARDWARE_ACCESS=none
HARDWARE_MUTATION=none
PROVEN=46 cache-related symbolic registers; six trace/identity definitions; bounded reference absence
UNPROVEN=what interface the external report used; trace sampling semantics; physical VCPU instruction execution
NEXT=retain these distinctions in the final evidence matrix

The external phrase “VCPU cache register” does not identify a single interface. The reference header contains BAR, OFFSET, SIZE and VMID names, with DPG and noncache variants. Readback of a mapping configuration register differs from reading backing bytes through an aperture, and both differ from VCPU instruction fetch. The 46-symbol inventory records relative dword offsets and base-index selectors only; it does not construct absolute device addresses or an acquisition procedure.

The header names UVD_VCPU_TRCE.PC (28-bit field), UVD_VCPU_TRCE_RD.DATA, VCPU identity and trace-control fields. Neither inspected vcn_v2_0.c nor amdgpu_vcn.c references the trace, trace-data or identity symbols. No sampling/validity contract for them is established by these files. This is a bounded two-file observation, not a claim that the registers are unusable or absent from other software.

A header field named PC is not by itself a documented live instruction-retirement counter. Trace selection, freshness, access side effects, inactive-state behavior and exact BC250 applicability remain unresolved. A zero or unchanged value cannot be promoted to “never executed,” and a changing trace-like value still needs attribution. No trace activation or register write is proposed or performed.

The useful next input is precise identification of the already-used external cache/ring interfaces, their mapping and test result, rather than guessing a cache-data interpretation from the report's wording. No independent raw capture was supplied in this session.
