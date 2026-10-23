# PyAutoFit Assistant

<img src="https://github.com/Jammy2211/PyAutoLogo/blob/main/gifs/pyautofit.gif?raw=true" width="900" />

**Bring your models, data and likelihood code. Perform scientific inference through conversation.**

**PyAutoFit** is a Python library for fitting models to data: you describe a model, say how it compares with your
data, and a search (nested sampling, MCMC or an optimiser) infers its parameters and their uncertainties.

This repository is the **PyAutoFit Assistant**: an AI assistant which **lets you use natural language** to do
statistical inference in your own field of science.

## Getting Started

The assistant runs inside an **AI coding agent**, a tool that can read this repository, run Python on your computer
and look at the results. Pick your agent:
[Claude Code](https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md#claude-code-recommended-paid) or
[Codex](https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md#codex-recommended-paid) are
recommended, and [GitHub Copilot CLI](https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md#github-copilot-cli)
or [OpenCode](https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md#opencode) are free AI options
if you want to try it without paying.

Once it is installed, open your AI coding agent and paste in the starting prompt below. The assistant installs
**PyAutoFit** for you, so there is nothing else to set up.

### Starting prompt

If you've not used the PyAutoFit Assistant before, use the prompt below. It starts a guided tour that you drive one
step at a time, typing each prompt yourself.

<sub><b>Starting prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
I want to perform scientific inference with PyAutoFit (https://github.com/PyAutoLabs/PyAutoFit) and the
autofit_assistant (https://github.com/PyAutoLabs/autofit_assistant).

Begin the "start here" guide for a new user.
```

The tour runs in two parts:

- **The bundled 1D Gaussian.** Six steps: compose a model, define a likelihood, choose a search, fit and read the
  result, save and reload it, then extend the workflow. You'll find out for yourself that the whole workflow is
  natural language.
- **Your own science.** A paper or a plain-language description of what you measure, then your model, your
  likelihood, a search chosen for your problem, the fit and the results.

You can stop and ask "what is a prior?" at any step without losing your place. Want to read ahead? The six steps are
written out, with every prompt, on [The tour, step by step](docs/tour.md).

Already have likelihood code? The [Bring Your Own Likelihood](#bring-your-own-likelihood-byol) prompt below is the
other way in, starting from your function instead of the Gaussian.

## Customize Your Assistant

The assistant adapts its behaviour to suit your prompt:

- Want it to ask questions before each step, so you understand the analysis and make the choices? Ask it to guide you
  through the process.

- Want to discuss a model, choose priors or plan an analysis without running anything? Just say so in your prompt.

- Want it to complete a task end-to-end without consulting you? Tell it to **one-shot** the task.

### Teacher Mode

If you're new to statistical inference and aren't sure what a model, a likelihood or sampling are, ask the assistant
to use **Teacher Mode**. It explains each concept in more detail as you go. Start your prompt with "Teacher mode." and
ask your questions:

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

### HowToFit mode

The [HowToFit lectures](https://github.com/PyAutoLabs/HowToFit) teach the basic principles of Bayesian inference,
pitched at undergraduate level and above. You can work through them in either format:

- **[Jupyter notebooks](https://github.com/PyAutoLabs/HowToFit/tree/main/notebooks)** if you want to run the code.
  Follow the course's setup instructions, open a lecture in Jupyter Notebook and run its cells as you read.
- **[Markdown lectures](https://github.com/PyAutoLabs/HowToFit/tree/main/markdown)** if you want to read the
  explanations on GitHub without running code.

Paste this prompt into the assistant to begin:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Enter HowToFit mode.

I want to work through the HowToFit lectures. Show me where to find them
and how to use Jupyter Notebook or Markdown, then help me with questions
as I go.
```

Keep the assistant open alongside the lecture and ask anything: share the lecture and section, paste an equation or
code cell, or show it an error. It explains the concepts and code, helps you read the results and sorts out notebook
problems at your pace. You choose when to move on.

## Scientific Context

PyAutoFit works in any field, so **you bring the scientific context**. The assistant ships with a statistics wiki
covering Bayesian inference, priors, searches and model comparison. Its **literature wiki** (`wiki/literature/`) is
yours to fill with the papers that define your field and analysis.

Adding papers lets the assistant connect how you describe your science to the inference: what the parameters mean,
which assumptions are standard, how earlier studies tackled the problem, and what might complicate reading a result.
To add a paper, just ask:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Ingest this paper into the literature wiki: [arXiv ID, link or local PDF].
Summarise its model, likelihood, priors and main conclusions, and explain
how it relates to the analysis we are developing.
```

The more relevant papers you add, the better the assistant gets at framing decisions, citing prior work and spotting
caveats in your results.

## Your own project

After the Gaussian, the tour runs the same six steps on your own science: your context, model, likelihood, search, fit
and results. [Your own project, step by step](docs/your_own_project.md) walks through what happens at each one.

### Bring Your Own Likelihood (BYOL)

Already have a likelihood function for your science problem? **Point the assistant at your code and it sets
PyAutoFit up around it**, defining the model, choosing priors with you, configuring a search and organising the
results:

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

This starts **BYOL mode**, named in the spirit of Bring Your Own Bottle: you bring the likelihood, the assistant brings
the inference. It works one stage per turn and fits nothing until you give the go-ahead.

Your code stays the source of the likelihood and is never rewritten. With PyAutoFit built around it, you gain:

- **Flexible models.** Priors, model composition and constraints, all described in plain English.
- **Many searches.** MCMC, nested sampling and optimisers behind one interface.
- **Organised results.** Output saved to disk in a layout you can browse, reload and query.
- **Room to grow.** Model comparison and workflows that scale to many datasets.

## Science Project

When you start a real scientific study, ask the assistant to set up a **science project**. This is a tidy folder,
backed by its own GitHub repository, that holds everything for that study: your data, model and likelihood code,
prior and search settings, results, plotting scripts and a record of your work with the assistant.

- **Readable.** Every script the assistant writes is documented and can be turned into a Jupyter notebook.
- **Shareable.** Collaborators can open the repository to see the assumptions behind each fit, reproduce the results
  and build on the analysis with their own assistant.
- **Scales up.** The project can send jobs to an HPC cluster, keep its files in sync and track the runs.
- **Reproducible.** If the work becomes a paper, the repository is its open-source companion, so readers can rerun
  the analysis or start their own from it.

To start one, include a request like this in your prompt:

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Start a science project using my likelihood code and dataset at [paths].
Set up an initial fit, record the model assumptions and priors, and organise
the project so we can compare alternative models and share the results
with collaborators.
```

## Conversational Assistants

You can also talk to the assistant in an ordinary chat, by connecting this repository to ChatGPT or Claude through
their GitHub connector. This works well for asking questions, planning an analysis and discussing papers, but a chat
cannot run code or look at your data, so for fitting itself use a coding agent. The
[PyAutoLabs AI options page](https://github.com/PyAutoLabs/PyAutoScientist/blob/main/AI_OPTIONS.md#chat-instead-of-an-agent)
shows how to set it up.

## Benchmarks

How well does the assistant work with a given AI agent and model? To answer that fairly, some of the example prompts
are saved as fixed **benchmark prompts** in [`benchmarks/`](benchmarks/), each with a scoring rubric, so different
agents and models, or the same model on different days, can be compared on evidence.

**No run has been scored yet**, so nothing here is a measured performance claim for any agent or model. The protocol
is in [`benchmarks/README.md`](benchmarks/README.md).

## License

The assistant ships agent instructions and reference material derived from the public
PyAuto\* repositories. The underlying libraries are released under their own licenses
(see each repo).

<details>
<summary><sub>Note for AI coding agents</sub></summary>

If a prompt sent you here and you are not already inside this repository, clone it
(`git clone https://github.com/PyAutoLabs/autofit_assistant.git && cd autofit_assistant`), then read `AGENTS.md`
in full and follow it. Hooks and project settings do not load for a folder cloned mid-session, so run the code gate
yourself (`python autoassistant/audit_skill_apis.py --code "<snippet>"`) before running PyAutoFit code, and tell the
user in one line that relaunching the agent inside `autofit_assistant/` gives the full setup.

</details>

<sub><i><a href="https://open.spotify.com/track/6LeTQu4NvTnLRRiB8GVFQe">if you don't know, don't worry</a></i></sub>
