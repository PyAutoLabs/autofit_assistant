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
> This index lists what exists now; the planned set (domain adaptation, search
> chaining, simulation, debugging) lands phase by phase.

### Meta

- [`_style.md`](./_style.md) — writing guide every skill is authored against. Read first
  before adding or editing any skill.
- [`_bootstrap_skill.md`](./_bootstrap_skill.md) — protocol for authoring a new skill on
  demand when a user requests a capability not yet covered.

### Setup & maintenance

- [`af_setup_environment.md`](./af_setup_environment.md) — detect absent or broken
  PyAuto\* installs; pip-in-venv or editable-clone setup; sandbox cache env vars.
- [`af_audit_skill_apis.md`](./af_audit_skill_apis.md) — audit every cited PyAuto\*
  symbol against the installed stack; owns the version baseline, idiom deny-list,
  provenance and citation-path checks.
- [`af_refresh_api_docs.md`](./af_refresh_api_docs.md) — the maintenance umbrella:
  symbol audit + wiki refresh + skill-recipe sweep in one pass.
- [`af_update_wiki.md`](./af_update_wiki.md) — refresh `wiki/core/` pages whose pinned
  source commits moved.

### Core inference

- [`af_compose_model.md`](./af_compose_model.md) — turn Python classes into
  `af.Model`/`af.Collection` with deliberate priors, fixing, linking and assertions.
- [`af_configure_search.md`](./af_configure_search.md) — choose and configure the
  non-linear search (nested / MCMC / MLE) for the problem at hand.
- [`af_run_search.md`](./af_run_search.md) — execute the fit, monitor output, first
  inspection of the Result; runtime triage.
- [`af_load_results.md`](./af_load_results.md) — posterior summaries, errors, evidence,
  and bulk result loading via the aggregator.

### Domain adaptation

- [`af_adapt_to_domain.md`](./af_adapt_to_domain.md) — the orchestrator: interview,
  drive the three adaptation channels, record everything durable in the profile.
- [`af_ingest_paper.md`](./af_ingest_paper.md) — add a verified paper from the user's
  field to the literature record (project-local or this clone's wiki).
- [`af_wrap_likelihood.md`](./af_wrap_likelihood.md) — wrap the user's existing
  likelihood code into an `Analysis` class, validated before any fit.

### Project workflow

- [`start-new-project.md`](./start-new-project.md) — the bridge to a standalone science
  project and its Create → Work → Collaborate → Publish lifecycle.
- [`contribute-upstream.md`](./contribute-upstream.md) — propose a scoped change back
  to `PyAutoLabs/autofit_assistant` as a draft PR.

### Utilities

- [`af_to_notebook.md`](./af_to_notebook.md) — convert a narrative-docstring script to
  a Jupyter notebook.
