"""
Start Here: The Model Component
===============================

The 1D Gaussian profile fitted by the "start here" tour, as a plain Python class. PyAutoFit
composes models from ordinary classes like this one — the `__init__` arguments become the
model's free parameters and `model_data_from` evaluates the profile — so the model code stays
the user's own rather than a framework object (`PyAutoFit:autofit/mapper/model.py`).

__Normalisation convention__

This Gaussian is **peak-normalised**: `normalization` is the profile's peak amplitude, matching
the equation quoted on the RTD natural-language page and in `dataset/gaussian_x1/README.md`:

    g(x) = N exp[-1/2 ((x - c) / sigma)^2]

The bundled dataset was simulated in that convention (`centre=50.0`, `normalization=25.0`,
`sigma=10.0`, per-pixel noise sigma 2.0), so a correct fit recovers a normalization near 25.

PyAutoFit's own example class, `af.ex.Gaussian`, is instead **area-normalised** — it divides by
`sigma * sqrt(2 pi)` — which on this dataset would put the normalization near 620, outside the
uniform 0-100 prior the tour prescribes. Neither convention is more correct; the point is that
the model class defines it, and the class is yours. If a user's own model uses the area
convention, their priors follow their convention.

__Contents__

- **Gaussian:** The model component whose three `__init__` arguments are the free parameters.
"""

import numpy as np


class Gaussian:
    def __init__(
        self,
        centre: float = 0.0,
        normalization: float = 1.0,
        sigma: float = 1.0,
    ):
        """
        A 1D Gaussian profile, peak-normalised (see the module docstring).

        Parameters
        ----------
        centre
            The x coordinate of the profile's centre.
        normalization
            The peak amplitude of the profile.
        sigma
            The standard deviation, setting the profile's width.
        """
        self.centre = centre
        self.normalization = normalization
        self.sigma = sigma

    def model_data_from(self, xvalues: np.ndarray) -> np.ndarray:
        """
        The profile evaluated on a 1D grid of x coordinates.

        Parameters
        ----------
        xvalues
            The x coordinates in the reference frame of the data.
        """
        return self.normalization * np.exp(
            -0.5 * ((xvalues - self.centre) / self.sigma) ** 2
        )
