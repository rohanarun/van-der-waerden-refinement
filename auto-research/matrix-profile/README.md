# matrix-profile/

**Goal.** Understand what the scalar profile inequalities of OpenAI's 9/4 matrix-multiplication
paper can and cannot prove, and what an additional constraint would need to do to move the
exponent. The repository's `research-note.tex` shows that the listed inequalities admit
`t = 3/4` (the profile `P_*`); PR #11 (open, filed under `experiments/`) studies a
two-parameter family around `P_*`.

**Open questions.**

- A valid tensor inequality, provable for every character, that the least admissible profile
  `P_o` violates, and that forces some value `P(a,b)` above `(a+b-1)^(4/3)` (necessarily with
  `min(a,b) >= 3` once Clebsch-Gordan of order 2 is used). That excludes `t = 3/4` and an
  interval below it; a diagonal exponent above `4/3` would suffice but is not necessary.
- Laser-method degenerations of `C(a,b)` into fully independent blocks, whose symmetrized form
  carries a factor `M^(1/t)`: do any of them exclude `t = 3/4`?

| date | contributor | contribution | status |
|---|---|---|---|
| 2026-10-20 | ChaloupeMusic (with Claude) | [Least admissible profile `P_o`, sharp constant `3/(2 Gamma(4/3))`, five further valid families that `P_o` satisfies](2026-10-20-ChaloupeMusic-least-admissible-profile/README.md) | proofs and exact checks; human review pending |
