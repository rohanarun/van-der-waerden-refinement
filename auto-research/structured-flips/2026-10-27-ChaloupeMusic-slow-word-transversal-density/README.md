# How sparse can a transversal of the slow words be?

**Status:** structural research, with proofs and exact finite checks. It
addresses step (D) of `key-measurable-colorings`: a lower bound on the
density of a key set that meets every slow word. Six results.

1. A **fractional barrier**. Every counting, averaging or LP argument stops
   at density `1/k`, which is what is already proved. Going further needs
   integrality.
2. A **reduction** of (D) to a covering problem for the signed combinatorial
   lines of `[p]^s` (Hales–Jewett type), with `s ≈ log_p` of the fibre
   length.
3. **A lower bound `k^{−a−o(1)}` for digit-linear sets.** These are the sets
   defined by unions of linear conditions on base-`p` digits. They include
   the digit sets, which meet every progression at `k^{−a+o(1)}` but
   saturate some. Each digit-linear transversal has density at least
   `k^{−a−o(1)}` on every fibre piece.
4. A **matching construction**, up to a constant factor, for linear sets of
   the box.
5. A **nonlinear counterexample to the box route**. A quadratic set
   `{Σ x_i² ∈ R}` meets every signed line at density `O(log p / p)`,
   whatever `s`. The box problem therefore has answer `p^{−1+o(1)}`, and
   boxes alone cannot prove (D) beyond the trivial exponent: a proof must
   use progressions with carries.

6. **Inside the key-measurable class**, with proper colorings (§ 6). Random
   key sets are proper at `k^{−a+o(1)}`, and the provable lower bound stays
   at the trivial exponent `1`. A closure must act on lenses with `λe`
   divisible by many primes, or with non-integer slope.

(D) for arbitrary sets stays open; § 5 says what a proof must use.
No closure of Door 1 and no new bound on `c` is claimed.

