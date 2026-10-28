# Notice

Pinned sources: this repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`
(`sharpened-region-proof.md`, `short-period-runs-proof.md`) and the track
README of `2026-10-20-erwan-binding-lever`; through them, the OpenAI
manuscript *Quantitative Superexponential Bounds for van der Waerden
Numbers* pinned in `source-manifest.json` (commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`; Sections 2 and 6 for the meshes,
keys, flips and the multiplicity lemma used in Lemma D).

Credits: the construction and every lemma it imports are due to the source's
authors. The sharpened and short-period regions, and the PR7 tuple examined
here, are due to this repository's contributors (#2, #4, #6, #7). The question
answered is the open question of the `short-period-sensitivity` track
(`2026-10-20-erwan-binding-lever`). Open PRs #9 and #12 are compared, not
modified.

Review history: several parallel Claude sessions worked on this together.
radar-e2 made an adversarial pass, which restricted the union-bound statement
to sub-prescription covers (a counterexample showed the broader statement was
false) and tightened Lemma C. radar-1a counter-checked the verifier and the
PR #12 comparison. radar-dd found P2 independently, with Gram-matrix layers.

AI assistance: the analysis, proofs, verifier and text were prepared with
Claude Opus 5.5 (Anthropic), in several cooperating sessions. Not
independently reviewed by a human. Standard library only; no upstream file is
modified.
