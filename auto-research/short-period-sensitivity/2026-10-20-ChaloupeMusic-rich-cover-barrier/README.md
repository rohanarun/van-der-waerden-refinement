# Rich-side barrier for cover bounds: c ≤ b/4, conditional on a rank statement (G♭)

**Status:** research note (conditional barrier, with exact certificates and a
scoped measurement). The hypothesis is weakened to (G♭), whose small-set half
is proved; its dense-set half is open. Not a new bound, and not a statement
about van der Waerden numbers: it is about what a family of proofs can show.
**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, on top of the
`short-period-sensitivity` track (`2026-10-20-erwan-binding-lever`).

## Question

In the short-period region the coefficient enters only through the rich
condition `2c < γb` with `γ < 1/2`. Can the rich side give more, for the
keys of the construction (V-box, `⌊‖qỹ‖²⌋`), by counting fewer than `N²`
rich events?

Every rich estimate in this repository (source, #4, #6, #7) is a **cover
bound**: a family 𝒢 of key sets such that every rich `(P, β)` has some
`G ∈ 𝒢` inside its minority key set `F_{P,β}`, and
`Pr[some rich P mono] ≤ Σ_𝒢 p^{|G|}`.

## Result

1. **Duality (rigorous, trivial).** If a probability measure ν on rich
   `(P, β)` satisfies `ν(F ⊇ S) ≤ p^{|S|}` for every nonempty key set `S`,
   every cover costs at least 1.
2. **Small sets (rigorous).** Take ν uniform on ≥ N²/4 non-short-period
   progressions **without a repeated V-box**, with β the majority color
   (`|F| ≤ k/2`). The restriction matters: the covers of this repository only
   cover coherent events (#4, § 5: "first discard F ∩ Z ≠ ∅", and likewise
   #6, #7, #9), and a key repeated at a minority and a majority position makes
   `(P, β)` empty, so such a cover may skip it. Without a repeated box no key
   repeats, every `(P, β)` in the support is coherent, and every cover of the
   repository must cover it. Few progressions are lost: a box repeated at gap
   `g < k` forces `‖ỹ(gd)‖_∞ ≤ 2H`, hence at most `(4q/k² + 1)^D` values of
   `gd`, hence of `d` (`g` is invertible), so at most `kN²(4/k² + 1/q)^D =
   o(N²)` progressions. On this support the bound holds for
   `|S| = 1` (box fibre ≤ `Π(q|I_i| + 1)`) and for `2 ≤ |S| < s₀`,
   `s₀ = ⌊(4 − 2/log k)D/b⌋` (two keys, two positions, two fibres).
3. **Linear rigidity is false (exact certificate).** Treating
   `Θ = (|A|², ⟨A,B⟩, |B|²)` as free, the band at position `t` is linear in
   `z = (A, B, Θ)` with integer row `r_t = (−2w_t, −2t w_t, 1, 2t, t²)`. One
   would like any `O(D)` rows to have full rank. They do not: by pigeonhole on
   the `2^D` sums `⟨g′,B⟩`, `g′ ∈ {0,1}^D`, some `g ∈ {−1,0,1}^D` has
   `|⟨g,B⟩| ≤ D2^{−D}`; when `2^D > Dk`, `⟨g, w_t⟩` takes ≤ `D+2` values, and
   on a level set `J_m` (≥ `k/(D+2)` positions) the vectors
   `(ug, vg, 2um, vm, 0)` annihilate every row. `verify.py` certifies this
   exactly (`D = 12, k = 300`: 138 positions of rank ≤ 25). This does **not**
   refute spread: with the true constraint `Θ = Θ(A,B)`, the band moves at first
   order by `2(u + vt)⟨φ_t, g⟩` along that direction, and `⟨φ_t, g⟩` is
   linear in `t` and vanishes at most once (checked).
4. **Tube lemma (rigorous).** Fix `s₀` keys, their positions and wrap vectors
   in `P′`; let `d = 2D + 3 − rank(r_t)`. At most `(1 + 4q√D)^d` progressions
   fit. Proof: by Cauchy–Binet, `Π σ_i² = det(M_ρ M_ρᵀ) ≥ 1`, with
   `σ₁ ≤ 2nk²`, so `σ_ρ ≥ (2nk²)^{−n}`; the solutions lie within
   `τ ≤ 1/(4q)` of an affine subspace of dimension `d` (because `a < 1/2`);
   points of the lattice `Λ² = {(ỹ(n₀), ỹ(d))}` are `1/q`-separated (sup
   norm, separation lemma of the source), so after projection they are
   `1/(2q)` apart in a ball of radius `√(D/2)` (circumscribing the cube),
   and packing gives `(1 + 4q√(D/2))^d ≤ (1 + 4q√D)^d`.
5. **Proposition (rigorous reduction).** Let `a < 1/2`, `0 < b < 1`,
   `c > b/4`, `θ < 2 − b/(2c)`. Assume
   > **(G_θ)** there are ≥ N²/4 non-short-period progressions without a
   > repeated V-box such that, for each one and every set `J` of `s₀` positions,
   > `rank(r_t : t ∈ J) ≥ 2D + 3 − θD`.

   Then for large `k` every rich cover costs ≥ 1. No full rank is needed:
   a deficit of a fixed fraction of `D` is tolerated. For `|S| ≥ s₀` the
   count is `k^{s₀}(k+2)^{Ds₀}(1 + 4q√D)^{θD}`, whose logarithm is
   `O(k^{2a} log k) + θck log k`, below `(2c − b/2)k log k`.

So the rich-side barrier `c ≤ b/4 = γb/2` at `γ = 1/2` holds for every cover
bound with these keys (covering at least the coherent rich events, as all
covers of this repository do), **conditional on (G_θ)**, a purely combinatorial
statement about Beatty vectors `w_t = round(A + tB)`. The only deficit
mechanism found is that of Dirichlet: `r` vectors `g` costing `2r` on a
common level set, which shrinks by ≈ 0.5–0.7 per added `g`. On `s₀` positions
that predicts `O(log k)`, far below `θD = θk^a`.

## A weaker sufficient hypothesis (Proposition 5′), and what of it is proved

(G_θ) asks for near-full rank on **every** set of `s₀ ≈ 4D/b` positions. The
proposition needs much less: near-full rank only on **dense** sets of
positions (`|J| ≥ δk`), and on smaller sets a rank that grows linearly with a
tiny slope. The small-set part is proved below; the dense part is open.

Write `rank_J(P)` for the rank of the rows `r_t`, `t ∈ J`.

1. **Integer relations (rigorous, elementary).** The rows are integer
   vectors, so their real null space has a rational basis: every rank deficit
   comes from integer relations `Σ_i (x_i + t y_i) w_{t,i} = c₀ + c₁t + c₂t²`
   on `J`. Moreover, with `V = span(w_{·,1}|_J, …, w_{·,D}|_J, 1, t) ⊂ R^J` and
   `T = diag(t)` (after the translation `t → t + 1`, which leaves the rank
   invariant and makes `T` injective), the column space is `V + TV`, hence
   `2D + 3 − rank_J = 2d₁ − 1 + dim(V ∩ TV)`, where `d₁ = D + 2 − dim V` counts
   the relations `⟨g, w_t⟩` affine in `t` on `J` (`g ∈ Z^D`, any height) and
   `dim(V ∩ TV) ≥ 1` (it contains `t`). Pure relations cost exactly 2 each;
   mixed ones are measured by `dim(V ∩ TV) − 1`. Neither term is bounded here
   on dense sets.
2. **Counting wrap patterns by faces (rigorous).** For `t` in a set `J₀` of
   `σ` positions, `w'_{t,i} = ⌊A'_i + tB'_i + 1/2⌋` depends only on the face of
   `(A'_i, B'_i)` in an arrangement of at most `σ(k+4)` lines of the plane.
   Hence at most `(4σ²(k+4)²)^D` wrap patterns, instead of `(k+2)^{Dσ}`: the
   cost is `O(D log k)` whatever `σ`.
3. **Larger `S₀` (rigorous).** In regime 3 take `S₀ ⊆ S` of size
   `σ = min(|S|, ⌊δk⌋)`. Positions cost `k^σ ≤ k^{δk}`, which is
   `δ k log k`, and the bound must beat `p^{|S|}`:
   `4 k^σ (4σ²(k+4)²)^D (1 + 4q√D)^{d} / N² ≤ k^{−b|S|}`.

> **Proposition 5′.** Let `a < 1/2`, `0 < b < 1`, `c > b/4`, `δ > 0` and
> `θ < 2 − (δ + b/2)/c`. Assume
> **(G♭)** there are ≥ N²/4 non-short-period progressions without a repeated
> V-box such that, for each one,
> (i) `rank_J ≥ 4 + ⌊(1+b+δ)|J|D/(ck)⌋` for every `J` with `s₀ ≤ |J| < ⌊δk⌋`;
> (ii) `rank_J ≥ 2D + 3 − θD` for every `J` with `|J| = ⌊δk⌋`.
> Then for large `k` every rich cover costs ≥ 1.

*Proof.* Regimes 1–2 are unchanged. For `s₀ ≤ |S| < δk`, take `S₀ = S`; with
`D log q ≥ ck log k`, the deficit `2D − 1 − ⌊(1+b+δ)σD/(ck)⌋` leaves a margin
`≥ min(δ/(1+b+δ) · log q, δσ log k) − O(D log k) > 0`, because
`log q ≫ D log k` when `a < 1/2`. For `|S| ≥ δk`, take `|S₀| = ⌊δk⌋` and the
worst `|S| = k/2`: the logarithm is `(θ + (δ + b/2)/c) D log q + O(D log k)`
against `2D log q`. ∎

(G_θ) implies (G♭) for `δ` small (rank is monotone in `J`, and
`2 − θ > b/(2c)`), so Proposition 5′ is a strict weakening of the hypothesis.

4. **Lemma (rank ≥ 4, rigorous).** `rank_J = 3` with `|J| ≥ 4` forces every
   coordinate to be affine on `J`: `w_{t,i} = α_i + β_i t`. Then `gβ_i ∈ Z` for
   `g = gcd(J − J)`, and `|B_i − β_i| · g(|J| − 1) < 1`, so
   `‖ỹ(gd)‖_∞ < 1/(|J| − 1)` with `g ≤ k/(|J| − 1)`. By the box-fibre bound and
   `gcd(g, N) = 1`, such `d` are at most `(k/s₀)(2q/(s₀−1) + 1)^D`, a
   fraction `≤ (k/s₀)(2/(s₀−1) + 1/q)^D = o(1)` of all progressions. Removing
   them, `rank_J ≥ 4` for every `|J| ≥ s₀`, which is all that (i) asks for
   `|J| ≤ σ₄ = ck/((1+b+δ)D)`.

So (i) is **proved** on `s₀ ≤ |J| ≤ σ₄` (sets of up to `≈ k^{1−a}`
positions). What remains open is (i) on `σ₄ < |J| < δk` and (ii): a deficit
`≤ θD` on sets of `δk` positions, for every fixed `θ > 0` if the barrier is to
sit at `b/4` (a fixed `θ₀` would only give `c ≤ (δ + b/2)/(2 − θ₀)`). No
union over `J` can prove it: the columns `w_{·,i}|_J` are independent across
`i`, but a single column falls in a given subspace with probability
`≥ k^{−2+o(1)}` (constant and step patterns), while there are
`binom(k, δk) = e^{Θ(k)}` sets. A structural statement is needed: for typical
`(A, B)`, every rational subspace of relations of dimension `θD` has a common
zero set of fewer than `δk` positions (a contraction `ρ < 1` per independent
relation, uniform in the height of `g`).

Note also that `ν` may live on any family of density `ε ≥ k^{−ηD}`, `η < 2`:
regimes 1 and 3 absorb `log(1/ε) = O(D log k)`, and regime 2 holds up to
`(4 − η − o(1))D/b`. (G♭) may thus be proved for a structured family of
`B`. Pinning `B` to a box of side `k^{−3}` (`ε = k^{−3D}`) also works if one
counts inside the family: a key then fixes `A` to a box, so regime 1 holds,
and two keys give `k²(2/k²)^D`, so regime 2 holds up to `≈ 2D/b > 2D + 3`.
(G♭) is then a statement about a single `B`. We did not find a `B` for which
(ii) is easier. One period with `D` phases (`B_i ≈ 1/r`, `r < k`) fails it:
on `J = {t : t mod r < δr}` the columns depend on `t mod r` through `≈ δD`
thresholds only, so `rank_J ≤ 2δD + O(1)`.

## Measurement of (G_θ) (scoped)

| progression | D | k | s₀ | deficit |
|---|---|---|---|---|
| affine, no coordinate wraps (positive control) | 8 | 400 | 40 | 16 = 2D |
| quasi-affine, 3 wrapping coordinates (positive control) | 8 | 400 | 40 | 10 = 2(D−3) |
| generic, seed 13: worst searched / 20 random sets | 8 | 400 | 40 | 5 / 0 |
| generic, seed 14 | 8 | 400 | 40 | 6 / 0 |

Domain: progressions with `A, B` drawn from dyadic rationals of denominator
`2^30`. Searched sets: intersections of the most frequent level sets of
`⟨g, w_t⟩` for the 40 best `g ∈ {−1,0,1}^D` (smallest `|⟨g,B⟩|`), up to 6
vectors, truncated to `s₀`. Stopping rule: 400 sets per level. Rank exact
modulo `2^61 − 1` (a lower bound for the rational rank, so an upper bound
for the deficit). Coverage: not exhaustive, and `D ≤ 8` is far from
`D = k^a`. "No worse deficit found" is not a proof. The positive controls
show the measurement does see clusters where they exist.

A brute force at small `q` would not test the right regime: with `q ≲ 400`
and `D ≤ 3` there are more keys than elements, whereas everything hinges on
`#keys = N^{o(1)}`.

## Reproduce

```sh
python3 -B verify.py
```

Expected: `OK: all checks pass and match RESULT.json` (≈ 12 s, standard
library only). It replays: the exact Dirichlet certificate (three instances),
the first-order check, the four deficit measurements, on small instances the
fibre bound, the `1/q` separation and the Gram determinant ≥ 1, and the
three regimes of the proposition (with the `1/q` terms kept) and the
repeated-box fraction at `a = 49/100, b = 97/200, c = 13/100,
θ = 13/100, k = 10^400` (margin `6·10⁻⁴` in units of `k log k`, which is
`2c − b/2 − θc`). Check 6 replays Proposition 5′ at the same point with
`δ = 1/2000`: (i) on a dyadic grid of `|J|` from `s₀` to `δk`, (ii) at
`|J| = δk` (margin `10⁻⁴`), the threshold `σ₄ = ck/((1+b+δ)D) ≈ 0.6732 ck/D`
up to which (i) asks only rank 4, and the rank-3 exception fraction
(`< 10^{−1.9·10^{198}}`).

## What is not claimed

No lower or upper bound on `W_r(k)`. (G_θ) is open, and so is the dense-set
half of (G♭) (part (ii), and part (i) beyond `σ₄`). The barrier only
concerns cover bounds with these keys. A failure of (G_θ) would be good
news: it would yield cheaper rich covers.
