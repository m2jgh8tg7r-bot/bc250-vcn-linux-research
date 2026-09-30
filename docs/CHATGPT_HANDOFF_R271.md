# R271 — Historical R173/R180 artifact integrity and replay-readiness checkpoint

Updated 2026-10-01. This checkpoint extends R270 with a live, read-only integrity audit of the historical R173/R180 experiment artifacts still present on the user's BC-250 system.

It does **not** re-run R173 or R180, does not boot the historical experiment kernel, does not send a new PSP VCN firmware transaction, and does not modify registers, firmware, boot entries, or hardware state.

## Why R271 exists

R270 established the current ordinary Bazzite/amdgpu baseline:

- AMDGPU/GFX path works.
- Standard VCN DEC/ENC/JPEG exposure is absent.
- Standard VIDEO_CAPS returns EINVAL.
- Same-boot detected-IP-block logging includes PSP but not VCN/UVD/JPEG.

The next research goal is to reproduce, locally and in order, externally reported progress beyond the old local PSP boundary.

Before any replay, R271 verifies whether the historical R173/R180 boot artifacts that produced the known local PSP observations still exist intact and can be tied back to their original experiment identities.

## New local live evidence

### 1. Historical initramfs artifacts still exist

Local copies:

- `r173-request-observation/initramfs-7.2.3-r173-observation.img`
- `r180-load-response-observation/initramfs-7.2.3-r180-observation.img`

Matching /boot copies also exist:

- `/boot/initramfs-7.2.3-r173-observation.img`
- `/boot/initramfs-7.2.3-r180-observation.img`

### 2. Local and /boot copies are byte-for-byte identical

R173:

```text
SHA256=5998a6cb7000ae76fd6c95dd5f729fff77fcb686e660abcf1aac22a6a8b5bd61
LOCAL_BOOT_MATCH=YES
```

R180:

```text
SHA256=b6ef569b85e24a5dedc81b076e4d4f977538bde400fb31c7d13d0674bb84c007
LOCAL_BOOT_MATCH=YES
```

This closes the question of whether the historical /boot copies drifted from the retained working-directory copies: they did not.

### 3. R173 and R180 contain distinct amdgpu modules

R173 amdgpu:

```text
size=46855689
sha256=27f3d114330876c54fb40d730529d440a31ebbe5f1794c31ce200dc726197bf4
build_id=90c4d49de3e79d30f63c61f595245d57b7d1e3e9
```

R180 amdgpu:

```text
size=46857713
sha256=5185df438a65ae63cd4619e10e4ead2fd8fe8483538743d81b7acdb48c8de78a
build_id=9e4870cde4dfbec0c4dab01a3a7667bd1c153223
```

Result:

```text
R173_R180_AMDGPU_IDENTICAL=NO
```

This is expected and important: R180 is not accidentally just another copy of the R173 module. The observation instrumentation changed.

### 4. Both historical initramfs images were built for the same 7.2.3+ environment and include the same VCN firmware payload file

Both images report:

- kernel version target: `7.2.3+`
- modules root: `r137-modules-root/lib/modules/7.2.3+`
- added driver: `amdgpu`
- included firmware path: `/usr/lib/firmware/amdgpu/vcn_2_0_3.bin`
- firmware file size in image: `405952` bytes

This does not prove PSP-visible payload identity. It only proves the historical boot images were constructed against the same kernel/module base and included the same-named VCN firmware file at the same size.

### 5. Historical 7.2.3+ kernel images are still present

Retained copies include:

- `r136-boot-artifact/vmlinuz-7.2.3-ogc-r135.bzImage`
- `r138-boot-repair/vmlinuz-7.2.3-r138`
- matching files under `/boot`

The kernel image metadata identifies version `7.2.3+`.

### 6. Current installed module tree is not 7.2.3+

The current ordinary environment exposes only:

```text
/usr/lib/modules/7.2.1-ogc4.1.fc44.x86_64
```

Therefore, do not treat the old R173/R180 initramfs as directly compatible with the current userspace/kernel module tree merely because the files still exist.

### 7. No current BLS entry was found referencing R173/R180 in the captured audit

The scan of `/boot/loader/entries` did not return R173/R180/7.2.3 references.

Interpretation: the old experimental initramfs files remain under /boot, but the captured ordinary BLS configuration did not show an active entry referencing them.

This is reassuring for accidental-boot risk, but it is not yet a complete boot-path reconstruction.

