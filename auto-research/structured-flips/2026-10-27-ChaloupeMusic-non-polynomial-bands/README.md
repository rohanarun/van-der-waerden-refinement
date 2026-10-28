# Band sequences of rich progressions are not polynomial modulo a large prime

**Status:** structural research note, with a complete proof and exact finite
checks. It closes a **method**, not a class of frozen sets: reading the band
sequence of a rich progression as the values of a polynomial modulo `ℓ`, so
that Weil or Deligne bounds apply along the progression. For the large moduli
of the template that method is already empty by length; the theorem adds a
closure for small moduli `k·2^{s+1} ≪ ℓ ≲ k²` (see "What this closes"). No
bound on `W_r(k)` is claimed.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, through the local
branch `pr/exits-past-1-8` (`83b872a`).

**Sources:** the construction, coordinates, keys and bands of OpenAI,
*Quantitative Superexponential Bounds for van der Waerden Numbers*, pinned in
`source-manifest.json` (Sections 2 and 6). The count of rich progressions is
Corollary A2 (2) of `2026-10-26-ChaloupeMusic-keyed-local-lemma-and-large-moduli`
(sprint 3, track P1b, not in this tree).

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-non-polynomial-bands/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. About eight seconds, standard library only.

## The question

Door 1 freezes a set `X` of keys. A natural candidate is a character rule on
the band coordinate, `X = {(W, t) : χ(f(t)) = 1}` for a character `χ` of
`F_ℓ` and a few polynomials `f`, with `ℓ` a large prime. To prove (II′) for
such a rule along a rich progression `P`, one would read `t_j = t(n₀ + jd)`
modulo `ℓ` as `g(j)` for a polynomial `g`, so that the pattern
`(χ(f(t_j)))_j` becomes `(χ(f(g(j))))_j`, which Weil (one variable) and
Deligne (several) control. This note shows that the reading is not available:
for almost every rich progression, no window of the band sequence is a
polynomial of bounded degree modulo `ℓ`.

## Setting

`q = P^e` with `P > k` prime, `N = q^D`, `λ` a unit modulo `N`. For `n ∈ ℤ/N`,
`y_i(n) = λn/q^i mod 1` (`1 ≤ i ≤ D`), `ỹ_i(n) ∈ [−1/2, 1/2)` its centred
representative, and the band is `t(n) = ⌊q²‖ỹ(n)‖²⌋` (source, Section 6). A
progression is `n_j = n₀ + jd`, `0 ≤ j < k`, `d ≠ 0`, with bands
`t_j = t(n_j)`. `ℓ` is a prime not dividing `2q`. A sequence agrees modulo `ℓ`
with a polynomial of degree at most `s` on a window of `m ≥ s + 2`
consecutive indices exactly when every `(s+1)`-st difference
`Δ^{s+1} t_j = Σ_{i=0}^{s+1} c_i t_{j+i}`, `c_i = (−1)^{s+1−i} binom(s+1, i)`,
inside the window vanishes modulo `ℓ`. Write `B_D = ỹ_D(d)`.

## Lemma 1 (Beatty sequences of polynomial shape)

Let `|B| ≤ 1/2`, `Y` real, `w_j = ⌊Y + jB + 1/2⌋` on `m` consecutive indices,
and `m ≥ 2s`. If `(w_j)` agrees with a real polynomial of degree at most `s`,
then `|B| ≤ 1/(m − 1)`.

*Proof.* The increments `δ_j = w_{j+1} − w_j` lie in `{0, 1}` if `B ≥ 0` and
in `{−1, 0}` if `B < 0` (here `|B| ≤ 1/2 < 1`). They agree with a polynomial of degree at most
`s − 1` on `m − 1` points. If it is not constant, it takes each value at most
`s − 1` times, so `m − 1 ≤ 2(s − 1)`, against `m ≥ 2s`. So `δ_j = σ` is
constant and `w_j = w₀ + jσ`. Then `|Y + jB − w₀ − jσ| ≤ 1/2` for every `j`
gives `|B − σ|(m − 1) < 1`, and `|B| ≤ 1/2 < 1 − 1/(m−1)` forces `σ = 0`
when `m ≥ 4`. For `m ≤ 3` the bound `1/(m−1) ≥ 1/2` is automatic. ∎

`verify.py` (check 1) confirms Lemma 1 on 462 480 rational cases and finds a
counter-example as soon as `m ≤ 2s − 1`.

## Lemma 2 (one orbit)

Fix `r` modulo `q^{D−1}` and a step `d` with `|B_D| > 1/(m − 1)`, and a
window of `m ≥ 2s` indices. Suppose `ℓ > (s + 1) 2^{s+1}`. Along the orbit
`n₀ = r + q^{D−1}u`, `u ∈ ℤ/q`, at most

```
(2^{s+1} + 1)(q/ℓ + m + 1)
```

values of `u` make the band residues on that window a polynomial of degree at
most `s` modulo `ℓ`.

