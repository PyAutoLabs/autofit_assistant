# The tour, step by step

When you paste the [starting prompt](../README.md#starting-prompt), the assistant takes you through six steps on a
bundled 1D Gaussian dataset, one step per turn. This page writes those steps out so you can read ahead or work through
them on your own.

Every step is a request in plain English, so you don't need to write any Python. The workflow is:
**model → priors → likelihood → search → results → scientific workflow**.

You can ask anything at any step ("what is a prior?", "why nested sampling?") without losing your place, and saying
**teacher mode** turns on full explanations for the rest of the tour.

To try the bundled example in one go, ask:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Fit the bundled dataset in dataset/gaussian_x1/ with a 1D Gaussian.
Explain the model, priors, likelihood, search and results as we go.
```

## The steps

- **Compose the model.** Describe the model's components and give each named parameter a prior.
- **Define the likelihood.** Say how the model is compared with your data, or supply likelihood code you already have.
- **Choose a search.** Pick between nested sampling, MCMC and optimisation.
- **Fit and inspect the result.** Run the fit, read the parameter estimates and uncertainties, and plot the fitted model.
- **Save and revisit the analysis.** Save results and images while fitting, then reload finished runs later.
- **Extend the workflow.** Build bigger models, compare inference algorithms and dig into saved results.

## The example

We will fit a 1D Gaussian profile to noisy data and infer its centre, normalization and width. Here are the data
points and their uncertainties:

![Noisy one-dimensional Gaussian data with error bars](https://raw.githubusercontent.com/PyAutoLabs/PyAutoFit/main/docs/images/data.png)

For the assistant's bundled dataset, the profile is:

$$
g(x) = N \exp\left[-\frac{1}{2}\left(\frac{x-c}{\sigma}\right)^2\right]
$$

Here, $x$ is the coordinate, $c$ is the centre, $N$ is the normalization (the peak amplitude in this example), and
$\sigma$ is the width. Our task is to infer $c$, $N$ and $\sigma$ from the data, together with their uncertainties.

## Compose the model

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Create a 1D Gaussian model with free centre, normalization and sigma.
Use uniform priors from 0 to 100 for centre, 0 to 100 for normalization,
and 0.1 to 30 for sigma. Show me the model and its priors.
```

This gives a model with three free parameters:

```bash
Total Free Parameters = 3

model                         Gaussian (N=3)

centre                        UniformPrior [0], lower_limit = 0.0, upper_limit = 100.0
normalization                 UniformPrior [1], lower_limit = 0.0, upper_limit = 100.0
sigma                         UniformPrior [2], lower_limit = 0.1, upper_limit = 30.0
```

You can customise models in many ways: fix a parameter, link parameters between components or add a constraint. For
your own science, just ask the assistant to compose your model for you.

**AI First Design.** PyAutoFit gives the model a name (`Gaussian`), named parameters (`centre`, `normalization`, `sigma`)
and readable paths to them (e.g. `model.gaussian.sigma`), so the AI can turn what you say about the model into the
right change.

**Try it:** reword the request ("make it two Gaussians", "fix sigma to 10", "put a Gaussian prior on centre, mean 50,
sigma 10") and watch `model.info` change.

## Define the likelihood

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Load the 1D Gaussian data and noise map, define a likelihood function which uses
independent Gaussian errors to compare the model with the data and for a random
set of parameters calculate the likelihood. Produce an image comparing the fit
to the data
```

The assistant sets up the likelihood function. Here it evaluates the Gaussian at each data point and compares the
predictions with the measurements, taking their uncertainties into account. You also get the image comparing the
model and data that you asked for.

For your own project, you can instead ask:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Use my existing likelihood code for this analysis [point to code]. Connect
it to PyAutoFit and check that it returns the same likelihood values at
the same parameter values.
```

**AI First Design.** Connecting your code is a small task the assistant can test: link the named model parameters to your
existing likelihood and check its numbers don't change. Your validated science code then works with all of
PyAutoFit's searches and results tools, without the assistant rewriting it.

You can also give the assistant papers and descriptions of your data, parameters and assumptions. That gives it the
scientific context, so you can talk in the language of your field while the inference code stays separate.

**Try it:** ask for the likelihood at the true parameters (`centre=50`, `normalization=25`, `sigma=10`) and compare it
with the random draw.

## Choose a search

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Show me the available non-linear searches, including those which support
gradient based inference using JAX. For this example fit, our likelihood
function is not implemented using JAX, so lets use Dynesty nested sampling
with 100 live points to estimate the posterior and evidence.
```

PyAutoFit supports several kinds of inference algorithm:

- **Nested sampling:** Dynesty and Nautilus, for posterior inference and Bayesian evidence estimation.
- **MCMC:** Emcee and Zeus, for posterior sampling.
- **Optimisation:** algorithms such as L-BFGS, for finding a best-fitting solution.
- **Gradient-based (JAX):** `BlackJAXNUTS` for Hamiltonian / NUTS sampling, and `MultiStartAdam` /
  `MultiStartProdigy` for optimisation. These take gradients of your likelihood automatically, so the likelihood must
  be written in JAX. That's why this example, whose likelihood is plain NumPy, uses Dynesty.

The assistant sets up the search you asked for. You can ask it to explain the settings, or to help choose an algorithm
for your likelihood and scientific goal.

**AI First Design.** Every PyAutoFit search works the same way, so the assistant can swap one for another while keeping
your model and likelihood, which makes comparing searches easy.

**Try it:** ask "use Emcee instead" or "what changes with 50 live points?", and have the trade-off explained before
you commit to it.

## Fit and inspect the result

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Run the model fit. Show the parameter estimates and uncertainties, and plot
the maximum-likelihood Gaussian over the data.
```

The assistant runs the search and summarises the inferred centre, normalization and width with their uncertainties,
plus a plot of the fitted profile. You can then explore the result:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Plot the posterior distributions. How well is sigma constrained, and
is it correlated with normalization?
```

**AI First Design.** Results keep the model's named parameters (e.g. `result.instance.gaussian.sigma`), so the assistant
can match the quantities you name to the numbers in the result.

**Try it:** ask "what is the Bayesian evidence, and what is it for?" or "how many likelihood evaluations did that
take?".

## Save and revisit the analysis

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Save the run to disk, with fit and residual images updated during
sampling. Afterwards, reload the saved samples and inspect the fit
without rerunning it.
```

Ask for results and images to be saved before the fit starts, and the assistant writes everything to disk in a layout
**designed for people to browse**.

Saved runs keep the model, search settings and samples, alongside any plots you ask for. At scale, you can collect
results into a database and search them by dataset, search, model or result. For example:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Find the completed Gaussian fits and make a table of the inferred widths
and their uncertainties, labelled by dataset and search algorithm.
```

**AI First Design.** Saved, structured results give the assistant a history of your experiments that it can reload,
search and compare as your analysis grows.

**Try it:** run the same script again. A finished search reloads its results instead of fitting again, which surprises
everyone once.

## Extend the workflow

The same building blocks handle bigger requests.

**Fit three Gaussians**

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Extend the model to three Gaussians and sum their profiles in the
likelihood. Assert that their centres are in ascending order, show me
the priors, perform inference with Dynesty again and compare the Bayesian
evidence with the single-Gaussian fit.
```

The assistant builds a model with three named components and reports how the Bayesian evidence compares under the
priors you gave.

**Compare inference algorithms**

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Fit the same model using Emcee, Dynesty and an optimiser for maximum
likelihood estimation. Keep the likelihood and parameter bounds fixed,
and use the same priors for both samplers. Compare runtime, likelihood
evaluations and best-fit values. For the samplers, also assess convergence
and agreement of posterior constraints.
```

You get a comparison for your own likelihood and computer, showing which method is fastest and which reliably finds
the best fit.

**Investigate a saved result**

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Load the saved Gaussian fit. Report the median and 68% credible interval
for sigma, plot its correlation with normalization, and inspect the
residuals for structure the model may have missed.
```

The assistant uses the saved samples and the original data to look again at a fit that has already finished.

**Try it:** pick one of these three prompts; you don't need to run them all. The three-Gaussian fit is the first that
takes real time, so say "use Nautilus instead" if you'd rather not wait on Dynesty.

## Next steps

Everything above was natural language. You didn't write a line of Python, though the assistant saved the scripts
anyway, one per step, so you can read, rerun and change them yourself.

When you're ready, move on to [your own project](your_own_project.md). The tour itself is scripted in
[`modes/start_here.md`](../modes/start_here.md).
