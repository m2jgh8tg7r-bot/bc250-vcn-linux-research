# R291-P0 v2 result — exact start reference scan; tooling stop

Date: 2026-10-01

Classification: PARTIAL STATIC / TOOLING FAILURE

Confirmed from exact token matching in vcn_v2_0.c:
- Exact references to vcn_v2_0_start(...): 3 total.
- One is the function definition.
- Two are real callsites:
  - one `return vcn_v2_0_start(vinst);`
  - one `ret = vcn_v2_0_start(vinst);`
- Exact references to vcn_v2_0_start_sriov(...): 3 total.

Tooling failure:
- The audit attempted to extract `vcn_v2_0_set_powergating_state`, but this source uses a differently named power-state helper.
- The script stopped before classifying the two exact vcn_v2_0_start callsites by their containing functions.
- Therefore P0-v2 is NOT a callgraph PASS and does not justify a live callsite yet.

Prior-source clue to verify next:
- Earlier R287 source output shows a function named `vcn_v2_0_set_pg_state(...)` with a Cyan quarantine branch.
- Earlier R287 source output also shows `vcn_v2_0_reset(...)` contains `return vcn_v2_0_start(vinst);`.

Safety:
HARDWARE_ACCESS=NO
SOURCE_MODIFICATION=NO
MODULE_BUILD=NO
BOOT_CHANGE=NO
RESET_RELEASE=NO
FILTER_WRITE=NO
