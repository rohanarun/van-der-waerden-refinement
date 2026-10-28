# Finite-field colorings: what the Galois-field certificate reaches in the key-measurable class

**Status:** structural research, with proofs and exact finite checks. Mixed
result. Sprint 5 asked (piste T5) whether the deterministic colorings of
Berlekamp (1968) and of Blankenship, Cummings and Taranchuk (2018) can supply
Door 1's open object: a good member of the class of key-measurable colorings
`𝒞(c₀) = {c₀∘L ⊕ 1_Y∘κ}` (Theorem 1 of `key-measurable-colorings`, PR #22)
at `N = k^{(1/8+ε)k}`, of any density.

* **Negative.** As colorings certified by Berlekamp's argument, both live on
  `N^{o(1)}` integers (Theorem 1).
  Their periodic lift, their position lifts and their blow-ups fall under
  published closures. A band rule that reads the band modulo `P` is closed by
  PR #16 up to modulus `≈ q/(1536k³)`. Above that, Berlekamp's certificate
  covers no slow block with `P > 2λ²e² + 1`.
* **Positive.** Read on the **square root** of the band, Berlekamp's coloring
  is a key-measurable rule that meets and does not saturate every aligned
  single-label block (Proposition R). Those blocks include all of the `P1`
  family and the shifted squares `x² + u²` with `u² < 2x + 1`, which defeat
  every residue rule of PR #16.
* **Limits.** Every rule that reads only (box, `⌊√band⌋`), this one
  included, takes one value on the band words of the "vertex" blocks of the
  shifted family (Proposition V). Those words are the bands of actual blocks,
  which are then monochromatic, only if the blocks are single-label
  (hypothesis (G), not proved here). The certificate says nothing on unaligned fibres,
  on slow words that are not single-label, or on rich progressions. On those
  `c₀` is not constant, so a non-constant `Y`-word protects nothing
  (Proposition 3 of `key-measurable-colorings`).

No good member of `𝒞` is produced, no closure of what remains is claimed,
and there is no bound on `c`.

**Base commit:** `061401f` (`research/door-one-continued`, PR #22).

**Sources:** see `NOTICE.md`. The statements below were read in the
published texts on 27/10/2026 (both PDFs rendered page by page). Kim's three
statements used here were checked in his full text by the referee (radar-cc);
this note read only his abstract.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-finite-field-colorings/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. Standard library only, a few seconds. The
sections "1. The sources", "3. The certificate", "4. Theorem 1",
"5. Carrying it to N", "6. Answers" and "What is not claimed" are frozen by
hash in `verify.py` (check 0), together with the preamble (title and
status) and "2. Setting and translation". The hash table lives in
`verify.py` itself, so an edit of both files plus a new `MANIFEST.json`
passes: the real anchor is the tree hash recorded by the referee.

## 1. The sources

**Berlekamp**, *A construction for partitions which avoid long arithmetic
progressions*, Canad. Math. Bull. 11 (1968) 409–414,
DOI 10.4153/CMB-1968-047-7. In his notation `W(k, t)` is the least `m` such
that every partition of `m` consecutive integers into `k` sets has a set
containing a `(t+1)`-term progression.

* **Theorem 1.** Let `k` be a prime power and `W̌` an integer such that
  (4) `W̌ ≤ t(k^t − 1)/(k^d − 1)` for every proper divisor `d` of `t`, and
  (5) `W̌ ≤ t(k^t − 1)/D` for every divisor `D < t` of `k^t − 1`. Then
  `W(k, t) > W̌`.
* **Theorem 2.** If `t` is prime, `W(2, t) > t·2^t`.
* **Construction.** `α` primitive in `GF(k^t)`, `β_1, …, β_t` a basis over
  `GF(k)`, `α^j = Σ_i A_{i,j} β_i`; the class of `j ∈ [0, W̌)` is
  `A_{1,j} ∈ GF(k)`. For Theorem 2 the basis is
  `1, 1+α, …, 1+α^{(t−1)/2}, 1+α^{−1}, …, 1+α^{−(t−1)/2}`, and
  `(t−1)/2` points are added at each end of `[0, t(2^t − 1))`.
* **Proof.** A progression `a, a+b, …, a+tb` in one class has `b` bounded by
  (9) `b < (k^t − 1)/(k^d − 1)` and (10) `b < (k^t − 1)/D`. Case `ξ ≠ 0`:
  the minimal polynomial `f^{(b)}` of `α^b` gives
  `Σ_n f^{(b)}_n A_{1,a+bn} = 0`, so `f^{(b)}(1) = 0`, so `α^b = 1`, against
  (10). Case `ξ = 0`: `t` distinct elements (distinct by (10)) of the
  `(t−1)`-dimensional `T_0` are dependent, so `α^b` lies in some `GF(k^d)`,
  `d` a proper divisor of `t`, against (9). The case `ξ ≠ 0` needs only
  `α^b ≠ 1`; the "proper subfield" condition serves only the case `ξ = 0`.
* Page 410 also recalls Folkman's partition for `W(2, 3) > 34` by quadratic
  non-residues modulo 11, and similar quadratic-residue constructions. Those
  are not of the form treated here.

**Blankenship, Cummings, Taranchuk**, *A new lower bound for van der Waerden
numbers*, Europ. J. Combin. 69 (2018) 163–168, DOI 10.1016/j.ejc.2017.10.007,
arXiv:1705.09673 (v3, 25 Oct 2017). Here `p` is the largest prime `≤ k`.

* **Definition 2.1.** `S_i(r, k) = (i, i+1, …, r, 1, 2, …)`, a `p`-tuple of
  colors.
* **Lemma 2.1.** One can choose `r − ⌈r/p⌉` of the `S_i` such that every
  concatenation of them has all its monochromatic `k`-APs of step divisible
  by `p`.
* **Theorem 2.1.** `w(r, k) > p·(w(r − ⌈r/p⌉, k) − 1)` for `r ≥ 2`.
* **Theorem 2.2.** For `p` prime and `2 ≤ r ≤ p ≤ k`,
  `w(r, p+1) > p^{r−1} 2^p`. Its base case is Berlekamp's Theorem 2.

Two corrections to the brief. The extension to prime powers is Berlekamp's
own Theorem 1 (`k` colors from `GF(k)`), not BCT's. BCT's extension is to `r`
colors, by a blow-up: `n = pi + j` gets the color `S_{c(i)}[j]`. For `r = 2`
it keeps `r − ⌈r/p⌉ = 1` outer color, so its 2-color content is Berlekamp's.

**Kim**, *Polychromatic blocks and explicit lower bounds for multicolour van
der Waerden numbers*, arXiv:2610.32000 (22 Oct 2026). Checked in the full text by the referee
(radar-cc): an `h`-coloring of `ℤ_q` is `k`-polychromatic if every `k`-AP of
`ℤ_q` with `d ≠ 0`, zero divisors included, meets all `h` colors (§ 2); such
a coloring gives `W(r, k) > q(W(r − ⌈r/h⌉, k) − 1)` (Corollary 2.2); and
such `q` is at most `(W(2, k) − 1)/(k − 1)` (Proposition 6.1). This note does not use blow-ups. It only places
Berlekamp in Kim's language (check 3).

## 2. Setting and translation

As in `key-measurable-colorings`: labels `L`, keys `κ(n) = (V-box, band)`,
an admissible outer coloring `c₀`, and the class `𝒞(c₀)`. A member is good
if no `k`-AP of `ℤ/N` is monochromatic. By its Proposition 3, `P` is
monochromatic in `β` iff `Y_P = {c₀ ≠ β} ∩ P`. On a slow single-label block
`c₀` is constant, so the block is monochromatic exactly when `Y` contains all
or none of its keys. Proper means meeting **and** not saturating. The band
word of such a block is `⌊C + (s + jλe)²⌋`, with `C`, `frac(s)` fixed by the
fibre `r` (Lemma 1 of `single-label-lenses`, PR #16). The key does not see
`C`. For `r = 0` (`P1`) `C = 0`. For `r = u λ⁻¹`, `D ≥ 3`, the band is
exactly `x_j² + u²` (its Lemma 2).

`K` is a prime power, `M ≥ 2`, `F = GF(K^M)`, `α` is primitive,
`P = K^M − 1`, `φ : F → GF(K)` is a nonzero linear form, and the
**Berlekamp coloring** is `χ(n) = φ(α^n)`. A **geometric run** of length `m`
is `γ, γβ, …, γβ^{m−1}` with `γ ≠ 0`. The index progression `a + jb` is sent
by `n ↦ α^n` to the geometric run of ratio `α^b`.

| Template | Berlekamp | BCT (`r` colors) |
|---|---|---|
| key `κ(n)` | the exponent class `n mod P`, that is `α^n ∈ F*` | the digit `n mod p` |
| label `L(n)`, outer `c₀` | none (`c₀` constant) | `⌊n/p⌋`, a valid `(r − ⌈r/p⌉)`-coloring |
| combination | `1_Y(κ)`, `Y = {φ = 1}` | color shift `S_{c₀}[κ]`, not an XOR |
| bands | none: the field sees the exponent, linearly | none |
| slow words | steps with `α^b = 1` (excluded by (10)) or in a proper subfield (excluded by (9)) | steps divisible by `p` (sent to the outer coloring) |

## 3. The certificate

**Lemma L.** Let `β ≠ 1` have degree `d` over `GF(K)`, and let `A ⊊ F` be an
affine subspace of dimension `w`.

1. If `0 ∉ A`, then `A` holds no geometric run of ratio `β` longer than
   `min(d, w + 1)`.
2. If `0 ∈ A` and `d > w`, then `A` holds none longer than `w`.

*Proof.* (2) `w + 1` terms in a space of dimension `w` are dependent, so
`g(β) = 0` for a nonzero `g` of degree `≤ w < d`. (1) `A` lies in an affine
hyperplane `{φ' = ξ}`, `ξ ≠ 0`. A run of `d + 1` terms gives, through the
minimal polynomial `f` of `β`, `Σ_j f_j γβ^{i+j} = 0`, and `φ'` gives
`ξ f(1) = 0`, so `x − 1` divides the irreducible `f`, and `β = 1`. A run of
`w + 2` terms lies in the span of `A`, of dimension `w + 1`, so `d ≤ w + 1`,
and then the bound `d` applies. ∎

Berlekamp's two cases are `w = M − 1`. The class `ξ ≠ 0` holds no run of
`M + 1` terms as soon as `β ≠ 1`. The class `0` holds none of `M` terms when
`d = M`. Check 4 tests random affine subspaces of `GF(16)`, `GF(32)`,
`GF(64)` and `GF(27)`, with every `γ` and every `β ≠ 1`. The bound is
reached in almost every case. Control: a subfield ratio inside a linear
subspace.

**Corollary L1 (certificates of the form of Lemma L).** Call `T ⊆ F*`
L-certified for `k` when `F* ∖ T` lies in one proper affine subspace that,
by Lemma L, holds no run of length `k` of any ratio `β ≠ 1` of degree `M`
(for `M` prime, the ratios `α^b` of every step `b ≢ 0 mod P`). Then `T` has
density at least
`1 − K^{M−1}/(K^M − 1)`. For `K = 2` that is `(2^{M−1} − 1)/(2^M − 1)`,
just below `1/2` (`3/7`, `15/31`, `63/127`). If both classes of a 2-coloring
of `F*` are L-certified, `F*` is covered by two proper affine subspaces.
This forces `K = 2` and, for `M ≥ 3`, a linear hyperplane and its
complement: Berlekamp's coloring. This classifies certificates of this one
form. It does not classify the finite-field method as a whole (Folkman's
quadratic residues, for instance, are of another form).

*Proof.* A proper affine subspace has at most `K^{M−1}` points. For
`K ≥ 3`, `2K^{M−1} < K^M − 1`. For `K = 2`, the two sizes add up to at least
`2^M − 1` and each is a power of 2 at most `2^{M−1}`, so for `M ≥ 3` both
are `2^{M−1}`: both are hyperplanes. They then meet in at
most one point, while two distinct affine hyperplanes meet in `0` or
`2^{M−2} ≥ 2` points. ∎
(Check 5, exhaustive on `GF(8)`, `GF(16)`, `GF(9)`, `GF(27)`: exactly
`2^M − 1` covering pairs for `K = 2`, all of that shape, and none for
`K = 3`.)

## 4. Theorem 1 (the scale)

**Theorem 1.** For every `K`, `M ≥ 2`, primitive `α` and nonzero `φ`, every
nonzero `M`-tuple occurs exactly once per period in `(χ(n))_n`, and `χ` has
period `P`. Hence, if `χ` has no monochromatic `k`-AP on an interval of
length `N`:

1. `N ≤ (k − 1)P`, since the `k`-AP of step `P` is constant;
2. if the interval contains a full period and `k − 1` more points, then
   `M ≤ k − 1`, since each `ξ ≠ 0` has a run of `M` consecutive values.

The step-1 words have ratio `α`, of degree `M`, and Lemma L certifies a
`k`-term word of ratio `β` in the class `ξ ≠ 0` as soon as `k ≥ deg β + 1`.
For ratios of smaller degree that happens for smaller `k`, but the step-1
words need `k ≥ M + 1`. So every coloring whose step-1 words are certified
has `M ≤ k − 1`, and by point 1 it lives on `N ≤ (k − 1)(K^{k−1} − 1)`
integers.

*Proof.* `x ↦ (φ(x), φ(xα), …, φ(xα^{M−1}))` is `GF(K)`-linear. Its kernel
is `{0}`: if `x ≠ 0` were in it, `φ` would vanish on
`x·span(1, …, α^{M−1}) = F`. So it is a bijection onto `GF(K)^M`, and the
window at `n` is the image of `α^n`, which runs over `F*` once per period.
The tuple `(ξ, …, ξ)` is a monochromatic `M`-AP of step `1`. ∎
(Check 2: every field `2^2` to `2^10`, `3^2` to `3^5`, `5^2`, `5^3`.
Check 1 replays Berlekamp's own table and set `S_1` for `t = 3`, word for
word, and his Theorem 2 for `t = 3, 5, 7`: no monochromatic `(t+1)`-AP on
`t·2^t = 24, 160, 896` integers. Control: the `t = 3` coloring has a
monochromatic 3-AP.)

**Scale.** BCT's colorings have length `p^{r−1}2^p ≤ k^{r−1}2^k`
(Theorem 2.2, `p ≤ k`). For `r = 2` this covers Berlekamp's `p·2^p`. The
template needs `ln N = c k ln k ⌊log₂ r⌋`. With `c = 1/8`, the length is
below `N` for every `k ≥ 299` when `r = 2`, `k ≥ 338` when `r = 3`, and
`k ≥ 573` for every `r ≤ k` (check 8). For fixed `r` the ratio of the logs
decreases in `k`. For `r ≥ 512` it is below `8/j + 8/j² < 1`,
`j = ⌊log₂ r⌋`. Both constructions live at the exponential scale, and the
template at the superexponential one.

## 5. Carrying it to N

**(a) Periodic lift.** `n ↦ χ(n mod P)` on `[0, N)`, or on `ℤ/N` when
`P | N` (otherwise there is a seam at `N`). The progression of step `P` is
constant (Theorem 1), and it is not degenerate since `N ≥ kP`.

**(b) Position rules** `X = {n : F(n mod P) = 1}`, alone or XORed with
`c₀∘L`. Theorem 2 of `digit-transversals-saturate` (PR #22) applies whenever
the modulus is below `(E + 1)^D = N^{1−o(1)}`, since `n` is a linear form of
the base-`q` digits. It applies to every certified `χ`, because
`P < K^{k−1} = N^{o(1)}`. It also applies to `M ≥ k`, which still gives only
`P ≈ K^M`. Escaping it needs `M ≥ (1 − o(1)) log_K N`, as radar-d9 points
out, and then Lemma L certifies no `k`-term word.

**(c) Blow-ups** (BCT, Kim). For `M` prime, `χ` on `ℤ/P` is a 2-colored
block in which every non-degenerate `(M+1)`-AP is bichromatic. Check 3
covers `P = 7, 31, 127` and the composite `P = 2047 = 23·89`, exhaustively
along each cycle of `n ↦ n + b`; the longest run is exactly `M`. Control: a
random coloring of `ℤ/127` has a run of 16. So `χ` is a polychromatic block in
Kim's sense (the referee checked his § 2 definition against `χ`, `P = 2047`
included). His Proposition 6.1 then bounds such a block by
`q ≤ (W(2, k) − 1)/(k − 1)`. For two colors no outer
color is left.

**(d) Band rules read modulo `P`**, `Y = {(V, t) : ψ_V(t mod P) = 1}`.

* If `P ≲ q/(1536k³)`: closed by `algebraic-band-rules` (PR #16, every truth
  table, total modulus up to `q^{1−o(1)}`).
* **Lemma S (slow blocks).** The word `b_j = ⌊θ + vj⌋ + Lj²` is arithmetic
  modulo `P` on `k ≥ 3` terms only if `P | 2L + ε` for some
  `ε ∈ {−1, 0, 1}`. So when `P > 2λ²e² + 1`, Lemma L certifies no slow block
  of step `e`.
  *Proof.* `Δ²b_j = 2L + Δ²⌊θ + vj⌋`, and a Beatty sequence has second
  differences in `{−1, 0, 1}`. ∎ (Check 6.)

**(e) Band rules read on the square root,**
`Y_√ = {(V, t) : φ(α^{⌊√t⌋}) = 1}`. This rule is key-measurable and not
periodic. PR #16 lists rules in `√(t − C₀)` outside its class.

**Lemma R (aligned blocks).** Let `x_j = s + jμ` with `s ≥ 0` real, `μ ≥ 1`
an integer, `f = frac(s)`, and `C ≥ 0` real with
`C < (1 − f)(2⌊s⌋ + 1 + f)`. Then `⌊√⌊C + x_j²⌋⌋ = ⌊s⌋ + jμ` for every
`j ≥ 0`.

*Proof.* `m_j = ⌊x_j⌋ = ⌊s⌋ + jμ` and `m_j² ≤ ⌊C + x_j²⌋`. Also
`C + x_j² < (m_j + 1)²` iff `C < (1 − f)(2m_j + 1 + f)`, which increases with
`m_j`. ∎ (Check 9: 16 000 aligned blocks; among 4 000 unaligned ones, 3 447
give a word that is not arithmetic.)

**The negative side.** Since the band reads `x_j²`, Lemma R applies to
`|x_j|`. A block with every `x_j < 0` is, read backwards, the progression
`|x_{k−1}|, |x_{k−2}|, …` of step `μ`. So the condition is Lemma R's with
`s` replaced by `t = |x_{k−1}| = min_j |x_j|`, whose fractional part is
`1 − frac(s)` when `s ∉ ℤ`, not `frac(s)`. Example: `s = −10.9`, step
`−60`, `C = 10`. Read with `frac(s) = 0.1` the condition would be
`10 < 18.99`, but the true one, for `t = 10.9`, is `10 < 2.19`, which fails.
The word is `11, 70, 130, 190`, not arithmetic (check 9).

**Proposition R.** Let `M` be prime, `P = 2^M − 1 > λ E_max`, and
`M ≤ ⌈k/2⌉ − 1`. Then `Y_√` meets and does not saturate:

* every single-label block of the `P1` family (`r = 0`, every step
  `e ≤ E_max`, blocks crossing `0` included);
* every single-label block on one side of `0` whose `|x_j|` satisfy Lemma R
  (with `t = min_j |x_j|` and its own fractional part on the negative side).
  This includes the shifted squares `x_j² + u²` with `u² < 2 min|x_j| + 1`,
  and the blocks with `ℓ | e`.

On these blocks `c₁` is not monochromatic.

*Proof.* By Lemma R (with `C = 0` on `P1`, where `⌊√(x²)⌋ = ⌊|x|⌋`), the
exponent word is arithmetic of step `±λe` on each side of `0`. One side has
at least `⌈k/2⌉ ≥ M + 1` terms. `α^{λe} ≠ 1` since `0 < λe < P`, and it has
degree `M` since `M` is prime. By Lemma L neither class holds that side, so
the `Y`-word is not constant, and `c₀` is constant on the block. ∎
For one-sided blocks `M ≤ k − 1` suffices. The window
`log₂(λE_max) < M ≤ ⌈k/2⌉ − 1` needs `log₂(λE_max) < k/2 − 1`. Since
`λE_max ≤ q` and `ln q ≈ c k^{1−a} ln k`, that is about
`k^a > (2c/ln 2) ln k`, i.e. `k^a > 0.36 ln k` at `c = 1/8`. By Bertrand
it contains a prime as soon as `⌈k/2⌉ − 1 ≥ 2 log₂(λE_max)`, about
`k^a > 0.72 ln k`. (Check 9: 39 184 `P1` blocks, `M = 5, 7`,
`k = 2M + 2`, none constant. Control: `P | μ` gives a constant word.)

**Reported from the toy banc (radar-dd, `banc/decale.py`, read by radar-d9;
not replayed by this note or its verifier).** `decale.py` does not use the
T0 toys: it enumerates the band words of Lemma 2 directly,
`t_j = (s + jg)² + u²` for all `s ∈ [0, q)`, `g ∈ [1, q)`, with no
single-label or admissibility filter. It reports, for `q = 113`,
0 monochromatic blocks at `u = 0`, 23 at `u = 10` and 94 at `u = 56`,
against a median of 98 for random sets. For `q = 1009` it reports 557 to
616, against 500 for pure chance and 544 to 552 for a random table read on
`⌊√b⌋`: as reported, the rule does worse there than both. Within
the statements of this note, the finite field gives a handle on the aligned
family only.

**Proposition V (vertex blocks).** Let `Λ ≥ 1`, `b ≥ 1`,
`a ≥ (2b + 1)kΛ`, `u = a² − b²` and `x_j = 2ab + jΛ`. Then
`⌊√(x_j² + u²)⌋ = a² + b²` for every `j < k`. So every rule that reads only
(box, `⌊√band⌋`) takes one value on these band words. They are the bands
of the block of Lemma 2 with this `u`, `Λ = λe` and `⌊s⌋ = 2ab` **only if**
that block is single-label (hypothesis (G)), and then the block is
monochromatic under `c₁` for every such rule.

*Proof.* `x_j² + u² ≥ (2ab)² + u² = (a² + b²)²`. Also
`x_{k−1}² − (2ab)² = 4ab(k−1)Λ + ((k−1)Λ)² < 2(a² + b²) + 1` when
`a ≥ (2b + 1)kΛ`. ∎ (Check 10: 3 000 instances. Control: `a` below the
threshold moves the word.)

Lemma 2 needs `u < q/2`, so `a < √(q/2)`, and then `x ≤ q/(2kΛ)`. The blocks
lie within `q/(2kλ)` of the vertex in the top coordinate, a window of about
`k/2` label cells. (G) asks that one of them avoid every label boundary.
That is not proved here, because the label mesh near the vertex is not
recalled in this tree. Under (G), the field gives a real handle on the
aligned blocks (Proposition R) and no rule of the form (box, `⌊√band⌋`) is
good.

**What the certificate does not reach.**

* Unaligned fibres, `C ≥ (1 − f)(2x_min + 1 + f)`, which are most of them,
  since `C` is of order `q²` for a generic `r`. There the word
  `⌊√⌊C + x_j²⌋⌋` is not arithmetic in general (check 9).
* Slow words that are not single-label (case (ii) with several labels, and
  case (i)), and the rich progressions. On those `c₀` is not constant. By
  Proposition 3 of `key-measurable-colorings`, `P` is monochromatic iff
  `Y_P` is a `c₀`-class of `P`, and Lemma L, which only says that the
  `Y`-word is not constant, controls nothing there.

The open question left by this note is whether some function `g` of
(box, band) makes the exponent word `g(band_j)` arithmetic on every
single-label block, aligned or not, and what replaces Lemma L where `c₀`
varies.

## 6. Answers

* **(A) Existence.** Berlekamp and BCT do not supply a good member of
  `𝒞(c₀)`. As colorings certified by Berlekamp's argument they live on `N^{o(1)}`
  integers (Theorem 1); an uncertified one of period `P ≥ N` is case 5(b). And
  their lifts (a), (b), (c) and the band rules modulo `P` fall under PR #16
  and PR #22 or are not certified (Lemma S). The square-root rule (e) is a
  genuine ingredient. It properly colors the aligned single-label blocks,
  including the families that defeat every residue rule of PR #16. It does
  not give a good member: under (G) it is constant on vertex blocks, and it
  says nothing on unaligned fibres, on multi-label slow words or on rich
  progressions. Within what this note proves, the finite field gives a handle
  on the aligned family only. The banc figures of radar-dd and radar-d9 point
  the same way but are reported, not replayed.
* **(B) Sparse transversals** (radar-d9). Nothing: an L-certified hitting
  set has density at least `1 − K^{M−1}/(K^M − 1)` (Corollary L1). The
  generalised Korsky question (Brown–Freedman `f(M, k)`, arXiv:2606.01780)
  is untouched.

## What is not claimed

* No good member of `𝒞`, no closure of the band rules of modulus above
  `q/(1536k³)` beyond Lemma S, and no bound on `c`.
* Hypothesis (G) of Proposition V is not proved. Without it, Proposition V
  is only arithmetic.
* Corollary L1 classifies certificates of the form of Lemma L only.
* Kim's three statements (§ 2, Corollary 2.2, Proposition 6.1 of
  arXiv:2610.32000) were checked in the full text by the referee, not by this
  note.
* Check 7 is evidence, not a theorem. On quadratic exponent windows
  `(x₀ + jμ)²` the Berlekamp coloring is monochromatic about as often as
  chance, up to 2.35 times (`P = 31`: 42 of 930 against 29 expected;
  `P = 127`: 294 of 16 002 against 125; `P = 8191`, 300 000 samples: about
  37 expected). On linear windows it never is.
* Measured by this session with radar-dd's banc (`banc/banc.py`, logs kept
  outside the package), not replayed by `verify.py`: on the T0 toy
  `11,2,7,12,1000,0.001` (the only one of tour 0 where some `X` exists), the
  band rule modulo `P = 63` violates 3 of 160
  slow and 103 of 7 100 rich lines, and the square-root rule (`M = 5`)
  violates 4 and 112, like the empty set (3 and 106); a random set of density
  `1/2` on the same instance violates 11 and 254. The toys have `D = 2`,
  where Lemma 2 is false, and sit below `q/(1536k³) = 1`, so they test none
  of the statements above.
* Attributions to PR #20 and PR #22 follow the index lines of `ACQUIS.md`.
  The dense-rule closure falls under the exact (II′) by
  `exact-door-one-condition` (PR #20), and the random second moment of every
  rule is Lemma B2 of `keyed-local-lemma-and-large-moduli` (PR #20).

## Checks in `verify.py`

0. Frozen sections: sha256 of the preamble and the seven sections named
   under "Reproduce".
1. Berlekamp's example (`t = 3`, `x³ + x + 1`, basis `1, α³, α²`): table
   and `S_1` equal to the paper's; Theorem 2 for `t = 3, 5, 7`. Control.
2. Theorem 1 on 15 fields.
3. Cyclic blocks for `M = 3, 5, 7, 11` (composite `P = 2047`). Control.
4. Lemma L by degree on random affine subspaces of `GF(16)`, `GF(32)`,
   `GF(64)`, `GF(27)`. Control: subfield ratio.
5. Corollary L1: every covering pair of affine subspaces, counted.
6. Lemma S on 20 000 random lenses.
7. Evidence: quadratic against linear exponent windows.
8. Scale thresholds for every `r`, and the analytic tail.
9. Lemma R on 20 000 blocks and 5 000 negative-side blocks, with the
   negative-side example; Proposition R on 39 184 `P1` blocks. Control.
10. Proposition V on 3 000 instances. Control.
11. Figures: every number this README quotes from the checks is read back
    in the text (a stale figure fails).
12. Provenance: `MANIFEST.json` hashes; summary equal to `RESULT.json`.
