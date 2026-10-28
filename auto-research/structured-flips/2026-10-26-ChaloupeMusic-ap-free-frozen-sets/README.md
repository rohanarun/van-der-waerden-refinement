# AP-free frozen key sets cannot carry door 1

**Status:** negative result (structural research note), with proofs and exact
finite checks. No new bound is claimed. What is closed, for `k` large, is
the **index-side** AP-sparse route to door 1: no `X` satisfying (I) can keep
the index set `I_X(P)` free of 3-term progressions on every rich `P`. That is
the reading in which Behrend, Salem–Spencer or Elkin sets would give (II).
Also closed: every band rule that forbids the quadratic band triple (Q),
which is not a 3-AP of `ℤ`. **Band-side** 3-AP-free sets (a Behrend set in
the band coordinate of each box) are closed only under Proposition 4, which
assumes flatness of the fibre weights and is conditional. For index-side
forbidden lengths `4 ≤ ℓ < p₀(k) = O(log k / log log k)` the note reduces
the route to an off-diagonal van der Waerden bound that is open, and shows
that every known construction fails it. Longer forbidden lengths cannot give
(II).

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, on top of the
local branch `pr/exits-past-1-8` (`83b872a`).

**Depends on:** `structured-flips/2026-10-20-ChaloupeMusic-single-label-lenses`
(Lemma 1, the exact lens, and Lemma R, the scale `Y₀` of single-label fibre
pieces). It uses the template's sharpened dichotomy
(`sharpened-region-proof.md`, `short-period-runs-proof.md`) as is.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-26-ChaloupeMusic-ap-free-frozen-sets/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and a JSON
summary equal to `RESULT.json`. It takes about 10 seconds and uses only the
standard library.

## The question

Door 1 freezes a key set `X` (`c₁ = c₀ ⊕ 1_X`, iid flips of rate `k^{−b}` on
the other keys) and asks for:

* **(I)** every case (ii) progression has a key of `X` at a position of its
  dominant color, without saturating it;
* **(II)** every rich progression `P` has at most `εk` keys in `X`. Beating
  `1/8` needs `ε < 1/4`, since the rich side then gives `c < (1/2 − ε)b/2`
  with `b < 1`.

For a progression `P = (n₀ + jd)_{j<k}` write
`I_X(P) = {j < k : κ(n_j) ∈ X}`. A random `X` of density `log q/k` gives (I)
and fails (II) in its tail. The idea examined here is a deterministic `X`
whose additive structure makes (II) automatic, as for Behrend-type sets.

Two readings of "AP-free" have to be separated:

* **index side, (II_ℓ):** for every rich `P`, `I_X(P)` contains no `ℓ`-term
  progression. Then `|X ∩ P| ≤ r_ℓ(k)` and (II) holds with
  `ε = r_ℓ(k)/k`. This is the only AP-type condition that bounds
  `|X ∩ P|`;
* **band side:** in each box `B`, the band set `X_B = {t : (B, t) ∈ X}` has
  no `ℓ`-term progression in `ℤ`. The bands of a rich progression are
  quadratic in `j` and spread over many boxes, so this says nothing about
  `|X ∩ P|`. It can only fail or pass (I), which Proposition 4 quantifies.

Only the hitting half of (I) is used below. Non-saturation is not needed, so
every statement also holds for the weaker condition.

## Setting

These are the source's notations, also used by the team's template:
`N = q^D`, `x_i(n) = n/q^i`, `y_i = λx_i`, the meshes `U` and `V`, labels
`L(n)` and keys `κ(n) = (V-box, ⌊‖qỹ(n)‖²⌋)`. The note uses four properties:

