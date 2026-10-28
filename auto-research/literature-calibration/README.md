# Literature calibration

Goal: place this repository's coefficient against the published lower bounds
on `W_r(k)`, in one normalization (`W_r(k) > k^{c k ⌊log₂ r⌋}`), and say what
an improvement past a given `c` would settle elsewhere. A contribution here
proves no new bound on `W_r(k)`: it converts, compares and locates.

Open questions:

- Whether a variant of Fox–Hunter's Lemma 4.3 (arXiv 2606.02541) can act on a
  two-color input, such as the source's cyclic coloring. Their Theorem 5 needs
  `4ms ≤ r`, so it does not act at `r = 2` or `3`, where the uniform
  coefficient is pinned.
- Any obstruction between `1/8` and `ln 2` that bounds the problem rather
  than the current template.

Related tracks, in open PRs: `short-period-sensitivity` (#14),
`structured-flips` and `template-ceilings` (#16), `trust-reduction` (#19).

## Index

| Date | Handle | Result | Status | PR |
|---|---|---|---|---|
| 2026-10-26 | ChaloupeMusic | the uniform coefficient is a two-color exponent (`max(c_cyc, c₂/3) ≤ c_unif ≤ c₂`); `c_unif > ln 2` would build, for every `r = 2^m`, the density-`1/r` progression-free set that Fox–Hunter name as their bottleneck; Fox–Hunter already pass any fixed `c < ln 2` once `r ≥ (ln k)^{2/(1−c/ln 2)+η}` | research note (elementary propositions and literature map) | — |
