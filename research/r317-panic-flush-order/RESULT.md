# R317 — Panic flush ordering limits the netconsole observation

STAGE=R317
RESULT=PROVEN_STATICALLY for retained source: unsafe nbcon final flush follows timed restart
STATIC_OR_LIVE=Source audit plus separately attributed R316 pasted log
HARDWARE_ACCESS=NONE
HARDWARE_MUTATION=NONE
HARDWARE_FAILURE=UNPROVEN
PROVEN=Specific source-level observation failure mechanism exists
REJECTED=No received panic proves no panic; generic packet-loss explanation is sufficient to identify cause
UNPROVEN=Actual R316 panic/checkpoint arrival, reset mechanism, exact running-kernel/source correspondence
NEXT=Offline review of observation alternatives; user has stopped further hardware tests today

## New static finding

Retained drivers/net/netconsole.c defines BOTH basic and extended consoles with CON_NBCON_ATOMIC_UNSAFE, alongside CON_NBCON and CON_ENABLED. The extended variant also has CON_EXTENDED. Switching basic to extended changes metadata, not this panic-flush property.

include/linux/console.h console_is_usable(..., use_atomic=true) rejects this unsafe callback unless nbcon_allow_unsafe_takeover() is true. kernel/printk/nbcon.c enables that permission inside nbcon_atomic_flush_unsafe(), only on the panic CPU. Its printer-thread checks also block during panic/emergency state.

kernel/panic.c orders the relevant calls as follows:

1. Shut down other CPUs (around line 673).
2. console_flush_on_panic(CONSOLE_FLUSH_PENDING) (710), which invokes ordinary nbcon flush; it does not itself grant unsafe takeover.
3. With positive panic_timeout, print the countdown and wait (719 onward).
4. With nonzero panic_timeout, call emergency_restart() (743).
5. Later in the fallback path, console_flush_on_panic and nbcon_atomic_flush_unsafe() (767–768).

If emergency_restart succeeds, step 5 is never reached. Thus panic=10 is structurally compatible with a successful reboot before unsafe netconsole's final backlog flush. Merely waiting the ten seconds is not a guarantee that printer threads transmit remaining records. The exact basic/extended property is shared, so R316's format change cannot by itself repair this condition.

This is a source-level mechanism, not proof that R311 panic executed on either trial. Earlier records may already have been transmitted; NIC state and other printk paths still matter. No new whole running-kernel binary-to-source identity was established. R315's packaged netconsole executable-section checks are narrower evidence and do not establish kernel panic.c identity.

## Separate early replay gap

The same retained init_netconsole sets CON_PRINTBUFFER before registering a command-line target, replaying existing printks. Therefore timestamp-zero records received after network setup are historical log timestamps, not packet arrival timestamps. R316 pasted sequence 275 to 900 omits 624 sequence numbers during this early region. Replay-burst loss or receiver backlog is a candidate, but copying omission remains possible until raw JSONL is inspected. Do not combine this interior gap with the entirely absent terminal suffix as one proven mechanism.

## Hypotheses

| Hypothesis | Supporting evidence | Contradicting evidence | Unknown | Discriminating evidence |
|---|---|---|---|---|
| Intended panic with undrained netconsole tail | Concrete unsafe-flush ordering; R312 operator-reported automatic reboot | None established | R316 recovery and actual named panic; running kernel correspondence | Named panic on an independent console, or a reviewed flush control in a future session |
| An earlier different panic/reset | Remains compatible with absent suffix | No positive signature of that alternative | Actual reset trigger | Independent named panic/reset record |
| Receiver or network drops | R316 paste has an interior gap; UDP does not ensure delivery | Records 900–1200 are continuous in supplied text, limiting interior-loss claims there | Raw capture vs copy omission, sender/receiver queues | Inspect existing raw capture timestamps and sequence ranges offline |
| Display warning directly terminates execution | No direct positive evidence | Earlier controls continue after the same warnings | Whether this trial follows a different path | A terminating trace or independent later checkpoint |

Counterexample to the favored observation explanation: another panic before R311 would encounter the same flush limitation and yield the same missing tail. Consequently no unique execution boundary or reset cause is selected.

## Next work without hardware

Preserve R316 as a partial live result, not an unsuccessful VCPU trial. Review source-to-kernel provenance and independent console availability before preparing another experiment. A future no-auto-restart or earlier-flush control would change recovery behavior and requires a separate reviewed plan and advance notice; neither was built or executed. Do not remove the unsafe flag casually. Do not repeat CP06/07 reads. No further hardware test is requested today.
