# Replaying the static checkpoint

From a checkout of the published repository, use Python 3 and an empty work directory outside the checkout:

```sh
python3 research/r260/replay_public.py --work /tmp/vcn-static-replay --download
```

This fetches hash-pinned Linux source files, copies the small audit scripts into the work directory, runs their static/synthetic checks and compares their JSON output with the published results. It performs no kernel build, device access, firmware loading or register operation. To replay an already populated source cache without network access, omit `--download`. Do not use Python optimization (`-O`), because these audit scripts use assertions.

The current reference manifest is `research/r260/source-manifest.json`; historical and generation manifests are in R254 and R257. These manifests identify source inputs, not the currently loaded kernel. The offline input template in R253 contains unknown values, not a hardware capture.

R252's private retained-source witnesses are excluded from public replay. R255's saved-firmware calculation is optional: supply `--saved-firmware` with a locally held file matching the published metadata to replay it. The tool reads that file only, does not upload it and never loads or executes firmware. Without the file, the replay report explicitly marks R255 as not replayed. The published saved-file result is retained as a historical static observation.

The result is written to `replay-result.json` inside the work directory. A passing replay reproduces source assertions and scalar interpretation, not hardware behavior or the authenticity of external reports.

## Limits of the audits

The source audits deliberately match known pinned C text and definitions. They are not a general C parser, symbolic execution engine, proof of complete hardware sequencing, or a substitute for a matching silicon specification. Historical comparison samples six revisions, not every intervening change. Decoder masks describe a single reference map and explicitly distinguish named bits from physical states.

The stage results overlap. Their check counts must not be added and described as independent hardware trials. R143/R162/R163/R196 provenance is retained in the handoff to distinguish older facts from new source comparisons.
