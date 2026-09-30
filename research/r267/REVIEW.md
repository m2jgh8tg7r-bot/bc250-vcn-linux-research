# Counter-analysis review disposition

Q36 ran an isolated advisory GPU review, with no research tree mounted or hardware acquisition. Its output is not evidence about VCN.

Accepted: reset/reconfiguration intervals should not retain apparently valid bound/rate interpretations. These fields are now null; the modulo difference remains raw arithmetic only. The independent enumeration and reset control pass.

Rejected: a bound on total increments requires constant frequency. It does not. For actual increments N, modulus M and observed difference d, candidates are N=d+kM, k>=0, bounded by the supplied maximum. Q36 also made unit-conversion errors (1000 Hz over 1 ms is one increment, not 1000). Its proposal to label the largest possible candidate the minimum is incorrect.

Additional limitation: a nominal oscillator frequency is not by itself a certified bound on sampled integer increments. Sampling phase, acquisition latency, timestamp uncertainty and counter semantics must be included in a conservative bound. The existing checker verifies supplied arithmetic constraints, not those acquisition assumptions. No external GPCNT samples have been replayed.

No hardware test was recommended merely to validate these arithmetic controls.

A second Q36 preflight review exhausted its output budget before a complete finding. Its illustrative UAPI layouts were not adopted. The installed header was independently inspected: the union members share the expected location, discovery version exists, and decode/encode constants are 0/1. Assignments now name the query-specific union member explicitly for clarity. The program rebuilt with warnings as errors and remains unexecuted. No physical VCN conclusion follows.

An additional units correction was made before publication: arithmetic output and independent bounds are now explicitly counter increments per second, not `Hz`. Relating a count slope to physical VCLK requires a separately justified tick-to-cycle contract. Numerical agreement with a clock setting remains external evidence; the generic analyzer does not silently assume one increment per VCLK cycle. Synthetic controls were rerun with the explicit units.
