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

The dynamic setter `FUN_0002e6c8` has no direct xrefs in the current database; this does not establish that it is unused because callback/table dispatch remains possible.

## R124D — initial profile and callback-shaped init path

The previously orphaned region around `0x0002e3e8` is now resolved at the instruction level.

It performs:

```text
movi a10, 0
call FUN_0002e69c
```

Therefore the init path directly loads **profile 0**.

The nearby sequence then loads event/index `0x18`, loads the function pointer stored at `0x000181dc`, and calls `FUN_0001b1e4`:

```text
0x000181dc -> 0x0002e448
```

So the policy applicator function pointer is explicitly passed through a registration-shaped `FUN_0001b1e4(0x18, callback)` call during init. The exact abstract semantics of `FUN_0001b1e4` are not claimed here until that helper is independently decompiled, but the argument shape is consistent with the many other ID+function-pointer call sites in the firmware.

The normal command/control path also converges on profile 0. `FUN_0002e0e8` calls:

```text
FUN_0002e190(0)
```

and `FUN_0002e190` passes that zero unchanged to `FUN_0002e69c`.

This materially narrows the next question: the clean live Domain6 baseline should now be compared against the **profile-0 source data** at the recovered profile table, rather than against zero-filled mutable runtime storage.

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

Recover profile-0 values from the source table at `0x00007b54`, map its 20 values onto the already recovered slot-ID order, and compare slot `0x16`, `0x17`, and `0x18` directly. Separately decompile `FUN_0001b1e4` to close the callback-registration semantics without relying on call-shape inference.
