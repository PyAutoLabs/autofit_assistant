---
name: af_wrap_likelihood
description: Wrap the user's existing likelihood code into a PyAutoFit `Analysis` class — the assistant's defining task and the ideal domain-adaptation entry point. Takes a function or method the user already trusts (anything that scores parameters against their data), builds the `af.Analysis` subclass around it without altering its numerics, pairs it with a composed model, and validates the wrapper on hand-built instances before any fit. Use when the user says "wrap my likelihood", "connect my code to PyAutoFit", "I already have a function that computes chi-squared/log-likelihood", or brings analysis code of their own. Not for composing priors (af_compose_model) or running fits (af_run_search).
user-invocable: true
---

# Wrapping your likelihood

This is the assistant's defining task. You already have code that scores a parameter set
against your data — a chi-squared, a log-likelihood, a forward model plus a noise model.
Wrapping it into an `af.Analysis` connects it to everything PyAutoFit has: every sampler,
prior machinery, output/resumption, posterior analysis, graphical models. Your code keeps
doing the science; PyAutoFit does the inference around it.

**The constitution's rule applies throughout** (`AGENTS.md` "Safety invariants"): the
likelihood code is *yours*. The wrapper never re-parametrises, adds guards, or "fixes"
numerics. If something in it looks wrong, the assistant says so and you decide.

## Orient

An `Analysis` is a small class: it holds your data in `__init__` and implements one
method, `log_likelihood_function(self, instance) -> float`, where `instance` is a real
instance of your model classes with the search's current parameter values filled in
(`PyAutoFit:autofit/non_linear/analysis/`). The wrapper's whole job is translating
between that `instance` and your function's calling convention.

Read `wiki/core/concepts/bayesian_inference.md` for where the likelihood sits;
`autofit_workspace:scripts/cookbooks/analysis.py` is the canonical worked example.

## Ask

Four things decide the wrapper's shape — get them before writing code:

1. **The signature.** What does your function take — a parameter vector in a fixed
   order? Named arguments? An object? What does it return — log likelihood, chi-squared
   (→ `-0.5 * chi2` plus the noise term, see below), or something else?
2. **The data.** What arrays/objects does it need at call time, and how are they loaded?
3. **Log or not, and complete or not.** Is the returned quantity already a *log*
   likelihood, and does it include the noise normalisation term? (For model comparison
   the constant terms matter — [[../wiki/core/concepts/evidence_and_model_comparison]].)
4. **The parametrisation.** Which arguments are free parameters (→ the model,
   `af_compose_model`) and which are fixed configuration?

## Branch — the wrapper

The pattern, for a function `my_log_like(params: dict, data, noise)`:

```python
"""
Analysis: <the user's problem>
==============================

Wrap <user's module>.my_log_like into a PyAutoFit Analysis. The likelihood code is
unchanged — this class only translates the search's `instance` into the function's
calling convention.

__Contents__

- **Model component:** The class whose __init__ defines the free parameters.
- **Analysis:** The wrapper.
- **Validation:** Hand-built instances scored before any fit.
"""
import autofit as af
from my_package import my_log_like   # the user's code, imported not copied


class MyModel:
    """Free parameters of the fit — mirrors the arguments my_log_like expects."""
    def __init__(self, centre=0.0, amplitude=1.0, width=1.0):
        self.centre = centre
        self.amplitude = amplitude
        self.width = width


class Analysis(af.Analysis):
    def __init__(self, data, noise):
        super().__init__()
        self.data = data
        self.noise = noise

    def log_likelihood_function(self, instance) -> float:
        """Translate `instance` -> the user's convention; return their number."""
        params = {
            "centre": instance.centre,
            "amplitude": instance.amplitude,
            "width": instance.width,
        }
        return my_log_like(params, self.data, self.noise)
```

Variations by input shape:

- **Vector-in-fixed-order functions** — build the list from named attributes explicitly
  (`[instance.centre, instance.amplitude, ...]`); never rely on attribute iteration
  order.
- **Chi-squared functions** — return `-0.5 * chi2` *plus* the noise normalisation
  (`-0.5 * sum(log(2π σ²))`) if evidence will ever be compared. Ask the user before
  adding the term — it belongs to *their* data model; adding it is their call.
- **Expensive setup** (grids, kernels, splines) — do it once in `__init__`, not per
  likelihood call; this is packaging, not a numerics change.
- **Multiple datasets** — one `Analysis` per dataset, combined with
  `af.AnalysisFactor` + `af.FactorGraphModel`
  ([[../wiki/core/concepts/graphical_models_and_ep]]).

## Branch — validate before fitting

Never hand a wrapper straight to a sampler. Three checks, in order:

```python
"""
__Validation__

1. A hand-built instance with known-good parameters returns a finite float.
2. The value matches calling the user's function directly (same inputs, same number).
3. A deliberately bad instance scores WORSE (lower log likelihood) — the sign
   convention is right.

Hand-built plain instances of the user's class — no priors needed yet, so validation
runs before the prior conversation. (`instance_from_prior_medians()` etc. only work
after every parameter has a prior, from `af_compose_model` or prior config — a bare
`af.Model(MyModel)` on a class without prior config raises ConfigException.)
"""
analysis = Analysis(data=data, noise=noise)

good = MyModel(centre=50.0, amplitude=25.0, width=10.0)   # known-good values
ll_good = analysis.log_likelihood_function(good)
assert ll_good == my_log_like({"centre": good.centre, "amplitude": good.amplitude,
                               "width": good.width}, data, noise)

bad = MyModel(centre=-1e3, amplitude=1e-6, width=0.1)     # known to fit poorly
assert analysis.log_likelihood_function(bad) < ll_good
```

A wrapper that fails check 3 has a sign flip (chi-squared vs log-likelihood) — the most
common wrapping bug, and one a sampler will happily *minimise your fit quality* with.

## JAX triage (optional, one question)

If the user's function is pure JAX (or trivially convertible), gradient-based search
(`af.BlackJAXNUTS`) and GPU execution open up. Ask once — "is your likelihood
JAX-compatible / worth making so?" — and record the answer in `profile.md`
("Likelihood & model code"). Don't convert their code uninvited.

## Combine

- Priors for the new model: `af_compose_model` (each parameter's prior is a scientific
  statement — this conversation is where the user's domain knowledge lands).
- First fit: `af_run_search` — start with a cheap sampler budget; the wrapper's cost per
  call, measured during validation, sets the budget arithmetic.
- Record the wrap in `wiki/project/` (default-yes): the function wrapped, its
  convention, the validation numbers, and where the code lives — plus `profile.md`'s
  "Likelihood & model code" section, so future sessions skip this interview.
