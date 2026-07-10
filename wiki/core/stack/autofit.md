---
title: PyAutoFit (autofit)
sources:
  - project: PyAutoFit
    paths:
      - autofit/mapper/
      - autofit/non_linear/
      - autofit/graphical/
      - autofit/aggregator/
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: 99e686c659bb02433afe526c2fb26c24f1840f64a147148fb9761fdd349e4f3a
---

# PyAutoFit (`autofit`, alias `af`)

The inference engine. Its sub-systems, each with a concepts page:

| Sub-system | Source | What it gives you | Page |
|---|---|---|---|
| Model mapper | `autofit/mapper/` | `af.Model`, `af.Collection`, priors, instances | [[../concepts/model_composition_and_priors]] |
| Non-linear searches | `autofit/non_linear/search/` | Nautilus, Dynesty, Emcee, Zeus, NUTS, LBFGS behind one interface | [[../concepts/non_linear_search]] |
| Analysis | `autofit/non_linear/analysis/` | the `af.Analysis` base your likelihood subclasses | [[../concepts/bayesian_inference]] |
| Samples | `autofit/non_linear/samples/` | posteriors, errors, evidence | [[../concepts/samples_and_posteriors]] |
| Aggregator / database | `autofit/aggregator/`, `autofit/database/` | bulk result loading, sqlite queries | [[../concepts/samples_and_posteriors]] |
| Graphical models | `autofit/graphical/`, `autofit/messages/` | factor graphs, hierarchical models, EP | [[../concepts/graphical_models_and_ep]] |
| Plot | `autofit/plot/` | corner plots, likelihood-vs-iteration, per-sampler plotters | [[../concepts/samples_and_posteriors]] |

The seam with your code is exactly two objects: an `af.Model` composed from **your
classes**, and an `af.Analysis` whose `log_likelihood_function(instance)` calls **your
likelihood**. Everything else — search, output, resumption, posterior analysis — is
engine.

API truth order (`AGENTS.md` "Source-of-truth resolution"): installed source /
`dir(af)` first, then `autofit_workspace` examples; never changelogs or memory.
