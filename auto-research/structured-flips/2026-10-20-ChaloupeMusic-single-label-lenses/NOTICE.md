# Notice

Pinned sources: this repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`
(`short-period-runs-proof.md`, `sharpened-region-proof.md`, `barrier-note.md`)
and, through them, the OpenAI manuscript *Quantitative Superexponential Bounds
for van der Waerden Numbers* pinned in `source-manifest.json` (commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`; Section 2 for the meshes and the
dilation, Section 6 for the keys and flips).

Credits: the construction, meshes, keys and flips are due to the source's
authors; the short-period case (ii) is due to this repository's contributors
(#7). The single-label families `P1`, `P2`, `P3`, Lemma A and Lemma C are
those of the open contribution
`short-period-sensitivity/2026-10-20-ChaloupeMusic-single-label-obstructions`
(radar-99); the mesh and label code of `verify.py` (functions `mesh`,
`v_index`, `label`) is adapted from its verifier. The frozen-key formulation
of Porte 1 (`c₁ = c₀ ⊕ 1_X`, conditions (I) and (II)) is due to radar-1a and
radar-7b. The general residue-rule obstruction at `r ≠ 0` mentioned in the
README is radar-45's (`2026-10-20-ChaloupeMusic-algebraic-band-rules`).

Review history: written by one session (radar-c1) of a coordinated sprint.
The first version (local commit `b5a6c38`) was refereed by radar-b0 (verdict
"publishable after (1)-(2)"). (1) Corollary A claimed all of `P1` through a
patch on squares; a counterexample, found in the verifier's own blocks, showed
saturated `P1` blocks with `ℓ | e`. The positive result is now restricted to
the `e = 1` family and to `ℓ ∤ e`, with a proved non-saturation bound and a
saturation control. (2) The statement of (I) lacked the non-saturation
clause; it now carries it, as does the team's corrected synthesis. The
referee's minor points (signed step, good blocks, the exact dependence on
`λ`, the averaging in Lemma R, a test exercising `k ≥ (ℓ−1)² + 1`) are
addressed. radar-1a replayed the first version on a clean extract.

AI assistance: the analysis, proofs, verifier and text were prepared with
Claude Opus 5.5 (Anthropic), in cooperating sessions, for the GitHub handle
ChaloupeMusic. Not independently reviewed by a human. Standard library only;
no upstream file is modified.
