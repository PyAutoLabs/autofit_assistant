---
name: af_load_results
description: Load and analyse the results of completed PyAutoFit fits — the Result object's posterior samples (medians, errors at sigma, instances), the Bayesian evidence, marginalisation, CSV export, and bulk loading of many fits via the aggregator/database. Use when the user says "load my results", "what did the fit find", "get the posterior/errors/evidence", or wants to compare or tabulate many completed fits. Not for running fits (that is `af_run_search`).
user-invocable: true
---

# Loading and analysing results

A completed fit is only the start of the science: the questions that matter — what are
the parameter constraints, how do models compare, what should the paper's table say —
are all answered from the `Samples` object, either straight off the returned `Result`
or reloaded later from `output/`.

## Orient

Every search writes its full state to `output/<path_prefix>/<name>/…`; the `Result`
returned by `search.fit` wraps the same information
(`PyAutoFit:autofit/non_linear/samples/`). For one fit, work with `result.samples`;
for many fits (parameter sweeps, dataset samples), the aggregator loads them in bulk.

## Ask

- One fit or many? (Many → aggregator branch.)
- What does the user actually need: headline constraints, a publication table, an
  evidence comparison, or draws for propagating uncertainty into a derived quantity?

## Branch — one fit's posterior

```python
"""
__Samples__

`samples` holds every accepted point (parameters, log likelihood, prior, posterior,
weight). The summary calls below are what a paper's constraints table is made of
(`PyAutoFit:autofit/non_linear/samples/`).
"""
samples = result.samples

instance = samples.median_pdf()                    # median-PDF model instance
upper = samples.values_at_upper_sigma(sigma=3.0)   # +3σ bounds per parameter
lower = samples.values_at_lower_sigma(sigma=3.0)   # -3σ bounds
errors_hi = samples.errors_at_upper_sigma(sigma=1.0)
errors_lo = samples.errors_at_lower_sigma(sigma=1.0)

best = samples.max_log_likelihood()                # max-likelihood instance
print("median centre:", instance.centre)
```

Instances are real instances of the user's classes — their own methods work on them,
which is how posterior uncertainty propagates into any derived quantity: map a method
over draws, take percentiles of the output.

```python
"""
__Evidence__

Nested samplers report the Bayesian evidence — the model-comparison currency. Compare
ln-evidence differences between fits of competing models on the SAME data; ~ln B > 5
is strong preference by the usual Jeffreys-style reading.
"""
print("ln evidence:", samples.log_evidence)
```

Also useful: `samples.parameter_lists`, `samples.log_likelihood_list`,
`samples.weight_list` (raw arrays for custom plots — corner plots via
`autofit.plot`'s `corner_cornerpy`), `samples.with_paths([...])` to slice a subset of
parameters, and CSV export for spreadsheet-bound collaborators.

## Branch — many fits: the aggregator

```python
"""
__Aggregator__

The directory aggregator walks an output/ tree and lazily loads every fit it finds
(as memory-efficient generators) — the tool for sweeps over datasets or models
(`PyAutoFit:autofit/aggregator/aggregator.py`).
"""
from autofit.aggregator.aggregator import Aggregator

agg = Aggregator.from_directory(directory="output/my_project")

for samples in agg.values("samples"):
    print(samples.log_evidence, samples.median_pdf().centre)
```

Note the import: the directory walker is `autofit.aggregator.aggregator.Aggregator`;
the top-level `af.Aggregator` is the *database* variant
(`af.Aggregator.from_database("database.sqlite")`), which adds queryable sqlite-backed
loading for large result sets. Filter by search name / unique tag to slice a sweep;
combine with the evidence values to build a model-comparison table across a whole
sample in a few lines.

## Sanity rules

- **Never hand-compose output paths** — reload via the aggregator or by re-running the
  script (a completed search reloads, it does not re-run). Manual path composition
  breaks the moment `unique_tag` or test-mode namespacing is involved.
- Quote `result.info` / `samples.summary` output to the user rather than re-deriving
  numbers by hand.

## Combine

- An evidence table across models is the input to a model-comparison write-up — offer
  a `wiki/project/` entry with the table and its interpretation.
- Constraints that look wrong route back to the model (`af_compose_model` — priors) or
  the fit (`af_run_search` — triage section).

## Further reading

- **Student / new to inference** — HowToFit chapter on interpreting results.
- **General reference** — [RTD: result cookbook](https://pyautofit.readthedocs.io/en/latest/cookbooks/result.html).
- **Experienced PyAutoFit user** — `autofit_workspace:scripts/cookbooks/result.py` and
  `samples.py`.
