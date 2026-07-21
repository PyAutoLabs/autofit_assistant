"""
The read-only results-inspector MCP server.

The tool core is the ``autofit[mcp]`` extra (``autofit.mcp``); `server.py` is a
thin launcher that pins this assistant's config and serves the core tools over
an MCP stdio server. `python -m autoassistant.mcp` runs it. Documentation, client
configuration and the design rules live in `skills/af_inspect_results_mcp.md`.
"""
