---
title: Installation
sources:
  - project: PyAutoFit
    paths:
      - pyproject.toml
    pinned_commit: 4592990b14cacab243cde9c17789d463ff4a674f
last_updated: 2026-07-10
content_sha256: 07e6c8ae383127cf837bb2b5007e078ec541477d31dd49f93ac07cbe83a56b8f
---

# Installation

The short version — full guided procedure in the `af_setup_environment` skill:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install autofit          # pulls autonerves transitively
python -c "import autofit; print(autofit.__version__)"
```

- **Python**: ≥ 3.9 declared; 3.11 recommended (what the tooling targets).
- **JAX extra**: `pip install "autofit[jax]"` when the likelihood is JAX-differentiable
  and gradient-based search (`af.BlackJAXNUTS`) is wanted.
- **Editable clones** (to read/modify library source): clone `PyAutoNerves` then
  `PyAutoFit` (URLs in `sources.yaml`), `pip install -e` each in that order.
- **Your own dependencies** install alongside in the same venv — the assistant never
  reshapes your code to fit the environment.

The workspace pins its validated stack version in `version.txt` +
`wiki/core/api_audit_baseline.json`; the session-start drift-check
(`python autoassistant/audit_skill_apis.py --check-version`) tells you when the
installed stack has moved beyond what these docs were validated against.
