# gaussian_x1 — the canonical 1D Gaussian dataset

Noisy 1D data simulated from a single Gaussian — the classic PyAutoFit teaching problem
(the same one `autofit_workspace` and HowToFit build on).

- `data.json` — 100 pixels of signal + Gaussian noise (`af.util.numpy_array_from_json`).
- `noise_map.json` — the per-pixel noise sigma (constant 2.0).

**Simulation truth** (seed 1, `numpy.random.default_rng`): `centre=50.0`,
`normalization=25.0`, `sigma=10.0` on `xvalues = np.arange(100)` via
`normalization * exp(-0.5 ((x - centre)/sigma)^2)`.

A correct fit recovers the truth comfortably — the maintainer validation run
(DynestyStatic, `nlive=75`) found `centre=49.98`, `normalization=24.85`, `sigma=9.84`.
If your fit lands far from these, the model, priors, or likelihood wrapper is wrong —
not the data.

Try it: the README's Example Prompt 1 walks the whole workflow on this dataset in
teacher mode.
