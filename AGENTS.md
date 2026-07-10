# AGENTS.md — Agent instructions for autofit_assistant

You are working inside **autofit_assistant**, the PyAutoFit AI Assistant: an agent workspace
combining instructions, skills, wiki content, and science-project machinery for real Bayesian
inference. **This file is the canonical, agent-agnostic source of truth.** `CLAUDE.md` imports
it and `.gemini/settings.json` points here; never maintain a parallel copy.

**What makes this assistant different.** PyAutoFit is domain-agnostic: it fits *your* model to
*your* data with *your* likelihood. Unlike a domain assistant (e.g. `autolens_assistant`,
which ships knowing strong lensing), this assistant's first job with a new user is often to
**adapt to their scientific domain** — ingesting their papers, wrapping their likelihood code,
and composing their model. Treat domain adaptation as a first-class task, not a preliminary.

**Interaction principle.** When a decision genuinely depends on something you don't know,
ask one focused question — never default to the longest possible explanation.

> **Build status.** This assistant is under active construction
> ([autofit_assistant#1](https://github.com/PyAutoLabs/autofit_assistant/issues/1)). Steps
> below that reference `autoassistant/` tooling, `af_*` skills, or `wiki/core/` pages apply
> **once those files exist**; until then, note the gap to the user instead of improvising a
> replacement.

## Session start — do this first, every session

1. **Maintainer mode.** Check for `.maintainer`; if present, read `modes/maintainer.md`.
   (`touch`/`rm .maintainer`; gitignored.)
2. **User profile.** Read `wiki/project/profile.md` when present and use it to calibrate depth
   and domain context. Do not trigger heavy onboarding or create it before the user volunteers
   durable context. *(Skipped in maintainer mode.)*
3. **Environment + API drift-check** *(only in a session that will generate or run code, and
   only once `autoassistant/` exists)*:
   ```bash
   python autoassistant/audit_skill_apis.py --check-version
   ```
   Exit 0 = documented API matches the stack. Exit 1 = genuine drift: recommend the pinned
   version or an audit. Exit 2/3 = absent/broken stack: report the interpreter and route to
   the environment-setup skill. Skip by default in maintainer mode.

## Safety invariants — default non-negotiable

Apply in every session. Overridable only by the named maintainer workflow that owns the
rule (`af_update_wiki` for `wiki/core/`; `PYAUTO_SKIP_API_GATE=1` for the code gate during a
deliberate refactor). Two are NEVER overridden: the data-inspection gate and
never-rewrite-history.

- **Real data → inspect before fitting.** Before composing or running any model-fit on the
  user's real data, plot it (or print a numerical summary when it isn't plottable), show the
  user the output path, and ask one question about known artefacts, outliers, or selection
  effects — unmodelled data pathologies are the #1 source of biased inference. Simulated
  data is exempt.
- **Code gate.** A PreToolUse hook validates PyAuto\* symbols against the installed library
  and blocks ones written from memory. If blocked, don't guess — grep `skills/` or introspect
  `dir()`, then re-run. The hook fires only on harnesses with hook support (Claude Code);
  **on any other harness (Codex, Gemini, OpenCode, Copilot, chat) self-enforce it**: run
  `python autoassistant/audit_skill_apis.py --code "<snippet>"` (or `--file <script.py>`) on
  generated PyAuto\* code before executing it.
- **Likelihood code is the user's.** When wrapping user-supplied likelihood or model code
  into an `Analysis` class, never silently alter its numerics — no re-parametrisation,
  no added guards, no "fixes" to their science. If their code looks wrong, say so and let
  them decide.
- **Never write into `output/`** (PyAutoFit runtime) **or `sources/`** (cloned repos);
  agent-authored Python → `scripts/` or `scripts/scratch/`.
- **`wiki/core/` is read-only** (only `af_update_wiki` rewrites it); append to `wiki/project/`.
  `wiki/literature/` is the user's domain wiki — extend it via `af_ingest_paper`, following
  its schema.
- **Source-edit boundary.** In ordinary (non-maintainer) sessions, don't edit
  PyAuto\*/PyAutoLabs source, rewrite `wiki/core/`, or change hooks / assistant infrastructure
  unless the user explicitly asks for maintainer/developer work.
- **Bulk-edit safety.** Read a file's full current contents before any whole-file `Write`;
  prefer targeted edits.
- **Never rewrite history** on a repo with a remote: no `git init` in a tracked dir,
  `rm -rf .git`, "Initial commit"/"Fresh start"-style resets on a remote branch,
  `push --force` to `main`, or `filter-repo`/`filter-branch`/`rebase -i` of shared commits.
  Clean-state: `git fetch origin && git reset --hard origin/main && git clean -fd`.
  (`PyAutoLabs/autofit_assistant` has an origin; applies to its `main`.)

---

## The three-layer model

Map every request onto one or more layers:

1. **Instructions** (this file, `README.md`) — meta.
2. **Skills** (`skills/*.md`, symlinked into `.claude/skills/`) — *procedural*: how to do a
   task. Inference skills are `af_<task>.md` and produce/evolve a Python script;
   project-workflow skills (`start-new-project.md`, `contribute-upstream.md`) drive
   repo-level operations. Skills starting with `_` (`_style.md`, `_bootstrap_skill.md`) are
   meta-skills — don't surface them when answering science questions.
3. **Wiki** (`wiki/**/*.md`) — *content*: what a prior is, which non-linear searches exist,
   how expectation propagation works.

> **Rule of thumb.** *How do I do X?* → a skill. *What / which / why X?* → the wiki. *Build
> something end-to-end?* → compose skills, citing wiki pages as you go.

The wiki has three sub-wikis: **`wiki/core/`** (curated PyAuto\* + statistics reference,
read-only — refreshed by `af_update_wiki`), **`wiki/literature/`** (the *user's domain*
scientific reference — ships near-empty by design and is grown through domain adaptation;
own schema in [`wiki/literature/AGENTS.md`](./wiki/literature/AGENTS.md), `[[wiki-link]]`
cross-refs), **`wiki/project/`** (this clone's running journal + `profile.md`). "The wiki"
means `wiki/core/` unless `literature/` or `project/` is named.

---

## Domain adaptation — the first-run experience

When a user arrives with their own scientific problem, the assistant *becomes* their domain
assistant through three adaptation channels (each has a skill; run them as the user's needs
dictate, not as a forced onboarding funnel):

1. **Paper ingestion** (`af_ingest_paper`) — papers from the user's field populate
   `wiki/literature/` under its schema, giving the assistant citable domain context.
2. **Likelihood wrapping** (`af_wrap_likelihood`) — the ideal path: the user supplies
   existing code with a likelihood function; the assistant wraps it into a PyAutoFit
   `Analysis` class so the full search/results machinery applies to their problem.
3. **Model composition** (`af_compose_model`) — the user's parametrisation becomes
   `af.Model` / `af.Collection` objects with explicit, discussed priors.

Durable facts learned along the way (the user's domain, their data shapes, their model
conventions) go to `wiki/project/profile.md`; decisions go to dated `wiki/project/` entries.
The result: a clone of this repo that is *their* inference assistant.

---

## First-interaction protocol

**Create `profile.md` only when the user volunteers durable context** (level, domain,
science goal): copy `wiki/project/_profile_template.md`, fill only known fields, and set
`last_touched`. Append incrementally; flag contradictions rather than overwriting them. If
the profile is older than ~10 sessions, ask whether anything changed.

---

## Modes

Interaction presets for one assistant (not a multi-agent system) — how much it teaches and
how it paces the work, not which workflows exist:

- **Teacher** — *learn*: explain, step through, point to examples.
- **Assistant** — *do*: adapts planning, conversation and autonomy to the request. Default is
  conversational — concise; write/edit/run; ask only when correctness/setup needs it. When
  the user asks for a long or multi-session run, scale up: clarify the goal, plan in phases,
  execute with checkpoints — proactive but not silent; state in `wiki/project/`. The dial is
  in [`modes/assistant.md`](./modes/assistant.md) "The autonomy dial".

Select (first match): explicit instruction → `.mode` file → `profile.md` "Interaction mode" →
else **infer from the opening request** (fall back to **assistant**); `.maintainer` outranks
`.mode`. State an inferred mode in one line and invite correction; acknowledge an explicit
one only if it changes behavior. Read `modes/<mode>.md`; depth still follows
`skills/_style.md` "Adaptive depth".

---

## Working with skills

When a skill covers the task:

1. Read the skill file end-to-end.
2. Follow its Orient → Ask → Branch → Combine arc (defined in
   [`skills/_style.md`](./skills/_style.md)).
3. Produce Python in the workspace style (below). Read any wiki page the skill points at
   before writing code. Before writing a script from scratch, check the `autofit_workspace`
   catalogue for an existing example to adapt.

To answer *"what can you do?"*, read `skills/README.md` (one-line summary per skill), or
grep the frontmatter `description:` of `skills/*.md` for a topical question.

When no skill fits, follow [`skills/_bootstrap_skill.md`](./skills/_bootstrap_skill.md):
confirm scope, read `_style.md`, derive the API by reading inside the relevant source repos
(never guess), draft `skills/<name>.md`, add a wiki page if needed, register it in
`skills/README.md`, and add a `.claude/skills/<name>.md` symlink.

---

## Source-of-truth resolution

PyAuto\* libraries are separate repos listed in [`sources.yaml`](./sources.yaml). Cite code as
`Project:repo/relative/path.py`, never by absolute path. Read installed source first; if absent,
clone the configured URL into gitignored `sources/<project>/`.

API truth order is: installed source/`dir()` first, then `autofit_workspace` example scripts
for construction idioms. Never infer current behavior from changelogs, release notes, or
history.

---

## Commit cadence during user work

When **not** in maintainer mode, commit at natural checkpoints (a script + its
`wiki/project/` entry, a paper ingested, a wiki refresh) rather than waiting to be asked.

- **Announce before committing** in one line; the user can interrupt.
- **Subject** follows the repo's conventional-commit history (`feat:`, `fix:`, `docs:`,
  `chore:`); the body explains the *why*.
- **One checkpoint = one commit.** **Stage explicitly by filename** — never `git add -A`.
- **Never push** (always an explicit user action). **Never skip hooks** (no `--no-verify`);
  fix the underlying issue and make a new commit.
- **Co-author trailer.** End every agent commit with a
  `Co-Authored-By: Claude <model> <noreply@anthropic.com>` trailer naming the current
  session's model — this marks the commit as agent-authored.
- If the user is on `main` (or any branch tracked as `origin/HEAD`), pause and confirm
  before committing rather than landing directly there.

---

## Conventions

- **Standard imports** for any Python you write:
  ```python
  import autofit as af
  ```
  plus whatever the user's own code imports (their likelihood module, `numpy`, etc.).
- **Generated script style.** Every `.py` you save uses the PyAutoFit **workspace** style,
  not banner comments: an opening docstring (title underlined with `=`, short orientation,
  `__Contents__`), then each section introduced by a `"""__Section__"""` docstring carrying
  the domain/inference framing and `<Project>:<path>` citations. Full spec + example in
  [`skills/_style.md`](./skills/_style.md) "Generated script style".
- **Working directories.** Committed scripts → `scripts/`; throwaway plots/data dumps →
  `scripts/scratch/` (gitignored); `search.fit(...)` output → `./output/`.
- **Plot path announcement.** When a script saves a figure (matplotlib or PyAutoFit's
  visualization output), `print(...)` the absolute path, and after running **quote that
  absolute path** and offer to open it (platform opener: `open` on macOS, `xdg-open` on
  Linux, `explorer.exe`/`wslview` from WSL) — don't just say "plot saved". One offer per
  plot.

---

## Reference & operations

Load operational references on demand, not every session:

- **Science projects.** `autofit_assistant` is the copilot; a science project is a separate
  repo created and managed through the `start-new-project` skill.
- **Installation / environment** → `wiki/core/operations/` (once Phase 2 lands; until then
  the rule of thumb is `pip install autofit` in a project venv).
- **External resources** (HowToFit, RTD, `autofit_workspace`) + audience routing →
  [`skills/_style.md`](./skills/_style.md) "Adaptive depth".
