# R182 results and R183–R185 static audit

## Current live boundary

R182 reused the fixed R180 module after user-reported power removal for several minutes. All 11 paired response patterns matched the earlier R180 capture. VCN still returned `0xffff0008` with zero placement; five other firmware types met placement-inclusive success-response conditions. The earlier boot's physical power history is unknown, so this is not a proven warm/cold causal comparison. Normal kernel/module recovery, GPU initialization and 1Gbps/full-duplex LAN were confirmed. Failed units returned to the two-service normal baseline. The user reported no display corruption/freezes during the experiment or recovery.

This supersedes the R182 pre-boot handoff's unexecuted/pending descriptions. VCN acceptance, VCPU/ring execution, VA-API and FFmpeg hardware decode remain unproven.

## R183: status domains

The observed value is a 32-bit GPCOM response field. Do not truncate it with a mailbox mask or assign names from HDCP/RAP interfaces. The inspected AMD-authored Linux header names cancellation and not-supported values but does not define `0xffff0008`. OP-TEE's matching item-not-found value does not identify Cyan's rejected object or internal failure stage. The existing unknown-status classification is retained.

Sources: [Linux PSP interface](https://raw.githubusercontent.com/torvalds/linux/master/drivers/gpu/drm/amd/amdgpu/psp_gfx_if.h), [Linux submit implementation](https://raw.githubusercontent.com/torvalds/linux/master/drivers/gpu/drm/amd/amdgpu/amdgpu_psp.c), [OP-TEE definitions](https://raw.githubusercontent.com/OP-TEE/optee_os/master/lib/libutee/include/tee_api_defines.h). Local retrieved bytes and SHA256 records are retained; master URLs may change.

## R184: official firmware history

The Navi10 VCN path history at official linux-firmware commit `d371ae3b6888b260e4c37b327a020401cfaaaefd` returned 21 commits with no next page. All 21 binaries were saved and independently rechecked offline for file/payload hashes, header bounds and CRC. They contain 21 distinct payloads, all with format 1.0 and IP 2.0 headers. The common header has no separate IP revision field; matching IP 2.0 does not establish Cyan 2.0.3 support. Hash/CRC checks do not validate PSP signature acceptance.

The current image is version `0x0811800d`, payload 405696 bytes, file SHA256 `a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5`. The preceding version is `0x08118009`, payload 404288 bytes. Unlike the three equal current Navi10/12/14 files, historical versions provide actual payload differences. Examined release messages do not establish Cyan compatibility or identify a preferred alternate candidate. Being older alone is not a selection rationale.

Sources: [fixed official path history](https://gitlab.com/kernel-firmware/linux-firmware/-/commits/d371ae3b6888b260e4c37b327a020401cfaaaefd/amdgpu/navi10_vcn.bin), [fixed catalogue](https://gitlab.com/kernel-firmware/linux-firmware/-/blob/d371ae3b6888b260e4c37b327a020401cfaaaefd/WHENCE). This is the returned path history, not all branches or renamed firmware history.

## R185: experiment readiness

A CPU-only substitution of the 18 distinct historical payload sizes into a copy of the verified live log showed that the current parser accepts only its fixed 405696-byte observation contract. The other 17 sizes were unproven. These are parser cases, not hardware trials. The R182 comparator also requires identical request sizes, so it must not be reused unchanged for version comparison.

A future alternate-version test needs a separate immutable profile and comparator, an explicit one-version selection rationale, unchanged non-VCN inputs and hardware guards, complete capture checks, and reviewed normal recovery. Existing R180 expectations must remain intact. Firmware size can also affect allocation layout; an observed difference would not uniquely establish a signature or policy cause.

|Observation|Allowed conclusion|
|---|---|
|VCN status zero, nonzero placement, completed fence; controls stable|Acceptance conditions in that captured configuration, not VCN execution|
|Different nonzero VCN status; controls stable|Response difference worth investigating, not a repair|
|Same failure|Those two versions/conditions did not meet acceptance conditions, not universal incompatibility|
|Controls changed or unexpected input/log differences|Comparison invalid for a VCN-specific conclusion|

No alternate firmware was selected, built into an image, installed or executed. The remaining priority is target-specific acceptance/support evidence or an explicit rationale for a limited exploratory version comparison. A maintainer question draft is stored locally and has not been sent.

Useful missing information: the meaning of this status in the Cyan LOAD_IP_FW ABI, support for firmware type 13, a compatible image/version, and an existing supported way to observe rejection prerequisites.
