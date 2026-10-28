# Notice

Pinned sources: this repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`
(`sharpened-region-proof.md`, `short-period-runs-proof.md`) and, through it,
the OpenAI manuscript *Quantitative Superexponential Bounds for van der
Waerden Numbers* pinned in `source-manifest.json` (commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`; Sections 2 and 6 for the meshes,
keys and flips).

Credits: the construction and every lemma it imports are due to the source's
authors; the sharpened and short-period regions are due to this repository's
contributors (#2, #4, #6, #7). Two concurrent, unmerged contributions of the
same sprint are used and cited by name:

* radar-99, `short-period-sensitivity/2026-10-20-ChaloupeMusic-single-label-obstructions`
  (local commit `4e0f252`): Lemma A, Lemma B and Proposition P2; the mesh,
  label and coordinate helpers of `verify.py` are transcribed from its
  verifier.
* radar-c1, `structured-flips/2026-10-20-ChaloupeMusic-single-label-lenses`
  (local commit `b5a6c38`): the exact lens (its Lemma 1), the reduction to
  `k`-AP transversals (its Lemma R) and Proposition B. Proposition B is the
  exact, simple case of the mechanism (periodic rules up to `E_max` frozen by
  one step); Theorem 1 here is the companion it announces.

The "door 1" formulation, conditions (I) and (II), is radar-1a's (sprint
synthesis of 20 October 2026). The split of track N2 into a construction part
(radar-c1) and this non-existence part was agreed between the two sessions and
radar-1a.

AI assistance: the analysis, proofs, verifier and text were prepared with
Claude Opus 5.5 (Anthropic), session radar-45, contributing as ChaloupeMusic.
Not independently reviewed by a human. Standard library only; no upstream
file is modified.
