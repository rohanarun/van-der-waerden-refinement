# Lean formalization of the least admissible profile

Lean 4.21.0 with Mathlib `v4.21.0` (the versions of PR #10) checks the profile side of this
package: Theorem 1 (both parts), Corollary 2 (including the constant `3/(2Γ(4/3))` and its
bracket for every `N`), the `t = 4/5` witnesses of Corollary 3, and the `Po` side of
Theorem 4 (K1 to K5). No `sorry`, no `native_decide`, no added axiom: `Axioms.lean` runs
`collectAxioms` on every declaration of the `Profile` namespace (101) and fails on anything
other than `propext`, `Classical.choice` and `Quot.sound`.

```sh
cd auto-research/matrix-profile/2026-10-20-ChaloupeMusic-least-admissible-profile/lean
lake exe cache get        # prebuilt Mathlib
lake build                # expected: Build completed successfully.
lake env lean Axioms.lean # expected: 101 declarations, axioms within propext, Classical.choice, Quot.sound
```

The profile is stated over an arbitrary linearly ordered field `K` (so over `ℚ` and `ℝ`),
with indices in `ℕ` and every statement assuming its indices are `≥ 1`.
`H n = ∏_{m ∈ [1,n)} (1 + 1/(3m))` and `Po a b = H u (v + (u-1)/2)`, `u = min a b`, `v = max a b`
(`Profile/Defs.lean`). Concavity is written with the centre at `c + 1`
(`P(a,c) + P(a,c+2) ≤ 2 P(a,c+1)`, `c ≥ 1`), which is (C) of the README.

## Statements

| README | Lean | File |
|---|---|---|
| Theorem 1 (i): (N) | `Po_one_left` | `Admissible.lean` |
| (S) | `Po_symm` | `Defs.lean` |
| (C), rows and columns | `Po_row_concave`, `Po_col_concave` | `Admissible.lean` |
| (T), with equality for `h ≥ a` | `Po_row_tripling`, `Po_col_tripling` | `Admissible.lean` |
| (E_{3/4}), cube form `Po^3 ≤ (a+b-1)^4` | `Po_envelope` | `Admissible.lean` |
| increasing in each coordinate | `Po_row_mono`, `Po_col_mono` | `Admissible.lean` |
| `Po ≤ P_*`, cube form; `H_u^3 ≤ (3u-1)/2` | `Po_cube_le_Pstar_cube`, `H_cube_le` | `Admissible.lean` |
| Theorem 1 (ii): hypotheses (no symmetry) | `LowerAdmissible` | `Least.lean` |
| Theorem 1 (ii): `P ≥ Po` | `LowerAdmissible.Po_le` | `Least.lean` |
| diagonal step (Lemma 5.1, exact constants) | `LowerAdmissible.diag` | `Least.lean` |
| `Po` satisfies the hypotheses | `Po_lowerAdmissible` | `Least.lean` |
| Corollary 2: `min P(a,a) = L_a` | `diag_min` | `Constant.lean` |
| `κ_a` strictly increasing (cube form) | `kappa_cube_strictMono` | `Constant.lean` |
| `κ_a < (3/2)^(4/3)` (cube form) | `kappa_cube_lt` | `Constant.lean` |
| `H_a^3/a` increases, `H_a^3/(a-1/3)` decreases | `lower_seq_mono`, `upper_seq_anti` | `Constant.lean` |
| `κ_a → 3/(2Γ(4/3))` | `kappaSeq_tendsto` | `Constant.lean` |
| `(27/8) H_N^3/N ≤ κ^3 ≤ (81/8) H_N^3/(3N-1)`, every `N ≥ 1` | `kappa_bracket` | `Constant.lean` |
| Corollary 3: (E_{4/5}) holds on the diagonal for `a < 63`, fails at `63` | `envelope_four_fifths_holds_below_63`, `envelope_four_fifths_fails_at_63` | `Witnesses.lean` |
| Theorem 4, `Po` side: K1 | `K1` | `Families.lean` |
| K2 (with `L_{sc} ≤ L_s L_c`) | `K2`, `L_mul_le` | `Families.lean` |
| K3 | `K3` | `Families.lean` |
| K4, K4' | `K4`, `K4'` | `Families.lean` |
| K5 | `K5` | `Families.lean` |
| Corollary 5, `Po` side | `corollary5` with the five above | `Families.lean` |

`κ_a = L_a / a^(4/3)` is `kappaSeq` (real `rpow`), and `κ = 3/(2Γ(4/3))` is `kappa`, with
Mathlib's `Real.Gamma`. The limit goes through Euler's formula `Real.GammaSeq_tendsto_Gamma`:
`∏_{j=0}^{n} (4/3 + j) = (n + 4/3) n! H_{n+1}` (`prod_four_thirds`) turns `GammaSeq (4/3) n` into
`n^(4/3) / ((n + 4/3) H_{n+1})`. The bracket then follows from the two monotone sequences and
their common limit; no inequality on the Gamma function is used. K1 is proved as in the README,
by applying Theorem 1 (ii) to `Q(c,d) = Po(a + K(c-1), b + K(d-1)) / Po(a,b)`.

## Outside this formalization

- The tensor side of Theorem 4 (that every symmetrized profile of a tensor character satisfies
  K1 to K5) and the paper's own (S), (N), (C), (T): they rest on the paper's tensor
  constructions, which are not formalized.
- The numerical bracket `[1.679751, 1.679770]` at `N = 10^4` and its comparison with an
  independent 48-digit value: `kappa_bracket` is proved for every `N`, but `H_{10^4}` is not
  evaluated in the kernel. `verify.py` does it in exact rationals.
- The `t = 7/9` witness at `a = 2494`: too deep for kernel reduction; in `verify.py`.
- The referee's example `P~_c`, the envelope gap at `(3,3)`, and the comparison with PR #11's
  family: in `verify.py`.
- Strict monotonicity and `κ_a < (3/2)^(4/3)` are stated in cube form (`κ_a^3 = L_a^3/a^4`,
  `kappaSeq_cube`), which is equivalent since both sides are positive.
