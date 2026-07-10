---
title: Initialization and search chaining
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/initializer.py
      - autofit/non_linear/search/
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: e3ad2a95d5c9f996858f1d9d55c22407f945cc77b29f15a535d8b7c2ebb85c3f
---

# Initialization and search chaining

## TL;DR

Samplers divide into **providers** and **consumers** of starting points. Global,
gradient-free searches (nested sampling) find modes from a cold prior; local,
efficient samplers (NUTS, ensemble MCMC, LBFGS refinement) need to start *at* a mode
to be worth running. Chaining — one search's result seeding the next search's start or
priors — is how the two are combined, and it is a first-class PyAutoFit pattern.

## The provider/consumer map

| Role | Searches | Notes |
|---|---|---|
| Cold-start providers | `Nautilus`, `DynestyStatic/Dynamic` | explore the full prior; multi-modal-safe; return posterior + evidence |
| Cheap mode-finders | `LBFGS` (`Drawer` as baseline) | point estimate only; fast way into a basin |
| Warm-start consumers | `BlackJAXNUTS`, `Emcee`, `Zeus` | refine a known mode; NUTS also needs its warmup to adapt step size/mass matrix |

Consumer requirements differ in strength: a bad start costs ensemble MCMC a long
burn-in, but costs NUTS its entire adaptation window (or divergence). The natural NUTS
provider is a nested-sampling posterior — seed chains from posterior draws.

## How PyAutoFit expresses it

- **Prior passing / chained searches** — a completed `result` carries its posterior
  into a follow-up model: `result.model` gives the fitted composition, from which the
  next search's priors are derived. This is how a cheap, simplified first fit
  ("fit the amplitude with the shape fixed") hands a focused starting space to the
  expensive full fit. Runnable example:
  `autofit_workspace:scripts/searches/start_point.py`.
- **Initializer classes** — `InitializerPrior` (cold), `InitializerBall`
  (concentrated), `InitializerParamBounds`
  (`PyAutoFit:autofit/non_linear/initializer.py`) control where a search's first
  samples are drawn; the API surface a warm start plugs into.

## Design rules

1. A search that *requires* initialization must have its provider named in the
   pipeline — never assume "something reasonable" starts it.
2. Chains narrow priors; they must not **bias** them. A follow-up prior should be wide
   enough that the first fit's systematic errors don't lock in — width at the level of
   several times the first posterior's sigma, not equal to it.
3. Record every link of the chain in the project journal — a chained result is only
   reproducible if the seeding is.

## See also

- [[nested_sampling]] · [[mcmc_and_hmc]] · [[mle_and_optimizers]] — the roles being
  chained.
