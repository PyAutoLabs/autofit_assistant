# wiki/literature/

The literature sub-wiki holds compiled syntheses of the scientific literature of **your
domain**: concepts, named entities (surveys, instruments, software, collaborations), and
per-paper bibliography pages.

> **Authoritative schema:** [`AGENTS.md`](./AGENTS.md) describes the page types,
> frontmatter, cross-reference convention (`[[page-slug]]`), and how an assistant
> should use this wiki. Read it before adding or editing pages.

**It ships near-empty by design.** PyAutoFit has no fixed scientific domain, so unlike a
domain assistant there is no base corpus to ship — the machinery (schema, index, log,
bibliography) is all here, and the content arrives as you adapt the assistant to your
field via `af_ingest_paper`.

It is self-contained: every page stands on its own and papers are cited by arXiv/DOI
link and/or author-year citation, never by a local file path.

## Layout

| Folder | Page type | Scope |
|---|---|---|
| `concepts/` | concept | one scientific concept per page |
| `entities/` | entity | one named thing per page (survey, instrument, code, collaboration) |
| `sources/` | sources | compact claim support, one paper section per topic |
| `bibliography/` | metadata | canonical BibTeX, key aliases, and citation workflow |
| `index.md` | meta | top-level navigation |
| `log.md` | meta | append-only compilation log |
