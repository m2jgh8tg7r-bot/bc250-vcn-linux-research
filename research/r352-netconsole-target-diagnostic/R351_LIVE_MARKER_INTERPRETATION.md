# R351 live receiver marker interpretation

Use a fresh Windows UDP capture for each boot. Old R351 lines from the first incorrectly assembled R352 image must not be mixed into the corrected R351 trial.

| Last confirmed R351 marker | What it establishes | STATUS read conclusion |
|---|---|---|
| No `QUALIFICATION_COMPLETE` | Network qualification was not witnessed | No gate acceptance evidence; do not enter token |
| `QUALIFICATION_COMPLETE`, no `INPUT_RESULT` | Init reached local confirmation input, but accepted input is not witnessed | No GPU-load/read evidence |
| `INPUT_RESULT ... bytes=16 escaped_prefix=R351-STATUS-READ` and `INPUT_EXACT_MATCH` | Exact local gate accepted | Driver load is about to be requested; STATUS not yet established |
| `AMDGPU_MODPROBE_BEGIN` | R351 module load request started | Probe/helper/read not established |
| R351 `ABORT final-base` or `ABORT PCI identity qualification` | Helper rejected its guard | No `PGFSM_STATUS` read; implementation then intentionally panics |
| `STATUS_READ_BEGIN` | Guard passed and execution reached the single `RREG32_SOC15(...mmUVD_PGFSM_STATUS)` call | Read was invoked, but return/value not established |
| `STATUS_READ_RETURN raw=0x........` | The single STATUS read returned and the value was logged | Read-return objective achieved; following panic is intentional |
| `Kernel panic - not syncing: BC250 R351 after single PGFSM_STATUS read; no write or wait` | Explicit checkpoint reached | Look for the preceding `STATUS_READ_RETURN`; a panic alone is insufficient because the code also panics after a guard abort |

The R351 helper's panic is unconditional after the guard/read branch. Therefore `Kernel panic` or a subsequent reset-reason string alone cannot establish that the STATUS read ran. The code performs no `PGFSM_CONFIG` write or poll in this test. The local init requests AMDGPU only after the exact `R351-STATUS-READ` token; no token means the gate is closed.

If capture stops at `STATUS_READ_BEGIN`, distinguish an unreturned read from lost panic packets using the full Windows raw capture, pstore, and console. If the only local evidence is the initramfs shell / TSC screen, do not infer the MMIO boundary.
