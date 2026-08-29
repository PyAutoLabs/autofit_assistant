# wiki/project/

The memory for *this clone* of `autofit_assistant`, and for any science project
scaffolded from it. Three things live here, and they answer different questions:

- [`state.md`](./state.md) — **where the work got to**: the head pointer a fresh session
  reads *first*. Science goal, data on hand, the user's likelihood and model code, where
  we are now, what is in flight (with output dirs / job IDs), what is carried forward,
  the traps not to repeat, and a one-line index of the journal. **Rewritten every
  session, never appended** — a head pointer that grows is a log, and there is already a
  log. Template: [`_state_template.md`](./_state_template.md).
- [`profile.md`](./profile.md) — **who you are working with**: their scientific domain,
  background, interaction mode, HPC access and authorization. A fact about the *user*, so
  it carries to their next project; the science goal is `state.md`'s, not this file's.
  Built up incrementally as the agent picks up durable cues. Template:
  [`_profile_template.md`](./_profile_template.md).
- **Dated entries** — `YYYY-MM-DD-<slug>.md`: **what happened, in order**. Every
  meaningful session — a modeling decision, a prior change, a sampler swap, a result
  interpretation, a paper ingested — gets one entry here, and it never changes once
  written.

A science project scaffolded by [`start-new-project`](../../skills/start-new-project.md)
also carries [`results_summary.md`](./results_summary.md) (the Publish phase's release
notes, template [`_results_summary_template.md`](./_results_summary_template.md)) and
`bibliography.md`.

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
**State (`state.md`).** Read it **first**, every session, before answering anything — it
is current by construction, because the previous session rewrote it. Then read the newest
dated entry for what that session actually did. Older entries are read on demand.

**Rewriting it is not optional and not appending.** At the end of a session, rewrite the
file so it describes the project *as it now is*: move a finished run out of "In flight"
into "Where we are now", drop the struck lines from "Open, carried forward", add the new
journal entry to the index. If you find yourself adding a dated section to `state.md`, you
are writing a journal entry in the wrong file.


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

> Want me to add a `wiki/project/` entry summarising this, and rewrite `state.md`?

Default to **yes** for: a new fit decision, a prior or model change, a non-trivial bug
encountered, a result the user wants to come back to, a paper ingested. Default to
**no** for: typo fixes, comment edits, exploratory throwaway scripts.

When the user says yes, copy [`_template.md`](./_template.md), fill it in, **then rewrite
`state.md`**, and commit both alongside the work they describe. **An entry is not finished
until `state.md` is current** — the entry is the record, `state.md` is what the next
session actually reads. The entry must cover:

1. **Domain motivation** — what science question this work is in service of.
2. **Statistical motivation** — what's being inferred, and how (search, priors,
   likelihood shape).
3. **Implementation choice** — the script(s) produced and the key decisions.

Cross-link every named concept and model into `wiki/core/` and `wiki/literature/`
using `[[wiki-link]]` slugs.

## How to read this folder

If the user asks **"what have we done on this project?"** or **"have we tried X
already?"**:

1. `state.md` — the answer is usually already there, including the traps list.
2. `ls wiki/project/` — chronological order via filenames; skim recent entries first.
3. `grep` for dataset names, model names, or other concrete tokens to find old
   decisions on the topic.

`state.md` plus the journal is the project's memory across sessions. Treat reading them as
part of the context-gathering step, like reading `AGENTS.md`, the relevant `core/` pages,
and `profile.md`.
