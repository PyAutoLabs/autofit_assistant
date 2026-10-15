---
title: Non-linear searches
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/search/
    pinned_commit: 3f4699b959e387b2eddca4508585c7812dc557be
last_updated: 2026-10-15
content_sha256: c56214e3dcb1c67d566bcf47d2cbec8bdef83890e8b4a434f8e1cd355073263b
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

Verify against the installed stack (`dir(af)`), never from memory. The table is generated
from the installed release's search manifest (`python -m autofit search-manifest --json`;
regenerate with PyAutoHands `autohands regenerate_search_roster --root .`, never by hand) —
one row per search, with the capabilities the search declares:

<!-- search-roster:begin style=table -->
<!-- search-manifest@1 autofit 2026.10.12.1 -->
| Search | Family | Status | JAX | Gradient | Evidence | Posterior | Example |
|---|---|---|---|---|---|---|---|
| `af.Emcee` | mcmc | stable | none | none | no | chain | `autofit_workspace:scripts/searches/mcmc.py` |
| `af.Zeus` | mcmc | stable | none | none | no | chain | `autofit_workspace:scripts/searches/mcmc.py` |
| `af.BlackJAXNUTS` | mcmc | stable | required | uses | no | chain | `autofit_workspace:scripts/searches/mcmc.py` |
| `af.SMC` | mcmc | experimental | required | uses | yes | weighted | — |
| `af.DynestyStatic` | nest | stable | optional | none | yes | weighted | `autofit_workspace:scripts/searches/nest.py` |
| `af.DynestyDynamic` | nest | stable | optional | none | yes | weighted | `autofit_workspace:scripts/searches/nest.py` |
| `af.Nautilus` | nest | stable | optional | none | yes | weighted | `autofit_workspace:scripts/searches/nest.py` |
| `af.NSS` | nest | experimental | required | none | yes | weighted | — |
| `af.Drawer` | mle | stable | none | none | no | point | `autofit_workspace:scripts/searches/mle.py` |
| `af.BFGS` | mle | stable | optional | none | no | point | — |
| `af.LBFGS` | mle | stable | optional | none | no | point | `autofit_workspace:scripts/searches/mle.py` |
| `af.MultiStartAdam` | mle | stable | required | uses | no | point | `autofit_workspace:scripts/searches/mle.py` |
| `af.MultiStartADABelief` | mle | experimental | required | uses | no | point | — |
| `af.MultiStartLion` | mle | experimental | required | uses | no | point | — |
| `af.MultiStartProdigy` | mle | stable | required | uses | no | point | — |
<!-- search-roster:end -->

`JAX: required` searches need an analysis built with `use_jax=True`; `experimental` ones
are new enough that their defaults may still move. The full capability matrix is
https://pyautofit.readthedocs.io/en/latest/searches/index.html.

Character, hand-written:

- `af.Nautilus` — neural-network-boosted region sampler; recommended default — [[nested_sampling]]
- `af.DynestyStatic` / `af.DynestyDynamic` — the long-standing pure-Python nested samplers
- `af.Emcee` — affine-invariant ensemble; dependable default MCMC — [[mcmc_and_hmc]]
- `af.Zeus` — ensemble slice sampling; often mixes faster on correlated posteriors
- `af.BlackJAXNUTS` — gradient-based NUTS; needs a JAX-differentiable likelihood
- `af.LBFGS` — quasi-Newton maximum-likelihood — [[mle_and_optimizers]]
- `af.Drawer` — draws from the priors; a sanity-check baseline

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
(parallelisation), and an `initializer` where the family supports it. Each search's
defaults are the keyword defaults of its class — there are no per-search YAML files, so
a non-default setting is passed as a kwarg. Execution: `search.fit(model=model, analysis=analysis)` → `Result`
(`PyAutoFit:autofit/non_linear/search/abstract_search.py`).

## See also

- Family pages: [[nested_sampling]] · [[mcmc_and_hmc]] · [[mle_and_optimizers]]
- [[initialization_and_chaining]] · [[samples_and_posteriors]]
- Skills: `af_configure_search`, `af_run_search`.
