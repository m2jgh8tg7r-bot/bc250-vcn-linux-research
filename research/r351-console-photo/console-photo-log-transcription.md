# R351 console photo — log transcription

## Evidence class

**LIVE_CONFIRMED (photo witness / manual transcription)**

This record contains only text visibly readable from the R351 physical console photo. It is not a reconstructed journal, and unreadable text is intentionally omitted.

## Visible log content

The photographed console shows the previous-system-reset diagnostic reporting:

```text
Previous system reset reason [0x10000400]: a parity error occurred
```

The boot then continues into TSC clocksource calibration/selection. The photographed output shows a refined TSC frequency of approximately:

```text
3194.029 MHz
```

The console subsequently reaches a shell/recovery-style prompt. The shell reports that job control is unavailable in the photographed context.

## VCN-specific observation

No VCN firmware authentication result, PSP `LOAD_IP_FW` result, firmware placement result, VCN ring initialization, or other VCN activation result is visibly present in the photographed portion.

Therefore this photo **does not establish VCN PASS or VCN FAIL**.

## Interpretation constraint

The reset reason `0x10000400` establishes that the platform reported a parity error, but the photo does **not** identify the originating block.

Do not attribute the parity error to VCN, PSP, SMU, memory, PCIe, CPU, or any other specific hardware block without a controlled causal experiment.

The correct current classification is:

- parity-error reset reason: **LIVE_CONFIRMED**
- VCN causality: **HYPOTHESIS / UNPROVEN**
- VCN activation: **NO EVIDENCE IN PHOTO**

## Relationship to R351

The photo was retained because the normal R351 log-capture path produced no usable log. It therefore serves as the physical-console witness for the failed capture attempt.

The intended R351 read-only `PGFSM_STATUS` observation was **not captured** in this photo.

## Next diagnostic requirement

A future controlled A/B comparison should distinguish:

1. control boot with no VCN-related register read;
2. boot with only the guarded read-only `PGFSM_STATUS` access.

The reset reason should then be compared between the two boots before assigning any causal relationship to the guarded read.
