# Claude chat — paid plans (GitHub connector)

Run the assistant inside claude.ai on a **paid plan** (Pro/Max/Team) by connecting this
repository through Claude's GitHub connector. The assistant reads the repository directly,
always sees current content, and grounds every PyAutoFit symbol in the live API surface.
The higher usage limits leave room for long modelling conversations, deep concept dives and
multi-script planning sessions.

## Setup (~2 minutes)

1. In Claude, open **Settings → Connectors** and connect **GitHub**. Authorise access to
   public repositories (this repo is public — you don't need to grant anything of your own),
   then attach `https://github.com/PyAutoLabs/autofit_assistant`.
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

**Prefer uploading to connecting?** Project knowledge is a fine alternative: create a Claude
Project and add `llms.txt` and `AGENTS.md` to its knowledge, then open with the same prompt.
On a paid plan the higher limits leave room for your own papers, data notes and analysis logs
in the same project knowledge.

## What it can and can't do

In chat the assistant does the thinking work — planning models, writing current-API scripts
for you to run, explaining concepts, reviewing errors and figures. It **cannot** run fits or
read your data files; for that, pair it with a coding agent such as
[Claude Code](claude_code.md), which shares your Claude subscription.

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
