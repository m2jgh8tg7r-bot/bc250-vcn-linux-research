# R321 — Final-base provenance and observation decision

STAGE=R321
RESULT=Parser samples, sysfs copies and helper-selected bases are distinct evidence; PGFSM uses segment 1
STATIC_OR_LIVE=PROVEN_STATICALLY; inherited R318 live checkpoint explicitly separate
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Last matching parser record assignment; sysfs base array copy; PGFSM CONFIG/STATUS segment-1 selection
REJECTED=Sysfs base array is the helper pointer; parser count3 alone proves final helper array length
UNPROVEN=Duplicate VCN records on this machine, final helper pointer/values, failed-read cause, VCPU execution
NEXT=Use saved full discovery evidence if available; optional bounded software observation only if it resolves a specific hypothesis

## Saved-source findings

1. amdgpu_discovery_validate_ip checks instance and hardware-ID ranges (749–767). It does not reject duplicate (hardware ID, instance) records. The parser assignment at 1663 keys by hardware IP and instance, not die. Later matching records therefore win. This is source semantics, not evidence that this board has duplicates.
2. The R311 parser message is emitted before pointer assignment and only for k < 3 inside the record's count-bounded loop. R318's received triplet attests that logged record. Without a complete record inventory, it cannot rule out a later assignment with a different count or values.
3. Sysfs creates a separate ip_hw_instance and copies each base into its own array (1254–1267). R308's normal-boot export is metadata from another boot, not direct attestation of the helper's reg_offset pointer.
4. SOC15_REG_OFFSET selects reg_offset[ip_HWIP][instance][BASE_IDX] then adds the register offset (soc15_common.h:36). Both PGFSM CONFIG and STATUS use BASE_IDX=1; their register offsets are 0 and 1 (vcn_2_0_0_offset.h:380–383).
5. Conditional on the observed triplet being the final selected array, CONFIG/STATUS dword addresses are 0x7e00/0x7e01, byte offsets 0x1f800/0x1f804. These are within the reported 524288-byte aperture. This arithmetic does not prove address validity, transaction completion or physical accessibility.

## Decision for further observation

Do not repeat CP06/CP07 or R318 unchanged. No live experiment is packaged or requested by this stage.
First prefer a retained full discovery capture from the relevant boot. A normal-boot capture may test normal metadata consistency but cannot settle a failed boot's state.
If a concrete final-pointer hypothesis warrants a future software-only checkpoint, associate the selected reg_offset pointer with its owning discovery record using validated allocation/table/record bounds, and derive its count from that record. Require a non-null pointer, matching hardware ID/instance, and count greater than BASE_IDX before dereferencing. Preserve the existing deliberate panic before helper VCN MMIO. Avoid treating the earlier logged count as a safe bound for an independently selected final pointer. Do not print kernel pointers into public logs.

## Publication correction

The previous conversational assessment that R319/R320 were not yet published was incorrect. Remote HEAD 2cf250fb already contains their individual handoffs. The stale STATUS entrance caused the mismatch; this stage updates that entrance. Raw user transcripts and machine-identifying information are not published.

No build, module load, register transaction, installation or reboot occurred.
