---
title: MLE and optimizers
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/search/mle/
    pinned_commit: 31537d5f5ae865aca69d10e6901741533116ed65
last_updated: 2026-07-10
content_sha256: c20b058b14e898416726a326cd3034bc5cf43bd1b296af14ca72983272e951f1
---

# MLE and optimizers

## TL;DR

Optimizers climb to a maximum-likelihood point: fast, no posterior, no evidence. In a
Bayesian workflow they are reconnaissance and plumbing — timing the likelihood,
sanity-checking the model, finding a basin to seed a sampler — never the final answer
(`PyAutoFit:autofit/non_linear/search/mle/`).

## The shipped optimizers

- **`af.LBFGS`** — quasi-Newton ascent; the workhorse for "where is the peak, roughly,
  and does my likelihood behave?".
- **`af.Drawer`** — draws N samples straight from the priors and keeps the best. Not
  really an optimizer: it is the sanity baseline. If Drawer's best likelihood is close
  to your sampler's, the sampler learned nothing the prior didn't already know — a
  strong hint the data are uninformative or the likelihood is broken.

## Legitimate uses

1. **Likelihood smoke test** — an LBFGS run that immediately plateaus at the starting
   point usually means a flat or broken likelihood, found in seconds instead of after
   an hour of sampling.
2. **Chain seeding** — the middle link of provider→consumer chains:
   NS → MLE polish → MCMC ([[initialization_and_chaining]]).
3. **Runtime scouting** — the cheapest way to count likelihood evaluations per unit
   progress before committing a sampler budget.

## The trap

An MLE point with error bars from a local Hessian is **not** a posterior: it misses
multi-modality, non-Gaussian degeneracies, and every parameter-volume effect that
priors and marginalisation encode. If a number goes in a paper, it comes from
[[samples_and_posteriors]], not from an optimizer.

## See also

- [[non_linear_search]] · [[initialization_and_chaining]] ·
  `autofit_workspace:scripts/searches/mle.py`.
