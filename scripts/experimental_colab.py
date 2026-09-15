"""
# Experimental: PyAutoFit assistant in Colab

Install the assistant's PyAutoFit stack in a **fresh CPU runtime** and give Colab's
Gemini sidebar its context, then experiment in your own cells. Run the two cells
below in order; installation can take a few minutes.

This is a notebook experiment, not the full CLI assistant or an HPC service.
Cloning the repository does **not** make Gemini read its instructions. Step 2
provides context to copy into the sidebar explicitly. Gemini availability depends
on your Google account and Colab settings.

Save a copy of this notebook in Drive to keep your edits. Runtime files disappear
when Colab resets: download anything you want to keep before disconnecting.

__Contents__

1. Setup
2. Gemini context
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

Only the text you supply is guaranteed to be part of that conversation. If Gemini
needs another skill, open that file in Colab's Files panel and paste the relevant
section. Sidebar access to notebook content can vary: include the cell or error
in your message when needed.
"""

context_paths = [
    "AGENTS.md",
    "modes/teacher.md",
    "skills/af_compose_model.md",
    "skills/af_wrap_likelihood.md",
]
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
for relative in context_paths:
    context += "\n--- " + relative + " ---\n" + Path(relative).read_text()
print(context)

"""
## That is the whole notebook

This is now your assistant sandbox. Add your own cells below and use Gemini in
the sidebar to do things in PyAutoFit — compose a model, wrap a likelihood, run
a search, read a result. Paste the cell or error you are working on into your
message: the sidebar cannot reliably see the notebook.

The assistant's own worked example (data, model, likelihood) is in
`scripts/start_here/` in the checkout. For larger inference projects, continue in
a local clone of [autofit_assistant](https://github.com/PyAutoLabs/autofit_assistant).
"""
