"""
# Experimental: PyAutoFit assistant in Colab

Install the assistant's PyAutoFit stack in a **fresh CPU runtime** and give Colab's
Gemini sidebar its context, then experiment in your own cells. Run the first two
cells in order; installation can take a few minutes.

This is a notebook experiment, not the full CLI assistant or an HPC service.
Cloning the repository does **not** make Gemini read its instructions. Step 2
provides context to copy into the sidebar explicitly. Gemini availability depends
on your Google account and Colab settings.

Save a copy of this notebook in Drive to keep your edits. Runtime files disappear
when Colab resets: download anything you want to keep before disconnecting.

__Contents__

1. Setup
2. Gemini context
3. Your sandbox
"""

import os
from pathlib import Path
import subprocess
import sys

# The public release includes the model, likelihood and assistant context used here.
ASSISTANT_REF = "2026.9.15.1"
STACK_VERSION = "2026.9.15.1"
COLAB_HOME = Path("/content")
repo = COLAB_HOME / "autofit_assistant"
if not repo.exists():
    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", ASSISTANT_REF,
         "https://github.com/PyAutoLabs/autofit_assistant.git", str(repo)],
        check=True,
    )
else:
    actual = subprocess.check_output(
        ["git", "-C", str(repo), "describe", "--tags", "--exact-match"], text=True
    ).strip()
    if actual != ASSISTANT_REF:
        raise RuntimeError("This folder has another assistant version; use a fresh runtime.")

subprocess.run(
    [sys.executable, "-m", "pip", "install", f"autofit=={STACK_VERSION}",
     f"autonerves=={STACK_VERSION}"], check=True,
)
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba_cache")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.chdir(repo)
sys.path.insert(0, str(repo))

import autofit as af
import autonerves

print("Assistant:", subprocess.check_output(
    ["git", "rev-parse", "HEAD"], text=True).strip())
print("PyAutoFit:", af.__version__, "PyAutoNerves:", autonerves.__version__)

"""
## 2. Give Gemini the assistant context

Run this cell, then **copy its printed text into the Gemini sidebar**. Ask Gemini
to acknowledge the supplied context before you start work. The context comes from
this pinned assistant checkout; no API key or Gemini SDK is needed.

What it sends: the parts of `AGENTS.md` a sidebar session can actually act on,
teacher and BYOL modes, and the skills for composing a model, wrapping a
likelihood, configuring and running a search, plotting a fit and debugging one
that fails. The rest of the assistant is left out deliberately — much of it
directs an agent that can read files and run commands, which the sidebar cannot.
Section 3 prints any other file on demand.

Only the text you supply is guaranteed to be part of that conversation. Sidebar
access to notebook content can vary: include the cell or error in your message
when needed.
"""

# The sidebar has no filesystem, so only what is pasted is in context. These
# AGENTS.md sections carry the invariants and the map; the omitted ones describe
# session start-up, commit cadence and maintainer workflows that cannot run here.
agents_sections = [
    "Safety invariants",
    "The three-layer model",
    "Domain adaptation",
]
context_paths = [
    "modes/teacher.md",
    "modes/byol.md",
    "skills/af_compose_model.md",
    "skills/af_wrap_likelihood.md",
    "skills/af_configure_search.md",
    "skills/af_run_search.md",
    "skills/af_plot_fit.md",
    "skills/af_debug_fit_failure.md",
]


def agents_excerpt(wanted):
    """Return the named `## ` sections of AGENTS.md, plus its preamble, in file order."""
    blocks = {"__preamble__": []}
    heading = "__preamble__"
    for line in Path("AGENTS.md").read_text().splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            blocks[heading] = []
        blocks[heading].append(line)
    excerpt = ["\n".join(blocks["__preamble__"]).strip()]
    for prefix in wanted:
        matched = [h for h in blocks if h.startswith(prefix)]
        if len(matched) != 1:
            raise RuntimeError(f"AGENTS.md section {prefix!r} matched {matched}")
        excerpt.append("\n".join(blocks[matched[0]]).strip())
    return "\n\n".join(excerpt)


bootstrap = (
    "Help me work on PyAutoFit in this experimental Colab notebook in teacher mode. "
    "Use only notebook-relevant guidance from the reference material below and "
    "the code I share. Skip CLI onboarding, filesystem checks, project-memory "
    "creation and maintainer workflows. Ask one question at "
    "a time; give hints before solutions. Do not claim to have read runtime files "
    "or run code unless you actually have. Preserve the numerics of any "
    "likelihood I supply. Before fitting real data, help me inspect it and discuss "
    "artefacts, outliers and selection effects. Explain proposed "
    "changes before I run them. If an API is uncertain, ask me to inspect it.\n"
)
context = bootstrap + "\nAssistant reference: " + ASSISTANT_REF + "\n"
context += "\n--- AGENTS.md (excerpt) ---\n" + agents_excerpt(agents_sections)
for relative in context_paths:
    context += "\n\n--- " + relative + " ---\n" + Path(relative).read_text()
print(context)
print("\n[context: %d characters]" % len(context))

"""
## 3. Your sandbox

This is now your assistant sandbox. Add your own cells and use Gemini in the
sidebar to do things in PyAutoFit — compose a model, wrap a likelihood, run a
search, read a result. Paste the cell or the error you are working on into your
message; the sidebar cannot reliably see the notebook.

__Bring your own likelihood.__ The context above includes the assistant's BYOL
mode — overview, model, wrap and validate, choose a search, your go-ahead, then
run and inspect. Paste your own likelihood function into the sidebar and have
Gemini set PyAutoFit up around it. Two rules it is told to keep: your numerics are
never re-parametrised or "fixed", and nothing is fitted before you say go. Paste
the code itself, since the sidebar reads no files — and before fitting real data,
plot it and say what artefacts, outliers or selection effects you know of.

The assistant's own worked example (data, model, likelihood, and the six steps
the guided tour walks) is in `scripts/start_here/` in the checkout. Run the cell
below to print any other assistant file when Gemini needs it, then paste the
output. For larger inference projects, continue in a local clone of
[autofit_assistant](https://github.com/PyAutoLabs/autofit_assistant).
"""


def show(relative):
    """Print any file from the assistant checkout, to copy into the Gemini sidebar."""
    print(Path(relative).read_text())


# e.g. show("skills/README.md")              — one line per skill, to pick the next one
#      show("skills/af_simulate_dataset.md") — any skill in full
#      show("wiki/core/index.md")            — the curated PyAutoFit reference
#      show("scripts/start_here/analysis.py") — the bundled Analysis class
show("skills/README.md")