**Scope.** (D) does not close a class of certificates: Theorem A of the
keyed-local-lemma note and Proposition 5 of `exact-door-one-condition`
already do that. (D) fixes the **random benchmark**. A random key set whose
transversal density is `k^{−b_Y}` puts the first-moment threshold at
`c > b_Y/4`. A lower bound `k^{−a}` therefore says that no well-built random
`X` can, even in principle, pass `1/8` by the first moment. A random key
set reaches `k^{−a+o(1)}` and is a **proper** 2-coloring of the slow words,
inside the class of key-measurable colorings (Proposition 7), so `k^{−a}`
would be optimal. The digit sets also reach `k^{−a+o(1)}` as plain
transversals, but they are neither key-measurable nor proper (they saturate
some progressions, radar-dd). This note proves the bound for digit-linear
sets, and shows why counting alone cannot prove it, for arbitrary sets or
inside the key-measurable class (§ 6).

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, through
`pr/door-one` (`00375ff`, PR #20).

**Depends on:** `2026-10-26-ChaloupeMusic-ap-free-frozen-sets` (the fibre
model (S4), the scale `Y₀`, the hitting property (H)), and on the
decomposition into (D) and (S) of
`2026-10-27-ChaloupeMusic-key-measurable-colorings` (radar-63, sprint 4,
not in this tree).

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-slow-word-transversal-density/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. Standard library only, about five seconds.

## Setting

As in `ap-free-frozen-sets` (S4), a fibre piece is an interval `J` of
indices `m` (single-label, no wraparound), with `|J| ≥ 2Y₀`,
`Y₀ = ⌊q/(2048k²λ)⌋` and `ln Y₀ = (c − o(1)) k^{1−a} ln k`. Every `k`-AP
contained in `J` is a case (ii) word, and (I) says that

```
S_J = { m ∈ J : κ(r + q^{D−1} m) ∈ X }   meets every k-AP contained in J.   (H)
```

Call such an `S ⊆ J` a **transversal** of `J`. The question (D) is the least
relative density `|S|/|J|` of a transversal. What is known:

* at least `⌊|J|/k⌋/|J|` (disjoint windows of step 1);
* at most `≈ ln|J| / (k ln k)` (the digit sets of P1a: some base-`p` digit is
  `0`, with `p ≤ k` prime), which is `k^{−a+o(1)}` at `|J| ≈ Y₀`.

Write `p` for the least prime `≥ k`, so `k ≤ p < 2k`. Every `p`-AP contains
a `k`-AP, so a transversal of `J` meets every `p`-AP contained in `J`.

## 1. The fractional barrier

**Theorem 1.** Let `𝒜` be the family of `k`-APs contained in `J`. Its
fractional transversal number, `min Σ_x w_x` over `w ≥ 0` with
`Σ_{x∈A} w_x ≥ 1` for every `A ∈ 𝒜`, lies in `[⌊|J|/k⌋, |J|/k]`.

*Proof.* `w ≡ 1/k` is feasible. The `⌊|J|/k⌋` disjoint windows of step 1
give a dual solution of that value. ∎

**Consequence.** Any lower bound obtained as a nonnegative combination of the
hitting constraints `|S ∩ A| ≥ 1` (double counting, averaging over
progressions or over dilations, LP duality) is at most the fractional
value, that is, density `1/k`. It cannot exceed what is already proved. With
a perfect (S), density `1/k` closes only `c > 1/4`. A bound `k^{−a}` needs an
argument that sees **integrality**, of Ramsey or Hales–Jewett type. The same
holds in the box of § 2: there `w ≡ 1/p` is feasible.

The integrality gap is real, and of known size. Greedy gives
`τ ≤ τ*(1 + ln Δ)`, with `Δ ≤ |J|` the largest number of progressions
through a point, so integral transversals have density `O(ln|J|/k)`. Digit
sets do better by a factor `ln k`. Between `1/k` and `ln|J|/(k ln k)`, only
integrality can decide.

## 2. Reduction to signed combinatorial lines

Identify `[p]^s` with `{0,…,p−1}^s`. A **signed combinatorial line** is given
by disjoint sets `S₊, S₋ ⊆ [s]`, not both empty, and values `z` on the other
coordinates `F`. Its `p` points are `j` on `S₊`, `p−1−j` on `S₋` and `z` on
`F`, for `j = 0, …, p−1`. Let `λ(p, s)` be the least density of a subset of
`[p]^s` meeting every signed line.

**Lemma 2 (boxes).** Let `B_t = t p^s + [0, p^s)`, and map `x ∈ B_t` to its
`s` low base-`p` digits. Each signed line of `[p]^s` is then a `p`-AP of `ℤ`
contained in `B_t`, with step `Σ_{S₊} p^i − Σ_{S₋} p^i` (no carries, since
the digits stay in `[0, p)`). Consequently, for every transversal `S` of `J`
and every `s` with `p^{s} ≤ |J|`,
`|S| / |J| ≥ (1 − 2p^{s}/|J|) λ(p, s)`.

*Proof.* Consecutive points differ by `Σ_{S₊} p^i − Σ_{S₋} p^i`, because each
coordinate in `S₊` rises by one and each in `S₋` falls by one, without
leaving `[0, p)`. So each aligned box `B_t ⊆ J` carries a set `S ∩ B_t` that
meets all signed lines, of size at least `λ(p,s)p^s`. The aligned boxes
inside `J` cover all of `J` except at most `2(p^s − 1)` points, at its two
ends. ∎

**Corollary.** (D) at exponent `a` follows from
`λ(p, s) ≥ s / p^{1+o(1)}` for `s ≤ p^{1−δ}`. Take `s = ⌊log_p |J|⌋ − 1`, so
that `s = (c − o(1)) k^{1−a}`, and `s/p = k^{−a−o(1)}`.

## 3. (D) for digit-linear sets

**Theorem 3 (linear transversals of the box).** Let `T ⊆ 𝔽_p^s` be a union
of `r` affine hyperplanes `{x : ⟨w_m, x⟩ = v_m}`, with `w_m ≠ 0`, and
suppose `T` meets every signed line (coordinates read in `𝔽_p`, so
`p − 1 − j = −1 − j`). Then `r ≥ p` or `r ≥ s / (1 + log₂ p)`. The density
of `T` is at least `min(r, p)/(2p)`.

*Proof.* Suppose `r < p` and `s ≥ r + ⌊r log₂ p⌋ + 1`. Remove one coordinate
of `supp w_m` for each `m`, and let `S_A` be `⌊r log₂ p⌋ + 1` of the
remaining coordinates. No `supp w_m` lies inside `S_A`. The map
`u ↦ (⟨w_m, u⟩)_m` from `{0,1}^{S_A}` to `𝔽_p^r` is not injective,
since `2^{|S_A|} > p^r`. A collision gives `ε = u − u' ∈ {0, ±1}^{S_A}`,
nonzero, with `⟨w_m, ε⟩ = 0` for every `m`. Take `S₊ = {ε = 1}`,
`S₋ = {ε = −1}`, and `F` the complement of `supp ε`; `F` contains the
removed coordinates. The line through `x₀(z)` (`0` on `S₊`, `−1` on `S₋`,
`z` on `F`) is `x₀(z) + jε`, and each `⟨w_m, ·⟩` is constant on it. Since
`supp w_m ⊄ S_A ⊇ supp ε`, `w_m` has a nonzero coefficient on `F`, so the
bad `z` for `m` form an affine hyperplane of `𝔽_p^F`. Fewer than `p` such
hyperplanes do not cover `𝔽_p^F`. Some `z` gives a line that misses `T`.
For the density: `r'` distinct affine hyperplanes cover at least
`r' p^{s−1} − C(r', 2) p^{s−2} ≥ (r'/2) p^{s−1}` points when `r' ≤ p`. ∎

**Digit-linear sets.** A set `S ⊆ J` is **digit-linear** (base `p`) if it is
a union of sets `{x : Σ_i w_{m,i} dig_i(x) ≡ v_m (mod p)}`, where `dig_i` is
the `i`-th base-`p` digit and the forms may use any digits. This includes:

* the digit sets of P1a (`w_m = e_i`, `v_m = 0`);
* every rule that reads a fixed set of digits linearly.

On an aligned box `B_t`, the digits of index `≥ s` are fixed. So `S ∩ B_t`
is either all of `B_t`, or a union of affine hyperplanes in the low digits
(forms supported on high digits become constant there).

**Corollary 4.** A digit-linear transversal of `J` has density at least

```
(1 − 2/p) · min( 1/2 , s / (2p(1 + log₂ p)) ),   s = ⌊log_p |J|⌋ − 1.
```

At `|J| ≈ Y₀`, this is `k^{−a−o(1)}`: a **lower bound** for every
digit-linear transversal. It is reached only for meeting, by the digit sets.
Those are not proper colorings: they saturate some progressions (radar-dd,
S7). Properly, the density `k^{−a+o(1)}` is reached by a uniform random set
of keys, globally and key-measurably (Proposition 7). The lower bound is
therefore at the right exponent. What falls is only "reached by the digit
sets": they meet every progression but saturate some. Check 6
computes `−log_k` of the bound: `0.3185`, `0.4685`, `0.5085` for
`a = 0.3`, `0.45`, `0.49` at `k = 2^739`, `c = 1/9`, with `ln|J|` at leading
order `c k^{1−a} ln k`. The excess over `a` (`0.0185`) is the factor
`2p(1 + log₂ p)`, that is `ln(2 log₂ k)/ln k`, which tends to `0`. The digit
sets sit at `0.3043`, `0.4543`, `0.4943`.

*Proof.* Lemma 2 applied to aligned boxes, Theorem 3 in each box. A box where
`S` is everything has density `1`. ∎

## 4. The box bound is tight for linear sets

**Proposition 5.** For `r = ⌊s log_p 3⌋ + 1`, there are forms
`w_1, …, w_r ∈ 𝔽_p^s` whose common kernel contains no nonzero vector of
`{0, ±1}^s`. The set `T = ∪_m {⟨w_m, x⟩ = 0}` then meets every signed line,
with density at most `r/p`.

*Proof.* For random forms, a fixed nonzero `ε` lies in the common kernel
with probability `p^{−r}`, and `3^s p^{−r} < 1`. On a line of pattern `ε`,
some `⟨w_m, ε⟩ ≠ 0`, so `⟨w_m, x₀ + jε⟩` runs through all of `𝔽_p` as `j`
does, and in particular hits `0`. ∎

So, for linear sets of the box, the least density lies between
`s/(2p(1 + log₂ p))` and `s ln 3/(p ln p) + 1/p`, a ratio that tends to
`2 ln 3/ln 2 ≈ 3.17`. Check 3 builds such families exhaustively for
`(p, s) = (7, 4)`, `(7, 6)`.

Proposition 5 concerns signed lines in one box, not every `k`-AP of `J`. It
does not give a sparser transversal of the slow words than the digit sets.
For linear sets, the box problem has the answer `s/p^{1+o(1)}`. For general
sets it does not, as § 4.1 shows.

### 4.1 A quadratic set beats every linear one in the box

**Proposition 6.** Let `1 ≤ s < p` and let `R ⊆ 𝔽_p` meet every set
`w + u·Q₀`, where `w ∈ 𝔽_p`, `u ≠ 0` and `Q₀ = {y² : y ∈ 𝔽_p}`. Then
`T = {x ∈ 𝔽_p^s : Σ_i x_i² ∈ R}` meets every signed line. Such an `R`
exists with `|R| ≤ ⌈log₂(2p)⌉ + 1`, and the density of `T` is at most
`|R| (1/p + p^{−s/2})`.

*Proof.* On the line of pattern `(S₊, S₋)`, the coordinates are `j` on
`S₊`, `−1 − j` on `S₋` and constant on `F`. So
`Σ x_i² = (|S₊| + |S₋|) j² + βj + γ` for some `β, γ ∈ 𝔽_p`. The leading
coefficient lies in `[1, s]`, hence is nonzero modulo `p`. As `j` runs over
`𝔽_p`, the value runs over a set of the form `w + u·Q₀` with `u ≠ 0`
(complete the square; `p` is odd), which `R` meets. Up to multiplication
by `u`, the sets `u·Q₀` are of two kinds, `Q₀` and `{0} ∪` non-squares, so
there are `2p` sets `w + u·Q₀`, each of size `(p+1)/2`. A random `m`-subset
misses a given one with probability at most `2^{−m}`. For
`m = ⌈log₂(2p)⌉ + 1`, some `R` meets them all. The diagonal quadratic form
takes each value `p^{s−1} + O(p^{s/2})` times (Gauss sums). ∎

So `λ(p, s) = O(log p / p)` for every `s < p`. In the regime of Lemma 2
(`s ≈ c k^{1−a}`), this is far below the linear bound `s/(2p(1 + log₂ p))`.
Check 8 confirms it exhaustively (`p = 7`, `s ≤ 6`; `p = 11, 13`): about
`|R|/p` whatever `s`, with `|R| = 3, 4, 4`.

The quadratic set does **not** lift to the fibre. Read on base-`p` digits,
`{Σ_i dig_i(x)² ∈ R}` misses hundreds of `p`-APs of `[p^L]` (check 9: 344 in
`[7³]`, 447 in `[5⁴]`). None of them is a signed line of an aligned box,
since Proposition 6 meets all of those. They are progressions whose digits
do not move as `j, −1−j` or stay fixed: steps with carries, or steps not of
the form `Σ ±p^i`. The box sees only the carry-free signed lines.

## 5. What (D) needs now, exactly

Lemma 2 is valid, but its target is false. By Proposition 6, every box
`[p]^s` with `s < p` has a transversal of its signed lines of density
`O(log p/p) = k^{−1+o(1)}`. So no argument that restricts a transversal of
`J` to carry-free boxes can prove more than the trivial exponent `1`.
Together with Theorem 1:

* counting, averaging and LP stop at `1/k` (Theorem 1);
* Hales–Jewett-type arguments on carry-free boxes stop at `k^{−1+o(1)}`
  (Proposition 6);
* a lower bound `k^{−a−o(1)}` is proved for digit-linear transversals
  (Corollary 4). It is at the right exponent, since random key sets reach
  `k^{−a+o(1)}` properly (Proposition 7), but not through digit sets.

A proof of (D) for arbitrary sets must use **progressions whose steps carry
between scales**: the interaction of the scales of `ℤ`, which the
quadratic set of § 4.1 cannot survive. The open question is now this:

> **(D).** For `ln|J| = k^{1−a+o(1)}`, does every set meeting every `k`-AP
> of `J` have density `k^{−a−o(1)}`, or is there a transversal of density
> `k^{−1+o(1)}` that is robust to carries?

The second answer would reopen the random benchmark past `1/8`. No such
transversal is known: the digit sets and random key sets reach
`k^{−a+o(1)}`, and Proposition 6 does not lift.

**Fibres and the cross-fibre count.** This answers the remark in the S6
brief, under the induced-class form of `key-measurable-colorings`,
Proposition 3, **for progressions whose keys are distinct**. Rich
progressions inside a single fibre line (step `q^{D−1}e`) number
`N^{1+o(1)}`: `N/q` lines times `q²` progressions. For a random key set of
transversal density `k^{−b_Y}`, the first moment of induced classes on those
with distinct keys is `N^{1+o(1)} ρ^{γk}`. It vanishes for every
`c < γ b_Y`, twice the benchmark threshold. This does **not** cover the
whole line. Along a line the bands are `s_j = s₀ + jμ`, and a key folds when
`s_j + s_{j'} ≈ 0` (Lemma F of S2, reflection symmetry of the bands). When
`2s₀ + tμ ≡ 0`, every pair `(j, t − j)` folds. That happens on about `Nk`
progressions, where an induced class needs only `≈ γk/2` keys. There the
first moment vanishes only for `c < γb_Y/2`, the benchmark itself. Unless
the two positions of a folded pair always carry different `c₀`-colors, which
is not proved here, single-line progressions **can** be binding. Where an
(S) step must act is therefore not established (the referee's (w2)).

## 6. Inside the key-measurable class, with proper colorings

`key-measurable-colorings` (Theorem 1) shows that Door 1 lives in the class
`𝒞 = {c₀∘L ⊕ 1_Y∘κ}`. On a fibre piece the box `V` is constant, so a
key-measurable `Y` reads `S_J = {m : ⌊C + (s₀ + λm)²⌋ ∈ B_V}`. Here `B_V` is a
set of bands shared by every fibre of the box, with different `(C, s₀)`.
Along a `k`-AP of step `e`, the bands form a **lens**
`b_j = ⌊θ + vj⌋ + Lj²`, with `L = λ²e²` (Lemma 1 of the single-label lenses
note). radar-dd (S7) points out that the right object is a **proper**
2-coloring: `Y` meets every slow word (a transversal) **and** contains none
entirely (non-saturation). Digit sets fail the second condition, since they
contain classes `x ≡ −t (mod p)` and hence `k`-APs of step `p`.

**Lemma 8 (a lens has many bands).** `j ↦ ⌊θ + vj⌋ + Lj² = ⌊g(j)⌋`, with
`g(j) = θ + vj + Lj²` strictly convex and `L ≥ 1` an integer. Its `k` values
contain at least `k/2 − 1` distinct integers.

*Proof.* The increments `g(j+1) − g(j) = v + L(2j+1)` grow by `2L ≥ 2` at
each step, so at most one of them lies in `(−1, 1)`. On each side of it,
`⌊g⌋` is strictly monotone. Each integer is taken at most once on each
side, and the step across the small increment adds at most one more
repetition. ∎

**Proposition 7 (random key sets are proper at `k^{−a+o(1)}`).** Let
`H = 6 ln q + O(D ln³ k)` be the log of the number of key words of slow
progressions together with their run codes (`source-only-1-16`, Theorem 8;
the codes carry the colour of each `s`-heavy label). Let each key lie in
`Y` independently with probability `ρ = 2(1+δ)H/k = k^{−a+o(1)}`. Then,
with probability `1 − o(1)`:

1. `Y` meets every slow word and contains none entirely;
2. `c₁ = c₀∘L ⊕ 1_Y∘κ` makes no slow progression monochromatic, that is,
   `Y_P ≠ {c₀ ≠ β} ∩ P` for every slow `P` and both `β`.

*Proof.* (1) A slow word carries at least `k/2 − 1` distinct keys (Lemma 8
within a fibre piece, where the key is the band). The bad event for one word
has probability at most `(1−ρ)^{k/2−1} + ρ^{k/2−1}`. Summing over at most
`e^H` words gives `e^{H − (1+δ)H(1 − o(1))} + e^{H} ρ^{k/2−1} → 0`.
(2) The event `Y_P = {c₀ ≠ β} ∩ P` also depends on the colour word of `c₀`,
which the key word does not fix. It is paid in two parts, as in
`key-measurable-colorings` (radar-63, in this PR, after the
referee's (s3)). In case (ii), the run codes fix the colour of every
`s`-heavy label, and the event prescribes `Y` on at least `k/2 − 1`
distinct keys; the factor `exp(O(D ln³ k))` is already in `H`. In case (i),
at least `(1/2 − ε)δ_s k` light positions of colour `≠ β` must lie in `Y`,
so at least `x = ⌈(1/2 − ε)δ_s k/2⌉` distinct keys; with no colour word
indexed, this has probability at most `C(k, x)ρ^x = e^{−Ω(k ln k)}` per key
word. ∎

So inside `𝒞`, proper colorings exist at density `k^{−a+o(1)}`. Propriety
cannot push the least density above that; it can only keep it there or push
it lower. The question is whether it can go lower.

**Theorem 9 (the fractional barrier holds in `𝒞`).** Giving every band the
weight `1/(k/2 − 1)` gives every lens weight at least `1` (Lemma 8). Any
lower bound on the density of a key-measurable transversal obtained by
counting, averaging or LP duality is therefore at most `2/(k − 2)`.
Propriety adds packing constraints ("not all of a word"), which a fractional
relaxation satisfies as soon as the weights are below `1`. It does not
change the bound.

**Proposition 10 (integer lenses are cheap).** Let `p` be prime, `k ≥ p`,
and `R` meet every `w + u·Q₀` (§ 4.1). Then `{b : b mod p ∈ R}`, of density
`O(log p / p)`, meets every **integer** lens `c + vj + Lj²` (`v ∈ ℤ`) with
`p ∤ L`. It misses some lens with `p | L` and `p | v`.

*Proof.* As in Proposition 6: over a full period of `j` modulo `p`, a
quadratic with leading coefficient `L ≢ 0` runs over `w + u·Q₀`. ∎

**What this gives, and the exact exponent.** Inside `𝒞`, the provable lower
bound on the least density of a proper key-measurable coloring is the
trivial `≈ 2/k`, exponent `1`. The upper bound is `k^{−a+o(1)}`
(Proposition 7). Theorem 9 rules out counting arguments. Proposition 10 shows
that a lower bound cannot rest on lenses with integer slope and `p ∤ λe`.
Two families remain where a closure could act:

* lenses with `λe` divisible by many primes (`e` up to `E ≈ q^{1−o(1)}`
  can carry `≈ ln E / ln k = k^{1−a+o(1)}` primes near `k`). This is the
  multi-scale structure, and it is where residue rules need many moduli
  (radar-dd's kernel theorem: `Π M ≥ N^{1−o(1)}`);
* lenses with non-integer slope `v`, where `⌊θ + vj⌋` is a Beatty sequence.
  This is where N2a's construction stops at `√k`. That barrier is
  constructive; no matching lower bound is known.

A closure of (D) in `𝒞` must use one of these two families, and an argument
of integrality on it. None is given here.

## What `verify.py` checks

1. Lemma 2: for `(p, s) ∈ {(3, 3), (5, 3), (7, 2)}`, every signed line maps to
   a `p`-AP of `ℤ` inside its box, with the stated step and no carry.
   Control: the "line" that wraps coordinates modulo `p` (start not at `0`
   on `S₊`) is not an AP of `ℤ`.
2. Theorem 3, exhaustively: no single affine hyperplane is a transversal for
   `(p, s) = (3, 3), (3, 4), (5, 4)`, as the theorem requires (`r = 1`,
   `s ≥ 2 + ⌊log₂ p⌋`). Control: below the threshold, `(3, 2)` and `(5, 2)`
   have one.
3. Proposition 5: the families found for `(7, 4)` and `(7, 6)` meet every
   signed line (all 4 160 and 413 792 lines enumerated), with densities
   `127/343` and `1105/2401`, below `r/p`.
4. The union bound of Theorem 3, `≥ min(r, p)/(2p)`, on 300 random
   families of affine hyperplanes in `𝔽_5^4` and `𝔽_7^3`, counted exactly.
5. Theorem 1: for `(Y, k) = (12, 3), (15, 3), (14, 4), (16, 4)`, the
   fractional value lies in `[⌊Y/k⌋, Y/k]`, while the exact integral minimum,
   by exhaustive search, is `6, 7, 5, 6`. The integrality gap that § 1 says
   only integrality arguments can see is already visible at this size.
6. The exponents of Corollary 4 and of the digit sets at `k = 2^739`,
   `c = 1/9`, `a ∈ {0.3, 0.45, 0.49}` (exact integer `ln` via `Decimal`).
7. Digit sets in `[p^L]`: restricted to each aligned box, they are unions
   of coordinate hyperplanes, and they meet every `p`-AP of `[p^L]`, for
   `(p, L) ∈ {(3, 4), (5, 3)}`.
8. Proposition 6: for `p = 7` (`s = 2, …, 6`), `p = 11` (`s = 3, 4, 5`) and
   `p = 13` (`s = 3, 4`), a smallest `R` meeting every `w + u·Q₀` is found
   exhaustively, and `{Σ x_i² ∈ R}` meets every signed line. Its density is
   within `p^{−s/2}|R|` of `|R|/p`, while the linear lower bound grows with
   `s`.
9. The digit-quadratic set misses `p`-APs with carries in `[7³]` and
   `[5⁴]`. The control proves the box is the wrong place to look.
10. Lemma 8 on 20 000 random lenses (`k < 40`, rational `θ, v`, integer
    `L`): at least `k/2 − 1` distinct values in every one.
11. Proposition 10 for `p = 7, 11, 13` on 20 000 random integer lenses with
    `p ∤ L` (no miss). Control: `p | L`, `p | v` and `c ∉ R` misses.

## What is not claimed

* (D) for arbitrary sets. The box route is closed by Proposition 6; (D)
  stays open.
* That digit-linear sets are the only good transversals. Theorem 3 says
  nothing about nonlinear sets.
* Anything on (S). The cross-fibre remark does not establish where (S) must act.
* A lower bound in `𝒞` above the trivial exponent: § 6 says where one must
  come from, not that it holds.
* No closure of Door 1 and no bound on `c`.
