# R346 — Bootstrap allocator-call count boundary

STAGE=R346
RESULT=One visible bootstrap traversal contains three direct 0x211a04 callsites, with a maximum of three executions; a supplied post-call backedge does not repeat them
STATIC_OR_LIVE=CONDITIONAL_STATIC_CONFIRMED from bounded saved-static instruction packet
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
Q36=ADVISORY_ONLY; model output missed a supplied post-call backedge; conclusion manually corrected against packet
PACKET_SHA256=3a72c83fe474bb70e62e12d5c94392524dba400689ba541c66614b1746b26516

## Call sites and path conditions

The bounded packet shows three direct call instructions to `0x211a04`: `0x21230c`, `0x212414`, and `0x212584`. The first is in the bootstrap body. At `0x2123f0`, `bge 0x212434` skips the second call on the taken path; the fallthrough path proceeds through `0x212414`. Both paths converge at `0x212434: bl 0x212544`, whose shown body contains `0x212584: bl 0x211a04`. Thus one visible traversal executes at most three of these calls; the packet does not establish that every callsite is reached on every path. The third site is inside the callee, so the count includes the shown direct call chain.

The packet also shows `0x212464: b 0x212460`, a backward branch within the later `svc 0x56` wait loop. It is after the listed allocator-call sites and does not branch to any of them. No supplied direct backedge repeats these three sites. This bounded result does not exclude an outer caller invoking the bootstrap more than once, or indirect/callee re-entry outside the supplied windows; runtime reachability and total run-wide count remain unproven.

No BIOS, firmware, kernel, module, boot entry, or hardware state was changed. No `sudo` command or real-device test preparation was required.
