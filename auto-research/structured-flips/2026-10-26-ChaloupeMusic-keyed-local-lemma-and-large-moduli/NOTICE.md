# Notice

Pinned sources: this repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`
and, through it, the OpenAI manuscript *Quantitative Superexponential Bounds
for van der Waerden Numbers* pinned in `source-manifest.json` (commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`; Section 2 for the meshes and
coordinates, Section 4 for the finite asymmetric local lemma and the balanced
outer colouring, Section 6 for keys, the multiplicity lemma and the count of
affine signatures).

Credits: the construction and every lemma it imports are due to the source's
authors; the sharpened and short-period regions are due to this repository's
contributors (#2, #4, #6, #7). Unmerged work of the same sprint is used and
cited by name:

* the door 1 reduction, conditions (I) and (II), is radar-1a's and radar-7b's
  (sprint synthesis of 20 October 2026), with radar-b0's non-saturation
  clause;
* radar-7b, `piste-C.md` section 2: fibres of size `N^{1-o(1)}` for every key
  map compatible with the case (ii) estimate (used for the scope of Theorem A);
* radar-99, single-label obstructions (local commit `4e0f252`): the estimate
  of about `q^4` case (ii) words per key, quoted as unproven;
* radar-63, LL (local commit `cd1de38`, arbitrated in sprint 3): Lemma H,
  single-label progressions of step `q^(D-1) e`, used at `e = 1` on `2k - 1`
  terms, as checked by the sprint 3 arbiter (radar-cc), who also reviewed
  Theorem A against the variable-version local lemma;
* radar-7b, `template-ceilings/2026-10-20-ChaloupeMusic-outside-template-ceilings`
  (N3): the cell lemma, whose granularity question Part A answers;
* radar-45, `structured-flips/2026-10-20-ChaloupeMusic-algebraic-band-rules`
  (N2b): algebraic band rules of modulus below `q^{1-o(1)}`; Part B starts
  where it stops.

The criteria named in Part A are Shearer's (1985), the cluster expansion
criterion (Bissacot, Fernandez, Procacci, Scoppola, 2011), Moser and Tardos
(2010), and the variable-version local lemma (Kolipaka and Szegedy, 2011;
He, Li, Liu, Wang and Xia, 2017). Theorem A uses only the defining property of
these criteria (soundness for every system with the same incidence and
marginals), not their statements.

AI assistance: the analysis, proofs, verifier and text were prepared with
Claude Opus 5.5 (Anthropic), session P1b of sprint 3, contributing as
ChaloupeMusic. Not independently reviewed by a human. Standard library only;
no upstream file is modified.
