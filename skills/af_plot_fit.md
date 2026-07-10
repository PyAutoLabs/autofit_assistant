---
name: af_plot_fit
description: Visualise fits and posteriors — corner plots and search diagnostics via autofit.plot (aplt), model-vs-data and residual figures via matplotlib over model instances, and the af.ex.plot_profile_1d helper for 1D profiles. Use when the user says "plot the fit", "show me the corner plot", "plot residuals", or wants figures from a completed search. Not for the in-search Visualizer hooks (that is af_custom_analysis) or for loading the results being plotted (af_load_results).
user-invocable: true
---

# Plotting fits and posteriors

Two kinds of figure answer two different questions. **Posterior plots** (corner,
trace) ask *what did the inference conclude and can I trust it*; **fit plots**
(model-vs-data, residuals) ask *does the model actually describe the data*. A healthy
analysis looks at both — a beautiful corner plot over a terrible fit is the classic
trap.

## Orient

PyAutoFit ships search-level plotting as `autofit.plot` (imported `aplt`); at the
pinned stack the entry points are `corner_cornerpy`, `corner_anesthetic`,
`log_likelihood_vs_iteration`, `subplot_parameters` and `output_figure`
(`PyAutoFit:autofit/plot/` — verify with `dir(aplt)`, never memory). Domain plots are
deliberately *not* framework-owned: your data is yours, so model-vs-data figures are
plain matplotlib over model instances.

The plot-output conventions from `_style.md` apply: deterministic paths under
`scripts/scratch/<context>/`, print the absolute path, quote it back and offer to
open it.

## Ask

- Which question first — posterior health or fit quality?
- One fit or a comparison across fits (→ load via the aggregator first,
  `af_load_results`)?

## Branch — posterior plots

```python
"""
__Corner Plot__

The pairwise posterior — degeneracies, multi-modality and prior-edge pile-ups are all
visible here and invisible in a summary table (`PyAutoFit:autofit/plot/`).
"""
import autofit.plot as aplt

samples = result.samples
aplt.corner_cornerpy(samples=samples)
```

`log_likelihood_vs_iteration(samples=samples)` is the convergence-at-a-glance
diagnostic; `subplot_parameters(samples=samples)` panels the per-parameter behaviour.
Read a corner plot for: contours truncated at a prior limit (prior too tight),
banana/curved degeneracies (consider reparametrising), separated islands (multi-modal
— ensemble MCMC results are suspect, [[../wiki/core/concepts/mcmc_and_hmc]]).

## Branch — fit plots (model vs data)

Instances are real instances of your classes, so the model curve is one method call:

```python
"""
__Fit + Residuals__

Model-vs-data and normalised residuals from the max-likelihood instance. Residuals
should look like noise: structure in them is model error, and no posterior statistic
substitutes for looking (`_style.md` "Plot output and path announcement").
"""
import matplotlib.pyplot as plt
import numpy as np

best = result.samples.max_log_likelihood()
xvalues = np.arange(data.shape[0])
model_data = best.model_data_from(xvalues=xvalues)

fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])
ax0.errorbar(xvalues, data, yerr=noise_map, fmt=".k", ms=3, elinewidth=0.5)
ax0.plot(xvalues, model_data, "r-")
ax1.plot(xvalues, (data - model_data) / noise_map, ".k", ms=3)
ax1.axhline(0.0, color="r", lw=0.5)
ax1.set_ylabel("residuals / sigma")

out = "scripts/scratch/my_fit/fit.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Saved to: {__import__('pathlib').Path(out).resolve()}")
```

Posterior *uncertainty on the curve*: overplot `model_data_from` for a few dozen
posterior draws at low alpha — the honest band, no Gaussian assumption. For 1D
profiles, `af.ex.plot_profile_1d(xvalues=..., profile_1d=...,
output_path=pathlib.Path(...), output_filename=...)` wraps the same figure in one
call — note `output_path` must be a `pathlib.Path`, not a string (the helper joins
with the `/` operator; a str raises TypeError).

## Combine

- The numbers behind the figures: `af_load_results`. In-search live figures: the
  Visualizer in `af_custom_analysis`. Residual structure you can't explain:
  `af_debug_fit_failure`.
- Publication-bound figures belong in a science project's `results/figures/` with a
  run manifest (`start-new-project` Phase 2), not in scratch.

## Further reading

- **General reference** — [RTD: result cookbook](https://pyautofit.readthedocs.io/en/latest/cookbooks/result.html) (plotting sections).
- **Experienced PyAutoFit user** — `autofit_workspace:scripts/plot/` (per-sampler
  plotter scripts).
