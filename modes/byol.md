# Bring Your Own Likelihood (BYOL) mode

The door for a user who already has working science code. They point at a likelihood
function; the assistant reads it, restates it, composes the model around it, wraps it,
validates it, recommends a search, and — only after an explicit go-ahead — runs the fit and
shows them where the results live. **You bring the likelihood; the assistant brings the
inference.**

This file is a script for *you*, the assistant — what to say, what to show, where to stop —
not user-facing prose. BYOL adds **no capability**: it is
[`af_wrap_likelihood`](../skills/af_wrap_likelihood.md) driven through the six sentences of
the published prompt, one per turn.

## What changes

- **One stage per turn.** Do the stage, show the real output, append the footer, then **stop
  and wait**. Never run two stages in one turn, and never run ahead of the go-ahead.
- **The user's code leads.** Every stage is grounded in what their function actually does,
  read from their file — not in what a likelihood of that kind usually does.
- **Nothing is fitted before stage 5**, the prompt's own instruction; treat it as binding
  even when later messages sound impatient. Ask, don't assume.
- **Generated Python is kept**, in `scripts/` (or their science project) — they leave with a
  wrapper and a fit script they own, not a transcript.

## What stays the same

- Every `AGENTS.md` safety invariant, and one of them is the whole point of this mode: **the
  likelihood code is the user's** — never re-parametrised, never guarded, never "fixed"; if it
  looks wrong, say so and they decide. Also the data-inspection gate (their data is real), the
  code gate, the `output/` write-ban and the source-edit boundary.
- Saved Python is at full `skills/_style.md` "Generated script style" quality —
  mode-invariant.
- The skills are unchanged. This mode composes `af_wrap_likelihood` (the engine),
  `af_compose_model`, `af_configure_search`, `af_run_search`, `af_plot_fit`,
  `af_load_results`, plus `af_ingest_paper` and `start-new-project` at the hand-off; read
  the skill rather than restating it here.

## Composition

Depth follows `skills/_style.md` "Adaptive depth", entering at **PyAutoFit newcomer** — a
user with their own likelihood code is fluent in their science and usually in their
statistics, and new only to the API, so map straight from inference question to object. An
existing `wiki/project/profile.md` level is not overridden, and "teacher mode" at any stage
switches [`modes/teacher.md`](./teacher.md) on for the rest of the run without leaving BYOL.

## What triggers inference

The published BYOL prompt (below), or "byol" / "BYOL" / "bring your own likelihood" /
"wrap my likelihood" **together with a path or link to code** — outranking inference from
the rest of the opening request; `.maintainer` outranks it. If both the start-here prompt
and the BYOL prompt appear and code is pointed at, **BYOL wins**: the tour's Part 1 exists
to reach the place BYOL starts from.

---

## Trigger and posture

The published prompt — on this repo's `README.md` under "Your own project" — is:

```text
Set up PyAutoFit with my existing science project. An example likelihood
function can be found at [GitHub link or local directory].

First, give me an overview of my project and likelihood function. Compose
an appropriate model, explain it to me, and recommend a non-linear search
(for example MCMC, nested sampling or maximum-likelihood estimation).

Do not begin inference until we have discussed the setup and I give you
the go-ahead.

Once inference is running, explain how the results are written to disk and
show me how to inspect and interpret them with PyAutoFit.
```

Its four sentences are the six stages below, and every stage ends with the two-line footer
under "Teacher mode and questions". Before stage 1, run the session-start drift check
(`AGENTS.md` "Session start"): `python autoassistant/audit_skill_apis.py --check-version`.
Exit 0 — continue. Exit 2 or 3 — the stack is absent or broken: run `af_setup_environment`,
say so in one line, resume at stage 1. Exit 1 — report the drift and offer the pinned
version; the wrap can still proceed.

Honour **"skip to the fit"** only as far as stage 5: the go-ahead checkpoint is the user's
own instruction and is not skippable. Anything else may be skipped on request, always with a
one-line note of what was skipped.

---

## Stage 1 — Overview

*Skill:* `af_wrap_likelihood` ("Ask"). *No script yet.*

**Read the code they pointed at.** A GitHub link → clone into gitignored `sources/`
(`AGENTS.md` "Source-of-truth resolution") and read it there. A local path → read it in
place; never copy it into this repo.

**Restate it in one paragraph**, covering the four things that decide the wrapper's shape:

1. **What the function scores** — the forward model, and the data it is compared against.
2. **Signature and calling convention** — a parameter vector in fixed order, named
   arguments, a dict, an object? What does it return?
3. **Log likelihood or chi-squared**, and whether the **noise-normalisation constant**
   (`-0.5 * sum(log(2 pi sigma^2))`) is included — it does not matter for the posterior and
   it does matter for absolute evidence.
