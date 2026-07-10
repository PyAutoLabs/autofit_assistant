---
title: MCMC and Hamiltonian Monte Carlo
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/search/mcmc/
      - autofit/non_linear/initializer.py
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: 35ff70e66527c76cac69e33dae8cc33348818528e42c3767a19e35988dadf7f0
---

# MCMC and Hamiltonian Monte Carlo

## TL;DR

MCMC samplers random-walk through parameter space so that, after convergence, the
chain's samples *are* posterior draws. They are **posterior-only** (no evidence) and
**local** (they refine from where they start), which makes them efficient for
committed, unimodal problems and hazardous as cold-start mode finders
(`PyAutoFit:autofit/non_linear/search/mcmc/`).

## The shipped samplers

### `af.Emcee` — dependable ensemble default

Affine-invariant ensemble: many walkers propose moves from each other's positions,
self-tuning to the posterior's linear correlations. Knobs: `nwalkers`, `nsteps`;
convergence is judged by auto-correlation analysis (`af.AutoCorrelationsSettings`).

### `af.Zeus` — ensemble slice sampling

Same ensemble ergonomics; slice moves often mix faster on strongly correlated
posteriors at a higher per-step cost.

### `af.BlackJAXNUTS` — gradient-based NUTS

The No-U-Turn Sampler over a **JAX-differentiable** likelihood: per-effective-sample
cost far below ensemble methods once its warmup has adapted step size and mass matrix.
Two hard requirements: the likelihood must be differentiable end-to-end, and the chain
must start in a region of reasonable density — a cold start in the tails wastes the
whole adaptation window or diverges.

## Initialization — the family's defining care

Where walkers/chains start is controlled by the `initializer` argument
(`PyAutoFit:autofit/non_linear/initializer.py`): `InitializerPrior` (cold — draws from
the priors), `InitializerBall` (a tight ball around a point — powerful with a good
estimate, biased with a bad one), `InitializerParamBounds`. The robust production
pattern is a chain: a global provider (nested sampling, or a quick MLE) finds the
mode; MCMC refines it — [[initialization_and_chaining]].

## Failure signatures

- **Auto-correlation times comparable to chain length** — the chain hasn't converged;
  more steps, better initialization, or a different sampler.
- **Walkers stuck in disjoint clumps** — a multi-modal posterior; ensemble MCMC will
  not equilibrate between well-separated modes. Use nested sampling.
- **NUTS divergences / all-warmup runs** — bad start or non-smooth likelihood; seed
  from a posterior/MLE and check differentiability.

## See also

- [[nested_sampling]] for when the evidence or multi-modality matters;
  `autofit_workspace:scripts/searches/mcmc.py` for runnable examples.
