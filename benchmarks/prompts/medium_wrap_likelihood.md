---
id: assistant-medium-wrap-likelihood
version: 1
mode: assistant
difficulty: medium
datasets:
  - dataset/gaussian_x1
added: 2026-07-10
---

# Benchmark: wrap a user's likelihood function (assistant · medium)

The assistant's defining task, with the user's "existing code" supplied inline
so the card is self-contained. The function deliberately returns a
**chi-squared** (not a log likelihood) and takes a **positional vector** — the
two conventions the wrapper must translate correctly, and the exact places a
careless wrap silently corrupts the inference.

## Prompt

Paste verbatim as the first message of a fresh session (see
[`../AGENTS.md`](../AGENTS.md) for the run protocol). Unlike the teacher card,
this prompt is not README-mirrored (the README keeps a generic version).

```
Assistant mode.

I have existing analysis code that scores a Gaussian model against my data. Here it is:

    import numpy as np

    def gaussian_chi2(theta, x, y, yerr):
        """theta = [centre, amplitude, width]; returns chi-squared."""
        centre, amplitude, width = theta
        model = amplitude * np.exp(-0.5 * ((x - centre) / width) ** 2)
        return float(np.sum(((y - model) / yerr) ** 2))

My data is the bundled dataset/gaussian_x1/ (data.json is y, noise_map.json is yerr,
x is just the pixel index). Wrap my function into PyAutoFit without changing it: build
the Analysis class around it, compose the model with priors (ask me about anything you
need), run a nested sampler, and show me the posterior and the evidence.
```

## What this measures

- The wrap discipline of `af_wrap_likelihood`: the user's function is imported/
  used **unchanged**; the wrapper owns the translation.
- The chi-squared → log-likelihood conversion (sign and factor), and whether
  the noise-normalisation term is *raised with the user* before the evidence is
  quoted.
- Pre-fit validation: hand-built good/bad instances checked before sampling.

## Success rubric (100 points)

### Machine-checkable (40)

| # | Check | Pts |
|---|-------|-----|
| M1 | A script under `scripts/` containing the user's `gaussian_chi2` verbatim (no edits to its body) | 10 |
| M2 | The Analysis wraps it with the correct −0.5 factor (verifiable in the script) | 10 |
| M3 | A completed nested-sampler result exists under `output/` with a finite log evidence | 10 |
| M4 | Recovered parameters bracket the dataset truth (50, 25, 10) within quoted errors | 10 |

### Judged (60)

| # | Criterion | Pts |
|---|-----------|-----|
| J1 | Validation before fitting: good/bad instance checks (or equivalent) actually run and shown | 15 |
| J2 | The noise-normalisation term: its absence from the user's chi2 is *surfaced to the user* as their call, with the evidence caveat explained | 15 |
| J3 | Prior conversation: the user is asked about parameter ranges; priors reflect the answers | 10 |
| J4 | The user's code ownership respected: no re-parametrisation, no silent "fixes", no guards added | 10 |
| J5 | Conduct: concise assistant-mode communication, honest reporting, API-gate discipline | 10 |

## Operator notes

- Expected wall-clock: 10–30 minutes.
- When asked about priors, the operator answers plainly ("centre is somewhere
  in the middle, amplitude order 10, width order 10") — honest, minimal, no
  coaching.
- If asked whether to add the noise-normalisation term, the operator says yes.
