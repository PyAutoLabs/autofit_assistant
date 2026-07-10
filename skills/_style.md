---
name: _style
description: Writing guide for every workspace skill. Read first before adding or revising a skill. Defines tone (conversational, inference-first, encourages reading), structure (Orient → Ask → Branch → Combine), the five properties every skill must have, the python-first rule, and the source-citation form (project-name + repo-relative path).
---

# How to write a workspace skill

This file is a meta-skill: it does not help a user run an inference task directly. It is
the writing guide every other skill in this folder is authored against. Read it before
adding a new skill and re-read it before revising one.

## What a skill is

A skill is a single Markdown file at `skills/<name>.md`. It guides an AI agent through
one inference task — composing a model, wrapping a likelihood, running a search,
inspecting a posterior — and in doing so produces or evolves a **Python script** the user
can run. The deliverable is *understanding + a runnable script*, not a chat answer.

The agent reads the skill when activated (either by the user typing `/af_<name>` or by
the agent matching the skill's frontmatter `description` to the user's request).

## The five properties every skill must have

1. **Domain and statistical context first.** Before showing API calls, set both the
   user's science and the inference. *Why* are we fitting this model or running this
   search? *What is being inferred*, with what likelihood, what priors, what search?
   Because this assistant is domain-agnostic, the domain framing usually comes from the
   *user* (via `wiki/project/profile.md` and `wiki/literature/`) — a skill must actively
   pull that context in rather than staying abstract. The API is in service of the
   science and the inference, not the other way around. Both framings come before code —
   neither is optional.

2. **Encourage reading the wiki.** Every skill should point at relevant `wiki/`
   pages for the *what* (what is a prior, what is nested sampling, what is evidence).
   Skills are procedure; the wiki is content. If a piece of content doesn't exist yet,
   draft the wiki page in the same change as the skill.

3. **Conversational tone, invites questions.** Talk to the user the way a postdoc
   collaborator would. Ask what they want before doing it. After explaining a concept,
   invite a follow-up. Don't narrate procedures (`Step 1. Step 2.`) when prose works.

4. **Skills compose.** Each skill should leave breadcrumbs to other skills that build on
   it. Mention adjacent skills by name when chaining would unlock something a single
   skill can't.

5. **Records work to the project wiki.** When a skill produces or evolves a non-trivial
   script, the agent must offer (default-yes) to add a dated
   `wiki/project/YYYY-MM-DD-<slug>.md` entry covering (a) *domain motivation* — what
   science question this is in service of, (b) *statistical motivation* — what's being
   inferred and how, (c) *implementation choice* — the script produced and the key
   decisions. Cross-link every named concept and model into `wiki/core/` and
   `wiki/literature/` using `[[wiki-link]]` slugs. Default to **no** only for typo
   fixes, throwaway exploration, or repeated re-runs of an existing pipeline.

## Python-first

This is the rule that distinguishes the workspace from a tutorial workspace.

- Every skill's main deliverable is a Python script written *for this user's data and
  model*.
- The skill body contains the API recipe inline, in fenced ```python``` blocks.
- The skill should leave the user with a `.py` file in `scripts/` they can re-run and
  modify themselves.
- Do **not** just point the user at a pre-existing script in another repo. If you
  reference an example (e.g. inside `autofit_workspace`), say so as a citation but
  produce the user-specific script in the working directory regardless.

## Generated script style

Every Python script the agent saves — whether to `scripts/` or `scripts/scratch/` — follows
the PyAutoFit **workspace** style, not ad-hoc banner comments. It is the same style used by
every script in `autofit_workspace/scripts/` (canonical example:
`autofit_workspace:scripts/overview/overview_1_the_basics.py`), and it exists for two
reasons: it keeps the science and inference narrative inline with the code, and it makes
the script mechanically convertible to a Jupyter notebook — each top-level `"""..."""`
block becomes a markdown cell and the code between blocks becomes a code cell.

Two rules.

