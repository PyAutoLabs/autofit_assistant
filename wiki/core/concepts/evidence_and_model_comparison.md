---
title: Evidence and model comparison
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/samples/
    pinned_commit: 31537d5f5ae865aca69d10e6901741533116ed65
last_updated: 2026-07-10
content_sha256: db249673c7745d4892ba1cc369ae9e6ddfd2286445c3ffe66a98de5c2f2682bb
---

# Evidence and model comparison

## TL;DR

The Bayesian evidence Z = p(d | M) is the probability of the data under a model,
marginalised over **all** its parameters weighted by their priors. Ratios of
evidences (Bayes factors) compare models with built-in Occam's razor: extra
parameters must earn their keep by improving the fit more than they dilute the prior.
Nested samplers return `samples.log_evidence` as a by-product
(`PyAutoFit:autofit/non_linear/samples/`).

## Using it

```python
ln_B = samples_complex.log_evidence - samples_simple.log_evidence
```

Same data, both fits converged, priors chosen deliberately — then a common reading
(Jeffreys-style):

| ln B | Reading |
|---|---|
| < 1 | not worth mentioning |
| 1 – 2.5 | weak preference |
| 2.5 – 5 | moderate |
| > 5 | strong |

Treat these as conventions, not laws; report ln B itself, and its stability across
reruns / live-point settings.

## The three ways evidence comparisons go wrong

1. **Prior sensitivity.** Widening a prior on a parameter only one model has *lowers*
   that model's evidence — legitimately (Occam), but it means a Bayes factor is a
   statement about model+prior pairs. Never tune priors after looking at ln B.
2. **Improper likelihoods.** Dropping "constant" terms (noise normalisation) from
   `log_likelihood_function` leaves posteriors intact but shifts ln Z; if the dropped
   term differs between models (e.g. different noise treatments), the comparison is
   corrupted.
3. **Unconverged evidence.** ln Z error bars shrink with live points; if ln B is of
   the same order as the sampler's evidence uncertainty, the comparison says nothing.
   Re-run with more live points before drawing conclusions.

## Alternatives and complements

- **Likelihood-ratio thinking** (Δ max-ln-L with parameter counting) is a quick sanity
  cross-check, not a substitute — it ignores the prior volume that is the whole point.
- For **nested model pairs** where the simpler model is a point in the complex one's
  space, the Savage–Dickey density ratio can estimate ln B from one posterior — useful
  when a second full run is unaffordable.

## See also

- [[nested_sampling]] — where the number comes from ·
  [[model_composition_and_priors]] — why the priors are half the comparison.
