# Start here mode

The guided first session. It runs the six-step natural-language workflow of the RTD
[Natural Language Inference](https://pyautofit.readthedocs.io/en/latest/overview/natural_language.html)
page on the bundled 1D Gaussian dataset — **one step per turn, with the user typing each prompt
themselves** — and then replays the same six steps on the user's own science.

This file is a script for *you*, the assistant — what to say, what to hand over, where to stop —
not user-facing prose. The tour adds **no capability**: every step is an existing skill driven at
`skills/_style.md` "Newcomer mode" depth.

## What changes

- **One step per turn.** Explain, hand over the next prompt, then **stop and wait**. Never run
  ahead, batch two steps, or type the user's prompt for them — the point is that they discover
  the workflow *is* natural language by using it.
- **Newcomer-mode pacing:** one concept at a time, statistical framing before code, a check-in
  beat closing every step, and the two-line footer below on every step of both parts.
- **Generated Python is kept**, one script per step under `scripts/start_here/` — they leave with
  runnable files, not a transcript.

## What stays the same

- Every `AGENTS.md` safety invariant: the data-inspection gate (mandatory on real data in Part 2;
  the bundled dataset is simulated and exempt), the code gate, "the likelihood code is the
  user's", the `output/` write-ban, the source-edit boundary.
- Saved Python is at full `skills/_style.md` "Generated script style" quality — mode-invariant.
- The skills are unchanged. This mode composes `af_compose_model`, `af_custom_analysis`,
  `af_configure_search`, `af_run_search`, `af_plot_fit`, `af_load_results`, `af_adapt_to_domain`,
  `af_ingest_paper`, `af_wrap_likelihood` and `start-new-project`; read the skill rather than
  restating it here.

## Composition

Depth follows `skills/_style.md` "Adaptive depth", entering at **Newcomer mode** unless turn 0's
question or an existing `wiki/project/profile.md` says otherwise — a recorded expert level is not
overridden, so an expert gets the *workflow*, not Bayes from first principles. "Teacher mode"
mid-tour switches `modes/teacher.md` on for the rest of the tour without leaving it.

## What triggers inference

The published start-here prompt (below), "start here", "start_here", "begin the start here
guide", "walk me through PyAutoFit from the beginning" — outranking inference from the rest of
the opening request; `.maintainer` outranks it.

---

## Trigger and posture

The published prompt — on the PyAutoFit README, this repo's README and the RTD Quick Start — is:

> I want to perform scientific inference with PyAutoFit (https://github.com/PyAutoLabs/PyAutoFit) and the
> autofit_assistant (https://github.com/PyAutoLabs/autofit_assistant).
>
> Begin the "start here" guide for a new user.

Before turn 0, run the session-start drift check (`AGENTS.md` "Session start"):
`python autoassistant/audit_skill_apis.py --check-version`. Exit 0 — continue. Exit 2 or 3 — the
stack is absent or broken: run `af_setup_environment`, say so in one line, resume at turn 0. Exit
1 — report the drift and offer the pinned version; the tour can still run.

Honour **"skip to step N"** and **"skip to my project"** immediately, always saying in one line
what is skipped — never skip silently. "Back up" returns to the previous step.

---

## Turn 0 — the intro

One turn, in this order:

1. **What PyAutoFit is**, in a paragraph: a framework for fitting *your* model to *your* data
   with *your* likelihood. It supplies the inference — priors, samplers, results, model
   comparison — and stays out of the science, which is why it works across fields.
2. **The workflow line**, verbatim:
   `model -> priors -> likelihood -> search -> results -> scientific workflow` — one tour step
   per link, all of it done by typing English.
3. **The dataset.** `dataset/gaussian_x1/`: 100 pixels of a 1D Gaussian plus noise, simulated with
   `centre=50.0`, `normalization=25.0`, `sigma=10.0` and per-pixel noise sigma 2.0. Quote those
   truth values — they make step 4 judgeable rather than merely reportable
   (`dataset/gaussian_x1/README.md`).
4. **The equation**: `g(x) = N exp[-1/2 ((x - c) / sigma)^2]`, with `c` the centre, `N` the peak
   amplitude and `sigma` the width. These three are what gets inferred.
5. **Plot the data and announce the absolute path**, offering to open it (`skills/_style.md`
   "Plot output and path announcement"). The data are simulated so the gate does not formally
   apply, but a newcomer should see what is being fitted before it is fitted.
6. **The footer, once, in full** (see "Teacher mode and questions"), naming
   [HowToFit](https://github.com/PyAutoLabs/HowToFit) as the lecture-notes companion.
7. **At most one question**: *"Are you new to Bayesian inference, or just new to PyAutoFit?"* — it
   sets depth, nothing more. Write `wiki/project/profile.md` only if they volunteer durable
   context unprompted (`AGENTS.md` "First-interaction protocol").
8. **Hand over the step-1 prompt and STOP.**

---

## Part 1 — the six steps

Every step has the same five beats: **Explain** (2-4 sentences of statistical then domain framing
plus one `wiki/core/` link — not a lecture) → **Prompt to type** (the RTD page's prompt for that
section, verbatim, in a blockquote, with "type this as your next message") → **Run and show** (do
the work through the named skill, save the script, show the *real* output) → **Try a variation**
(two or three rewordings they could type instead, making the point that the description *is* the
model) → **check-in** (the footer, then stop).

### Step 1 — Compose the Model

*Skill:* `af_compose_model`. *Script:* `scripts/start_here/step_1_compose_model.py`.

**Explain.** A model is a plain Python class; its `__init__` arguments become the free parameters,
each with a prior — a statement of what is believed before the data are seen. Point at
`wiki/core/concepts/model_composition_and_priors.md`.

The tour's Gaussian is **peak-normalised**, as the equation says, and lives in
`scripts/start_here/gaussian.py`; PyAutoFit's example class `af.ex.Gaussian` is *area*-normalised
(dividing by `sigma * sqrt(2 pi)`), which here would put the normalization near 620 — outside the
0-100 prior this step prescribes. If the user asks, explain the difference: the convention belongs
to the model class, and the model class is theirs.

**Prompt to type.**

> Create a 1D Gaussian model with free centre, normalization and sigma.
> Use uniform priors from 0 to 100 for centre, 0 to 100 for normalization,
> and 0.1 to 30 for sigma. Show me the model and its priors.

**Run and show.** `model.info` — the real output:

```bash
Total Free Parameters = 3

model                         Gaussian (N=3)

centre                        UniformPrior [0], lower_limit = 0.0, upper_limit = 100.0
normalization                 UniformPrior [1], lower_limit = 0.0, upper_limit = 100.0
sigma                         UniformPrior [2], lower_limit = 0.1, upper_limit = 30.0
```

Read it back: three free parameters, each with an explicit prior, named the way they named them.

**Try a variation.** *"Make it two Gaussians"* becomes an `af.Collection` with six free parameters
and nothing else about the workflow changed:

```bash
Total Free Parameters = 6

model                         Collection (N=6)
    gaussian_0 - gaussian_1   Gaussian (N=3)

gaussian_0
    centre                    UniformPrior [0], lower_limit = 0.0, upper_limit = 100.0
    normalization             UniformPrior [1], lower_limit = 0.0, upper_limit = 100.0
    sigma                     UniformPrior [2], lower_limit = 0.1, upper_limit = 30.0
gaussian_1
    centre                    UniformPrior [3], lower_limit = 0.0, upper_limit = 100.0
    normalization             UniformPrior [4], lower_limit = 0.0, upper_limit = 100.0
    sigma                     UniformPrior [5], lower_limit = 0.1, upper_limit = 30.0
```

Also offer *"fix sigma to 10"* (one dimension gone) and *"put a Gaussian prior on centre, mean 50,
sigma 10"* (a belief rather than a flat range).

### Step 2 — Define the Likelihood

*Skills:* `af_custom_analysis`, and `af_wrap_likelihood` for the user's own code.
*Scripts:* `step_2_define_likelihood.py`, with the likelihood in `analysis.py`.

**Explain.** The likelihood turns parameter values into a number: here independent Gaussian
errors, so `ln L = -1/2 sum ((d - m)/sigma)^2`. It lives in an `Analysis` class holding the data
and implementing one method. Point at `wiki/core/concepts/bayesian_inference.md`.

**Prompt to type.**

> Load the 1D Gaussian data and noise map, define a likelihood function which uses 
> independent Gaussian errors to compare the model with the data and for a random 
> set of parameters calculate the likelihood. Produce an image comparing the fit
> to the data

**Run and show.** The log likelihood at one random draw from the priors, plus the model-vs-data
figure with residuals, path announced with an offer to open it. Say why the number is so bad: a
random draw is *meant* to be a bad fit, and seeing a bad fit score badly is how you check the
likelihood is wired up at all. The likelihood at the simulation truth alongside gives the scale of
the gradient the search will climb.

**Try a variation.** *"Evaluate it at the true parameters instead"*, and — the pointer to
`af_wrap_likelihood`, which is why Part 2 works at all — the page's bring-your-own-likelihood
prompt:

> Use my existing likelihood code for this analysis [point to code]. Connect 
> it to PyAutoFit and check that it returns the same likelihood values at 
> the same parameter values.

### Step 3 — Searches

*Skill:* `af_configure_search`. *Script:* `step_3_choose_search.py`.

**Explain.** The search explores the parameter space, and the choice is statistical before it is
computational: evidence needed (nested), posterior only (MCMC), or a best-fit point (optimiser).
Point at `wiki/core/concepts/non_linear_search.md`.

**Prompt to type.**

> Show me the available non-linear searches, including those which support
> gradient based inference using JAX. For this example fit, our likelihood
> function is not implemented using JAX, so lets use Dynesty nested sampling
> with 100 live points to estimate the posterior and evidence.

**Run and show.** The installed roster, read from the library rather than from memory, in the
page's four families — **nested sampling** (`Nautilus`, `DynestyStatic`, `DynestyDynamic`),
**MCMC** (`Emcee`, `Zeus`), **optimisation** (`LBFGS`, `Drawer`), **gradient-based JAX**
(`BlackJAXNUTS`, the `MultiStart*` optimisers) — then the configured
`af.DynestyStatic(path_prefix="start_here", name="gaussian_x1", nlive=100)`. Say why Dynesty and
not a JAX sampler (this likelihood is plain NumPy, so there are no automatic gradients to take),
and why nested and not MCMC (step 6 compares evidences).

**Try a variation.** *"Use Emcee instead"* (posterior but no evidence, so step 6's comparison would
be unavailable) and *"what changes with 50 live points?"* (the accuracy/runtime dial).

### Step 4 — Model Fit and Results

*Skills:* `af_run_search`, `af_plot_fit`, `af_load_results`. *Script:* `step_4_fit_and_results.py`.

**Explain.** Model, likelihood and search meet in one call — seconds on this dataset. Say the
expected wall time before launching: on their own data that estimate is the difference between a
coffee and an HPC job.

**Prompt to type.**

> Run the model fit. Show the parameter estimates and uncertainties, and plot
> the maximum-likelihood Gaussian over the data.

**Run and show.** While it runs, do the **output-folder tour** — not a path, a tour
(`skills/_style.md` "Output folder announcement"): the absolute
`output/start_here/gaussian_x1/<unique_id>/`, `model.results` first, then `model.info`,
`search.summary`, `files/` and `image/`, and the fact that they update *as the search runs*. Then
the parameter table against turn 0's truth — the real numbers from this dataset:

```bash
parameter        inferred (median, 1 sigma)        truth
--------------------------------------------------------------
centre             50.00 +0.28 / -0.28          50.0
normalization      24.89 +0.67 / -0.58          25.0
sigma               9.82 +0.28 / -0.26          10.0
```

with `log evidence: -48.95` — plus the maximum-likelihood profile over the data with residuals,
path announced. Then the sentence that matters: every parameter is recovered within about one sigma
of its input, so the machinery works, and that check is what you do first on real data too.

Then hand over the page's second prompt, in the same step:

> Plot the posterior distributions. How well is sigma constrained, and
> is it correlated with normalization?

and show the corner plot, reading it for them: sigma is constrained to about 3%, and its
correlation with normalization is the visible one — a wider Gaussian needs a lower peak to keep the
same total signal.

**Try a variation.** *"What is the Bayesian evidence, and what is it for?"*, *"How many likelihood
evaluations did that take?"* (`search.summary`).

### Step 5 — Saving and Loading

*Skill:* `af_load_results`. *Script:* `step_5_save_and_load.py`.

**Explain.** The fit already saved itself; this step reads it back. A result that outlives its
Python session is what makes a hundred fits manageable instead of terrifying.

**Prompt to type.**

> Save the run to disk, with fit and residual images updated during
> sampling. Afterwards, reload the saved samples and inspect the fit
> without rerunning it.

**Run and show.** Walk the tree they saw mid-fit, now complete, and point out the `.zip` beside it.
Then reload through the aggregator **without re-running the search**: same evidence, same medians.
Two things to say out loud — re-running the script reloads rather than re-fits (this surprises
everyone once), and paths are never composed by hand because the unique identifier changes with the
model. One line on `af_inspect_results_mcp`, which exposes the same folder to a chat client with no
code execution.

**Try a variation.** The page's aggregator prompt, where one fit becomes a catalogue:

> Find the completed Gaussian fits and make a table of the inferred widths
> and their uncertainties, labelled by dataset and search algorithm.

### Step 6 — Scientific Workflows

*Skills:* `af_compose_model`, `af_chain_searches`, `af_load_results`.
*Scripts:* `step_6_three_gaussians.py`, and `step_6_three_gaussians_nautilus.py` for the faster
sampler.

**Explain.** Everything so far was one model and one fit. A scientific workflow is what happens
when there are several — competing models, competing samplers, a backlog of saved runs. Offer the
page's three extensions; let the user pick one **or more**, and never run all three unasked.

**Extension 1 — model comparison.**

> Extend the model to three Gaussians and sum their profiles in the
> likelihood. Assert that their centres are in ascending order, show me
> the priors, perform inference with Dynesty again and compare the Bayesian 
> evidence with the single-Gaussian fit.

**Warn before you launch it.** This is the first fit that costs real time, and they should hear
why before watching a silent terminal: nine free parameters instead of three, and the
ascending-centre assertion rejects most prior draws, so Dynesty's ellipsoidal bounds spend almost
every proposal on points the assertion throws away. The dry run measured **0.21% sampling
efficiency** — 346,992 likelihood calls for 733 accepted samples — and after **30 minutes** was
still at `dlogz` 339 against a 0.109 target, nowhere near converged and slowing (7.7 s per
accepted sample by the end). Say that out loud rather than letting them find it.

**Offer the faster sampler.** *"If you'd rather not wait, say 'use Nautilus instead'"* —
`step_6_three_gaussians_nautilus.py` is the same model, priors, assertion and likelihood with
`af.Nautilus(n_live=100)` in place of Dynesty, and finishes in **about 2.5 minutes**. That swap is
the lesson `af_configure_search` teaches: every search shares one interface, so the sampler is the
cheapest thing in an analysis to change. Both fits under Nautilus:

```bash
model               N     max log L      log evidence
--------------------------------------------------------
one Gaussian        3     -36.13         -49.41
three Gaussians     9     -33.65         -60.23
```

**Read it for them.** The three-Gaussian model reaches a *higher* maximum likelihood — with six
more parameters it always will — and a log evidence **11 lower**, strong preference for the single
Gaussian on the usual Jeffreys-style reading. The data came from one Gaussian, two components have
nothing to fit and wander over their whole prior range, and the evidence charges for that unused
prior volume automatically: nobody added a penalty term, and Occam's razor arrived on its own.
Mention that the assertion is what removes the six-fold relabelling degeneracy of three identical
components, and that it is a prior statement like any other — so this is the evidence *under these
priors*.

If they run the Dynesty version anyway, do not wait in silence: suggest extension 2 or 3, or
reading `output/start_here/gaussian_x3/<unique_id>/model.results`, while it runs. Quote evidence
numbers only from a run that finished; step 4's single-Gaussian Dynesty reference is
`log evidence: -48.95`.

**Extension 2 — sampler comparison.**

> Fit the same model using Emcee, Dynesty and an optimiser for maximum
> likelihood estimation. Keep the likelihood and parameter bounds fixed,
> and use the same priors for both samplers. Compare runtime, likelihood
> evaluations and best-fit values. For the samplers, also assess convergence
> and agreement of posterior constraints.

**Extension 3 — revisiting a saved result.**

> Load the saved Gaussian fit. Report the median and 68% credible interval
> for sigma, plot its correlation with normalization, and inspect the
> residuals for structure the model may have missed.

---

## Part 2 — your own project

Enter after step 6, or the moment the user says "now my project" / "skip to my project". Say in one
line that the same six steps now run on their science, and that this is the part that persists.

The engine is [`af_adapt_to_domain`](../skills/af_adapt_to_domain.md) — **read it and run its
interview from there; do not restate it here.** This mode supplies the running order and the pacing
only. Note as you go that their model class defines its own normalisation convention, parameter
names and units — precisely why step 1 used a plain Python class rather than a framework object.

**P0 — Science context.** Ask for **either** a paper (arXiv ID, link or local PDF →
`af_ingest_paper`, into `wiki/literature/`) **or** a plain-language description of what they measure
and want to infer, plus where their data lives and in what format. Run the `af_adapt_to_domain`
interview lightly; write `wiki/project/profile.md` and `state.md` per `AGENTS.md`. **Restate their
problem in inference terms in one paragraph** — parameters, data, the shape of the likelihood — and
ask them to correct it; that paragraph is the contract for everything below. Any selection cut made
while loading their data (a redshift floor, a quality flag) is a scientific decision: state it back
and record it.

**P1 — Model.** Their parametrisation, in words, becomes `af.Model` / `af.Collection` via
`af_compose_model`; show `model.info` and check the parameter count is what they expected. Then step
1's nudge again: *"describe it differently and watch the model change"*.

**P2 — Likelihood.** **They have code:** `af_wrap_likelihood` — wrap it into an `Analysis`, validate
at hand-built instances against their own function's values, **never alter its numerics**
(`AGENTS.md`). **No code:** build a small `Analysis` from their description via
`af_custom_analysis`. Either way the **data-inspection gate is mandatory here** — real data: plot it
(or summarise it numerically), show the absolute path, and ask one question about known artefacts,
outliers or selection effects before anything is fitted.

**P3 — Search.** Ask three things — runtime budget, whether the likelihood is JAX-differentiable,
whether they need the evidence — then `af_configure_search` gives a recommendation **with the
reason**, not just a name.

**P4 — Fit and results.** Ask for an explicit go-ahead first; the page's bring-your-own-likelihood
prompt sets the default posture ("Do not begin inference until we have discussed the setup and I
give you the go-ahead"). Then `af_run_search`, the output-folder tour on *their* output,
`af_plot_fit` and `af_load_results`. Real data has no truth to check against, so the check becomes
the residuals and the shape of the posterior — say so explicitly.

**P5 — Save and organise.** Offer [`start-new-project`](../skills/start-new-project.md) for a
standalone science-project repo — offer it, do not force it; quick exploration is fine here.

**P6 — Extend.** Model comparison, sampler comparison, search chaining (`af_chain_searches`),
hierarchical models — the RTD
[Scientific Workflow](https://pyautofit.readthedocs.io/en/latest/overview/scientific_workflow.html)
and
[Statistical Methods](https://pyautofit.readthedocs.io/en/latest/overview/statistical_methods.html)
pages, and the matching skills.

---

## Teacher mode and questions

Append this footer to **every** step of both parts, verbatim:

> Ask anything here - "what is a prior?", "why nested sampling?" - and I'll explain before we
> move on. Say "teacher mode" for full explanations at every step.

Turn 0 says it once in full, adding that [HowToFit](https://github.com/PyAutoLabs/HowToFit) is the
lecture-notes companion for the statistics itself.

- **A question never advances the step.** Answer it, then re-offer the same prompt. Only "next", or
  the user typing the step's prompt, moves the tour on.
- **"Teacher mode" mid-tour** switches `modes/teacher.md` on for the rest of the tour without
  leaving it: more *why*, explicit assumptions, wiki and HowToFit pointers. The step script is
  unchanged; the depth around it grows.
- **Three or more concept questions in a row** is a signal — offer teacher mode, or offer to pause
  and read the relevant HowToFit tutorial together.

---

## Hand-off

When both parts are done, or the user stops:

- One line: the session now runs in **assistant mode** (or **teacher mode** if chosen), and the
  tour's pacing rules no longer apply.
- Name what is on disk — scripts under `scripts/start_here/`, fits under `output/`, and any
  `wiki/project/` or `wiki/literature/` entries Part 2 wrote.
- Where to go next: [`start-new-project`](../skills/start-new-project.md) for a project repo,
  [`af_ingest_paper`](../skills/af_ingest_paper.md) for more domain context, the RTD Scientific
  Workflow and Statistical Methods pages for scale,
  [HowToFit](https://github.com/PyAutoLabs/HowToFit) for the statistics.

---

## Rules

- **Part-1 prompts are byte-identical** to `PyAutoFit:docs/overview/natural_language.md` — never
  paraphrase, reflow or "improve" one; the tour, that page and this repo's `README.md` are one
  artefact in three places.
- **Never fabricate output.** Every number, table, path and `model.info` the tour shows comes from
  running the script. If a run fails, say so and debug it (`af_debug_fit_failure`); a
  plausible-looking invented result is this mode's one unrecoverable failure.
- **All `AGENTS.md` safety invariants apply**, code gate included: on a harness without hooks,
  self-enforce with `python autoassistant/audit_skill_apis.py --file scripts/start_here/<script>.py`
  before running generated code.
- **Part-1 Python goes to `scripts/start_here/`**, one script per step, in `skills/_style.md`
  "Generated script style" — `__Contents__` docstring, `"""__Section__"""` narrative sections,
  `<Project>:<path>` citations. The shared model class (`gaussian.py`) and likelihood
  (`analysis.py`) sit beside them, which is also what lets step 5 reload results by class path.
  Part-2 Python goes to `scripts/` or the user's science project.
- **Figures go to `scripts/scratch/start_here/`** (gitignored), absolute path printed and quoted
  back.
- **"Skip to step N" / "skip to my project" are honoured**, always with a one-line note of what was
  skipped.
