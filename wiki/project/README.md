# wiki/project/

A running journal for *this clone* of `autofit_assistant`. Two things live here:

- [`profile.md`](./profile.md) — **one** living file describing who's working on this
  clone, their scientific domain, and what they're doing. Built up incrementally as the
  agent picks up cues from conversation. Light-touch: the agent only writes when it
  learns something durable (level, domain, science goal). The template is
  [`_profile_template.md`](./_profile_template.md).
- **Dated entries** — `YYYY-MM-DD-<slug>.md`. Every meaningful session — a modeling
  decision, a prior change, a sampler swap, a result interpretation, a paper ingested —
  gets one entry here.

## File naming

```
YYYY-MM-DD-<short-slug>.md
```

Examples:

```
2026-07-12-first-lightcurve-fit.md
2026-07-13-tightened-depth-prior.md
2026-07-14-evidence-comparison-two-planet.md
```

If two entries land on the same day, suffix one with `-2`. Keep the slug short — five
words at most.

## How an agent should use this folder

**Profile (`profile.md`).** On session start, read it if it exists. Use it as context
for adaptive-depth decisions (see `skills/_style.md` "Adaptive depth") **and as the
primary record of the user's scientific domain** — the profile is what makes a fresh
session domain-aware without re-interviewing the user. When the user volunteers
something durable that the profile doesn't already record (or that contradicts a
recorded fact), update the profile and bump `last_touched`. **Do not create
`profile.md` reflexively** — wait until the user has volunteered something durable. If
`last_touched` is older than ~10 sessions, ask the user whether anything has changed
before relying on it.

**Maintainer mode skips profile capture.** When `.maintainer` exists at the repo root,
the agent is editing the assistant itself, not doing science — see `AGENTS.md`
"Maintainer mode".

**Dated entries.** When you finish a piece of work that the user will want to recall
later, ask:

> Want me to add a `wiki/project/` entry summarising this?

Default to **yes** for: a new fit decision, a prior or model change, a non-trivial bug
encountered, a result the user wants to come back to, a paper ingested. Default to
**no** for: typo fixes, comment edits, exploratory throwaway scripts.

When the user says yes, copy [`_template.md`](./_template.md), fill it in, and commit
alongside the work it describes. The entry must cover:

1. **Domain motivation** — what science question this work is in service of.
2. **Statistical motivation** — what's being inferred, and how (search, priors,
   likelihood shape).
3. **Implementation choice** — the script(s) produced and the key decisions.

Cross-link every named concept and model into `wiki/core/` and `wiki/literature/`
using `[[wiki-link]]` slugs.

## How to read this folder

If the user asks **"what have we done on this project?"** or **"have we tried X
already?"**:

1. `ls wiki/project/` — chronological order via filenames.
2. Skim recent entries first.
3. `grep` for dataset names, model names, or other concrete tokens to find old
   decisions on the topic.

The journal is the project's memory across sessions. Treat it as part of the
context-gathering step, like reading `AGENTS.md`, the relevant `core/` pages, and
`profile.md`.
