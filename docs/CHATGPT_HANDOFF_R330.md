# R330 — R329 live partial PCI completion observation

STAGE=R330
RESULT=Pre-write PCI identity read and CONFIG write-return received; post-read begin is pasted tail
STATIC_OR_LIVE=PROVEN_LIVE user-supplied transcript; capture completeness unproven
HARDWARE_ACCESS=User-selected R329 boot; no agent register access
HARDWARE_MUTATION=User boot reports established CONFIG write; no new agent mutation
HARDWARE_FAILURE=UNPROVEN
PROVEN=R329 input accepted; bounded final base1=0x7e00; pre-read ret0 identity0x13fe1002 matches; WRITE_RETURN; CFG_AFTER_BEGIN
REJECTED=This excerpt demonstrates post-read return or VCN power/execution
UNPROVEN=Post-read return, planned panic, stop instruction/cause, reset method, complete receiver capture, VCN execution
NEXT=Obtain existing receiver suffix and operator recovery account; no unchanged repeat

## Boot separation

The pasted PowerShell window contains the prior R325 checkpoint/panic through sequence1280, then a new sequence0 and later R329 qualification/input. These are separate boots. The displayed PowerShell receiver decodes and prints only: no datagram file writing is present. Do not claim raw JSONL preservation or complete capture from this command. Prior R325 evidence is not R329 evidence.

R329 sequences1181–1182 establish selected discovery die0/count3/one instance0 record and base1=0x7e00. Sequence1184 at50.744075s reports pre-read ret0, identity and expected both0x13fe1002. Sequences1185–1186 at50.744087/50.744098s report CONFIG write begin and return. Sequence1187 at50.744106s reports CFG_AFTER_BEGIN and is the pasted tail. No CFG_AFTER_RETURN or named R328 panic is supplied.

The begin marker precedes the standard PCI API call in the audited candidate. Missing return alone does not prove the CPU entered/stalled in that call: scheduling, logging loss or excerpt truncation remain alternatives. Explicit operator confirmation of the terminal receiver suffix and recovery is needed. No new boot is required to resolve those observations. The agent currently reads normal7.2.1 kernel; this does not identify recovery mechanism or certify full system health.

The R329 init line says panic before helper VCN MMIO, an inherited stale description. The module transaction markers and compiled contract correctly show one CONFIG write before panic; use those as authoritative sequence evidence. Correct this label in a future distinct package, without repackaging or repeating the current trial solely for wording.
