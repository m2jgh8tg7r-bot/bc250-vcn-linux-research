# R297 CP04 object final PASS — 2026-10-02 JST

Status: PASS

Exact identities:
- CP04 source SHA-256: 49416974d1a816a22dc0f7a768fc3528a98eb643525156afb0f9dbd358203f42
- CP04 object SHA-256: 9594ead048e817baaec5f30d98eb49c59bd0ba55558c0832b307f6ac1e977399
- clean R152 vcn_v2_0.c SHA-256: eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075

Compiler shape:
- standalone helper symbol absent
- helper prefix inlined into vcn_v2_0_hw_init.cold
- hw_init.cold symbol count exactly 1

Machine-code order:
- P1 begin line 322
- helper entry line 524
- pg/cg guard line 530
- SR-IOV guard line 533
- guards-pass line 537
- panic line 539
- panic relocation follows
- zero executable instructions after panic in the cold symbol

Debug-line contract:
- helper entry/guards/panic lines survive
- first WREG line 556 absent
- first WAIT line 558 absent
- first RREG line 561 absent

Final machine-code conclusions:
- CP04_HELPER_INLINED_INTO_HW_INIT_COLD=YES
- CP04_HELPER_ENTRY_MACHINE_CODE=YES
- CP04_PGCG_GUARD_MACHINE_CODE=YES
- CP04_SRIOV_GUARD_MACHINE_CODE=YES
- CP04_GUARDS_PASS_MACHINE_CODE=YES
- CP04_PANIC_MACHINE_CODE=YES
- CP04_FIRST_WREG_MACHINE_CODE_ABSENT=YES
- CP04_FIRST_WAIT_MACHINE_CODE_ABSENT=YES
- CP04_FIRST_RREG_MACHINE_CODE_ABSENT=YES
- CP04_PANIC_TERMINATES_COLD_PATH=YES
- CP04_NO_EXECUTABLE_MMIO_AFTER_PANIC=YES
- R297_CP04_OBJECT_MACHINE_CODE_CONTRACT=PASS

Marker contract:
- P1 begin present
- CP04 helper_entry present
- CP04 guards_pass log present
- CP04 panic text present
- CP01/CP02/CP03 absent
- U panic retained

Tooling correction:
The previous forensic run accidentally used Bash special variable LINES; the final audit used CP04_MACHINE_AUDIT_DECODED_LINES.txt and confirmed it was byte-identical to the accidental artifact.

Final:
- R297_CP04_OBJECT_FINAL=PASS
- CP04_MACHINE_AUDIT_EXIT_CODE=0
- R297_CP04_OBJECT_MACHINE_AUDIT=PASS

Stable artifacts:
- cold disassembly SHA-256: a41bb4fb299714de16c2432ca678fc6bd9f25b2330f15d5d7310a12a8e1c49bb
- decoded line map SHA-256: 14c0c358cf9a18663ce1cd284365f2530cb089557d5fbdf15e9dfe3635adb690
- final audit log SHA-256: 712da4cd94aa0f3098273bf1cbf8402ab350d7c74daea351ce2027519d9f4fac

Safety:
- no rebuild during final machine audit
- no source overlay
- no /boot write
- no module load
- no hardware/MMIO access
- no reset/filter/power action
- no reboot

Next:
Compose the exact R274B amdgpu_vcn.c candidate with the exact CP04 vcn_v2_0.c candidate into the clean R152 tree and build the full amdgpu module. Audit the resulting full module for the same CP04 inlined cold-path machine-code contract before packaging.
