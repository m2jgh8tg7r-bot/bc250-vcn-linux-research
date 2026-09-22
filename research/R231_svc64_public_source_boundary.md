# R231 — SVC64 semantics remain unresolved; use public text sources only

Date: 2026-09-22. No hardware access or mutation.

The saved TOS call site confirms that `FUN_00211a04` passes a parsed item class/type and a pointer to a stack byte where SVC `0x64` returns a slot index. A successful call is followed by writing that index into the 0x54-byte row. The SVC implementation, exact allocator policy, returned index range, and live behavior remain unknown.

AMD's public `firmware_binaries` repository lists a Vangogh PSP type-2 blob, but the repository README license prohibits reverse engineering, disassembly, and decompilation of licensed binaries. A raw copy was briefly fetched before the license was read; only metadata/hash/basic byte-comparison checks were run, no disassembly occurred, and the copy was deleted. The comparison did not establish exact identity with the local saved TOS. No licensed binary payload is retained or redistributed. No SVC mapping or allocator behavior is inferred from unrelated Cezanne release-note references.

Continue SVC research through public text documentation and other permitted non-binary sources. Keep SVC `0x64` allocation semantics marked unknown unless authorized, version-matched textual evidence establishes them.

Local reproduction: `r218-service-image-provenance/instructions.txt` around Ghidra `0x211cbc..0x211cc6`; `r231-svc64-slot-semantics/STATUS.md`. The AMD repository and license are documented at the official repository README.