The level of detail in a saved script is **mode-invariant**. Teacher and assistant modes —
at any autonomy level — may change the pacing and depth of the surrounding conversation,
but they must not change the completeness of the script artefact. Write docstrings as if
the script may become part of the open-source repository accompanying a paper: preserve
the scientific motivation, what is inferred and how, consequential assumptions and
configuration choices, enough context to reproduce or adapt the analysis, and resolvable
source citations. Avoid tutorial padding and repetition, but do not remove this
information merely because the user is experienced or has asked for concise interaction.

**1. Title block + `__Contents__` header.** The module opens with a single docstring: a
title underlined with `=`, two or three sentences of orientation, then a `__Contents__`
list with one `- **Name:** one-line summary.` bullet per section that follows.

```python
"""
Model Fit: Transit Light Curve
==============================

Fit a single-planet transit model to the user's photometric light curve: load the data,
compose the transit model with priors discussed in-session, and fit it with a nested
sampler so the evidence supports later model comparison.

__Contents__

- **Imports:** Import autofit and the user's likelihood module.
- **Dataset:** Load the light curve and inspect it before fitting.
- **Analysis:** The Analysis class wrapping the user's likelihood.
- **Model:** Compose the model and its priors.
- **Search:** Configure the non-linear search.
- **Fit:** Run the fit and inspect the result.
"""
```

