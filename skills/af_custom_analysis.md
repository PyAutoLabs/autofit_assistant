---
name: af_custom_analysis
description: Extend an Analysis class beyond plain likelihood wrapping — extra data/config inputs in __init__, a custom Visualizer that plots model fits during and after the search, and a custom Result carrying science-specific attributes. Use when the user wants on-disk visualization of fits as the search runs, richer Result objects, or an Analysis carrying masks/kernels/covariances. Builds on af_wrap_likelihood (do that first if the likelihood isn't wrapped yet); not for the wrapping itself.
user-invocable: true
---

# Customizing an Analysis

`af_wrap_likelihood` gets your likelihood into PyAutoFit; this skill is what you reach
for when the wrapper should *do more* — carry every input your likelihood needs, draw
its own diagnostic figures while the search runs, and return a `Result` that speaks
your science's language. All three extensions are class-attribute overrides on the
same `af.Analysis` you already have (`PyAutoFit:autofit/non_linear/analysis/`).

## Orient

The canonical worked example is `autofit_workspace:scripts/cookbooks/analysis.py` —
its sections map one-to-one onto the branches below. The constitution's rule stands
throughout: extra inputs and visualization never alter the likelihood's numerics.

## Ask

- What extra inputs does the likelihood genuinely need at call time (mask, kernel,
  covariance, instrument config)? Everything else stays out of the class.
- What figure would tell *you* at a glance whether a fit is healthy? That's the
  Visualizer's job — not publication plots, health plots.
- What derived quantities do you reach for from every result? Those belong on a
  custom `Result`.

## Branch — extra `__init__` inputs

Anything the likelihood needs is constructor state — computed once, reused per call:

```python
"""
__Analysis__

The Analysis carries everything the likelihood needs: here a noise covariance, a mask
and a convolution kernel. Expensive derived state (e.g. a Cholesky factor) is computed
once here, not per likelihood call — packaging, never a numerics change
(`autofit_workspace:scripts/cookbooks/analysis.py` __Customization__).
"""
class Analysis(af.Analysis):
    def __init__(self, data, noise_covariance_matrix, mask, kernel):
        super().__init__()
        self.data = data
        self.mask = mask
        self.kernel = kernel
        self.noise_covariance_matrix = noise_covariance_matrix
```

## Branch — a custom Visualizer

Override the `Visualizer` class attribute; PyAutoFit calls its hooks with the
search's current best instance, writing into the search's own `output/` tree:

```python
"""
__Visualization__

`visualize_before_fit` runs once (plot the data being fitted); `visualize` runs at the
search's update intervals and at completion, receiving the current max-likelihood
instance — the live health check for a long fit
(`autofit_workspace:scripts/cookbooks/analysis.py` __Visualization__).
"""
class Visualizer(af.Visualizer):
    @staticmethod
    def visualize_before_fit(analysis, paths: af.DirectoryPaths, model):
        ...  # plot analysis.data into paths' image directory

    @staticmethod
    def visualize(analysis, paths: af.DirectoryPaths, instance, during_analysis):
        ...  # plot instance's model against analysis.data + residuals


class Analysis(af.Analysis):
    Visualizer = Visualizer
    ...
```

For 1D-profile problems, `af.ex.plot_profile_1d(xvalues=..., profile_1d=...,
output_path=pathlib.Path(...), output_filename=...)` is a ready-made figure helper
(`output_path` must be a `pathlib.Path`, not a str). Quote the output
directory to the user — the point of a Visualizer is that someone looks.

## Branch — a custom Result

Override `Result` (and `make_result` when construction needs extra inputs) so every
fit returns your science's objects directly:

```python
"""
__Custom Result__

result.best_model_data becomes a first-class attribute of every fit of this Analysis —
no re-deriving in every notebook (`autofit_workspace:scripts/cookbooks/analysis.py`
__Custom Result__ section; `PyAutoFit:autofit/non_linear/analysis/`).
"""
class Result(af.Result):
    @property
    def best_model_data(self):
        xvalues = np.arange(self.analysis.data.shape[0])
        return self.instance.model_data_from(xvalues=xvalues)


class Analysis(af.Analysis):
    Result = Result
    ...
```

## Combine

- The upgraded Analysis drops straight into `af_run_search` and the aggregator flow of
  `af_load_results` — custom Result attributes come back on reload too.
- Fits that misbehave despite good visuals route to `af_debug_fit_failure`.
- Offer (default-yes) a `wiki/project/` entry: what the Analysis now carries, what the
  Visualizer draws, what the Result exposes.

## Further reading

- **General reference** — [RTD: analysis cookbook](https://pyautofit.readthedocs.io/en/latest/cookbooks/analysis.html).
- **Experienced PyAutoFit user** — `autofit_workspace:scripts/cookbooks/analysis.py`.
