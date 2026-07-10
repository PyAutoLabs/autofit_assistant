---
title: HPC — running fits on a cluster
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/search/abstract_search.py
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: d0f060a5ae9c2a941f7ec14bbca725461d1ff3503b46bb4b446495cf020c3eb8
---

# HPC — running fits on a cluster

When a fit's runtime estimate (cost per likelihood call × sampler budget) outgrows a
laptop, the analysis moves to a cluster. The concepts that transfer:

- **Estimate before you queue.** Time one likelihood call; multiply by the sampler's
  expected evaluations. Queue time + wrong-sized request costs more than the
  measurement ever does.
- **Cores**: every search takes `number_of_cores` — likelihood evaluations
  parallelise within one node. Match it to the job request; over-subscription
  thrashes.
- **Resumption is free**: a completed or killed search resumes from `output/` on
  re-run (same `path_prefix`/`name`/`unique_tag`) — design job scripts to simply
  re-execute the same script after time-limit kills.
- **Environment**: activate the project venv inside the job script
  (`source $PROJECT_PATH/activate.sh` — it resolves relative to its own location);
  set the writable cache dirs ([[sandbox]]).
- **Secrets discipline**: cluster hostnames/aliases are constraints recorded in
  `wiki/project/profile.md` ("HPC access"); credentials never enter the repo.

The shipped infrastructure lives in `hpc/`: SLURM batch templates
(`hpc/batch_cpu/template`, `hpc/batch_gpu/template` — one dataset per array task,
thread pinning, `--use_cpu` wiring), the `hpc/sync` push/pull CLI
(`hpc/sync.conf.example` documents the gitignored per-machine config), and
`hpc/template.py`, the fit-script template whose `parse_fit_args`/`__main__` interface
the batch templates depend on. Default posture stays prepare-only: the assistant writes
and configures; the user submits.
