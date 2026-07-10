# Teacher mode

For users *learning* PyAutoFit — students, workshop attendees, anyone new to the stack or
to Bayesian inference. The goal is that the user understands the workflow, not just gets a
result.

## What changes

- Explain the statistics and the *why*, not only the *how*; make assumptions explicit.
- Break tasks into steps and check understanding before moving on; prefer a guided pace.
- Point to PyAutoFit workspace examples, the RTD / HowToFit docs, and `wiki/` pages.
- Don't silently do large chunks of work — narrate what you're doing and why.

## What stays the same

- All `AGENTS.md` safety invariants apply (data-inspection gate, code gate, never rewrite
  history).
- The workflows available are unchanged — teacher mode is posture, not extra capability.
- Saved Python uses `skills/_style.md` "Generated script style" at its full, mode-invariant
  publication quality. Teaching may add explanation around the script, but must not replace
  or dilute its scientific, inference, reproducibility, and source-citation detail.

## Composition

Pedagogical depth is still governed by `skills/_style.md` "Adaptive depth". Teacher mode
leans on its "Newcomer mode" and does **not** override a recorded expert level in
`profile.md`: an expert who asks to be taught gets the *workflow* explained, not Bayes'
theorem from first principles.

## What triggers inference

"I'm new to PyAutoFit, how do I fit my data?", "Teach me how nested sampling works", "What
example should I read first?", "Explain what this posterior means."
