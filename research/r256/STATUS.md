# R256 — observation interfaces are not execution certificates

STAGE=R256
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=pinned source, with separate passive host parameter observation
HARDWARE_ACCESS=passive module metadata; Q36 GPU_COMPUTE; no VCN register/debugfs read
HARDWARE_MUTATION=none for research target
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=9 source checks; 33-register dump coverage; firmware-log consumer side effect
REJECTED=0444 implies side-effect-free; host log header or Active label proves VCPU execution; empty log proves no instruction executed
UNPROVEN=external firmware logging support, fresh log production and VCPU execution
NEXT=integrate existing evidence and refine the exact missing same-boot observations

The reference firmware-log initialization is host code: it initializes the header, sizes, both pointers and wrapped flag. Those values alone cannot serve as a VCPU heartbeat. The read handler advances the shared read pointer despite the file's0444 permission. Thus a read can consume existing log evidence. Empty output due to equal pointers is not proof that firmware never ran; disabled logging instead follows an error gate and should not be mislabeled as an empty successful read.

The register-dump path separates collection from printing. Collection first reads power status and conditionally reads the remaining registers; printing uses saved `ip_dump` values. The Active/Inactive label evaluates a tile-off predicate, not VCPU instruction execution. No actual stale or uninitialized dump is alleged.

The pinned VCN2 register list has33 entries, but lacks VCPU control, soft reset, firmware cache BAR/OFFSET/SIZE0 and RBC_RB_CNTL. It cannot alone supply the full tuple requested by the new external report. Register indices also need the matching ASIC mapping; names or BASE_IDX values alone are not physical addresses.

Passive host metadata at13:30 UTC reports the existing kernel release and default-selecting fw_load_type=-1; these do not identify effective PSP loading mode or every loaded module byte. A later passive parameter read found vcnfw_log=0. No debugfs file was opened, logging enabled, VCN register read, kernel changed or boot test prepared.

A short Q36 review agreed with the six supplied ACCEPT/CHALLENGE classifications. Its speculative examples for empty output were not adopted: the source distinguishes disabled-logging error from equal-pointer EOF. Independent source checks are the evidence.
