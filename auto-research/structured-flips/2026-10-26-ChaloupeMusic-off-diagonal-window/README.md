# The off-diagonal window `4 ≤ ℓ < p₀(k)` is open in both directions

**Status:** research note: a literature state, two short propositions, and
exact numerics. No bound is claimed, and the window is neither closed nor
opened. The note says which off-diagonal van der Waerden statement would
close the window and which one is needed to open it, measures how far each
is from the literature, and shows that the cut at `p₀` comes from the
literal form of (II).

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, on top of the
local branch `pr/exits-past-1-8` (`83b872a`).

**Depends on:** `2026-10-26-ChaloupeMusic-ap-free-frozen-sets` (Lemma E,
Theorem 3, `p₀(k)`, and its template model), and through it
`2026-10-20-ChaloupeMusic-single-label-lenses` (Lemma R: fibre pieces of
length at least `2Y₀`, `Y₀ = ⌊q/(2048k²λ)⌋`).

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-26-ChaloupeMusic-off-diagonal-window/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. It takes under a second and uses only the
standard library.

## The question

Write `W(ℓ, k)` for the least `N` such that every split `[N] = S ⊔ A` puts
an `ℓ`-AP in `S` or a `k`-AP in `A`. Theorem 3 of `ap-free-frozen-sets`
shows the following. If a frozen set `X` satisfies (I), and no rich
progression has `ℓ` indices in arithmetic progression inside `X` (II_ℓ),
then every fibre piece `J` satisfies `|J| < W(ℓ, k)`. Pieces of length
`N₀ = 2Y₀` exist, so the route needs

```
W(ℓ, k) > N₀,    ln N₀ = ln q − ln λ − 2 ln k − ln 1024 = (c − o(1)) k^{1−a} ln k.     (V_ℓ)
```

(II_ℓ) gives the literal (II), `|X ∩ P| ≤ εk` with `ε < 1/4`, only for
`ℓ < p₀(k) = O(log k / log log k)` (89, 113, 353 at `k = 2^739, 2^1024,
2^4096`). The case `ℓ = 3` is closed by Theorem 2 of that note. The
question is whether (V_ℓ) can hold for some `4 ≤ ℓ < p₀(k)`.

## Literature, as of 26/10/2026

| Quantity | Best known | Source |
|---|---|---|
| `W(3, k)`, lower | `exp(c (log k)^{4/3} / (log log k)^{1/3})` | Green, arXiv:2102.01543 (2021; Forum Math. Pi 2022) |
| `W(3, k)`, lower | `exp(c (log k)² / log log k)` | Hunter, arXiv:2111.01099 (2021) |
| `W(3, k)`, upper | `exp(k^{c})` with `c < 1` | Schoen (2021), per erdosproblems.com/721 |
| `W(3, k)`, upper | `exp(O((log k)⁹))` | Bloom–Sisask, arXiv:2309.02353 (2023), after Kelley–Meka, arXiv:2302.05537 (2023) |
| `W(ℓ, k)`, `ℓ ≥ 4` fixed, lower | `c_ℓ (k / log k)^{ℓ−1}` | Li–Shu, Adv. Appl. Math. 44 (2010) |
| `W(ℓ, k)`, `ℓ ≥ 4`, upper | none stated; only through `r_ℓ` (Proposition 1) | erdosproblems.com/721 (updated 04/04/2026) lists none |
| `r_4(N)`, upper | `N (log N)^{−c}`, `c > 0` not explicit | Green–Tao, arXiv:1705.01703 (2017; Mathematika) |
| `r_ℓ(N)`, `ℓ ≥ 5`, upper | `N exp(−(log log N)^{c_ℓ})`, `c_ℓ ∈ (0, 1)` | Leng–Sah–Sawhney, arXiv:2402.17995 (2024) |
| `r_ℓ(N)`, lower | `N exp(−n 2^{(n−1)/2} (log N)^{1/n} + O_ℓ(log log N))`, `n = ⌈log₂ ℓ⌉` | Rankin (1961), O'Bryant, arXiv:0811.3057 (EJC 2011) |

Nothing is known uniformly in `ℓ` once `ℓ` grows with `k`. Every bound above
has constants that depend on `ℓ` in an unspecified way.

