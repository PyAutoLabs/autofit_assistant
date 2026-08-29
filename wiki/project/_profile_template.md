---
title: Project profile
type: profile
last_touched: YYYY-MM-DD
---

# User profile

Captures **who** is working here — their field, background, how they want to be worked
with, and what their compute access allows. Recorded incrementally over conversations.
Light-touch and freeform: not every field needs a value, and the agent updates it only
when it learns something **durable** the user has volunteered, not guessed at.

**This file is about the user, not the project.** The science goal, the data on hand and
where the work got to belong to `state.md` (template: `_state_template.md`), which is
rewritten each session. The split matters because these facts are *portable*: the person
who starts a second project brings their domain, background, HPC access and automation
preference with them, and should not be asked for them twice — a new project seeds its
`profile.md` from the assistant clone's.

To start a real profile, copy this file to `wiki/project/profile.md` and fill in what you
know. The agent will append to it as the conversation proceeds.

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

## How to update this file

The agent should append to or rewrite sections when the user volunteers something
**durable**. Bump `last_touched` in the frontmatter on every change. If a recorded
fact appears to contradict what the user says now, **flag it to the user** before
overwriting.

If `last_touched` is older than roughly ten sessions, ask whether anything has
changed before relying on the recorded facts.
