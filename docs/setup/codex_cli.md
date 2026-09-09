# Codex CLI (coding agent — limited free / paid)

OpenAI's command-line coding agent, and one of the two **primary, thoroughly tested**
harnesses for the assistant (alongside [Claude Code](claude_code.md)). It reads the
assistant's canonical instructions (`AGENTS.md`) directly, and can install PyAutoFit, run
fits end-to-end and inspect the results.

A [limited free plan](https://developers.openai.com/codex/pricing/) may be available; paid
ChatGPT plans or API billing provide more usage.

## Setup

1. Install Codex CLI — follow the official instructions at
   [developers.openai.com/codex](https://developers.openai.com/codex).
2. Clone this repository and start the agent inside it:

```bash
git clone https://github.com/PyAutoLabs/autofit_assistant.git
cd autofit_assistant
codex
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
