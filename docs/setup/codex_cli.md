# Codex (coding agent — recommended)

OpenAI's coding agent (CLI, IDE extension and cloud), and one of the two **recommended,
thoroughly exercised** harnesses for the assistant (alongside [Claude Code](claude_code.md)). It
reads the assistant's canonical instructions (`AGENTS.md`) directly, and can install PyAutoFit,
run fits end-to-end and inspect the results. The tracked `.codex/hooks.json` registers the
assistant's API gate and end-at-deliverable guard. Open `/hooks` after cloning (and after that
file changes) to review and trust its exact current hash; Codex skips untrusted project hooks.
The separate Claude remote-session Python bootstrap is intentionally not registered for Codex,
so continue to use `source activate.sh` for local development setup.

**Access.** Codex is included with paid ChatGPT plans (Plus, Pro, Business, Edu and Enterprise —
the last three are the usual institutional routes) and can also be used with an OpenAI API key on
usage-based billing. Whether a Free-plan allowance exists has changed over time and could not be
re-verified against the official pricing page when this page was last revised (2026-09-10);
check [OpenAI's Codex pricing page](https://developers.openai.com/codex/pricing/) for the current
position rather than relying on this page. Sustained scientific use should be budgeted as paid
access.

## Setup

1. Install Codex — follow the official instructions at
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

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Fit the bundled dataset in dataset/gaussian_x1/ with a 1D Gaussian.
Explain the model, priors, likelihood, search and results as we go.
```

New to Bayesian inference? Start the prompt with `Teacher mode.` and the assistant explains
the concepts as it goes — or just ask, the start-here tour takes questions at every step. You do
not have to let it run anything: ask it to plan the analysis and discuss the model and priors
before any search is submitted.

Experimental alternative if you cannot use Claude Code or Codex: [OpenCode](opencode_cli.md).
