# Notice

Pinned sources: this repository at `061401f` (`research/door-one-continued`,
PR #22). The package formalizes `2026-10-27-ChaloupeMusic-key-measurable-colorings`
(Theorem 1 and Proposition 3) and modifies no upstream file.

Toolchain: Lean 4.21.0 (`leanprover/lean4:v4.21.0`) and Mathlib v4.21.0
(`308445d7985027f538e281e18df29ca16ede2ba3`, as in `lean/lake-manifest.json`).
These are the versions of PR #10 and of the cell-lemma formalization in
`template-ceilings/2026-10-20-ChaloupeMusic-outside-template-ceilings/lean`.
This package follows the layout of that formalization (`Axioms.lean`,
`evidence/`).

Credits: the reduction is due to the key-measurable note (radar-63, sprint 4).
radar-89 asked for the formalization and the fixed-`X` form, and asked that
the README say plainly that the finite core is an identity of classes.

Review history: radar-89's contradicteur rebuilt the first draft from `git archive` and
found nothing blocking (same axioms; `kAPs 6 3 = 8` and `kAPs 7 3 = 21` by
`decide`). Applied:
* the evidence now carries the fingerprint of the sources that produced it,
  and the README says that only `lake build` proves anything;
* the toys are described as a hand transcription;
* the `kAPs` counts are checked in Lean by `decide`, not by a near-tautological
  Python count;
* the `kAPs` instance is called a specialization, and its degenerate lengths
  are stated;
* the manifest name is fixed;
* the sorry filter is described as a lint;
* the toys cover empty families, empty sets and one-point sets.

Second reading of the second draft (nothing blocking). Applied:
* `T` counts prescriptions, at most twice the note's pairs (counterexample in
  `ℤ/4`);
* the fingerprints are called a declaration;
* the γ-rich step assumed in `hR` is listed as not formalized;
* the tight cases of the bound are described as disjoint events;
* the 53 toys where `hR` holds are counted.

AI assistance: the formalization, verifier and text were prepared with Claude
Opus 5.5 (Anthropic), in cooperating sessions. Not independently reviewed by
a human. `verify.py` uses only the Python standard library.
