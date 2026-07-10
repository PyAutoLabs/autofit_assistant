---
name: af_debug_fit_failure
description: Triage a misbehaving fit — garbage posteriors, stuck samplers, NaN likelihoods, truth not recovered, walls of sampler warnings. A strict-order diagnostic flowchart: likelihood sanity first, then prior coverage, then data pathology, then sampler diagnostics — because each later stage is meaningless if an earlier one is broken. Use when the user says "the fit isn't working", "the posterior looks wrong", "the sampler is stuck", or a simulation recovery failed. Not for slow-but-correct fits (that is a chaining/budget conversation, af_chain_searches / af_configure_search).
user-invocable: true
---

# Debugging a failing fit

Fit failures are diagnosed in strict order: **likelihood → priors → data → sampler**.
The order matters because every stage assumes the ones before it — retuning a sampler
on top of a sign-flipped likelihood just converges to the wrong answer faster. Resist
the reflex to swap samplers first; it's stage 4 for a reason.

## Orient

Get the failure's shape before touching anything (one question each):

- *Instant garbage* (finishes fast, posterior absurd) → almost always stage 1.
- *Stuck / crawling* (log-likelihood plateaus at a bad value) → stages 2–3.
- *Crashes / NaN warnings* → stage 3 (data) or stage 1 (likelihood domain errors).
- *Simulation truth not recovered* → the best failure to have; run all four stages
  with the truth in hand (`af_simulate_dataset`).

## Stage 1 — likelihood sanity

The wrapper validation trio from `af_wrap_likelihood`, run *again*, now with
suspicion:

```python
"""
__Likelihood Sanity__

A known-good instance must score a finite float, match the user's function called
directly, and beat a known-bad instance. A bad instance scoring HIGHER is the classic
sign flip (chi-squared returned where a log likelihood is expected) — the sampler then
dutifully maximises misfit.
"""
good = MyModel(centre=50.0, amplitude=25.0, width=10.0)
bad = MyModel(centre=-1e3, amplitude=1e-6, width=0.1)
ll_good = analysis.log_likelihood_function(good)
ll_bad = analysis.log_likelihood_function(bad)
assert np.isfinite(ll_good) and ll_bad < ll_good
```

Also at this stage: parameter-order bugs (vector-convention wrappers scoring
`[a, b, c]` as `[b, a, c]` — check by perturbing one parameter and watching the
response), and unit mismatches between instance attributes and what the function
expects.

## Stage 2 — prior coverage

```python
"""
__Prior Coverage__

Draws from the priors must bracket every plausible solution. A truth (or expected
value) outside the drawn range cannot be found by any sampler — that is a prior bug,
not a sampler bug.
"""
for _ in range(5):
    print(vars(model.random_instance()))
print(model.info)
```

Red flags: a fitted parameter hugging a prior limit (widen it, or justify the bound);
`LogUniformPrior` limits crossing zero; a linked/fixed parameter you forgot is no
longer free (`model.prior_count` says).

## Stage 3 — data pathology

The constitution's inspection gate, re-run with hindsight: plot the data *with the
current best model over it* (`af_plot_fit`). NaN/inf in data or noise-map, zero or
negative noise values, outliers the noise model doesn't cover, masked regions leaking
into the likelihood. Fix the **producer** of bad values — a crash you can see beats a
silent guard that biases every fit after it (never add clipping inside the
likelihood; that is the user's science to change or not).

## Stage 4 — sampler diagnostics

Only now, with 1–3 clean, per family
([[../wiki/core/concepts/non_linear_search]] and the family pages):

- **Nested**: evidence wandering between reruns or a known mode missing → raise
  `n_live`/`nlive`; check `log_likelihood_vs_iteration` for a plateau that never
  turns over (budget too small).
- **Ensemble MCMC**: auto-correlation time ~ chain length → not converged (longer
  chains, better start); walkers in disjoint clumps → multi-modal posterior, wrong
  tool — use nested sampling.
- **NUTS**: divergences / all-warmup → bad start or non-smooth likelihood; seed from
  a provider ([[../wiki/core/concepts/initialization_and_chaining]]).
- Cross-check with `af.Drawer`: if the "fit" barely beats prior draws, the data are
  uninformative for this model — a science conclusion, not a bug.

## The decisive instrument

When stages disagree, simulate: generate data from the current model at plausible
parameters (`af_simulate_dataset`) and run the identical pipeline. Recovery works →
the pipeline is fine and the real data/model mismatch is the finding. Recovery fails
→ you've reproduced the bug with a known answer, and stages 1–4 will now pin it.

## Combine

- Fixes route back to their owners: priors → `af_compose_model`; wrapper →
  `af_wrap_likelihood`; budget/chaining → `af_configure_search` /
  `af_chain_searches`.
- Journal the diagnosis (`wiki/project/`, default-yes): symptom, stage, root cause —
  the next failure in this project will look the same.

## Further reading

- **Student / new to inference** — HowToFit's fitting chapters (what healthy
  convergence looks like).
- **Experienced PyAutoFit user** — `autofit_workspace:scripts/cookbooks/analysis.py`
  (the likelihood contract being checked in stage 1).
