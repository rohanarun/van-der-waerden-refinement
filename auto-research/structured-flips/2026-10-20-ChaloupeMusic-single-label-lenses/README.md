# Structured flips on single-label progressions: what a frozen key set must hit

**Status:** structural research. One partial positive result: a residue rule
meets, without saturating, every block of the `e = 1` single-label family,
the family behind the iid obstructions. One negative result: an exact family
on which that rule, and every rule of its kind, is constant. One exact
reduction. No new bound is claimed, and no admissible `X` passing (I) on all
of case (ii) is known.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.

**Sources:** the OpenAI manuscript *Quantitative Superexponential Bounds for
van der Waerden Numbers*, pinned in `source-manifest.json` (commit
`fd4aeeb`; Section 2 for the meshes and dilation, Section 6 for the keys).
Also `short-period-runs-proof.md` (case (ii)) and the single-label families
of the open contribution
`short-period-sensitivity/2026-10-20-ChaloupeMusic-single-label-obstructions`
(its Lemma A, Lemma C, Theorem 1 and `P2`).

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-20-ChaloupeMusic-single-label-lenses/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and a JSON
summary equal to `RESULT.json`. It takes about 20 seconds and uses only the
standard library.

## The question

Every proof in this repository colors `C(n) = c₀(L(n)) + E_{κ(n)}`, with iid
Bernoulli(`p`) flips `E` on the keys `κ(n) = (V-box of ỹ(n), ⌊‖qỹ(n)‖²⌋)`.
On case (ii) (short-period progressions) this costs `b < a` (band words) and
`a + b < 1` (heavy runs). Theorem 1 of the single-label obstructions note
shows that iid flips cannot avoid either cost. Its family uses step `e = 1`
in the top coordinate, every low part `r`, and many blocks per `r`. Below it
is called the `e = 1` family, or `P3`. `P1` denotes `r = 0` with every step
`e`.

Porte 1 freezes a set `X` of keys instead: `c₁ = c₀ ⊕ 1_X`, then iid flips on
the other keys. The team's reduction (radar-1a, radar-7b) asks for two
conditions. The implication "they give every `c < 1/4`" is theirs and is
not proved here.

* **(I)** Every case (ii) progression has a key of `X` at a position of its
  dominant color, **without saturating it**. At least `ω(k^{1−a})` keys of
  the dominant color must stay outside `X`; more precisely `ω(H/(b log k))`,
  with `H` the log of the number of case (ii) key words. Without that clause
  the frozen keys make the block monochromatic for every flip assignment.
  Taking `X` = all keys satisfies the first half and (II), and freezes
  everything.
* **(II)** Every rich progression has at most `εk` keys in `X`.

A remark on (II): for the union bound only a weaker condition is needed. A
rich `P` can be monochromatic in color `β` only if every key of `X` on `P`
sits at a position with `c₀ ≠ β`. If `X ∩ P` meets both colors of `c₀`, then
`P` is never monochromatic. Otherwise the cost of target `β` is
`p^{#(c₀⁻¹(¬β) ∩ P) − t}`, with `t = |X ∩ P|`.

## Results

### Lemma 1 (exact lens on a single-label block)

Take `n_j = r + q^{D−1}(m + je)` for `j < k`, with `0 ≤ r < q^{D−1}`, inside
one full label. Let `e` be the signed step for which the real segment
`s + jλe` (`j < k`) stays in `[−q/2, q/2)`; this is the hypothesis of Lemma A
of the single-label note. It holds when `(k − 1)λ|e| < q/2` and the segment
does not cross `±q/2`. Put `s = qỹ_D(n₀)` and `C = Σ_{i<D} (qỹ_i(r))²`.
Then

```
band(n_j) = ⌊θ + v j⌋ + λ²e²j²,   θ = C + s²,   v = 2sλe,   frac(s) = y_{D−1}(r).
```

