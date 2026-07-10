---
title: Nested sampling
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/search/nest/
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: 7b45b6b49438804dc8f4072e6e3952b330ca7737c40c65f4fcf84d6aea618358
---

# Nested sampling

## TL;DR

Nested sampling is the **evidence-first** sampler family: it maintains a set of "live
points" drawn from the prior and repeatedly replaces the worst one with a new point at
higher likelihood, integrating the marginal likelihood Z as it shrinks inward. The
posterior comes out as weighted by-product samples. It is multi-modal-safe (no burn-in,
no starting point) and the reason PyAutoFit can do routine Bayesian model comparison
(`PyAutoFit:autofit/non_linear/search/nest/`).

## The shipped samplers

### `af.Nautilus` — recommended default

Neural-network-boosted region sampling: a network learns the likelihood contour so new
live points are proposed efficiently even in curved, degenerate spaces. Key knobs:

- `n_live` — accuracy/cost dial; more live points resolve more modes and tighten the
  evidence error.
- `number_of_cores` — likelihood evaluations parallelise across cores.

### `af.DynestyStatic` / `af.DynestyDynamic`

The long-standing pure-Python nested samplers, extensively documented in the
literature. `Static` keeps `nlive` fixed (predictable, evidence-oriented); `Dynamic`
re-allocates live points adaptively (posterior-oriented). Key knobs: `nlive`, `dlogz`
(evidence-precision stopping criterion), `maxiter`.

## Failure signatures

- **Evidence estimates that wander between reruns** — too few live points for the
  structure of the space; raise `n_live`/`nlive` and confirm ln Z stabilises.
- **A mode you know exists is missing** — priors may exclude it, or live points are
  too sparse to seed it; check `model.random_instance()` draws bracket the mode.
- **Runtime exploding** — nested sampling pays per likelihood call; profile the call
  and consider whether a chained approach (cheap global pass → refined local pass,
  [[initialization_and_chaining]]) answers the question at lower cost.

## When *not* nested sampling

A unimodal posterior for a committed model, with an expensive likelihood, is often
better served by MCMC seeded from a quick MLE run — you give up the evidence you
weren't going to use. See [[mcmc_and_hmc]].

## See also

- [[evidence_and_model_comparison]] — what the evidence buys and its prior
  sensitivity.
- [[non_linear_search]] — the full roster; `autofit_workspace:scripts/searches/nest.py`
  for runnable examples.
