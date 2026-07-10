# wiki/core/

Curated reference content for the PyAutoFit stack and the statistics it implements. The
core wiki documents *what* the API contains and *why* the inference methods work the way
they do; the skills in [`../../skills/`](../../skills/) document *how* to use them. The
two siblings — [`../literature/`](../literature/) and [`../project/`](../project/) — hold
the user's domain papers and a per-clone journal respectively (see
[`../README.md`](../README.md) for the overview).

## Organisation

- [`index.md`](./index.md) — top-level map; the entry point for an agent or human
  reader.
- `stack/` — one page per source library (`autoconf`, `autofit`), plus an overview of
  how they fit together.
- `concepts/` — statistics + framework explanations: priors, model composition,
  searches, samples, graphical models, evidence.
- `operations/` — installation, sandbox tuning, HPC.

## Page format

Every wiki page begins with YAML frontmatter:

```yaml
---
title: <Page title>
sources:
  - project: PyAutoFit
    paths:
      - autofit/non_linear/search/nest/nautilus/
    pinned_commit: <sha-or-tag>
last_updated: 2026-07-10
---
```

The `sources` field is what the `af_update_wiki` skill reads to know when a page is
stale relative to upstream. After every source file change between `pinned_commit` and
current HEAD, the relevant section of the page is rewritten and `pinned_commit` is
bumped.

## Read-only rule

`wiki/core/` is read-only outside `af_update_wiki` maintenance runs — see `AGENTS.md`
"Safety invariants".
