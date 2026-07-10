---
title: Bayesian inference
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/
      - autofit/mapper/
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: abc98d1818b521cba5170dea8e907d4432e236c917537aee4e1cd85e6fa7601d
---

# Bayesian inference

## TL;DR

PyAutoFit is a Bayesian framework: every fit returns a **posterior** over a parametric
model — the update of your **priors** by the **likelihood** of the data — and model
comparison uses the **marginal likelihood (Bayesian evidence)**, which nested samplers
compute as a by-product. Everything else in this wiki (priors, searches, evidence,
graphical models) is a working part of this one equation:

    p(θ | d, M) = p(d | θ, M) p(θ | M) / p(d | M)
      posterior      likelihood    prior      evidence

## The four objects, mapped to the API

| Statistics | PyAutoFit object | Where |
|---|---|---|
| Model parameters θ and priors p(θ) | `af.Model` / `af.Collection` with `af.*Prior` | `PyAutoFit:autofit/mapper/` |
| Likelihood p(d\|θ) | your `Analysis.log_likelihood_function` | `PyAutoFit:autofit/non_linear/analysis/` |
| Posterior samples | `result.samples` | `PyAutoFit:autofit/non_linear/samples/` |
| Evidence p(d\|M) | `samples.log_evidence` (nested samplers) | same |

The division of responsibility is deliberate: **you own the likelihood** (it encodes
your data model, noise properties and physics); PyAutoFit owns everything either side
of it.

## Choosing an inference route

- **Posterior + evidence** → nested sampling ([[nested_sampling]]) — the default for
  model comparison and multi-modal problems.
- **Posterior only, unimodal, cheap gradients** → MCMC/HMC ([[mcmc_and_hmc]]).
- **A quick point estimate** → MLE optimizers ([[mle_and_optimizers]]) — never the
  final answer of a Bayesian analysis, always a useful reconnaissance.
- **Many datasets sharing structure** → factor graphs and expectation propagation
  ([[graphical_models_and_ep]]) fit each dataset at low dimension instead of sampling
  one enormous joint space.

## The parts users most often get wrong

1. **Priors are model choices.** A log-uniform prior on a positive quantity says "the
   order of magnitude is unknown"; a uniform prior on the same quantity concentrates
   prior mass at the top of the range. Evidence values are *only* comparable between
   models whose priors were chosen deliberately ([[evidence_and_model_comparison]]).
2. **The likelihood must be a proper log density** for the evidence to mean anything —
   dropping "constant" noise-normalisation terms changes ln Z even though it leaves
   the posterior untouched.
3. **Convergence is a diagnosis, not a default.** Each sampler family has its own
   failure signature — see the family pages.

## See also

- [[model_composition_and_priors]] · [[non_linear_search]] ·
  [[samples_and_posteriors]] · [[evidence_and_model_comparison]]
