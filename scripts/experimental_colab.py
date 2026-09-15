"""
# Experimental: PyAutoFit assistant in Colab

Try a small inference problem alongside Colab's Gemini sidebar. Use a **fresh CPU
runtime**, then run the cells in order. Installation can take a few minutes.

This is a notebook experiment, not the full CLI assistant or an HPC service.
Cloning the repository does **not** make Gemini read its instructions. Step 2
provides context to copy into the sidebar explicitly. Gemini availability depends
on your Google account and Colab settings; the fit also works without Gemini.

Save a copy of this notebook in Drive to keep your edits. Runtime files disappear
when Colab resets: download your results at the end.

__Contents__

1. Setup
2. Gemini context
3. Data inspection
4. Model and likelihood
5. Fit
6. Download and continue
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
to acknowledge the supplied context before discussing the next cell. The context
comes from this pinned assistant checkout; no API key or Gemini SDK is needed.

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
    "Help me work through this experimental PyAutoFit notebook in teacher mode. "
    "Use only notebook-relevant guidance from the reference material below and "
    "the code I share. Skip CLI onboarding, filesystem checks, project-memory "
    "creation and maintainer workflows. Ask one question at "
    "a time; give hints before solutions. Do not claim to have read runtime files "
    "or run code unless you actually have. Preserve the supplied likelihood's "
    "numerics. Before adapting this example to real data, help me inspect the "
    "data and discuss artefacts, outliers and selection effects. Explain proposed "
    "changes before I run them. If an API is uncertain, ask me to inspect it.\n"
)
context = bootstrap + "\nAssistant reference: " + ASSISTANT_REF + "\n"
for relative in context_paths:
    context += "\n--- " + relative + " ---\n" + Path(relative).read_text()
print(context)

"""
## 3. Inspect the bundled simulated data

The assistant's Gaussian is **peak-normalised**: normalization is its height,
not its integrated area. The simulation used centre 50, height 25 and width 10.
Its likelihood assumes independent Gaussian measurement errors and omits the
constant noise-normalisation term. Evidence values therefore use that convention.

Ask Gemini: *What features of this plot should constrain the three parameters?*
The model and likelihood below are imported unchanged from the assistant's tour.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, str(repo / "scripts" / "start_here"))
from gaussian import Gaussian
from analysis import Analysis

data = np.asarray(json.loads(Path("dataset/gaussian_x1/data.json").read_text()))
noise_map = np.asarray(json.loads(Path("dataset/gaussian_x1/noise_map.json").read_text()))
x = np.arange(data.size)
plt.errorbar(x, data, yerr=noise_map, fmt=".k")
plt.xlabel("x")
plt.ylabel("Profile amplitude")
plt.show()

"""
## 4. Compose the model and check the likelihood

Ask Gemini: *Explain these priors. What would happen if I fixed the width?*
The check below compares the imported likelihood with its written equation.
"""

model = af.Model(
    Gaussian,
    centre=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
    normalization=af.UniformPrior(lower_limit=0.0, upper_limit=100.0),
    sigma=af.UniformPrior(lower_limit=0.1, upper_limit=30.0),
)
analysis = Analysis(data=data, noise_map=noise_map)
truth = Gaussian(centre=50.0, normalization=25.0, sigma=10.0)
expected = -0.5 * np.sum(((data - truth.model_data_from(x)) / noise_map) ** 2)
assert np.isclose(analysis.log_likelihood_function(truth), expected)
print(model.info)
print("Log likelihood at simulation inputs:", expected)

"""
## 5. Run a small fit

Run this cell when ready. It performs actual nested sampling with 50 live points,
chosen for experimentation, not precision results. Runtime varies. The same
completed run reloads if you execute this cell again. Change `name` for a new
experiment, especially after changing the data or likelihood.

Ask Gemini: *Before I run this, what do you expect the recovered parameters to be?*
"""

search = af.DynestyStatic(
    path_prefix="experimental_colab", name="gaussian_x1", nlive=50,
    number_of_cores=1,
)
result = search.fit(model=model, analysis=analysis)
print(result.info)
best = result.max_log_likelihood_instance
plt.errorbar(x, data, yerr=noise_map, fmt=".k", label="data")
plt.plot(x, best.model_data_from(x), label="maximum likelihood fit")
plt.xlabel("x")
plt.ylabel("Profile amplitude")
plt.legend()
plt.show()

"""
## 6. Keep the results and continue

Ask Gemini: *Help me explain the parameter uncertainties and one limitation of
this fit. Then suggest one change I can predict and test.* Share `result.info`
with your question. The fit and residual figures are also under
`output/experimental_colab/` in the Files panel.

Run this last cell to download the fit outputs plus the model, likelihood, data,
configuration and context used here. Save your notebook copy separately: the
archive does not contain your edited notebook or Gemini conversation. Download
before disconnecting. For larger inference projects, continue in a local clone
of [autofit_assistant](https://github.com/PyAutoLabs/autofit_assistant), carrying
your scientific question, priors, likelihood and results with you.
"""

import zipfile
from google.colab import files

archive = repo.parent / "autofit_colab_results.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
    for directory in ["output/experimental_colab", "scripts/start_here",
                      "dataset/gaussian_x1", "config"]:
        for path in Path(directory).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                bundle.write(path, str(path))
    bundle.writestr("gemini_context.txt", context)
    bundle.writestr("environment.txt", subprocess.check_output(
        [sys.executable, "-m", "pip", "freeze"], text=True))
    bundle.writestr("assistant_ref.txt", ASSISTANT_REF + "\n" +
        subprocess.check_output(["git", "rev-parse", "HEAD"], text=True))
files.download(str(archive))
