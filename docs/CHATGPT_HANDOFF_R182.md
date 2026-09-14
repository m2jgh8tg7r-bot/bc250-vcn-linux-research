# R180 live results and R182 next experiment

Updated 2026-09-14. This supersedes the pre-boot status in the R180 handoff. R180 was installed, booted, captured, and returned to the normal kernel. The user reported no display corruption or freezes during R180 or after recovery. VCN execution remains **UNPROVEN**.

## What R180 established

The loaded amdgpu GNU Build ID matches the prepared R180 artifact in the same captured boot. The parser verified all 14 capture-manifest hashes and 11 paired existing LOAD_IP_FW observations, with no trace inconsistencies. No new PSP transactions were introduced by the comparison instrumentation.

| Host ucode ID | PSP firmware type | Request bytes | Response status | Placement nonzero |
|---|---|---|---|---|
| 1 | 9 | 33536 | `0x00000000` | 0 |
| 2 | 10 | 33536 | `0x00000000` | 0 |
| 12 | 3 | 263040 | `0x00000000` | 1 |
| 13 | 2 | 263168 | `0x00000000` | 1 |
| 14 | 1 | 263168 | `0x00000000` | 1 |
| 26 | 4 | 267440 | `0x00000000` | 1 |
| 27 | 5 | 896 | `0x00000000` | 0 |
| 28 | 4 | 267440 | `0x00000000` | 1 |
| 29 | 6 | 896 | `0x00000000` | 0 |
| 50 | 8 | 25088 | `0x00000000` | 0 |
| 57 | 13 | 405696 | `0xffff0008` | 0 |

All 11 observations had ret=0, submission and copied response present, matching fence completion, remaining timeout, and no observed RAS interruption. Ten non-VCN responses had status=0, but only five also had nonzero placement. Do not describe all ten as having met the project's placement-inclusive acceptance conditions.

VCN ID57/type13 had 405696 request bytes, status `0xffff0008`, zero placement, fence 12 completion, and timeout remaining 19998. R173's bounded host payload comparison remained positive. This proves a selective response pattern, not PSP-visible payload identity or a unique cause. VCN acceptance conditions were not met. Firmware incompatibility, a PSP-side missing target, policy, and power conditions remain unresolved.

GPU initialization and 1 Gbps/full-duplex Ethernet were captured. Normal recovery restored the baseline kernel and loaded GPU module identity. The normal failed-unit list returned to its previous two entries (CU manager and TDP service), rather than the experimental boot's six. User-reported visual stability is not long-term stability or physical cold-recovery proof.

## R181: reset and evidence boundaries

The fixed Cyan PSP source has ring create/stop/destroy/get/set callbacks, without mode1_reset or SOS-load callbacks. Its mode1_reset wrapper has a false/numeric-zero fallback when the callback is absent. Ring recreation and wrapper zero are therefore not proof of a global PSP reset. The Linux path waits for an already-ready trust OS. This does not establish what the platform firmware resets during reboot. [AMD-authored upstream source](https://raw.githubusercontent.com/torvalds/linux/master/drivers/gpu/drm/amd/amdgpu/psp_v11_0_8.c).

The attributed R171, R173, and R180 capture manifests were checked. They use different instrumented modules and do not form a fixed-binary warm/cold comparison. A new boot ID does not establish physical power removal. The prior boot methods are awaiting user confirmation; they are not assumed to be warm restarts.

## R182: prepared, not executed

R182 reuses the exact installed R180 kernel/module/firmware and existing boot entry. It adds an offline comparison tool and a read-only boot-file preflight, not a new driver image. The next attended experiment is a normal shutdown followed by removal/restoration of power supply and a manual R180 boot. The user records the actual operation and approximate off duration. Physical supply removal is a user report, not measurement of internal rails or PSP memory loss.

The comparator requires different boot IDs, matching module/kernel identity, exact command line and request sequence, valid existing R180 observations, and verified capture hashes. Boot-method records are bound to the capture manifest and boot ID. Missing history remains unknown. It compares VCN and controls separately and separates exact remaining-timeout counts from completion/failure conditions.

Thirteen new unittest methods (including subtests) passed, covering provenance, malformed or mismatched inputs, tampered/missing evidence, response changes, and read-only file checks. The inherited R180 parser's 371 synthetic cases also passed. These are CPU tests, not 384 hardware experiments. A real normal-boot capture was rejected by the comparison CLI. No new cold-start comparison has been collected.

All 49 locked local inputs and three readable installed files match. Root-only installed image and GRUB-environment rereads remain pending terminal authentication. The preflight fails closed until those checks pass. No boot files, default selection, services, or hardware registers were changed during this preparation.

An unchanged cold-start response would show failure to meet acceptance conditions in that recorded condition; it would not rule out every power hypothesis. A changed VCN response with stable controls would motivate further investigation, not prove a fix. Power cycling also changes elapsed time and temperature, so one pair cannot isolate residual power or establish causality/reproducibility. VCN/JPEG hardware guards remain in place, including if a response takes a success-shaped form.

Next: attended read-only preflight, manual cold-start R180 observation, comparison and GPU/LAN/display review, then normal recovery. VCPU execution, hardware rings, VA-API, FFmpeg decode, and sustained video playback remain unproven. Raw personal logs, machine identifiers, and private keys are not published.
