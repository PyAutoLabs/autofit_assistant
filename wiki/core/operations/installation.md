---
title: Installation
sources:
  - project: PyAutoFit
    paths:
      - pyproject.toml
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: 20af1b79664d3bfc1a6f9fe46c5f1038a7bf5e932cbecd6ba4bdb7498a3ad789
---

# Installation

The short version — full guided procedure in the `af_setup_environment` skill:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install autofit          # pulls autoconf transitively
python -c "import autofit; print(autofit.__version__)"
```

- **Python**: ≥ 3.9 declared; 3.11 recommended (what the tooling targets).
- **JAX extra**: `pip install "autofit[jax]"` when the likelihood is JAX-differentiable
  and gradient-based search (`af.BlackJAXNUTS`) is wanted.
- **Editable clones** (to read/modify library source): clone `PyAutoConf` then
  `PyAutoFit` (URLs in `sources.yaml`), `pip install -e` each in that order.
- **Your own dependencies** install alongside in the same venv — the assistant never
  reshapes your code to fit the environment.

The workspace pins its validated stack version in `version.txt` +
`wiki/core/api_audit_baseline.json`; the session-start drift-check
(`python autoassistant/audit_skill_apis.py --check-version`) tells you when the
installed stack has moved beyond what these docs were validated against.
