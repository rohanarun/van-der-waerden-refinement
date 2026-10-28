# Track: structured-flips

Goal: replace the iid flips of the current template, on part of the keys, by a
deterministic set `X` of frozen keys (`c₁ = c₀ ⊕ 1_X`, iid flips elsewhere),
so that the short-period case (ii) stops costing `b < a`. The team's
reduction asks for two conditions. (I): `X` meets every case (ii) key word on
its dominant color without saturating it, so that `ω(k^{1−a})` dominant keys
stay outside `X`. (II): `X` puts at most `εk` keys on any rich progression.
Under these, every `c < 1/4` would follow. This is the only known route past
`1/8` with the current keys (Porte 1).

Open questions:

* an admissible `X` (meeting without saturating) that passes (I) on the whole
  single-label family at key density `k^{-1/2-δ}`, not only on the `e = 1`
  family;
* the minimal density of a set meeting every `k`-AP of `[Y]` when
  `log Y = k^{Θ(1)}`: a power of `k` below `log Y / k` would be needed;
* a dense `X` (density `k^{-a}`) whose large deviations on rich progressions
  beat those of a random set.

Related: `template-ceilings` (the dual, asymmetric flips), the
`short-period-sensitivity` contributions on `P1`, `P2`, `P3` (open PRs), and
`barrier-note.md`.

## Index

| Date | Handle | Result | Status | PR |
|---|---|---|---|---|
| 2026-10-20 | ChaloupeMusic | Exact lens identity on single-label blocks. A residue rule meets, without saturating, every block of the `e = 1` family (the one behind the iid obstructions) at key density `O(log k/√k)` (`b_X → 1/2 > a`), but is constant on blocks with `ℓ \| e`. The exact shifted family `x² + u²` makes every rule of this kind constant on some block. (I) reduces, fiber by fiber, to `k`-AP hitting sets in `[q^{1-o(1)}]` | structural research (partial positive, negative, reduction) | – |
| 2026-10-20 | ChaloupeMusic | Every flip rule built from band residues (`band mod L0` and memberships `band mod ℓ ∈ T_ℓ` with each `T_ℓ` square-blind or sparse, any truth table) leaves some single-label blocks either saturated (monochromatic for every draw) or untouched, for moduli up to about `q/(1536k³)`; this covers periodic rules, CRT unions, the non-residue character and sparse polynomial conditions | structural research (negative, class closed) | – |
| 2026-10-26 | ChaloupeMusic | Deterministic AP-sparse frozen sets. Every pattern of a single-label fibre piece embeds, at indices `0, h, 2h, …`, into a rich progression (Lemma E). Hence (I) plus "no ℓ-AP in `I_X(P)` for rich `P`" forces the piece length below `W(ℓ, k)`. For `ℓ = 3` this is impossible for `k` large (Kelley–Meka): no `X` satisfying (I) keeps `I_X(P)` 3-AP-free on every rich `P` (the reading in which Behrend, Salem–Spencer or Elkin sets would give (II)), and no band rule forbidding the quadratic triple (Q) satisfies (I). Band-side 3-AP-free sets are closed only conditionally (flatness of fibre weights). `ℓ ≥ p₀(k) = O(log k/log log k)` cannot give (II); `4 ≤ ℓ < p₀(k)` reduces to an open off-diagonal van der Waerden bound that every known construction misses | structural research (negative on the index side; band side conditional; one window reduced) | – |
| 2026-10-26 | ChaloupeMusic | Choosing `X` by a local lemma after freezing gains nothing on the exponent scale. Any criterion that reads only the event-variable incidence and the marginals (asymmetric LLL, Shearer, cluster expansion, Moser-Tardos, variable-version LLL) needs total probability `< 1` through every random key, so `Σ_rich μ(B_P) < 4\|𝒦\|/k = N^{o(1)}`: a first moment. Uniform laws stay at `c ≤ 1/8` (for `b ≤ 1`); beyond, a certificate contains a deterministic set doing door 1's job up to `N^{2−Ω(1)}` rich exceptions. The obstruction is intrinsic, not N3's granularity. Large-modulus band rules: dense ones fail the literal (II) at every modulus (density lemma), and the exact (II) is restated (X_P must not lie inside either colour class); every rule has exactly the random second moment along progressions; the affine rich progressions (including a family with bands `(a+j)²`) carry only `e^{o(k log k)}` key words, too few to refute a sparse rule | structural research (negative for local-lemma certificates and dense rules; sparse large-modulus rules left open) | – |
| 2026-10-26 | ChaloupeMusic | The index-side window `4 ≤ ℓ < p₀(k)` of `ap-free-frozen-sets` is open both ways: it closes under `r_{p₀−1}(N₀) < N₀/k` (a polylog bound on `r_ℓ` with exponent above `1/(1−a)`, uniform in `ℓ ≤ p₀`), and opening it needs `ℓ`-AP-free sets of density `1/k` at scale `N₀`, a factor `2^{367}` beyond known constructions in `ln W`; the cut at `p₀` comes from the literal (II) only, and Theorem 3 is vacuous for `ℓ ≥ ℓ_rand ≈ k^{1−a}` | research note (literature state, reduction) | – |
| 2026-10-26 | ChaloupeMusic | Exact form of Door 1: the event `X_P` inside one colour class and covering all but `θk` of it (minority **or majority**); (I) and (II′) are one condition, "split or leave enough to flip", with different thresholds, plus a mild case (i) clause that (I) + (II) had left out; (I′) + (II′) give every `c < θb/2` for **every** `b > 0` (no ceiling on `b` from the reduction; `1/4` is `b = 1`); splitting every progression is the whole van der Waerden problem; the first moment of a random-like `X` certifies nothing beyond `c < b_X/4`. Closures re-read: only the dense-rule closure falls | structural research (exact condition, closures ledger) | – |
