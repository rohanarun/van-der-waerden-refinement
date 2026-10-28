# Line progressions never witness: a type count for (S), and moment certificates of every order

**Status:** structural research, with proofs and exact checks. It adds two things to the notes
`2026-10-27-ChaloupeMusic-supersaturation-is-global` and `2026-10-27-ChaloupeMusic-moment-certificates`.
(A) A uniform key set `Y` makes **no** progression contained in a line `r + q^{D−1}ℤ` monochromatic,
with probability `1 − e^{−(ln 2/2 − o(1))k}`, for every fixed `a < 1/2` and every fixed `c` (beyond
`1/8` included), for every outer colouring of the labels. So
an argument whose final witness is a line progression cannot prove a van der Waerden upper bound for
the class `𝒞(c₀)`, even if it chooses the line from `Y`. With Proposition 2.2 of
`key-measurable-colorings`, the same holds for (S). (B) The exact form of moment certificates of
every order `m`, and a spread bound. No closure of Door 1, no bound on `W_r(k)` and no admissible `X`
is claimed.

**Base commit:** `061401f` (through `pr/door-one-continued`).

## The family of methods, and the scope

The template of the source, in the region of `source-only-1-8`: `N = q^D`, `D = ⌈k^a⌉`,
`0 < a < 1/2` fixed, `x_i(n) = n/q^i`, `y_i(n) = λx_i(n)` mod 1, full labels
`L(n) = ((U(x_i(n)))_i, (V(y_i(n)))_i)`, keys `κ(n) = ((V(y_i(n)))_i, ⌊q²‖Y(n)‖²⌋)` (source, Sections 2
and 6). Two colours. An outer colouring `c₀` of the labels (admissibility is not used), a frozen set
`X ⊆ 𝒦`, iid flips outside `X`. By Theorem 1 of `key-measurable-colorings`, the method succeeds iff
`𝒞(c₀) = { c₀∘L ⊕ 1_Y∘κ : Y ⊆ 𝒦 }` has a good member.

* `r = 2` throughout. The random shifted products of Fox and Hunter (arXiv:2606.02541,
  `c = (1−ε) ln 2` for `r ≥ (log k)^{3/ε}`) are not in this family, and nothing here concerns `W_r(k)`.
* Theorem A is a union bound over a family **fixed in advance**, all line progressions. It produces a
  `Y` that avoids all of them at once, so an argument that picks its witness from `Y` **inside that
  family** fails on this `Y`. An argument whose witness may leave the lines is not affected.
* The family is not Door 1 itself: a uniform `Y` avoids it, at every fixed `c`.
* `a` and `c` are **fixed** as `k → ∞`. Lemma A1 gives `o(k)` only then. The bound no longer gives
  `o(k)` once `1/2 − a ≲ (3/2) ln ln k/ln k`, where `D ln λ ≍ k^{2a} ln³ k` reaches `k`, or once `c`
  grows like `k^a/ln k`, where `8 ln q ≍ k`.

## A. Line progressions

A **line progression** is a `k`-term progression of `ℤ/N` contained in a line `r + q^{D−1}ℤ`, that
is, with step `d ∈ q^{D−1}ℤ ∖ {0}` and any start. There are `N(q−1)` of them. Its **type** is the pair
(key word `(κ(n_j))_j`, label word `(L(n_j))_j`). The colour word `(c₀(L(n_j)))_j` is a function of the
label word, for every `c₀`.

**Lemma A1 (an upper bound on the number of types).** Assume `λ < q`. Line progressions have at most

```
T_line = (k²λJ)^{D−1} · (⌊q²(D−1)/4⌋ + 1) · q(q−1) · 2(L+1)²,
L      = k(⌊k²λ/q⌋ + J + 1) + 2k(⌊q²/4⌋ + 1)
```

types, where `J = |V| = O(k³ log k)` (source, Lemma 2.5) and `k²λ = |U|`. In the region
(`0 < a < 1/2` fixed, `log λ ≤ h₀ log(2M)`, `h₀ = D⌈log k⌉²`, `M = ⌈k^m⌉` with `2a < m < 1`,
`D log q = ck log k + O(D log k)`), `λ < q` holds for large `k` and

```
ln T_line ≤ 8 ln q + O(D log λ + D log J + log k) = O(k^{1−a} log k + k^{2a} log³ k) = o(k).
```

