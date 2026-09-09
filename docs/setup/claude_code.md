# Claude Code (coding agent — paid)

The **primary, most thoroughly tested** harness for the assistant. Claude Code is Anthropic's
command-line coding agent: it reads the repository's instructions through `CLAUDE.md`, runs
the code-gate hook that blocks stale PyAutoFit API written from memory, and can install
PyAutoFit, run fits end-to-end and inspect the results.

Normally requires a paid Claude subscription or metered API usage
([costs](https://code.claude.com/docs/en/costs)).

## Setup

1. Install Claude Code — follow the official instructions at
   [code.claude.com/docs](https://code.claude.com/docs).
2. Clone this repository and start the agent inside it:

```bash
git clone https://github.com/PyAutoLabs/autofit_assistant.git
cd autofit_assistant
claude
```

The assistant configures itself on your first prompt, and will install PyAutoFit for you if
it isn't already installed.

## Your first prompt

You're set up — copy and paste this to start (the 1D Gaussian dataset ships with the
repository, so it works immediately):

```text
Fit the bundled dataset in dataset/gaussian_x1/ with a 1D Gaussian.
Explain the model, priors, likelihood, search and results as we go.
```

New to Bayesian inference? Start the prompt with `Teacher mode.` and the assistant explains
the concepts as it goes.
