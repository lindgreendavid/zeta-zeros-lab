# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-09

### Added

- Preregistered protocol (`docs/research-protocol.md`), committed before the registry existed: four
  hypotheses with numeric thresholds, an exact-GUE reference, a Poisson control, and a seeded
  simulated-GUE null for calibration.
- Two frozen blocks of 2,000 consecutive zeta zeros (n = 1…2000 and n = 100000…101999) computed
  with `mpmath`, verified complete by Hardy-Z sign alternation on every gap.
- Exact GUE nearest-neighbour spacing law via the sine-kernel Fredholm determinant (mean 1,
  variance 0.17999), replacing the approximate Wigner surmise.
- Frozen registry `reports/v0.1-zeta-registry.json` and research report. H1 and H2 confirmed; H3
  not confirmed (the zeros are more rigid than finite-size GUE); H4 confirmed (agreement improves
  with height).
- Interactive vinext/Cloudflare Workers site with a "which row is random?" exercise, spacing and
  pair-correlation charts with accessible data tables, and a statistics table against the simulated
  null.
