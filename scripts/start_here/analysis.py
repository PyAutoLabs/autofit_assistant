"""
Start Here: The Likelihood
==========================

The `Analysis` class that connects the Gaussian model to the bundled dataset. An Analysis holds
the data in `__init__` and implements one method, `log_likelihood_function`, which scores a
model instance against that data (`PyAutoFit:autofit/non_linear/analysis/`). Everything
PyAutoFit does — every search, the output tree, the posterior machinery — is built on that one
method, which is why wrapping an existing likelihood is the assistant's defining task
(`skills/af_wrap_likelihood.md`, `skills/af_custom_analysis.md`).

__The likelihood__

The data are 100 independent measurements with known, uncorrelated Gaussian errors, so the log
likelihood is the usual chi-squared sum,

    ln L = -1/2 sum_i [ (d_i - m_i(theta)) / sigma_i ]^2

with the noise-normalisation term dropped because it is a constant: it cancels in every
posterior and in every evidence *difference* between models fitted to the same data, which is
the only way evidences are compared here.

__Contents__

- **Visualizer:** Figures written into the search's own output tree, refreshed as it runs.
- **Analysis:** The likelihood, plus the dataset it is evaluated against.
"""

import numpy as np

import autofit as af


class Visualizer(af.Visualizer):
    """
    Live figures for the fit. `visualize_before_fit` runs once, before the search starts, and
    plots the data on its own; `visualize` runs at the search's update intervals and at
    completion, receiving the best model found so far, and plots it over the data with the
    normalised residuals underneath.

    The figures land in the search's own output directory (`paths.image_path`), which is why the
    output folder is worth opening the moment a fit starts rather than when it ends
    (`skills/_style.md` "Output folder announcement").
    """

    @staticmethod
    def visualize_before_fit(analysis, paths: af.AbstractPaths, model):
        import matplotlib.pyplot as plt

        xvalues = np.arange(analysis.data.shape[0])

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.errorbar(
            xvalues, analysis.data, yerr=analysis.noise_map, fmt=".k", ms=4, elinewidth=0.7
        )
        ax.set_xlabel("x")
        ax.set_ylabel("profile normalization")
        ax.set_title("The 1D dataset being fitted")

        paths.image_path.mkdir(parents=True, exist_ok=True)
        fig.savefig(paths.image_path / "data.png", dpi=140, bbox_inches="tight")
        plt.close(fig)

    @staticmethod
    def visualize(analysis, paths: af.DirectoryPaths, instance, during_analysis: bool):
        import matplotlib.pyplot as plt

        xvalues = np.arange(analysis.data.shape[0])
        model_data = analysis.model_data_from(instance=instance)

        fig, (ax0, ax1) = plt.subplots(
            2, 1, figsize=(7, 5), sharex=True, height_ratios=[3, 1]
        )
        ax0.errorbar(
            xvalues, analysis.data, yerr=analysis.noise_map, fmt=".k", ms=4, elinewidth=0.7
        )
        ax0.plot(xvalues, model_data, "r-", lw=1.5)
        ax0.set_ylabel("profile normalization")
        ax0.set_title("Best fit so far" if during_analysis else "Maximum likelihood fit")

        ax1.plot(xvalues, (analysis.data - model_data) / analysis.noise_map, ".k", ms=4)
        ax1.axhline(0.0, color="r", lw=0.8)
        ax1.set_ylabel("residual / sigma")
        ax1.set_xlabel("x")

        paths.image_path.mkdir(parents=True, exist_ok=True)
        fig.savefig(paths.image_path / "subplot_fit.png", dpi=140, bbox_inches="tight")
        plt.close(fig)


class Analysis(af.Analysis):
    """
    The likelihood for the bundled 1D Gaussian dataset.

    Attaching `Visualizer` as a class attribute is what makes the search write fit and residual
    images as it runs (`skills/af_custom_analysis.md` "a custom Visualizer").
    """

    Visualizer = Visualizer

    def __init__(self, data: np.ndarray, noise_map: np.ndarray):
        super().__init__()

        self.data = data
        self.noise_map = noise_map

    def model_data_from(self, instance) -> np.ndarray:
        """
        The model's prediction for the data.

        A single-component model arrives as an instance of the `Gaussian` class itself; a
        `Collection` arrives as an iterable of such instances, whose profiles sum. Handling both
        here is what lets steps 4 and 6 of the tour share one likelihood across the one-Gaussian
        and three-Gaussian models.
        """
        xvalues = np.arange(self.data.shape[0])

        try:
            return sum(profile.model_data_from(xvalues=xvalues) for profile in instance)
        except TypeError:
            return instance.model_data_from(xvalues=xvalues)

    def log_likelihood_function(self, instance) -> float:
        """
        The log likelihood of a model instance: independent Gaussian errors, so a chi-squared
        sum (see the module docstring for the dropped constant).
        """
        model_data = self.model_data_from(instance=instance)

        chi_squared_map = ((self.data - model_data) / self.noise_map) ** 2.0

        return float(-0.5 * np.sum(chi_squared_map))