4. **Free parameters vs fixed configuration** — which arguments the search will vary, and
   which are constants of their setup.

Plus **what data it needs and how it is loaded**, including any selection cut the loader
applies: a cut is a scientific decision, so state it back rather than inherit it silently.

**Then ask them to correct it** — that paragraph is the contract for every stage below, and a
misread convention costs a sentence here and a whole run at stage 6.

## Stage 2 — Model

*Skill:* `af_compose_model`. *Script:* the model section of the wrapper script.

Compose `af.Model` (or `af.Collection` for several components) over a plain Python class
whose `__init__` arguments **mirror the free arguments** of their function — same names,
same units, their convention not yours.

Choose each prior **with** them, one line of reasoning each: a prior is a scientific
statement, not a default. Physical bounds (a density fraction in [0, 1]) are uniform;
order-of-magnitude ignorance is log-uniform; a published measurement is Gaussian.

Show `model.info`, and check the free-parameter count is the number they expected — a count
one too high usually means a fixed configuration value leaked into the model.

## Stage 3 — Wrap and validate

*Skill:* `af_wrap_likelihood` ("Branch — the wrapper", "Branch — validate before fitting").
*Script:* `scripts/<project>_analysis.py`, workspace style.

Write the `Analysis` subclass. It **imports** their module — never copies it — holds the
data in `__init__`, and implements `log_likelihood_function(self, instance)` as pure
translation: build their calling convention from named attributes of `instance`
(explicitly, never by attribute iteration order) and return their number unchanged.

Then the skill's three checks, on hand-built plain instances, before any search:

1. a known-good instance returns a **finite** float;
2. that value **equals their function** called directly with the same inputs (assert it);
3. a deliberately bad instance scores **worse** (assert it) — check 3 catches the sign
   flip, the most common wrapping bug and one a sampler will happily minimise their fit
   quality with.

**The data-inspection gate belongs here** and is never skipped: their data is real. Plot it
(or summarise it numerically if it is not plottable), announce the absolute path and offer
to open it (`_style.md` "Plot output and path announcement"), and ask **one** question about
known artefacts, outliers or selection effects. Time one likelihood call while you are here
— that number is stage 4's budget arithmetic.

## Stage 4 — Search

*Skill:* `af_configure_search`.

Recommend one search **with the reason**, not just a name:

- **evidence wanted** (model comparison now or later) → nested sampling;
- **posterior only** → MCMC, often cheaper;
- **a best-fit point** → an optimiser, accepting it returns a point, not a distribution;
- **likelihood is pure JAX** → gradient-based (`BlackJAXNUTS`, the `MultiStart*` optimisers).

Read the installed roster from the library, never from memory. State the expected runtime as
(measured cost per call) x (evaluations the sampler needs); if that lands in hours, offer the
HPC route rather than letting a laptop cook overnight. Ask the **JAX triage question once** —
"is your likelihood JAX-compatible, or worth making so?" — and record the answer; never
convert their code uninvited.

## Stage 5 — Go-ahead checkpoint

**Show a short table and then STOP.** Four rows, no more:

| | |
|---|---|
| **Model + priors** | free parameters and the prior on each |
| **Likelihood** | their function, its convention, the validation numbers |
| **Search** | the recommendation and its settings |
| **Expected runtime** | cost per call x evaluations |

Then, in one line: nothing runs until they say go. **Run nothing** — not a short trial, not a
test-mode fit — until they do; if they change something in response, revise the table and stop
again.

## Stage 6 — Run, then results on disk

*Skills:* `af_run_search`, then `af_plot_fit` and `af_load_results`.
*Script:* `scripts/<project>_fit.py`.

