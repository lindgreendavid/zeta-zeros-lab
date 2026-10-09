# Contributing

Zeta Zeros Lab welcomes small, evidence-backed changes.

1. Open an issue for new research scope or a change to what a statistic measures.
2. Create a focused branch.
3. Add or update tests and documentation with the implementation.
4. Run `pytest`, `ruff check .`, `ruff format --check .`, `mypy src`, the registry generator with a
   comparison against the committed registry, `python scripts/verify_zeros.py`, and the web
   lint/build/test suite in `site/`.
5. Use English Conventional Commits and submit a draft pull request.

The thresholds in `docs/research-protocol.md` are fixed before results are generated. A change to a
hypothesis or threshold needs a new protocol version committed *before* the corresponding registry is
regenerated; never edit a threshold after seeing the numbers. The frozen registry
(`reports/v0.1-zeta-registry.json`) and the frozen zero blocks (`data/*.csv`) may change only alongside
their protocol, generator, tests and report. Never describe a numerical agreement as a proof, and never
report a KS p-value for zeta spacings: the zeros are not independent samples.
