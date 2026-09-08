# R124 — Dynamic Domain6 policy-table trace

This note records confirmed **static reverse-engineering** findings from the local Robin1 / SMU 88.6.0 analysis. No hardware access, SMU command, PSP operation, MMIO access, or VCN state change occurred in these stages.

## R124A — dynamic policy-table geometry

The recovered policy list spans:

```text
base  = 0x00013ed4
end   = 0x00013fc4
delta = 0x000000f0
count = 20 entries
```

Domain-6-related slot IDs are present in the generic list:

```text
slot 0x18 -> entry 10
slot 0x16 -> entry 14
slot 0x17 -> entry 15
```

The image-resident OLD/TARGET storage for these entries is zero-filled. These are mutable runtime-storage initial contents and do **not** by themselves prove that boot policy requests all three slots off.

## R124B — runtime policy applicator

The policy table is processed indirectly by base+index, so individual slot16/17/18 element addresses have no direct code xrefs in the current Ghidra database.

The central applicator is `FUN_0002e448`.

Its recovered semantics are:

```text
for each policy slot:
    read desired/target value

    if target == 0:
        FUN_00023730(slot)
    else:
        compare current vs desired
        if a state update is required:
            FUN_0002362c(slot, value)
```

This connects the previously recovered slot-off path to the generic dynamic-policy engine rather than to a VCN-specific fixed call site.

## R124B/R124C — profile source and target architecture

Recovered pointer values:

```text
policy profile source = 0x00007b54
policy state base     = 0x00013ed4
policy state end      = 0x00013fc4
policy target array   = 0x00014020
```

`FUN_0002e69c(param)` acts as a profile loader. It stores the selected profile index and loads a 20-element profile into mutable policy-target storage from a profile-indexed source region.

One normal wrapper is:

```text
FUN_0002e190(param)
    -> FUN_0002b018(param)
    -> FUN_0002e69c(param)
    -> ...
```

The wrapper passes `param` unchanged into the profile loader.

A second call to `FUN_0002e69c` exists at `0x0002e3ed` in code not currently assigned to a function by the existing Ghidra project. Nearby, `FUN_0002e448` appears as a parameter reference around `0x0002e3f5` associated with a call to `FUN_0001b1e4`, and a data reference to the applicator exists at `0x000181dc`. This is a strong lead for init/callback registration and is the next static trace target.

The dynamic setter `FUN_0002e6c8` has no direct xrefs in the current database; this does not establish that it is unused because callback/table dispatch remains possible.

## Proof boundary

These findings explain more of the **software policy machinery** behind the observed Domain6 state. They do not establish the physical meaning of the final control bits and do not prove VCN power or execution.

```text
OUTER_WHOLE_BLOCK_VCN_POWER=UNPROVEN
VCN_DEISOLATION=UNPROVEN
VCN_REGISTER_BLOCK_ACCESSIBILITY=UNPROVEN
LOCAL_PSP_BYPASS=UNPROVEN
VCN_VCPU_EXECUTION=UNPROVEN
VCN_RING_HARDWARE_EXECUTION=UNPROVEN
```

## Next static task

Trace the orphan/init region around `0x0002e3ed..0x0002e3f5`, the callback cell at `0x000181dc`, and the caller chain that selects the initial profile. The goal is to explain why the clean live Domain6 baseline singles out slot17 without treating mutable image defaults as runtime-policy proof.
