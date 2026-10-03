# R312 partial receiver result

The cumulative user-supplied text contains historical R298/R299/R300/R302/R303 boots before the R312 segment. Only R312 is used for this result.

R312 qualification2–10 and completion are visible (1 is absent in this excerpt), followed by exact input acceptance and module load. Parser records show die0/instance0/count3, bases 0x7800, 0x7e00 and 0x02403000. These agree with R308 normal-boot exported metadata, now observed inside the research driver's parser. Aperture report is 524288 bytes. Firmware host-copy reports equality for 405696 bytes; not VCPU execution.

This supplied excerpt ends at 47.220948 during Display IRQ warnings. R311 META, this boot's helper-entry/guards and final panic are not visible. Earlier R303 guard records cannot fill that gap. Missing output does not establish a hang, the stopping instruction or a hardware cause. The user confirmed there is no further receiver output and recovery was an automatic reboot. This establishes the reported recovery outcome, not the reset mechanism or arrival at the intended panic. No repeat test is requested.
