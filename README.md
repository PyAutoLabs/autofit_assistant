# PyAutoFit Assistant

**Bring your models, data and likelihood code. Perform scientific inference through conversation.**

## Getting Started

**PyAutoFit** and the **autofit_assistant** allow one to perform scientific inference using purely natural language.
Simply open your AI coding agent (`codex` or `Claude Code` are recommended) and input the following prompt:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
I want to perform scientific inference with PyAutoFit (https://github.com/PyAutoLabs/PyAutoFit) and the
autofit_assistant (https://github.com/PyAutoLabs/autofit_assistant).

Begin the "start here" guide for a new user.
```

**What happens when you type it.** The assistant starts a guided tour that runs in two tracks. First the **bundled
1D Gaussian**: six steps — compose a model, define a likelihood, choose a search, fit and read the result, save and
reload it, then extend the workflow — one step per turn, with **you** typing each prompt, so you find out for
yourself that the whole workflow is natural language. Then **your own science**: a paper or a plain-language
description of what you measure, then your model, your likelihood, a search chosen for your problem, the fit, and
the results. You can stop and ask "what is a prior?" at any step without losing your place, and saying
**teacher mode** turns on full explanations for the rest of the tour. If you already have likelihood code, the
**Bring Your Own Likelihood (BYOL)** prompt under [Your own project](#bring-your-own-likelihood-byol) is the other
door in — it starts from your function instead of the Gaussian.

The tour is scripted in [`modes/start_here.md`](modes/start_here.md); the sections below are the same six steps,
written out so you can read ahead or work through them on your own.

## Setting up the assistant

The assistant runs inside an **AI coding agent** — a tool that reads this repository, executes Python on your
computer and inspects the results. That is what lets it install **PyAutoFit**, wrap your likelihood code, run
searches and look at the plots they produce. You do not have to run anything to use it: discussing a model, choosing
priors, planning an analysis or learning in Teacher Mode all happen inside the same agent.

1. **Choose Claude Code or Codex.** These are the two recommended agents and the ones the assistant is developed and
   tested against — see [Claude Code](docs/setup/claude_code.md) and [Codex](docs/setup/codex_cli.md). For sustained
   scientific work expect to pay for one of them, but how depends on your situation: a personal subscription, access
   through your institution or team, or usage-based API billing. Check the provider's current plans rather than
   assuming a subscription is the only route. Desktop and IDE versions of either agent are fine, provided they can
   read this repository and execute code.
2. **Open the assistant workspace.** Clone this repository and start the agent inside it — the instructions load
   automatically, and the assistant installs PyAutoFit for you if it is missing:

   ```bash
   git clone https://github.com/PyAutoLabs/autofit_assistant.git
   cd autofit_assistant
   claude        # or: codex
   ```

3. **Submit the starting prompt — the tour begins.** Paste the prompt at the top of this README and the assistant
   opens the guided tour at step 1. (If you already have likelihood code, the "Bring Your Own Likelihood" prompt
   under [Your own project](#bring-your-own-likelihood-byol) starts **BYOL mode** instead, running the same
   workflow from your code.)

**Experimental alternative.** [OpenCode](docs/setup/opencode_cli.md) is an open-source coding agent whose client is
free; the model you connect it to is a separate choice with its own cost and capability, free offerings are often
time-limited, and no provider/model configuration has yet been validated against this assistant — treat it as
compatible, not tested. Browser chats with a GitHub connector are **no longer supported** (retired 2026-09-10; the old
pages are archived with a notice under [`docs/archive/`](docs/archive/README.md)).

## The tour, step by step

Every step below can be requested in natural language — you do not need to write Python to follow it.
The workflow is: **model → priors → likelihood → search → results → scientific workflow**.

To try the bundled example, ask:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Fit the bundled dataset in dataset/gaussian_x1/ with a 1D Gaussian.
Explain the model, priors, likelihood, search and results as we go.
```

### Contents

- **Compose the Model**: Describe model components and assign priors to named parameters.
- **Define the Likelihood**: Specify how the model is compared with your data, or supply existing likelihood code.
- **Searches**: Choose between nested sampling, MCMC and optimisation.
- **Model Fit and Results**: Run a fit, inspect parameter estimates and uncertainties, and plot the fitted model.
- **Saving and Loading**: Save results and images during fitting, then reload completed runs for further analysis.
- **Scientific Workflows**: Compose more complex models, compare inference algorithms and investigate saved results.

### Example

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

### Compose the model

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Create a 1D Gaussian model with free centre, normalization and sigma.
Use uniform priors from 0 to 100 for centre, 0 to 100 for normalization,
and 0.1 to 30 for sigma. Show me the model and its priors.
```

This specifies a model with three free parameters:

```bash
Total Free Parameters = 3

model                         Gaussian (N=3)

centre                        UniformPrior [0], lower_limit = 0.0, upper_limit = 100.0
normalization                 UniformPrior [1], lower_limit = 0.0, upper_limit = 100.0
sigma                         UniformPrior [2], lower_limit = 0.1, upper_limit = 30.0
```

Models are highly customizable: you can ask to fix a parameter, 
link parameters between components, or assert a constraint. For your own 
science, simply ask the assistant to compose your model for you.

**AI First Design.** Internally, PyAutoFit composes the model with a name (`Gaussian`), named parameters (`centre`, `normalization`, `sigma`) and an expressive naming convention (e.g. `model.gaussian.sigma`) which ensure the AI can easily map natural language descriptions of the model to changes in its internal representation.

**Try it:** reword it — "make it two Gaussians", "fix sigma to 10", "put a Gaussian prior on centre, mean 50, sigma 10" — and watch `model.info` change.

*Ask anything at this step — "what is a prior?", "why nested sampling?" — or say "teacher mode" for full explanations.*

### Define the likelihood

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Load the 1D Gaussian data and noise map, define a likelihood function which uses
independent Gaussian errors to compare the model with the data and for a random
set of parameters calculate the likelihood. Produce an image comparing the fit
to the data
```

The assistant sets up the likelihood function: which in this case evaluates the 
Gaussian at each data point and compares the predictions with the measurements, 
accounting for their uncertainties. As requested, you get an image comparing
the model and data.

For your own project, you can instead ask:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Use my existing likelihood code for this analysis [point to code]. Connect
it to PyAutoFit and check that it returns the same likelihood values at
the same parameter values.
```

**AI First Design.** PyAutoFit gives the agent a small, testable integration task: connect named model parameters to your existing likelihood and check that its numerical outputs are unchanged. Your validated science code then becomes available to PyAutoFit's searches and result-analysis tools, without the agent having to reimplement it.

You can also give the assistant papers and descriptions of your data,
parameters and assumptions. This supplies the scientific context so you can
use domain-specific natural language while keeping it separate from the inference code.

**Try it:** ask for the likelihood at the true parameters (`centre=50`, `normalization=25`, `sigma=10`) and compare it with the random draw.

*Ask anything at this step — "what is a prior?", "why nested sampling?" — or say "teacher mode" for full explanations.*

### Choose a search

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Show me the available non-linear searches, including those which support
gradient based inference using JAX. For this example fit, our likelihood
function is not implemented using JAX, so lets use Dynesty nested sampling
with 100 live points to estimate the posterior and evidence.
```

PyAutoFit supports several types of inference algorithm:

- **Nested sampling:** Dynesty and Nautilus, for posterior inference and
  Bayesian evidence estimation.
- **MCMC:** Emcee and Zeus, for posterior sampling.
- **Optimisation:** algorithms such as L-BFGS, for finding a best-fitting
  solution.
- **Gradient-based (JAX):** `BlackJAXNUTS` for Hamiltonian / NUTS sampling, and
  `MultiStartAdam` / `MultiStartProdigy` for optimisation. These take gradients
  of your likelihood automatically, so they require it to be written in JAX —
  which is why this example, whose likelihood is plain NumPy, uses Dynesty.

The assistant configures the requested search. You can ask it to explain
the settings or help choose an algorithm for your likelihood and scientific
goal.

**AI First Design.** All PyAutoFit searches share a common interface, so the agent can switch between them while retaining the model and likelihood, making it easy to compare inference across different searches.

**Try it:** ask "use Emcee instead" — or "what changes with 50 live points?" — and have the trade-off explained before you commit to it.

*Ask anything at this step — "what is a prior?", "why nested sampling?" — or say "teacher mode" for full explanations.*

### Fit and inspect the result

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Run the model fit. Show the parameter estimates and uncertainties, and plot
the maximum-likelihood Gaussian over the data.
```

The assistant runs the search and presents a summary of the inferred
centre, normalization and width, together with their uncertainties and
a plot of the fitted profile. You can then explore the result:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Plot the posterior distributions. How well is sigma constrained, and
is it correlated with normalization?
```

**AI First Design.** Results preserve the model's named parameters (e.g. `result.instance.gaussian.sigma`), so the agent can connect the scientific quantities you specify via language to the numerical results.

**Try it:** ask "what is the Bayesian evidence, and what is it for?" or "how many likelihood evaluations did that take?".

*Ask anything at this step — "what is a prior?", "why nested sampling?" — or say "teacher mode" for full explanations.*

### Save and revisit the analysis

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Save the run to disk, with fit and residual images updated during
sampling. Afterwards, reload the saved samples and inspect the fit
without rerunning it.
```

Ask to save results and visualization for before starting the fit and the 
assistant will ensure all results and output to hard-disk in a way **designed for efficient human inspection**.

Saved runs retain the model, search settings and sample information, alongside the domain and model specific 
visualization you request. At scale, results can also be collected into a database and queried by dataset metadata,
search, model or result properties. For example:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Find the completed Gaussian fits and make a table of the inferred widths
and their uncertainties, labelled by dataset and search algorithm.
```

**AI First Design.** Structured, persistent outputs give the agent a history of experiments it can reload, query and compare as your analysis grows.

**Try it:** run the same script again — a completed search reloads instead of re-fitting, which surprises everyone once.

*Ask anything at this step — "what is a prior?", "why nested sampling?" — or say "teacher mode" for full explanations.*

### Extend the workflow

The same building blocks support more involved requests:

**Fit three Gaussians**

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Extend the model to three Gaussians and sum their profiles in the
likelihood. Assert that their centres are in ascending order, show me
the priors, perform inference with Dynesty again and compare the Bayesian
evidence with the single-Gaussian fit.
```

The assistant builds a model with three named components and reports
the Bayesian evidence comparison under the stated priors. 

**Compare inference algorithms**

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Fit the same model using Emcee, Dynesty and an optimiser for maximum
likelihood estimation. Keep the likelihood and parameter bounds fixed,
and use the same priors for both samplers. Compare runtime, likelihood
evaluations and best-fit values. For the samplers, also assess convergence
and agreement of posterior constraints.
```

This produces a comparison for your likelihood and computing environment,
making it easy to work out which inference method is fastest and which
ones successfully find the best-fit reliably.

**Investigate a saved result**

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Load the saved Gaussian fit. Report the median and 68% credible interval
for sigma, plot its correlation with normalization, and inspect the
residuals for structure the model may have missed.
```

The assistant uses saved samples and the original data to reinspect an
already completed fit.

**Try it:** pick one of the three prompts above; you do not have to run all of them — and note the three-Gaussian fit is the first that takes real time, so say "use Nautilus instead" if you would rather not wait on Dynesty.

*Ask anything at this step — "what is a prior?", "why nested sampling?" — or say "teacher mode" for full explanations.*

## Your own project

The tour does not stop at the Gaussian. The same six steps run on your science, in this order — ask for any of them
directly if you would rather skip ahead.

**P0. Science context.** Start from a paper or from a plain-language description of what you measure and what you
want to infer, plus where your data lives and in what format. The assistant restates your problem in inference terms
— parameters, data, the shape of the likelihood — for you to correct.

PyAutoFit is domain agnostic: **you bring the scientific context**. The assistant ships with a statistics wiki 
covering Bayesian inference, priors, searches and model comparison. Its **literature wiki** at `wiki/literature/` 
is yours to populate with the papers that define your field and analysis.

Adding papers lets the assistant connect your natural language scientific descriptions to its inference: what 
parameters mean, which assumptions are conventional, how previous studies approached the problem, and what might 
complicate the interpretation of a result.

To add a paper, simply ask:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Ingest this paper into the literature wiki: [arXiv ID, link or local PDF].
Summarise its model, likelihood, priors and main conclusions, and explain
how it relates to the analysis we are developing.
```

The wiki builds a lasting reference for your project, so scientific context is available alongside your code and 
results. As you add relevant papers, the assistant can draw on them to frame decisions, cite prior work and identify 
caveats worth investigating.

**P1. Model.** Your parametrisation, described in words, becomes a PyAutoFit model with explicit priors, and
`model.info` shows you exactly what will be fitted. Describe it differently and the model changes with it.

**P2. Likelihood.** If you already have likelihood code, it stays yours: the assistant wraps it and checks it
returns the same numbers, never re-parametrising or "fixing" your science. If you do not, it builds a simple one
from your description. Either way your real data is plotted and discussed — unmodelled data pathologies are the
first source of biased inference, so this step is not optional. Already have the code? See [Bring Your Own Likelihood (BYOL)](#bring-your-own-likelihood-byol) below.

**P3. Search.** Runtime budget, whether your likelihood is JAX-differentiable, and whether you need the Bayesian
evidence pick the sampler between them. You get a recommendation with the reason, not just a name.

**P4. Fit and results.** Nothing is fitted until you give the go-ahead. Then the search runs, the output folder is
toured while it does, and the results are plotted and read back to you. There is no truth to check against on real
data, so the check becomes the residuals and the shape of the posterior.

**P5. Save and organise.** When the analysis is worth keeping, it can become a **science project** of its own.

When you begin a scientific study, `autofit_assistant` can create a dedicated **science project**: a structured folder linked to a GitHub repository containing your data, model and likelihood code, prior and search configurations, results, plotting scripts, and a record of your work with the assistant.

The assistant documents the analysis scripts, which can be converted into Jupyter notebooks with explanations as Markdown cells and Python as executable code cells. Collaborators can inspect the project, understand the assumptions behind each fit, reproduce results and extend the analysis with their own assistant.

Projects can also connect to configured HPC facilities for bidirectional synchronisation, job submission and monitoring, supporting larger datasets and more demanding inference workflows. If the study leads to a paper, the repository can become its **open-source companion**, bringing together the scientific assumptions, inference workflow and results needed to reproduce and build on the work.

To begin, include a request like this in your prompt:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Start a science project using my likelihood code and dataset at [paths].
Set up an initial fit, record the model assumptions and priors, and organise
the project so we can compare alternative models and share the results
with collaborators.
```

**P6. Extend.** Model comparison, sampler comparison, chaining searches into a pipeline, hierarchical models over
many datasets — the PyAutoFit
[Scientific Workflow](https://pyautofit.readthedocs.io/en/latest/overview/scientific_workflow.html) and
[Statistical Methods](https://pyautofit.readthedocs.io/en/latest/overview/statistical_methods.html) pages describe
what is available, and you can ask for any of it the same way.

*Ask anything at this step — "what is a prior?", "why nested sampling?" — or say "teacher mode" for full explanations.*

Everything above was natural language. You did not write a line of Python — though the assistant saved you the
scripts anyway, one per step, so you can read, re-run and modify them yourself.

### Bring Your Own Likelihood (BYOL)

Already have a likelihood function for your science problem? **Point the assistant at your existing code and it can set it up with PyAutoFit** — defining the model, choosing priors with you, configuring a search and organising the results:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Set up PyAutoFit with my existing science project. An example likelihood
function can be found at [GitHub link or local directory].

First, give me an overview of my project and likelihood function. Compose
an appropriate model, explain it to me, and recommend a non-linear search
(for example MCMC, nested sampling or maximum-likelihood estimation).

Do not begin inference until we have discussed the setup and I give you
the go-ahead.

Once inference is running, explain how the results are written to disk and
show me how to inspect and interpret them with PyAutoFit.
```

This prompt launches **BYOL mode** ([`modes/byol.md`](modes/byol.md)) — Bring Your Own
Likelihood, in the spirit of Bring Your Own Bottle: you bring the likelihood, the assistant
brings the inference, one stage per turn and nothing fitted until you give the go-ahead.

Your existing science code remains the source of the likelihood. With PyAutoFit built around it, you can perform inference through natural language while gaining access to features such as flexible priors and model composition, MCMC and nested sampling, automated result handling, model comparison and scalable workflows.

## Teacher mode and HowToFit

For users less familiar with Bayesian inference and scientific analysis you may wish to read through
the **HowToFits** lectures. These teach you the basic principles of Bayesian inference, with the
content pitched at undergraduate level and above.

The lectures are available in the [standalone HowToFit repository](https://github.com/PyAutoLabs/HowToFit).

If you're new to statistical inference and are not totally sure what concepts like a model, likelihood or
sampling are, you can use **teacher mode** to have the assistant explain concepts in more detail. Simply
start a prompt with "Teacher mode." and ask questions:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Teacher mode.

I'm new to PyAutoFit and want to learn the basic workflow end-to-end. Fit the
bundled 1D Gaussian dataset in dataset/gaussian_x1/ and recover its input
parameters.

Explain what each step is doing and why as we go: composing the model, choosing
the priors, picking the non-linear search, and how to read the posterior. So I
come away understanding the workflow, not just the commands.
```

## License

The assistant ships agent instructions and reference material derived from the public
PyAuto\* repositories. The underlying libraries are released under their own licenses
(see each repo).

<sub><i><a href="https://open.spotify.com/track/6LeTQu4NvTnLRRiB8GVFQe">if you don't know, don't worry</a></i></sub>