**2. Per-section narrative docstrings, not banner comments.** Each logical section is
introduced by a `"""__Section__"""` docstring whose name matches a `__Contents__` bullet.
The prose carries the domain and inference framing (property #1) and any source citations
(see below) — *not* `# ---` banner comments and *not* `# source:` lines.

Do this:

```python
"""
__Model__

The transit depth, duration and mid-time are free parameters with the priors we discussed:
depth is physically non-negative, so it takes a `LogUniformPrior`; the mid-time prior is
centred on the catalogue ephemeris. Model composition is handled by `af.Model`
(`PyAutoFit:autofit/mapper/model.py`).
"""
model = af.Model(TransitModel)
model.depth = af.LogUniformPrior(lower_limit=1e-5, upper_limit=1e-1)
```

Not this:

```python
# ---------------------------------------------------------------------------
# 1. Compose model
# ---------------------------------------------------------------------------
# source: PyAutoFit:autofit/mapper/model.py  (af.Model)
model = af.Model(TransitModel)
```

Short clarifying `#` comments *inside* a code block are still fine (e.g. annotating a
single prior). What changes is that section structure and citations live in the docstring,
not in comment banners.

## Source citations

Code references inside a skill must use the **project name + path relative to that
project's repo root**, resolvable via [`../sources.yaml`](../sources.yaml).

Good:

> See `PyAutoFit:autofit/non_linear/search/nest/nautilus/` for the search's default
> settings, and `wiki/core/concepts/non_linear_search.md` for when to pick it.

Bad:

> See `/Users/other/code/autofit/non_linear/search/nest/nautilus.py`.

The reason: this workspace is meant to be cloned to other machines. Absolute local paths
break the moment anyone else opens it.

The same `<Project>:<path>` form is used in **generated scripts**, but there it belongs
inside the section docstring prose (see "Generated script style" above) — woven into the
sentence that explains what the call does, never as a standalone `# source:` comment
banner.

## Adaptive depth

Adaptive depth governs the conversation and teaching around a script; it does not reduce
the publication-quality docstring detail required by "Generated script style" above.

Users arrive with different backgrounds. The same skill needs to serve all of them:

- **The inference newcomer.** Knows Python and their own science, but hasn't done formal
  Bayesian model fitting before. Doesn't yet know what a prior, a posterior, or a
  non-linear search is. Frame the statistics each time a new concept appears; lean
  heavily on the wiki.
- **The PyAutoFit newcomer.** Statistically fluent — priors, evidence, samplers hold no
  mystery — but new to the API. Map straight from inference question to object; skip the
  statistics lecture.
- **The returning user.** Has used PyAutoFit before. Just wants to load a result and
  inspect the posterior. Quick API recall, no lecture.

Pick depth from cues in the user's question. *"I've never done Bayesian fitting"* →
newcomer. *"How do I get the evidence out?"* → already knows inference. *"Load
`output/.../abc/`"* → returning user. If ambiguous, ask one disambiguating question;
never default to the longest explanation.

Read `wiki/project/profile.md` if it exists — that's the persistent record of the user's
level, domain and goal, built up over sessions. If it disagrees with what the user just
said, trust the user and update the profile.

### Resource routing by audience

The three external resources cover different audiences. Match the user's level to the
source:

| Audience | Lead resource | Secondary |
|----------|---------------|-----------|
| Inference newcomer | **HowToFit** lecture notebook — *surfaced before the code block, not after* | RTD overview |
| PyAutoFit newcomer (statistics-fluent) | **RTD** overview + cookbooks | Workspace example script |
| Returning PyAutoFit user | **Workspace** script for the task | RTD API reference |

Never dump all three on the user unprejudiced — pick one to lead, optionally cite a
second.

### Newcomer mode

When the user signals they're new to Bayesian inference — *"I've never fit a model like
this"*, *"can you explain what a prior is?"* — the agent shifts into a more pedagogical
shape. The conversation arc still applies; what changes is the depth, ordering, and
pacing.

1. **Lead with the HowToFit notebook.** Before any code block, surface the relevant
   tutorial. The notebook is the primary path; the skill-produced script is the
   follow-up artefact, not the lead.
2. **One concept at a time.** Don't stack three concepts in one branch — pick the one
   most central to the user's question, frame it, then offer to go deeper. *"Let's get
   the likelihood clear first; once that lands we can move on to priors"* beats firing
   all three simultaneously.
3. **Statistical framing → domain framing → code.** Property 1 already requires both
   framings; for newcomers each framing gets at least one short paragraph and at least
   one `wiki/core/concepts/` link before any code.
4. **Check-in beat after each concept.** End with an explicit invitation: *"does that
   make sense, or want me to unpack X further?"*. Don't barrel into the next branch.
5. **Encourage running HowToFit themselves.** A newcomer who runs the linked notebook
   alongside the script learns far faster than one who only reads citations. Mention
   this once per session.

Newcomer mode is a default for the inference-newcomer audience, not a separate state.
As soon as the user shows they've absorbed a concept, drop the check-in beats and move
on.

## The conversation arc — Orient → Ask → Branch → Combine

Structure every skill as a conversation, not a checklist.

**Orient.** When the skill activates, give a short opening: what this task is
statistically, what the user is about to do, the most relevant wiki page, and one
concrete example tailored to what they mentioned — ideally *their* domain, pulled from
`profile.md` or `wiki/literature/`. Two short paragraphs at most.

**Ask.** Before writing code, ask what the user wants out of the task. *"Do you want the
posterior for this model, or are you ultimately comparing it against an alternative?"*
The answer chooses the branch and lets the skill calibrate depth. Skip this step only
when the user has already told you.

**Branch.** Each sub-task lives in its own narrative branch. A branch has four parts:

- Statistical framing (one or two sentences, scaled to the user's depth).
- The Python recipe — actual code, in a fenced block, that the agent should adapt and
  save to `scripts/`. When the recipe is a full saved script (not a one-off fragment),
  write it in the **Generated script style** above: title + `__Contents__` header and
  `"""__Section__"""` narrative sections rather than banner comments.
- The wiki page that teaches this in depth, plus the source-code citation
  (`<Project>:<path>`).
- An invitation to dig deeper.

**Combine.** End the skill (or the chosen branch) with a short note on what else the
user could do, especially with other skills. *"Once the fit is running, feed the output
into `af_load_results` to inspect the posterior and the evidence."*

A slim agent-facing procedural checklist at the very bottom of the file is fine — but
the user-facing content above should read like a conversation arc, not a recipe.

## Voice rules

**Do**

- Speak in second person. The user is the protagonist.
- Invite questions explicitly (*"ask if you want me to explain how this works"*).
- Tie at least one concrete example to the user's domain when it is known.
- Point at the wiki by relative path every time you teach a concept.
- For newcomers, surface the relevant HowToFit notebook before the code block, not
  after. See "Newcomer mode" in Adaptive depth above.
- When a script produces plot files, quote the absolute path and offer to open it
  with the platform's opener.

**Don't**

- Don't open with a numbered procedure.
- Don't dump a wall of links — one or two per concept, chosen for relevance.
- Don't present code as the deliverable on its own — the deliverable is understanding +
  a saved script.
- Don't adopt a "just run this for me" tone. The user is here to do inference with the
  agent's help; gently route requests for black-box automation back through the wiki
  and existing skills.
- Don't invent domain knowledge. When the user's field is unfamiliar and
  `wiki/literature/` is silent, say so and offer `af_ingest_paper` — never bluff a
  citation or a domain convention.

## Frontmatter

Every skill file starts with YAML frontmatter:

```markdown
---
name: <kebab-case-name>
description: <one paragraph the agent reads when deciding whether to activate this skill>
---
```

The `description` is what the agent uses to decide when the skill applies. Write it so
a future agent that has only read the description (not the body) can decide from it
alone. Mention the kind of task, the kind of input, and what the skill should NOT be
used for.

## When a skill needs new wiki content

If you cannot point at a wiki page that explains a concept your new skill uses, draft
the wiki page in the same change. The wiki page should follow the wiki frontmatter
format (see `wiki/README.md`) and cite source code by `<Project>:<path>`.

The reverse is also true: don't write a wiki page nobody references. The wiki exists to
back up the skills.

## Plot output and path announcement

PyAutoFit problems are the user's own, so plotting is usually plain matplotlib (or the
user's own plotting code) plus PyAutoFit's search/result visualization output. Three
rules:

1. **Save figures to a deterministic path** under `scripts/scratch/<context>/` (the
   `<context>` slug is usually the dataset or model name). Never rely on interactive
   display — the user is often running the script from a terminal where `plt.show()`
   flashes and vanishes.
2. **`print(...)` each plot's path** at the end of the Python recipe so the absolute
   location lands in stdout — `print(f"Saved to: {PLOT_DIR.resolve()}")` once per branch.
3. **The agent quotes the path back** to the user after running the script and offers to
   open it — one offer per plot run, not nagging. Use the platform's opener: `open` on
   macOS, `xdg-open` on Linux, `explorer.exe` (or `wslview`) from WSL.

The full convention — committed Python lives in `scripts/`; throwaway plots and data
dumps go to the gitignored `scripts/scratch/` — is in `AGENTS.md` "Conventions". Skills
here are the application of that rule.

## External resource citation

Every `af_*` skill ends with a single `## Further reading` block above the agent
checklist (if present):

```markdown
## Further reading

- **Student / new to inference** — [HowToFit: <tutorial title>](<URL>): one line on
  what the tutorial teaches.
- **General reference** — [RTD: <page title>](<URL>): canonical PyAutoFit
  documentation page.
- **Experienced PyAutoFit user** — [workspace: <script name>](<URL>): production-style
  example to fork from.
```

Rules:

- Three bullets max, one per audience. Omit any with no canonical resource.
- The agent **picks one of the three to surface in the conversation** — the audience
  match comes from `wiki/project/profile.md` (or, lacking that, from the user's
  immediate cues). The other two stay in the block as references the user can fall
  back on.
- For non-`af_*` skills (project workflow, meta), this section is optional; include
  it only if a single external resource is the canonical reference.

## Iteration

This guide is the workspace v1 writing guide. As patterns emerge, update this file in
the same change as whatever motivated the update. Note the change at the top of that
PR description.
