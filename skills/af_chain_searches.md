---
name: af_chain_searches
description: Chain non-linear searches — pass one fit's result into the next fit's priors or start points, so a cheap simplified fit hands a focused parameter space to the expensive full fit. Covers `result.instance` (fix at fitted values), `result.model` (posterior-updated priors), the `model_centred*` variants, and the Initializer start-point classes. Use when the user says "use the first fit to seed the second", "fix these components at the previous result", "chain searches", or wants a staged/pipelined analysis. Not for choosing a single sampler (af_configure_search) or combining datasets (that is the factor graph).
user-invocable: true
---

# Chaining searches

A staged analysis fits a deliberately simplified problem first, then uses its result to
focus the real fit: fewer wasted evaluations, more robust convergence, and each stage
cheap enough to inspect before committing to the next. PyAutoFit makes the hand-off a
one-liner — the design question is *what* to pass, and how tightly.

## Orient

A completed `Result` offers three hand-off currencies
(`PyAutoFit:autofit/non_linear/result.py`):

- **`result.instance.<component>`** — the max-likelihood *values*, passed as **fixed**
  (no longer free). Use for components the next stage treats as known.
- **`result.model.<component>`** — the component with **priors updated from the
  posterior**. The next search explores around stage 1's answer instead of the cold
  prior.
- **`result.model_centred*`** — explicit-width variants when you want to control the
  hand-off width rather than inherit the posterior's: `model_centred_absolute(a=...)`
  (GaussianPriors of absolute sigma `a` around the fitted values),
  `model_centred_relative(r=...)` (sigma = `r` × each value),
  `model_centred_max_lh_bounded(b=...)`.

Canonical runnable example: `autofit_workspace:scripts/features/search_chaining.py`.
Background: `wiki/core/concepts/initialization_and_chaining.md` — including the design
rule that a chain must *narrow* priors, never bias them.

## Ask

- What does stage 1 fix or learn, and what stays free in stage 2? (The split *is* the
  pipeline design.)
- Fixed values or refreshed priors for each passed component — is stage 1's answer
  trustworthy enough to freeze?

## Branch — pass fixed values vs updated priors

```python
"""
__Chained Fit__

Stage 1 fitted the left Gaussian alone. Stage 2 fixes it at the fitted values
(`result.instance`) while fitting the right Gaussian fresh — the left component costs
zero parameters in stage 2 (`PyAutoFit:autofit/non_linear/result.py`).
"""
model_2 = af.Collection(
    gaussian_left=result_1.instance.gaussian_left,   # fixed at stage-1 values
    gaussian_right=af.Model(Gaussian),               # free, cold priors
)

"""
__Prior Passing__

If stage 1's answer should guide but not freeze, pass `result.model` instead: the
component arrives with priors centred on the stage-1 posterior.
"""
model_3 = af.Collection(
    gaussian_left=result_1.model.gaussian_left,      # free, posterior-updated priors
    gaussian_right=af.Model(Gaussian),
)
```

Width control when the posterior's own width is not what you want handed on
(anti-lock-in: several × the stage-1 sigma is the usual safe choice):

```python
model_3 = result_1.model_centred_relative(r=0.5)     # sigma = 0.5 × each fitted value
```

## Branch — start points (same sampler, warmer start)

When the model is unchanged and only the *starting region* should improve — e.g.
seeding MCMC after a quick MLE — use an initializer rather than touching priors
(`PyAutoFit:autofit/non_linear/initializer.py`):

```python
"""
__Start Point__

Walkers start inside the given bounds; priors (and therefore the posterior and any
evidence) are unchanged — model.info confirms it.
"""
initializer = af.InitializerParamBounds(
    {model.centre: (49.0, 51.0), model.sigma: (9.0, 11.0)}
)
search = af.Emcee(name="warm_start", nwalkers=30, nsteps=500, initializer=initializer)
```

`InitializerBall` / `InitializerParamStartPoints` are the tighter variants; parameters
not named fall back to prior draws. Start points change *where sampling begins*, prior
passing changes *the inference itself* — say which you're doing out loud.

## Design rules (from the chaining wiki page)

1. Name every link's provider — never assume "something reasonable" seeds a consumer.
2. Chains narrow, never bias: a follow-up prior tight enough to lock in stage 1's
   systematics has replaced inference with anchoring.
3. Journal each link (`wiki/project/`): what was passed, in which currency, and why —
   a chained result is only reproducible if the seeding is.

## Combine

- Stage design usually pairs with `af_configure_search` (cheap sampler for stage 1,
  production sampler for stage 2) and `af_load_results` (inspect stage 1 before
  trusting it).
- Multi-dataset problems chain *into* the factor graph: fit one dataset alone, pass
  `result.model` as the shared components' starting priors
  ([[../wiki/core/concepts/graphical_models_and_ep]]).

## Further reading

- **Student / new to inference** — HowToFit's search-chaining chapter.
- **General reference** — [RTD: search chaining](https://pyautofit.readthedocs.io/en/latest/features/search_chaining.html).
- **Experienced PyAutoFit user** — `autofit_workspace:scripts/features/search_chaining.py`
  and `scripts/searches/start_point.py`.
