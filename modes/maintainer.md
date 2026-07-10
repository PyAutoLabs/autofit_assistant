# Maintainer mode

Active when `.maintainer` exists at the repo root (gitignored; `touch .maintainer` /
`rm .maintainer`). The session is **assistant-maintenance** — editing the constitution,
skills, wiki schema, hooks, or infrastructure — not user inference work. `AGENTS.md`
"Session start" routes here when the sentinel is present.

## What changes

- Skip the `wiki/project/profile.md` read/create and the newcomer-mode defaults.
- Skip the session-start API drift-check by default (run it manually before testing any
  generated script).
- **No auto-commit.** The maintainer drives every commit; stage explicitly, announce, and
  never push.
- Don't offer to add `wiki/project/YYYY-MM-DD-*.md` entries.
- The **source-edit boundary** is lifted: you may edit `wiki/core/`, hooks, and assistant
  infrastructure (that is the point of maintenance work).

## What does NOT change

- Every safety invariant in `AGENTS.md` still applies — in particular the two hard-absolutes
  (the data-inspection gate and never-rewrite-history), plus bulk-edit safety and the
  `output/` write-ban.
- Commits still end with the `Co-Authored-By: Claude <model> <noreply@anthropic.com>` trailer.

## Maintainer procedures

Use the existing skills, not new docs:

- Authoring or evolving a skill → [`skills/_bootstrap_skill.md`](../skills/_bootstrap_skill.md).
- Regenerating `wiki/core/` against pinned sources → `af_update_wiki`.
- API gate / version baseline → [`skills/af_audit_skill_apis.md`](../skills/af_audit_skill_apis.md).

## Relationship to autolens_assistant (the reference implementation)

`autolens_assistant` is the reference implementation this assistant is modelled on; its
maintainer doc carries the canonical **generic-vs-domain-specific seam** every PyAuto
assistant respects. When maintaining this repo:

- **Generic infrastructure** (constitution skeleton, modes, skills framework, wiki split,
  science-project lifecycle, `sources.yaml` pattern, API gate, benchmark machinery) should
  stay structurally aligned with `autolens_assistant` — if you improve the pattern here,
  consider whether the improvement belongs upstream in the reference too, and vice versa.
- **Domain content** is where this repo deliberately differs: `af_*` skill bodies target
  generic inference; `wiki/core/` teaches statistics rather than lensing; and
  `wiki/literature/` ships **near-empty by design** — it is the *user's* domain wiki,
  grown through domain adaptation, not a shipped corpus.

## Release-time wiki-currency check

The currency rules (symbol audit, idiom deny-list, provenance, citation paths, version
drift) live in exactly one place —
[`.github/workflows/wiki-currency.yml`](../.github/workflows/wiki-currency.yml), driving
`autoassistant/audit_skill_apis.py` — and run on every PR (plus `workflow_dispatch`, and
`workflow_call` for PyAutoBuild releases once the release-side wiring lands). When you
change the rules, edit them there only.
