# Claude Code (coding agent — recommended)

The **primary, most thoroughly exercised** harness for the assistant. Claude Code is Anthropic's
coding agent (terminal, desktop app and IDE extensions): it reads the repository's instructions
through `CLAUDE.md`, runs the code-gate hook that blocks stale PyAutoFit API written from memory,
and can install PyAutoFit, run fits end-to-end and inspect the results.

**Access.** Claude Code is a paid product. Anthropic's [cost page](https://code.claude.com/docs/en/costs)
describes the routes: a Claude subscription (Pro / Max, or a Team / Enterprise seat through your
institution), usage-based billing through the Claude Console (API), or a cloud provider your
institution already uses (Amazon Bedrock, Google Cloud, Microsoft Foundry). Sustained inference
work is heavy use, so budget for it rather than assuming a personal subscription is the only or
best option.

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
the concepts as it goes — or just ask, the start-here tour takes questions at every step. You do
not have to let it run anything: ask it to plan the analysis and discuss the model and priors
before any search is submitted.

Experimental alternative if you cannot use Claude Code or Codex: [OpenCode](opencode_cli.md).
