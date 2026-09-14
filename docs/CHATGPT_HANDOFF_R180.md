# BC-250 VCN research: R173 live findings and R180 next test

Updated 2026-09-14. R180 is prepared but **not installed or booted**. VCN hardware execution remains **UNPROVEN**.

## Live findings since R169

R157's guarded enrollment-suppression control was booted and collected. R171 then enabled only the existing VCN enrollment path while retaining the VCN/JPEG hardware-init and IB execution guards. R173 retained the same request and payload, adding a bounded host-memory observer. All three were followed by normal-entry recovery checks.

In R173, the loaded module GNU Build ID and same-boot kernel capture corresponded to the prepared artifact. The VCN request reported:

```text
ucode_id=57 command=6 fw_type=13 size=405696
source_aligned=1 source_matches=1
bo_present=1 map_present=1 iomem=0 map_matches=1
bounds_ok=1 header_ok=1 payload_checked=1 payload_equal=1
```

This proves the observed host request and CPU buffer comparison, not the bytes visible to PSP.

Both R171 and R173 reported status `0xffff0008`, zero returned firmware placement, matching expected/observed fence 12, remaining timeout, and Linux return 0. The status warning agreed with the recorded response. The PSP acceptance conditions were **not met**. Return 0 and fence completion do not establish firmware acceptance. The AMD-specific meaning of this status remains unknown; a same-valued constant from another TEE API is not a diagnosis.

Normal recovery restored the known normal kernel/module identity, GPU initialization, and 1Gbps full-duplex LAN. The user reported no noticed display corruption or freezes during R173 or after recovery. Two previously present failed services remained; long-term stability and cold recovery are unproven. Capture manifests were rechecked locally; raw logs and machine identifiers are not published.

## What the static work excludes

The host file, packaged payload, header bounds and CRC were consistent. R176 checked linux-firmware commit `d371ae3b6888b260e4c37b327a020401cfaaaefd`: Navi10/12/14 VCN files were byte-identical to the packaged candidate (405952 bytes, SHA-256 `a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5`). Renaming between these three does not test a different payload. That fixed catalogue did not list a Cyan-specific VCN image; this is not proof of worldwide absence.

The saved HDP wrapper can return before a hardware callback on a normal x86 APU path. R174 checked 512 CPU branch conditions. This does not diagnose missing coherence or justify a forced flush. R177 added ASan/UBSan checks to the unchanged host observer, covering 254 cases with no detected sanitizer failure.

R179 rechecked the two experimental captures. Only VCN has detailed per-request response evidence. No warning for other firmware loads is not direct evidence of their status values; fence 12 is not a list of the preceding command identities or results. The saved Cyan PSP function table contains five ring callbacks, without a bootloader/SOS loading callback, consistent with the [AMD-authored upstream implementation](https://raw.githubusercontent.com/torvalds/linux/master/drivers/gpu/drm/amd/amdgpu/psp_v11_0_8.c). Replacing a host firmware file is not established as a way to replace Cyan's trust OS.

## R180 experiment

R180 observes existing LOAD_IP_FW submissions for Cyan, preserving their type, payload, order and hardware execution guards. The source delta from R173 consists of a trace predicate and two log blocks in the existing submit function. Removing those blocks restores the R173 source exactly. No extra command, device access, mapping, flush or payload comparison is added.

Each begin records ID, command, firmware type, size, existing fence number and source alignment/match booleans. Each end records ID/fence, return code, submitted/copied-response flags, raw status, observed fence, timeout, RAS flag and a boolean for nonzero returned placement. The new records omit raw addresses.

A different firmware type with completed status-zero/nonzero-placement conditions, alongside a completed nonzero VCN response in the same loading interval, would establish a selective response pattern. It would not uniquely distinguish firmware incompatibility, missing PSP-side target, policy, resources or power conditions. If VCN changes to a success-shaped response, logging-induced timing differences remain an alternative; it is not automatically a repair.

Verification completed:

- 30,720 CPU cases comparing the exact R173/R180 submit functions: equal returns, command/response state, firmware metadata, fences, submission counts, invalidations and sleeps. The additional trace values were checked.
- The same 30,720 cases under ASan/UBSan with leak detection passed. This models host behavior, not device timing or a complete kernel.
- 371 parser cases covering missing/duplicate/reordered records, numeric bounds, wrong ID/fence, incomplete responses, warning contradictions and un-attributed data.
- Full module build, source restoration, signed initramfs, cryptographic signature verification and modified-content rejection.
- The sole packaged file difference from R173 is amdgpu.ko; archive contents, file modes, root ownership, module ABI and dependencies were checked.
- R173 and normal captures remain negative for R180 attribution. Modified captures and missing required manifest evidence were rejected.
- Six temporary-directory archive/recovery cases passed. No boot files were changed for R180.

The parser requires a single loading interval and one-to-one trace pairs, cross-checks the VCN pair against the retained R173 request and R142 response, and separates observation success from PSP acceptance and VCN execution. Runtime retries, overlapping records or out-of-interval traces require review.

## Next boundary

R180 awaits attended manual validation: install the reviewed fixed artifact, boot it once, collect module identity and same-boot logs, inspect display/GPU/LAN, then return to the known normal entry and collect again. Do not repeat a hung trial. No VCN execution guard is removed by this experiment.

```text
R173_HOST_REQUEST=PROVEN_LIVE
R173_NORMAL_RECOVERY=PROVEN_LIVE
R180_PREPARATION=PROVEN_STATICALLY
R180_LIVE_OBSERVATION=UNPROVEN
PSP_VCN_ACCEPTANCE=UNPROVEN
VCN_VCPU_AND_RING_EXECUTION=UNPROVEN
VAAPI_AND_FFMPEG_HARDWARE_VIDEO=UNPROVEN
ROOT_CAUSE=UNPROVEN
```
