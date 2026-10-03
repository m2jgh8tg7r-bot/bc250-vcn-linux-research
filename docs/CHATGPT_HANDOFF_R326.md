# R326 — R325 live final-pointer observation

STAGE=R326
RESULT=R325 final-pointer checkpoint received with expected segment1 and named panic end
STATIC_OR_LIVE=PROVEN_LIVE user-supplied receiver transcript; retained-source interpretation separated
HARDWARE_ACCESS=No agent register access; user boot includes existing GPU initialization
HARDWARE_MUTATION=No agent mutation in this stage; no new helper VCN MMIO in checkpoint
HARDWARE_FAILURE=UNPROVEN
PROVEN=Helper-side pointer matches bounded discovery record; die0/count3; one VCN instance0 record in accepted traversal; base1=0x7e00; planned panic and end received; current normal kernel read
REJECTED=This boot's final segment1 differs from the recorded parser segment1; display warnings were terminal on this boot
UNPROVEN=Historical CP06/07 bases/stop/cause, physical register response, VCPU execution, full raw capture completeness, operator recovery method
NEXT=Preserve raw JSONL and confirm recovery; no repeat of this achieved checkpoint or unchanged CP06/07

## Received evidence

The pasted excerpt spans sequence899–1280. R325 qualification completes at908, input matches at911 and GPU loading begins at913. Parser sequences923–925 report die0/instance0/count3 and bases 0x7800/0x7e00/0x02403000.
Helper/guards/META are visible at1197–1200. Sequence1201 at56.422120s reports FINAL matched=YES die=0 count=3 vcn0_records=1. Sequence1202 at56.422128s reports base1=0x7e00, config_byte=0x1f800 and status_byte=0x1f804 with aperture524288.
Sequence1203 at56.422139s names the deliberately introduced R324 pre-helper-MMIO panic; sequence1280 at56.426610s is its matching end marker. A later read of uname reports the normal 7.2.1-ogc4.1.fc44.x86_64 kernel. This kernel read does not independently establish the reset method or complete post-recovery system health.

## Interpretation

Under the retained observer and successfully bounded traversal, the selected VCN instance0 pointer belongs to the die0/count3 record, and only one VCN instance0 record exists in the inspected discovery image. The matching segment1 supplies live evidence at the helper-side observation time, closing the specific parser-versus-selected-pointer gap for this boot. It does not attest every base entry, arbitrary aliased writes or subsequent/historical state.
The byte offsets plus a 4-byte access fit inside the mapped aperture. Arithmetic fit is not physical accessibility: no new helper register transaction occurred, so no CONFIG write completion or STATUS response is established.
The initialization continued past display IRQ warnings to the final checkpoint. Those warnings are not the terminal event of this run. This says nothing conclusive about old failed boots.
One accepted record on this run is not proof that all boots/boards have identical discovery records. No unchanged hanging-read replay is warranted merely because the software-address premise is now stronger.

## Capture and next decision

The raw-saving receiver was reported running, but its JSONL has not been independently inspected. The excerpt omits earlier records, including qualification1/10; no full datagram or sequence-completeness claim is made. The explicit final/panic evidence remains sufficient for this observation objective.
The operator recovery method is pending confirmation; do not repeat the trial to answer that question. Keep the JSONL and use the existing offline analyzer for capture quality if needed.
This live test is complete as an observation. Before a different hardware experiment, re-evaluate physical power/clock/access prerequisites and a discriminator with more information than an unchanged read. No new hardware candidate, installation or reboot is requested here.
