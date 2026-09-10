"""
Start Here Step 5: Saving and Loading
=====================================

The fifth step of the "start here" tour. The fit in step 4 wrote everything it learned to disk
as it ran. This script walks that output folder and then reloads the completed run *without
re-fitting it* — the difference between a result that lives in one Python session and a result
that is still there next month, alongside every other fit you have run.

Nothing here launches a search. If `output/start_here/gaussian_x1/` does not exist yet, run
`step_4_fit_and_results.py` first.

__Contents__

- **Imports:** autofit's aggregator and the tour's model class.
- **The Output Folder:** What the search wrote, and what to open first.
- **Reload:** Load the completed fit from disk via the aggregator.
- **Inspect:** Posterior summaries from the reloaded samples.
"""

import pathlib

from autofit.aggregator.aggregator import Aggregator

import gaussian  # noqa: F401  (the model class the saved samples are rebuilt from)

"""
__The Output Folder__

Output is keyed by `path_prefix`/`name` and then by a **unique identifier** derived from the
model and search settings, so changing the model produces a new folder rather than overwriting
the old fit. Inside it:

- `model.results` — the human-readable parameter summary. Open this first.
- `model.info` — the model composition and priors that produced it, i.e. step 1's output.
- `search.summary` — how the search behaved: runtime and likelihood evaluations.
- `files/` — the machine-readable record: `model.json`, `samples.csv`, `samples_summary.json`,
  `covariance.csv` and the search's own settings.
- `image/` — the figures the Analysis's `Visualizer` drew, refreshed while the search ran.

The `.zip` beside the folder is the same content archived for transfer. The full breakdown is in
the workspace's own prose, at
`autofit_workspace:scripts/overview/overview_2_scientific_workflow.py` under "output folder" —
worth reading once rather than restating here.
"""

output_path = pathlib.Path("output") / "start_here" / "gaussian_x1"

if not output_path.exists():
    raise FileNotFoundError(
        f"{output_path.resolve()} not found — run step_4_fit_and_results.py first."
    )

print(f"Output folder: {output_path.resolve()}\n")

for entry in sorted(output_path.rglob("*")):
    depth = len(entry.relative_to(output_path).parts) - 1
    if depth <= 1 and not entry.name.startswith("."):
        print(f"{'    ' * depth}{entry.name}{'/' if entry.is_dir() else ''}")

results_file = next(output_path.glob("*/model.results"), None)

if results_file is not None:
    print(f"\n--- {results_file.name} ---")
    print(results_file.read_text().strip())

"""
__Reload__

The aggregator walks an `output/` tree and lazily loads every fit it finds, as generators rather
than all at once (`PyAutoFit:autofit/aggregator/aggregator.py`, and
`skills/af_load_results.md`). For one fit it is the honest way to get the samples back; for a
sweep over many datasets or models it is the only practical one, and the same call scales to
both. At larger scale the sqlite-backed `af.Aggregator.from_database(...)` adds queries over
dataset metadata, search and model properties.

Note what is *not* done here: no output path is composed by hand. Paths carry a unique
identifier that changes with the model, so hand-built paths break silently — reload through the
aggregator, or by re-running the script, which reloads a completed search instead of repeating
it.

The saved `model.json` records the model class by import path (`gaussian.Gaussian`), which is
why this script imports the module: rebuilding an instance means importing the user's own class.
Result folders are portable as long as the code that defines the model travels with them, which
is the practical argument for a science project repo (`skills/start-new-project.md`).
"""

agg = Aggregator.from_directory(directory=str(output_path))

print(f"\nFits found by the aggregator: {len(agg)}")

"""
__Inspect__

Everything step 4 printed is available again, with no sampler run: the evidence, the posterior
medians and their errors, and the maximum-likelihood instance — a real `Gaussian` object whose
own methods work on it.
"""

for samples in agg.values("samples"):
    median = samples.median_pdf()
    errors_hi = samples.errors_at_upper_sigma(sigma=1.0)
    errors_lo = samples.errors_at_lower_sigma(sigma=1.0)

    print(f"\nlog evidence: {samples.log_evidence:.2f}")

    for name in ["centre", "normalization", "sigma"]:
        print(
            f"{name:<16} {getattr(median, name):>7.2f} "
            f"+{getattr(errors_hi, name):.2f} / -{getattr(errors_lo, name):.2f}"
        )
