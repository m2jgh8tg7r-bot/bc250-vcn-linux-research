# BC-250 VCN: support evidence and upstream history (R186–R190)

Updated 2026-09-14. This static research updates [R185](CHATGPT_HANDOFF_R185.md). No new hardware test, firmware installation, kernel image, or reboot was performed. VCN execution remains unproven.

## What changed

A July 31 AMD developer reply provides product-specific context: VCN was outside the BC-250 product definition; the reply says firmware was unavailable for it and that BC-250 uses signed firmware through standard PSP loading. The remarks about possible individual-chip defects and PMFW/VBIOS support are explicitly uncertain. They do **not** establish a defect, permanent disablement, or impossible power-up on the tested unit. The reply does not define `0xffff0008`. [Original AMD reply](https://www.mail-archive.com/amd-gfx@lists.freedesktop.org/msg148015.html)

The reply quotes a question that assumes DIRECT loading. That quoted assumption is not the developer's conclusion. Upstream history resolves the distinction: Cyan Skillfish2 initially had a temporary DIRECT default; a subsequent July 2021 commit enabled PSP loading by default once the PSP firmware was ready. PCI ID `1002:13FE` selects the Skillfish2 flag. The normal default parameter therefore selects PSP. [Temporary default](https://github.com/torvalds/linux/commit/c5d0aa482e10d669437c2b660ecda5ee6ee448e1), [PSP default transition](https://github.com/torvalds/linux/commit/b8e42844b48d441589eb18ade29dee29bbd78657), [variant mapping](https://github.com/torvalds/linux/commit/dfcc3e8c24cc1fcdf9e14ef98803e295b5e4f721)

## Driver and distribution evidence

| Evidence | Finding and limit |
|---|---|
| Original Cyan IP registration | No VCN/JPEG registration in the initial block list. [Commit](https://github.com/torvalds/linux/commit/f36fb5a0e3611aaf2e68623fc12fae41c4990de5) |
| IP-discovery registration | The original UVD 2.0.3 case adds no multimedia block. That empty case is also present in reviewed v6.11, v6.19, and current fixed-HEAD snapshots. This is not an exhaustive proof across every intermediate revision. [Original](https://github.com/torvalds/linux/commit/795d08391b8627603c8327391ae3ea8fb0d0293a), [current snapshot](https://github.com/torvalds/linux/blob/704340f1cd0dcef829eb62f5b48ae95a2ce17bdf/drivers/gpu/drm/amd/amdgpu/amdgpu_discovery.c#L2909) |
| Display support | The display change adds display IP 2.0.3, not VCN 2.0.3. [Commit](https://github.com/torvalds/linux/commit/fe04957e26e7a633e0b4052590c5c6a1d5cb3e89) |
| SMU support | The 2025 change retains SMU registration for Skillfish2; its title should not be read as disabling BC-250 SMU. [Commit](https://github.com/torvalds/linux/commit/94bd7bf2c920998b4c756bc8a54fd3dbdf7e4360) |
| Official firmware catalogue | The September 12 fixed WHENCE lists eight Cyan-named GFX/SDMA files, with no Cyan-named VCN/JPEG or VCN 2.0.3 entry. This does not prove absence under every other name or in nonpublic distribution. [WHENCE](https://gitlab.com/kernel-firmware/linux-firmware/-/blob/d371ae3b6888b260e4c37b327a020401cfaaaefd/WHENCE) |

The August 2026 Navi10 VCN update postdates the AMD reply, but its release chronology does not establish Cyan compatibility. It is the current payload already observed in R180/R182. The 21 historical official payloads audited in R184 still lack a target-specific compatibility basis.

## Public success claims reviewed

Five repository documentation sets were checked at fixed commits, with releases/issues inspected for the first three. No unchanged-standard-PSP VCN acceptance profile suitable for the tested board was obtained in this scope.

- **thelamer/bc250-lab-image:** release text explicitly describes VCN bring-up as unproven; the findings document contains a template, without an actual result. [Release](https://github.com/thelamer/bc250-lab-image/releases/tag/v0.3.0)
- **daveconde/bc250-vcn-enable:** describes a DIRECT route. Its September 11 issue proposes future observations and does not supply a completed success result. [Issue](https://github.com/daveconde/bc250-vcn-enable/issues/2)
- **simpmix/bc250-encoding-decoding-fix:** the current README and development log describe Vulkan-compute encoding. VA-API or hardware-acceleration wording does not establish VCN execution. [Fixed README](https://github.com/simpmix/bc250-encoding-decoding-fix/blob/125803198b0c67efbe895a94667001a0eb3b8075/README.md)
- **thelamer/bc250-vcn:** describes a DIRECT firmware-placement workaround and blocked decoder-ring execution. [Fixed README](https://github.com/thelamer/bc250-vcn/blob/e53aa40d8a51c11a1a0fa939928164938924c4b0/README.md)
- **Shalasere/bc250-vcn-research:** the latest README's authentication-success claim depends on an altered PSP execution context. It is not evidence for acceptance in an unchanged standard loading environment. Only claim context was reviewed; no bypass implementation was investigated or reproduced. [Fixed README](https://github.com/Shalasere/bc250-vcn-research/blob/cf153bf49c1ce945cefe834798e4e47fb92bba9c/README.md)

This audit does not establish worldwide absence of success, and external reports are not live verification by this project. An inaccessible issue-comment API and private community messages remain unverified.

## Implication for the next experiment

The saved live baseline remains R180/R182: command 6/type 13, completed response fence, VCN status `0xffff0008`, zero placement; five other firmware types satisfy placement-inclusive response-success conditions. The reported power-removal boot matched all 11 response patterns. Normal recovery and no noticed display corruption/freezes were confirmed previously.

Priority now goes to one of these new inputs:

1. A public BC-250-compatible firmware/support update with exact revision and prerequisites.
2. A same-variant standard-PSP acceptance record identifying firmware hash, request/response, completion, placement, and relevant platform conditions.
3. A definition of `0xffff0008` in the specific Cyan GPCOM ABI or a supported read-only capability diagnostic.

Without such evidence, comparing an old Navi10 payload remains limited exploration, not a demonstrated increase in success probability. Any future comparison must use a separate immutable profile and preserve the existing R180/R182 evidence and parsers. No alternate candidate or image was selected in this session. Updated maintainer questions were drafted locally and were not sent.

## 日本語要点

AMDの製品固有の説明と上流履歴を確認した。BC-250は標準PSPロードが既定だが、VCNは製品定義の対象外で、対応firmware不在との説明がある。現行上流でもVCN 2.0.3は未登録。公開の成功表現はcompute・DIRECT・変更されたPSP条件を区別し、当機へ使える標準PSP成功条件は得られなかった。物理故障や永久的な動作不能は未証明。次は対応情報・同条件の成功対照・拒否ABI定義を優先する。

```text
STATIC_OR_LIVE=STATIC
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=NO_EVIDENCE
STANDARD_PSP_VCN_ACCEPTANCE_ON_TESTED_UNIT=UNPROVEN
VCN_HARDWARE_EXECUTION=UNPROVEN
```
