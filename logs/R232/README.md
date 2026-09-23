# R232 offline reproduction

Run with Python 3, without `-O`, from this directory:

```sh
python3 run_checks.py
python3 verify_negative_controls.py
```

Expected: 9,563 cases pass, covering580 saved instruction positions;3 incorrect model interpretations are rejected. No packages, network, firmware download, device access, or privilege are required. Test scripts write their JSON results beside themselves.

This is a bounded interpreter of already-saved instruction text, not a complete PSP emulator. SVC/helper hooks supply hypothetical outcomes. Artificial export code coordinates and seeded user pointers are an abstraction, not a live relocation model. Unsupported instructions and unseeded memory reads fail. No firmware file is modified or generated.

`saved-instruction-index.json` contains only tested instructions and documentary anchors. `evidence-manifest.json` gives the original export hashes and distinguishes full-source counts from this selection. `full-local-evidence-audit-results.json` records the original28-export audit:4,926 byte matches and95 literal matches.

If you independently have the exact existing TOS body, optional byte/source checks are:

```sh
python3 audit_saved_evidence.py /path/to/existing/tos-body.bin
```

The optional `--source-root /path/to/research` checks all original28 local exports. The body is not included or downloaded. Wrong hashes fail. For the public selection the byte-match count is smaller than the full local audit; this is intentional.

SVC67 worker implementation, scheduler/service execution, running identity, live occupancy, PSP acceptance and VCN operation remain unproven. Kernel source manifests provide pinned links; full external source files are not republished here.
