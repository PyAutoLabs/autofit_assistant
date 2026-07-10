---
id: assistant-hard-sne-cosmology
version: 1
mode: assistant
difficulty: hard
datasets:
  - dataset/sne_cosmology
added: 2026-07-10
---

# Benchmark: autonomous SNe cosmology with model comparison (assistant · hard)

Real data, no shipped likelihood: the agent must select the sample, write the
flat-ΛCDM distance-modulus likelihood from scratch (numerical comoving-distance
integral), fit it, then extend to wCDM and answer a genuine model-comparison
question with the evidence. The dataset README's maintainer validation numbers
(Ωm = 0.344, H0 = 73.14 on the same cuts) make correctness checkable.

## Prompt

Paste verbatim as the first message of a fresh session (see
[`../AGENTS.md`](../AGENTS.md) for the run protocol):

```
Assistant mode.

Fit flat LambdaCDM to the Pantheon+ supernova distances bundled at
dataset/sne_cosmology/: select the Hubble-flow sample, write the
distance-modulus likelihood, compose the model with sensible priors on
Omega_m and H0, run a nested sampler, and report the posterior constraints
and the evidence. Then compare against a model with a free dark-energy
equation of state w, and tell me whether the evidence justifies the extra
parameter.

Plan the whole analysis first, execute it end-to-end, and record your
decisions in the project journal as you go.
```

This is Example Prompt 3 of the top-level `README.md`; the two texts must stay
identical (a divergence is a bug — fix the README or bump this card's
`version`).

## What this measures

- Autonomy-dial behaviour: a phased plan up front, execution with checkpoints,
  journal entries — proactive but not silent.
- Real-data discipline: the dataset README actually read (sample cuts,
  diagonal-errors caveat surfaced); data inspected before fitting.
- A correct physical likelihood written from scratch, and an evidence-based
  model comparison interpreted honestly.

## Success rubric (100 points)

### Machine-checkable (40)

| # | Check | Pts |
|---|-------|-----|
| M1 | Scripts under `scripts/` for both fits (ΛCDM and wCDM), workspace style | 5 |
| M2 | Completed nested-sampler results for BOTH models under `output/` with finite evidences | 10 |
| M3 | ΛCDM constraints consistent with the README validation values (Ωm within ~2σ of 0.344; H0 within ~2σ of 73.1) on the stated cuts | 15 |
| M4 | At least one dated `wiki/project/YYYY-MM-DD-*.md` journal entry recording the analysis decisions | 10 |

### Judged (60)

| # | Criterion | Pts |
|---|-----------|-----|
| J1 | Plan quality: sample selection, likelihood design, priors and the comparison laid out before execution | 10 |
| J2 | Likelihood correctness: proper comoving-distance integral, (1+z) factor, log-space conversion, noise normalisation included (evidence use) | 15 |
| J3 | The diagonal-errors caveat from the dataset README is surfaced when reporting constraints (uncertainties acknowledged as underestimated) | 10 |
| J4 | Model comparison read correctly: ln B computed from the two evidences, interpreted against a stated scale, with prior-sensitivity acknowledged for w | 15 |
| J5 | Conduct: honest throughout; failures/retries reported; no fabricated numbers; API-gate discipline | 10 |

## Operator notes

- Expected wall-clock: 20–90 minutes depending on hardware; two nested-sampler
  runs over a 1500-point likelihood dominate.
- The operator lets the plan run; if the agent asks scope questions, answer
  minimally ("your call").
- A run that honestly concludes the evidence does *not* justify free w (the
  expected answer on this data) scores full J4 — the benchmark rewards the
  correct negative result.
