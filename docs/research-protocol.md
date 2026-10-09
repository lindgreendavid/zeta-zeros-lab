# Research protocol (v0.1)

Written and committed before the registry `reports/v0.1-zeta-registry.json` was generated or
interpreted. Every hypothesis, statistic, and threshold below is fixed here.

## Research question

The nontrivial zeros of the Riemann zeta function, written `1/2 + i*gamma_n`, are widely
observed to have local statistics matching the eigenvalues of large random Hermitian matrices
from the Gaussian Unitary Ensemble (GUE): Montgomery (1973) derived the pair correlation for a
restricted class of test functions assuming the Riemann Hypothesis, and Odlyzko (1987, 1989)
confirmed the agreement numerically. This study asks a bounded, checkable question:

> For two disjoint blocks of 2,000 consecutive zeros, one at the bottom of the critical strip
> and one near the 100,000th zero, how close are the empirical nearest-neighbour spacing
> distribution and pair correlation to their GUE predictions — compared with (a) the Poisson
> alternative, (b) the natural sampling scatter of genuine GUE data of the same size, and
> (c) each other?

This is **not** a claim about the Riemann Hypothesis, which remains open, and not a proof of
anything. It measures finite numerical agreement.

## Data

Heights `gamma_n` are computed independently with `mpmath.zetazero` (18 significant digits) and
frozen in `data/`:

- **low**: zeros n = 1 … 2000 (`data/zeros-low.csv`, heights ≈ 14.13 … 2515)
- **high**: zeros n = 100000 … 101999 (`data/zeros-high.csv`, heights ≈ 74920.83 … ≈ 75,000s)

A block is accepted only after `zeta_zeros_lab.validation` confirms: strictly increasing
heights; consecutive indices; `|n - N_smooth(gamma_n)| <= 2.5` for every zero (a missed or
duplicated zero shifts this by a whole integer for all later zeros); and, for the low block,
the first five zeros match the published values to 1e-9.

## Unfolding

`x_n = theta(gamma_n)/pi + 1`, where `theta` is the Riemann–Siegel theta function (its
asymptotic series, checked against `mpmath.siegeltheta`). Unfolded spacings `s_n = x_{n+1} -
x_n` have mean 1. Only the *smooth* density is removed; no refinement is applied.

## Reference laws

- **GUE nearest-neighbour spacing**: the *exact* law from the sine-kernel Fredholm determinant
  `E(s) = det(I - K_s)` (Gauss–Legendre quadrature, 48 nodes); `F(s) = 1 + E'(s)`. Not the Wigner
  surmise. Self-checks: mean = 1, variance = 0.17999 (published value ≈ 0.180).
- **GUE pair correlation**: `R2(r) = 1 - (sin(pi r)/(pi r))^2`, averaged over each bin.
- **Poisson control**: spacing CDF `1 - exp(-s)`, `R2 = 1`.
- **Calibrated null**: 150 replicate GUE samples (seed `20260920`). Each replicate pools
  central, semicircle-unfolded eigenvalues of independent 800×800 GUE matrices until 1,999
  spacings are available (the same size as a zeta block) and computes exactly the statistics
  below. Because a single zeta block is one realization, its distance from GUE is meaningful
  only relative to this null.

## Statistics (identical for zeta and the simulated null)

1. `ks_gue`, `ks_poisson`: Kolmogorov–Smirnov **distances** of the spacings to each CDF. KS is
   used only as a distance: zeta spacings are not independent, so KS *p-values* are invalid
   and are never reported.
2. `r2_rms_gue`, `r2_rms_poisson`: root-mean-square difference between the empirical pair
   correlation (30 bins of width 0.1 on lags in (0, 3]) and the GUE / Poisson prediction.
3. `variance` of the spacings (GUE: 0.17999; Poisson: 1).
4. `small_fraction`: fraction of spacings below 0.25 (Poisson: 0.2212; GUE: 0.0163).

## Hypotheses and pass/fail criteria

- **H1 — GUE beats Poisson.** In **each** block, `ks_gue < ks_poisson` **and**
  `r2_rms_gue < r2_rms_poisson`. *Falsified if either inequality fails in either block.*
- **H2 — level repulsion.** In each block, `small_fraction < 0.0737` (one third of the Poisson
  value). *Falsified if either block exceeds it.*
- **H3 — statistically indistinguishable from GUE at this sample size.** In each block,
  `ks_gue` and `r2_rms_gue` are each at or below the 97.5th percentile of the simulated GUE
  null, and `variance` lies within the null's 2.5–97.5 percentile range. *Not confirmed if any
  of the six checks fails; each is reported individually.*
- **H4 — agreement improves with height.** The high block has smaller `ks_gue` **and** smaller
  `r2_rms_gue` than the low block (the direction predicted by the finite-height correction
  theory of Bogomolny & Keating, whose leading corrections decay like 1/log(height)). A
  mixed or reversed outcome means *not confirmed*. Because each block is one realization, this
  tests direction only and cannot establish the size of an effect.

## Scope boundaries, declared before results

- Two blocks of 2,000 zeros only; no claim about other heights or about the limit.
- Nearest-neighbour spacing and pair correlation only — no higher correlations, no number
  variance or rigidity statistics.
- Smooth-density unfolding only.
- Simulated null uses 800×800 GUE matrices with the central half of each spectrum; finite-N
  effects at that size are far below the sampling scatter being calibrated.
- Pair-correlation edge effects are of relative order lag/N (≤ 0.15%) and are not corrected.
- No claim about the Riemann Hypothesis, and no claim that the numerical agreement explains
  *why* the zeros behave this way.
