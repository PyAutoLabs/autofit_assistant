---
title: Project profile
type: profile
last_touched: YYYY-MM-DD
---

# Project profile

Captures who's working on this fork and what they're doing — recorded incrementally
over the course of conversations. Light-touch and freeform: not every field needs a
value, and the agent updates it only when it learns something **durable** (a level,
a domain fact, a science goal that the user has volunteered, not just guessed at).

To start a real profile, copy this file to `wiki/project/profile.md` and fill in
what you know. The agent will append to it as the conversation proceeds.

## Scientific domain

**The most important section of this profile.** PyAutoFit is domain-agnostic, so this
is where the assistant records *your* field: what you study, your data's shape and
units, the models and parametrisations standard in your area, and the conventions the
assistant should respect. Examples:

- "Supernova cosmology — Pantheon+ style distance-modulus fits; SALT2 conventions."
- "Exoplanet radial velocities; Keplerian orbit fits; data are (time, RV, error) CSVs."
- "Chemical kinetics — ODE-based rate models fit to concentration time series."

_unrecorded_

## Statistics background

One or two sentences on the user's prior exposure to Bayesian inference. Examples:

- "First encounter with Bayesian fitting — no prior coursework."
- "Comfortable with MCMC, new to nested sampling and evidence."
- "Teaches Bayesian methods; fluent in samplers and model comparison."

_unrecorded_

## PyAutoFit background

How familiar the user is with the PyAuto\* stack. Examples:

- "Never used."
- "Ran a HowToFit tutorial last year."
- "Day-to-day user; just started a new fork."

_unrecorded_

## Interaction mode

Durable preference for how the assistant should interact: `teacher` (learn the
workflow) or `assistant` (do the workflow — note a preferred autonomy level in prose
if it's durable). Leave unrecorded to let the assistant infer the mode from each
opening request. See `AGENTS.md` "Modes".

_unrecorded_

## Science goal

The current project's aim, in the user's words. Examples:

- "Constrain the two-planet model's evidence against the one-planet baseline."
- "Publishable posterior on the reaction rate constants by autumn."

_unrecorded_

## Likelihood & model code

Where the user's own code lives and how the assistant wraps it. Examples:

- "Likelihood in `my_analysis/likelihood.py::log_like(params, data)`; wrapped in
  `scripts/analysis.py`."
- "Pure PyAutoFit built-ins — no external code."

_unrecorded_

## Data inventory

What data exists and where. Examples:

- "One light curve CSV in `dataset/tess/toi-1234.csv`."
- "No data yet — will simulate via `af_simulate_dataset`."

_unrecorded_

## HPC access

Constraints on the user's High-Performance-Computing access — **constraints, not
secrets**. The assistant captures these by asking once, lightly, when cluster work
first comes up (not by demanding a config upfront). Connection details live in
gitignored config; SSH credentials live as host aliases in `~/.ssh/config`. **Never
record secrets here.**

- **Cluster / SSH host alias:** which cluster, by its `~/.ssh/config` alias.
- **Requires MFA?** yes / no.
- **Requires VPN?** yes / no.
- **Jump / bastion host?** none, or the alias of the relay host.
- **Agent-driven remote execution permitted?** yes / no.
- **Preferred automation level:** `prepare-only` (default) | `user-confirms-each` |
  `assistant-runs`.

_unrecorded_

## Decisions log

Links to the dated `wiki/project/YYYY-MM-DD-<slug>.md` entries that capture concrete
work done. Newest first.

- _no entries yet_

## How to update this file

The agent should append to or rewrite sections when the user volunteers something
**durable**. Bump `last_touched` in the frontmatter on every change. If a recorded
fact appears to contradict what the user says now, **flag it to the user** before
overwriting.

If `last_touched` is older than roughly ten sessions, ask whether anything has
changed before relying on the recorded facts.
