# skills/

Procedural how-to-do-X skills for PyAutoFit-driven statistical inference. Each skill is a
single Markdown file with YAML frontmatter; the body teaches an agent (and through them,
the user) how to write Python that accomplishes one inference task.

Skills are also exposed at `.claude/skills/` (Claude Code) and `~/.codex/skills/` (when
configured) via symlinks; the canonical files live here.

## Conventions

- File names use the `af_<task>` convention for inference-API skills, e.g.
  `af_run_search.md`.
- Project-workflow skills (repo-level operations, template manipulation) use a plain
  kebab-case name, e.g. `start-new-project.md`.
- Meta-skills (writing guide, bootstrap protocol) start with `_`.
- Every inference-API skill is **python-first**: the deliverable is a runnable `.py`
  script + the understanding to evolve it. Project-workflow skills may instead drive
  `rsync`, `cp`, or other repo-level operations.
- Source citations use the project-name + repo-relative-path form,
  e.g. `PyAutoFit:autofit/non_linear/search/nest/nautilus/`, resolved via
  [`../sources.yaml`](../sources.yaml).
- Wiki references use workspace-relative paths,
  e.g. `wiki/core/concepts/non_linear_search.md`.

## Index

> 🚧 The `af_*` skill set is being built
> ([roadmap: issue #1](https://github.com/PyAutoLabs/autofit_assistant/issues/1)).
> This index lists what exists now; the planned set (workspace pairing, domain
> adaptation, results analysis) lands phase by phase.

### Meta

- [`_style.md`](./_style.md) — writing guide every skill is authored against. Read first
  before adding or editing any skill.
- [`_bootstrap_skill.md`](./_bootstrap_skill.md) — protocol for authoring a new skill on
  demand when a user requests a capability not yet covered.
