# Digit transversals saturate slow blocks

**Status:** structural research, negative, with proofs. Sprint 4 asked
(piste S7) whether the digit transversal of `key-measurable-colorings`, the
only deterministic slow-word transversal of density `k^{−a}`, satisfies (II′)
on rich progressions. It does not reach that question. It fails (I′) itself,
because it **contains** whole slow blocks, which then end monochromatic for
every flip. The failure holds for every base, shift and set of digit
positions. A second theorem closes, more broadly, every rule that reads a
linear form of the base-`q` digits modulo `M`, unless `M ≥ N^{1−o(1)}`. No
new bound is claimed, and no `c > 1/8`.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, through
`pr/door-one` (`00375ff`) and `key-measurable-colorings` (this PR).

**Sources:** `2026-10-27-ChaloupeMusic-key-measurable-colorings` (Theorem 1,
Proposition 3, the digit sets of its (D)); `2026-10-26-ChaloupeMusic-ap-free-frozen-sets`
((S4) and (H)); `2026-10-26-ChaloupeMusic-exact-door-one-condition`
(Proposition 1, (I′), (II′)); Lemma F of `2026-10-27-ChaloupeMusic-more-keys`.
See `NOTICE.md`.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-digit-transversals-saturate/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and a JSON
summary equal to `RESULT.json`. Standard library only, under a second.

## What a slow block asks of X

A **fibre piece** `J` is an interval of indices `m` on which
`r + q^{D−1}m` keeps one full label ((S4) of `ap-free-frozen-sets`). Every
`k`-AP of `J` is a case (ii) block, and `c₀` is constant on it. Write
`S_J = {m ∈ J : κ(r + q^{D−1}m) ∈ X}`. By Proposition 1 of
`exact-door-one-condition`, with `c₀ ≡ α` on a block `B`:

* if `S_J ∩ B = ∅`, the target `α` is reached when no key of `B` flips:
  this is the hitting half of (I′), condition (H);
* if `B ⊆ S_J`, every position of `B` is frozen at `¬α`, and `B` is
  monochromatic **for every flip assignment**. This is the non-saturation
  half. Proposition 3 of `key-measurable-colorings` asks for it too, since a
  slow word must be properly 2-colored.

So `S_J` must **properly 2-color** the `k`-APs of `J`: it must meet every one
of them and contain none.

