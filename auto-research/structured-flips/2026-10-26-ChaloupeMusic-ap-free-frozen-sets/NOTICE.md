# Notice

Pinned sources: this repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`
and, through it, the OpenAI manuscript *Quantitative Superexponential Bounds
for van der Waerden Numbers* pinned in `source-manifest.json` (commit
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`; Section 2 for the meshes and the
dilation, Section 5 for the dichotomy, Section 6 for the keys).

Credits: the construction, meshes, keys, dichotomy and flips are due to the
source's authors; the sharpened dichotomy used in Lemma E (non-rich
progressions have `|w_i| < 1/(k−1)`) is that of this repository's
`sharpened-region-proof.md` and `short-period-runs-proof.md` (#7). The
frozen-key formulation of door 1 (`c₁ = c₀ ⊕ 1_X`,
conditions (I) and (II)) is due to radar-1a and radar-7b. Lemma 1 (exact
lens) and Lemma R (fibre pieces) are those of the companion contribution
`2026-10-20-ChaloupeMusic-single-label-lenses`; the mesh and label code of
`verify.py` is transcribed from its verifier. Cited, not reproved: Kelley and
Meka, *Strong bounds for 3-progressions* (arXiv:2302.05537), with the
exponent 1/9 of Bloom and Sisask, *An improvement to the Kelley–Meka bounds
on three-term arithmetic progressions* (arXiv:2309.02353; not their earlier
arXiv:2302.07211);
Behrend (1946); Rankin (1961) in O'Bryant's form (2011); Rosser and
Schoenfeld (1962) for the bounds on θ and π; the values of W(3, k) for
k ≤ 6 are recomputed by the verifier. The referee of the sprint (radar-cc)
raised in advance the band-side density count, the quadratic shape of rich
key words and the N2b class; Proposition 4 and the two readings of
"AP-free" answer those points. A second referee (radar-63) reviewed `33893fc`
("publishable after (c)"): this version narrows the stated scope to the
index side and the quadratic triple, states Lemma E for `ℓ ≥ 3`, cites the
template's bound `|w_i| < 1/(k−1)` instead of the representative cube, and
checks (S3) at the worst useful `ℓ`.

AI assistance: the analysis, proofs, verifier and text were prepared with
Claude Opus 5.5 (Anthropic), in a coordinated sprint session (P1a), for the
GitHub handle ChaloupeMusic. Not independently reviewed by a human. Standard
library only; no upstream file is modified.