## Relation to the historical local PSP evidence

Keep the old results intact:

- R173 proved a host-side VCN LOAD_IP_FW request with `ucode_id=57`, `command=6`, `fw_type=13`, `size=405696`, with equal host payload comparison.
- R180 observed 11 paired LOAD_IP_FW transactions; ten non-VCN requests returned zero status, while VCN ID57/type13 returned `0xffff0008`, placement zero.
- R182 confirmed that the amdgpu GNU Build ID loaded during the R180 experiment matched the prepared R180 artifact and that capture-manifest verification passed.
- R182 also recorded successful normal recovery to the baseline environment.

R271 does not replay those observations. It verifies that the retained historical artifacts are still structurally present and internally distinguishable.

## What R271 newly proves

```text
R173 local initramfs retained                           PROVEN_LIVE
R173 /boot copy byte-identical to local copy            PROVEN_LIVE
R180 local initramfs retained                           PROVEN_LIVE
R180 /boot copy byte-identical to local copy            PROVEN_LIVE
R173 amdgpu module extracted and identified             PROVEN_LIVE
R180 amdgpu module extracted and identified             PROVEN_LIVE
R173 vs R180 amdgpu are distinct                        PROVEN_LIVE
historical 7.2.3+ kernel images retained                PROVEN_LIVE
current installed module tree is 7.2.1 only             PROVEN_LIVE
current captured BLS entries reference R173/R180        NOT OBSERVED
historical R180 replay is safe/ready                    NOT YET PROVEN
```

## Important interpretation boundary

Do **not** infer any of the following from R271:

- that R180 can be booted safely today without additional checks;
- that the old initramfs is ABI-compatible with the current ordinary 7.2.1 environment;
- that firmware acceptance will reproduce;
- that the R180 `0xffff0008` outcome is still the present blocker;
- that the external GPCNT/RBC/reset-release observations are already locally reproduced;
- that VCPU first-fetch or execution has been proven.

## Next Codex objective

Before any historical replay, close provenance and boot-path reconstruction.

Recommended order:

1. Search retained R173/R180 manifests/logs for the exact current extracted identities:
   - R173 initramfs SHA256 `5998a6cb...`
   - R173 amdgpu SHA256 `27f3d114...`
   - R173 Build ID `90c4d49d...`
   - R180 initramfs SHA256 `b6ef569b...`
   - R180 amdgpu SHA256 `5185df43...`
   - R180 Build ID `9e4870cd...`
2. Tie those identities to the original same-boot capture and historical R182 statement that the loaded R180 module matched the prepared artifact.
3. Reconstruct the exact historical boot command line, kernel image, initramfs pairing, and known-normal recovery path.
4. Only after that, decide whether a one-shot attended R180 replay is justified.
5. If replayed, preserve strict A/B evidence:
   - normal baseline identity,
   - experiment module Build ID,
   - paired PSP transaction logs,
   - GPU/display/LAN state,
   - return to normal baseline.
6. Do not proceed to speculative GPCNT/SMN/MMIO work until a primary-source, target-matched acquisition method is available.

## Safety / stop rules

- No booting R173/R180 yet.
- No new PSP transaction yet.
- No direct harvesting/fuse manipulation.
- No speculative SMN/MMIO access.
- No assumption that retained files imply replay safety.
- Do not repeat a hung live trial.
- A replay decision must include exact kernel/initramfs/module identity plus rollback path first.

## Status

```text
STAGE=R271
RESULT=PROVEN_LIVE_HISTORICAL_ARTIFACT_INTEGRITY
STATIC_OR_LIVE=live read-only filesystem/initramfs integrity audit
HARDWARE_MUTATION=none
BOOT_MUTATION=none
PSP_TRANSACTION=none
R173_BOOT_COPY_INTEGRITY=proven
R180_BOOT_COPY_INTEGRITY=proven
R173_R180_MODULE_DISTINCTNESS=proven
R180_REPLAY_READY=not yet proven
VCN_PSP_ACCEPTANCE=current state unproven; historical R180 outcome was 0xffff0008
LOCAL_GPCNT=unproven
LOCAL_RBC_EXECUTION=unproven
LOCAL_VCPU_RESET_RELEASE=unproven
LOCAL_FIRST_FETCH=unproven
NEXT=close exact provenance and historical boot/recovery reconstruction before considering one-shot attended R180 replay
```
