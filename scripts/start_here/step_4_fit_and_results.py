"""
Start Here Step 4: Fit the Model and Read the Result
====================================================

The fourth step of the "start here" tour, where the three ingredients meet: the model from step
1 (what is free, with what priors), the Analysis from step 2 (how a parameter set is scored) and
the search from step 3 (how the space is explored). One call runs the inference and everything
the fit learns is written to `output/` for inspection now and reloading in step 5.

The dataset's simulation truth is known — `centre=50.0`, `normalization=25.0`, `sigma=10.0` —
so the result can be judged rather than merely reported. `dataset/gaussian_x1/README.md` records
a maintainer validation run recovering 49.98 / 24.85 / 9.84.

__Contents__

- **Imports:** autofit, its plotting module, and the tour's model and likelihood.
- **Dataset:** Load the data and noise map.
- **Model, Analysis, Search:** Reassemble steps 1 to 3.
- **Fit:** Run the non-linear search.
- **Results:** Parameter estimates with 1-sigma errors, against the truth.
- **Figures:** The maximum-likelihood fit and the posterior corner plot.
"""

import pathlib

import matplotlib.pyplot as plt
import numpy as np

import autofit as af
import autofit.plot as aplt

from analysis import Analysis
from gaussian import Gaussian

"""
__Dataset__

The same 100-pixel dataset loaded in step 2. It is simulated data, so the constitution's
data-inspection gate does not apply here — on the user's own data, it does, and the data is
plotted and discussed before any search is launched (`AGENTS.md` "Safety invariants").
"""

dataset_path = pathlib.Path("dataset") / "gaussian_x1"

data = af.util.numpy_array_from_json(file_path=dataset_path / "data.json")
noise_map = af.util.numpy_array_from_json(file_path=dataset_path / "noise_map.json")

xvalues = np.arange(data.shape[0])

"""
__Model, Analysis, Search__

Steps 1 to 3 in three statements. Nothing new is introduced: this is the point at which the
tour's pieces are shown to be independent — the model could be widened, the likelihood swapped
for the user's own code, or the search exchanged for Emcee, each without touching the other two.
"""

model = af.Model(
    Gaussian,
    centre=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
    normalization=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
    sigma=af.UniformPrior(lower_limit=0.1, upper_limit=30.0),
)

analysis = Analysis(data=data, noise_map=noise_map)

search = af.DynestyStatic(
    path_prefix="start_here",
    name="gaussian_x1",
    nlive=100,
    number_of_cores=1,
)

"""
__Fit__

`search.fit` blocks until the sampler terminates and returns a `Result`
(`PyAutoFit:autofit/non_linear/search/abstract_search.py`). It writes to
`output/start_here/gaussian_x1/<unique_id>/` **as it runs**, using the best model found so far,
so the folder is worth opening the moment the fit starts rather than when it finishes:
`model.results` for the human-readable parameter summary, `model.info` for the composition that
produced it, and `image/` for the figures the Analysis's Visualizer draws
(`skills/_style.md` "Output folder announcement").

Re-running this script with the same `path_prefix`/`name` reloads the completed search instead
of repeating it.
"""

result = search.fit(model=model, analysis=analysis)

print(result.info)

"""
__Results__

`result.samples` holds every accepted sample: parameters, likelihoods, weights. The median of
the marginalised posterior and its 1-sigma errors are what a paper's constraints table is made
of (`PyAutoFit:autofit/non_linear/samples/`, and `skills/af_load_results.md`).
"""

samples = result.samples

median = samples.median_pdf()
errors_hi = samples.errors_at_upper_sigma(sigma=1.0)
errors_lo = samples.errors_at_lower_sigma(sigma=1.0)

"""
Each of these is a real instance of the `Gaussian` class with the summary values filled in, so
the parameters are reached by name — `median.sigma`, not a position in an array. That naming is
what lets a natural-language request ("how well is sigma constrained?") map onto a number
without anyone having to remember parameter ordering.
"""

truth = {"centre": 50.0, "normalization": 25.0, "sigma": 10.0}

print("\nparameter        inferred (median, 1 sigma)        truth")
print("-" * 62)

for name in ["centre", "normalization", "sigma"]:
    value = getattr(median, name)
    error_hi = getattr(errors_hi, name)
    error_lo = getattr(errors_lo, name)
    print(
        f"{name:<16} {value:>7.2f} +{error_hi:.2f} / -{error_lo:.2f}"
        f"{'':<8}{truth[name]:>6.1f}"
    )

print(f"\nlog evidence: {samples.log_evidence:.2f}")

"""
__Figures__

Two figures answering two different questions. The maximum-likelihood profile over the data with
its residuals asks *does the model describe the measurements*; the corner plot asks *what did
the inference conclude, and can it be trusted* — degeneracies, prior-edge pile-ups and
multi-modality are visible there and invisible in the table above
(`skills/af_plot_fit.md`).
"""

plot_path = pathlib.Path("scripts") / "scratch" / "start_here"
plot_path.mkdir(parents=True, exist_ok=True)

best = samples.max_log_likelihood()
model_data = analysis.model_data_from(instance=best)

fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(7, 5), sharex=True, height_ratios=[3, 1])
ax0.errorbar(xvalues, data, yerr=noise_map, fmt=".k", ms=4, elinewidth=0.7, label="data")
ax0.plot(xvalues, model_data, "r-", lw=1.5, label="maximum likelihood model")
ax0.set_ylabel("profile normalization")
ax0.set_title("Maximum likelihood Gaussian over the data")
ax0.legend()

ax1.plot(xvalues, (data - model_data) / noise_map, ".k", ms=4)
ax1.axhline(0.0, color="r", lw=0.8)
ax1.set_ylabel("residual / sigma")
ax1.set_xlabel("x")

fig.savefig(plot_path / "step_4_max_likelihood_fit.png", dpi=140, bbox_inches="tight")
plt.close(fig)

aplt.corner_cornerpy(
    samples=samples, path=plot_path, filename="step_4_corner", format="png"
)

print(f"\nSaved to: {(plot_path / 'step_4_max_likelihood_fit.png').resolve()}")
print(f"Saved to: {(plot_path / 'step_4_corner.png').resolve()}")
