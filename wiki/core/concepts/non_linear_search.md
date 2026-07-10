---
title: Non-linear searches
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/search/
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: b6e938919e7b4ce44ca05f18908290d0653ca37a296a579fdd109b07dc446ed7
---

# Non-linear searches

## TL;DR

A non-linear search is the algorithm that explores the model's parameter space,
calling your `log_likelihood_function` at points it chooses and assembling the result
into samples. PyAutoFit wraps three families behind one interface — **nested
sampling** (evidence + posterior), **MCMC** (posterior), **MLE** (a point) — so the
model/analysis code is identical whichever engine runs
(`PyAutoFit:autofit/non_linear/search/`).

## The installed roster

Verify against the installed stack (`dir(af)`), never from memory. At the pinned
version:

| Family | Search | One-line character |
|---|---|---|
| Nested | `af.Nautilus` | neural-network-boosted region sampler; recommended default — [[nested_sampling]] |
| Nested | `af.DynestyStatic` / `af.DynestyDynamic` | the long-standing pure-Python nested samplers |
| MCMC | `af.Emcee` | affine-invariant ensemble; dependable default MCMC — [[mcmc_and_hmc]] |
| MCMC | `af.Zeus` | ensemble slice sampling; often mixes faster on correlated posteriors |
| MCMC | `af.BlackJAXNUTS` | gradient-based NUTS; needs a JAX-differentiable likelihood |
| MLE | `af.LBFGS` | quasi-Newton maximum-likelihood — [[mle_and_optimizers]] |
| MLE | `af.Drawer` | draws from the priors; a sanity-check baseline |

## Choosing

Ask two questions:

1. **Is the evidence needed** — now or plausibly later, for model comparison? If yes,
   nested sampling; retrofitting evidence onto MCMC output is brittle.
2. **What does one likelihood evaluation cost, in how many dimensions?** Nested
   samplers are robust and multi-modal-safe but evaluation-hungry; up to ~30
   dimensions they are the safe default. MCMC needs initialization care but scales
   further; NUTS is extremely efficient per effective sample *if* gradients exist.

The chaining pattern resolves most tensions: a global provider finds the modes, a
local consumer refines — [[initialization_and_chaining]].

## The shared interface

Every search takes `name` / `path_prefix` / `unique_tag` (output identity — a
completed search **reloads instead of re-running**), `number_of_cores`
(parallelisation), and an `initializer` where the family supports it. Per-sampler
defaults live in `config/non_linear/*.yaml`, so a project can retune once rather than
in every script. Execution: `search.fit(model=model, analysis=analysis)` → `Result`
(`PyAutoFit:autofit/non_linear/search/abstract_search.py`).

## See also

- Family pages: [[nested_sampling]] · [[mcmc_and_hmc]] · [[mle_and_optimizers]]
- [[initialization_and_chaining]] · [[samples_and_posteriors]]
- Skills: `af_configure_search`, `af_run_search`.
