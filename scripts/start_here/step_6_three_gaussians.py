"""
Start Here Step 6: Extend the Workflow - Three Gaussians
=======================================================

The sixth and final step of the "start here" tour, and the first of the RTD page's three
extensions. The model is widened to three Gaussians whose profiles sum, their centres are
asserted to be in ascending order, the same Dynesty search is run again, and the Bayesian
evidence is compared with the single-Gaussian fit of step 4.

The data were simulated from *one* Gaussian, so the expected answer is that the three-Gaussian
model is not preferred: it fits marginally better but pays for six extra parameters, and the
evidence — which charges for that automatically — should come out lower. Seeing the penalty
arrive on its own is the point of the exercise.

This script re-runs step 4's single-Gaussian fit if it is not already on disk (it reloads if it
is), so the evidence comparison always has both numbers.

__Contents__

- **Imports:** autofit and the tour's model and likelihood.
- **Dataset:** Load the data and noise map.
- **Single Gaussian:** The step 4 fit, reloaded or re-run, for the comparison.
- **Three Gaussians:** The wider model, with the ascending-centre assertion.
- **Fit:** Run the search on the wider model.
- **Evidence Comparison:** What the Bayesian evidence says about the extra components.
"""

import pathlib

import numpy as np

import autofit as af

from analysis import Analysis
from gaussian import Gaussian

"""
__Dataset__
"""

dataset_path = pathlib.Path("dataset") / "gaussian_x1"

data = af.util.numpy_array_from_json(file_path=dataset_path / "data.json")
noise_map = af.util.numpy_array_from_json(file_path=dataset_path / "noise_map.json")

analysis = Analysis(data=data, noise_map=noise_map)


def gaussian_model() -> af.Model:
    return af.Model(
        Gaussian,
        centre=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
        normalization=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
        sigma=af.UniformPrior(lower_limit=0.1, upper_limit=30.0),
    )


"""
__Single Gaussian__

Identical to step 4, so this reloads that completed search rather than repeating it — the
`path_prefix`, `name` and model are unchanged, which is exactly what the unique identifier keys
on (`skills/af_configure_search.md` "Output discipline").
"""

result_x1 = af.DynestyStatic(
    path_prefix="start_here",
    name="gaussian_x1",
    nlive=100,
    number_of_cores=1,
).fit(model=gaussian_model(), analysis=analysis)

"""
__Three Gaussians__

Three components in an `af.Collection`, summed by the same `Analysis` used throughout — the
likelihood already handles a collection by summing each profile, so widening the model changed
no code.

Three identical components leave the posterior invariant under relabelling them: every solution
appears six times, once per permutation, which is a genuinely harder space for a sampler than a
single peak. `add_assertion` fixes that by declaring the centres ascending, so exactly one
labelling survives (`PyAutoFit:autofit/mapper/prior_model/abstract.py`, and
`skills/af_compose_model.md` "customization"). An assertion is a prior statement like any
other — it carves the rejected region out of the prior volume, and the evidence below is the
evidence *under these priors*.
"""

model_x3 = af.Collection(
    gaussian_0=gaussian_model(),
    gaussian_1=gaussian_model(),
    gaussian_2=gaussian_model(),
)

model_x3.add_assertion(model_x3.gaussian_0.centre < model_x3.gaussian_1.centre)
model_x3.add_assertion(model_x3.gaussian_1.centre < model_x3.gaussian_2.centre)

print(model_x3.info)

"""
__Fit__

A different model means a different unique identifier, so this fit writes to its own folder
beside step 4's and neither overwrites the other. Nine free parameters instead of three: expect
it to take noticeably longer, which is itself the lesson about model complexity.
"""

result_x3 = af.DynestyStatic(
    path_prefix="start_here",
    name="gaussian_x3",
    nlive=100,
    number_of_cores=1,
).fit(model=model_x3, analysis=analysis)

print(result_x3.info)

"""
__Evidence Comparison__

The Bayesian evidence is the likelihood averaged over the prior, so a model that spends prior
volume on parameter space the data do not need is penalised without anyone adding a penalty
term. Compare log evidences between models fitted to the **same data**; the difference is what
carries meaning, and on the usual Jeffreys-style reading a difference of more than about 5 is
strong preference (`skills/af_load_results.md`, and `wiki/core/` on evidence and model
comparison).

The maximum log likelihood is shown alongside deliberately: the wider model always fits at
least as well by that measure, which is precisely why it is the wrong measure for choosing
between models of different size.
"""

log_evidence_x1 = result_x1.samples.log_evidence
log_evidence_x3 = result_x3.samples.log_evidence

print("\nmodel               N     max log L      log evidence")
print("-" * 56)
print(
    f"{'one Gaussian':<20}{result_x1.model.prior_count:<6}"
    f"{np.max(result_x1.samples.log_likelihood_list):<15.2f}{log_evidence_x1:.2f}"
)
print(
    f"{'three Gaussians':<20}{result_x3.model.prior_count:<6}"
    f"{np.max(result_x3.samples.log_likelihood_list):<15.2f}{log_evidence_x3:.2f}"
)

difference = log_evidence_x3 - log_evidence_x1

preferred = "three Gaussians" if difference > 0 else "one Gaussian"

print(
    f"\nlog evidence difference (three - one) = {difference:.2f}"
    f"  ->  preferred: {preferred}"
)
