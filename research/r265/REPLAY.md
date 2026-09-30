# Replay the extended source checkpoint

From a published checkout, with Python 3:

```sh
python3 research/r265/replay_public.py --work /tmp/vcn-extended-replay --download
```

The work directory must be outside the checkout. The script verifies the R260 current-source manifest and R254/R257 historical manifests, then reproduces the core checks plus R261–R264. It downloads public pinned source only and performs no device access, kernel build, firmware load or experiment. Omit `--download` to reuse a complete verified source cache. Do not use Python `-O`.

Private retained-source witnesses are excluded. R255's saved-firmware calculation remains optional through `--saved-firmware FILE`; the file is read locally and never uploaded or executed. The default report explicitly records that it was not replayed. Matching results establish static reproducibility, not BC250 hardware behavior.

The source matching is deliberately bounded to these pinned files. It is not a general C parser, symbolic execution proof or silicon specification. Counts overlap and must not be presented as independent hardware experiments. R263 does not repeat all historical fence internals or prove a historical regression boundary. See the R260 replay documentation for the original core scope.
