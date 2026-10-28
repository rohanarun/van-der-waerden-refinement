# Literature calibration: the `ln 2` ceiling of the uniform coefficient

**Status:** three elementary propositions and a map of the 2024–2026
literature. No new bound on `W_r(k)`. Proposition 2 says what an improvement
past `ln 2` would settle; it is not an impossibility result.
**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.
**Depends on:** the source's digit product (Proposition 7.1 of the pinned
manuscript, `\label{transfer:product}`), used as stated, and Fox–Hunter's
Lemma 6.1, quoted.

## Normalization

All logarithms `ln` are natural, as in Fox–Hunter ("All logarithms are base
`e` unless otherwise specified"). For `r ≥ 2` and `α > 0`,

```
r^{α k ln k} = exp(α k ln k ln r) = k^{(α ln 2) k log₂ r},
```

so a bound `W_r(k) ≥ r^{α k ln k}` gives this repository's form
`W_r(k) > k^{c k ⌊log₂ r⌋}` for every `c < α ln 2` (strict because
`c < α ln 2`; the floor only helps, since `⌊log₂ r⌋ ≤ log₂ r`).

## Where the literature stands, in this normalization

| Result | Statement | `c` here |
|---|---|---|
| Erdős–Lovász 1975 | `W_r(k) ≥ r^{k−1}/(4k)` | 0 |
| Szabó 1990 | `W_2(k) ≥ 2^k/k^ε` | 0 |
| Kozik–Shabanov 2016 | `W_r(k) ≥ β r^{k−1}` | 0 |
| Berlekamp 1968 | `W_2(p+1) > p 2^p`, `p` prime | 0 |
| Campos–Fox–Schildkraut 2026 (arXiv 2608.20824) | `W_2(k) ≥ (1−o(1)) k 2^{k−1}`, all `k` | 0 |
| Blankenship–Cummings–Taranchuk 2018 | `w(r,k) > p(w(r−⌈r/p⌉,k) − 1)`, `p ≤ k` prime | 0 |
| Hunter 2025 (arXiv 2301.06212), as described by Fox–Hunter p. 2 | `(3^{r/3})^{(1−o(1))k}`, `r ≥ 6`, `3 ∣ r` | 0 |
| Kim 2026 (arXiv 2610.32000) | explicit blocks for `3 ≤ r ≤ 6`, `9 ≤ k ≤ 28`; proved not to change asymptotics | 0 |
| Fox–Hunter 2026, Thm 1 (arXiv 2606.02541) | `W_3(k) > 2^{k log* k / 4}` | 0 (superexponential, but `log* k = o(ln k)`) |
| **Fox–Hunter 2026, Cor. 5.1 and Thm 2** | `W_r(k) ≥ r^{(1−2/(2+α)−ε)k ln k}` for `r ≥ (ln k)^{2+α}`, `k` large | **up to `ln 2`**, for `r ≥ (ln k)^{2+α}` (Prop. 3) |
| OpenAI 2026 (pinned source) | uniform in `r ≥ 2`, absolute threshold | `10⁻⁵` |
| This repository (conditional) | uniform in `r ≥ 2` | `1/9`; sup `1/8` of the current template |

The density side, relevant to a deterministic progression-sparse set
(Porte 1): Behrend 1946 and Rankin 1961; Elsholtz–Hunter–Proske–Sauermann
2024 (arXiv 2406.12290, Theorem 1.1), the first improvement of Behrend's
constant for three-term progressions: `r₃(N) ≥ N·2^{−(C+o(1))√(log₂ N)}` with
`C = 2√(log₂(24/7)) < 2√2`, Behrend's being `2√2`; Kelley–Meka 2023 and
Leng–Sah–Sawhney 2024 on the upper side. Green 2022 and Hunter 2022 treat
the asymmetric `w(3,k)`. The pinned source cites most of these; this
repository did not.

Where `ln 2` comes from. The Erdős–Turán set `T_p` (integers with no base-`p`
digit equal to `p−1`) has no `p`-term progression and density `(1−1/p)^t` in
`[p^t]` (Fox–Hunter, Corollary 2.1). With `p ≈ k`, density `1/r` is reached
at `t ≈ k ln r`, that is in an interval of length `k^{k ln r} =
r^{(1−o(1)) k ln k}`: exactly the exponent Fox–Hunter call a bottleneck, and
`c = ln 2` in our units.

## Proposition 1 (the uniform coefficient is a two-color exponent)

Let `N_cyc(k)` be the largest `N` such that some `C : ℤ/Nℤ → {0,1}` has no
monochromatic `a, a+d, …, a+(k−1)d` with `d ≢ 0 (mod N)`. Put

```
c_cyc  = liminf_k  ln N_cyc(k)      / (k ln k),
c_2    = liminf_k  ln (W_2(k) − 1)  / (k ln k),
c_unif = sup { c : ∃K ∀k ≥ K ∀r ≥ 2,  W_r(k) > k^{c k ⌊log₂ r⌋} }.
```

Then `N_cyc(k) ≤ W_2(k) − 1`, and

```
max(c_cyc, c_2/3) ≤ c_unif ≤ c_2.
```

*Proof.* A progression in `{0, …, N−1}` with step `d ≥ 1` and
`(k−1)d ≤ N−1` has `d ≢ 0 (mod N)`, so a cyclic coloring restricts to a valid
interval coloring: `N_cyc(k) ≤ W_2(k) − 1`.

`c_cyc ≤ c_unif`: if `c < c_cyc`, then `N_cyc(k) > k^{ck}` for all large `k`,
and the digit product gives `W_r(k) > N_cyc(k)^{⌊log₂ r⌋} > k^{ck⌊log₂ r⌋}`
for every `r ≥ 2` at once.

`c_2/3 ≤ c_unif`: Fox–Hunter's Lemma 6.1 turns two interval `2`-colorings
into a `4`-coloring of `ℤ/Nℤ` without monochromatic `k`-term progressions,
for every `N ≤ 2W_2(k) − 2`. (Its two halves carry disjoint color sets. A
degenerate progression, whose terms fill a coset of a subgroup of order
`2 ≤ s < k`, has terms spaced `N/s ≤ N/2` apart around the whole circle and
never fits in one half, so the source's hypothesis, degenerate progressions
included, holds too.) The digit product's proof never uses the number
of colors, so with this `4`-coloring it gives `W_{4^m}(k) > (2W_2(k) − 2)^m
≥ (W_2(k) − 1)^m`. For `r ≥ 4` take `m = ⌊log₄ r⌋ = ⌊⌊log₂ r⌋/2⌋ ≥
⌊log₂ r⌋/3`; for `r = 2, 3` use `W_r(k) ≥ W_2(k)`. If `c < c_2`, this gives
`W_r(k) > k^{(c/3) k ⌊log₂ r⌋}` for all large `k`, uniformly in `r`.

`c_unif ≤ c_2`: the case `r = 2` of the uniform statement. ∎

So the uniform question is the two-color question, up to a factor 3
unconditionally, and from below by its cyclic form. Fox–Hunter's Theorem 2 and
Corollary 5.1 do not move `c_unif`: their range never contains `r = 2`. The
pinned manuscript says as much ("The bound here holds uniformly down to two
colors", with the crossover at `ε = 1/2`), and so does PR #16, *Remark
(consolidation)*; the sandwich is the precise form.

## Proposition 2 (the `ln 2` ceiling)

Suppose `c_unif > ln 2`, and fix `δ > 0` with `c_unif > (1+δ) ln 2`. Then for
every large `k` and **every** `r = 2^m`, `m ≥ 1`, the interval
`[⌊r^{(1+δ)k ln k}⌋]` contains a set of density at least `1/r` with no
`k`-term arithmetic progression.

*Proof.* For large `k` and every `m`, `W_{2^m}(k) > k^{(1+δ)(ln 2) k m} =
r^{(1+δ)k ln k}`. So `M = ⌊r^{(1+δ)k ln k}⌋` integers can be `r`-colored without
a monochromatic `k`-term progression, and one class has at least `M/r`
elements (the averaging observation of Fox–Hunter, §1). ∎

By Proposition 1 the hypothesis holds as soon as `c_cyc > ln 2`, or
`c_2 > 3 ln 2`. The source's two-color theorem (`\label{perturb:cyclic}`) is
cyclic, so an improvement of its template that reaches `c > ln 2` falls under
the first case.

Fox–Hunter (arXiv 2606.02541, §1, after Theorem 2): *"However, when `r` is
not too large with respect to `k` (i.e., when `r ≤ k^{O(1)}`), the authors
are not aware of any way to construct a set `S ⊂ [r^{(1+Ω(1))k log k}]` with
density `1/r` which does not contain a `k`-term arithmetic progression. This
serves as a bottleneck for improving the exponent in Theorem 2 by a factor
of `1 + Ω(1)`. Moreover, any improvement to this bottleneck would
immediately improve the lower bound above, by plugging the improved
parameters into Theorem 5."* Proposition 2 produces that set for every
`r = 2^m`, including every `2^m ≤ k^{O(1)}`.

Reading. A uniform coefficient above `ln 2 ≈ 0.693` would settle a
construction Fox and Hunter state they do not know how to make, and by their
last sentence improve their Theorem 2; for `r = 2^m` it would already beat
their Theorem 2 directly, `r^{(1+δ)k ln k}` against `r^{(1−ε)k ln k}`. Between `1/8` and `ln 2` no
obstruction is known from the literature: the `1/8` ceilings of PR #16, and
the obstructions of PR #14 behind them, bound the current template, not the
problem. In these units the conditional `1/9` is `16.0 %` of `ln 2`, the
template's `1/8` is `18.0 %`, and the rank-split `1/16` (PR #6) is `9.0 %`.

## Proposition 3 (where Fox–Hunter already pass a given `c`)

For a fixed `0 < c < ln 2` and any `η > 0`, Fox–Hunter's Corollary 5.1 with
`2 + α = 2/(1 − c/ln 2) + η` and `ε` small enough gives `W_r(k) ≥
r^{(c/ln 2)k ln k} = k^{c k log₂ r} ≥ k^{c k ⌊log₂ r⌋}` for all large `k`
and every `r ≥ (ln k)^{2+α}`.

| `c` | Fox–Hunter reach `c` once `r ≥ (ln k)^{e}`, any `e > 2/(1 − c/ln 2)` ≈ |
|---|---|
| `1/16` | `2.19821` |
| `1/9` | `2.38180` |
| `1/8` | `2.44003` |

Their thresholds in `k` are not explicit, so this is an asymptotic statement
only; against the explicit thresholds of PR #15 (`2^{960}`, `2^{739}`) no
comparison is possible from their text. Their §6 also remarks that
`w(k;r) ≥ r^{(1−o(1))k log k}` could be obtained for `r = (log k)^{Ω(1)}`
through their Lemma 6.2; that is a remark, not a stated theorem.

## What the literature leaves open

Fox–Hunter's products come in two forms. Lemma 4.2 keeps the number of
colors fixed (three in Theorem 4, hence Theorem 1) and gains a factor
exponential in `k` per step. Lemma 4.3, through Theorem 5, gains about
`(2m)^{k/3}` per step, with `m = ⌈6 r^{2/k} ln r ln k⌉` in Corollary 5.1:
`exp(Θ(k ln ln k))` for `r ≤ k^{O(1)}`, `k^{Θ(k)}` only when `m = k^{Θ(1)}`.
It spends colors:
Theorem 5 assumes `4ms ≤ r`, so it does not act at `r = 2` or `3`, where
Proposition 1 pins `c_unif`. Whether a variant of Lemma 4.3 can act on a
two-color input such as the source's cyclic coloring is not addressed in
their paper, and not here.

## Reproduce

```sh
python3 -B verify.py
```

Expected: `OK: all checks pass and match RESULT.json` (standard library,
about two seconds). It checks the normalization, then the digit product
exhaustively on small cases. The bases are the largest `N` with a cyclic
two-coloring within the searched ranges (`4` for `k = 3`, `11` for `k = 4`,
`20` for `k = 5`; maximality is re-checked for `k = 3, 4`; `N_cyc` is not
monotone). The products on `[0, N^m)`, `m = 2, 3`, have no monochromatic
progression. The averaging step of Proposition 2 is plain pigeonhole and is
checked only as such. Controls that must fail: for each case, a base that is
a valid interval coloring but not a valid cyclic one makes the product fail,
so the cyclic hypothesis is load-bearing; a base with a monochromatic
progression is caught. Finally it recomputes the table of Proposition 3.
