# sne_cosmology — Pantheon+ Type Ia supernova distances

A real-data demo: the Pantheon+SH0ES compilation of 1701 Type Ia supernova light-curve
fits, reduced to the columns a distance-modulus cosmology fit needs.

- `pantheon_plus_distances.csv` — columns: `cid` (supernova ID), `z_hd` (Hubble-diagram
  redshift), `z_hd_err`, `mu` (SH0ES-calibrated distance modulus `MU_SH0ES`),
  `mu_err_diag` (its **diagonal** uncertainty), `is_calibrator` (1 = Cepheid-calibrator
  SN, 0 = Hubble-flow).

## Provenance and citation

Extracted from the public Pantheon+SH0ES data release
(`Pantheon+SH0ES.dat`, https://github.com/PantheonPlusSH0ES/DataRelease). Any use of
these data must cite **Scolnic et al. 2022 (ApJ 938, 113)** for the Pantheon+ sample,
**Brout et al. 2022 (ApJ 938, 110)** for the cosmology analysis, and **Riess et al.
2022 (ApJL 934, L7)** for the SH0ES calibration.

## The deliberate simplification (read before drawing conclusions)

This demo uses **diagonal errors only**. The published analyses use the full
statistical+systematic covariance matrix (~1701×1701, in the same data release);
ignoring the off-diagonal terms *underestimates* parameter uncertainties and can shift
central values at the fraction-of-sigma level. That trade is made here so the
likelihood stays a few lines of transparent numpy — the point of the demo is the
inference workflow (wrap a likelihood → priors → sampler → posterior + evidence), not a
publishable H0. Extending the wrapper to the full covariance is a natural follow-up
exercise, and exactly the kind of change `af_wrap_likelihood` handles.

**Maintainer validation run** (flat ΛCDM, Hubble-flow SNe with `z_hd > 0.023`,
`is_calibrator = 0`; DynestyStatic `nlive=75`): `Ωm = 0.344 +0.021/−0.019`,
`H0 = 73.14 +0.27/−0.32 km s⁻¹ Mpc⁻¹` — consistent with the published Pantheon+SH0ES
values (Ωm = 0.334 ± 0.018, H0 = 73.30 ± 1.04), with the too-small H0 error expected
from the diagonal approximation and no systematics floor.

Try it: the README's Example Prompt 3 uses this dataset to demonstrate assistant-mode
autonomy end-to-end.
