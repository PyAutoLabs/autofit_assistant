# PyAutoFit Core Wiki — Index

Top-level navigation for the curated PyAutoFit + statistics reference. Pages pin the
source commits they were validated against (see `README.md` "Page format"); the
committed API baseline is `api_audit_baseline.json`.

## The stack

- [stack/overview.md](./stack/overview.md) — how `autoconf` and `autofit` fit together.
- [stack/autofit.md](./stack/autofit.md) — the inference engine, sub-system by sub-system.
- [stack/autoconf.md](./stack/autoconf.md) — configuration and prior resolution.

## Concepts (the statistics the assistant uses on your behalf)

- [concepts/bayesian_inference.md](./concepts/bayesian_inference.md) — likelihood,
  priors, posterior, evidence, and how each maps to the API.
- [concepts/model_composition_and_priors.md](./concepts/model_composition_and_priors.md)
  — `af.Model`/`af.Collection`, prior types and pitfalls, fixing/linking/assertions.
- [concepts/non_linear_search.md](./concepts/non_linear_search.md) — the search
  landscape, the installed roster, and how to choose.
- [concepts/nested_sampling.md](./concepts/nested_sampling.md) — Nautilus and Dynesty;
  evidence-first sampling and its failure signatures.
- [concepts/mcmc_and_hmc.md](./concepts/mcmc_and_hmc.md) — Emcee, Zeus, BlackJAX NUTS;
  initialization care.
- [concepts/mle_and_optimizers.md](./concepts/mle_and_optimizers.md) — LBFGS and
  Drawer; reconnaissance, not results.
- [concepts/initialization_and_chaining.md](./concepts/initialization_and_chaining.md)
  — provider/consumer searches and prior passing.
- [concepts/graphical_models_and_ep.md](./concepts/graphical_models_and_ep.md) —
  factor graphs, hierarchical models, expectation propagation.
- [concepts/evidence_and_model_comparison.md](./concepts/evidence_and_model_comparison.md)
  — Bayes factors in practice and the three ways they go wrong.
- [concepts/samples_and_posteriors.md](./concepts/samples_and_posteriors.md) — the
  Samples API, visualisation, and the aggregator.

## Operations

- [operations/installation.md](./operations/installation.md)
- [operations/sandbox.md](./operations/sandbox.md)
- [operations/hpc.md](./operations/hpc.md)
