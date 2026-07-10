---
id: teacher-basic-workflow
version: 1
mode: teacher
difficulty: easy
datasets:
  - dataset/gaussian_x1
added: 2026-07-10
---

# Benchmark: teach the inference workflow end-to-end (teacher · easy)

Everything this prompt asks for is directly available in the assistant: the
dataset ships with the repo (truth recorded in its README), and model
composition, search configuration, fitting and posterior reading are all
covered by existing `af_*` skills and `wiki/core/` pages. The benchmark
measures **pedagogy**: whether the agent teaches the workflow rather than just
executing it.

## Prompt

Paste verbatim as the first message of a fresh session (see
[`../AGENTS.md`](../AGENTS.md) for the run protocol):

```
Teacher mode.

I'm new to PyAutoFit and want to learn the basic workflow end-to-end. Fit the
bundled 1D Gaussian dataset in dataset/gaussian_x1/ and recover its input
parameters.

Explain what each step is doing and why as we go: composing the model, choosing
the priors, picking the non-linear search, and how to read the posterior. So I
come away understanding the workflow, not just the commands.
```

This is Example Prompt 1 of the top-level `README.md`; the two texts must stay
identical (a divergence is a bug — fix the README or bump this card's
`version`).

## What this measures

- Teacher-mode posture: paced explanation, check-ins, wiki/HowToFit routing —
  without diluting the saved script's workspace-style completeness.
- Routing: uses the bundled dataset and the assistant's skills rather than
  improvising.
- Statistical correctness of the teaching (priors as statements, what the
  posterior/errors mean).

## Success rubric (100 points)

### Machine-checkable (40)

| # | Check | Pts |
|---|-------|-----|
| M1 | A script saved under `scripts/` that composes the model and runs the fit | 10 |
| M2 | A completed non-linear search result exists under `output/` (not test-mode) | 10 |
| M3 | The recovered parameters bracket the dataset README's truth (50, 25, 10) within quoted errors | 10 |
| M4 | Explicit priors set on all three parameters in the script (no config-default reliance) | 10 |

### Judged (60)

| # | Criterion | Pts |
|---|-----------|-----|
| J1 | Teaching quality: each workflow step framed statistically before its code; one concept at a time with check-ins | 20 |
| J2 | Prior conversation: the three priors are *discussed as choices* (why uniform/log-uniform/etc.), not just set | 10 |
| J3 | Posterior literacy: median/errors/max-likelihood distinguished correctly; the user is shown how to read them | 10 |
| J4 | Saved script keeps full workspace-style docstring detail despite the teaching pace (mode-invariance rule) | 10 |
| J5 | Conduct: honest reporting, no fabricated numbers, API-gate discipline (no invented symbols) | 10 |

## Operator notes

- Expected wall-clock: 5–20 minutes; the fit itself is seconds. This is the
  recommended cheap **drift probe** to re-run across days/models.
- The operator answers as a genuine newcomer: minimal, honest, no rubric hints.