* (S1) **dichotomy**: a progression that is not rich (case (i)) has
  `ỹ(n_j) = A + jw` with `|w_i| < 1/(k−1)` for every `i`. This is the
  sharpened dichotomy of the template (`sharpened-region-proof.md`, "The
  new dichotomy constant", restated in `short-period-runs-proof.md`, "The
  shape of a non-rich progression", where `k|w_i| ≤ 4MH/h < 1/2`). The
  template does not require the path `A + jw` to stay in the
  representative cube. The source's dichotomy (Section 5) is the
  case `a = 1/10`;
* (S2) every prime factor of `λ` is at most `h₀`. This is true of the
  primorial-type dilation of Section 2. Also `h₀ < (k−1)/2`, and
  `q` is a power of a prime `P > k`;
* (S3) `ln q < θ((k−1)/(ℓ−1)) − θ(h₀)`, where `θ` is Chebyshev's function.
  Then the primes in `(h₀, (k−1)/(ℓ−1)]` have product larger than `q`;
* (S4) a **fibre piece** is an interval `J` of `m` (no wraparound in `ℤ/q`)
  on which `r + q^{D−1}m` keeps one full label, with `r` fixed. Lemma R of
  the lens note gives pieces of length `≥ 2Y₀`, `Y₀ = ⌊q/(2048k²λ)⌋`,
  carrying at least 9/10 of the points of every box of its `P1` region.

Every `k`-AP `m + iδ` (`i < k`) contained in a fibre piece is a case (ii)
block: one full label makes it affine (source, *Affinity inside a small box*) and gives it one
outer color. So the hitting half of (I) says that

```
S_J = {m ∈ J : κ(r + q^{D−1} m) ∈ X}   meets every k-AP contained in J.     (H)
```

In particular `|S_J| ≥ ⌊|J|/k⌋` (disjoint windows of step 1).

## Results

### Lemma E (embedding a fibre pattern into a rich progression)

Assume (S1)–(S3). Let `J` be a fibre piece of `r`, and let `m + iδ ∈ S_J`
for `0 ≤ i < ℓ`, with `δ ≥ 1` and `ℓ ≥ 3`. Then there are a prime
`h ∈ (h₀, (k−1)/(ℓ−1)]` and a **rich** progression `P` such that

```
{0, h, 2h, …, (ℓ−1)h} ⊂ I_X(P).
```

*Proof.* Since `δ < q`, (S3) gives a prime `h` in the range that does not
divide `δ`. By (S2), `h ∤ λδ` and `h ≠ P`. Put `e ≡ δh^{−1} (mod q)`,
`d = q^{D−1}e`, `n₀ = r + q^{D−1}m`, and `P = (n₀ + jd)_{j<k}`. Then
`n_{ih} = r + q^{D−1}(m + ihe) = r + q^{D−1}(m + iδ)` in `ℤ/N`, since
`he ≡ δ (mod q)`. The positions `0, h, …, (ℓ−1)h < k` therefore carry the
`ℓ` given keys of `X`.

`P` is not affine. Its `D`-th coordinate moves by `y_D(d) = λe/q (mod 1)`.
Write `w` for the centred residue of `λe` mod `q`. It is `(λδ + tq)/h`
reduced, where `t ∈ {1, …, h−1}` is the unique residue with
`h | λδ + tq` (`t = 0` would mean `h | λδ`). Hence
`|w| ≥ (q − λδ)/h`. The `ℓ` points lie in one `V` cell of width at most
`2H`, so `λδ ≤ 2Hq < q/2`. Since `ℓ ≥ 3`, `h ≤ (k−1)/2`, and so
`|w| ≥ q/(2h) ≥ q/(k−1)`. If `P` were not rich, (S1) would give
`ỹ(n_j) = A + jw'` with `|w'_D| < 1/(k−1)`. But `w'_D ≡ y_D(d) = λe/q
(mod 1)`, so `|w'_D| ≥ |w|/q ≥ 1/(k−1)`. Hence `P` is rich. ∎

For `ℓ = 2`, `h` may reach `k − 1` and the inequality fails. Only `ℓ ≥ 3`
is used below. A second argument, noted by the referee, works for every
`ℓ`: the step in `y_D` is `t/h + λδ/(hq)`, so no label returns within fewer
than `h > h₀` steps.

### Theorem 2 (index-side 3-AP-free mechanisms are closed)

Let `c_KM > 0` be the constant of the Kelley–Meka bound (arXiv:2302.05537),
in the form of Bloom–Sisask (arXiv:2309.02353), which gives the exponent 1/9:
every 3-AP-free `A ⊂ [M]` has
`|A| ≤ M exp(−c_KM (log M)^{1/9})`. Assume (S1)–(S3) with `ℓ = 3`, and a
fibre piece `J` with

```
log |J| > (log(2k) / c_KM)^9   and   |J| ≥ 2k.                         (KM)
```

Then every `X` satisfying the hitting half of (I) has:

1. a rich progression `P` with `{0, h, 2h} ⊂ I_X(P)` for some prime
   `h ∈ (h₀, (k−1)/2]`, so (II_3) fails;
2. three keys of `X` in the box of `J`, with bands

   ```
   ⌊θ⌋,   ⌊θ + v⌋ + λ²δ²,   ⌊θ + 2v⌋ + 4λ²δ²,
   θ = C + s²,  v = 2sλδ,  s = qỹ_D(r + q^{D−1}m),  C = Σ_{i<D} (qỹ_i(r))²   (Q)
   ```

   (Lemma 1 of the lens note). So no band rule that forbids this quadratic
   triple, which is the polynomial variant of Salem–Spencer adapted to
   `⌊t₀ + t₁j + t₂j²⌋`, satisfies (I). The triple (Q) is not a 3-AP of
   `ℤ`: its two gaps differ by `2λ²δ²` up to the integer parts. So (2)
   does **not** exclude a band set `X_B` without 3-APs. That case is
   Proposition 4's, under its flatness hypothesis.

*Proof.* By (H), `|S_J| ≥ ⌊|J|/k⌋ ≥ |J|/(2k)`. By (KM),
`exp(−c_KM (log |J|)^{1/9}) < 1/(2k)`, so `S_J` contains a 3-AP
`m, m+δ, m+2δ`. Lemma E gives (1). The lens identity on the block
`m + iδ`, `i = 0, 1, 2`, gives (2). ∎

**When (KM) holds.** In the template, `log Y₀ = (c − o(1)) k^{1−a} log k`
for `a < 1/2`. In the source, `log Y₀ ≍ 10^{−5} k^{9/10} log k`. Either way
`(log Y₀)^{1/9}` grows like a power of `k`, so (KM) holds for every `k`
beyond a threshold that depends only on `c_KM`. `c_KM` is not explicit in
the literature. At the computed points, (KM) holds as soon as `c_KM`
exceeds the critical value below. (S3) holds there with a large margin,
both at `ℓ = 3` and at the worst useful length `ℓ = p₀(k) − 1` of
Theorem 3:

| point | `log₂ ln Y₀` | critical `c_KM` | `log₂(θ-margin / ln q)`, `ℓ = 3` | same, `ℓ = p₀ − 1` |
|---|---|---|---|---|
| `k = 2^739`, `a = 0.3`, `c = 1/9` | 523.1 | `2^{−49.1}` | 214.9 | 209.4 |
| `k = 2^739`, `a = 0.49`, `c = 1/9` | 382.0 | `2^{−33.4}` | 355.3 | 349.8 |
| `k = 2^1024`, `a = 0.45`, `c = 1/4` | 570.7 | `2^{−53.9}` | 452.3 | 446.5 |
| `k = 2^4096`, `a = 0.49`, `c = 1/9` | 2097.3 | `2^{−221.6}` | 1997.7 | 1990.3 |
| `k = 2^739`, source | 657.5 | `2^{−64.1}` | 80.5 | 75.1 |

All 21 points are in `RESULT.json`. The template is modelled by
`D = ⌈k^a⌉`, `h₀ = D⌈ln k⌉²`, `ln q = ck ln k/D`, and
`ln λ ≤ 1.25506 (h₀/ln h₀) ln k`.

**Densities, as the brief asks.** (H) forces relative density at least
`1/(2k)` on every fibre piece. The team's guess `ρ_AP ≈ log q/k` is not
needed and is not proved. These are densities of the pullback `S_J`, not
of band sets. A Behrend-type `S_J` at scale `Y₀` has density
`exp(−2√(2 ln 2 · ln Y₀))`. At `k = 2^739`, `a = 0.3`, that is
`exp(−2^{262.8})`, against `1/(2k) = exp(−2^{9.0})`. Kelley–Meka shows that
no 3-AP-free set does better than `exp(−c_KM k^{(1−a)/9 + o(1)})`, which is
`k^{−ω(1)}`.

### Theorem 3 (longer forbidden lengths: a reduction, and where it stops)

Assume (S1)–(S3) for `ℓ`, and let `J` be a fibre piece. If `X` satisfies
the hitting half of (I) and (II_ℓ), then

```
|J| < W(ℓ, k),
```

where `W(ℓ, k)` is the least `Y` such that every split `[Y] = S ⊔ A` has an
`ℓ`-AP in `S` or a `k`-AP in `A`.

*Proof.* (H) says `A = J ∖ S_J` has no `k`-AP. By Lemma E, an `ℓ`-AP in
`S_J` would contradict (II_ℓ). ∎

The verifier checks the split formulation against the known values
`W(3, k) = 9, 18, 22, 32` for `k = 3, …, 6`, exhaustively.

**Useful lengths are short.** (II_ℓ) gives (II) with `ε < 1/4` only if
`r_ℓ(k) < k/4`. For a prime `p ≤ ℓ` and `L = ⌈log_p k⌉`, the shifted digit
sets `{j : the L low base-p digits of j + t are nonzero}` have no `p`-AP
inside `[k] ⊂ [p^L]`. The lowest nonzero digit of the step runs through all
residues. Their average size on `[k]` is `k(1 − 1/p)^L`. So
`r_ℓ(k) ≥ k(1 − 1/p)^L`, and (II_ℓ) is useless once `ℓ ≥ p₀(k)`, the least
prime with `(1 − 1/p₀)^{⌈log_{p₀} k⌉} ≥ 1/4`. Then
`p₀(k) = O(log k / log log k)`. The values are 89, 113 and 353 for
`k = 2^739, 2^1024, 2^4096`.

**The open window `4 ≤ ℓ < p₀(k)`.** Closing it amounts to
`W(ℓ, k) ≤ Y₀`, that is `log W(ℓ, k) ≤ (c − o(1)) k^{1−a} log k`, for these
`ℓ`. No such upper bound is known for `ℓ ≥ 4`. Gowers and Leng–Sah–Sawhney
only give `log log W(ℓ, k) ≤ (log k)^{O_ℓ(1)}`. The known lower-bound
constructions all fail by a wide margin:

* random splits need `ℓ ≥ 2 ln Y₀ / ln(k/(2 ln Y₀))`, which is about
  `2^{517}` at `k = 2^739`, `a = 0.3`, against `p₀ = 89`;
* digit sets in base `p ≤ ℓ` (complement of "some digit is 0") reach
  relative density `1/(2k)` only if `(1 − 1/p)^{ln Y₀/ln p} ≥ 1/(2k)`, which
  needs `p ln p ≳ ln Y₀ / ln 2k`, far above `p₀`;
* Rankin's construction, in O'Bryant's form, has density
  `exp(−n2^{(n−1)/2}(ln Y)^{1/n} + O_ℓ(log log Y))` with `n = ⌈log₂ ℓ⌉`.
  For every `n ≤ ⌈log₂ p₀⌉` the exponent at `Y₀`, up to the constant
  `C_ℓ`, is at least `2^{60}` for every computed point, against `ln 2k ≤ 2^{11.5}`.

So no known `ℓ`-AP-free design reaches (I) in the useful range. Proving
that none exists is an off-diagonal van der Waerden problem, open but
expected: to our knowledge, no lower bound `log W(ℓ, k) ≥ k^{Ω(1)}` is known for any `ℓ` of
size `O(log k)`.

### Proposition 4 (band-side AP-free sets: the count the referee asked for)

For a box `B` of the `P1` region, let `w_B(t)` count the points `n` of the
long fibre pieces (`|J| ≥ 2Y₀`) of `B` with band `t`, and let
`W_B = Σ_t w_B(t)`. By (H), summed over the pieces,

```
Σ_{t ∈ X_B} w_B(t) ≥ W_B / (2k).                                       (H_B)
```

This is exact. It is the weighted form of "(I) needs density `≥ 1/(2k)`".
Call `w_B` **`(M, K)`-flat** when, after cutting the band range into windows
of `M` consecutive bands, each window's maximum of `w_B` is at most `K`
times its mean. If `X_B` has no 3-AP and `w_B` is `(M, K)`-flat, then
`Σ_{X_B} w_B ≤ K exp(−c_KM (log M)^{1/9}) W_B`. With (H_B), this gives

```
log M ≤ (log(2kK) / c_KM)^9.
```

So a band-side 3-AP-free `X` passes (I) only if, in every box of the `P1`
region, the fibre weight `w_B` is not flat at any scale
`M ≥ exp((log(2kK)/c_KM)^9)`. Those scales are tiny next to the band range
`≍ q²H` of a box. The weight would have to correlate with `X_B` exactly as
the referee says. Flatness of `w_B` is plausible: it is a shell volume in a
box, smooth at scales `≪ q`. It is **not proved** here. The crude bound
from one point per band per fibre only gives `K ≤ O(Dqλ/H)`, which is too
weak. Proposition 4 is therefore conditional. Theorem 2 needs no such
hypothesis, because it works on the pullback `S_J` directly.

### On the N2b class

Theorems 2 and 3 hold for every `X`, whatever rule defines it, so they do
not overlap with N2b. A candidate for the open window must also avoid N2b's
class: band-residue rules of total modulus `< q/(1536k³)`, which leave
saturated or untouched blocks. A digit construction in base
`< q^{1−o(1)}` would fall there.

## Checks in `verify.py`

1. Lemma E on the real-mesh toy of the lens note (`q = 2⁶¹ − 1`, `D = 3`,
   `λ = 840`, `k = 145`). 24 single-label case (ii) blocks, each with
   patterns of length `ℓ = 3, 4, 5` embedded at indices `0, h, 2h, …` of the
   constructed progression. Each embedding is checked for the index identity,
   `|w| ≥ (q − λδ)/h`, `|w|(k−1) ≥ q` (minimum ratio 2.15), and
   non-affinity by exact increments; the progressions visit 11 to 71 labels.
   Control: `h = 5`, which divides `λ`, gives an affine progression.
   On the toy, `λ = 840` replaces the source's primorial dilation, so the
   primes `h > 7` play the role of `h > h₀`.
2. The band triple (Q), exactly in Fractions.
3. The split formulation of `W(3, k)` for `k = 3..6`, exhaustive.
4. Digit sets: `p`-AP-free for every shift (`p = 3, 5, 7`), and averages
   exact.
5. Exact numerics, Decimal to 60 digits: `ln Y₀`, (S3) at `ℓ = 3` and at
   `ℓ = p₀(k) − 1`, through Rosser–Schoenfeld (`θ(x) > x(1 − 1/ln x)` for `x ≥ 41`,
   `θ(x) < 1.01624x`), Behrend against `1/(2k)`, the critical `c_KM`,
   `p₀(k)`, the Rankin/O'Bryant exponent and the random-split threshold.
   This covers 18 template points (`a ∈ {0.3, 0.45, 0.49}`,
   `c ∈ {1/9, 1/4}`) and 3 source points.

## What is not claimed

* No bound changes. 1/9 and every `c < 1/8` stand as they are.
* Theorem 2 depends on the Kelley–Meka / Bloom–Sisask theorem, which is
  cited and not reproved. Its threshold on `k` is ineffective until `c_KM`
  is made explicit. The Bloom–Sisask bound also holds only for `M` beyond
  its own threshold, another ineffective constant.
* Band-side 3-AP-free sets are not closed unconditionally. Theorem 2 closes
  the index-side reading and the quadratic triple (Q). A Behrend set in the
  band coordinate is closed only under Proposition 4.
* The window `4 ≤ ℓ < p₀(k)` is open. Only "no known construction works" is
  shown there, and that is not an impossibility theorem.
* Proposition 4 is conditional on flatness of the fibre weights, which is not
  proved.
* Nothing is said against deterministic `X` that get (II) by means other
  than AP-freeness of `I_X(P)` (discrepancy, pseudorandomness). Inside one
  fibre, (H) and the fibre part of (II) are compatible: a random set of
  density `C log Y₀/k` meets every `k`-AP of `J` and has `o(k)` points on
  every `k`-AP of `ℤ/q`. The obstruction to random `X` is global, and the
  route through `X` dense on slow lines and "anti-random" on rich ones
  stays open.
* The implication (I) + (II) ⇒ `c < 1/4` is the team's reduction, not
  proved here.
