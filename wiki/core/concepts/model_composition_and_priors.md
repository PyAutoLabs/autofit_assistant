---
title: Model composition and priors
sources:
  - project: PyAutoFit
    paths:
      - autofit/mapper/
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: 17c0db29d642cd841aad4a4f91026be19cbdef490d0afee521140ef26590a9d8
---

# Model composition and priors

## TL;DR

`af.Model(YourClass)` turns a plain Python class into a fittable model: each `__init__`
argument becomes a free parameter with a prior. `af.Collection(name=..., ...)` groups
components into one parameter space whose fitted `instance` mirrors the same named
structure. Priors are set explicitly per parameter; parameters can be fixed, linked, or
constrained by assertions (`PyAutoFit:autofit/mapper/`).

## Prior types and when each is right

| Prior | Statement it makes | Watch out |
|---|---|---|
| `af.UniformPrior(lower_limit, upper_limit)` | any value in range, equally plausible | implies a scale; too-wide ranges waste sampler effort |
| `af.LogUniformPrior(lower_limit, upper_limit)` | order of magnitude unknown (positive quantities) | log-prior diverges as value → 0: limits must be strictly positive, and a fit hugging the lower limit is a red flag |
| `af.GaussianPrior(mean, sigma)` | prior estimate with uncertainty | unbounded — pair with an assertion if the parameter has a hard physical bound |
| `af.TruncatedGaussianPrior(mean, sigma, lower_limit, upper_limit)` | estimate + hard physical range | truncation moves prior mass — relevant to evidence comparisons |

Rules of thumb:

- **Every prior is a scientific statement** — set each one deliberately and record the
  reasoning in the project journal; never rely on defaults for a production analysis.
- Priors can also live in `config/priors/*.yaml`, keyed by class — the right home for
  a *project's standard* parametrisation, so scripts stay clean and the choice is
  centralised (`PyAutoNerves:autonerves/`).

## Customization

```python
model = af.Model(Gaussian)
model.centre = 50.0                      # fixed — removed from the search
model.sigma = model.normalization        # linked — one dimension, two roles
model.add_assertion(model.sigma > 0.0)   # zero prior outside the constraint
```

Links work across `Collection` components (`model.b.centre = model.a.centre`) — the
standard way to express shared physical quantities. Assertions carve unphysical
corners out of the space; they are part of the prior, so they affect the evidence.

## Instances

The bridge back to your code: `model.random_instance()` draws from the priors;
`samples.max_log_likelihood()` / `samples.median_pdf()` return real instances of your
classes, so your own methods run on fitted results unchanged. This is also the model
sanity check — if random instances look unphysical, a prior is wrong.

## Serialisation

`model.output_to_json(file=...)` / `af.Model.from_json(file=...)` write and reload the
full composition including priors — commit the JSON with an analysis for an exact
reproducibility record.

## Advanced composition

Multi-level models (components containing components), `af.Array` for
NumPy-array-valued parameters, and free-form customization are covered by
`autofit_workspace:scripts/cookbooks/model.py`, `model_internal.py` and
`multi_level_model.py`.

## See also

- [[bayesian_inference]] · [[non_linear_search]] · the `af_compose_model` skill for
  the guided procedure.
