# Proofs

Notation is that of `README.md`. Every probability is under the law `L` of `X`. `n^* = max_X Z(X)`; the
maximum is over all subsets of `𝒦`, so `Z <= n^*` under every law.

## Theorem 1

*Proof.* `S_j = Σ P(E_1 ∩ … ∩ E_j)` over `j`-subsets of `𝓔`. Each `E_i` is determined by
`X ∩ κ(P_{E_i})`, so their intersection is determined by `X` on `∪_i κ(P_{E_i})`, a set of at most `jk`
keys. Its probability is therefore a function of the marginal of `L` on that set. A certificate of order
`m` is a function of `(S_1, …, S_m)` (Bonferroni's inequalities, or the optimum of the moment linear
programme). It takes the same value for two laws with the same marginals on all sets of at most `mk`
keys. An `mk`-wise independent law with marginals `ρ` has the marginals of the iid law. ∎

## Theorem 2

For `1 <= w <= n^*`, `w(n^* + 1 − w) >= n^*`: the left side is concave in `w` and equals `n^*` at `w = 1`
and `w = n^*`. So, for every integer `w` in `{0, …, n^*}`,

```math
 \mathbf 1[w\ge1]\ \le\ w-\frac{w(w-1)}{n^*}=\frac{w(n^*+1-w)}{n^*}. \tag{1}
```

*If.* Take `W` in `{0, …, n^*}` with moments `S_1, S_2`. By (1),
`P(W >= 1) <= S_1 − 2S_2/n^* < 1`. If `S_1 < 1`, then `P(W >= 1) <= S_1 < 1`.

*Only if.* Suppose `S_1 >= 1` and `S_1 − 2S_2/n^* >= 1`. The points `(w, C(w,2))`, `1 <= w <= n^*`, are
in convex position, since `C(w,2)` is convex. Their hull is the region `1 <= x <= n^*`,
`g(x) <= y <= (x − 1)n^*/2`. Here `g` is the piecewise-linear interpolation of `C(w,2)` at the integers,
and the upper edge is the chord from `(1, 0)` to `(n^*, C(n^*, 2))`. The point `(S_1, S_2)` is in that
region:

* `S_1 <= n^*` because `Z <= n^*`;
* `S_2 >= g(S_1)` because `Z` lives on `{0, …, n^*}`, and the lower envelope of `C(w,2)` over
  `{0, …, n^*}` agrees with `g` on `[1, n^*]` (`C(0,2) = C(1,2) = 0`);
* `S_2 <= (S_1 − 1)n^*/2` is the hypothesis.

By Carathéodory's theorem, some `W` supported on `{1, …, n^*}` has moments `(S_1, S_2)`, and
`P(W = 0) = 0`. So no certificate from these two moments exists. ∎

## Theorem 3

The statement proved: for every `δ` in `(0, 1]`, `E[Z ; Z <= (1 − δ)n^*] <= (1 − π − c)/δ`, where
`c = P(Z > (1 − δ)n^*)`. For `δ > 1 − π`, the conditional mean below is less than `1`.

*Proof.* By (1) applied to `Z`, `1 − π = S_1 − 2S_2/n^* = E[Z(n^* + 1 − Z)]/n^*`. Fix `δ` and let
`A = {Z <= (1 − δ)n^*}` and `c = P(Z > (1 − δ)n^*)`.

* On `A ∩ {Z >= 1}`, `n^* + 1 − Z >= δn^* + 1`, so `Z(n^* + 1 − Z)/n^* >= δZ`.
* On `A^c`, `1 <= Z <= n^*`, so `Z(n^* + 1 − Z)/n^* >= 1` by (1).

Hence `1 − π >= δ E[Z; A] + c`. Since `P(A) = 1 − c` and `0 <= π <= 1`,

```math
 \mathbb E[Z\mid A]\le\frac{1-\pi-c}{\delta(1-c)}\le\frac{1-\pi}{\delta}<1\qquad\text{for }\delta>1-\pi .
```

`A` contains `{Z = 0}`, and `P(Z = 0) >= π > 0`, so the conditioning is well defined. ∎

*Reading.* With `S_1 >> 1`, Theorem 2 needs `2S_2 > n^*(S_1 − 1)`, and Theorem 3 says that the failure
mass outside catastrophes is `O(1)`. So two moments certify only a law whose failures cluster to the
extreme. This describes the certificates and closes nothing: the law conditioned on non-catastrophe is in
general outside any computable class, and conditioning on `{Z = 0}` would trivially give `E[Z] = 0`.
Whether some designed law clusters this way is open.

## Corollary 4

*Proof.* The first moment is `S_1`, a function of `k`-marginals (Theorem 1). For the rich part, a
failure at `(P, β)` needs `X ∩ κ(C_β(P)) = ∅` and `|C_{¬β}(P) \ X_P| < θk`. A rich `P` has
`|C_{¬β}(P)| >= γk`, so `X` covers at least `(γ − θ)k` positions of `C_{¬β}(P)`. A key covers at most two
positions (Lemma 3 of `source-only-1-16`), so `X` contains at least `j = ⌈(γ − θ)k/2⌉` keys of
`κ(C_{¬β}(P))`, a set of at most `k` keys. Under a `k`-wise independent law with marginal `ρ`, this has
probability at most `C(k, j)ρ^j <= 2^k ρ^j`. There are at most `2N^2` pairs `(P, β)`, and
`log N = ck log k (1 + o(1))`. So the expected number of rich failures is at most