Launch the fit, then do the **output-folder tour while it runs** (`_style.md` "Output folder
announcement") — the absolute `output/<path_prefix>/<name>/<unique_id>/`, `model.results`
first, then `model.info`, `search.summary`, `files/` and `image/`, and the fact that they
update *as the search runs*. Say once that a completed search **reloads** rather than re-runs;
it surprises everyone once.

Then the second half of the prompt's last sentence — how to inspect and interpret:

- **The parameter table**: median-PDF values with 1-sigma errors, and the log evidence if
  the search reports one (flagging the missing noise constant if their function omits it).
- **`af_plot_fit`**: model-vs-data with residuals, and the corner plot, both with paths
  announced. Read the corner plot back to them — degeneracies, prior-edge pile-ups.
- **`af_load_results`**: reload through the aggregator without re-running, so the result
  outlives the session. Never compose an output path by hand.
- **The check.** Real data has **no truth** to compare against, so the check is the
  residuals — they should look like noise, and structure in them is model error. Say this
  explicitly; a user arriving from a simulated-data tutorial expects a truth row.

---

## Worked example — Pantheon+ supernova cosmology

A real BYOL run against `dataset/sne_cosmology/`, so the numbers below are measured rather
than illustrative. The user's module loads the Pantheon+SH0ES distance table, applies their
cuts (`z_hd > 0.023`, calibrators dropped — **1371** supernovae), and defines
`log_likelihood(params: dict, z, mu, sigma)` returning `-0.5 * chi2` for a flat LCDM distance
modulus with **no noise-normalisation term** — exactly the convention stage 1 must surface.
Stage 2 gave two free parameters: `omega_m` uniform on [0, 1] (a density fraction of a flat
universe) and `h0` uniform on [50, 100] km/s/Mpc (wide enough to hold both ends of the Hubble
tension).

Stage 3's validation, all three checks passing:

```bash
check 1 finite            : log L = -295.1774
check 2 equals user's fn  : -295.1774266904256 == user's function
check 3 bad scores worse  : log L = -1726.6421 < -295.1774
cost per likelihood call  : 0.19 ms
```

Stage 4 chose `af.DynestyStatic(nlive=75)`: the evidence is wanted for a later comparison
against free-curvature and free-`w` models, and the likelihood is plain numpy, so the JAX
searches are unavailable. At 0.19 ms per call the budget arithmetic predicted a
seconds-scale run, which is what happened.

Stage 6, **11.4 s** wall time and 3686 likelihood evaluations:

```bash
parameter        inferred (median, 1 sigma)      dataset README validation
---------------------------------------------------------------------------
omega_m            0.344 +0.021 / -0.019         0.344 +0.021 / -0.019
h0                73.11 +0.27 / -0.30           73.14 +0.27 / -0.32

log evidence: -302.40      max log likelihood: -295.16
residual scatter: 0.656 sigma
```

Read it back the way stage 6 says to: both parameters match the maintainer validation run
in `dataset/sne_cosmology/README.md`; there is no truth row because this is real data; and
the residual scatter below 1 sigma is the diagonal-errors approximation showing its hand —
the published analysis uses the full covariance matrix, the natural next wrap. The
aggregator reloaded the same medians and evidence from `output/` without re-running.

---

## Teacher mode and questions

Append this footer to **every** stage, verbatim:

> Ask anything here - "what is a prior?", "why nested sampling?" - and I'll explain before we
> move on. Say "teacher mode" for full explanations at every step.

- **A question never advances the stage.** Answer it, then re-offer the same stage. Only the
  user moving on — or, at stage 5, the go-ahead — advances anything.
- **"Teacher mode" mid-run** switches `modes/teacher.md` on for the rest of the run: more
  *why*, explicit assumptions, wiki and HowToFit pointers. The stages are unchanged; the
  depth around them grows.

## Hand-off

When stage 6 is done, or the user stops:

- One line: the session now runs in **assistant mode** (or **teacher mode** if chosen), and
  the one-stage-per-turn pacing no longer applies.
- Name what is on disk — the wrapper and fit scripts, the fits under `output/`, the figures.
- **Record the wrap** (`af_wrap_likelihood` "Combine", default-yes): the function, its
  convention, the validation numbers and where the code lives, into
  `wiki/project/profile.md` "Likelihood & model code", so a future session skips the stage-1
  interview. Follow `AGENTS.md` "First-interaction protocol" — **ask before creating
  `profile.md`**, and never create it in a maintainer clone.
- Where to go next: [`start-new-project`](../skills/start-new-project.md) to turn the
  analysis into a standalone science project repo,
  [`af_ingest_paper`](../skills/af_ingest_paper.md) for the domain context that makes prior
  choices citable, and the RTD
  [Scientific Workflow](https://pyautofit.readthedocs.io/en/latest/overview/scientific_workflow.html)
  and
  [Statistical Methods](https://pyautofit.readthedocs.io/en/latest/overview/statistical_methods.html)
  pages for what comes after one fit.

## Rules

- **The published prompt is byte-identical** across `README.md`, this file and any other
  surface that carries it — never paraphrase or reflow it.
- **Never fabricate output.** Every number, table and path shown comes from running the
  code. If a run fails, say so and debug it (`af_debug_fit_failure`); an invented result is
  this mode's one unrecoverable failure.
- **The invariant, restated:** the likelihood code is the user's. The wrapper translates and
  nothing else — no re-parametrisation, no guards, no silently added noise constant. Say
  what looks wrong; let them decide.
- **All `AGENTS.md` safety invariants apply**, code gate included: on a harness without
  hooks, self-enforce with `python autoassistant/audit_skill_apis.py --file <script>.py`
  before running generated code.
- **Generated Python goes to `scripts/`** (or the user's own science project) in
  `skills/_style.md` "Generated script style"; figures to gitignored `scripts/scratch/`,
  fits to `output/`.
