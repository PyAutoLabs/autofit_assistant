---
name: af_simulate_dataset
description: Simulate a dataset from a composed model — draw or fix "true" parameters, generate noiseless model data, add noise, and save it alongside a truth record, so fits can be validated against a known answer before touching real data. Use when the user says "simulate data", "make a test dataset", "check the pipeline recovers known inputs", or before a first fit on an expensive real dataset. Not for preparing real data (that is the data-inspection conversation in af_run_search).
user-invocable: true
---

# Simulating a dataset

A simulation is the only fit where you know the answer. Every new pipeline earns its
first real-data run by first recovering known inputs: it validates the likelihood, the
priors, the sampler budget, and your read of the posterior, all at once. The bundled
`dataset/gaussian_x1/` was made exactly this way — its README records the truth.

## Orient

The recipe is three lines of physics and one of bookkeeping: instantiate your model
class with chosen "true" values, evaluate its model data, add noise drawn from the
noise model you claim in the likelihood, save data + noise-map + truth. The workspace's
generators are the canonical reference
(`autofit_workspace:scripts/simulators/simulators.py`).

## Ask

- Simulate with *hand-picked* truth (a clean pedagogical recovery) or truth *drawn
  from the priors* (a stress test of the whole prior volume)?
- What noise model does the likelihood assume? The simulation must add **that** noise
  — simulating Gaussian noise then fitting a Poisson likelihood "validates" nothing.

## Branch — the simulation script

```python
"""
Simulate: Gaussian 1D
=====================

Generate noisy 1D data from a Gaussian with recorded truth, for validating the fit
pipeline before real data.

__Contents__

- **Truth:** The chosen true parameters (recorded, always).
- **Model data:** Noiseless evaluation of the model.
- **Noise:** Gaussian noise matching the likelihood's assumption.
- **Output:** data + noise-map + truth record.
"""
import numpy as np
import autofit as af

"""
__Truth__

Hand-picked here; `model.random_instance()` draws truth from the priors instead when
stress-testing. Either way the values are written down — an unrecorded simulation
truth is a lost validation (`autofit_workspace:scripts/simulators/simulators.py`).
"""
rng = np.random.default_rng(1)
truth = Gaussian(centre=50.0, normalization=25.0, sigma=10.0)

"""
__Model data + Noise__

The noise added is exactly what the likelihood assumes (independent Gaussian with this
noise-map); the noise-map is saved with the data because the fit needs the same one.
"""
xvalues = np.arange(100)
model_data = truth.model_data_from(xvalues=xvalues)
noise_map = np.full(xvalues.shape, 2.0)
data = model_data + rng.normal(0.0, noise_map)

"""
__Output__

JSON via af.util keeps the round-trip trivial (`af.util.numpy_array_from_json` on the
fitting side). The truth goes in a README/info file next to the data — never only in
the script.
"""
af.util.numpy_array_to_json(data, file_path="dataset/my_sim/data.json", overwrite=True)
af.util.numpy_array_to_json(noise_map, file_path="dataset/my_sim/noise_map.json", overwrite=True)
```

For teaching sessions, `af.ex.Gaussian` / `af.ex.Exponential` are ready-made model
classes with `model_data_from` — the workspace simulators compose multi-component
datasets from exactly these.

## The recovery check (the point of it all)

Fit the simulation with the *production* setup (`af_run_search`) and require:

1. Truth inside the quoted intervals at the expected sigma (most parameters within
   1σ; systematic misses mean bias, not bad luck).
2. Posterior widths plausible for the noise level.
3. (If evidence matters) ln Z stable across live-point settings.

A recovery that fails is a gift: the pipeline is broken *and you know it* before the
real data ever saw it. Record the recovery table in `wiki/project/`.

## Combine

- Seed and validate priors with `af_compose_model`; wrap real likelihoods with
  `af_wrap_likelihood` and validate the wrapper on simulated data first.
- Failed recoveries route to `af_debug_fit_failure` with the enormous advantage of a
  known answer.

## Further reading

- **General reference** — [RTD: the basics](https://pyautofit.readthedocs.io/en/latest/overview/the_basics.html) (simulate → fit → recover).
- **Experienced PyAutoFit user** — `autofit_workspace:scripts/simulators/simulators.py`.
