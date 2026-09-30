# R285 — first R274-B live boot plan

Purpose: perform the first live boot of the exact R281/R282 artifact while retaining hardware-start guards and recovery paths.

## Selection method

Prefer manual boot-menu selection of:

BC-250 R282 R274-B direct provisioner (hardware start guards retained)

Do not set a persistent default and do not schedule a one-shot next_entry before the first test.

## Expected live evidence

Strong success for this stage requires:

- boot is attributable to kernel 7.2.3+ and the R282 BLS entry;
- the R274-B module loads;
- journal contains the exact R274-B direct-copy marker;
- direct-copy reports equal=1;
- retained PSP enrollment and VCN hw-init guards are observed;
- system remains sufficiently functional to collect the kernel log.

This stage does not require VCPU execution, ready, ring execution, VA-API, decode, or encode.

## Failure/recovery

If boot hangs or display does not recover:

- power-cycle only if necessary;
- choose normal Bazzite or R180 recovery entry manually;
- do not retry R282 repeatedly before inspecting the prior boot log if available.

No undocumented MMIO/SMN access is part of R285.