*Proof.* Lemma A gives `f(n_j) = C + (s + jλe)²`. The term `λ²e²j²` is an
integer and comes out of the floor. The fractional part of
`q y_D(n) = (λn mod q^D)/q^{D−1}` is `(λn mod q^{D−1})/q^{D−1} = y_{D−1}(r)`.
Centering changes `q y_D` by an integer. ∎

The step has to be read signed. In `ℤ/N` the step `q − e` gives the same
points as `−e`, and the identity read with `q − e` is false; the verifier
checks this.

Consequently, on every single-label block, the whole real part of the band
word is a Beatty sequence `⌊θ + vj⌋`. The key does not see `θ` (through `C`)
nor `frac(v)` (through `y_{D−1}(r)`). Both range over essentially every real
value inside one box.

### Lemma 2 (exact shifted squares)

Let `D ≥ 3`, `0 ≤ u < q/2` and `r = u λ⁻¹ mod q^{D−1}`. Then on every
single-label block of this `r` whose segment satisfies Lemma 1 and lies in
`qỹ_D ≥ 0`:

```
band(n_j) = x_j² + u²,   x_j = ⌊s⌋ + jλe ∈ ℤ.
```

*Proof.* `λr mod q^i = u` for `i ≤ D − 1`, so `qỹ_i(r) = u/q^{i−1}`. Hence
`C = u²(1 + q⁻² + …)` and `frac(s) = u/q^{D−1}`. The remainder
`u²(q⁻² + …) + 2 frac(s) x_j + frac(s)²` lies in `[0, 1)`, because
`u < q/2`, `x_j < q/2` and `D ≥ 3`. ∎

`P1` is the case `u = 0`. For `D = 2` the identity is false (the verifier
finds counterexamples).

### Lemma 3 (blocking the squares)

For an odd prime `ℓ`, let `SQ_ℓ` be the set of squares mod `ℓ`, 0 included.
It has `(ℓ+1)/2` elements. Some `R' ⊂ ℤ/ℓ` with
`|R'| ≤ ⌈log₂ ℓ⌉ + 1` meets every translate `c + SQ_ℓ`.

*Proof.* Take `s = ⌈log₂ ℓ⌉ + 1` and a uniformly random `s`-subset. It
misses `c + SQ_ℓ` with probability
`Π_{i<s} ((ℓ−1)/2 − i)/(ℓ − i) < 2^{−s} ≤ 1/(2ℓ)`. A union bound over the
`ℓ` translates finishes the proof. ∎

### Theorem A (a residue rule meets, without saturating, every block with `ℓ ∤ e`)

Let `ℓ` be an odd prime with `ℓ ∤ λ` (for instance `ℓ > h₀`). Let `R'` be
as in Lemma 3, `R = R' + {−1, 0, 1}`, and `k ≥ (ℓ − 1)² + 1`. Put

```
X_ℓ = {(B, t) : t mod ℓ ∈ R}   (every box B).
```

Then on every single-label block (Lemma 1) with `ℓ ∤ e`, whatever `r`:

1. at least one position has its key in `X_ℓ`;
2. at most `10|R'| k/ℓ + ℓ²` positions have their key in `X_ℓ`.

The key density of `X_ℓ` is `|R|/ℓ ≤ 3(⌈log₂ ℓ⌉ + 1)/ℓ`.

*Proof.* By Dirichlet, there are `1 ≤ β ≤ ℓ − 1` and an integer `a` with
`|βv − a| ≤ 1/ℓ`.

Fix an offset `o < β` and a run of `ℓ` consecutive `i` on which
`J + βi'` stays below `k`, where `J = o + βi₀` and `0 ≤ i' < ℓ`. Put
`θ' = θ + vJ`. Since `|(βv − a)i'| < 1`, we get
`band(n_{J+βi'}) ≡ g(i') + δ_{i'} (mod ℓ)`, with `δ_{i'} ∈ {−1, 0, 1}` and

