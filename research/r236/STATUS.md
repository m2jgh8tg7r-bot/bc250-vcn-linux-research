# R236 — retained control firmware provenance

Static checkpoint verified 2026-09-27. Official linux-firmware GitLab file **HEAD metadata only** was queried; no firmware payload was downloaded.

Eight retained decompressed control files match SHA-256, Git blob SHA-1 and byte count at both the prior R189 pinned revision and official main `9b858e5bb58d7bf1fc4d8818cb9100aed6d46f6a` (2026-09-26). Of the 2021 introduction revision, SDMA, SDMA1 and RLC match, while CE, ME, MEC, MEC2 and PFP differ. The five latter paths were modified by official 2022 commit `9f84af7645b9e63a616b4e8384b2ae19bad7b2bc`; the saved diff explicitly names those five paths. Results: 24 metadata comparisons, 19 matches, five expected older-revision mismatches; all 24 assertions rechecked offline.

Therefore the R235 outer CRC mismatch is also present in the official distributed byte sequences; it does not by itself establish local corruption. This does not explain the CRC convention, validate signatures, prove submitted bytes for the historical control requests, or establish running firmware identity. HTTPS metadata is a server assertion, not a signed attestation or locally cloned Git object.

Path-history queries can return pre-introduction unrelated filename history through similarity/rename following. Those older entries are **not** evidence of Cyan firmware availability before its explicit 2021 addition.

Evidence: `official-file-metadata.json`, `results.json`, `update-2022-diff.json`. Run `verify_metadata.py` against retained R180 files. Raw HTTP correlation headers and unsanitized history are local-only.
