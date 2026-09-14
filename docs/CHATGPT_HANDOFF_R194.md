# BC-250 VCN: additional evidence checks (R191–R194)

2026-09-14. Read [R186–R190](CHATGPT_HANDOFF_R190.md) for the AMD product-support statement, PSP-default history, official firmware catalogue, and five-project claim audit. This continuation adds static evidence about what reported success can actually establish. No new VCN hardware experiment or image was made.

## A zero return is not an acceptance receipt

A [2019 upstream change](https://github.com/torvalds/linux/commit/466bcb75b0791ba301817cdadeed20398f2224fe) deliberately retained warning-only handling of some nonzero PSP responses for compatibility with firmware behavior. In the [current submission function](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/gpu/drm/amd/amdgpu/amdgpu_psp.c#L726), a bare-metal submission can return zero despite a nonzero response. A skipped hardware-access path can also return zero without submission. Aggregate firmware-loading return values are not individual VCN acceptance records.

A [2026 PTL caller fix](https://github.com/torvalds/linux/commit/c13ff096437c6d470edf754c78e0cb83d24505fa) explicitly checks the response status after submission. This is a separate caller example, not a VCN fix. The historical compatibility rationale does not define Cyan's `0xffff0008` as harmless or identify its internal cause.

R180/R182 already recorded completion, raw status, returned placement, and non-VCN controls. Their VCN response remains `0xffff0008` with zero placement, so the project's acceptance-response conditions remain unmet.

## IP discovery and harvest are metadata

The [original harvest sysfs addition](https://github.com/torvalds/linux/commit/4d7ba312dd1f94cce23f1f93f33bdf92db090688) explicitly described inconsistent VBIOS harvest information at that time. A [2023 correction](https://github.com/torvalds/linux/commit/f2b8447b1f309901c3fdd4045febfe5cab545d87) changed reporting to use per-IP driver state.

| Reviewed source | Meaning of the reporting path |
|---|---|
| Upstream v6.19 and saved research source | Ordinary VCN harvest reporting derives from the driver's instance mask; it is not a physical VCN test. |
| Current fixed upstream HEAD | Early standalone sysfs passes a null device context and returns zero when harvest information is unavailable. Normal sysfs setup preserves the standalone instance. This newer path is absent from the saved research source and must not be retroactively assigned to its live captures. |

Current-source references: [harvest value](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/gpu/drm/amd/amdgpu/amdgpu_discovery.c#L1189), [early recursion](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/gpu/drm/amd/amdgpu/amdgpu_discovery.c#L1669).

The [early-export design](https://github.com/torvalds/linux/commit/402e04f11ff75fe4580a6e5f00622b58f4c544b9) intentionally retains IP information when driver probing fails. IP visibility or `harvest=0` therefore cannot, by itself, prove successful initialization, absence of manufacturing defects, or working decode. Neither can these sources establish a defect on the tested unit.

## Codec lists are a further software boundary

Both v6.11 and the fixed current upstream [nv_query_video_codecs](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/gpu/drm/amd/amdgpu/nv.c#L211) lack a VCN 2.0.3 case; that version reaches the default error branch. The [VIDEO_CAPS ioctl](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/gpu/drm/amd/amdgpu/amdgpu_kms.c#L1299) serializes the selected codec table rather than decoding a frame. These are static source findings, not new live ioctl results, and do not establish every possible userspace driver's behavior.

Adding an IP-registration case alone would not complete firmware, execution, and userspace support. No capability-table or runtime change was made to produce a superficial success result.

## Next evidence needed

A useful standard-PSP success report needs identifiable hardware/variant, source/module version, firmware identity, actual request and completion, response status and placement, and relevant platform conditions. Metadata, power claims, firmware placement, firmware acceptance, VCPU/ring execution, and correct video output must remain separate milestones. Compute-based VA-API results and altered PSP environments cannot substitute for an unchanged standard-PSP acceptance profile.

The next priority remains a target-specific firmware/support update, a same-condition acceptance control, or a definition of the specific Cyan response ABI. No demonstrably better alternate firmware candidate emerged. Historical payload comparison remains limited exploration. Existing evidence and fixed parsers are preserved; technical questions were drafted but not sent.

## 日本語要点

延長調査で、関数ret0・harvest0・codec一覧をVCN動作成功と取り違えない根拠を上流コードと原commitで確認した。現機の受理成功条件未達という結論は維持。新規VCN実験・image作成は行っていない。対応情報・同条件の受理成功対照・拒否ABI定義を次の入力として優先する。

```text
STATIC_OR_LIVE=STATIC
VCN_HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
STANDARD_PSP_VCN_ACCEPTANCE_ON_TESTED_UNIT=UNPROVEN
VCN_HARDWARE_EXECUTION=UNPROVEN
```