## Proposition 1 (density reduction)

```
W(ℓ, k) ≤ min{ N : r_ℓ(N) < ⌊N/k⌋ }.
```

*Proof.* If `[N] = S ⊔ A` and `A` has no `k`-AP, then `S` meets each of the
`⌊N/k⌋` disjoint windows of `k` consecutive integers, so `|S| ≥ ⌊N/k⌋`. If
`S` also has no `ℓ`-AP, then `|S| ≤ r_ℓ(N)`. ∎

## Proposition 2 (first moment)

If `3 ln N < k` and `N² (3 ln N / k)^ℓ < 1`, then `W(ℓ, k) > N`. In
particular (V_ℓ) holds for every

```
ℓ ≥ ℓ_rand := 2 ln N₀ / ln(k / (3 ln N₀))  ≈  2c k^{1−a} / a.
```

*Proof.* Put each integer in `S` independently with probability
`ρ = 3 ln N / k`. `[N]` has at most `N²/(2(m−1))` progressions of length
`m`. The expected number of `ℓ`-APs in `S` is at most `N² ρ^ℓ / 2 < 1/2`.
The expected number of `k`-APs in `A` is at most
`N² (1 − ρ)^k / 2 ≤ N² e^{−3 ln N} / 2 < 1/2`. ∎

Consequence for the window. Theorem 3 constrains only `ℓ < ℓ_rand`, and
`ℓ_rand` is about `2^{375}` to `2^{3674}` at the 21 points, against
`p₀ ≤ 353`. The cut at `p₀` therefore comes entirely from the **literal**
(II), through `r_ℓ(k) ≥ k/4` for `ℓ ≥ p₀`, and not from Theorem 3.

The exact form (II′) of (II) (track II) does **not** move the cut far.
(II_ℓ) implies (II′) only if `X_P` cannot cover almost a whole color class
of `c₀` on `P`, that is, only if every color class of `c₀` on a rich `P`
contains an `ℓ`-AP. For an arbitrary `c₀`, a class of about `k/2` positions
can avoid `ℓ`-APs as soon as `r_ℓ(k) ≥ k/2`, which is again near `p₀`. For
a `c₀` that behaves randomly on rich progressions, the longest AP inside a
half of `[k]` has length about `2 log₂ k` (1 478 at `k = 2^739`, 8 192 at
`k = 2^4096`), which is not proved for the template's `c₀`. So under (II′)
the useful window extends **at most** to the length beyond which the color
classes of `c₀` on rich progressions must contain an `ℓ`-AP: about
`2 log₂ k` if `c₀` behaves randomly, far below `ℓ_rand`. (Correction of the
referee, radar-cc.)

Above `ℓ_rand`, AP-freeness of `I_X(P)` is compatible with (I) on every
single fibre, and only the global question remains.

## Verdict: open, and exactly what would settle it

### What would close the window

Since `r_ℓ` grows with `ℓ`, one statement covers the whole literal window:

```
(Cl)   r_{p₀(k)−1}(N₀) < ⌊N₀/k⌋   for all large k.
```

By Proposition 1, (Cl) gives `W(ℓ, k) ≤ N₀` for every `ℓ < p₀`, which
contradicts (V_ℓ). In growth form, (Cl) follows from

```
r_ℓ(N) ≤ N (log N)^{−κ}   uniformly in 4 ≤ ℓ ≤ C log log N / log log log N,   with κ > κ*,
κ* = ln(2k) / ln ln N₀ → 1/(1 − a).
```

At the 21 template and source points, `κ*` lies in `[1.11, 1.95]`
(`verify.py`, check 3).

* Green–Tao give `κ = c` for `ℓ = 4` only, with `c` small and not explicit.
  So even the single slot `ℓ = 4` closes only if their exponent exceeds
  `1/(1 − a)`, which is between 1 and 2 for `a < 1/2`. This is not known.
* Leng–Sah–Sawhney give `exp(−(log log N)^{c_ℓ})` with `c_ℓ < 1`. That is
  weaker than every power of `log N`. Proposition 1 then yields only
  `ln W(ℓ, k) ≤ exp((ln Ck)^{1/c_ℓ})`, which is superpolynomial in `k` and
  cannot beat `ln N₀ = k^{1−a+o(1)}`.
