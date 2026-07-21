"""
The read-only results-inspector MCP stdio server.

The tool core is the ``autofit[mcp]`` extra (``autofit.mcp``); this thin launcher
pins the assistant's config and hardens stdout before importing it, then serves
the core tools unchanged. Run with ``python -m autoassistant.mcp``; client
configuration and the design rules live in ``skills/af_inspect_results_mcp.md``.

Every tool is read-only: nothing here composes models, runs fits, or writes into
``output/``.
"""

# pyauto-api-gate: skip — this is a thin launcher, not skill-API surface. The
# read-only tool functions (and their `af.`/`autofit.aggregator` usage) graduated
# to the autofit[mcp] extra (`autofit.mcp`, covered by PyAutoFit's own tests); the
# only references here are internal imports of that library core.
import contextlib
import os
import sys
from pathlib import Path

# autofit reads autonerves config at import time, and jax's xla_bridge logs its
# backend probe to stdout during that import — both fatal to the JSON-RPC channel.
# So, before importing anything under autofit (including autofit.mcp): force CPU
# (skips the jax probe), pin config to this assistant's own config/ (so it does
# not depend on the launch directory), and guard the import's stdout. The pin uses
# only autonerves — it MUST precede the first autofit import, so it cannot come
# from a helper that itself lives under autofit.
os.environ.setdefault("JAX_PLATFORMS", "cpu")

from autonerves import conf

_config = Path(__file__).resolve().parents[2] / "config"
conf.instance = conf.Config(str(_config), output_path=str(_config.parent / "output"))

with contextlib.redirect_stdout(sys.stderr):
    from autofit.mcp import core_server

mcp = core_server()


if __name__ == "__main__":
    mcp.run()
