---
title: The PyAutoFit stack — overview
sources:
  - project: PyAutoFit
    paths:
      - autofit/__init__.py
    pinned_commit: 31537d5f5ae865aca69d10e6901741533116ed65
  - project: PyAutoConf
    paths:
      - autoconf/__init__.py
    pinned_commit: 5e784ca9291a0057e82ddf810912cd39e7665775
last_updated: 2026-07-10
content_sha256: 37c8d4947e08d3285aace1874b93fd42a7617f9e564135128f3c536a25112cdd
---

# The stack

Two libraries, one dependency edge:

```
PyAutoConf (autoconf)   — configuration: YAML config trees, prior resolution
      ▲
PyAutoFit  (autofit)    — the inference engine: models, priors, searches,
                          samples, aggregator, graphical models
```

`pip install autofit` brings both. The user's own code sits **on top**: their classes
become models ([[../concepts/model_composition_and_priors]]), their likelihood becomes
an `Analysis`, and PyAutoFit supplies everything either side of that seam.

- What each library is: [[autofit]] · [[autoconf]].
- Domain layers (PyAutoGalaxy, PyAutoLens, …) are separate PyAutoLabs projects built
  on this same engine; this assistant deliberately targets the engine itself.

Standard import convention (`AGENTS.md` "Conventions"):

```python
import autofit as af
import autofit.plot as aplt   # when search visualisation is needed
```
