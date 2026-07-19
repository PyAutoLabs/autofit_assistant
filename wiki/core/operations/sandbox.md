---
title: Sandbox and environment variables
sources:
  - project: PyAutoNerves
    paths:
      - autoconf/
    pinned_commit: 89c4714449797b0c049e8a95d16d499c863f4811
last_updated: 2026-07-10
content_sha256: 68b1f5e3b5b36fbb2b8fa030ba41f0d1de8df8d8fb830fc0b729c5c8a0a644f1
---

# Sandbox and environment variables

Environment variables that matter when running in restricted filesystems (CI
containers, sandboxed agents) or when smoke-testing scripts:

| Variable | Effect | When |
|---|---|---|
| `NUMBA_CACHE_DIR=/tmp/numba_cache` | writable numba JIT cache | any environment where the default cache dir is read-only |
| `MPLCONFIGDIR=/tmp/matplotlib` | writable matplotlib config | same |
| `PYAUTO_TEST_MODE=1` | searches do a fast, non-converging pass; output namespaced under `output/test_mode/` | smoke-testing a script's plumbing — **never** real inference |
| `PYAUTO_SKIP_API_GATE=1` | bypasses the PreToolUse code gate | deliberate pre-refactor/debugging work only |

Canonical smoke-test invocation:

```bash
PYAUTO_TEST_MODE=1 NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib \
  python scripts/<script>.py
```

Note the test-mode namespacing: anything that composes output paths by hand will miss
`output/test_mode/` — one more reason the rule is "reload via the aggregator, never
hand-compose paths" ([[../concepts/samples_and_posteriors]]).
