# PyAutoFit Assistant

**Perform statistical inference with Natural Language.**

The **PyAutoFit Assistant** allows you to **perform scientific inference with Natural Language**. 
Describe a model, likelihood function and simply ask it to perform fits with different samplers. 

## Getting Started

### Choosing Your AI Tool

There are two kinds of AI tool you could use the assistant with:

* **Conversational AI assistant:** Use a browser-based tool such as **ChatGPT** or **Claude** to ask questions, plan analyses, and generate scripts that you transfer to your computer and run manually.
* **CLI coding agent:** Use a terminal-based agent such as **Claude Code** or **Codex**. It can work directly on your computer to inspect your data, write and execute scripts, diagnose errors, run model fits, and inspect their results.

**Both kinds are supported, and both currently require a paid plan.** The recommended route is a CLI coding agent: the paid-subscription agents **[Claude Code](docs/setup/claude_code.md)** and **[Codex](docs/setup/codex_cli.md)**, which install **PyAutoFit**, run fits and inspect their results directly on your computer. Conversation assistants work too: **ChatGPT** on a paid plan (Plus/Pro/Team) reads this repository through its [GitHub connector](docs/setup/chatgpt_paid_connector.md), and **Claude** chat on a paid plan (Pro/Max/Team) reads it live through its [GitHub connector](docs/setup/claude_chat_paid.md).

