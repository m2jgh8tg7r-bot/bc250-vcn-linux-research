# R265 — Extended VCPU execution-boundary handoff

STAGE=R265
RESULT=PROVEN_STATICALLY
STATIC_OR_LIVE=pinned source, historical samples, saved metadata and offline interpretation
HARDWARE_ACCESS=none by research checks; separate Q36 GPU compute
HARDWARE_MUTATION=none
PROVEN=R251–R264 source findings; distinct counter definitions; saved instance metadata; 18 matched offline checks and 66 hashed source inputs
UNPROVEN=live VCPU execution; cause of external observations; pre-ABL harvesting writer
NEXT=user requested stopping; publish verified checkpoint and await further instruction

The extension connects the startup boundary to normal idle shutdown, conditional partial-stop residue and the exact fence-test contract. These additions constrain interpretation of a reported snapshot or successful test return; they do not identify an actual hardware failure. Final findings and the source/evidence matrix are in the R265 handoff.

The latest positive GPCNT/RBC report materially demotes whole-domain VCLK absence and complete physical disconnection. Direct harvesting-clear variants are outside the main line. Cause, mirror and unrelated availability interpretations remain parallel. Priority is the VCPU instruction-fetch boundary, reset/isolation and bootstrap source. All primary hypotheses include support, contradiction, unknowns and discriminating A/B outcomes.

The public replay passed18 checks over66 source-file instances using the previously downloaded, hash-verified cache after the first fresh-download attempt received HTTP429. Private retained source and firmware are excluded from the default replay. No new hardware result is claimed.
