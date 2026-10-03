# R319 — R318 live checkpoint and software-field audit

STAGE=R319
RESULT=R318 intended metadata panic received; software fields mapped to retained source
STATIC_OR_LIVE=User-supplied live transcript plus offline source inspection
HARDWARE_ACCESS=NONE by agent in this stage
HARDWARE_MUTATION=NONE by agent in this stage
HARDWARE_FAILURE=UNPROVEN
PROVEN=PROVEN_LIVE R318 markers, panic=0, helper/guards/META/named panic; PROVEN_STATICALLY software flag definitions and discovery assignment
REJECTED=Zero pg/cg flags prove physical power-off; display warning proves terminal fault; old UNCALLED comment describes current control flow
UNPROVEN=VCN execution, physical power/clock state, past R312/R316 panic identity, final live reg_offset contents
NEXT=Audit later writers and lifetime of discovery-backed offsets; no repeat of unchanged hanging reads

## Live result (2026-10-04)

User supplied a fresh PowerShell console transcript and explicitly confirmed actual R318 boot and manual-reset recovery.
This supersedes R318 preparation-only status. No independent post-reset health audit is claimed.

- Command line contains panic=0; qualification markers identify R318 NETHOLD.
- Seq 924–926: instance 0, count 3, bases 0x7800 / 0x7e00 / 0x02403000.
- Seq 1181–1183: pre_reset begin, helper_entry, guards_pass.
- Seq 1184 at 47665961 us: apu=0x40 pg=0x0 cg=0x0 no_hw=0 aperture=524288.
- Seq 1185: META complete before helper VCN MMIO.
- Seq 1186 at 47665979 us: Kernel panic - not syncing: BC250 R311 metadata checkpoint before helper VCN MMIO.
- Seq 1255 at 47670383 us: matching end Kernel panic line.
- Visible sequence runs are 0–275 and 900–1255. 276–899 (624 records) are absent from the pasted transcript. Missing prefix/interior records do not invalidate the explicit named checkpoint, but full capture completeness is unproven.
- Receiver command prints decoded UDP data only; it does not save raw datagrams. Network loss cannot be separated from console/copy omissions using this evidence alone.

The observation objective is met. The end marker proves receipt of that marker, not that every possible later record was captured. R318 supports the R317 panic-flush ordering explanation, without proving the actual flush call or retroactively identifying prior boots' terminal paths.

## Static interpretation

Paths below are relative to the retained R310 build tree.

1. drivers/gpu/drm/amd/include/amd_shared.h:53 defines AMD_APU_IS_CYAN_SKILLFISH2 as 0x40. amdgpu/amdgpu_device.c:1592–1595 sets this bit for Cyan PCI IDs 0x13FE or 0x143F.
2. amdgpu/amdgpu_discovery.c:3060–3070 selects discovery register initialization for that bit; the fixed Cyan table is the else branch. The observed parser messages independently show discovery parsing on this boot.
3. amdgpu/nv.c:833–836 sets cg_flags and pg_flags to zero for GFX 10.1.3/10.1.4. This agrees with the live scalar values, but does not prove this is the only writer or measure physical gating.
4. amdgpu/vcn_v2_0.c:530–534 returns for nonzero pg/cg or SR-IOV VF. The received guard marker and scalar values establish passage of these guards for this run. no_hw=0 is a software flag; aperture=524288 is the mapped aperture size, not proof that each register responds.
5. include/soc15_hw_ip.h:33–34 aliases VCN_HWID to UVD_HWID (12). amdgpu_discovery.c:246 maps UVD_HWIP to that ID. At 1663–1664 the parser assigns reg_offset to the converted base_address array, after the bounded logging loop. This closes the naming/assignment connection statically. It is not a live read of the final pointer or a proof against later mutation.
6. vcn_v2_0.c:325 calls the helper; its line 504-era comment says intentionally UNCALLED and is stale. Source was preserved unchanged. Runtime markers and panic trace supersede that comment.
7. The intended panic is before this helper's first VCN MMIO. Earlier initialization has already performed hardware operations; this is not a claim of no hardware access throughout the boot.

## Decision

Do not classify the display IRQ warnings as the terminal failure: this run continued beyond them to the deliberate panic.
Do not request another R318 trial merely to repeat an achieved observation.
Continue static provenance/lifetime checks before considering a different, discriminating hardware observation.
