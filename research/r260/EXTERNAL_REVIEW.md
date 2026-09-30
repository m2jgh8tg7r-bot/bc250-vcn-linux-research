# External claims, revisions and independence

This review examines what public documents claim and how they cite evidence. It does not reproduce their hardware procedures or adopt their physical diagnoses. Exact repository heads and file hashes are in `external-review.json`.

The toolkit's VCN note contains a September 23 categorical conclusion following a reported MMIO hang, followed by a September 26 addendum that revises the conclusion using external research. Reading only the earlier heading loses that correction. The addendum also cites this project's earlier handoffs; it is not an independent measurement confirming those handoffs. This is an attribution finding, not confirmation of the addendum's proposed physical cause. [Pinned toolkit note](https://github.com/rpf16rj/bc250-steamos-real-toolkit/blob/d0e41ed5ad74a4d8b50293c37d41b4c935a69869/.kb/vcn.md#external-research-that-revises-the-dead-verdict-2026-09-26).

The video-driver README makes a categorical claim about permanent factory disabling. Its description of CPU decoding and Vulkan-compute encoding does not itself establish that silicon claim or dedicated VCN execution. We retain the distinction between a project's implementation path and its explanation of unavailable hardware. [Pinned README](https://github.com/simpmix/bc250-encoding-decoding-fix/blob/98828189e95de4c07a99c6174939101947e0076c/README.md).

The community issue index labels VCN support as not planned and links an upstream discussion. The linked freedesktop page returned access denied during this session. We therefore do not attribute a detailed physical explanation to the upstream comment or present it as newly verified. [Pinned issue index](https://github.com/AMD-BC-250/documentation/blob/b20bc51eafa89b662324e96c2d40a14d2d6420b6/issues.md).

The user's September 30 RBC/cache-access summary remains a separate attributed input. This bounded public review did not identify a new independent raw capture that validates it under matching source, firmware, mapping and boot conditions. That does not show the observation is false or that no such capture exists elsewhere.

For the current research, both the old permanent-disable conclusion and a new assertion of successful VCPU execution would overstate the evidence available here. The useful next step is matching existing observations to the versioned startup and observation contract.
