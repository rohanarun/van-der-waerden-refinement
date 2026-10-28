# Optimistic ceilings of templates outside the current one

**Status:** structural research, negative with one conditional exception. No
new bound. The numbers are first-order optimistic ceilings (exponents in units
of `k log k`) of the *oblivious* versions of each template, not theorems about
`W_2(k)`.
**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.
**Depends on:** the obstructions P1 and P3 of the `short-period-sensitivity`
track (PR #14, package `single-label-obstructions`, commit `4e0f252`), which
are not in this tree; publish with or after them.

## Frame

Every known superexponential construction for `W_2(k) > k^{ck}` is a base
coloring `c₀` plus a rare perturbation of rate `p = k^{−b}`. Two first-moment
costs decide it:

* **rich** progressions (`c₀` balanced): monochromatic means changing the
  minority, `Pr ≥ p^{k/2}` when the positions carry distinct units of
  randomness, so `2c ≤ γb` with `γ ≤ 1/2`;
* **structured** progressions (`c₀` constant): they must receive a
  perturbation, `Pr[none] ≈ e^{−pk}`, so their events need entropy
  `H ≪ pk = k^{1−b}`.

Hence `c ≤ (1/4)(1 − log_k H)` for this shape, and **`c > 1/8` needs `H ≪
k^{1/2}`**. The unwritten hypotheses are: one rate `p` for both colors (which
is what makes `γ ≤ 1/2` bind), distinct units of randomness on rich
progressions, and union bounds by sub-prescriptions of each progression. The
exception below escapes through the first one.

## The torus uncertainty principle

On the `D`-dimensional torus (`N = q^D`, `D = k^a`) the structured events of
case (ii) pay for two words, each shown necessary, for union bounds by
sub-prescriptions of each progression with iid flips, by the obstructions P1
and P3 (PR #14):

* the band word, three real coefficients at resolution `q²`:
  `6 log q = 6 log N/D = k^{1−a+o(1)}` (P1, `b < a`);
* the box word, two parameters per coordinate: `(D−1)·log(k²/2) =
  k^{a+o(1)}` (P3, `a + b < 1`).

So, for union bounds by sub-prescriptions of each progression,
`H ≥ log N/D + D log k`, whose exponent `max(1 − a, a)` is at least `1/2`
**for every `a`**: `b ≤ 1/2` is one phenomenon seen from both sides, not two
coincidences. A template beyond `1/8` must break this product (keys whose
slow words cost `o(log N/D)`, or a box/run structure costing `o(D)`), **or
break `γ ≤ 1/2`** by unequal rates (the exception below). Separately, the label
entropy `D^{2−o(1)}` (dilation `λ`) keeps `a < 1/2` (constraint F); dropping
only the box word gains nothing (`b < a ≤ 1/2`).

## Candidates (oblivious versions)

| template | what changes | optimistic system | ceiling |
|---|---|---|---|
| current (PR #7) | — | `b ≤ a`, `a + b ≤ 1`, `a ≤ 1/2`, `2c ≤ b/2` | **1/8** |
| asymmetric flips, rates `p₀ ≠ p₁`, base with a fraction θ of ones | rich progressions pay only the flips of one color | structured progressions of both colors exist (every label cell contains step-1 progressions), so both `b₀, b₁ ≤ 1/2`; `2c ≤ min(θb₁, (1−θ)b₀)` | **1/8** at θ = 1/2 (1/40 at θ = 1/10) |
| asymmetric, **if no structured progression has mostly ones** | `p₁ = 0`: a progression containing a one is never monochromatic 0 | `2c ≤ (1−θ)b₀`, with `b₀ ≤ a`, `a + b₀ ≤ 1` imported from P1/P3 | optimistic **(1−θ)/4 → 1/4** (19/80 at θ = 1/20), under imported constraints |
| fine / coarse split, flips only on a set Σ of density `k^{−s}`, Σ oblivious to the progressions | structured progressions should see Σ densely | step-1 progressions tile `G`, so density(Σ) ≥ min over structured S of `|S∩Σ|/k`; rate seen by both sides `k^{−(b+s)}` | **1/8** |
| one flip per group (covering designs), disjoint groups of size `g ≥ 2` | a deterministic transversal of the slow words | ≤ `#keys/g = q^{2+o(1)}` groups for `q^{6−o(1)}` distinct slow words, each containing O(1) groups: needs `1 − a ≤ a` | infeasible for `a < 1/2` |
| random radii or offsets per box (Green 2022, Hunter 2022), independent between positions | randomness in the geometry | dense: each position of a generic P is an independent fair coin, `Pr[mono] ≥ 2^{1−k}`, `c ≤ log 2/(2 log k) → 0`; sparse: the current template | 0 or 1/8 |
| LCM dilations (Fox–Hunter) | control of rational returns | already the `λ` of the current template | 1/8 |
| finite-field norm colorings (Shi–Dong) | norm colorings with digit-carry control (credited to them upstream, for a related symmetric-progression problem) | not priced: whether they give a 2-coloring of `Z/N` with a first-moment budget is not examined here | not priced |
| iterated products, direct `r`-color templates | more colors | the uniform-in-`r` coefficient is the `r = 2` one; a direct 3-coloring gives `(1−1/r)b/2 → 1/6` for `W_3` only | 1/8 for `r = 2` |

The **adapted** versions of three lines are not covered by these ceilings: a
set Σ chosen to follow the slow progressions, groups of size `g = 1` (a
deterministic transversal), and radii coupled per center (a union of random
annuli). Each falls back either on the structured transversal (Porte 1) or on
the exception below, both open; a union of random annuli is a candidate for
the exception, outside the no-go of the next section.

## The one exception, stated exactly

The asymmetric template has the optimistic ceiling `(1−θ)/4 → 1/4`, under the
constraints `b₀ ≤ a`, `a + b₀ ≤ 1` imported from P1/P3, if there is a set
`A = c₀^{−1}(1)` with

1. **AP-sparse:** every `k`-term progression has at most `θk` points in `A`
   (so monochromatic 1 needs `(1−θ)k` flips, and no progression lies in `A`),
2. **generic hitting:** every progression disjoint from `A` belongs to a
   family whose flip events have entropy `≪ k^{1−b₀}`.

Those imported constraints come from mono-label families that `A` may touch,
so `(1−θ)/4` is a value under imported constraints, not the ceiling of the
exception itself.

No label-based `A` works: a label cell contains step-1 progressions of length
`k`, which would lie in `A`. A random `A` of density `δ` fails (2): `N²`
generic progressions each miss it with probability `(1−δ)^k`, so it needs
`1 − δ ≤ k^{−2c}(1+o(1))`, contradicting (1). The object needed is a **sparse
hitting set of the high-entropy progressions containing no dense part of any
progression**, the dual of the open "structured transversal" (Porte 1: a
sparse transversal of the low-entropy slow words). Both give `1/4`
optimistically, and both are open.

**No-go for one named class.** Suppose `A` is a union of cells of a partition
of the `y`-torus into boxes, the cell colors being chosen at random by a
product measure whose margins lie in `[η, 1−η]` for a fixed `η > 0`, and
`A`'s properties being established by a union bound or a local lemma over
events indexed by cell words, as in the source.

1. *(Cell lemma, cyclic progressions, `C = 1`; proof due to the referee
   session of this sprint.)* The representatives form the lattice
   `Λ = Z^D + Z·u`, `u = (1/q, …, 1/q^D)` (independent of the unit `λ`). A cell
   of widths `≤ 1` lifts to a half-open box `B̃` whose points are `Λ ∩ B̃`. If
   it holds more than `(k−1)^D = [Λ : (k−1)Λ]` points, two of them `x ≠ y` are
   congruent mod `(k−1)Λ`; then `v = (y−x)/(k−1) ∈ Λ`, `0 < max|v_i| < 1`, so
   `v` is a nonzero step, and `x + jv ∈ B̃` for `j < k` by convexity. So every
   1-cell of a `k`-AP-free `A` has `≤ (k−1)^D` points. The bound is sharp: the
   cell `[0, (k−1)/q)^D` holds exactly `(k−1)^D` points and no `k`-AP. This is
   for progressions of `Z/N`; for progressions of integers it fails (a box of
   49 > 36 points without a progression exists at `q = 11, D = 2, k = 7`).
2. *(Entropy.)* A cell of `≤ (k−1)^D` points determines its point up to
   `(k−1)^D`. A generic progression with two points in `A` is therefore fixed,
   up to `(k−1)^{2D}k²`, by its cell word: there are `≥ N^{2−o(1)}` distinct
   words, and `≥ N^{1−o(1)}` through any one 1-cell. Under margins in
   `[η, 1−η]`, every event about the colors of `≤ k` cells has probability
   `≥ η^k = e^{−O(k)}`, so both the union bound and the local-lemma condition
   (incident weight per cell `≪ 1`) fail, since `log N = ck log k ≫ k`.

The margin restriction is needed: with margins `1 − k^{−β}`, a generic
progression crossing `m ≤ θk` such cells misses `A` with probability
`≤ k^{−βm}`, which pays the entropy `2ck log k` once `β ≥ 2c/θ`. That biased
case is close to a deterministic choice. What survives is a deterministic,
algebraic or strongly biased choice of `A`, outside the class. Bohr sets are
one convex cell and fall under 1. Band-level sets `{n : band(n) ∈ Λ}` have
cell words of entropy `≈ 2 log N` on generic progressions, so only a
deterministic hitting theorem for pseudo-random band sets could serve; none is
known.

Equivalently, the exception asks for an outer coloring whose monochromatic
progressions are **all of color 0** and all in a family of event entropy
`≪ k^{1/2}`: color 1 must be `k`-AP-free (indeed `θ`-sparse on every
progression) while still meeting every non-structured progression. The
current outer coloring has monochromatic structured progressions of both
colors (one per label cell), which is exactly what pins the two rates to the
same `k^{−1/2}`. Three further obstructions, all heuristic:

* **tiling:** step-1 progressions tile `G`, so some structured progression sees
  `A` at least at its global density; a set denser on generic progressions than
  on every structured one does not exist;
* **deterministic hitting** of all `N²` generic progressions is only available
  through a local lemma over low-entropy label words, i.e. coarse cells, which
  contain whole progressions; finer structure is random-like on generic
  progressions, and a random-like `A` of density `μ` misses `N²(1 − μ)^k ≫ 1`
  of them unless `1 − μ ≤ k^{−2c}(1+o(1))`;
* **geometric regions** `A = ỹ^{−1}(R)`: AP-freeness forbids `R` from
  containing an orbit that is slow in any subset of coordinates (cylinders,
  slabs, small boxes all fail), while `k ≪ 2^D` points cannot equidistribute
  in dimension `D = k^a`, so no discrepancy argument forces every generic orbit
  into a thin `R`.

## Remark (consolidation)

Fox–Hunter (Theorem 2, cited in the upstream introduction): for every fixed
`ε ∈ (0,1)` and `k` sufficiently large in terms of `ε`, `W_r(k) ≥
r^{(1−ε)k log k}` for `r ≥ (log k)^{3/ε}`, i.e. a coefficient `(1−ε) ln 2` in
the normalization `k^{ck⌊log₂ r⌋}`, already `ln 2/2 ≈ 0.35` at `r ≥ (log k)^6`.
The uniform-in-`r` statement is pinned by small `r`.

## Reproduce

```sh
python3 -B verify.py
```

Expected: `OK: all checks pass and match RESULT.json` (standard library,
under a second). Each optimistic system is solved exactly by vertex
enumeration in Fractions. Negative controls: dropping `b ≤ a`, or both
`a ≤ 1/2` and `a + b ≤ 1`, must give `1/4`, and dropping only one of the
latter must give `1/8`. With `s` pinned at `1/4`, the fine/coarse model keeps
`1/8` while its mutation (rich side paying `b` alone) drops to `1/16`. The cell
lemma is checked exactly at `(q, D, k, λ) = (13, 3, 4, 1)`, `(13, 3, 4, 5)` and
`(31, 2, 5, 7)`: 12 random fine boxes (widths `1/q` to `2k/q`) above the
threshold `(k−1)^D` each, down to 28 points against 27, with steps `d ≠ 1`;
the pair congruent mod `(k−1)Λ` is found and its progression checked. The
tight box `[0, (k−1)/q)^D` is checked to hold exactly `(k−1)^D` points and no
`k`-AP.

Lean: item 1 of the no-go (the cell lemma, `C = 1`) is formalized as
`cyclic_cell_lemma` in `lean/` (Lean 4.21, Mathlib v4.21.0, as PR #10), the
`k` terms distinct in `Z/N`; the sharpness and item 2 are not. Build and
axioms in `lean/evidence/`: `cd lean && lake build && lake env lean Axioms.lean`.

## Scope

First-order optimistic costs only: lower-order terms, local-lemma weights and
the outer-coloring construction are not modeled. A ceiling `≤ 1/8` here means
that the favorable budget of the oblivious version does not pass `1/8`; the
adapted versions listed after the table reduce to Porte 1 or to the exception.
"No candidate found" is not an impossibility theorem, and the exception is
open, not refuted.
