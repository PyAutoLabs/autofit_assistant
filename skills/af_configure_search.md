---
name: af_configure_search
description: Choose and configure a PyAutoFit non-linear search — nested samplers (Nautilus, DynestyStatic/Dynamic), MCMC (Emcee, Zeus, BlackJAXNUTS), and MLE optimizers (LBFGS, Drawer) — including output paths, cores, initializers and per-sampler settings. Use when the user asks "which sampler should I use", "configure the search", or wants to tune convergence/runtime. Not for actually executing the fit (that is `af_run_search`) or for composing the model (that is `af_compose_model`).
user-invocable: true
---

# Choosing and configuring the non-linear search

The search is the engine that explores the model's parameter space. The choice is
statistical before it is computational: **do you need the Bayesian evidence** (for
model comparison) — then a nested sampler; **or only the posterior** of a model you've
already committed to — then MCMC is often more efficient; **or just a quick maximum
likelihood estimate** — then an optimizer, accepting that it returns a point, not a
distribution.

## Orient

Every search class shares the same construction pattern: a `name`/`path_prefix` that
decides where output lands, `number_of_cores` for parallelisation, and per-sampler
settings (`PyAutoFit:autofit/non_linear/search/`). The installed roster (verify with
`dir(af)` — never from memory): `Nautilus`, `DynestyStatic`, `DynestyDynamic` (nested);
`Emcee`, `Zeus`, `BlackJAXNUTS` (MCMC); `LBFGS`, `Drawer` (MLE).

Read `wiki/core/concepts/non_linear_search.md` for the decision guide (until the core
wiki lands, the canonical references are `autofit_workspace:scripts/searches/nest.py`,
`mcmc.py`, `mle.py`).

## Ask

- Do you need the evidence (model comparison now or later)? If yes → nested.
- How expensive is one likelihood evaluation, and how many parameters? (Rules of
  thumb: nested samplers shine ≲ ~30 dimensions; MCMC scales further but needs
  initialization care; gradient-based NUTS needs a differentiable likelihood.)
- Where should output go, and how many cores may the fit use?

## Branch — nested sampling (evidence + posterior)

```python
"""
__Search__

Nautilus is the recommended default nested sampler: neural-network-boosted region
sampling, robust on multi-modal posteriors, and it returns the Bayesian evidence
(`PyAutoFit:autofit/non_linear/search/nest/nautilus/`).
"""
import autofit as af

search = af.Nautilus(
    path_prefix="my_project",
    name="gaussian_fit_nautilus",
    unique_tag="dataset_1",     # separates output per dataset
    n_live=200,                  # more live points = more accurate, slower
    number_of_cores=4,
)
```

`af.DynestyStatic(nlive=50, ...)` / `af.DynestyDynamic(...)` are the alternative nested
samplers — long-standing, well-understood defaults with extensive literature.

## Branch — MCMC (posterior only)

```python
"""
__Search__

Emcee's affine-invariant ensemble is a dependable default when the evidence is not
needed. Initialization matters: by default walkers start from the priors; an
`InitializerBall` concentrates them around a starting point — powerful with a good
guess, biased with a bad one (`PyAutoFit:autofit/non_linear/search/mcmc/emcee/`).
"""
search = af.Emcee(
    name="gaussian_fit_emcee",
    nwalkers=30,
    nsteps=1000,
)
```

`af.Zeus` (slice-sampling ensemble) often mixes faster on correlated posteriors;
`af.BlackJAXNUTS` is the gradient-based option when the likelihood is JAX-differentiable.
Convergence is governed by auto-correlation settings (`af.AutoCorrelationsSettings`) —
see `autofit_workspace:scripts/searches/mcmc.py`.

## Branch — MLE / optimizers

```python
"""
__Search__

LBFGS climbs to a maximum-likelihood point — fast, no posterior, no evidence. Right
for quick checks and for seeding a later sampler via start points; wrong as the final
answer of a Bayesian analysis (`PyAutoFit:autofit/non_linear/search/mle/`).
"""
search = af.LBFGS(name="gaussian_fit_lbfgs")
```

## Output discipline

`path_prefix` + `name` (+ `unique_tag`) map to `output/<path_prefix>/<name>/<tag>/…`.
Keep them stable across re-runs of the same fit — PyAutoFit resumes a completed search
from its output rather than re-running it, which is exactly what you want and worth
telling the user before they wonder why a second run finishes instantly.

Per-sampler defaults live in `config/non_linear/` — a project can retune a sampler
globally there instead of repeating kwargs in every script
(`PyAutoNerves:autonerves/conf.py`).

## Combine

- Hand the configured search plus the model/analysis to
  [`af_run_search`](./af_run_search.md).
- If the user is choosing *between* samplers for a production analysis, propose a
  benchmark on their real likelihood rather than folklore — a short run of each on the
  same fit, comparing wall-time and (for nested) evidence stability.

## Further reading

- **Student / new to inference** — HowToFit chapter 2: what a non-linear search is.
- **General reference** — [RTD: search cookbook](https://pyautofit.readthedocs.io/en/latest/cookbooks/search.html).
- **Experienced PyAutoFit user** — `autofit_workspace:scripts/searches/` (`nest.py`,
  `mcmc.py`, `mle.py`, `start_point.py`).
