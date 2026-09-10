<!-- ARCHIVED 2026-09-10 — UNSUPPORTED. Conversational chat routes (ChatGPT / Claude chat with a GitHub
     connector, Claude Project knowledge) were retired when the assistants moved to an agentic-only support
     policy. This page is kept for reference only and is not maintained; the setup it describes is not a
     supported way to use the assistant. Use a coding agent instead — see the top-level README. -->

> **Archived and unsupported (2026-09-10).** This describes a retired conversational-chat route. See the
> [README](../../../README.md) for the supported agentic setup.

# ChatGPT — paid plans (GitHub sync)

Run the assistant inside ChatGPT on a **paid plan** (Plus/Pro/Team) by connecting this
repository through ChatGPT's GitHub connector. The assistant reads the repository directly,
always sees current content, and grounds every PyAutoFit symbol in the live API surface.

ChatGPT's connectors are **paid-plan only**, which is why this route has no free equivalent.

## Setup (~2 minutes)

1. In ChatGPT, open **Settings → Connectors** and connect **GitHub**. Authorise access to
   public repositories (this repo is public — you don't need to grant anything of your own).
2. Start a chat with this bootstrap prompt:

```text
Use the autofit_assistant repository: https://github.com/PyAutoLabs/autofit_assistant

Start by reading its front door:
https://raw.githubusercontent.com/PyAutoLabs/autofit_assistant/main/llms.txt

Follow its read order (AGENTS.md → skills/README.md → the relevant skill → wiki/) and
its API rules. First tell me whether you can actually read llms.txt — if you can't, say
so plainly and don't answer from memory.
```

**Naming `llms.txt` explicitly matters** — connectors do not reliably find it on their own,
and answers are markedly better when it is pointed there first. The final sentence is a
deliberate honesty check: if the assistant can't read the file, you want to know immediately,
not after it writes you a script from an old API.

## What it can and can't do

In chat the assistant does the thinking work — planning models, writing current-API scripts
for you to run, explaining concepts, reviewing errors and figures. It **cannot** run fits or
read your data files; for that, use a coding agent such as [Codex CLI](../../setup/codex_cli.md), which
shares your ChatGPT subscription.

## Your first prompt

You're set up — copy and paste this to start (the 1D Gaussian dataset ships with the
repository, so it works immediately):

```text
Use the autofit_assistant repository: https://github.com/PyAutoLabs/autofit_assistant

Start by reading its front door:
https://raw.githubusercontent.com/PyAutoLabs/autofit_assistant/main/llms.txt

Follow its read order (AGENTS.md → skills/README.md → the relevant skill → wiki/) and
its API rules. First tell me whether you can actually read llms.txt — if you can't, say
so plainly and don't answer from memory.

Then walk me through fitting the bundled dataset in dataset/gaussian_x1/ with a 1D
Gaussian: the model, the priors, the likelihood, the search, and how to read the results.
```
