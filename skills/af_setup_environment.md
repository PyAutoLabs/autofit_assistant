---
name: af_setup_environment
description: Detect, install, and configure a Python environment for the PyAutoFit stack. First checks the active interpreter and distinguishes an absent, broken, or ready stack; then offers pip in a venv (the normal user path) or editable clones (contributors). Sets sandbox cache env vars and verifies imports. Use when PyAutoFit is unavailable, imports fail, or a new machine needs setup.
---

# Setting up an environment for the PyAuto\* stack

This skill installs the libraries the workspace targets — PyAutoConf and PyAutoFit —
and prepares the sandbox so the rest of the skills will run. The user picks one of two
install modes only if the active environment is not already usable: pip (fastest path to
"import autofit works") or editable-clone (source-level access, slower but lets you read
and modify the libraries). Never install automatically without confirmation.

## Orient — inspect before installing

If the project has an `activate.sh`, source it first. Then run the cheap structured
preflight:

```bash
python autoassistant/audit_skill_apis.py --check-install
```

It reports the active Python executable and environment prefix, installed versions, the
loaded `autofit` path, and a best-effort install type. Its exit codes are:

- `0` — both PyAuto\* roots import; do not reinstall.
- `2` — packages are absent from this interpreter. The user may only need to activate
  the right environment, so check that before creating another one.
- `3` — packages were found but imports failed. Fix the reported dependency, cache, or
  partial installation error rather than treating it as ordinary version drift.

The probe supplies writable temporary defaults for numba and matplotlib caches when the
user has not configured them, preventing a read-only cache from being misreported as a
missing install. If the install is ready, continue to the user's actual inference task.
Only continue below when setup or repair is genuinely required.

## Ask

Before changing the environment, confirm with the user:

- Are you running on macOS, Linux, or Windows / WSL?
- Do you already have a Python environment manager (venv, conda, mamba)? If yes, will
  you use it for this workspace too?
- Do you need to *read or modify* the PyAuto\* source while you work (editable clone
  mode), or just *use* the libraries (pip mode)?
- Does your own likelihood/model code have dependencies of its own that must live in
  the same environment? (They install alongside — the assistant never modifies your
  code to fit the environment.)

Recommend a venv plus pip for most users. If they already use conda or mamba, it is fine
to create/activate the environment with that tool and then install PyAutoFit with pip
inside it; do not introduce conda solely for this package. Use editable clones only when
they need source access. If they pick pip, branch into "Pip install". If they want
editable clones, branch into "Editable clones".

For background on what each library does, point at `wiki/core/stack/overview.md`.

## Branch — Pip install

The simplest path. PyAutoFit declares autoconf as a transitive dep, so a single
`pip install` pulls everything in.

```bash
# Create or activate a Python 3.11 env (use whatever env manager you have)
python3.11 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install autofit
```

Python ≥ 3.9 works in principle (the repos declare `requires-python = ">=3.9"`); 3.11 is
the recommended baseline — it's what the workspace tooling targets. If the user's
likelihood is JAX-able and they want gradient-based tooling, `pip install "autofit[jax]"`
adds the JAX extra.

Verify:

```bash
python -c "import autofit, autoconf; print(autofit.__version__)"
```

If that prints a version (no traceback), the install is good.

## Branch — Editable clones

Use this when you want to read or modify the PyAuto\* source. Each repo is cloned, then
installed with `pip install -e .` in dependency order.

```bash
# Pick a parent directory for the source clones. The workspace's .gitignore excludes
# ./sources/ — clone there if you want the repos co-located with the workspace.
mkdir -p sources && cd sources

# Order matters — install from the bottom of the dependency chain up.
# URLs come from ../sources.yaml.
git clone https://github.com/PyAutoLabs/PyAutoConf.git
git clone https://github.com/PyAutoLabs/PyAutoFit.git

cd ..

python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

for repo in PyAutoConf PyAutoFit; do
    pip install -e "sources/$repo"
done
```

Resolve git URLs from [`../sources.yaml`](../sources.yaml) so the workspace stays the
source of truth; if you want to change a URL or add a repo, edit `sources.yaml` rather
than hand-editing this skill.

Verify the same way as for pip:

```bash
python -c "import autofit, autoconf; print(autofit.__version__)"
```

## Sandbox / restricted-filesystem environments

If you're in a CI container or anywhere caches cannot write to their default locations,
override them once per shell:

```bash
export NUMBA_CACHE_DIR=/tmp/numba_cache
export MPLCONFIGDIR=/tmp/matplotlib
```

You can also bake them into the venv activation script. `PYAUTO_TEST_MODE=1` makes
searches run a fast, non-converging pass for smoke-testing scripts — never use it for
real inference.

## Verification — write a one-off script

Save this to `scripts/verify_environment.py` and run it:

```python
import autoconf
import autofit as af

print("autoconf :", autoconf.__version__)
print("autofit  :", af.__version__)

# A minimal model composition — proves the inference stack is wired up.
class Gaussian:
    def __init__(self, centre=0.0, normalization=1.0, sigma=1.0):
        self.centre = centre
        self.normalization = normalization
        self.sigma = sigma

model = af.Model(Gaussian)
model.centre = af.UniformPrior(lower_limit=-1.0, upper_limit=1.0)
print("Model free parameters:", model.prior_count)
print("A random instance:", vars(model.random_instance()))
```

Run with sandbox env vars set if you need them:

```bash
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib \
  python scripts/verify_environment.py
```

If that prints versions, a parameter count and a random instance (no traceback), the
environment is ready for the rest of the skills.

## Combine — what to do next

Now you can:

- Compose your model with [`af_compose_model`](./af_compose_model.md).
- Configure and run a fit with [`af_configure_search`](./af_configure_search.md) and
  [`af_run_search`](./af_run_search.md).
- Load and inspect an existing fit's results with
  [`af_load_results`](./af_load_results.md).
- Refresh the wiki against installed sources with
  [`af_update_wiki`](./af_update_wiki.md).

## Further reading

- **General reference** — [RTD: PyAutoFit installation](https://pyautofit.readthedocs.io/en/latest/installation/overview.html):
  canonical installation guide — Python version, dependencies, troubleshooting.
