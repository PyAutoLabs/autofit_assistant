---
title: PyAutoNerves (autonerves)
sources:
  - project: PyAutoNerves
    paths:
      - autonerves/
    pinned_commit: 89c4714449797b0c049e8a95d16d499c863f4811
last_updated: 2026-07-10
content_sha256: 72fb17423e00b996f512f3799ee4d7a35cee3280760ce0f0c490386db51cb4e6
---

# PyAutoNerves (`autonerves`)

The configuration layer under the whole PyAuto family. For an autofit user it
matters in three places:

1. **Config trees.** The workspace's `config/` directory is an autonerves config tree:
   `general.yaml`, `logging.yaml`, `output.yaml`, `non_linear/GridSearch.yaml`,
   `priors/*.yaml`, `visualize/*.yaml`. Values resolve **workspace-first**: a key
   present in the project's `config/` overrides the library default — which is how a
   project retunes an output or visualization policy once, globally
   (`PyAutoNerves:autonerves/conf.py`). Individual searches are not configured here:
   their defaults are the keyword defaults of each search class.
2. **Default priors by class.** `config/priors/<Class>.yaml` (or module-level files)
   supply priors for model classes so scripts need not repeat them — the right home
   for a project's standard parametrisation. Note: autonerves lowercases YAML dict
   keys on load — keep config keys snake_case-lowercase.
3. **Serialisation.** The dictable machinery (`autonerves.dictable`) underlies model
   JSON round-tripping ([[../concepts/model_composition_and_priors]] "Serialisation").

Users rarely import `autonerves` directly; they feel it through `config/` behaviour.
When a config value seems ignored, check resolution order (is a workspace file
shadowing the library default?) before suspecting the library.
