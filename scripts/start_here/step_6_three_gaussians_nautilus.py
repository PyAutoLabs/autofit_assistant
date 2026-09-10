"""
Start Here Step 6 (variant): Three Gaussians with Nautilus
==========================================================

The same extension as `step_6_three_gaussians.py` — three summed Gaussians with their centres
asserted into ascending order, compared on Bayesian evidence with step 4's single-Gaussian model
— but sampled with `af.Nautilus` instead of `af.DynestyStatic`, both fits alike.

Why the variant exists: nine free parameters plus a hard ordering assertion is a genuinely
awkward space for Dynesty, whose ellipsoidal bounds keep proposing draws the assertion rejects,
and the fit crawls. Nautilus's neural-network-boosted region sampling handles the same space far
better. The model, the priors, the assertion and the likelihood are identical — only the search
changed, which is the point `af_configure_search` makes about the common search interface.

The data were simulated from *one* Gaussian, so the expected answer is that the three-Gaussian
model is not preferred: it fits marginally better but pays for six extra parameters, and the
evidence — which charges for that automatically — should come out lower. Seeing the penalty
arrive on its own is the point of the exercise.

This script fits the single-Gaussian model with Nautilus too, so both evidences in the
comparison come from the same sampler; it reloads rather than re-runs on any later execution.

__Contents__

- **Imports:** autofit and the tour's model and likelihood.
- **Dataset:** Load the data and noise map.
- **Single Gaussian:** Step 4's model under Nautilus, for a same-sampler comparison.
- **Three Gaussians:** The wider model, with the ascending-centre assertion.
- **Fit:** Run Nautilus on the wider model.
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

Step 4's single-Gaussian model, but sampled with Nautilus so **both** evidences in the
comparison below come from the same estimator. Evidence is a property of the model and priors,
not of the sampler, but two samplers' estimates carry different biases and error bars, so a
model comparison is cleanest when one sampler produces both numbers. It costs seconds here.
"""

result_x1 = af.Nautilus(
    path_prefix="start_here",
    name="gaussian_x1_nautilus",
    n_live=100,
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

A different model and a different search each give a new unique identifier, so this fit writes
to its own folder beside step 4's and the Dynesty variant's; none of them overwrites another.
Nine free parameters instead of three still costs real time, which is itself the lesson about
model complexity — but the sampler choice is the other half of that lesson.
"""

result_x3 = af.Nautilus(
    path_prefix="start_here",
    name="gaussian_x3_nautilus",
    n_live=100,
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
