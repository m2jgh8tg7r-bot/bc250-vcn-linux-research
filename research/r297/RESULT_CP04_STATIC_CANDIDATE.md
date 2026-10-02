# R297 CP04 static candidate PASS — 2026-10-02 JST

Status: PASS

Candidate:
- path: research working tree cp04-v1/vcn_v2_0-r297-cp04.c
- SHA-256: 49416974d1a816a22dc0f7a768fc3528a98eb643525156afb0f9dbd358203f42

Baseline P1 SHA-256:
97e33967c54696540d621227e36b0e533007a5cc2d29121a9015dda76dfca38a

Exact source changes versus P1:
- add linux/panic.h
- add helper-entry dev_info immediately after helper locals
- add guards-pass dev_emerg and panic after pg/cg and SR-IOV guards
- no older CP01/CP02/CP03 checkpoint markers

Definition-scoped order:
- helper definition: 16672
- helper body: 16760
- helper entry marker: 16866
- pg/cg guard: 17034
- SR-IOV guard: 17084
- guards-pass marker: 17150
- panic: 17207
- first helper WREG32_SOC15: 17877
- first helper SOC15_WAIT_ON_RREG: 17927
- first helper RREG32_SOC15: 17999

Contracts:
- CP04_HELPER_DEFINITION_EXACT=YES
- CP04_HELPER_ENTRY_BEFORE_GUARDS=YES
- CP04_GUARDS_PASS_BEFORE_FIRST_MMIO=YES
- CP04_PANIC_BEFORE_FIRST_MMIO_WRITE=YES
- CP04_PANIC_BEFORE_FIRST_MMIO_READ=YES
- CP04_PANIC_BEFORE_FIRST_MMIO_WAIT=YES
- CP04_NO_OLDER_CHECKPOINTS=YES
- R297_CP04_STATIC_CONTRACT=PASS
- CP04_STATIC_AUDIT_EXIT_CODE=0
- R297_CP04_STATIC_AUDIT=PASS

Static audit V3 log SHA-256:
8b84b1071c71a36991df165865c093ed4d98f5c63946f8ada5896dae7a173599

Safety boundary:
- no module build
- no module load
- no boot write
- no boot selection change
- no VCN MMIO access
- no reset release
- no FILTER write
- no PowerUpVcn
- no reboot

Scientific purpose:
CP04 is designed to prove helper entry and guard passage in LIVE while still panicking before the helper's first VCN MMIO access.
