---
title: Samples and posteriors
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/samples/
      - autofit/aggregator/
    pinned_commit: 31537d5f5ae865aca69d10e6901741533116ed65
last_updated: 2026-07-10
content_sha256: a33d80418aaa6d7218f6d9fb105f90b3aadf724c11779935f80de2fa3f18847d
---

# Samples and posteriors

## TL;DR

Every search returns a `Result` whose `samples` object holds the accepted points —
parameters, log likelihood, log prior, log posterior, weights — plus summary methods
that turn them into science: median-PDF instances, errors at any sigma, the
max-likelihood model, and (for nested samplers) the evidence
(`PyAutoFit:autofit/non_linear/samples/`).

## The calls that matter

```python
samples = result.samples

samples.median_pdf()                    # median-PDF instance of your classes
samples.max_log_likelihood()            # max-likelihood instance
samples.errors_at_upper_sigma(sigma=1.0)
samples.errors_at_lower_sigma(sigma=1.0)
samples.values_at_upper_sigma(sigma=3.0)
samples.log_evidence                    # nested samplers only
samples.parameter_lists                 # raw arrays for custom analysis
samples.weight_list
```

Summary instances are **real instances of your model classes** — your own methods run
on them unchanged. That is how uncertainty propagates into derived quantities: map a
method over posterior draws, take percentiles of the outputs. `samples.with_paths()` /
`without_paths()` slice a parameter subset; CSV export serves spreadsheet-bound
collaborators; `af.marginalize` handles marginalisation over nuisance dimensions.

Fast summaries: common quantities are also stored in a `samples_summary` on disk —
loading it avoids re-computing from the full sample list and is much faster for bulk
work.

## Visualisation

`autofit.plot` (imported as `aplt`) provides search-level visualisation:
`corner_cornerpy` (corner plot), `log_likelihood_vs_iteration`, `subplot_parameters`,
plus per-sampler plotters. For domain plots, plain matplotlib over instances/draws is
the norm — this stack does not impose a plotting framework on your data.

## Many fits: the aggregator

```python
from autofit.aggregator.aggregator import Aggregator

agg = Aggregator.from_directory(directory="output/my_project")
for samples in agg.values("samples"):
    ...
```

The directory aggregator lazily walks an `output/` tree (generators — memory-safe for
large sweeps). The top-level `af.Aggregator` is the *database* variant
(`from_database("db.sqlite")`) adding queryable sqlite-backed loading. Never
hand-compose output paths — reload via the aggregator, or re-run the script (a
completed search reloads rather than re-running).

## See also

- [[evidence_and_model_comparison]] · [[bayesian_inference]] · the `af_load_results`
  skill for the guided procedure;
  `autofit_workspace:scripts/cookbooks/samples.py` and `result.py`.