```
g(i') = ⌊θ'⌋ + λ²e²J² + (a + 2λ²e²Jβ) i' + (λeβ)² i'².
```

Since `ℓ ∤ λeβ`, the leading coefficient is a nonzero square mod `ℓ`.
Completing the square shows that `g` takes on `ℤ/ℓ` exactly the values of a
translate of `SQ_ℓ`, each at most twice.

* For (1), take `o = 0` and `i₀ = 0`. The indices `βi' ≤ (ℓ−1)² < k` are
  admissible, `g` meets `R'`, and that position has its band in `R`.
* For (2), a position of the run with its band in `R` has
  `g(i') ∈ R' + {−2, …, 2}`. That is at most `5|R'|` values, each attained at
  most twice, so at most `10|R'|` positions per run. Cut each offset class
  `{o + βi}` into disjoint runs of length `ℓ`. There are at most `k/ℓ` runs,
  and fewer than `βℓ ≤ ℓ²` indices are left over. ∎

### Corollary A (the `e = 1` family at `b_X → 1/2`)

Take `ℓ` prime in `(√k/4, √k/2]` (Bertrand). Once `k` is large this prime
exceeds `h₀ = D⌈log k⌉²`, because `a < 1/2`. Then `X_ℓ` meets every block of
the `e = 1` family `P3`, and every single-label block with `ℓ ∤ e`. It does
so in at least 1 and at most `40(log₂ k + 2)√k + k/4 < k/2` positions, so at
least `k/4 ≫ k^{1−a}` keys of the (single) color stay outside `X_ℓ`. The key
density is `O(log k/√k)`, which means `b_X = 1/2 − o(1) > a`.

**On the family of Theorem 1 of the single-label note, which forces both
`b < a` and `a + b < 1` on iid flips, a structured rule evades both, with
(I) and its non-saturation clause.** The limit `√k` comes from the Dirichlet
step, not from the family.

**`X_ℓ` is not an admissible `X` by itself.** On the blocks with `ℓ | e` it
is constant (Proposition B below, with `u = 0`, which is `P2`). It either
misses them or contains all their keys. In the second case it freezes them
monochromatic for every flip assignment. The verifier shows both branches.

