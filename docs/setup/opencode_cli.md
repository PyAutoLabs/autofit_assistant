# OpenCode (coding agent — experimental alternative)

[OpenCode](https://github.com/sst/opencode) is an **open-source** coding agent. The client is
free; you connect it to a model provider of your choice. It reads `AGENTS.md` from the repository
root, so the assistant's instructions, skills and wiki all apply, and it can install PyAutoFit,
wrap your likelihood, run searches and inspect results **if the model you connect can drive the
workflow**.

## What "free" does and does not mean

- **The client is free; the model is not OpenCode's.** Cost, capability, rate limits and
  availability belong to the provider you configure. OpenCode's own docs recommend new users start
  with its hosted provider (OpenCode Zen), which is pay-as-you-go with a handful of models offered
  at no cost — and OpenCode describes those free models as available *for a limited time*. Do not
  plan a project around a free model staying free.
- **Not every model can run the assistant.** The workflow needs a model that follows multi-step
  tool use reliably, does not hallucinate PyAutoFit API faster than the self-enforced audit can
  catch it, and can **look at figures** — checking a fit means inspecting the plots it wrote. Many
  free models have no image input, which rules them out for the full workflow.
- **Nothing is validated yet.** As of 2026-09-10 **no provider/model configuration has been
  tested against this assistant's benchmarks**, so there is no default free model to recommend.
  Treat OpenCode as *compatible* rather than *supported*; the evaluation protocol maintainers use
  is the sibling assistant's
  [`docs/evaluation/agent_evaluation.md`](https://github.com/PyAutoLabs/autolens_assistant/blob/main/docs/evaluation/agent_evaluation.md).

## Setup

1. Install OpenCode and configure a model provider — follow the official instructions at
   [github.com/sst/opencode](https://github.com/sst/opencode). Pick a model that supports **tool
   use and image input**; check the provider's model card, not the model's name.
2. Clone this repository and start the agent inside it (running from the repository root is what
   lets it discover `AGENTS.md`):

```bash
git clone https://github.com/PyAutoLabs/autofit_assistant.git
cd autofit_assistant
opencode
```

3. OpenCode has no PreToolUse hook, so the code gate is self-enforced: the assistant should run
   `python autoassistant/audit_skill_apis.py --file <script.py>` on generated PyAutoFit code
   before executing it. If the model skips this, ask it to.

## Your first prompt

<sub><b>Example Natural Language Prompt for Claude Code, Codex or other AI coding agent</b></sub>

```text
Fit the bundled dataset in dataset/gaussian_x1/ with a 1D Gaussian.
Explain the model, priors, likelihood, search and results as we go.
```

Then a quick capability check before trusting it with your own science: ask it to plot the fit
and *describe what it sees in the figure*. A model that describes the code instead cannot run
the full workflow.

Please [open an issue](https://github.com/PyAutoLabs/autofit_assistant/issues) with the
provider, model, date and what worked or failed — user reports are how a configuration
graduates from "compatible" to "tested".
