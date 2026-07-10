---
title: PyAutoConf (autoconf)
sources:
  - project: PyAutoConf
    paths:
      - autoconf/
    pinned_commit: 5e784ca9291a0057e82ddf810912cd39e7665775
last_updated: 2026-07-10
content_sha256: 0696bbee076d6e484e290c345ec017479c7a69477a387a300f790a4eda9afa63
---

# PyAutoConf (`autoconf`)

The configuration layer under the whole PyAuto family. For an autofit user it
matters in three places:

1. **Config trees.** The workspace's `config/` directory is an autoconf config tree:
   `general.yaml`, `logging.yaml`, `output.yaml`, `non_linear/*.yaml` (per-search
   defaults), `priors/*.yaml`, `visualize/*.yaml`. Values resolve **workspace-first**:
   a key present in the project's `config/` overrides the library default — which is
   how a project retunes a sampler or an output policy once, globally
   (`PyAutoConf:autoconf/conf.py`).
2. **Default priors by class.** `config/priors/<Class>.yaml` (or module-level files)
   supply priors for model classes so scripts need not repeat them — the right home
   for a project's standard parametrisation. Note: autoconf lowercases YAML dict
   keys on load — keep config keys snake_case-lowercase.
3. **Serialisation.** The dictable machinery (`autoconf.dictable`) underlies model
   JSON round-tripping ([[../concepts/model_composition_and_priors]] "Serialisation").

Users rarely import `autoconf` directly; they feel it through `config/` behaviour.
When a config value seems ignored, check resolution order (is a workspace file
shadowing the library default?) before suspecting the library.