*Proof.* **Only coordinate `D` moves.** For `i < D`, `λq^{D−1}u/q^i` is an
integer, so `ỹ_i(n_j)` does not depend on `u`. In coordinate `D`, `y_D`
shifts by `μ/q` with `μ = λu mod q`, and `u ↦ μ` is a bijection of `ℤ/q`.

**Arcs.** As `μ` runs over `ℤ/q`, each of the `m` window positions crosses the
cut of coordinate `D` once, so `ℤ/q` splits into at most `m + 1` arcs `I` on
which every wrap is fixed. On an arc, `x_j(μ) = qỹ_D(n_j) = x_j + μ` with
`x_j` fixed. With `R_j = Σ_{i<D} (qỹ_i(n_j))²`, the band is
`⌊R_j + x_j² + 2μx_j⌋ + μ²`, since `μ²` is an integer.

**The difference.** Write `Y_j = ỹ_D(n₀) + jB_D` (unreduced) and
`w_j = Y_j − ỹ_D(n_j) ∈ ℤ`, the wraps of coordinate `D` on the arc. For a
sub-window starting at `j`, `Σ c_i = Σ c_i i = 0` (as `s ≥ 1`) gives
`Σ c_i x_{j+i} = −qW` with `W = Σ c_i w_{j+i} ∈ ℤ`, constant on the arc, and
`Σ c_i μ² = 0`. Hence

```
Δ^{s+1} t_j(μ) = K − 2qWμ − E(μ),
```

with `K` constant on the arc and `E(μ) = Σ c_i {R_{j+i} + x_{j+i}² + 2μx_{j+i}}`.
`E(μ)` lies in an interval of length `Σ|c_i| = 2^{s+1}`, and
`E(μ) ≡ K (mod 1)` because `2qWμ` and the left side are integers. So `E(μ)`
takes at most `2^{s+1} + 1` values.

**A sub-window with `W ≠ 0`.** On the arc, the wraps `(w_j)` of the window are
`⌊Y′ + jB_D + 1/2⌋` for a real `Y′`. Since `|B_D| > 1/(m−1)`, Lemma 1 says
they are not a polynomial of degree at most `s` on the window, so some
sub-window has `W ≠ 0`. Successive wraps differ by at most 1, so
`|W| ≤ (s + 1) 2^{s+1} < ℓ`. With `ℓ ∤ 2q`, `2qW` is invertible modulo `ℓ`.

**Count.** If the window is polynomial modulo `ℓ`, this sub-window has
`Δ^{s+1} t_j(μ) ≡ 0 (mod ℓ)`, that is `2qWμ ≡ K − E(μ)`. For each of the
`2^{s+1} + 1` values of `E`, `μ` lies in one residue class modulo `ℓ`, which
meets the arc in at most `|I|/ℓ + 1` points. Summing over the arcs,
`Σ_I (2^{s+1} + 1)(|I|/ℓ + 1) ≤ (2^{s+1} + 1)(q/ℓ + m + 1)`. ∎

`verify.py` (check 4) recomputes the identity exactly on 20 970 orbit points:
`W` is an integer, constant on each arc, the unfloored combination has slope
exactly `−2qW`, and the noise stays within `2^{s+1}`. With small `ℓ` (7 to 31)
the per-window count of zeros (650 in total) stays below the bound of each
arc. Check 2 runs Lemma 2 on whole orbits (`q = 1009, D = 2` and
`q = 211, D = 3`).

## Theorem 3

Let `s ≥ 1`, `2s ≤ m ≤ k` and `ℓ` a prime, `ℓ ∤ 2q`, `ℓ > (s+1)2^{s+1}`. The
number of progressions `(n₀, d)`, `d ≠ 0`, whose band sequence agrees modulo
`ℓ` with a polynomial of degree at most `s` on **some** window of `m`
consecutive indices is at most

```
N² [ k (2^{s+1} + 1)(1/ℓ + (k + 1)/q) + 2/(m − 1) + 1/N ].
```

*Proof.* `d ↦ λd mod N` is a bijection, so `ỹ_D(d)` is uniform on
`q^{−D}ℤ ∩ [−1/2, 1/2)`, and `|B_D| ≤ 1/(m−1)` holds for at most
`2N/(m−1) + 1` steps. For the other steps, the orbits `r + q^{D−1}ℤ/q`
partition `ℤ/N`, and Lemma 2 applies to each of the at most `k` windows. ∎

**Corollary 4 (rich progressions).** At least `N(N−1) − N²(1/λ + k²/(2N))`
progressions have `k` distinct full labels and are rich (P1b, Corollary A2
(2)). So all but a fraction

```
k (2^{s+1} + 1)(1/ℓ + (k+1)/q) + 2/(m − 1) + 1/λ + k²/N + O(1/N)
```

of rich progressions have no window of length `m` on which the bands are a
polynomial of degree at most `s` modulo `ℓ`. In the template
(`ln q = c k^{1−a} ln k`, `ℓ ≥ q^{1−o(1)}`), the first term is
`2^{s+1} k^{2+o(1)}/min(ℓ, q)`, negligible while `s ≤ (1 − o(1)) log₂ min(ℓ, q)`, and the
fraction is `2/(m − 1) + o(1)`. With `m = ⌈√k⌉`, all but `O(k^{−1/2})` of
the rich progressions qualify.