*Proof.* Write `n₀ = v + q^{D−1}u` with `0 ≤ v < q^{D−1}`, `u ∈ ℤ/q`, and `d = q^{D−1}e′` with
`e′ ∈ {1, …, q−1}`. For `i < D`, `x_i(n)` and `y_i(n)` depend only on `n mod q^i`, hence on `v`: they
are **constant** along the progression. Their cells give a datum `σ ∈ (U × V)^{D−1}` (at most
`(k²λJ)^{D−1}` values), and `S₀ = Σ_{i<D} Y_i(v)²` splits as `B₀ = ⌊q²S₀⌋ ∈ {0, …, ⌊q²(D−1)/4⌋}` and
`f = q²S₀ − B₀`. The last coordinate is `x_D(n_j) = (ψ + s_j)/q` with `ψ = v/q^{D−1} ∈ [0, 1)` and
`s_j = u + je′ mod q`, and `y_D = λx_D` mod 1. So the type is a function of `(σ, B₀, u, e′)` and of
`(ψ, f) ∈ [0, 1)²`. We treat these parameters as free, which only overcounts.

Fix `(σ, B₀, u, e′)` and vary `(ψ, f)`. As `ψ` runs over `[0, 1)`, `x_D(n_j)` runs over an interval
of length `1/q` without wrapping, so it crosses at most `⌊k²λ/q⌋ + 1` boundaries of `U`. `y_D(n_j)`
runs over an arc of length `λ/q < 1`, which contains at most `J` boundaries of `V`, among them the cut
`±1/2` (it starts an interval of `V`). These are vertical lines `ψ = const`: at most
`k(⌊k²λ/q⌋ + J + 1)`. Between two of them, `qY_D(n_j) = λψ + A_j` with `A_j` a constant integer, and
there are at most two such pieces. The band of position `j` is
`⌊q²S₀ + (λψ + A_j)²⌋ = B₀ + ⌊h + 2λA_jψ + A_j²⌋`, after the bijective change of variable
`h = f + λ²ψ²`. In the `(ψ, h)` plane it changes only across the **lines** `h + 2λA_jψ + A_j² = n`.
Since `f + q²Y_D² ∈ [0, 1 + q²/4)`, only `n ∈ {1, …, ⌊q²/4⌋ + 1}` matter: at most `2k(⌊q²/4⌋ + 1)`
lines. Extended to full lines, these `≤ L` lines form an arrangement that refines the subdivision,
and the type is constant on each of its faces (cells, edges, vertices), half-open conventions
included. (A value of `ψ = v/q^{D−1}` determines `v`, so a `ψ` lying on a vertical boundary is a single
progression class `(v, u, e′)`, and its vertical face holds one type.) An arrangement of `L` lines has at most `1 + 2L² ≤ 2(L+1)²` faces. Multiply.

For the order of magnitude, `ln T_line ≤ 2 ln q + 2 ln q + 4 ln q + O(…)` and
`(D−1) ln(k²λJ) = O(D h₀ log M + D log k) = O(k^{2a} log³ k)`. ∎

**Theorem A (no line witnesses).** For every large `k` in the region, every outer colouring `c₀` of
the labels, and `Y ⊆ 𝒦` uniform,

```
Pr[ some line progression is monochromatic under c₀∘L ⊕ 1_Y∘κ ] ≤ 2 T_line 2^{−⌈k/2⌉}
                                                               = e^{−(ln 2/2 − o(1)) k}.
```

*Proof.* By Proposition 3 of `key-measurable-colorings`, `P` is monochromatic in `β` iff
`Y_P = {c₀ ≠ β} ∩ P`; this event depends only on the type of `P` and on `β`. A key occupies at most two
positions of a progression (Lemma 3 of `source-only-1-16`), so a type has at least `⌈k/2⌉` distinct
keys, and the event has probability `0` or `2^{−#keys} ≤ 2^{−⌈k/2⌉}`. Sum over the `T_line` types and
the two targets, and use Lemma A1. ∎

The proof uses `c` only through `ln q = ck ln k/D + O(log k)`: the theorem holds **for every fixed
`c`** and every fixed `a < 1/2`, beyond `1/8` in particular. It says nothing when `c` grows with `k`
like `k^a/ln k` or faster.