* The conjectured Rankin-type truth, `r_ℓ(N) = N exp(−Θ_ℓ((log N)^{1/⌈log₂ ℓ⌉}))`,
  would give (Cl) at once if the constants stay bounded for
  `ℓ ≤ p₀(k)`. Then `ln W(ℓ, k) ≤ (ln k)^{O(log ℓ)} = k^{o(1)}`.

So the window closes under a uniform polylogarithmic bound on `r_ℓ` with
exponent above `1/(1 − a)`. Nothing of this strength is proved, for any
`ℓ ≥ 4`. Proposition 1 uses only density. A closure could also use more
than density, since `S` must meet every `k`-AP and not only the
consecutive windows. No such argument is known.

### What would open it

A necessary condition, for some `4 ≤ ℓ < p₀(k)`:

```
(Op)   W(ℓ, k) > N₀,   which by Proposition 1 forces   r_ℓ(N₀) ≥ ⌊N₀/k⌋.
```

That is, an `ℓ`-AP-free set of density at least `1/k = (log N₀)^{−κ*}` at
scale `N₀`, with `ℓ = O(log log N₀ / log log log N₀)`. The literature is far
from this.

* The best known `ℓ`-AP-free sets (Rankin–Elkin–O'Bryant) have density
  `exp(−E)` with `log₂ E ≥ 60.4` at every point, against
  `log₂ ln(2k) ≤ 11.5`.
* The best known lower bounds on `W(ℓ, k)` for `ℓ < p₀` (Li–Shu, and
  Proposition 2 used at its limit) give `ln W ≈ (ℓ/2) ln k`, that is
  `log₂ ln W ≈ 14.4` to `18.9`. (V_ℓ) needs `log₂ ln N₀ ≈ 382` to `3681`.
  The smallest gap over the 21 points is a factor `2^{367}` in `ln W`.
* Green's and Hunter's constructions exist only for `ℓ = 3`, which is
  already closed.

(Op) is necessary, not sufficient. A real door-1 set would also need:

* (I) on every fibre piece at once, through one set of keys;
* non-saturation;
* (II) on every rich progression, not only those of Lemma E.

### Summary

| `ℓ` | status |
|---|---|
| 3 | closed (Theorem 2 of `ap-free-frozen-sets`, Kelley–Meka / Bloom–Sisask) |
| `4 ≤ ℓ < p₀(k)` | open: closes under (Cl), needs (Op) to open; both far from the literature |
| `p₀(k) ≤ ℓ < ℓ_rand` | not usable under the literal (II); under (II′), usable at most up to the length where every color class of `c₀` on a rich progression contains an `ℓ`-AP (about `2 log₂ k` if `c₀` behaves randomly, not proved), with the same open status there |
| `ℓ ≥ ℓ_rand` | no constraint from Theorem 3 (Proposition 2) |

## What is not claimed

* That the window is closed, or open. Both directions need results about
  `r_ℓ` or `W(ℓ, k)` that no one has.
* Anything about door 1 beyond AP-freeness of `I_X(P)`.
* Anything proved about (II′). The remarks above only locate where the cut at
  `p₀` comes from.
* The literature table is a survey as of the date above, from the cited
  arXiv abstracts and erdosproblems.com/721. It is not a re-proof.

## Checks in `verify.py`

1. Exact values of the split form, by exhaustive search: `W(3,3) = 9`,
   `W(3,4) = 18`, `W(3,5) = 22`, `W(4,4) = 35`, all matching the known
   values.
2. Proposition 2, exactly: at `N = 200`, `k = 120`, `ℓ = 9`, the expected
   number of bad progressions is `3.3·10^{−5} < 1`.
3. Template numerics at the 21 points of `ap-free-frozen-sets` (same model,
   with `N₀ = 2Y₀`): `p₀`, `ℓ_rand`, the known lower bound for `ln W` at
   `ℓ = p₀ − 1`, `κ*`, and the O'Bryant exponent at `n = ⌈log₂(p₀ − 1)⌉`.
   The checks assert that no known lower bound reaches (V_ℓ),
   `p₀ < ℓ_rand`, `1 < κ* < 2`, and that O'Bryant's density stays below
   `1/(2k)`.
