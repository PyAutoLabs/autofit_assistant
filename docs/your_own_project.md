# Your own project, step by step

The [tour](tour.md) doesn't stop at the Gaussian. The same six steps run on your own science, in the order below. You
can ask for any of them directly if you'd rather skip ahead, and you can ask anything at any step or say
**teacher mode** for full explanations.

If you already have likelihood code, start from the
[Bring Your Own Likelihood prompt](../README.md#bring-your-own-likelihood-byol) instead.

## The steps

**P0. Science context.** Start from a paper, or from a plain-language description of what you measure and what you
want to infer, plus where your data lives and in what format. The assistant restates your problem in inference terms
(parameters, data, the shape of the likelihood) for you to correct. Adding the papers that define your field to the
literature wiki helps here; see [Scientific Context](../README.md#scientific-context).

**P1. Model.** Your parametrisation, described in words, becomes a PyAutoFit model with explicit priors, and
`model.info` shows you exactly what will be fitted. Describe it differently and the model changes with it.

**P2. Likelihood.** If you already have likelihood code, it stays yours: the assistant wraps it and checks it returns
the same numbers, and never re-parametrises or "fixes" your science. If you don't, it builds a simple one from your
description. Either way, your real data is plotted and discussed. Unmodelled problems in the data are the first source
of biased inference, so this step is not optional.

**P3. Search.** Your runtime budget, whether your likelihood is JAX-differentiable, and whether you need the Bayesian
evidence decide the sampler between them. You get a recommendation with the reason, not just a name.

**P4. Fit and results.** Nothing is fitted until you give the go-ahead. Then the search runs, you're shown around the
output folder while it does, and the results are plotted and read back to you. Real data has no known truth to check
against, so the check becomes the residuals and the shape of the posterior.

**P5. Save and organise.** When the analysis is worth keeping, it can become a
[science project](../README.md#science-project) of its own.

**P6. Extend.** Model comparison, sampler comparison, chaining searches into a pipeline, hierarchical models over many
datasets: the PyAutoFit
[Scientific Workflow](https://pyautofit.readthedocs.io/en/latest/overview/scientific_workflow.html) and
[Statistical Methods](https://pyautofit.readthedocs.io/en/latest/overview/statistical_methods.html) pages describe
what is available, and you can ask for any of it the same way.

Everything here is natural language. The assistant still saves the scripts, one per step, so you can read, rerun and
change them yourself.
