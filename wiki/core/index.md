# PyAutoFit Core Wiki — Index

Top-level navigation for the curated PyAutoFit + statistics reference.

> 🚧 **Scaffold.** The pages below are the planned Phase 2 set
> ([autofit_assistant#1](https://github.com/PyAutoLabs/autofit_assistant/issues/1));
> unlinked entries do not exist yet. An agent must not cite a page that is not present —
> read the installed source instead.

## The stack

- `stack/overview.md` — how `autoconf` and `autofit` fit together.
- `stack/autoconf.md` — configuration and prior resolution.
- `stack/autofit.md` — the inference engine.

## Concepts (statistics the assistant uses on your behalf)

- `concepts/bayesian_inference.md` — likelihood, priors, posterior, evidence.
- `concepts/model_composition_and_priors.md` — `af.Model` / `af.Collection`, prior
  types and pitfalls.
- `concepts/non_linear_search.md` — the search landscape and how to choose.
- `concepts/nested_sampling.md` — evidence-first samplers.
- `concepts/mcmc_and_hmc.md` — posterior-first samplers.
- `concepts/initialization_and_chaining.md` — starting points and search chaining.
- `concepts/graphical_models_and_ep.md` — factor graphs and expectation propagation.
- `concepts/evidence_and_model_comparison.md` — Bayes factors in practice.
- `concepts/samples_and_posteriors.md` — result objects, aggregator, database.
- One page per shipped sampler (roster audited from the installed PyAutoFit at write
  time).

## Operations

- `operations/installation.md`
- `operations/sandbox.md`
- `operations/hpc.md`
