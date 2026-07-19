---
name: af_adapt_to_domain
description: The domain-adaptation orchestrator — turn a fresh clone of this assistant into the user's own domain inference assistant. Runs a light interview about their field, data and conventions; drives the three adaptation channels (paper ingestion into wiki/literature/, likelihood wrapping, model composition); and records everything durable in wiki/project/profile.md so future sessions start domain-aware. Use when a user says "become my assistant for <field>", "adapt to my domain", "train yourself on my papers", or arrives with a new scientific domain the assistant hasn't recorded. Not for a single paper (af_ingest_paper) or a single wrap (af_wrap_likelihood) — this composes them.
user-invocable: true
---

# Adapting the assistant to your domain

A fresh clone of `autofit_assistant` knows inference, not your science. This skill closes
that gap deliberately: after it runs, the clone is *your* assistant — it can cite your
field's papers, respects your data conventions, knows your standard parametrisations, and
starts every future session from that knowledge instead of an interview.

Adaptation is **incremental and user-paced**, not a form. Run the channels the user's
situation calls for, in whatever order their material arrives; a partial adaptation that
grows over weeks is the normal case, not a failure.

## Orient — what adaptation writes, and where

| What is learned | Where it lives | Written by |
|---|---|---|
| The field, data shapes, conventions, goals | `wiki/project/profile.md` (led by its **Scientific domain** section) | this skill, incrementally |
| The field's literature | `wiki/literature/` (concepts, entities, sources, BibTeX) | `af_ingest_paper`, per paper |
| The likelihood connection | an `Analysis` wrapper + `profile.md` "Likelihood & model code" | `af_wrap_likelihood` |
| The standard model + priors | a composed model (script/JSON) + optionally `config/priors/` defaults | `af_compose_model` |
| Decisions along the way | dated `wiki/project/` entries | every channel |

Nothing else. Adaptation never edits `wiki/core/` (that is the stack's reference, not the
user's), never touches the user's own code, and adds no new state stores.

## Ask — the interview (light, once)

Open with the smallest set that unlocks work; volunteer-first, never interrogate:

1. **The field, in their words** — and the two or three analyses they run most.
2. **The data** — formats, units, sizes, where it lives, known pathologies (the
   data-inspection gate will ask about these per-dataset anyway; here it's the general
   shape).
3. **The starting material** — papers (PDFs/arXiv IDs)? Existing likelihood code? A
   standard parametrisation? Whichever exists picks the first channel below.
4. **The goal** — learning the workflow (→ teacher-mode pacing) or production analysis?

Record the durable answers in `profile.md` immediately (copy
`wiki/project/_profile_template.md` if absent; the **Scientific domain** section is the
headline). Flag contradictions with existing entries rather than overwriting.

## Branch — channel 1: papers → the literature wiki

For each paper (or batch): run [`af_ingest_paper`](./af_ingest_paper.md) targeting **this
clone's** `wiki/literature/`. Early in adaptation most ingestions will *create* concept
and entity pages — that is by design; follow the schema in `wiki/literature/AGENTS.md`
and keep `index.md` growing into the domain's map.

Prioritise, don't hoover: the 3–5 papers that define the user's standard analyses beat
30 skimmed abstracts. After each batch, demonstrate the gain — answer one of the user's
domain questions *citing the new pages* — so they can judge whether the wiki now says
what they'd want a collaborator to know.

## Branch — channel 2: likelihood code → an Analysis

If the user has existing analysis code, run
[`af_wrap_likelihood`](./af_wrap_likelihood.md) — the single highest-value adaptation
step, because it makes every later session immediately runnable on their real problem.
Its validation step doubles as the assistant learning their conventions (parameter
order, units, sign conventions), which land in `profile.md`.

If they have *no* code yet, don't force this channel — a first analysis can be built
from `af_compose_model` + a simple built-in-style Analysis, and their code can arrive
later.

## Branch — channel 3: parametrisation → models and default priors

Run [`af_compose_model`](./af_compose_model.md) for their standard model(s). If a
parametrisation is truly standard for them, offer to write its priors into
`config/priors/` as project defaults (see
[[../wiki/core/stack/autonerves]]) and to serialise the composed model to JSON — both make
"the usual model" a one-liner in every future script.

## Combine — proving and closing the loop

Adaptation "done for now" looks like:

- `profile.md` reads like a colleague's briefing (domain, data, code, goal recorded).
- `wiki/literature/index.md` maps the field's core concepts, each page citing real
  papers.
- One **end-to-end validated fit** exists — wrapped likelihood (or composed model), a
  cheap search, results inspected via `af_load_results` — proving the pipeline, not the
  science.
- A dated `wiki/project/` entry summarises what the assistant now knows and what it
  still doesn't (the honest gaps list matters as much as the achievements).

Offer next steps by situation: a real analysis → `start-new-project` (the science moves
to its own repo, inheriting the adaptation via refer-back); more depth → further
ingestion batches; production runtime concerns → the HPC conversation
([[../wiki/core/operations/hpc]]).

**Honesty rule, restated** (`_style.md` voice rules): after adaptation the assistant
cites the user's wiki where it can — and *still says so plainly* when a question falls
outside what has been ingested, offering another ingestion round instead of bluffing.
