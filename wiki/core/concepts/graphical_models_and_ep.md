---
title: Graphical models and expectation propagation
sources:
  - project: PyAutoFit
    paths:
      - autofit/graphical/
      - autofit/messages/
    pinned_commit: 31537d5f5ae865aca69d10e6901741533116ed65
last_updated: 2026-07-10
content_sha256: e354936533e079415896523a8c592f2133d562548feb4f951d510f379828ccc5
---

# Graphical models and expectation propagation

## TL;DR

When many datasets share model structure — every dataset has its own nuisance
parameters, but some parameters are common or drawn from a shared (hierarchical)
distribution — sampling the enormous joint space is wasteful and often intractable.
PyAutoFit's answer is a **factor graph**: one factor per dataset, plus prior factors,
with **expectation propagation (EP)** iterating low-dimensional per-factor fits until
the shared variables' posteriors agree (`PyAutoFit:autofit/graphical/`).

## The factor-graph API (no EP required)

```python
analysis_factor_list = [
    af.AnalysisFactor(prior_model=model_i, analysis=analysis_i)
    for model_i, analysis_i in zip(models, analyses)
]
factor_graph = af.FactorGraphModel(*analysis_factor_list)

result_list = search.fit(model=factor_graph.global_prior_model, analysis=factor_graph)
```

This composes the joint problem and fits it with one search. It replaces the removed
analysis-summing combine (joining analyses with the addition operator, or folding a
list of them with the builtin sum) — that overload is gone; the factor graph is the
current multi-dataset combine
(`autofit_workspace:scripts/features/graphical_models.py`).

Hierarchical extensions declare that per-dataset parameters are draws from a shared
parent distribution whose hyper-parameters are themselves free — the factor graph
gains a hierarchical factor connecting them.

## Expectation propagation — fitting the graph piece by piece

For graphs too large to sample jointly, EP approximates the posterior with an
exponential-family "message" per factor per variable and iterates over factors:

1. **Cavity** — combine every *other* factor's messages (natural parameters add).
2. **Tilted fit** — fit this factor against the cavity-as-priors. PyAutoFit's
   distinctive move: this fit is a full non-linear search (e.g. Dynesty/Nautilus), so
   each dataset is fit in its own low-dimensional space.
3. **Moment match** — project the tilted posterior back onto the exponential family.
4. **Update with damping** — an exponential moving average on natural parameters
   guards against oscillation; invalid projections fall back to the previous message.

Convergence is declared when successive global mean fields agree (KL-based
tolerance). Messages live in `PyAutoFit:autofit/messages/`; the optimiser loop in
`PyAutoFit:autofit/graphical/expectation_propagation/`.

When a factor is conjugate with its cavity, the update is **analytic** — no sampler —
which is dramatically faster where it applies.

## Practical guidance

- Start with the plain factor graph and one joint search; reach for EP when the joint
  dimensionality or dataset count makes that infeasible.
- EP is iterative and approximate: inspect per-factor convergence history, and treat
  shared-variable posteriors that keep drifting between sweeps as unconverged, not as
  results.
- Evidence from an EP mean field has historically been the layer's sharpest edge —
  the bookkeeping was overhauled in mid-2026 (nested-sampler factor fits). For
  model-comparison-grade evidence, check the current status on the PyAutoFit issue
  tracker before relying on it.

## Reading

- Minka (2001), *Expectation Propagation for Approximate Bayesian Inference* — the
  original algorithm.
- Vehtari et al. (2020), *Expectation propagation as a way of life* — the
  data-partitioned framing PyAutoFit's per-dataset factors follow.

## See also

- [[bayesian_inference]] · [[nested_sampling]] (the per-factor sampler) ·
  [[model_composition_and_priors]] (shared/linked parameters in one search).
