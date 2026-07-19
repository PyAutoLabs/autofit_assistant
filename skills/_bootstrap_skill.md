---
name: _bootstrap_skill
description: Meta-skill the agent runs when a user requests an inference capability that isn't covered by an existing skill. Walks through confirming scope, identifying source repos, reading the relevant API, drafting the new skill in the workspace house style, adding any missing wiki content, and registering the skill in the index. Use only when a genuinely new skill is needed — don't invoke for variants that an existing skill already handles.
---

# Bootstrapping a new workspace skill

When the user wants something this workspace can't already do, your job is to create a
new skill that can do it, and to teach the user the underlying API along the way. This
file is the protocol.

The output of running this skill is:

- A new `skills/af_<name>.md` file authored against `skills/_style.md`.
- A symlink at `.claude/skills/af_<name>.md` pointing to `../../skills/af_<name>.md`.
- An updated `skills/README.md` entry.
- Optionally, one or more new wiki pages the new skill links into.
- A working `.py` script in `scripts/` that demonstrates the new skill on the user's data.

## Step 1 — confirm scope with the user

Before reading any code, restate the requested capability and confirm it with the user.
Be explicit about what the skill will and won't do. A skill that tries to cover three
different inference tasks is worse than three small skills. If the request spans more
than one task, propose a split and ask which to write first.

Also confirm:

- The shape of the user's problem (own likelihood code vs. a PyAutoFit built-in model;
  one dataset vs. many; single fit vs. model comparison vs. graphical/hierarchical).
- The user's depth (inference newcomer / API-newcomer / returning) — this changes the
  framing.
- Whether they have real data to validate the skill on, or want a synthetic dataset
  first (in which case the new skill may chain into `af_simulate_dataset`).

## Step 2 — read the house style

Read [`_style.md`](./_style.md) end-to-end. The new skill must match its conventions:
Orient → Ask → Branch → Combine arc, five properties (inference first, encourage
reading, conversational, composes, records to the project wiki), python-first, source
citations as `<Project>:<path>`.

## Step 3 — identify source repos

Open [`../sources.yaml`](../sources.yaml). Decide which projects the new skill needs to
touch. Common patterns:

- Model composition, priors, searches, samples, aggregator, graphical models →
  `PyAutoFit`.
- Configuration option → `PyAutoNerves` + the config you're touching.
- Construction idioms and worked examples → `autofit_workspace` (read-only reference).

If the new skill needs a repo not in `sources.yaml`, add it there first (with a `name`,
`import`, `role`, and `git` URL) and tell the user what you added.

## Step 4 — read inside the source repos

You need real API knowledge, not guesses. Either:

```bash
python -c "import autofit, pathlib, inspect; print(pathlib.Path(inspect.getfile(autofit)).parent)"
```

…and read from the installed location, or clone the repo from its git URL into
`./sources/<project>/` (gitignored) and read from there:

```bash
mkdir -p sources && git clone <git_url_from_sources_yaml> sources/<project>
```

Read the relevant module(s). Identify:

- The class(es) the new skill will instantiate or subclass.
- Their constructor signatures and key methods.
- Existing usage patterns in `PyAutoFit/test_autofit/` (tests) or
  `autofit_workspace/scripts/` (tutorials).

Take notes; quote signatures in the new skill where they matter.

## Step 5 — locate or draft the wiki page

For every concept the new skill teaches, identify the matching wiki page. If one exists,
the skill will link to it (don't restate the wiki). If it doesn't exist, draft the wiki
page in the same change.

A new wiki page has:

- Frontmatter listing the `sources` (project + paths + pinned commit).
- A short overview of the concept.
- A table or list of the API surface (classes / functions / configs).
- Links to ReadTheDocs or other primary references.

See `wiki/README.md` for the wiki page template.

## Step 6 — draft the skill

Save the new skill at `skills/af_<task>.md`. Follow `_style.md`:

- Frontmatter `name:` matches the filename (without extension).
- Frontmatter `description:` is one paragraph; a future agent must be able to decide
  whether to activate this skill from the description alone.
- Body uses Orient → Ask → Branch → Combine.
- Python recipes are full, runnable snippets — not pseudocode.
- Every code-aware concept cites `<Project>:<path>` and links to the wiki page.

## Step 7 — register the skill

```bash
ln -s ../../skills/af_<task>.md .claude/skills/af_<task>.md
```

Add a one-line entry under the appropriate category in `skills/README.md`.

## Step 8 — verify

Write the Python script the new skill recommends — for the user's actual data, in
`scripts/`. Run it with:

```bash
PYAUTO_TEST_MODE=1 NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib \
  python scripts/<script>.py
```

If it doesn't run, fix the skill. Don't ship a skill whose recipe doesn't execute.

When it runs, tell the user:

- What the new skill is called and where it lives.
- The path to the generated script.
- What wiki pages were added or updated.
- One or two natural next-step skills the user can chain into.

## When NOT to bootstrap a new skill

- The request is a small variant of an existing skill — extend the existing skill
  instead.
- The request is essentially "run this existing tutorial script for me" — point the
  user at the existing script in `autofit_workspace` and the relevant wiki page, but
  don't wrap it in a new skill.
- The request requires source code we genuinely cannot read (closed-source dep, dead
  link). Surface this to the user and don't fake it.

## Agent procedural checklist (slim, for your sanity)

1. Confirm scope with the user, propose a name.
2. Read `_style.md`.
3. Resolve source repos from `sources.yaml`; clone or import as needed.
4. Read the relevant source. Take signature notes.
5. Read or draft the matching wiki page(s).
6. Write `skills/af_<task>.md`.
7. Add symlink under `.claude/skills/`; add entry to `skills/README.md`.
8. Generate the user-specific script in `scripts/`. Run it with `PYAUTO_TEST_MODE=1`.
9. Report to the user: skill name, script path, new wiki pages, suggested chain.
