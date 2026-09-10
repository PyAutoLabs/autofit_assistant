"""
Start Here Step 1: Compose the Model
====================================

The first step of the "start here" tour. A model in PyAutoFit is a plain Python class whose
`__init__` arguments become the free parameters of the fit, wrapped in an `af.Model`. Here the
class is the 1D Gaussian profile in `gaussian.py` and the three free parameters are its centre,
normalization and width, each given an explicit prior stating what we believe before seeing the
data.

The bundled dataset in `dataset/gaussian_x1/` was simulated from this profile with
`centre=50.0`, `normalization=25.0`, `sigma=10.0` and per-pixel noise sigma 2.0, so the fit in
step 4 has a known truth to be judged against.

__Contents__

- **Imports:** autofit and the tour's Gaussian class.
- **Model:** Wrap the class in `af.Model` and state every prior explicitly.
- **Variation - Two Gaussians:** The same request reworded as a two-component model.
"""

import autofit as af

from gaussian import Gaussian

"""
__Model__

`af.Model(Gaussian)` inspects the class's `__init__` signature and creates one free parameter
per argument. Every prior is stated explicitly — defaults are convenient for a demonstration,
but a prior is a scientific statement, so a real analysis always states it
(`PyAutoFit:autofit/mapper/prior/`, and `skills/af_compose_model.md`).

`UniformPrior` says "any value in this range, equally likely". The centre is bounded by the
100-pixel grid, the normalization by the observed dynamic range, and sigma is kept strictly
positive by a lower limit of 0.1.

The priors are passed as keyword arguments **at construction** rather than assigned afterwards.
Both forms compose the same model; passing them at construction means the priors printed in
`model.info` carry the ids `[0]`, `[1]`, `[2]`, because assigning after construction first
mints the class's default priors and the surviving ids then start at `[3]`. The ids are a
creation-order counter over every prior made in the process — worth knowing before they look
surprising.
"""

model = af.Model(
    Gaussian,
    centre=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
    normalization=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
    sigma=af.UniformPrior(lower_limit=0.1, upper_limit=30.0),
)

print(model.info)

print(f"\nFree parameters: {model.prior_count}")

"""
__Variation - Two Gaussians__

The point of describing a model in natural language is that rewording the description rewords
the model. "Make it two Gaussians" becomes an `af.Collection` of two `af.Model` objects: the
search explores a single flat six-dimensional space and the likelihood receives an instance
with two named attributes, `instance.gaussian_0` and `instance.gaussian_1`
(`PyAutoFit:autofit/mapper/prior_model/collection.py`).

Nothing else about the workflow changes — the same likelihood, the same search and the same
result machinery apply to the wider model. That is the point of the tour's "describe it
differently" nudge: the model is the part you restate, not the pipeline around it.

Prior ids continue from the single-Gaussian model above, so this collection's ids run `[3]` to
`[8]`; run the variation on its own and they run `[0]` to `[5]`.
"""


def gaussian_model() -> af.Model:
    return af.Model(
        Gaussian,
        centre=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
        normalization=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
        sigma=af.UniformPrior(lower_limit=0.1, upper_limit=30.0),
    )


model_x2 = af.Collection(gaussian_0=gaussian_model(), gaussian_1=gaussian_model())

print("\n" + "=" * 70)
print('Variation: "make it two Gaussians"')
print("=" * 70 + "\n")

print(model_x2.info)

print(f"\nFree parameters: {model_x2.prior_count}")