**Lemma K (what keys can do on a piece).** On a fibre piece the `V`-box is
constant, so a set of keys acts there only through the band
`⌊C(r) + (s₀ + λm)²⌋`. The band is at most 2-to-1 on the piece (Lemma F of
`more-keys`), so every trace on one piece is key-measurable up to the `±s`
pairs. Whether one set of bands serves every piece at once is a separate,
global question (see R's sorting of S6-63). Theorem 1 below makes it moot for
digit rules, because they already fail on a single piece, even with keys fine
enough to realise any index set.

## Theorem 1 (every digit rule saturates or misses a block)

Fix a base `p ≥ 2`, a shift `t ≥ 0` and a non-empty finite set `U` of digit
positions, with `u₀ = min U`. Put

```
S = {x : some base-p digit of x + t at a position of U is 0}.
```

Let `J` be an interval with `|J| ≥ 8k³`. Then `J` contains a `k`-AP that lies
entirely in `S` or entirely outside it.

*Proof.* Membership in `S` reads only the digits at positions `≥ u₀`.

* **Case A: `k p^{u₀+1} ≤ |J|`.** The starts `x` with
  `x + (k−1)p^{u₀+1} ∈ J` fill an interval of length at least `p^{u₀+1}`. So
  one of them has digit `u₀` of `x + t` equal to `0`. Adding a multiple of
  `p^{u₀+1}` changes no digit at a position `≤ u₀`. So
  `x, x + p^{u₀+1}, …` all lie in `S`: **saturated**.
* **Case B(i): `k p^{u₀+1} > |J|` and `p^{u₀} ≥ k`.** Take `x` with
  `x, …, x+k−1 ∈ J` and `(x+t) mod p^{u₀} ≤ p^{u₀} − k`. Among any `k`
  consecutive starts one qualifies, and `J` has at least `k` starts. Then
  `x + t + i` has no carry into position `u₀` for `i < k`. So every digit at
  a position `≥ u₀` is constant, and the block is saturated or untouched.
* **Case B(ii): `k p^{u₀+1} > |J|` and `p^{u₀} < k`.** Here
  `p ≥ p^{u₀+1}/p^{u₀} > (8k³/k)/k = 8k`. The points where digit `u₀` of
  `x + t` vanishes form runs of `p^{u₀} < k` integers, one every
  `p^{u₀+1}`. At most `|J|/p^{u₀+1} + 1 < k + 1` of these runs meet `J`, so
  they give fewer than `k(k+1)` points. A zero at a position `u > u₀` of `U`
  makes a run of `p^u ≥ p^{u₀+1} > 8k²` consecutive integers. If such a run
  meets `J` in `k` consecutive points, those points are a saturated block.
  Otherwise each such run sticks out of `J` and meets it in fewer than `k`
  points at one end, which gives at most `2(k−1)` points in all. So
  `|S ∩ J| < k² + 3k ≤ ⌊|J|/k⌋`, and one of the `⌊|J|/k⌋` disjoint windows of
  `k` consecutive integers is **untouched**. ∎

(Check 1: 400 random rules with `p` up to 199, all three cases exercised. The
proof's witness is found each time, and a full search over every `k`-AP
confirms on a subsample. Control: step `p^{u₀}` does not saturate.)

**Corollary 1 (the S6-63 candidate).** The transversal of
`key-measurable-colorings` is `U = {0, …, L−1}` with `p ≤ k`, so it is case
A with `u₀ = 0`. Every block of step `p` whose start has `x + t ≡ 0 (mod p)`
lies in `S`. On a fibre piece (`|J| ≥ 2Y₀ ≫ kp`), that is a fraction `1/p`
of the starts of every step `δ ≡ 0 (mod p)`, and higher zero digits add more
(check 2). Through two layers (`more-keys`), these blocks are entirely
frozen, and `c₁` makes them monochromatic whatever the flips. **The candidate
fails (I′) before (II′) is reached.** It meets every `k`-AP, as S6-63 and R
proved, but it also contains some. A shift, a change of base or a choice of
digit positions does not repair it (Theorem 1).

Consequences for `key-measurable-colorings` § (D). The lower bounds are
untouched, since they hold for every trace. The statement "deterministic
transversals reach `k^{−a+o(1)}`" is not established by digits, because they
give hitting sets and not proper colorings. A witness at that density does
exist on the single-label blocks: a random `Y` on the source keys, of density
`(2+δ)H′/k = k^{−a+o(1)}`, with `H′ = 6 ln q + O(D ln³ k)` the log of the
number of slow key words. It meets every such block by the union bound over
the `e^{H′}` key words (C1), and it saturates none, since
`e^{H′}ρ^{k/2} → 0` (radar-63's remark; Theorem C of `more-keys` with
`κ = 1 − a` says the same). This establishes (I′) on the single-label blocks
only. A proper coloring of **all** slow words also needs the argument on the
color word given in `key-measurable-colorings` (this PR) and in radar-d9's
(D) note (`slow-word-transversal-density`, Proposition 7 (2)), which this note does not reprove.
With that argument, `k^{−a}` is the right order for (D), with a random
witness and no deterministic one.

## Theorem 2 (rules linear in the digits need a modulus of size N)

Write `n = Σ_t n_t q^t`, with `0 ≤ n_t < q` and `t < D`. Consider any rule

```
X = {n : F(ψ₁(n) mod M₁, …, ψ_s(n) mod M_s) = 1},   ψ_ℓ(n) = Σ_t a_{ℓ,t} n_t,  a_{ℓ,t} ∈ ℤ,
```

with any `F`. This covers digit rules on `m = n_{D−1}` and on each `n_t`, on
digit sums, and on `n` itself (`a_{ℓ,t} = q^t`). Put
`E = ⌊q/(k⁶λ²)⌋`. If `Π M_ℓ < (E+1)^D`, then there are a non-zero step `d`
and a set `G` of starts of density `1 − o(1)` such that `X` is constant on
every block `n₀ + jd` (`j < k`, `n₀ ∈ G`) and each such block has one full
label. Hence, unless the density of `X` is `o(1)` or `1 − o(1)`, some slow
block is saturated (monochromatic for every flip) and some is untouched.

*Proof.* Pigeonhole the `(E+1)^D` vectors `e ∈ [0, E]^D` by
`(Σ_t a_{ℓ,t} e_t mod M_ℓ)_ℓ`. Two of them collide, so their difference
`e ≠ 0`, with `|e_t| ≤ E`, has `Σ_t a_{ℓ,t} e_t ≡ 0 (mod M_ℓ)` for every
`ℓ`. Put `d = Σ_t e_t q^t`, which is non-zero mod `N` since `|e_t| < q/2`.
For a start whose digits lie in `[kE, q − kE)`, the digits of `n₀ + jd` are
`n₀,t + j e_t` with no carry. Every `ψ_ℓ` then moves by
`j Σ_t a_{ℓ,t} e_t ≡ 0`, so `X` is constant.

Along the block, `x_i` moves by at most `2kE/q` and `y_i = λx_i` by at most
`2kλE/q`. A start is in `G` if it lies at least that far from every `U`
boundary (spacing `H/λ = 1/(k²λ)`) and every `V` boundary (`O(k³ log k)` of
them per coordinate, as in the mesh proof of `research-note.tex`), in all `D`
coordinates. The excluded fraction is
`O(D(k³λE/q + k⁴ log k · λE/q + kE/q)) = O(D log k/(k²λ)) = o(1)`.
A block with one full label has constant `c₀` and is case (ii). ∎

Since `ln λ = O(h₀ log k)` with `h₀ = D⌈log k⌉²`, we get
`D ln(E+1) = ln N − O(k^{2a} log³ k) = (1 − o(1)) ln N` for `a < 1/2`. So **a
rule linear in the digits must read them modulo `N^{1−o(1)}`.** This is the
scale of the whole group, not of one fibre (`q`). Rules of modulus at most
`q^{O(1)}` fall, for any `F` and any forms. That includes coordinate-wise
residue rules and digit sums: along `d = q − 1` the base-`q` digit sum is
constant. (Check 3: kernel found and block constant on 60 random forms by
direct arithmetic in `ℤ/q^D`. Control: `ψ = n` modulo `q^D` has no kernel in
the box.)

## Lemma W (where (II′) can fail at all)

For any `X` and any rich `P` with minority class of `γ_P k` positions,
(II′_θ) can fail at `P` only if

```
(γ_P − θ) k < |X_P| ≤ (1 − γ_P) k.
```

*Proof.* A failure needs `X_P ⊆ C_{¬β}` and `|C_{¬β} ∖ X_P| < θk`, so
`|X_P| > |C_{¬β}| − θk ≥ (γ_P − θ)k` and `|X_P| ≤ |C_{¬β}| ≤ (1 − γ_P)k`. ∎

For a future candidate of density `ρ < γ − θ`, (II′) is therefore a question
about the rich progressions on which `X` is unusually dense, about half of
`P`, and aligned with a color class. This is radar-2a's "dense row" in Q-S1b.
The digit candidate never reaches this test. (Check 4, exhaustive on toys.)

## Answer to S7

* **No.** The digit transversal does not get to (II′). It saturates slow
  blocks (Theorem 1, Corollary 1), so `c₁` has monochromatic slow progressions
  for every flip. No choice of base, position or shift avoids it.
* The obstruction is not specific to digits. Every rule that reads linear
  forms of the base-`q` digits modulo `M` is constant along a slow step,
  unless `M ≥ N^{1−o(1)}` (Theorem 2).
* What Door 1 needs on the slow side, stated exactly: a set that **properly
  2-colors** the `k`-APs of every fibre piece, with every other slow word and
  key-measurability on top, at density `k^{−a+o(1)}`. Only a random set is
  known to do it (Corollary 1). The rich side then has to be handled by a set
  that is not random, which is the open problem of Door 1, now without the
  digit candidate.

## What `verify.py` checks

1. **Theorem 1** on 400 random digit rules (`k = 3, 4`, `|J| = 8k³`, `p` up
   to 199, random `t` and `U`): the witness of the proof in each of the three
   cases, plus a full search on 25 of them. Control: step `p^{u₀}`.
2. **Corollary 1**: among the `k`-APs of `J` with `p | δ`, the saturated ones
   include every start with `x + t ≡ 0 (mod p)` (`p = 3, 5, 7`, exhaustive).
3. **Theorem 2**: pigeonhole kernel and constant block, in `ℤ/q^D`
   (`q ∈ {101, 103, 107}`, `D = 3`). Control: no kernel for `ψ = n` modulo
   `q^D`.
4. **Lemma W**, exhaustive on 3,000 toy progressions.
5. **The random witness**: at `k = 2^{739}` (`a = 0.3, 0.49`) and
   `k = 2^{1024}` (`a = 0.45`), with `c = 1/9`, a random set of density
   `3k^{−a} ln k` has both union bounds on a fibre piece tending to `0`.
   Hitting gives `2 ln Y₀ − ρk < 0`, and avoiding containment gives
   `2 ln Y₀ + k ln ρ < 0`.
6. **Provenance**: MANIFEST hashes; summary equal to `RESULT.json`.

## What is not claimed

* No closure of Door 1, and no bound on `c`.
* Theorem 1 is about digit rules on an interval of indices. For bands under
  the source keys, the rule becomes `S_J = {m : band(m) ∈ B}` with a
  quadratic band. A digit rule on the band saturates in the same way when the
  linear part `2sλδ` of the band step is close to `0 mod p^{u₀+1}`. This is
  a lens argument in the style of N2b, sketched and not proved here.
* Theorem 2's set `G` uses the mesh count `|V| = O(k³ log k)` of the source,
  as stated in `research-note.tex`.
* Lemma W is elementary. It only says where a failure of (II′) can lie.
