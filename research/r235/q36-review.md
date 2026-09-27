# Q36 advisory review — disposition

Date: 2026-09-27. The user explicitly permitted using local Q36 as an assistant.

Model: Qwen3.6-35B-A3B, locally installed quantized GGUF. Backend: Vulkan GPU compute. Only a bounded text argument was supplied; the research tree was not mounted and networking was disabled. The final trace reports `tool_round=0`, `context_limited=0`, 815 generated tokens, return code 0. No Q36 statement is promoted to evidence.

The first invocation exited 1 before generation because the working directory prevented a required Vulkan shader from being found. The retry used the runtime directory and completed. This was a configuration failure, not a hardware failure. Both attempt logs remain local.

| Review suggestion | Deterministic disposition |
| --- | --- |
| Define “better candidate” | Adopted: the comparison criterion is signer-ID membership only; the usage-10 record is observed but runtime selection/enforcement is unproven. |
| State whether metadata checks actually passed | Adopted: declared bounds and two-copy equality passed; SHA-256 values were recorded. Whole-payload control CRC comparison did not pass. |
| Describe duplicate KDBs more clearly | Adopted the two-distinct-body fact. Rejected the speculative suggestion of “re-injections”: matching saved bytes do not establish how they got there. |
| Replace the no-signer wording with “absence of signer metadata in VCN controls remains unexplained” | Rejected: the VCN signer metadata is present. What is absent is a matching record in the saved candidate KDBs. The supplied wording would erase that distinction. Explicit model/runtime assumptions are retained instead. |
| Clarify version-reader limits and PSP-generation scope | Retained: version numbers are not image digests; PSP 13 counterexample prevents a universal cached-file-origin claim. The review's description of version fields as strings is unnecessary. |

The review improved wording and exposed model-generated overgeneralizations. All factual decisions remain based on saved files and source checks. No hardware experiment was proposed or performed by Q36.
