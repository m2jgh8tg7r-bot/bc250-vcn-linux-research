# Response evidence contract — verified static clarification

Historical R180/R182 controls have ten status-zero responses, of which five also have nonzero returned TMR addresses. VCN has a nonzero response status and zero returned placement. R235's strict five-control count is an analysis predicate, not an upstream universal requirement that every accepted firmware must return a nonzero TMR address.

The driver copies response address fields into ucode bookkeeping. In the bounded Cyan generation source files, VCN startup consumes these fields whereas GFX10 and SDMA5.2 do not reference this member. This does not prove exactly how the internal PSP loads each control; it does show why a cross-IP placement rule must be stated as a conservative evidence filter.

Host return zero is transport/control-flow completion, not a sufficient firmware status check: the source deliberately tolerates some nonzero response statuses to preserve initialization compatibility. This source caveat does not convert the historical VCN rejection into success, and no VCN decode or ring execution proof exists.

Separate: transport completion, response status, returned address presence, input payload identity, resident firmware identity, execution, codec results. No inference across an unmeasured boundary.

Source excerpts and SHA-256 are in `results.json`. Source is the retained working tree with historical instrumentation; no exact-upstream claim is made. The member-reference absence is restricted to the named GFX10 and SDMA5.2 files, not all paths or firmware internals. No new live responses were collected.
