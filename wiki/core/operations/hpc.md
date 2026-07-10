---
title: HPC — running fits on a cluster
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/search/abstract_search.py
    pinned_commit: 31537d5f5ae865aca69d10e6901741533116ed65
last_updated: 2026-07-10
content_sha256: 576d47ac519cb6d982d4b3dbc5af35f8383cc766402d1efdf5b3b603ab22091a
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

> 🚧 Shipped batch templates and a sync CLI (`hpc/`) land in Phase 4 of
> [autofit_assistant#1](https://github.com/PyAutoLabs/autofit_assistant/issues/1);
> until then the assistant writes SLURM scripts per the user's cluster docs, in
> prepare-only posture by default.
