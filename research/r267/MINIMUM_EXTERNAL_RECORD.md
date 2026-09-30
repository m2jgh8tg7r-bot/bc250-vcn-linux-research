# Minimum useful original record

No new acquisition is requested by this document. Existing records can satisfy it; unknown fields remain null in board-comparison-template.json.

For Thomas's two-rate GPCNT result, the smallest useful bundle is the exact measurement code revision plus unedited sampled count/timestamp pairs at each configuration, counter width and selector-map source, board/boot/configuration aliases, and the reset/reconfiguration interval. A reported final MHz number alone cannot be replayed. Clock request values remain labels, never an input for choosing modulo wrap count. Sample timing uncertainty and counter tick units also constrain the result.

For the cross-board mirror comparison, retain the three separate values and their validity from one identified trial, the acquisition method already used, and the matching clock/RBC/VCPU observations. A difference is evidence of a recorded configuration difference; OTP origin remains unknown. Equality with both VCPUs inactive leaves VCPU-specific disable unresolved.

For stock versus modified BIOS, first compare existing records with matched driver/module, firmware, acquisition path and capture phase. Keep reset history explicit. An image change alters more than the added warm reset, so a changed outcome establishes BIOS/history dependence before it identifies a particular reset mechanism. Repeated failures with unvalidated observers add little discrimination.

The stronger first-fetch question requires an independently validated observer and its positive control. A successful DRM information query, register readback, generic clean bit or absent marker is not this control. A negative capture without coverage of the relevant reset/start interval cannot eliminate fetch or reset hypotheses.
