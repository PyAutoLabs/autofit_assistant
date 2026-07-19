"""Regression tests for the PyAuto* installation preflight."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "autoassistant" / "audit_skill_apis.py"
ENV = {
    **os.environ,
    "NUMBA_CACHE_DIR": "/tmp/numba_cache",
    "MPLCONFIGDIR": "/tmp/matplotlib",
    "PYAUTO_SKIP_WORKSPACE_VERSION_CHECK": "1",
}


def _run(*args: str, isolated: bool = False, env: dict[str, str] | None = None):
    command = [sys.executable]
    if isolated:
        command.append("-S")
    command.extend([str(VALIDATOR), *(args or ("--check-install",))])
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env or ENV,
        timeout=180,
    )


def test_install_preflight_reports_ready_environment():
    process = _run()

    assert process.returncode == 0
    assert "[install] READY" in process.stdout
    assert f"python: {sys.executable}" in process.stdout
    assert "autofit:" in process.stdout
    assert "install type:" in process.stdout


def test_install_preflight_distinguishes_absent_stack():
    process = _run(isolated=True, env={**ENV, "PYTHONPATH": ""})

    assert process.returncode == 2
    assert "[install] NOT INSTALLED" in process.stderr
    assert "missing from this interpreter" in process.stderr
    assert "af_setup_environment.md" in process.stderr


def test_install_preflight_distinguishes_broken_import(tmp_path):
    for package in ("autonerves", "autofit"):
        package_path = tmp_path / package
        package_path.mkdir()
        body = (
            "raise RuntimeError('broken dependency')\n"
            if package == "autofit"
            else "__version__ = 'test'\n"
        )
        (package_path / "__init__.py").write_text(body, encoding="utf-8")

    process = _run(isolated=True, env={**ENV, "PYTHONPATH": str(tmp_path)})

    assert process.returncode == 3
    assert "[install] IMPORT FAILED" in process.stderr
    assert "autofit import failed: RuntimeError: broken dependency" in process.stderr
    assert "missing from this interpreter" not in process.stderr


def test_version_check_routes_absent_stack_to_install_preflight():
    process = _run("--check-version", isolated=True, env={**ENV, "PYTHONPATH": ""})

    assert process.returncode == 2
    assert "[install] NOT INSTALLED" in process.stderr
    assert "API DRIFT" not in process.stderr


def test_write_baseline_refuses_dev_stack(tmp_path, monkeypatch):
    """The baseline contract is 'validated against this RELEASED stack'; a dev-source
    stack's version string can trail PyPI (wheels/tags-only nightlies), so snapshotting
    one without --allow-dev-stack must refuse."""
    import importlib.util
    import sys as _sys

    spec = importlib.util.spec_from_file_location(
        "audit_under_test_baseline", ROOT / "autoassistant" / "audit_skill_apis.py"
    )
    mod = importlib.util.module_from_spec(spec)
    _sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

    dev_check = mod.InstallationCheck(
        status="ready", python="py", prefix="env", versions={}, locations={},
        missing=[], errors={}, install_kind="source checkout or PYTHONPATH install",
        cache_defaults={},
    )
    monkeypatch.setattr(mod, "inspect_installation", lambda: dev_check)

    import pytest as _pytest

    with _pytest.raises(SystemExit) as exc:
        mod.write_baseline(tmp_path)
    assert "refusing to write" in str(exc.value)

    # With the explicit flag the same stack is snapshotted deliberately.
    path = mod.write_baseline(tmp_path, allow_dev_stack=True)
    assert path.exists()
