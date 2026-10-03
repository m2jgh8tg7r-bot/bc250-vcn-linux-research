# R339 — Future sampled-RIP reference, not a new observation

STAGE=R339
RESULT=Saved linked-kernel PCI instruction offsets indexed for unambiguous future sample interpretation
STATIC_OR_LIVE=PROVEN_STATICALLY; no actual sampled R329 RIP exists
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Exact pci_conf1_read instruction sites preserved against R332 text hash
REJECTED=Call-trace occurrence/return address is equivalent to sampled RIP; a sampled IO site alone proves hardware stall cause
UNPROVEN=Future sample collection, artifact attribution, runtime code/backend state and physical failure cause
NEXT=Use reference only for genuinely independent sampled RIP with artifact/boot/CPU provenance; no live retry

## Reference sites

For retained research-kernel pci_conf1_read size0xe9, lock-call instruction is offset0x4c; address-port32-bit output at0x79; unlock-call instruction at0xa5; data-port32-bit input at0xbe. Byte/word input alternatives are separately indexed in PCI_SAMPLE_REFERENCE.json. For R329's requested4-byte read, the dword data-input path is the relevant ordinary branch. Addresses in the underlying linked file are link addresses, not live KASLR addresses. Use symbol+offset only after same artifact attribution.

A sampled RIP at a port IO instruction identifies a sampled instruction site, not automatic proof that the instruction has been issued indefinitely or why a device/fabric failed. Sampling at a lock-call site does not establish lock ownership; execution actually waiting may be inside a generic lock function. Conversely a generic queued-spinlock sample requires surrounding stack/CPU and ownership evidence to link it to pci_config_lock; the name alone is insufficient. A call-trace line may be a return address rather than the actual sampled RIP and cannot be substituted.

Require full watchdog/sample context, affected CPU/boot, exact kernel/module provenance, sample RIP and stack distinction, symbol size and code correspondence. Reject unrelated display warning traces, prior R325 records and unsupported raw KASLR addresses as evidence of the R329 post-read location. Unknown/mid-instruction/unmatched offsets remain unknown. Multiple same-site samples strengthen persistence at the site only when timing and provenance are known; no synthetic reference supplies a live sample.

Current R329 transcript contains earlier display warning RIPs then progresses to helper/post-read begin. Those warnings are not terminal PC samples. No PCI watchdog RIP was received. This reference is preparation for interpreting an independently qualified future capture, not readiness to repeat the trial. R338 says serial electrical/output qualification remains missing; R337 independent durable route is unprepared; R336 watchdog constraints remain.

User continues static work; this week's more-live-tests prohibition remains. No new build, image, installation, boot argument, watchdog/backend setting or hardware operation. All results are shared and remote content verified; R335 remains broad restart summary, and R339 is the newest artifact reference. Quota is not observable, Q36 allowed but not needed for these deterministic instruction checks.