The first version of this note (`b5a6c38`) claimed all of `P1` through a
patch on exact squares, and was wrong: `R` meets `SQ_ℓ`, so `P1` blocks with
`ℓ | e` and `x₀² mod ℓ ∈ R` are saturated (the referee's counterexample). A
repair would remove the large squares from `X_ℓ` and patch them with a
random hitting set. It would then need Theorem A to find a band that is not
a perfect square, which is not proved. In any case Proposition B with
`u ≥ 1` stands.

The asymptotic choice of `ℓ` needs `h₀ < √k/4`, that is roughly
`(1/2 − a) ln k > 2 ln ln k + ln 4`. For `a = 0.45` this means
`ln k ≳ 249`; for `a = 0.49`, `ln k ≳ 1617`.

*Measured, not proved.* With `k = 2ℓ`, an exhaustive enumeration covers every
real lens: all `θ`, all `v`, all nonzero squares `λ²e²`, and all mechanical
words of length `k`. It finds that every lens covers at least `(ℓ+1)/2`
residues, and that a set `R` of 4, 4 and 5 residues meets every lens for
`ℓ = 13, 17, 19`. Four is minimal for `ℓ = 13`. If "at least `(ℓ+1)/2`
residues per lens" holds for all `ℓ` with `k ≥ 2ℓ`, the counting of Lemma 3
gives `|R| = O(log k)`, hence `b_X → 1` on the `e = 1` family (the
non-saturation would need its own count).

### Proposition B (the shifted family defeats every such rule)

Let `X` be any key set whose band rule in each box depends only on the band
mod `L`, with `L ≤ E_max`, plus any patch on perfect squares. Let
`1 ≤ u ≤ √q/2`. Then the family of Lemma 2 contains a single-label block with
`e = L` on which `X` is constant. Either `X` misses all its keys, so (I)
fails, or `X` contains all of them, so the block is monochromatic for every
flip assignment. With `u = 0` and no patch, this is `P2`.

*Proof.* `x_j ≡ x₀ (mod L)`, so `band(n_j) = x_j² + u² ≡ x₀² + u²`. A number
`x² + u²` with `x ≥ q/8 ≥ u²/2` is never a perfect square: `z² = x² + u²`
with `z > x` would give `u² = (z − x)(z + x) ≥ 2x + 1 > u²`. Good blocks
with `e = L` exist by the argument of Lemma C of the single-label note, as
for `P2`; the verifier exhibits one for `u = 1`, `L = 13`. ∎

On the real instance (`q = 2⁶¹ − 1`, `D = 3`, `k = 145`, `ℓ = 13`), the
verifier exhibits a single-label block with `u = 1` and `e = 13` that misses
`X_13`, and none of its bands is a perfect square.

Unions of residue rules therefore have to cover the `e`-direction, where `e`
runs up to `E_max = q^{1−o(1)}`. Each prime of the union handles only
`ℓ ∤ e` and costs `≈ log k/ℓ`, so the total cost is `≈ log E_max / k`, that
is `k^{−a+o(1)}`, and `b_X ≤ a` again. This is a count, not a theorem.
A general version for residue rules at `r ≠ 0`, CRT unions included, is the
companion contribution `2026-10-20-ChaloupeMusic-algebraic-band-rules`.

### Lemma R (the exact reduction behind (I))

Fix `r` and a maximal interval `J` of `m` on which `r + q^{D−1}m` keeps one
full label. Then (I) on the single-label blocks inside `J` says in
particular that `S_J = {m ∈ J : κ(r + q^{D−1}m) ∈ X}` meets every `k`-AP
contained in `J`: those APs are exactly the blocks.

Call **`P1` region** the boxes whose `D`-th `V` interval lies in
`{1/8 ≤ |Y| ≤ 3/8}`. In `m`, the `U` cells are intervals of length
`qH/λ = q/(k²λ)`. A `V` cell is a union of runs of length
`q|I_D|/λ ≥ q/(32k²λ)`, and each run is cut by at most two `U` boundaries.

Put `Y₀ = ⌊q/(2048 k²λ)⌋`. Pieces shorter than `2Y₀` then hold at most `6Y₀`
points per run, which is less than a tenth of the run. A piece `J` of length
`≥ 2Y₀` splits into blocks of length `Y₀`, and `S_J` meets every `k`-AP of
each block. So in every box of the `P1` region, at least 9/10 of the points
lie in pieces where `X` has density `≥ ρ_AP(Y₀, k)/2`. Here `ρ_AP(Y, k)` is
the least density of a set meeting every `k`-AP contained in `[Y]`, and
`log Y₀ = (1 − o(1)) log q = (c − o(1)) k^{1−a} log k`.

Known constructions give `ρ_AP ≈ log Y/(k log k)`: unions of residue classes
modulo primes up to `k`, or "some base-`k` digit is 0". That is `k^{−a+o(1)}`,
the same exponent as random. So:

* **Porte 1 through a sparse `X` needs a new additive-combinatorics object:**
  sets of density `k^{−1/2−δ}` meeting every `k`-AP of
  `[exp(Θ(k^{1−a} log k))]`, a power of `k` below every known construction.
  On top of that, the pullback has to work for every lens at once.
* A lower bound `ρ_AP(Y, k) ≥ log Y / k^{1+o(1)}` would close this route in
  the `P1` region. The remaining route would then be a dense `X` (density
  `k^{−a}`) that is anti-random on rich progressions: `X ∩ P` must
  essentially never equal the `c₀`-minority of a rich `P`, while a random
  set of that density does so on about `N² k^{−aγk}` progressions, which is
  `≫ 1` as soon as `2c > aγ`.

The analogous families moving in coordinate `i < D` (`d = q^{i−1}e`) carry
the same lens up to a quadratic perturbation below `10⁻⁵`. They are not
checked here.

### On (II)

On the real instance, 2000 uniformly random progressions of `ℤ/N` (generic
rich ones) meet `X_13` with the binomial mean and variance of density `7/13`.
This is the typical behaviour only. The tail, which is what (II) needs,
cannot be tested at this size.

A rule that is random-like on rich progressions gives at best
`c < γ min(b_X, b)/2`. So the `b_X → 1/2` of Corollary A would sit exactly at
`1/8`, even if `X_ℓ` could be completed into an admissible `X`.

## Checks in `verify.py`

1. Lemma 1 on 534 positions (random `q`, `D`, `λ`, `r`, `m`, `e`, Fractions).
   Control: the unsigned step `q − e` breaks it.
2. Lemma 2 on 979 positions (`q` up to `2⁶¹ − 1`, `D = 3, 4`). Control:
   `D = 2` breaks it.
3. Lemma 3: stored `R'` for 10 primes (exhaustive), and the counting
   inequality for the 665 odd primes below 5000. Control: no single residue
   blocks.
4. Theorem A (1) on 1500 random lenses (`ℓ = 13`, `k = 145`), with the
   Dirichlet witness of the proof recomputed. A tight lens (`v = 37/12`,
   `θ = 13/2`) forces the witness index `(ℓ−1)² = 144`, so the hypothesis
   `k ≥ (ℓ−1)² + 1` is exercised. Control: an `ℓ | e` lens misses `R`.
5. Measured table, `k = 2ℓ`, exhaustive over all real lenses, for
   `ℓ ∈ {13, 17, 19}`. Control: no 3-element set works for `ℓ = 13`.
6. The real construction (`q = 2⁶¹ − 1`, `D = 3`, `λ = 840`, `k = 145`, the
   source's `U` mesh and adaptive `V` mesh with 200-digit decimals):
   * 30 `P3` blocks meet `X_13` and are not saturated (at most 88 keys of 145
     in `X_13`);
   * 15 `P1` blocks with `13 ∤ e` meet `X_13` and are not saturated;
   * saturation control, Proposition B with `u = 0`: `P1` blocks with
     `13 | e` are either missed (6) or have all 145 keys in `X_13` (3), never
     in between;
   * the killer block of Proposition B (`u = 1`, `e = 13`) misses `X_13` and
     has no perfect-square band.
7. Typical rich behaviour (2000 progressions), as above.

### What the toy instance is

The lemmas use exactly these properties of `λ`:

* `gcd(λ, q) = 1`;
* `ℓ ∤ λ` (Theorem A);
* `λL ≤ q/(400k³)`, so that blocks with `e = L` exist (Lemma C, `P2`,
  Proposition B);
* the segment conditions of Lemma 1.

The toy takes `λ = 840`, chosen coprime to `13`. It is not the dilation of
the source. For `k = 145` and `D = 3` that dilation is divisible by every
prime up to `h₀`, 13 included, and exceeds `q`, so `ℓ = 13` would be
inapplicable there. The toy illustrates the lemmas in the right regime of
fibers (`q = 2⁶¹ − 1`); it is not an instance of the source's parameters.
The proofs are the text above.

## What is not claimed

* No admissible `X` passing (I), with non-saturation, on all of case (ii) is
  known, at any density below random.
* `X_ℓ` alone is not admissible: it saturates some `P1` blocks with `ℓ | e`.
* No lower bound on `ρ_AP` is proved. "No construction known" is not an
  impossibility theorem.
* The measured `k = 2ℓ` table is a finite enumeration for three primes, not a
  proof for general `ℓ`.
* Nothing is claimed about (II) beyond typical behaviour, and the implication
  (I) + (II) ⇒ `c < 1/4` is the team's reduction, not proved here.
* Nothing changes for the current results: `1/9` and every `c < 1/8` stand as
  they are.
