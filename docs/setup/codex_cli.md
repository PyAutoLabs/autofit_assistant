# Codex (coding agent — recommended)

OpenAI's coding agent (CLI, IDE extension and cloud). It reads the shared
`AGENTS.md` instructions, and this repository exposes its canonical `skills/*.md`
through generated, project-level `.codex/skills/` adapters. Discovery was checked
with an installed Codex CLI; adapter validation and fixture guard tests cover the
setup, while scientific fits still need to be exercised in the user's environment.
See the [harness smoke record](https://github.com/PyAutoLabs/PyAutoBrain/blob/main/docs/agent_harness_smoke.md)
for the measured scope.

The tracked `.codex/hooks.json` registers the API and end-at-deliverable guards.
Review and trust its current hash in `/hooks` after cloning and after changes;
Codex skips project hooks until that hash is trusted. The separate Claude
remote-session Python bootstrap is not registered for Codex, so use
`source activate.sh` for local development setup.

**Access.** Check [OpenAI's Codex pricing page](https://developers.openai.com/codex/pricing/)
for current plans and API billing.

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
