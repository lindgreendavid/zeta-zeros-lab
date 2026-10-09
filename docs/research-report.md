# Research report (v0.1)

What the frozen registry (`reports/v0.1-zeta-registry.json`) shows, hypothesis by hypothesis,
against the thresholds fixed in [`research-protocol.md`](research-protocol.md) before the
registry existed. Data: zeros n = 1…2000 (heights 14.13…2515.29) and n = 100000…101999 (heights
74920.83…76257.69), 1,999 unfolded spacings each. Every number can be reproduced with
`python scripts/generate_registry.py`.

## Data integrity first

Both blocks passed every completeness check before any statistic was computed:

| Check | Low block | High block |
| --- | --- | --- |
| Heights strictly increasing, indices consecutive | pass | pass |
| max \|n − N_smooth(γ_n)\| (screen: ≤ 2.5) | 1.255 | 1.606 |
| Hardy-Z sign alternation on every gap (1,999 of 1,999) | pass | pass |
| First five zeros equal published values (1e-9) | pass | n/a |

The Z-sign test is the decisive one: a single missed or duplicated zero always breaks the
alternation (and a unit test deletes a zero to prove it does).

## Headline

The zeta zeros are **overwhelmingly closer to random-matrix (GUE) statistics than to random points**,
yet at these heights they are **measurably more regular than finite-size GUE** — and that gap
**shrinks with height**.

| Statistic | Low block | High block | Exact GUE | Poisson | GUE sampling band (95%) |
| --- | --- | --- | --- | --- | --- |
| Spacing KS distance to GUE | 0.0426 | 0.0255 | n/a | 0.3161 / 0.3052 (distance to Poisson) | ≤ 0.0243 (median 0.0151) |
| Pair-correlation RMS to GUE | 0.0681 | 0.0606 | n/a | 0.3608 / 0.3489 (distance to Poisson) | ≤ 0.0703 (median 0.0553) |
| Spacing variance | 0.1479 | 0.1618 | 0.17999 | 1 | 0.1686 – 0.1946 |
| Share of spacings < 0.25 | 0.0080 | 0.0110 | 0.0163 | 0.2212 | 0.0115 – 0.0225 |

## Hypothesis disposition

- **H1 — GUE beats Poisson: confirmed.** In both blocks the KS distance and the pair-correlation
  RMS are 5 to 12 times smaller to GUE than to Poisson (e.g. 0.0255 vs 0.3052 for the high block).
- **H2 — level repulsion: confirmed.** Only 0.80% (low) and 1.10% (high) of spacings fall below
  0.25, against 22.1% for random points and a threshold of 7.37%.
- **H3 — statistically indistinguishable from GUE: not confirmed.** Of the six checks, two pass
  and four fail:
  - Pair-correlation RMS is inside the GUE sampling band in both blocks (0.0681 and 0.0606 vs a
    95% limit of 0.0703) — **passes**.
  - Spacing KS distance is outside the band in both blocks: clearly in the low block (0.0426, about
    2.8× the null median) and only marginally in the high block (0.0255 vs a limit of 0.0243).
  - Spacing variance is below the whole band in both blocks (0.1479 and 0.1618 vs a lower limit of
    0.1686), i.e. the zeros are *more rigid* than genuine GUE samples of this size.
- **H4 — agreement improves with height: confirmed.** The high block is closer to GUE on both
  distances (KS 0.0255 < 0.0426; RMS 0.0606 < 0.0681), and its variance (0.1618) is closer to
  0.180 than the low block's (0.1479). As protocol stated, each block is one realization, so this
  establishes direction only, not the size of the effect.

## Interpretation, kept separate from the evidence

The pair correlation at the smallest lags sits *below* the GUE curve in both blocks (first bin
centres 0.005 and 0.025 versus 0.011 and 0.074 for GUE in the low block), the same extra
repulsion seen in the spacings. A tidy, known explanation exists: the Montgomery–Odlyzko
agreement is an asymptotic statement, and at finite height the zeros are described better by
a Gaussian Unitary Ensemble of *finite effective dimension*, growing only like the logarithm of the
height, with computable corrections (Bogomolny, Bohigas, Leboeuf & Monastra, *J. Phys. A* 39,
10743 (2006); see also Odlyzko 1987). That predicts exactly the direction measured here — more
rigid than the limit, improving with height. **This repository did not test that model**: no
effective dimension was fitted and the quantitative prediction was not compared with the data.
The agreement of direction is suggestive, not confirmed.

## Limitations (declared in advance)

- Two blocks of 2,000 zeros; nothing is claimed about other heights or the asymptotic limit.
- Nearest-neighbour spacing and pair correlation only; no higher correlations or rigidity.
- Smooth-density unfolding only. Residual edge effects in the pair correlation are of relative
  order lag/N (≤ 0.15%).
- The simulated null uses 800×800 GUE matrices (central half of the spectrum), 150 replicates, so
  band edges carry their own sampling error of a few percent; the high block's KS exceedance
  (0.0255 vs 0.0243) is within that uncertainty and should be read as marginal.
- KS values are distances, never p-values, because zeta spacings are not independent.
- The "which row is random?" strip on the site is an illustration drawn from a single seeded
  sample of 61 points per row; no reported statistic uses it.
- No claim about the Riemann Hypothesis, and no explanation of *why* the statistics arise.

## Exploratory thesis (not a finding)

A well-posed next experiment, to be preregistered as v0.2 *before* running it: replace the
infinite-N GUE reference with a **circular unitary ensemble of effective dimension N_eff**, set
N_eff for each block from the published log-height formula **without fitting to this data**, and
test whether the spacing KS distance and variance of both blocks then fall inside that model's
simulated sampling band. If they do, finite-height rigidity is explained quantitatively; if not,
the residual is a genuine open discrepancy. Either outcome would be informative, and neither is
asserted here.

## References

- H. L. Montgomery, "The pair correlation of zeros of the zeta function", *Proc. Sympos. Pure Math.* 24 (1973), 181–193.
- A. M. Odlyzko, "On the distribution of spacings between zeros of the zeta function", *Math. Comp.* 48 (1987), 273–308.
- F. J. Dyson, "Statistical theory of the energy levels of complex systems", *J. Math. Phys.* 3 (1962), 140–175.
- M. L. Mehta, *Random Matrices*, 3rd ed. (Elsevier, 2004).
- F. Bornemann, "On the numerical evaluation of distributions in random matrix theory: a review", *Markov Process. Related Fields* 16 (2010), 803–866.
- E. B. Bogomolny, O. Bohigas, P. Leboeuf, A. G. Monastra, "On the spacing distribution of the Riemann zeros: corrections to the asymptotic result", *J. Phys. A* 39 (2006), 10743–10754.
- H. M. Edwards, *Riemann's Zeta Function* (Academic Press, 1974).