**Corollary A2 (scope of arguments).**
1. *Unconditional.* An argument that proves a van der Waerden upper bound for `𝒞(c₀)` by producing,
   for **every** `Y`, a monochromatic progression contained in a line, chosen in any way from `Y`, is
   wrong for every large `k`: most `Y` have none.
2. *For (S), which concerns proper `Y` only,* one needs a proper `Y` without a line witness. That
   holds when `π_slow > 2 T_line 2^{−⌈k/2⌉}`, which follows from Proposition 2.2 of
   `key-measurable-colorings` (`π_slow = 1 − o(1)`; its count of colour words of short-period label
   words is a sketch there). Under it, with probability `1 − o(1)` a uniform `Y` is proper and has no
   monochromatic line progression. A proof of (S) must then find its witness among progressions with
   step outside `q^{D−1}ℤ` that are not slow.
3. *The case of the P1a route where the final witness comes from Lemma E* of `ap-free-frozen-sets`.
   Its rich progressions all lie on the line of their fibre piece (`n₀ = r + q^{D−1}m`,
   `d = q^{D−1}e`). Such an argument is excluded, unconditionally for an upper bound on `𝒞`, and under
   Proposition 2.2 for (S). The P1a route with witnesses off the lines stays open.

**The right measure of a family of witnesses is its number of types, not of progressions.** This is
Proposition 1 of `supersaturation-is-global` with the union taken over types. A family `𝓕` of
progressions, of any size, is avoided by some proper `Y` as soon as `τ(𝓕) · 2^{1−⌈k/2⌉} < π_slow`,
where `τ(𝓕)` is its number of types. One line carries `q(q−1)` progressions and all lines together
`N(q−1)`, but they have only `e^{o(k)}` types.

### Relation to `supersaturation-is-global`

This note **complements** that note; it does not contradict it. Its Propositions 1, 2, 3 and its
Corollary 1′ (a range of more than `2^{k/2−3}` progressions) are unchanged. Two sentences there are
superseded or sharpened:

* `README.md`, lines 39–41: "*over all lines, a uniform `Y` has about `N q 2^{1−k}` induced classes on
  line progressions, a number that tends to infinity. So an argument that looks for its line
  depending on `Y` is not excluded.*" The conclusion is right as a statement about Corollary 1′, which
  does not exclude such arguments. The expectation is right too. But the heuristic it suggests, that a
  typical `Y` has line witnesses, is superseded by Theorem A. On average a type is shared by about
  `N(q−1)/T_line` progressions, and with probability `1 − o(1)` none of them is monochromatic.
