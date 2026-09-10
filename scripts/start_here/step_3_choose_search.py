"""
Start Here Step 3: Choose a Search
==================================

The third step of the "start here" tour. A model and a likelihood define a surface over
parameter space; the non-linear search is the algorithm that explores it. The choice is
statistical before it is computational — do you need the Bayesian evidence, only the posterior,
or just a best-fitting point? — and PyAutoFit gives every search the same interface, so it can
be swapped without touching the model or the likelihood
(`PyAutoFit:autofit/non_linear/search/`, and `skills/af_configure_search.md`).

This script lists the searches installed in the current stack and configures the one the tour
uses: Dynesty static nested sampling with 100 live points. Nested sampling is chosen because it
returns the Bayesian evidence as well as the posterior, and step 6 compares evidences.

__Contents__

- **Imports:** autofit.
- **Available Searches:** What the installed stack actually offers.
- **Search:** Configure Dynesty for the tour's fit.
"""

import autofit as af

"""
__Available Searches__

The roster is read from the installed library rather than from memory — a stale list of sampler
names is the classic way a generated script fails on someone else's machine.

The four families PyAutoFit exposes:

- **Nested sampling** — `Nautilus`, `DynestyStatic`, `DynestyDynamic`: posterior *and* Bayesian
  evidence, the currency of model comparison.
- **MCMC** — `Emcee`, `Zeus`: posterior only, often more efficient once the model is settled.
- **Optimisation (MLE)** — `LBFGS`, `Drawer`: a best-fitting point, no distribution.
- **Gradient-based (JAX)** — `BlackJAXNUTS` for Hamiltonian/NUTS sampling and the `MultiStart*`
  optimisers. These differentiate the likelihood automatically, so they require it to be written
  in JAX. The tour's likelihood is plain NumPy, which is why it uses Dynesty.
"""

families = {
    "Nested sampling": ["Nautilus", "DynestyStatic", "DynestyDynamic"],
    "MCMC": ["Emcee", "Zeus"],
    "Optimisation (MLE)": ["LBFGS", "Drawer"],
    "Gradient-based (JAX)": [
        name for name in dir(af) if name == "BlackJAXNUTS" or name.startswith("MultiStart")
    ],
}

for family, names in families.items():
    installed = [name for name in names if hasattr(af, name)]
    print(f"{family}: {', '.join(installed)}")

"""
__Search__

`nlive` is the number of live points Dynesty maintains: more live points explore the space more
thoroughly and give a more accurate evidence, at proportionally more likelihood evaluations. 100
is generous for a three-parameter model and still runs in seconds here; a fit with a slow
likelihood is where the trade-off starts to bite.

`path_prefix` and `name` decide where output is written — `output/start_here/gaussian_x1/` —
and they are what makes a completed search *reload* rather than re-run when the script is
executed again. That is deliberate and worth knowing before it surprises you
(`skills/af_configure_search.md` "Output discipline").
"""

search = af.DynestyStatic(
    path_prefix="start_here",
    name="gaussian_x1",
    nlive=100,
    number_of_cores=1,
)

print(f"\nConfigured: {type(search).__name__} with nlive=100")
print(f"Output will be written to: output/start_here/gaussian_x1/")
