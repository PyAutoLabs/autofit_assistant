# PyAutoFit Assistant

**PyAutoFit** is a probabilistic programming language for model fitting: you bring a model,
a dataset, and a likelihood function, and it delivers the full machinery of modern Bayesian
inference — non-linear searches, priors, posteriors, evidence, model comparison, and
database-backed result analysis.

This repository is the **PyAutoFit Assistant**: an AI assistant you talk to in natural
language to perform statistical inference *in your own scientific domain*. Describe your
data and your model, hand it your likelihood code, or discuss inference theory — the
assistant explains the statistics as it goes and writes runnable PyAutoFit Python
workflows that stay in your repo.

## What makes this assistant different

Domain assistants like [`autolens_assistant`](https://github.com/PyAutoLabs/autolens_assistant)
ship already knowing their science (strong gravitational lensing). PyAutoFit has no fixed
domain — **you bring the domain**, and one of the assistant's first jobs is to adapt to it:

- **Ingest your papers.** Point it at the key papers of your field and it builds a
  cross-linked literature wiki it cites when framing decisions.
- **Wrap your likelihood.** The ideal starting point: you have existing code that computes
  a likelihood. The assistant wraps it into a PyAutoFit `Analysis` class, and from then on
  every search, prior, and result-analysis tool applies to *your* problem.
- **Compose your model.** Your parametrisation becomes `af.Model` / `af.Collection`
  objects with explicit, discussed priors.

The result is a clone of this repo that is *your* inference assistant — fluent in your
domain, honest about the statistics, and leaving every analysis as a runnable script.

## Getting Started

### Recommended: work inside the repository

Clone the `autofit_assistant` repo:

```bash
git clone https://github.com/PyAutoLabs/autofit_assistant.git
cd autofit_assistant
```

Open a CLI coding-agent session inside that directory. This is the primary and most capable
way to use the assistant because the agent can read the full instructions, inspect data,
write scripts, run checks, and keep project state with you. Coding agents often require a
paid subscription or metered API account for sustained use, although limited free tiers and
organization or student access may be available.

| Interface | Support | Access and cost | Notes |
|---|---|---|---|
| **Claude Code** | Primary | Normally a [paid Claude subscription or metered API usage](https://code.claude.com/docs/en/costs). | Loads the canonical instructions through `CLAUDE.md`. |
| **Codex CLI** | Primary | A [limited free plan](https://developers.openai.com/codex/pricing/) may be available; paid plans or API billing provide more usage. | Reads `AGENTS.md` directly and can edit and run the project locally. |
| **Gemini CLI** | Supported | Offers [limited free quotas](https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/quota-and-pricing.md); subscriptions or usage billing provide higher limits. | Loads the repository instructions through `.gemini/settings.json`. |
| **OpenCode** | Supported | The client is open source; model-provider access may be free or paid. | Use it from the repository root so it can discover the project context. |
| **GitHub Copilot CLI** | Compatible | [Copilot Free](https://docs.github.com/copilot/get-started/plans-for-github-copilot) has limited usage; paid or organization plans are common. | GitHub documents direct support for root `AGENTS.md` instructions. |

```bash
claude        # alternatively: codex, gemini, opencode, or copilot
```

These agents load the project instructions automatically, so you do not need to paste a
large system prompt. If PyAutoFit is not installed in the active environment, the assistant
checks the setup and guides you through it. Then describe your science case or ask a
question — see the example starting prompts below.

### Browser and chat-only use

If you are more familiar with conversation-based AI assistants such as ChatGPT or Claude on
the web, you can still use `autofit_assistant`: give the assistant this repository's URL, or
paste `AGENTS.md` directly. This is effective for learning PyAutoFit, asking how to compose
models or configure searches, interpreting and debugging errors, and getting draft code.
However, it is not fully agentic: the assistant cannot inspect your local data, run the
code, or maintain a science project unless you provide the relevant files and outputs.

## Modes

The assistant works in two modes, and you never have to choose one — it **infers the mode
from your first message and tells you which it picked** (e.g. *"Mode: teacher — I'll explain
as we go."*). If it guesses wrong, just say so. To set the mode yourself, start your message
with it; to make a choice permanent, drop a `.mode` file in the repo containing `teacher` or
`assistant`.

- **Teacher** — *learn the workflow.* `Teacher mode: I'm new to Bayesian inference — how do I fit a model to my data?`
- **Assistant** — *do the workflow.* `Assistant mode: wrap my likelihood function and run a first fit.`

Assistant mode adapts how much it plans, talks, and acts to your request. By default it
works conversationally — doing each step with you and checking in before big decisions. Ask
for autonomy (*"take my likelihood, explore three model parametrisations, and compare their
evidence"*) and it plans in phases and runs with checkpoints instead. There is no separate
mode to manage: just say how hands-on you want to be.

## Example Prompt 1 using Teacher Mode: learn the inference workflow end-to-end

A good first session if you're new to PyAutoFit (or to Bayesian model fitting) and want to
learn the workflow on clean data with a known answer, so the focus stays on understanding
each step. The bundled dataset at `dataset/gaussian_x1/` is simulated from a single
Gaussian (its README records the truth to check against).

```
Teacher mode.

I'm new to PyAutoFit and want to learn the basic workflow end-to-end. Fit the
bundled 1D Gaussian dataset in dataset/gaussian_x1/ and recover its input
parameters.

Explain what each step is doing and why as we go: composing the model, choosing
the priors, picking the non-linear search, and how to read the posterior. So I
come away understanding the workflow, not just the commands.
```

## Example Prompt 2 using Assistant Mode: wrap your own likelihood

The assistant's defining task — turning *your* code into a fully-instrumented inference
problem.

```
Assistant mode.

I have a Python function that computes the log likelihood of my model given my
data — it lives in my analysis code and takes a parameter vector. Wrap it into
PyAutoFit: build the Analysis class around it, compose the model with sensible
priors (ask me about each parameter), run a first fit with a nested sampler, and
show me the posterior and the evidence.
```

## Example Prompt 3 asking Assistant Mode for Autonomy: a real cosmology analysis

For users who want to see how far the assistant can be pushed when **asked to run
autonomously**, on real data. The bundled dataset at `dataset/sne_cosmology/` holds the
Pantheon+ Type Ia supernova distance compilation (1701 SNe; see its README for
provenance, citations, and the deliberate diagonal-errors simplification).

```
Assistant mode.

Fit flat LambdaCDM to the Pantheon+ supernova distances bundled at
dataset/sne_cosmology/: select the Hubble-flow sample, write the
distance-modulus likelihood, compose the model with sensible priors on
Omega_m and H0, run a nested sampler, and report the posterior constraints
and the evidence. Then compare against a model with a free dark-energy
equation of state w, and tell me whether the evidence justifies the extra
parameter.

Plan the whole analysis first, execute it end-to-end, and record your
decisions in the project journal as you go.
```

## Example Prompt 4: adapt the assistant to your field

The assistant's defining workflow — for users who want it to become a long-term
collaborator in their own domain.

```
Assistant mode.

I work on [your field — e.g. exoplanet radial velocities / chemical kinetics /
epidemiology]. I want you to become my inference assistant for this domain.

Here are the three papers that define the analyses I run: [arXiv IDs or PDFs].
Ingest them into your literature wiki. Then interview me about my data formats,
my standard model parametrisations, and my priors, and record what you learn so
future sessions start from it. I also have existing likelihood code — wrap it
so we can fit my real data. Finish by proposing the first analysis we should
set up together.
```

## Science Project

**`autofit_assistant` is the copilot; a science project is a separate repo.** This repo is
the assistant you clone once — its skills, wiki, and tooling. Your actual science lives in a
**science project**: a separate, self-contained git repo for one analysis or paper, created
by `start-new-project`. The project holds your data, config, scripts, results, and a
`wiki/project/` journal; for the assistant's *skills and reference wiki* it **refers back to
this `autofit_assistant` clone** (cloning it on demand if absent), so there's one source of
truth and no drift. Quick exploration can happen inside this clone; a real analysis headed
for a paper gets its own project.

**Built to be shared.** The project repo is the collaboration surface: push it to GitHub and
a collaborator simply **forks or clones it and continues the work with their own
assistant** — the project refers back to `autofit_assistant` automatically, so they inherit
the same skills, reference wiki and safety rules it was built with, plus your full decision
journal. And when the paper is ready, the same repo is its natural **open-source
companion**: the data (or its availability statement), the results, and every python script
that produced them, in one citable repo — hardened by a publish checklist and released with
a Zenodo DOI and `CITATION.cff`.

## Benchmarks

The example prompts above will ship as **frozen benchmark prompts** under `benchmarks/`,
with scoring rubrics and a small harness that records each run's conversation, results and
score — run them against different AI agents and models for an evidence-backed comparison,
exactly as `autolens_assistant` does today.

## Statistical Context

The assistant doesn't just know the PyAutoFit API — it ships with a **core statistics
wiki** at `wiki/core/` covering the inference concepts it uses on your behalf: priors and
model composition, the non-linear search landscape (nested sampling, MCMC, optimizers —
with a page per shipped sampler), initialization and search chaining, graphical models and
expectation propagation, evidence and model comparison, and posterior analysis. When the
assistant makes a statistical choice, it can point you at the page that explains it.

The **literature wiki** at `wiki/literature/` is intentionally different: it ships
near-empty, because it is *yours*. As you ingest the papers of your field, the assistant
gains the domain context to frame decisions, cite prior work, and spot when a result has
caveats — in your science, not someone else's.

## License

The assistant ships agent instructions and reference material derived from the public
PyAuto\* repositories. The underlying libraries are released under their own licenses
(see each repo).
