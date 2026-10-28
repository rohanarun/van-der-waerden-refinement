# Track: short-period-sensitivity

Goal: identify which inequality of the short-period region
(`short-period-runs-proof.md`, supremum c < 1/8) must change for any further
gain, so that new work targets the right step.

Open question: can the case (ii) key-word entropy of non-rich progressions
(the bands, `6 log q`) be made `exp(k^{1-θa+o(1)})` with θ > 1, or avoided?

Related: `barrier-note.md` (rigidity of `6 log q` in the earlier template).

## Index

| Date | Handle | Result | Status | PR |
|---|---|---|---|---|
| 2026-10-20 | erwan | `b < a` is the only single lever; relaxing `2a<m` or `a+b<1` alone gains nothing | research note (exact LP sensitivity) | – |
| 2026-10-20 | ChaloupeMusic | single-label progressions make `b < a` and `a + b < 1` necessary for every sub-prescription union bound with iid flips (`λ ≤ q/(400k³)`); periodic band flips fail deterministically; PR7 tuple's threshold exceeds `10^{402}` | negative result (proofs + exact checks) | – |
| 2026-10-20 | ChaloupeMusic | past `a = 1/2` (λ > q/k²) the x-label is injective, so the first local-lemma family must balance every k-AP of Z/N: circular; F cannot be relaxed by better counting | research note (negative, template-scoped) | – |
| 2026-10-26 | ChaloupeMusic | a key lies in `≈ q/(64k³λ)` single-label progressions, so `b < a` holds for every graph-only or variable-only local lemma on the canonical events; re-chosen families are complete or contain door 1; `R` is implied by F and B, so dropping it gains nothing | negative result (proofs + exact checks) | – |
| 2026-10-20 | ChaloupeMusic | Rich side: every cover bound with these keys needs `c ≤ b/4`, conditional on a rank statement (G♭), weaker than (G_θ), whose small-set half is proved (dense-set half open); linear band rigidity refuted by an exact Dirichlet certificate | research note (conditional barrier) | – |
