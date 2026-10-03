# R312 installed; live observation pending

User-run installation returned PASS. Independent unprivileged audit confirms installed image/entry hashes, both R303 backup hashes and absence of retired paths. Privileged protected-hash records equal preflight; not all protected files were independently readable. No module load, boot selection or reboot has occurred.

Next, start saving receiver output, then run the prepared arm-menu.py with sudo. It verifies installed/protected hashes and include existence/content, saves grubenv, and sets only a transient 30-second manual menu timeout. It does not select an entry or reboot. Review its PASS before manually rebooting.

Select `BC-250 R312 pre-access metadata - manual gate`. On the receiver confirm this boot's R312 QUALIFICATION_COMPLETE before entering the intentionally retained public confirmation string R299-CP03-RECEIVED. Expected observations are R311 DISC records, then the CP04-derived guard boundary and R311 META records before deliberate panic. Records may be missing; absence is inconclusive. If automatic restart does not occur, manually recover to a normal entry. Do not repeat a failed register probe.

Saved receiver evidence should include qualification through the last received line. VCN execution remains unproven.