## What this closes, and in which range of `ℓ`

A proof of (II′) for a character rule must control, on each rich `P`, the
pattern `(χ(f(t_j)))_{j<k}`. Two facts limit what any bound **along one
progression** can say, and Theorem 3 is only the second one.

* **Length.** Such a sum has at most `k` terms. Weil and Deligne say
  something from length about `√ℓ log ℓ` on, Burgess from `ℓ^{1/4+ε}`, and
  sums over Beatty-type sequences (Banks and Shparlinski, Bull. Austral.
  Math. Soc. 73 (2006), arXiv:math/0608042) from `ℓ^{1/3+ε}`. For the moduli
  of the template, `ℓ ≥ q^{1−o(1)} = e^{k^{1−a+o(1)}}`, every one of them is
  empty along a progression, whatever the shape of the bands. This needs no
  theorem.
* **Shape (Theorem 3).** It has content only where the length allows Weil,
  `ℓ ≲ k²`, and where its error term is small, `ℓ ≫ k·2^{s+1}`. In that range
  it adds that, for all but an `O(1/m)` fraction of rich progressions, no
  window of `m ≥ 2s` bands is a polynomial of degree `≤ s` modulo `ℓ`, so the
  pattern is not `(χ(F(j)))_j` for any polynomial `F` of degree at most
  `s·deg f`.

**The border with N2b** (`2026-10-20-ChaloupeMusic-algebraic-band-rules`,
moduli up to about `q/(1536k³)`, which contains the range `ℓ ≲ k²`). A
character rule `X = {(W, t) : χ(f_i(t)) = 1, i ≤ r}` modulo one prime `ℓ` is
a membership `t mod ℓ ∈ T`. When it is **sparse**, `2k|T| < ℓ` (density below
`1/(2k)`, about `r ≥ log₂(2k)` independent conditions), it satisfies (G-ii) of
N2b and is already closed on the side of (I): some single-label blocks are
saturated or untouched. When it is **dense**, it is outside N2b unless `T` is
square-blind (G-i), and (II′) does not exclude it (B1 of P1b falls under
(II′)). Theorem 3 then closes, for these dense rules and small moduli, the
reading of (II′) through Weil along the progressions. It adds nothing on the
side of (I).

On the exceptional progressions (`|B_D| ≤ 1/(m−1)`, which contain the affine
ones of Proposition B3 with bands `(a + j)²`), the bands may be polynomial,
and the length obstruction still applies.

## What is not claimed

* Nothing about the class of character rules itself: a rule `X_χ` could still
  satisfy (II′) for reasons that are not read along the progression.
* Three methods do not read the bands as a polynomial and are **not** closed
  here: the Fourier expansion of the floor in `t_j = ⌊Q(j)⌋` (Vinogradov's
  method), character sums over Beatty-type sequences, and sums averaged over
  the parameters `(n₀, d)` of the progressions. Along one progression, the
  first two are empty by length for `ℓ ≥ k^{4+ε}`. The third is a different
  method, whose natural output is a first moment, which Proposition 5 of the
  exact-door-one note (`2026-10-26-ChaloupeMusic-exact-door-one-condition`)
  shows cannot certify past `b_X/4`.
* The exceptional fraction `2/(m − 1)` comes from one coordinate. It is not
  claimed optimal.
* The count of rich progressions is imported from P1b (Corollary A2 (2)).

## Checks in `verify.py`

1. **Lemma 1** on 462 480 rational cases (`m ≤ 14`, `B = p/r`, `r ≤ 40`, 12
   phases). Control: for `m = 5`, `s = 3` (`m ≤ 2s − 1`), a non-affine
   polynomial wrap sequence with `|B| > 1/(m−1)` exists.
2. **Lemma 2** on whole windows of `k`: `q = 1009, D = 2` (`k = 12`, `s = 1, 2, 3`,
   `ℓ = 31, 101, 2003`) and `q = 211, D = 3` (`k = 10, 16`, `ℓ = 13, 7`), 60 or
   40 random `(r, d)` each. The number of `u` with polynomial bands never
   exceeds the bound; the steps with `|B_D| ≤ 1/(k−1)` are set aside, about
   `2/(k−1)` of them, as predicted.
2b. **Lemma 2 where it bites**: one window of `m = 4` at a random start,
   `s = 1, 2`, `ℓ = 11, 29`, on `q = 1009, D = 2` and `q = 211, D = 3`. Bad
   shifts occur (572 in total, the check requires some), and the largest
   ratio to the bound is about `0.14`.
3. **The exceptional set is needed.** The squares family `n_j = λ^{−1}(a + j)`
   (80 progressions) has bands exactly `(a + j)²`, a polynomial of degree 2,
   and every one has `|B_D| ≤ 1/(k−1)`.
4. **The identity of Lemma 2**, exactly (`Fraction`), on three orbit
   families, with the per-window count against the bound.
5. **Provenance**: MANIFEST hashes; summary equal to `RESULT.json`.