* `README.md`, lines 74–78 ("*has a range over all lines, and this note says nothing against it. The
  route this leaves open is the P1a route*"): a statement of scope, true as written. Theorem A goes
  further for line witnesses (Corollary A2.3).

The sentence "*Arguments that choose their line from `Y` (the P1a route) are not excluded*" also
appears in the index line of this track (`auto-research/structured-flips/README.md`, line 40) and in
the sprint's list of results. It stays true of Corollary 1′; the index line of this note records
the complement.

### Sketch A3 (not proved in detail): how far the count goes

The same proof should work for progressions with step `d ∈ q^{D−s}ℤ`, contained in a class
`r + q^{D−s}ℤ`. Coordinates `i ≤ D−s` are constant. The last `s` depend only on
`(u mod q^s, e′ mod q^s)` and on the **single** real `ψ = v/q^{D−s}`. The coefficient of `ψ²` in
`q² Σ_{i>D−s} Y_i²` does not depend on `j`, so the same change of variable straightens the band
curves. This would give `ln T_s ≤ (2s + O(1)) ln q + o(k)`, hence Theorem A for
`s ≤ (ln 2/4 − ε) D/(c ln k)`. The pieces per coordinate and the centring jumps are not counted here.
**Sketch only.**

## B. Moment certificates of order m

Setting of `moment-certificates`: `Z` counts failure events and lies in `{0, …, n*}`, with
`S_j = E C(Z, j)`. A certificate of order `m` is the conclusion "every `W ∈ {0, …, n*}` with the same
`S_1, …, S_m` has `P(W = 0) > 0`".

**Theorem B1 (exact form).** A certificate of order `m` exists iff some real polynomial `u` of degree
`≤ m` has `u(0) = −1`, `u(z) ≥ 0` for `z ∈ {1, …, n*}`, and `E u(Z) < 0`. Here `E u(Z)` is computed
from `S_0, …, S_m` (`u = Σ y_j C(z, j)`).

*Proof.* (⇐) If `W` has the same moments, `0 > E u(W) ≥ −P(W = 0)`. (⇒) Without a certificate, the
vector `(S_j)_{j ≤ m}` lies in the polytope `conv{(C(z, j))_{j ≤ m} : 1 ≤ z ≤ n*}`. With one it does
not, and a separating hyperplane gives `u = y₀ + Σ y_j C(z, j) ≥ 0` on `{1, …, n*}` with
`E u(Z) < 0`. Since `E u(Z) ≥ y₀ P(Z = 0)`, `y₀ < 0`; normalise `y₀ = −1`. ∎

For `m = 2` the certifying `u` include `z − 1` (the first moment) and `(z−1)(n*−z)/n*`, which is
`f − 1` for the `f` of Theorem 2 of `moment-certificates`.

**Lemma B2 (Lagrange).** If `u` is as above and `1 ≤ z₀ < … < z_m ≤ n*` are integers, then
`Σ_i u(z_i) |ℓ_i(0)| ≥ 1`, where `ℓ_i(0) = Π_{j≠i} z_j/(z_j − z_i)`.

*Proof.* Interpolation is exact in degree `≤ m`: `−1 = u(0) = Σ_i u(z_i)ℓ_i(0)`, and `u(z_i) ≥ 0`. ∎

**Corollary B4 (spread).** Suppose the law of `Z` is certified at order `m`. Let `g ≥ 1` be an
integer and let `W₀, …, W_m ⊆ {1, …, n*}` be non-empty, with `|z − z′| ≥ g` whenever `z ∈ W_i`,
`z′ ∈ W_j`, `i ≠ j`. Then

```
P(Z = 0) > min_i P(Z ∈ W_i) · (g/n*)^m.
```

*Proof.* Take `z_i ∈ W_i` minimising `u` on `W_i`. Then `|ℓ_i(0)| ≤ (n*/g)^m`, so by B2
`Σ_i u(z_i) ≥ (g/n*)^m`. Hence
`P(Z = 0) > E[u(Z); Z ≥ 1] ≥ Σ_i P(Z ∈ W_i) u(z_i) ≥ min_i P(Z ∈ W_i) · (g/n*)^m`. ∎

**Proposition B3 (order 3).** For every real `t > 0`, `u_t(z) = (z−1)(z−t)²/t²` satisfies the
conditions of B1. So a law is certified at order 3 as soon as

```
E[(Z − 1)(Z − t)² ; Z ≥ 1] < t² P(Z = 0).
```

Example (checked): `Z ∈ {0, n*/2}` with equal weights, `n* = 1000`. Two moments do not certify
(`S_1 − 2S_2/n* = 125.25 ≥ 1`), three do (`E u_t = −1/2`).

**Reading.**
* Theorem 3 of `moment-certificates` assumes that the second moment certifies, and it is correct. Its
  conclusion, that all failure mass beyond `O(1)` sits on catastrophes, is specific to order 2 and
  **does not extend to order 3**. There, clustering around any level `t` suffices, provided it is
  tight: its weighted spread must stay below `t² P(Z = 0)`. At order `m`, Corollary B4 gives the price.
  Outside a mass `P(Z = 0)(n*/g)^m`, `Z` must live near at most `m` values. Since `n* ≤ 2N²`, a law
  whose success is rare (`P(Z = 0) ≤ N^{−2m−ε}`) is certifiable at order `m` only if `Z` is
  concentrated to that precision.
* *Why there is no general barrier.* A point mass on a good `Y` is certified at order 1, so every
  barrier on moments must restrict the class of laws. The natural restriction, `d`-wise independent
  laws (Theorem 1 of `moment-certificates`), reduces everything to the iid law with the same
  marginals. **Open:** under an iid `Y` of density `k^{−b_X}`, beyond `b_X/4`, is the law of `Z`
  concentrated near at most `m` values, to precision `P(Z = 0)`?

## What this says about Door 1

A definitive barrier is a van der Waerden upper bound for `𝒞(c₀)` (Corollary of
`key-measurable-colorings`); it is not proved here. For fixed `a < 1/2` and fixed `c`, Theorem A places
a constraint on any such bound: its monochromatic progression cannot be a line progression. With Proposition 2.2 of that note, a proof
of (S) cannot use slow words or line progressions either, and must use progressions with step outside
`q^{D−1}ℤ` (outside `q^{D−s}ℤ` for `s ≲ (ln 2/4)D/(c ln k)` if Sketch A3 holds). This is a constraint
on proofs, not a statement about where a uniform `Y` fails: no probability bound for the remaining
progressions is given here.

## What is not claimed

* No bound on `W_r(k)`, no closure of Door 1, nothing about Fox–Hunter (`r = 2` here).
* Corollary A2.2, and A2.3 for (S), inherit the status of Proposition 2.2 of
  `key-measurable-colorings`. Theorem A and Corollary A2.1 do not depend on it.
* Theorem A needs `a < 1/2` and `c` **fixed**. `ln T_line` contains `(D−1) ln λ`, whose bound
  `O(k^{2a} ln³ k)` is `o(k)` only while `1/2 − a ≫ (3/2) ln ln k/ln k`, and `8 ln q`, which is `o(k)`
  only while `c ≪ k^a/ln k`. Sequences `a_k → 1/2` with `ln λ ≍ ln q` give `D ln λ ≍ ck ln k`, and the
  count fails. No counterexample to the conclusion is given there: the bound simply says nothing.
* Sketch A3 is a sketch.
* Lemma 3 of `source-only-1-16` (multiplicity two) is cited, not re-proved; on the toys the maximum
  multiplicity on line progressions is 1.
* B1–B4 describe certificates. They close no class of laws.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-line-witnesses/verify.py
```

Expected: exit code 0, a JSON summary equal to `RESULT.json`, and last line
`Test passé : all checks pass`. Standard library only, about 10 seconds.

## Checks in `verify.py`

1. **Lemma A1, exactly**, on toys of the literal template (`U`, adaptive mesh `V`, bands, keys and
   labels): `(k, q, D, λ) = (3, 15625, 2, 15624), (3, 15625, 2, 7), (3, 125, 3, 124),
   (4, 2401, 2, 2399)`, random `(u, e′)`, every `v`. Checked: coordinates `i < D` constant, the number
   of vertical boundaries, constancy of the coordinate-`D` cells and of `A_j` on each vertical cell, at
   most two pieces `A_j`, the band law, and the type as a function of the face. The toys are chosen so
   that tens of thousands of values of `ψ` share a vertical cell. Without that the check would have no
   grip, since at small `q` every progression has its own type (more keys than points). Three mutants
   must be rejected: `V` boundaries omitted, `λ²ψ²` dropped from `h`, `J` dropped from the vertical
   bound. Multiplicity `≤ 2` on every line progression of two small toys.
2. **Scale.** `ln T_line ≤ (k/2) ln 2 / 1.01` from `ln k ≈ 34, 80, 189, 1272` for
   `a = 0.3, 0.4, 0.45, 0.49` and `c ∈ {1/9, 1/2, 1}`, with `m = (1+2a)/2`. The hypotheses `λ < q` and
   `J ≤ q` are checked as upper bounds of `ln λ` and `ln J` against a lower bound of `ln q`. The
   thresholds stated here are compared with the computed ones. Hence
   `2 T_line 2^{−⌈k/2⌉} ≤ 2e^{−(1/101)(k/2) ln 2}`. Negative control: the bound fails at `a = 1/2`.
3. **Moments.** Lemma B2 on random exact cases, with the negative control that the signed sum is
   `−1`; Proposition B3's example; the `m = 2` identity (an identity only); Corollary B4 with
   singletons `W_i` on random certified laws.
4. **Frozen statement.** Nine sentences (the scope, `T_line`, Theorem A, Corollary A2.1–A2.3, the
   scope of "What is not claimed") must occur verbatim, and four sections ("The family of methods",
   "A. Line progressions", "What this says about Door 1", "What is not claimed") must have the
   sha256 recorded in `verify.py`.
5. **Provenance.** MANIFEST hashes of the four files, `RESULT.json` included; summary equal to
   `RESULT.json`. Every check stops the run on failure, so `--write` (and `--manifest`) cannot record a
   failing run.
