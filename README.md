# Zeta Zeros Lab

**Part of the [Lab Notes Research Portfolio](https://blog-interactive.lindgreendavid.workers.dev/)** · Number theory × random matrices · Question → measurement → finding → boundary

A reproducible test of whether the nontrivial zeros of the Riemann zeta function follow
random-matrix (GUE) statistics, measured on 4,000 real zeros against the exact GUE law, a
random-points control, and a simulated null that shows how far genuine random-matrix data strays
by chance.

**Research question:** for two blocks of 2,000 consecutive zeros (the lowest, and those near the
100,000th), how close are the nearest-neighbour spacings and the pair correlation to the GUE
prediction, compared with Poisson, with the sampling scatter of real GUE data, and with each other?

**[Open the live interactive laboratory](https://zeta-zeros-lab-interactive.lindgreendavid.workers.dev)**

This is **not** a claim about the Riemann Hypothesis and not a proof of anything. It measures
numerical agreement. The protocol ([`docs/research-protocol.md`](docs/research-protocol.md)) was
committed before the registry was generated.

**Headline finding (v0.1.0):** the zeros are 5–12 times closer to GUE than to random points
(**H1, H2 confirmed**), but at these heights they are **measurably more regular than finite-size
GUE**: the spacing variance is 0.148 (low block) and 0.162 (high block), against 0.180 for GUE and
a 95% sampling band of 0.169–0.195, so **H3 is not confirmed**. The gap **shrinks with height**
(**H4 confirmed**). That direction matches published finite-height corrections to the
Montgomery–Odlyzko law, but this repository did **not** test that model. Full numbers and
limitations: [`docs/research-report.md`](docs/research-report.md).

## What's here

| Path | What it is |
| --- | --- |
| [`docs/research-protocol.md`](docs/research-protocol.md) | Hypotheses, statistics and thresholds, fixed before any result existed. |
| [`docs/research-report.md`](docs/research-report.md) | Results, dispositions, limitations, references, and a flagged exploratory thesis. |
| [`data/`](data/) | The two frozen blocks of zeta zeros (heights, 17 significant digits). |
| [`src/zeta_zeros_lab/`](src/zeta_zeros_lab/) | Unfolding, exact GUE law (Fredholm determinant), statistics, simulated null, validation. |
| [`scripts/`](scripts/) | `compute_zeros.py`, `verify_zeros.py` (Hardy-Z completeness), `generate_registry.py`, `compare_registry.py`. |
| [`reports/v0.1-zeta-registry.json`](reports/v0.1-zeta-registry.json) | The frozen results, including the hypothesis verdicts. |
| [`site/`](site/) | Interactive Next.js (vinext) laboratory for Cloudflare Workers. |

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
python scripts/verify_zeros.py                                   # completeness of both blocks (~1 min)
python scripts/generate_registry.py --output /tmp/registry.json  # ~3 min, seeded
python scripts/compare_registry.py reports/v0.1-zeta-registry.json /tmp/registry.json
zeta-zeros-lab                                                   # print the headline statistics
```

The zeros themselves can be recomputed with `python scripts/compute_zeros.py START COUNT OUT.csv`
(about 0.3–0.6 s per zero).

## Quality gates

```bash
ruff check . && ruff format --check . && mypy src && pytest     # 95% coverage gate
cd site && pnpm install && pnpm run sync-registry && pnpm run lint && pnpm run test
```

## Scope and limitations

Two blocks of 2,000 zeros; spacing and pair correlation only; smooth-density unfolding only; KS is
used as a distance, never a p-value (zeta spacings are not independent). See the report.

## License

MIT. See [`LICENSE`](LICENSE). Citation metadata: [`CITATION.cff`](CITATION.cff).
