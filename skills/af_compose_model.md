---
name: af_compose_model
description: Compose a PyAutoFit model from the user's parametrisation — turn Python classes into `af.Model` objects, combine components with `af.Collection`, and set every prior deliberately (uniform, log-uniform, Gaussian, fixed, linked, asserted). Use when the user wants to define what is being fitted — "set up my model", "what priors should I use", "fix this parameter", "tie these two parameters together". Not for writing the likelihood (that is `af_wrap_likelihood` / a custom Analysis) or for running the fit (that is `af_run_search`).
user-invocable: true
---

# Composing a model and its priors

Model composition is where your science becomes a statistics problem: each free
parameter you declare is a dimension of the space the non-linear search must explore,
and each prior is a statement about what you believe before seeing the data. Getting
this step right matters more than any sampler setting — an over-free model wastes
compute and an ill-considered prior can silently drive the posterior.

The deliverable is a `scripts/` Python script (workspace style, `_style.md`) that
composes the user's model, prints its `model.info` summary, and is ready to hand to
`af_run_search`.

## Orient

PyAutoFit composes models from **plain Python classes** — usually the user's own. The
class's `__init__` arguments become the model's free parameters
(`PyAutoFit:autofit/mapper/model.py`). If the user has already adapted the assistant to
their domain, read `wiki/project/profile.md` for their standard parametrisation before
proposing one.

Read `wiki/core/concepts/model_composition_and_priors.md` for the underlying ideas
(once the core wiki lands; until then the canonical reference is
`autofit_workspace:scripts/cookbooks/model.py`).

## Ask

- What are the components of the model, physically? One class or several?
- For each parameter: what is physically plausible, and is the scale known to within
  a factor of a few (→ uniform/Gaussian) or uncertain over decades (→ log-uniform)?
- Should any parameter be fixed, or shared between components?

## Branch — a single component

```python
"""
__Model__

The Gaussian's three `__init__` arguments become free parameters. Priors are set
explicitly — never rely on defaults for a real analysis; each prior is a scientific
statement (`PyAutoFit:autofit/mapper/model.py`).
"""
import autofit as af

model = af.Model(Gaussian)
model.centre = af.UniformPrior(lower_limit=0.0, upper_limit=100.0)
model.normalization = af.LogUniformPrior(lower_limit=1e-4, upper_limit=1e4)
model.sigma = af.GaussianPrior(mean=10.0, sigma=5.0)

print(model.info)
```

Prior choice in one line each: `UniformPrior` = "any value in this range, equally";
`LogUniformPrior` = "the order of magnitude is unknown" (strictly positive quantities
only — its log-prior diverges at zero); `GaussianPrior` = "I have an estimate with an
uncertainty"; `TruncatedGaussianPrior` = the same, hard-bounded to a physical range.

## Branch — customization: fixing, linking, asserting

```python
"""
__Model Customization__

Fixed values remove a dimension from the search; links declare two parameters equal;
assertions carve away unphysical corners of the space.
"""
model = af.Model(Gaussian)
model.centre = 50.0                        # fixed — no longer free
model.sigma = model.normalization          # linked — one dimension, two roles
model.add_assertion(model.sigma > 0.0)     # rejected regions get zero prior
```

Priors can also be passed at construction:
`af.Model(Gaussian, centre=af.UniformPrior(lower_limit=0.0, upper_limit=1.0))`.

## Branch — multiple components with `af.Collection`

```python
"""
__Collection__

A Collection groups components under named attributes; the search sees one flat
parameter space, the likelihood receives a matching `instance` with the same named
attributes (`instance.gaussian`, `instance.exponential`).
"""
model = af.Collection(gaussian=af.Model(Gaussian), exponential=af.Model(Exponential))

model.gaussian.centre = af.UniformPrior(lower_limit=0.0, upper_limit=100.0)
model.exponential.rate = af.LogUniformPrior(lower_limit=1e-2, upper_limit=1e1)

# Cross-component sharing works exactly like within-component linking:
model.exponential.centre = model.gaussian.centre
```

## Branch — save and reload the model

```python
"""
__Json Output__

A composed model serialises to human-readable JSON — commit it with the analysis so
the exact parametrisation and priors are part of the paper's reproducibility record.
"""
model.output_to_json(file="scripts/model.json")
model = af.Model.from_json(file="scripts/model.json")
```

## Sanity checks before fitting

- `model.prior_count` — is the dimensionality what you expect?
- `model.random_instance()` — instantiate from the priors and eyeball the values;
  wildly unphysical draws mean a prior is wrong.
- `print(model.info)` — the full tree, priors included; paste it into the
  `wiki/project/` entry for the fit.

## Combine

- The model meets its data through an `Analysis` class — the user's own likelihood is
  wrapped via `af_wrap_likelihood`; simple built-in-style cases via `af_custom_analysis`.
- Configure the sampler with `af_configure_search`, run with `af_run_search`.
- Offer (default-yes) a dated `wiki/project/` entry recording the parametrisation and
  the reasoning behind each prior.

## Further reading

- **Student / new to inference** — HowToFit chapter 1: model composition from first
  principles.
- **General reference** — [RTD: model cookbook](https://pyautofit.readthedocs.io/en/latest/cookbooks/model.html).
- **Experienced PyAutoFit user** — `autofit_workspace:scripts/cookbooks/model.py`
  (also `model_internal.py`, `multi_level_model.py` for advanced composition).
