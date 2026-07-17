"""
The read-only results-inspector MCP server.

`tools.py` holds the plain tool functions (no MCP dependency — the test suite
exercises them directly); `server.py` registers them with an MCP stdio server;
`python -m autoassistant.mcp` runs it. Documentation, client configuration and
the design rules live in `skills/af_inspect_results_mcp.md`.
"""
