# The first family caps the dilation: the 1/8 barrier of K1 and K3 holds for every choice of `a`

**Status:** structural research, with proofs and exact checks. It closes the
one exception left in the scope of `one-eighth-barrier` (PR #23, § 2,
"Fixed `a`"): sequences `a_k → 1/2⁻` with `ln E = o(ln q)`. The template's own
first local-lemma family forbids them. Lemma 1 below is a count, and
Theorem 2 a necessary condition on the dilation. Corollary 3 shows that
`ln λ = O(ln q / ln k)` for every choice of the parameters allowed by
(P1) to (P5) below, so the regime `ln λ ≍ ln q` is empty. Theorem 4 then
gives the barrier for K1 and K3, indexed by `(P, β)`, with the first family
certified in `𝒞_LL`, and with no condition on `a`: **no fixed `c > 1/8`**.
K2, and the merged forms, are not covered. No new bound on `W_r(k)` is
claimed.

**Base commit:** `e302239` (PR #23, `research/door-one-sprint5`).

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-first-family-caps-dilation/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. Standard library only, a few seconds.
`--git` also checks the cited statements of PRs #14, #19 and #21 at their
pinned commits, and `--source <dir>` checks them in the source manuscript.

## Setting, and what may vary with `k`

This is the template of the source (OpenAI manuscript, § 02 and § 04, pinned
in `source-manifest.json`), as it is used in `source-only-1-16` (#19, § 2)
and in the notes of #23. The statement is about the two-colour coefficient:
`r = 2`, then the digit product. Fox–Hunter's growing `r` is outside it, as
in `one-eighth-barrier`, § 1. Here **every parameter may depend on `k`**:
`D = ⌈k^{a_k}⌉`, `M`, `h₀`, `λ`, `q`, `ε`. Only (P1) to (P5) are used, with
`D < h₀ < 2M < k` and `D ≥ 2`.

* **(P1) The U mesh.** The first partition `U` has intervals of length
  `H_x = H/λ = 1/(k²λ)` (source, 02-setup, `H_x = H/λ` and
  `[aH_x, (a+1)H_x), 0 ≤ a < k²λ`). The x-label of `n` is
  `(U(x_i(n)))_{i≤D}`, with `x_i(n) = (n mod q^i)/q^i`. The full label is
  finer.
* **(P2) The dilation contains the primorial up to `h₀`, with
  `D < h₀ < 2M`.** By definition, `λ = ∏_{ℓ ≤ h₀} ℓ^{⌊log(2M)/log ℓ⌋}`
  (source, 02-setup). The source asks `h₀ < 2M < k` (02-setup, "We take `k`
  large enough that `h₀ < 2M < k`"), so each exponent is `≥ 1` and
  `ln λ ≥ θ(h₀)`. The source's count of regular positions,
  `D(4η + 1/h₀) < 1/2` (05-dichotomy), needs `h₀ > 2D`. #19 asks
  `D(4η + 1/h₀) ≤ ε_r` too, and `first-family-circularity` (#14, after
  Lemma 2) notes that every admissible `h₀` is at least `D`. The source takes
  `h₀ = D²`, and #19 takes `h₀ = D⌈ln k⌉²`. Without `h₀ < 2M`, only
  `ln λ ≥ θ(min(h₀, 2M))` remains, and check 3's mutant shows what is then
  lost.
* **(P3) The modulus.** `N = q^D`, where `q` is a power of a prime `P > k`,
  and `ck ln k ≤ D ln q ≤ ck ln k + D ln(2k²)` (source, 02-setup,
  q-bounds).
* **(P4) The first family.** The outer colouring gives each full label `β` an
  independent uniform bit `ξ_β`. The first family has one event per row of
  each label word of a cyclic progression with at least `δk` light positions
  (source, 04-outer, proof of the Balanced outer coloring; #19,
  Proposition 5). A label is light when its multiplicity is at most `k/M`
  (04-outer), so with `M < k` every label of a word with `k` **distinct**
  labels is light. Such a word has `w_max = 1`, hence a single row: its `k`
  labels. Its event is that some bit occurs on fewer
  than a fixed fraction `τ > 0` of the row (`τ = 1/4` in the source,
  `1/2 − ε` in #19). It contains the event that all `k` bits are equal, so
  its probability is at least `2^{1−k}`. **This is the only place where
  `r = 2` enters.** With `r ≥ 3` colours per label, the bad event of a row
  ("some colour on fewer than a fraction `τ > 0` of it") contains "colour `v`
  is absent from the row", of probability `(1 − 1/r)^k`. That is better than
  `r^{1−k}`. Write `μ_r = 2^{1−k}` for `r = 2`, and `μ_r = (1 − 1/r)^k` for
  `r ≥ 3`. For `r = 2` the two bounds are the same up to the factor `2`.
* **(P5) The certificate of the first family** is a criterion of `𝒞_LL`, the
  class of `keyed-local-lemma-and-large-moduli` (#20, Part A), in which the
  source's finite asymmetric local lemma lies.

## 1. The count

Fix `n₀ ∈ ℤ/N`. Let `F` be the largest fibre of the x-label, and `Δ` the set
of differences of two elements of one fibre. By `first-family-circularity`
(#14, "More generally"), `F ≤ (⌊qH_x⌋ + 1)^D` and
`|Δ| ≤ (2qH_x + 1)^D`.

**Lemma 1.** The progressions of `ℤ/N` through `n₀` whose `k` x-labels are
pairwise distinct carry at least

```
(N − 1 − (k−1)|Δ|) / (k F)
```

distinct **sets** of x-labels.

*Proof.* Count the pairs `(j₀, d)`, with `d ≠ 0` and `0 ≤ j₀ < k`, of the
progression `n₀ + (j − j₀)d`, `j < k`. Its terms are distinct, since every
nonzero element has order at least `P > k`. There are `k(N − 1)` pairs.
Positions `i < j` with equal x-labels force `(j − i)d ∈ Δ`. Since
`0 < j − i < k < P`, `j − i` is invertible modulo `N`, so at most
`(k − 1)|Δ|` steps `d` do so for each `j₀`. That leaves at least
`k(N − 1 − (k − 1)|Δ|)` pairs with distinct x-labels.

Given its set `S` of labels and `j₀`, a pair is determined by the neighbour
`n₀ + d` (or `n₀ − d` if `j₀ = k − 1`). Its label lies in `S`, which gives
at most `k` choices, each fibre has at most `F` elements, and there are `k`
values of `j₀`. So each set comes from at most `k²F` pairs. ∎

The same holds for full labels, since they are finer. Distinct x-label sets
give distinct full-label sets.

## 2. The condition on the dilation

**Theorem 2 (the first family caps `λ`).** Under (P1) to (P5), with `r`
colours per label (`r = 2` for the template), suppose a criterion of `𝒞_LL`
certifies the first family for some `k ≥ 6`. Then

```
(U)    D · ln( min(k²λ, q) / 2 )  <  ln(1/μ_r) + ln(4k),
```

that is, `(k − 1) ln 2 + ln(4k)` for `r = 2`, and, for `r ≥ 3`,

```
       D · ln( min(k²λ, q) / 2 )  <  k ln(r/(r−1)) + ln(4k).
```

*Proof.* Take the bit `ξ_β` of `β = L(n₀)`. By Lemma 1 applied to full
labels, at least `(N − 1 − (k−1)|Δ|)/(kF)` distinct sets of `k` distinct
labels contain `β`. Each set is the single row of a word with `k` distinct
labels, all of them light. Distinct sets give distinct events, since an event
reads the set of labels of its row. Each event has probability at least
`μ_r` (P4). By Theorem A of the keyed-local-lemma note, a criterion of
`𝒞_LL` that certifies needs `Σ_{E ∋ ξ_β} μ(E) < 1`. So

```
μ_r · (N − 1 − (k−1)|Δ|) / (kF) < 1.
```

* If `qH_x < 1`, the x-label is injective, so `F = 1` and `Δ = {0}`. Then
  `N − 1 − (k−1)|Δ| = N − k ≥ N/2`, and `N ≥ (q/2)^D`.
* If `qH_x ≥ 1`, then `F ≤ (2qH_x)^D = N(2/(k²λ))^D` and
  `|Δ| ≤ (3qH_x)^D ≤ N·3/(k²λ)`. So `(k−1)|Δ| ≤ 3N/(kλ) ≤ N/2` for
  `kλ ≥ 6`, hence `N − 1 − (k−1)|Δ| ≥ N/2 − 1 ≥ N/4`, and
  `N/F ≥ (k²λ/2)^D`.

In both cases `(N − 1 − (k−1)|Δ|)/(kF) ≥ (min(k²λ, q)/2)^D / (4k)`. ∎

With the row's own threshold, the event "some bit on fewer than `τk` of the
row" has probability about `e^{−kI(τ)}`, with `I(τ) = ln 2 − H(τ)`. That
gives the stronger condition `D ln(min(k²λ, q)/2) < kI(τ) + O(ln k)`. It is
not used below.

## 3. The regime of the exception is empty

**Corollary 3.** Under (P1) to (P5), with `r = 2` and `c > 0` fixed, the
following hold for `k` large, uniformly in all the other parameters.

1. `λ < q/k²`.
2. `D θ(D) < k ln 2 + ln(4k)`, hence `D < √(k ln 2)·(1 + o(1))`.
3. `ln λ < (k ln 2 + ln(4k))/D − 2 ln k + ln 2`, hence
   `ln λ / ln q < (ln 2 + ln(4k)/k)/(c ln k)`.
4. `λ ≤ q/(400k³)`, and the hub of `local-lemma-hub` (#14, Lemma H) has
   `ln E ≥ ln q − ln λ − 3 ln k − ln 67 ≥ (1 − ε_k) ln q`, with `ε_k → 0`
   uniformly.

In particular `ln λ ≍ ln q` never happens, and neither does `ln E = o(ln q)`:
the sequences excepted in `one-eighth-barrier`, § 2, do not satisfy the
template's own first family.

*Proof.*

1. If `λ ≥ q/k²`, the left side of (U) is
   `D ln(q/2) ≥ (D ln q)/2 ≥ (ck ln k)/2`, which exceeds `k ln 2 + ln 4k`.
2. By (P2), `ln λ ≥ θ(h₀) ≥ θ(D)`, and the left side of (U) is
   `D(2 ln k − ln 2 + ln λ) ≥ D θ(D)`. For `D ≥ 41`,
   `θ(D) > D(1 − 1/ln D)` (Rosser–Schoenfeld).
3. Rearrange (U), and use `ln q ≥ ck ln k/D` (P3).
4. From 2 and (P3), `ln q ≥ ck ln k/D ≥ (c/√(ln 2)) √k ln k (1 − o(1))`.
   From 3, `ln q − ln λ ≥ (1 − O(1/ln k)) ln q`, which exceeds
   `3 ln k + ln 400` and `3 ln k + ln 67` by far. ∎

Item 1 also recovers (A) of `one-eighth-barrier` for the template's `λ`: the
injective regime and the window `q/(400k³) < λ ≤ q/k²` fail (U). Corollary 3
says more. The first family alone keeps `D ln λ` below `k ln 2`, so `λ` is
never a power of `q`.

## 4. The barrier with no condition on `a`

K1 and K3 are as in `one-eighth-barrier`, § 2. In K1, iid flips at rate
`p ≤ 1/2` are certified by a criterion of `𝒞_LL` on the canonical events
indexed by `(P, β)`. In K3, a product law of constant marginal `ρ ≤ 1/2` is
certified on the failure events of (I′) and (II′_θ), with `θ > 0`.

**Theorem 4.** Fix `c > 1/8`. Then there is `k₀(c)`, depending only on `c`,
such that for every `k ≥ k₀(c)` and every choice of the parameters subject to
(P1) to (P5), `D < h₀ < 2M < k` and `D ≥ 2`, the following do not both hold:

* the first family is certified by a criterion of `𝒞_LL`;
* a certificate of kind K1 (or K3) concludes at `N ≥ k^{ck}`.

So the method has **no fixed `c > 1/8`** through K1 or K3, indexed by
`(P, β)`, whatever `a_k`.

`p ≤ 1/2` and `ρ ≤ 1/2` are assumed. For the flips this costs nothing.
Exchanging the two colours maps the rate `p` to `1 − p` and the canonical
events `(P, β)` to `(P, ¬β)`, with the same probabilities, and it does not
change which progressions are monochromatic.

*Proof for K1.* Corollary 3 gives `λ ≤ q/(400k³)`, `D ≤ √(k ln 2)(1+o(1))`
and `ln E ≥ (1 − ε_k) ln q`. The two halves of Proposition 1 of
`one-eighth-barrier` then hold with explicit terms. Neither half used a fixed
`a` beyond these three facts.

* *Hub.* `E(1−p)^k < 1` gives `p > ln E/(k + ln E)`, so
  `ln(1/p) ≤ ln 2 + max(0, ln(D/((1 − ε_k) c ln k)))`.
* *Rich side.* (T) is applied to the `≥ N²/4` progressions with no repeated
  V-box. The count is item 2 of `rich-cover-barrier` (#21):
  `kN²(4/k² + 1/q)^D = o(N²)` for `D ≥ 2`. Each has probability at least
  `p^{k/2}(1−p)^k ≥ p^{k/2} 2^{−k}`. Summing (T) over the keys, with `k`
  keys per event, gives `(N²/4)·p^{k/2}2^{−k}·k < |𝒦|`. Write
  `ln|𝒦| ≤ D v_k + ln D + 2 ln q`,
  with `v_k = ln(4k²(D+1) ln q + 4) = O(ln k)`, by Corollary A1 of the
  keyed-local-lemma note and the mesh of 02-setup
  (`|V| = 2⌈k²R⌉`, `R ≤ (D+1) ln q`). With `ln q = ln N/D` and
  `ln N ≥ ck ln k`, this gives

  ```
  c (1 − 1/D)  <  ln(1/p)/(4 ln k)  +  (k ln 2 + D v_k + ln 4D)/(2k ln k).
  ```

* *The two together.* If `D ≥ ln k`, then
  `ln(1/p) ≤ ½ ln k − ln ln k + O(1)` and `D v_k = O(√k ln k)`, so
  `c < 1/8 − (ln ln k)/(4 ln k) + O(1/ln k)`. If `D < ln k`, the right side is
  `O(1/ln k)` while the left side is at least `c/2`. Either way `c > 1/8`
  fails for large `k`. Every term is bounded uniformly in the parameters, by
  Corollary 3 and `D ≥ 2`. So the threshold `k₀(c)` depends only on `c`. ∎

*Proof for K3.* The proof is the same. The hub gives `ρ > ln E/(k + ln E)`.
On the rich side, the progressions with `k` distinct full labels and no
repeated V-box are `γ`-rich by (P4): every bit occurs on at least `τk`
positions. There are at least `N²/4` of them. By Lemma B1 of the
keyed-local-lemma note, a repeated label occurs on at most a fraction
`η = 2/λ + k²/N` of the pairs, and `λ ≥ 30`. Item 2 of #21 handles the
repeated V-boxes. Each has failure probability at
least `ρ^{(1/2−θ)k+1}2^{−k}` (Proposition 5 of `exact-door-one-condition`).
This gives `c(1 − 1/D) < (1/2 − θ) ln(1/ρ)/(2 ln k) + O(1/ln k)`, hence
`c ≤ (1/2 − θ)/4 + o(1) < 1/8`. ∎

**On "`≤ 1/8 + o(1)`" and "no fixed `c > 1/8`".** The theorem claims exactly
the second. The inequality obtained is stronger: for large `k`,
`c(1 − 1/D) < 1/8 − (ln ln k)/(4 ln k) + O(1/ln k)`. At the three points
computed (check 3), the least `c` that K1 cannot certify is `0.12357`,
`0.12385` and `0.12459` at `k = 2^739, 2^1024, 2^4096`. These lie below `1/8`
by `0.0014`, `0.0012` and `0.0004`. They are computed **on a grid of `D`**,
about 25 values from `2` to the largest `D` allowed by (U), both ends
included. The proof covers every `D`; the grid does not. No claim is made at
`c = 1/8` itself.

**An explicit threshold, measured.** The same computation at smaller `k`
gives `0.14468`, `0.12683`, `0.12342`, `0.122` and `0.12216` at
`k = 2^20, 2^40, 2^60, 2^100, 2^200` (check 3b). They pass below `1/8`
between `2^40` and `2^60`, and stay below at every larger point computed.
They are not monotone. From `2^100` on they rise back towards `1/8` from
below, as the bound `1/8 − (ln ln k)/(4 ln k) + O(1/ln k)` predicts. So, on
this grid of `D`, K1 cannot certify any `c ≥ 1/8` at the six points from
`k = 2^60` on. This is a measurement at these points, not a proof for every
`k ≥ 2^60`, nor of `k₀(1/8 + ε)` for every `ε`.

## 5. What this changes in `one-eighth-barrier`

* The paragraph "Fixed `a`" of its § 2 names the only exception to K1 and K3.
  By Corollary 3 it is empty for the template. K1 and K3, indexed by
  `(P, β)`, hold for every choice of `a_k`. The barrier of #23 is then
  complete for these two certificate kinds.
* **Not changed:**
  * K2. Its flip side is uniform: Theorem 1 of `single-label-obstructions`
    needs only `λ ≤ q/(400k³)`, which Corollary 3 gives. Its rich side
    (Proposition 5′ of #21) uses `ln q ≫ D ln k`. Near `a = 1/2` this holds
    only up to a constant, since `D ≤ √(k ln 2)` gives
    `ln q/(D ln k) ≥ c/ln 2`. It is not re-examined here, and stays
    conditional on (G♭).
  * The merged forms of K1 and K3, which stay conditional on (G♭)(ii).
  * The certificates outside `𝒞_LL`.
* **`line-witnesses`** needs `a < 1/2` fixed for `T_line = e^{o(k)}`. The
  count `D ln λ` that it bounds is now `< k ln 2` (Corollary 3), but its
  `o(k)` needs more. That is not examined here.

## What is not claimed

* No bound on `W_r(k)`, and no ceiling for it.
* Theorem 4 concerns K1 and K3 indexed by `(P, β)`, for the template
  (P1)–(P5). A template with another U mesh, a dilation without the
  primorial up to `h₀ ≥ D`, or a first family certified outside `𝒞_LL` is
  not covered.
* K2's rich half, and the merged forms, are unchanged and conditional.
* The `O(1/ln k)` terms of Theorem 4 are made explicit only at the points of
  check 3, on a grid of `D`. The asymptotic statement is the proof above.
* Theorem 2 with `r` colours is the count only. Its use for `r ≥ 3` belongs
  to U2.
* `h₀ < 2M < k` and `D < h₀` are hypotheses of the source. A template that
  drops them is not covered.

## Checks in `verify.py`

0. **References.** The cited statements are checked verbatim, with
   whitespace normalised:
   * in the notes of this tree, always;
   * with `--git`, in the notes of PRs #14, #19 and #21, at their pinned
     commits;
   * with `--source <dir>`, in the sections `02-setup`, `04-outer` and
     `05-dichotomy`, whose sha256 must equal `source-manifest.json`.

   `source-manifest.json` itself is checked against its pinned hash.
1. **Lemma 1 on fifteen toys.** These are `ℤ/q^D` with the source's U mesh,
   `q ≤ 31`, `D = 2, 3`, `k = 3, 4, 6` and several `λ`, including both cases
   `qH_x < 1` and `qH_x ≥ 1`. Lemma 1 has no condition on `k`. The `k ≥ 6`
   of Theorem 2 only enters its last step. The check is exhaustive over every pair
   `(j₀, d)` through `n₀ = 0`, and verifies:
   * the fibre bound `F ≤ (⌊qH_x⌋ + 1)^D`;
   * the two steps of the proof: at most `k(k−1)|Δ|` pairs with a repeated
     label, and at most `k²F` pairs per label set;
   * the bound of Lemma 1.

   Mutants: an injective map to label sets fails (each set comes from at
   least two pairs, one per direction), and so does `(k−1)(|Δ|−1)` repeated
   pairs.
2. **Corollary 3 at `k = 2^739, 2^1024, 2^4096`.** The check finds the
   largest `D` allowed by (U) with `ln λ ≥ θ(D)`: `log_k D_max` is `0.49965`,
   `0.49974` and `0.49994`. At that `D`, with `c = 1/9`, it computes
   `ln λ/ln q ≤ 0.0122`, `0.0088` and `0.0022`, the scope
   `λ ≤ q/(400k³)`, and `ln E/ln q ≥ 0.988`, `0.991` and `0.998`.
3. **Theorem 4, explicit.** For every `D` of a grid up to `D_max` (both ends
   included), the check finds the least `c` at which the necessary inequality
   of K1 fails. It uses the most permissive values: the largest `λ` allowed
   by (U), `ln q` at its lower bound in `ln E` and at its upper bound in
   `ln|𝒦|`, and `p ≤ 1/2`. The search is by bisection in 80-digit `Decimal`.
   Its supremum over `D` is below `1/8` at the three points. Mutant: with
   `ln λ ≥ 0` in place of `θ(D)`, `D` can reach `k/ln k`, and the supremum
   rises to `0.2458`, `0.2467` and `0.2489`, towards `1/4`. The scope
   `λ ≤ q/(400k³)` of Lemma H is checked at every `(c, D)` used, and no
   failure is inferred where it does not hold.

   3b. The same supremum at `k = 2^20, 2^40, 2^60, 2^100, 2^200`. The check
   requires it above `1/8` at `2^40`, and below `1/8` at `2^60` and every larger
   point.
4. **Provenance.** The MANIFEST hashes are checked, and the summary must
   equal `RESULT.json`. `--write` rewrites `RESULT.json` only, and
   `--manifest` rewrites `RESULT.json` and `MANIFEST.json`. Neither writes
   anything when a check fails.
5. **Frozen statement.** Seven sentences and numbers of this README must
   occur verbatim: (U) for `r ≥ 3`, `h₀ < 2M < k`, `k₀(c)`, the conclusion
   of Theorem 4, the three `c*`, "no claim at `c = 1/8`", and the
   unchanged K2. Like every internal freeze, this guards only against
   oversight. The guard against a false change is the referee's tree hash
   (`METHODE.md`).
