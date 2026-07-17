---
name: af_inspect_results_mcp
description: Run and configure the read-only results-inspector MCP server, which lets chat harnesses without code execution (Claude Desktop, Claude Code) inspect PyAutoFit output directories — list fits ranked by evidence, read model and posterior summaries, and view result images inline in chat. Use when the user wants to "browse/inspect my results from chat", asks about the MCP server, or wants Claude Desktop wired to their output folder. Not for loading results in Python (that is `af_load_results`) and not for running fits.
user-invocable: true
---

# The results-inspector MCP server

`autoassistant/mcp/` is a read-only MCP (Model Context Protocol) stdio server over
PyAutoFit output directories. It exists for harnesses that cannot execute code — a
Claude Desktop chat gets tools to list fits, read summaries and display result images
inline, against the same `output/` folder a script-based session works with.

It is deliberately **not** a fitting interface: composing models and running searches
stay python-first through the other skills. Exposing `search.fit` through a JSON tool
schema flattens the compositional API and is out of scope by design.

## Orient

- Server: `autoassistant/mcp/server.py`, run as `python -m autoassistant.mcp` from the
  repo root (stdio; nothing listens on a port).
- Requires the `mcp` package in the PyAutoFit environment: `pip install mcp`
  (assistant-environment dependency only — never add it to library requirements).
- All tools are read-only; exceptions surface as MCP tool errors, nothing is written.

## Tools

| Tool | Returns |
|------|---------|
| `list_searches(directory, sort_by="log_evidence", limit=20, completed_only=False)` | One row per fit found recursively: name, unique tag, directory, completion, log evidence, max log likelihood, free-parameter count. Row `directory` values feed the other tools. |
| `get_model(directory)` | Human-readable model `info` + full model dict. |
| `get_result_summary(directory)` | The `model.results` text. |
| `get_samples_summary(directory)` | Log evidence, max log likelihood, parameter paths, max-LH and median-PDF vectors (`None` fields where a search legitimately lacks them, e.g. MLE). |
| `get_search_info(directory)` | Search name, unique tag, completion, serialized settings. |
| `list_images(directory)` | Names of `image/*.png` visualizations. |
| `fetch_image(directory, name="subplot_fit")` | The image itself, rendered inline in chat. |

Wrappers over `PyAutoFit:autofit/aggregator/aggregator.py` (`Aggregator.from_directory`)
and `PyAutoFit:autofit/aggregator/search_output.py` (`SearchOutput`).

## Configure a client

**Claude Desktop** (`claude_desktop_config.json`, Settings → Developer → Edit Config):

```json
{
  "mcpServers": {
    "pyauto-results-inspector": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["-m", "autoassistant.mcp"],
      "env": { "PYTHONPATH": "/absolute/path/to/autofit_assistant" }
    }
  }
}
```

Use the interpreter that has PyAutoFit + `mcp` installed. Ask about fits by absolute
path ("list the fits under /home/me/project/output ranked by evidence").

MCP clients spawn the server with a **minimal environment** — nothing from your shell
propagates. Anything the stack needs (`PYTHONPATH` for editable/source checkouts,
`NUMBA_CACHE_DIR`/`MPLCONFIGDIR` in restricted setups) must be declared in the
config's `env` block.

**Claude Code**: the repo-root `.mcp.json` registers the same server automatically for
sessions opened in this repo (marginal there — a Claude Code session can already run
the aggregator in Python — but it costs nothing and exercises the same wiring).

## Deployment tiers

1. **Local stdio (built, above)** — Claude Desktop / Claude Code on the machine that
   holds `output/`.
2. **Remote (documented only)** — claude.ai web/mobile custom connectors and ChatGPT
   developer mode speak MCP but only to servers reachable over the public internet
   (no stdio): expose the server via `mcp.run(transport="streamable-http")` behind an
   ngrok/cloudflared tunnel. Not built or hardened here; do not tunnel a machine you
   care about without thinking about auth.
3. **Hosted (future)** — a collaboration-scale deployment next to shared outputs
   (e.g. sample-wide triage). Same tools; hosting, auth and scale are its own task.

## Design rules (maintainers)

- **Glue, not code.** Every tool is argument parsing + one existing public PyAutoFit
  call + serialization. If a tool needs more, add the method to PyAutoFit first.
- **Read-only.** No fit-running, no compute, no writes into `output/`.
- **stdout is the protocol.** Autofit calls run under `tools._stdout_to_stderr()` and
  `server._route_logging_to_stderr()` rebinds stdout log handlers — keep both when
  adding tools; a single stray print corrupts the JSON-RPC channel.
- **Anti-drift.** `autoassistant/mcp/*.py` is scanned by `al`/`af` symbol audits via
  `autoassistant/audit_skill_apis.py` (`--scope scripts`); tests
  (`autoassistant/tests/test_mcp_tools.py`) build their fixture by running a real
  tiny fit so format drift fails loudly.
