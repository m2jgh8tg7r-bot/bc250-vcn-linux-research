# R249 — frame-delivery timing, initial source checkpoint

STAGE=R249
RESULT=PROVEN_STATICALLY; delivery measurements pending
STATIC_OR_LIVE=static source inspection
HARDWARE_ACCESS=separate authorized Q36 review; no video GPU access
HARDWARE_MUTATION=no boot options, firmware, drivers or clock changes
HARDWARE_FAILURE=NO_EVIDENCE
PROVEN=standalone harness queues output and drains at IDR/end-of-stream
REJECTED=using aggregate fps alone as proof of smooth per-frame delivery
UNPROVEN=measured delivery latency; full-player/VAAPI behavior; dedicated VCN
NEXT=bounded pipe-delivery measurement with ordinary previously validated clips

The unchanged R244 diagnostic harness copies completed frames into a queue, then sorts and emits the queue at the next IDR or end-of-stream. This can make output arrive in groups despite adequate average fps. The source observation applies to the standalone test harness, not automatically to the production VAAPI path. Timing measurements are still pending; this checkpoint preserves an independently reviewable finding before further work.

The user requests local saving and GitHub sharing at progress checkpoints because remaining weekly usage is low. Q36 completed a bounded review; consumer overhead/backpressure and uncontrolled cache/frequency effects will be recorded. Hash verification will be separate from timed delivery measurements. No boot-option/reboot-style test is prepared.
