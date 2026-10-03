# R313 — R312 receiver boundary audit

STAGE=R313
RESULT=PROVEN_STATICALLY for retained source; reset cause UNPROVEN
STATIC_OR_LIVE=Static audit plus explicitly attributed R312 user observations
HARDWARE_ACCESS=NONE during this audit
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=R312 parser metadata received; user reports automatic reboot and no further receiver tail
REJECTED=Treating final received display warning as the stopped instruction
UNPROVEN=R311 helper arrival, intended panic, actual reset mechanism, VCPU activity
NEXT=Review a sequence-aware observation control; do not repeat CP06/07

## Findings

1. R312 init contains no automatic reboot action. Its failure and unexpected-modprobe-return paths enter an interactive hold. The printed reboot command is advice, not execution. The generated boot entry supplies panic=10. Retained kernel/panic.c assigns the panic parameter to panic_timeout and calls emergency_restart for a nonzero timeout. Thus automatic reboot is consistent with the planned panic, but also with another panic; it does not prove the planned checkpoint.
2. Retained netconsole.c netconsole_write skips disabled/non-running targets and returns if nbcon_enter_unsafe fails. Its send_udp wrapper accounts for NET_XMIT_DROP and -ENOMEM with dynamic support. Retained netpoll.c can queue an unsent skb for delayed work and return NETDEV_TX_OK. Successful enqueue is not receiver delivery. These are possible loss/defer paths, not evidence that a particular path occurred in R312.
3. The R312 invocation uses basic netconsole output and oops_only=0. Therefore oops-only filtering is not the configured explanation. It does not provide printk sequence numbers for checking missing records. The retained documentation describes explicit extended mode via a leading + and headers with sequence number and fragmentation offsets. The default extended-log configuration being disabled does not alone exclude explicit extended mode.
4. R311 source places scalar logging and the intentional panic after helper guards, before the helper's first VCN MMIO. The received parser metadata precedes this checkpoint. Prior compiled-checkpoint audit remains separate from this source audit. No complete running-kernel/netconsole binary-to-source identity is newly established here.
5. Display warnings were followed by later messages and CP03/CP04 markers in older controls. This contradicts a universal claim that these warnings always stop initialization. It does not rule out a new display-path failure in R312. The last R312 received line alone cannot discriminate.

## Hypothesis matrix

| Hypothesis | Supporting evidence | Contradicting evidence | Unknown | Next discriminating experiment |
|---|---|---|---|---|
| Intended panic occurred; tail was not delivered/captured | Automatic reboot report; panic=10; planned source path | None established; absent witness is not a contradiction | Whether checkpoint executed; where records were lost | Sequence-aware capture with the same driver; a received META and named panic supports this model |
| Another panic/reset occurred before helper | No helper witness; automatic reboot | No specific alternate error/reset witness | Reset cause and reached instruction | An alternate panic signature from an independent console distinguishes it; another absent tail does not |
| Display warning burst contributed to missing output | Large burst immediately before last receipt; transport can defer/drop | Older controls delivered later markers despite warnings | Sender queue state, receiver loss, console ownership | Record raw datagrams with sequence and arrival times; internal sequence gaps show missing capture records, not their loss location |
| VCN MMIO caused this reset | No new positive evidence | Intended R311 helper path panics before its first VCN MMIO | Actual running path and unrelated earlier hardware operations | Do not add VCN reads to diagnose this observation failure |

If intended-panic-with-lost-tail is wrong, an earlier independent panic or reset explains the same automatic reboot. No unique cause is selected.

## Proposed observation control (not built or installed)

Keep the R311 driver, firmware, input gate and panic timeout unchanged. Change only basic to extended netconsole format, with a receiver that preserves raw datagrams and receive timestamps and understands ncfrag fragments. Validate its parsing offline before any boot. Preserve the initial qualification and manual confirmation gate.

A: META plus named R311 panic received — directly establishes checkpoint arrival for that new boot only.
B: A different panic received — identifies an alternative path for analysis.
C: Sequence gaps between received records — establishes missing records in the capture, not whether sender, network or receiver lost them. Fragment duplication and reordering must be handled before classifying gaps.
D: Tail ends again with no later record — still cannot bound missing suffix length or identify the reset cause. Stop this variant; consider an independently qualified serial observation channel instead of repeated boots.

Sequence numbering cannot detect an entirely absent suffix without a later anchor. This proposal improves observability but is not guaranteed to discriminate the current outcome. No new image, boot modification, module load or reboot was performed in R313.
