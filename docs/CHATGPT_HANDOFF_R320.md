# R320 — Discovery offset lifetime audit

STAGE=R320
RESULT=Discovery bases have device-owned heap lifetime; no normal-path early free found in inspected source
STATIC_OR_LIVE=PROVEN_STATICALLY source ownership and assignment; R318 live evidence inherited separately
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Heap allocation, in-buffer pointer assignment, failure/teardown free sites, parser overwrite semantics
REJECTED=Parser-local pointer automatically expires on return; VCN info getter replaces register bases
UNPROVEN=Final live pointer contents, exhaustive alias-write absence, past hanging-read cause, VCN execution
NEXT=Prioritize observation provenance over repeated MMIO; final-pointer observation remains optional, not a test request

## Scope and method

Inspected retained R310 build-tree AMD driver source, without changing source, building, loading modules or accessing registers. Searches covered reg_offset references/assignments, discovery.bin ownership, base_address assignments and discovery_fini callers. This is source review, not formal whole-program alias analysis. Prior R319 flag interpretation remains unchanged.

Paths below are relative to drivers/gpu/drm/amd/.

## Ownership

- amdgpu/amdgpu_discovery.c:346 allocates adev->discovery.bin with kzalloc.
- The register parser (1498 onward) first calls discovery_init, propagating its error; it then derives ip from the retained allocation (1552).
- It converts base entries in place (1644/1647), logs inside the count-bounded loop, then assigns reg_offset[hw_ip][instance] = ip->base_address (1663).
- Therefore the stored target is not stack storage. Returning from the parser does not itself invalidate it.
- Initialization failure frees the allocation and nulls the owner (732–733). Successful discovery_init returns before that failure block.
- discovery_fini removes sysfs then frees/nulls the allocation (742–746). The only external caller found in the AMDGPU C/header scan is amdgpu_device_fini_sw (amdgpu_device.c:4350, call at 4405), after MMIO unmapping.
- No normal successful-initialization early free was found in this inspected path. This does not prove absence of corruption or all possible concurrent lifetime faults.

## Later writers and consumers

The direct reg_offset assignment scan outside fixed *_reg_init.c tables found the generic discovery assignment. Fixed ASIC tables exist, but R319 established the Skillfish2 discovery branch rather than the alternative fixed Cyan branch. Searches are syntactic and cannot exclude every indirect/aliased write.

The immediate Cyan post-parser calls harvest IP, get GFX info, get MALL info and get VCN info. In particular, amdgpu_discovery_get_vcn_info (1932–1985) writes codec-disable-mask metadata, not the base pointer or base-address entries. The nearby amdgpu_device.c discovery.bin references at 1880/1885 are presence checks for GPU-info handling, not frees.

One important limit remains: the parser loops over dies/IP records and assigns by hardware IP plus instance, without including die in the reg_offset key. A later matching record can replace an earlier pointer. This is a structural observation, not evidence of duplicate VCN records on this machine. R318 visibly logs one VCN instance-0 triplet; it does not constitute an independently captured full discovery image or a final helper-side pointer read.

## Interpretation and next-step decision

The temporary-buffer-expiration explanation is not supported by the reviewed ownership path. Discovery-backed bases surviving to the intended helper checkpoint are strongly supported under the normal initialization path, while final live values remain unproven.

R318 already achieved its intended metadata/panic observation. No repeat of CP06/CP07 or another R318 boot is requested. A future final-pointer observation, if required to distinguish a concrete hypothesis, should remain software-only, preserve count/bounds provenance, and precede the existing planned panic. No such package was created here. Do not add a live MMIO read merely to resolve this software-pointer question.
