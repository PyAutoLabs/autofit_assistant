"""
Start Here Step 2: Define the Likelihood
========================================

The second step of the "start here" tour. A model on its own says nothing about data; the
likelihood is what turns a set of parameter values into a number saying how well they describe
the measurements. This script loads the bundled 1D Gaussian dataset, pairs it with the
`Analysis` in `analysis.py`, evaluates the log likelihood at a single random draw from the
priors composed in step 1, and saves an image comparing that random model with the data.

A random draw is deliberately a bad fit. Seeing a bad fit score badly is how you check the
likelihood is wired up at all — which is exactly the validation `af_wrap_likelihood` performs
before any search is launched on a user's own code.

__Contents__

- **Imports:** autofit, the tour's model and likelihood, and the plotting helpers.
- **Dataset:** Load the data and the noise map.
- **Analysis:** Pair the likelihood with the dataset.
- **Random Instance:** Draw one model from the priors and score it.
- **Figure:** Model versus data, with normalised residuals.
"""

import pathlib

import matplotlib.pyplot as plt
import numpy as np

import autofit as af

from analysis import Analysis
from gaussian import Gaussian

"""
__Dataset__

The dataset is 100 pixels of a noisy 1D Gaussian, stored as JSON and loaded with PyAutoFit's
array helper (`PyAutoFit:autofit/tools/util.py`). The noise map holds the per-pixel standard
deviation of the measurement errors — a constant 2.0 here — and is what makes the likelihood a
statement about probability rather than a bare sum of squares.
"""

dataset_path = pathlib.Path("dataset") / "gaussian_x1"

data = af.util.numpy_array_from_json(file_path=dataset_path / "data.json")
noise_map = af.util.numpy_array_from_json(file_path=dataset_path / "noise_map.json")

xvalues = np.arange(data.shape[0])

print(f"Dataset: {data.shape[0]} pixels, noise sigma = {noise_map[0]}")

"""
__Analysis__

The Analysis holds the data and implements `log_likelihood_function`. Its likelihood assumes
independent Gaussian errors, so it is a chi-squared sum — see `analysis.py` for the expression
and the constant it drops. Nothing about the search or the model is baked in here: the same
Analysis scores the one-Gaussian model of step 4 and the three-Gaussian model of step 6.
"""

analysis = Analysis(data=data, noise_map=noise_map)

"""
__Random Instance__

`model.random_instance()` draws each parameter from its prior and returns a real instance of the
`Gaussian` class, so the user's own methods work on it directly
(`PyAutoFit:autofit/mapper/prior_model/abstract.py`). The seed makes the draw reproducible; drop
it and every run gives a different bad fit.
"""

np.random.seed(1)

model = af.Model(
    Gaussian,
    centre=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
    normalization=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
    sigma=af.UniformPrior(lower_limit=0.1, upper_limit=30.0),
)

instance = model.random_instance()

print(
    f"Random draw from the priors: centre={instance.centre:.2f}, "
    f"normalization={instance.normalization:.2f}, sigma={instance.sigma:.2f}"
)

log_likelihood = analysis.log_likelihood_function(instance=instance)

print(f"log likelihood at that draw: {log_likelihood:.2f}")

"""
The truth used to simulate the data is recorded in `dataset/gaussian_x1/README.md`. Scoring it
too shows the scale: a good model beats a random one by hundreds of log-likelihood units, which
is the gradient the non-linear search of step 3 climbs.
"""

truth = Gaussian(centre=50.0, normalization=25.0, sigma=10.0)

print(
    f"log likelihood at the simulation truth: "
    f"{analysis.log_likelihood_function(instance=truth):.2f}"
)

"""
__Figure__

Model versus data with normalised residuals underneath: the plot that says whether the model
describes the measurements, as opposed to the posterior plots of step 4 which say what the
inference concluded. Throwaway figures go to the gitignored `scripts/scratch/` and their
absolute path is printed, per `skills/_style.md` "Plot output and path announcement".
"""

model_data = analysis.model_data_from(instance=instance)

fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(7, 5), sharex=True, height_ratios=[3, 1])
ax0.errorbar(xvalues, data, yerr=noise_map, fmt=".k", ms=4, elinewidth=0.7, label="data")
ax0.plot(xvalues, model_data, "r-", lw=1.5, label="random model")
ax0.set_ylabel("profile normalization")
ax0.set_title(f"A random draw from the priors (log likelihood = {log_likelihood:.1f})")
ax0.legend()

ax1.plot(xvalues, (data - model_data) / noise_map, ".k", ms=4)
ax1.axhline(0.0, color="r", lw=0.8)
ax1.set_ylabel("residual / sigma")
ax1.set_xlabel("x")

plot_path = pathlib.Path("scripts") / "scratch" / "start_here"
plot_path.mkdir(parents=True, exist_ok=True)

fig.savefig(plot_path / "step_2_random_model.png", dpi=140, bbox_inches="tight")
plt.close(fig)

print(f"Saved to: {(plot_path / 'step_2_random_model.png').resolve()}")
