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