```math
 \exp\Bigl(2ck\log k+k\log2-\tfrac{b_X(\gamma-\theta)}2k\log k+o(k\log k)\Bigr)\to0
 \quad\text{iff}\quad 4c<b_X(\gamma-\theta).
```

The (I′) failures depend on at most `k` keys each, so they too have their iid probabilities. Their union
over the `e^{o(k log k)}` case (i) and case (ii) words goes to `0` under the iid condition `b_X < a`
(the hitting cost C1, as in the exact-condition note). Theorem 2 of that note adds `2c < θb`. At fixed `b_X`
the supremum over `θ` and `b` is `b_Xγ/4`, approached with `θ → 0` and `θb → ∞`. With `b_X < a < 1/2` and
`γ < 1/2`, it is below `1/16`. This bounds `E Z` from above, so it is a sufficient condition, not a
ceiling. The proved ceiling is Proposition 5 of the exact-condition note: the first moment certifies
nothing once `2c > (1/2 − θ)b_X`, hence nothing beyond `a/4 < 1/8`. ∎

*Remark (radar-d9).* The bound counts every key as covering two positions, on every progression.
Progressions with a repeated key are rare: a repeated box has step density at most `k(4H)^D`, and
Lemma C\* counts the rest. On the dominant family, whose `k` keys are distinct, the exponent is
`b_X(γ − θ)k` and not half of it. A split in the style of Theorem 9 of `source-only-1-8` should then
give `2c < b_X(γ − θ)`, with supremum `γa/2 < 1/8`. That split is not written out here. Either way, a
`k`-wise independent `X` stays below `1/8`.

## Proposition 5

Let `𝒦 = ⊔ B` be a partition into blocks, and let `X` be the union of the blocks chosen, each
independently with probability `ρ`. Fix `(P, β)`.

1. *(No block meets both classes of `P`.)* Let `j_B` be the least number of blocks inside
   `κ(C_{¬β}(P))` whose positions cover at least `|C_{¬β}(P)| − θk` positions, and `n_B` the number of
   blocks meeting `κ(C_β(P))`. Then `P(F_{P,β}) >= ρ^{j_B}(1−ρ)^{n_B}`. Since each key lies in one block,
   `j_B <= j_K` and `n_B <= n_K`, the corresponding numbers of keys. So the first-moment lower bound of
   the exact-condition note (Proposition 5 there) can only grow under blocks.
2. *(A block meets both classes.)* A failure at `(P, β)` needs `X` to avoid every block meeting
   `κ(C_β(P))`, including the straddling ones. Their positions in `C_{¬β}(P)` then stay outside `X_P`. If
   the straddling blocks carry at least `θk` positions of `C_{¬β}(P)`, (II′_θ) holds at `(P, β)` for every
   draw. That is a property of the partition and `c₀`, not of the law.

*Proof.* (1) Choosing the `j_B` blocks and none of the `n_B` blocks is one outcome inside `F_{P,β}`. The
two sets of blocks are disjoint, because no block meets both classes. (2) is read off the definition. ∎

So blocks help (II′) only by straddling, and a straddling partition that serves every rich `P` is a
deterministic splitting structure. Producing one for `N^2` progressions is a combinatorial problem of the
kind that Proposition 4 of the exact-condition note isolates. This note does not decide whether one
exists.

## Proposition 6

Janson's inequality: for a product measure and increasing events `A_i`,
`P(∩ ¬A_i) <= exp(−μ + Δ/2)`. It is an upper bound on the probability that none occurs. It can certify
that a law fails, never that it succeeds. The failure event of (II′) at `(P, β)` is `U ∩ V`, with
`U = {X covers C_{¬β} \ θk}` increasing and `V = {X ∩ κ(C_β) = ∅}` decreasing. So it is not monotone,
and neither Janson nor Harris applies to it as stated. Harris's inequality for product measures gives
`P(I ∩ D) <= P(I)P(D)` for `I` increasing and `D` decreasing. The event "every hitting condition of (I′)
holds" is increasing, and the event "no covering event `U` occurs" is decreasing. They are therefore
**negatively** correlated. (II′) forbids only `U ∩ V`, which is weaker than forbidding `U`, so this is a
remark about the tension between (I′) and (II′), not a proved obstacle. ∎

## Proposition 7

Let `Q` be a prime, `ι: 𝒦 → F_Q` injective (`Q >= |𝒦|`), `0 <= r <= Q`, and
`h(x) = Σ_{i<d} a_i x^i` with `(a_i)` uniform on `F_Q^d`. Then `X = {κ : h(ι(κ)) < r}` (residues read as
`0, …, Q−1`) is `d`-wise independent, with marginal `r/Q`.

*Proof.* For distinct `x_1, …, x_d`, the map `a ↦ (h(x_1), …, h(x_d))` is the Vandermonde matrix, which
is invertible. So the values are uniform on `F_Q^d`, hence independent and uniform. ∎

The seed has `d log Q` bits. With `|𝒦| = N^{o(1)}`, `log Q = o(log N)`. Hash families of every order are
available with the keys at hand.
