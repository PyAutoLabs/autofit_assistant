# wiki/

Three independently maintained sub-wikis. Each one answers a different question.

| Sub-wiki | Question | Provenance | Edited by |
|---|---|---|---|
| [`core/`](./core/) | *What is X / which X / why X* in the PyAuto\* stack and the statistics it implements? | Curated from source repos listed in [`../sources.yaml`](../sources.yaml) | `af_update_wiki` skill, against pinned source commits |
| [`literature/`](./literature/) | *What does the literature of **your** scientific domain say about X?* | Grown per-clone from the papers the user ingests. Schema in [`literature/AGENTS.md`](./literature/AGENTS.md). | The user (via `af_ingest_paper`), extending their domain wiki |
| [`project/`](./project/) | *What did we do in this fork, and why?* | Dated journal entries | Agent + user, every meaningful session |

**The key structural difference from a domain assistant** (e.g. `autolens_assistant`):
there, `literature/` ships full of strong-lensing science; here it ships **near-empty by
design**, because PyAutoFit has no fixed domain. The schema, index and bibliography
machinery are all in place — the *content* arrives when you adapt the assistant to your
field.

## When to read which

- A user asks **"what's the difference between Nautilus and Dynesty?"** →
  `core/concepts/` (searches).
- A user asks a question about *their scientific field* → `literature/` (follow
  `literature/index.md`; if it's silent, offer `af_ingest_paper` rather than guessing).
- A user asks **"what fits have we already tried on this dataset?"** → `project/`, grep
  for the dataset name.

## When to write which

- **`core/`** is treated as read-only outside of `af_update_wiki` runs. Don't edit pages
  ad-hoc as part of unrelated work.
- **`literature/`** has its own schema (see [`literature/AGENTS.md`](./literature/AGENTS.md))
  with `concepts/`, `entities/`, and `sources/` page types and `[[wiki-link]]`
  cross-references. Extend it when a new paper is read, following that schema. Don't
  treat it as scratch space.
- **`project/`** is append-only. After any session where the agent helps with a real
  modeling decision, dataset change, pipeline tweak, or interpretation, ask the user
  whether to add a journal entry. Use [`project/_template.md`](./project/_template.md).

## Sub-wiki layout

```
wiki/
├── README.md            # this file
├── core/                # PyAuto* API + statistics reference
│   ├── README.md  index.md
│   ├── stack/  concepts/  operations/
├── literature/          # the USER'S domain scientific reference (ships near-empty)
│   ├── AGENTS.md        # schema + usage rules (canonical; CLAUDE.md imports it)
│   ├── README.md  index.md  log.md
│   ├── concepts/  entities/  sources/  bibliography/
└── project/             # running journal for this fork
    ├── README.md
    ├── _template.md     # dated-entry template
    └── _profile_template.md
```
