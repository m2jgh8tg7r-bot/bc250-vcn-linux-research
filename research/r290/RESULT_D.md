# R290-D result — modeled 0xffff0008 response preservation

Date: 2026-10-01

A Linux host-side C model was used to exercise the already-audited response ordering for the isolated VCN probe.

Model result:
- build: PASS
- generic return: -22 (-EINVAL)
- PSP status: 0xffff0008
- TMR address: 0x0
- CommandsDone: 1
- normal Loaded state: retained
- RingUp state: retained
- TmrUp state: retained

Explicit checks:
- PSP_STATUS_PRESERVED=YES
- ZERO_PLACEMENT_PRESERVED=YES
- COMMAND_COMPLETION_RECORDED=YES
- BASELINE_PSP_STATE_RETAINED=YES
- R290_D_RESPONSE_MODEL=PASS

Artifacts:
- r290d_response_model.c SHA256:
  67f66592864881f6d59b9aebc442bee509807e29dac1d2ef5d06aff780309caf
- host model binary SHA256:
  3531c3dd936403b92c5ee82f7a84f7599a556459e58bd0afa8abbcb72e96aa7e
- log SHA256:
  3a7677f5da09387a0ae8e5a15d7a615b5da0db00a5fc5d7e19471e371af2c384

Interpretation:
This is MODEL proof only. It proves that when a completed PSP command yields status 0xffff0008 and fw_addr 0, the R290 response-handling contract can preserve those diagnostic values while surfacing -EINVAL and keeping the previously-good PSP loaded/ring/TMR state unchanged.

It does not prove that a Windows BC-250 PSP will actually return 0xffff0008 for VCN type 13. That remains untested until a future real Windows-side probe is run.
