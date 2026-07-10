# bibliography/

Canonical citation metadata for the literature wiki.

- `literature.bib` — canonical BibTeX entries, one per ingested paper. Created on first
  ingestion.
- `bibkey_aliases.yaml` — maps known alternate keys to canonical keys, so downstream
  LaTeX projects with their own `.bib` conventions can be patched without duplication.

## Rules

- A paper enters the wiki with **verified** public metadata: arXiv ID, DOI, or a full
  journal reference. Never fabricate fields; if a field can't be verified, leave it out
  and add a TODO in the source entry.
- Canonical keys are local to this repository (`AuthorYYYY` style, disambiguated with
  `a`/`b` suffixes). Before citing into an external LaTeX project, resolve against that
  project's `.bib` and prefer its existing local key — record the mapping in
  `bibkey_aliases.yaml`.
- Never record local PDF paths. PDFs stay outside the repo (the gitignored `papers/`
  convention), and pages cite by public reference only.

Validation (`python -m autoassistant.literature validate-citations`) lands with the
Phase 1 tooling ([autofit_assistant#1](https://github.com/PyAutoLabs/autofit_assistant/issues/1)).