**Free options are being tested** but do not yet have first-class support: the free coding agent **OpenCode** is the most promising (see [Free AI tools](#free-ai-tools) at the bottom of this README), and the free chat routes are listed under [Conversation Assistants](#conversation-assistants).

### Using PyAutoFit Assistant

Every step below can be requested in natural language — you do not need to write Python to follow it.
The workflow is: **model → priors → likelihood → search → results → scientific workflow**.

To begin instantly, install the assistant (above) and ask:

> Fit the bundled dataset in dataset/gaussian_x1/ with a 1D Gaussian.
> Explain the model, priors, likelihood, search and results as we go.

#### Contents

- **Compose the Model**: Describe model components and assign priors to named parameters.
- **Define the Likelihood**: Specify how the model is compared with your data, or supply existing likelihood code.
- **Searches**: Choose between nested sampling, MCMC and optimisation.
- **Model Fit and Results**: Run a fit, inspect parameter estimates and uncertainties, and plot the fitted model.
- **Saving and Loading**: Save results and images during fitting, then reload completed runs for further analysis.
- **Scientific Workflows**: Compose more complex models, compare inference algorithms and investigate saved results.

#### Example

We will fit a 1D Gaussian profile to noisy data and infer its centre,
normalization and width. The data points and their uncertainties are shown
below:

![Noisy one-dimensional Gaussian data with error bars](https://raw.githubusercontent.com/PyAutoLabs/PyAutoFit/main/docs/images/data.png)

For the assistant's bundled dataset, the profile is:

$$
g(x) = N \exp\left[-\frac{1}{2}\left(\frac{x-c}{\sigma}\right)^2\right]
$$

Here, $x$ is the coordinate, $c$ is the centre, $N$ is the normalization
(the peak amplitude in this example), and $\sigma$ is the width. Our task
is to infer $c$, $N$ and $\sigma$ from the data, together with their
uncertainties.

#### Compose the model

> Create a 1D Gaussian model with free centre, normalization and sigma.
> Use uniform priors from 0 to 100 for centre, 0 to 100 for normalization,
> and 0.1 to 30 for sigma. Show me the model and its priors.

This specifies a model with three free parameters:

```bash
Total Free Parameters = 3

model                         Gaussian (N=3)

centre                        UniformPrior [1], lower_limit = 0.0, upper_limit = 100.0
normalization                 LogUniformPrior [2], lower_limit = 1e-06, upper_limit = 1000000.0
sigma                         UniformPrior [3], lower_limit = 0.0, upper_limit = 25.0
```

Models are highly customizable: you can ask to fix a parameter, 
link parameters between components, or assert a constraint. For your own 
science, simply ask the assistant to compose your model for you.

**AI First Design: Internally, **PyAutoFit** composes the model with a name
(`Gaussian`), named parameters (`centre`, `normalization`, `sigma`) and 
an expressive naming convention (e.g. `model.gaussian.sigma`) which ensure
the AI can easily map natural language descriptions of the model to changes in its
internal representation.**

#### Define the likelihood

> Load the 1D Gaussian data and noise map, define a likelihood function which uses 
> independent Gaussian errors to compare the model with the data and for a random 
> set of parameters calculate the likelihood. Produce an image comparing the fit
> to the data

The assistant sets up the likelihood function: which in this case evaluates the 
Gaussian at each data point and compares the predictions with the measurements, 
accounting for their uncertainties. As requested, you get an image comparing
the model and data.

For your own project, you can instead ask:

> Use my existing likelihood code for this analysis [point to code]. Connect 
> it to PyAutoFit and check that it returns the same likelihood values at 
> the same parameter values.

**AI First Design: PyAutoFit gives the agent a small, testable integration task: connect 
named model parameters to your existing likelihood and check that its numerical outputs are unchanged. 
Your validated science code then becomes available to PyAutoFit's searches and result-analysis tools, 
without the agent having to reimplement it.**

You can also give the assistant papers and descriptions of your data,
parameters and assumptions. This supplies the scientific context so you can
use domain-specific natural language while keeping it separate from the inference code.

#### Choose a search

> Show me the available searches. For this first fit, use Dynesty nested
> sampling with 100 live points to estimate the posterior and evidence.

PyAutoFit supports several types of inference algorithm:

- **Nested sampling:** Dynesty and Nautilus, for posterior inference and
  Bayesian evidence estimation.
- **MCMC:** Emcee and Zeus, for posterior sampling.
- **Optimisation:** algorithms such as L-BFGS, for finding a best-fitting
  solution.

The assistant configures the requested search. You can ask it to explain
the settings or help choose an algorithm for your likelihood and scientific
goal.

**AI First Design: All **PyAutoFit** searches share a common interface,
so the agent can switch between them while retaining the model and likelihood,
making it easy to compare inference across different searches.**

#### Fit and inspect the result

> Run the model fit. Show the parameter estimates and uncertainties, and plot
> the maximum-likelihood Gaussian over the data.

The assistant runs the search and presents a summary of the inferred
centre, normalization and width, together with their uncertainties and
a plot of the fitted profile. You can then explore the result:

> Plot the posterior distributions. How well is sigma constrained, and
> is it correlated with normalization?

**AI First Design: Results preserve the model's named
parameters (e.g. `result.instance.gaussian.sigma`), so the agent can connect 
the scientific quantities you specify via language to the numerical results.**

#### Save and revisit the analysis

> Save the run to disk, with fit and residual images updated during
> sampling. Afterwards, reload the saved samples and inspect the fit
> without rerunning it.

Ask to save results and visualization for before starting the fit and the 
assistant will ensure all results and output to hard-disk in a way **designed for efficient human inspection**.

Saved runs retain the model, search settings and sample information, alongside the domain and model specific 
visualization you request. At scale, results can also be collected into a database and queried by dataset metadata,
search, model or result properties. For example:

> Find the completed Gaussian fits and make a table of the inferred widths
> and their uncertainties, labelled by dataset and search algorithm.

**AI First Design: Structured, persistent outputs give
the agent a history of experiments it can reload, query and compare as
your analysis grows.**

#### Extend the workflow

The same building blocks support more involved requests:

**Fit three Gaussians**

> Extend the model to three Gaussians and sum their profiles in the
> likelihood. Assert that their centres are in ascending order, show me
> the priors, perform inference with Dynesty again and compare the Bayesian 
> evidence with the single-Gaussian fit.

The assistant builds a model with three named components and reports
the Bayesian evidence comparison under the stated priors. 

**Compare inference algorithms**

> Fit the same model using Emcee, Dynesty and an optimiser for maximum
> likelihood estimation. Keep the likelihood and parameter bounds fixed,
> and use the same priors for both samplers. Compare runtime, likelihood
> evaluations and best-fit values. For the samplers, also assess convergence
> and agreement of posterior constraints.

This produces a comparison for your likelihood and computing environment,
making it easy to work out which inference method is fastest and which
ones successfully find the best-fit reliably.

**Investigate a saved result**

> Load the saved Gaussian fit. Report the median and 68% credible interval
> for sigma, plot its correlation with normalization, and inspect the
> residuals for structure the model may have missed.

The assistant uses saved samples and the original data to reinspect an
already completed fit.

#### HowToFit

For users less familiar with Bayesian inference and scientific analysis you may wish to read through
the **HowToFits** lectures. These teach you the basic principles of Bayesian inference, with the
content pitched at undergraduate level and above.

The lectures are available in the [standalone HowToFit repository](https://github.com/PyAutoLabs/HowToFit).

If you're new to statistical inference and are not totally sure what concepts like a model, likelihood or
sampling are, you can use **teacher mode** to have the assistant explain concepts in more detail. Simply
start a prompt with "Teacher mode." and ask questions:

```
Teacher mode.

I'm new to PyAutoFit and want to learn the basic workflow end-to-end. Fit the
bundled 1D Gaussian dataset in dataset/gaussian_x1/ and recover its input
parameters.

Explain what each step is doing and why as we go: composing the model, choosing
the priors, picking the non-linear search, and how to read the posterior. So I
come away understanding the workflow, not just the commands.
```

## Science Project

When you begin a scientific study, `autofit_assistant` can create a dedicated **science project**: a structured folder linked to a GitHub repository containing your data, model and likelihood code, prior and search configurations, results, plotting scripts, and a record of your work with the assistant.

The assistant documents the analysis scripts, which can be converted into Jupyter notebooks with explanations as Markdown cells and Python as executable code cells. Collaborators can inspect the project, understand the assumptions behind each fit, reproduce results and extend the analysis with their own assistant.

Projects can also connect to configured HPC facilities for bidirectional synchronisation, job submission and monitoring, supporting larger datasets and more demanding inference workflows. If the study leads to a paper, the repository can become its **open-source companion**, bringing together the scientific assumptions, inference workflow and results needed to reproduce and build on the work.

To begin, include a request like this in your prompt:

> Start a science project using my likelihood code and dataset at [paths].
> Set up an initial fit, record the model assumptions and priors, and organise
> the project so we can compare alternative models and share the results
> with collaborators.

## Scientific Context

PyAutoFit is domain agnostic: **you bring the scientific context**. The assistant ships with a statistics wiki 
covering Bayesian inference, priors, searches and model comparison. Its **literature wiki** at `wiki/literature/` 
is yours to populate with the papers that define your field and analysis.

Adding papers lets the assistant connect your natural language scientific descriptions to its inference: what 
parameters mean, which assumptions are conventional, how previous studies approached the problem, and what might 
complicate the interpretation of a result.

To add a paper, simply ask:

> Ingest this paper into the literature wiki: [arXiv ID, link or local PDF].
> Summarise its model, likelihood, priors and main conclusions, and explain
> how it relates to the analysis we are developing.

The wiki builds a lasting reference for your project, so scientific context is available alongside your code and 
results. As you add relevant papers, the assistant can draw on them to frame decisions, cite prior work and identify 
caveats worth investigating.

## License

The assistant ships agent instructions and reference material derived from the public
PyAuto\* repositories. The underlying libraries are released under their own licenses
(see each repo).

<sub><i><a href="https://open.spotify.com/track/6LeTQu4NvTnLRRiB8GVFQe">if you don't know, don't worry</a></i></sub>
