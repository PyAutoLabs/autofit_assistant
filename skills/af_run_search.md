---
name: af_run_search
description: Execute a PyAutoFit model-fit — bring together the composed model, the Analysis (likelihood) and the configured search, run `search.fit(...)`, monitor progress, and do the first inspection of the returned Result. Use when the user says "run the fit", "fit my data", or has a model+analysis ready to execute. Not for choosing the sampler (that is `af_configure_search`) or deep posterior analysis (that is `af_load_results`).
user-invocable: true
---

# Running the fit

This is where the three ingredients meet: the **model** (what is free, with what
priors), the **analysis** (how a parameter instance is scored against the data), and
the **search** (how the space is explored). One call runs the inference; everything
the fit learns is written to `output/` for inspection now and reloading later.

Before running on **real data**, the constitution's data-inspection gate applies
(`AGENTS.md`): plot or summarise the dataset, show the user, and ask once about
artefacts/outliers/selection effects. Simulated data is exempt.

## Orient

`search.fit(model=model, analysis=analysis)` blocks until the sampler terminates and
returns a `Result` (`PyAutoFit:autofit/non_linear/search/abstract_search.py`). Runtime
is (cost of one likelihood call) × (evaluations the sampler needs) — estimate both for
the user *before* launching anything that might run for hours; if it will, offer the
HPC route instead of letting a laptop cook overnight.

## Ask

- Is this a first exploratory fit (favour speed: fewer live points / steps) or the
  production run (favour accuracy)?
- Roughly how long does one likelihood evaluation take? (Time it if unknown —
  `%timeit`-style, three calls, before committing to a sampler budget.)

## Branch — the fit script

```python
"""
Fit: Gaussian 1D
================

Fit the 1D Gaussian model to the dataset with a nested sampler, returning the
posterior and the Bayesian evidence.

__Contents__

- **Imports:** autofit and the model/analysis defined earlier.
- **Fit:** Run the non-linear search.
- **Result:** First inspection of what came back.
"""
import autofit as af

"""
__Fit__

The search writes live output under `output/<path_prefix>/<name>/` — samples,
`model.info`, and visualization — so progress is inspectable mid-run
(`PyAutoFit:autofit/non_linear/search/abstract_search.py`).
"""
search = af.Nautilus(path_prefix="my_project", name="gaussian_fit", n_live=200)

result = search.fit(model=model, analysis=analysis)

"""
__Result__

`result.info` is the human summary; the maximum-likelihood instance is a plain
instance of the model's classes, so the user's own methods work on it directly.
"""
print(result.info)

best = result.max_log_likelihood_instance
print("max-likelihood centre:", best.centre)
```

## Monitoring a running fit

- The output folder updates live: `output/<path_prefix>/<name>/` gains a
  `model.info`, sampler-specific progress files, and (for samplers that support it)
  intermediate visualization. Quote the absolute path so the user can watch.
- A **completed** search re-loads instead of re-running when the script is executed
  again with the same `path_prefix`/`name`/`unique_tag` — say this out loud the first
  time; it surprises everyone once.
- For smoke-testing a script's plumbing without a real run:
  `PYAUTO_TEST_MODE=1 python scripts/fit.py` (fast, non-converging — never for real
  inference).

## When the fit misbehaves

Quick triage before reaching for a different sampler (a dedicated
`af_debug_fit_failure` skill is planned):

- **Instant garbage posterior** — almost always the likelihood: check
  `analysis.log_likelihood_function` on a hand-built instance returns a finite float.
- **Sampler stalls at low likelihood** — priors may exclude the true solution;
  `model.random_instance()` draws should bracket plausible values.
- **NaN/inf likelihoods** — clip or reject in the *data preparation*, don't silently
  guard inside the likelihood; a crash you can see beats a bias you can't.

## Combine

- Full posterior work — medians, errors, evidence, database queries — is
  [`af_load_results`](./af_load_results.md).
- If this fit seeds a harder one (better priors, more complex model), chain searches
  via start points / prior passing (`autofit_workspace:scripts/searches/start_point.py`;
  a dedicated `af_chain_searches` skill is planned).
- Offer (default-yes) a `wiki/project/` entry: dataset, model, search settings, output
  path, and the headline numbers.

## Further reading

- **Student / new to inference** — HowToFit chapter 2: running your first fit.
- **General reference** — [RTD: the basics overview](https://pyautofit.readthedocs.io/en/latest/overview/the_basics.html).
- **Experienced PyAutoFit user** — `autofit_workspace:scripts/overview/overview_1_the_basics.py`.
