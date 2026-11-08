---
name: af_load_data
description: Load the user's real data — CSV, FITS, HDF5, npy/npz or JSON — into the arrays their Analysis takes, name each column's meaning and units, and surface every selection cut (a redshift floor, a quality flag, a calibrator exclusion) back to the user with its scientific justification before anything is fitted. Records the column map, units and cuts in wiki/project/ (profile "Data shapes" + a dated entry); the data-inspection gate follows immediately. Use when the user says "load my data", "here's my CSV/FITS file", "which rows should we keep", or arrives at the data step of af_adapt_to_domain, af_wrap_likelihood or start-here Part 2. Not for simulated data (af_simulate_dataset), wrapping the likelihood (af_wrap_likelihood) or plotting fits (af_plot_fit).
user-invocable: true
---

# Loading your data and its selection cuts

Before a single parameter is inferred, two decisions shape the answer more than any prior
or sampler: **what each number in your file means**, and **which rows you keep**. A
mislabelled column (a magnitude read as a distance modulus, an error read as a variance)
and an unstated cut (a redshift floor, a quality flag, dropping calibrators) are science
choices — they change what the posterior is a posterior *of*. This skill makes both
explicit, gets them into Python as plain arrays your `Analysis` can hold, and writes them
down so the next session (and the paper's methods section) inherits them.

**The constitution's rules apply** (`AGENTS.md` "Safety invariants"): the data are yours,
so the assistant proposes and you decide — and the **data-inspection gate** follows this
skill immediately, before any model is composed or run.

## Orient

In inference terms, loading fixes the *data vector* `d` and its noise model inputs that the
likelihood `p(d | θ)` is evaluated against
([[../wiki/core/concepts/bayesian_inference]]). A selection cut redefines `d` itself:
fitting only the rows with `z > 0.023` means the posterior answers a question about the
Hubble-flow sample, not about every supernova in the file. If the cut depends on the
quantity being modelled, it can also bias the inference unless the likelihood accounts for
it — which is exactly why each cut needs a stated justification.

A concrete example, the bundled `dataset/sne_cosmology/pantheon_plus_distances.csv` (see
its `README.md`): six columns — `cid`, `z_hd`, `z_hd_err`, `mu`, `mu_err_diag`,
`is_calibrator`. A flat-ΛCDM distance fit keeps `is_calibrator == 0` (Cepheid-calibrator
hosts anchor the distance ladder, they are not Hubble-flow tracers) and `z_hd > 0.023`
(below it, peculiar velocities dominate the redshift error). Two lines of numpy, two
consequential scientific decisions.

## Ask

Get these before writing code — most come straight from the user or from their file's own
header/README; read `wiki/project/profile.md` first, it may already record them:

1. **Where and what format.** Path, and CSV / FITS / HDF5 / npy / JSON. One file or many?
2. **What each column means, with units.** Which is the independent variable, which the
   measurement, which the uncertainty — and is the uncertainty a σ, a variance, or a
   covariance? Any identifier, flag or grouping columns?
3. **Which rows to keep, and why.** Every cut: the expression and its scientific reason. If
   the user doesn't know of any, ask once about quality flags, sample membership and range
   limits — then state "no cuts" back as an explicit decision.
4. **What the Analysis needs.** The arrays (and their shapes) the likelihood takes — this is
   the hand-off to `af_wrap_likelihood` or `af_custom_analysis`.

Never infer a column's meaning or a cut silently from its name. Propose ("`mu` looks like
the SH0ES-calibrated distance modulus in mag — right?"), and let the user confirm.

## Branch — read the file

The deliverable is a small, re-runnable loader in `scripts/` (or a `load_data()` function
the fit script imports), written in the workspace script style. The pattern, for the
Pantheon+ CSV:

```python
"""
Data: Pantheon+ Hubble-flow distances
=====================================

Load the Pantheon+SH0ES distance moduli (Scolnic et al. 2022; Brout et al. 2022), apply
the selection cuts agreed in-session, and return the arrays the distance-modulus Analysis
takes.

__Contents__

- **Imports:** numpy and pathlib only — loading is not PyAutoFit's job.
- **Columns:** What each column means, with units.
- **Selection:** Every cut, with its scientific justification.
- **Arrays:** The arrays handed to the Analysis.
"""
from pathlib import Path

import numpy as np

"""
__Columns__

`z_hd` is the Hubble-diagram redshift (dimensionless), `mu` the SH0ES-calibrated distance
modulus (mag), `mu_err_diag` its diagonal 1σ uncertainty (mag — a σ, not a variance), and
`is_calibrator` flags Cepheid-calibrator hosts (1) versus Hubble-flow SNe (0). See
`dataset/sne_cosmology/README.md`.
"""
path = Path("dataset") / "sne_cosmology" / "pantheon_plus_distances.csv"
data = np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding="utf-8")
n_total = len(data)

"""
__Selection__

Two cuts, each a scientific decision recorded in `wiki/project/`:

- `is_calibrator == 0` — calibrator hosts anchor the absolute magnitude via Cepheids; they
  are not Hubble-flow distance tracers.
- `z_hd > 0.023` — below this, peculiar velocities dominate the redshift uncertainty.
"""
keep = (data["is_calibrator"] == 0) & (data["z_hd"] > 0.023)
print(f"Kept {keep.sum()} of {n_total} rows "
      f"(is_calibrator == 0: {(data['is_calibrator'] == 0).sum()}, "
      f"then z_hd > 0.023: {keep.sum()})")

"""
__Arrays__

The Analysis takes three 1D float arrays of equal length.
"""
z = np.asarray(data["z_hd"][keep], dtype=float)
mu = np.asarray(data["mu"][keep], dtype=float)
mu_err = np.asarray(data["mu_err_diag"][keep], dtype=float)
print(f"z: {z.shape}, mu: {mu.shape}, mu_err: {mu_err.shape}")
```

Print the row count after **each** cut, not just the final one: a cut that removes far more
(or fewer) rows than the user expected is the cheapest bug catch in the whole pipeline.

Other formats — same shape, different reader; use what the user already has installed and
don't add dependencies uninvited:

- **CSV / text** — `np.genfromtxt(..., names=True)` as above, or `pandas.read_csv` if the
  user already uses pandas. Check the delimiter, header row and missing-value marker.
- **FITS** — `astropy.io.fits.open(path)`; a table is in an extension HDU
  (`hdul[1].data["COLUMN"]`), an image in `hdul[0].data`. Header keywords (`BUNIT`,
  `TUNITn`) often state units — read them back to the user.
- **HDF5** — `h5py.File(path, "r")`; list `f.keys()` (and `f[key].attrs` for units) with
  the user before picking datasets.
- **npy / npz** — `np.load(path)`; an `.npz` is a dict of arrays (`.files`). No metadata, so
  meanings and units must come from the user.
- **JSON** — `json.load`; convert lists to `np.asarray(..., dtype=float)` explicitly.

Whatever the format: check for NaN/inf and non-positive uncertainties *after* the cuts and
report them — don't silently drop them. Dropping them is itself a cut the user decides.

## Branch — state the cuts back and record them

Before moving on, say the full selection back in one short paragraph — every cut, its
justification, and the rows kept — and ask the user to correct it. That paragraph is the
data half of the inference contract (the `modes/start_here.md` P0 restatement is the other
half).

Then record it (default-yes; this is never a trivial change):

- **`wiki/project/profile.md` → "Data shapes"** (copy `wiki/project/_profile_template.md`
  if absent): the format, the column map with units, and the error convention. Durable —
  the next dataset of the same kind reuses it.
- **A dated `wiki/project/YYYY-MM-DD-<dataset>-data.md` entry** (from
  `wiki/project/_template.md`): the file loaded, every cut with a one-line justification
  and the rows kept after each, and where the loader lives. For the Pantheon+ example:

  ```markdown
  - `is_calibrator == 0` — calibrators anchor the distance ladder, not Hubble-flow tracers.
  - `z_hd > 0.023` — peculiar velocities dominate below this redshift.
  ```

If a cut later changes, write a new dated entry rather than editing the old one — the
record of what each fit was run on must stay true.

## Combine

- **Next, always: the data-inspection gate** (`AGENTS.md` "Safety invariants") — plot the
  kept data (or summarise it numerically), quote the absolute path, and ask one question
  about artefacts, outliers or selection effects. The cuts you just recorded are the first
  thing to look at in that plot.
- Then the likelihood: `af_wrap_likelihood` if the user has code (the arrays above are its
  "data" question, already answered), or `af_custom_analysis` to build one from their
  description.
- Testing the pipeline before the real data: `af_simulate_dataset` produces arrays of the
  same shape with a known truth.
- Domain context for a cut (why 0.023?): `af_ingest_paper` puts the defining paper into
  `wiki/literature/` so the justification can be cited, not asserted.

## Further reading

- **General reference** — [RTD: Scientific Workflow](https://pyautofit.readthedocs.io/en/latest/overview/scientific_workflow.html):
  where data loading and inspection sit in a PyAutoFit analysis.
- **Experienced PyAutoFit user** — [workspace: overview_1_the_basics](https://github.com/PyAutoLabs/autofit_workspace/blob/main/scripts/overview/overview_1_the_basics.py):
  loading a dataset into arrays an `Analysis` holds.

## Agent checklist

- [ ] Format, column meanings and units confirmed by the user, not inferred from names.
- [ ] Every cut stated with its justification; rows kept printed after each.
- [ ] NaN/inf/non-positive errors reported, not silently dropped.
- [ ] Profile "Data shapes" + dated `wiki/project/` entry written.
- [ ] Data-inspection gate run before any model is composed or fitted.
