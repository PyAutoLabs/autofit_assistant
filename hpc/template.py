"""
Template: HPC Fit Script
========================

This template lives in `hpc/`, paired with the CPU and GPU batch submit templates
(`hpc/batch_cpu/template`, `hpc/batch_gpu/template`). It provides the standard interface
between those batch scripts and PyAutoFit analysis code: command-line argument parsing,
configuration setup, and the fit entry point, so that the same script runs identically on
a local machine and on the HPC.

Copy this file into `scripts/` and rename it for your science case (e.g.
`scripts/fit.py`), then fill in the `Dataset` and `Model, Analysis & Search` sections —
your data loading and your wrapped likelihood (`af_wrap_likelihood`) go there. The batch
templates run `scripts/$SCRIPT`, so the copy belongs in `scripts/`. The HPC interface
(`parse_fit_args`, `__main__`, `--use_cpu`, `--number_of_cores`) must be preserved — the
CPU and GPU batch templates depend on it.

This file is written in the project's generated-script style (title + `__Contents__`
header, with each section introduced by a triple-quoted `__Section__` docstring) — see
the project root `AGENTS.md` "Conventions" and `skills/_style.md` "Generated script
style". Keep that style when you adapt it.

__Contents__

- **Imports:** Import autofit and the user's likelihood/model code.
- **Configuration:** Push the project `config/` and `output/` paths.
- **Fit:** Dataset loading + Model, Analysis & Search — science-specific, fill in.
- **HPC Interface:** `parse_fit_args()` and `__main__` — leave unchanged.

__HPC Interface (usage)__

GPU batch scripts call:

    python3 scripts/fit.py --sample=<sample> --dataset=<dataset>

CPU batch scripts call:

    python3 scripts/fit.py --sample=<sample> --dataset=<dataset> --use_cpu --number_of_cores=$THREADS

`--use_cpu` signals a CPU run (disable JAX/GPU paths in a JAX-able likelihood;
`use_jax=not use_cpu` is the usual wiring) and `--number_of_cores` sets the sampler's
multicore parallelism; on GPU the sampler runs single-core and JAX handles parallelism.
"""

import argparse
import os
from pathlib import Path

"""
__Configuration__

Anchor config and output to the project root (the directory holding this script's
parent), so the script behaves identically from a local shell and from a SLURM batch
working directory (`PyAutoConf:autoconf/conf.py`).
"""
PROJECT_PATH = Path(__file__).resolve().parents[1]

from autoconf import conf

conf.instance.push(
    new_path=str(PROJECT_PATH / "config"),
    output_path=str(PROJECT_PATH / "output"),
)

import autofit as af  # noqa: E402  (import after conf push, workspace convention)


def fit(sample: str, dataset: str, use_cpu: bool, number_of_cores: int) -> None:
    """
    __Dataset__

    Load the dataset named by the batch script. Replace with your project's loading —
    the convention is dataset/<sample>/<dataset>/ holding whatever your likelihood
    needs (see the dataset's README).
    """
    dataset_path = PROJECT_PATH / "dataset" / sample / dataset

    raise NotImplementedError(
        f"Fill in the Dataset and Model/Analysis/Search sections for {dataset_path}. "
        "Your wrapped likelihood (af_wrap_likelihood) and composed model "
        "(af_compose_model) go here."
    )

    """
    __Model, Analysis & Search__

    Compose the model, build the Analysis around your likelihood, configure the search
    with `number_of_cores=number_of_cores` and a `unique_tag=dataset` so every array
    task writes to its own output path, then `search.fit(...)`.
    """


"""
__HPC Interface__

Leave unchanged — the batch templates depend on this exact argument contract.
"""


def parse_fit_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a PyAutoFit model-fit (HPC interface).")
    parser.add_argument("--sample", type=str, required=True, help="dataset/<sample>/ group dir")
    parser.add_argument("--dataset", type=str, required=True, help="dataset name inside the sample dir")
    parser.add_argument("--use_cpu", action="store_true", help="CPU run: disable JAX/GPU paths, enable multicore sampling")
    parser.add_argument("--number_of_cores", type=int, default=1, help="sampler multicore parallelism (CPU runs)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_fit_args()
    if args.use_cpu:
        os.environ.setdefault("JAX_PLATFORM_NAME", "cpu")
        os.environ.setdefault("JAX_PLATFORMS", "cpu")
    fit(
        sample=args.sample,
        dataset=args.dataset,
        use_cpu=args.use_cpu,
        number_of_cores=args.number_of_cores,
    )
