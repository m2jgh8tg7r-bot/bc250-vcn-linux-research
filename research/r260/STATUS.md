# R260 — VCPU boundary handoff and reproducibility

STAGE=R260
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=consolidation of pinned static audits and synthetic interpretation
HARDWARE_MUTATION=none
PROVEN=see completed R251–R259 artifacts; no new live VCN result
UNPROVEN=VCPU execution, hardware decode, physical failure cause, pre-ABL harvesting writer
NEXT=continue extension-stage test/lifecycle audits; publish after the revised interval or an explicit interruption

The handoff distinguishes external attributed reports, current reference source, retained prior evidence and unresolved physical behavior. Stage counts are not hardware experiment counts. R250 remains incomplete; R249 remains a separate CPU checkpoint.

`REPLAY.md` explains public-source reproduction and explicitly excluded private inputs. This stage does not introduce a kernel patch, boot option or device experiment.

Core checkpoint complete: the public replay matched12 checks using65 hash-verified source-file instances, without private firmware or retained private source. Optional saved-firmware geometry was separately revalidated. Publication is still deferred under the extended schedule.
