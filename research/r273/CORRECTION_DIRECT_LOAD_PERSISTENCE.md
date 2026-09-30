# R273 correction — external direct-load persistence

R273 established that amdgpu contains a native non-PSP VCN provisioning architecture. That static conclusion remains valid.

A later R274 audit found two points that narrow the interpretation of the Shalasere external direct-load report.

## Native placement

The native `amdgpu_vcn_resume()` non-PSP path copies ucode to the VCN BO base.

The separate `AMDGPU_UVD_FIRMWARE_OFFSET=256` value is programmed into the VCPU cache-offset register by `vcn_v2_0_mc_resume()`; it is not used as the CPU destination offset in the native VCN copy path.

Therefore R273 wording that described the native software copy itself as placing payload at BO+256 was too strong and is superseded by R274.

## Published Shalasere source lifecycle

At external commit `6c85b2fe382599ec80d6222b5ffe70eabb97457b`:

1. `amdgpu_vcn_sw_init()` copies VCN ucode to BO+256 and logs completion.
2. `vcn_v2_0_sw_init()` then calls `amdgpu_vcn_resume()`.
3. the published `amdgpu_vcn_resume()`, with global PSP load type and no saved BO on initial init, clears the full VCN BO.

Therefore:

```text
external copy attempt/log completion       EXTERNALLY_REPORTED
external post-resume BO payload persistence UNPROVEN
external VCPU-visible payload              UNPROVEN
external first fetch/execution             UNPROVEN
```

This correction does not invalidate the broader external observations such as amdgpu loading or DRM-node emergence. It only narrows what the published direct-copy log proves.

R273's key local conclusion remains:

```text
a native non-PSP VCN BO provisioning architecture exists in amdgpu
```

but local implementation should follow the native copy/layout semantics rather than infer BO+256 from the external patch.
