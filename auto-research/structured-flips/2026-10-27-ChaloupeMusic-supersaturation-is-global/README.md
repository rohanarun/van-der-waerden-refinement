# Supersaturation for Door 1 needs a large range of witnesses

**Status:** structural research, with proofs and exact checks. It is about step (S) of
`2026-10-27-ChaloupeMusic-key-measurable-colorings`. (S) says that every set of keys `Y` that properly
colours the slow words contains an induced class of some rich progression, with a multiplicity close to
the random count. Three facts constrain any proof of (S). They concern the **range** of an argument, the
set of all rich progressions it may ever produce as witnesses, over all `Y`. A witness chosen adaptively,
depending on `Y` (as P1a chooses its line), is allowed. Only the range must be large. No proof of (S), no
closure and no new bound is claimed.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, through `pr/door-one` (`00375ff`) and the
note `key-measurable-colorings` (this PR).

## Setting

As in `key-measurable-colorings`: `c₁ = c₀∘L ⊕ 1_Y∘κ` for a set of keys `Y`. `Y` is **proper** when no
slow progression is monochromatic under `c₁`. By Proposition 3 there, a rich `P` is monochromatic in `β`
exactly when `Y_P = {c₀ ≠ β} ∩ P`; call that an **induced class** of `P`. A key occupies at most two
positions of a progression (Lemma 3 of `source-only-1-16`), so every progression has at least `k/2`
distinct keys.

## Results

**Proposition 1 (small families never witness (S)).** Let `𝓕` be any family of rich progressions, and let
`π_slow` be the probability that a uniform random `Y` is proper. If `|𝓕| · 2^{1−k/2} < π_slow`, some proper
`Y` has no induced class on any member of `𝓕`. By Proposition 2.2 of `key-measurable-colorings`,
`π_slow = 1 − o(1)`, so every family with `|𝓕| <= 2^{k/2−3}` qualifies once `k` is large.

*Proof.* For a fixed `(P, β)`, an induced class asks `Y` to take one prescribed value on each of at least
`k/2` distinct keys. Under the uniform law this has probability at most `2^{−k/2}`. Two targets and a union
bound over `𝓕` give expected count at most `|𝓕| 2^{1−k/2}`. So `P(proper and no induced class on 𝓕) >=
π_slow − |𝓕| 2^{1−k/2} > 0`. ∎

**Corollary 1′ (adaptive arguments).** Suppose an argument assigns to every proper `Y` a rich progression
`P(Y)` carrying an induced class, chosen in any way that depends on `Y`. Its range
`𝓖 = {P(Y) : Y proper}` has more than `2^{k/2−3}` members for `k` large. Otherwise Proposition 1, applied to
`𝓕 = 𝓖`, gives a proper `Y` with no induced class on `𝓖`, and `P(Y)` would be in `𝓖`. Proposition 1 alone
bounds a family fixed in advance. The corollary bounds the range of an adaptive choice. It does **not**
bound what one draw of `Y` looks like: over all lines, a uniform `Y` has about `N q 2^{1−k}` induced
classes on line progressions, a number that tends to infinity. So an argument that looks for its line
depending on `Y` is not excluded.

**Proposition 2 (a line carries too few progressions).** For `r ∈ ℤ/N`, the progressions of `ℤ/N` contained
in the line `r + q^{D−1}ℤ` number at most `q^2`, and `2 ln q = 2ck^{1−a} ln k (1 + o(1))`, which is
`o(k)`. So every family inside a **fixed** set of at most `2^{k/2−3}/q^2` lines satisfies Proposition 1,
and so does the range of any argument whose witnesses stay in such a fixed set. This includes:

* the rich progressions produced by Lemma E of `ap-free-frozen-sets` from one **given** fibre piece, which
  all lie on the line of that piece (`n₀ = r + q^{D−1}m`, `d = q^{D−1}e`);
* any argument run inside a bounded number of given fibre pieces, or of given lines.

It does not include an argument that picks its piece or its line depending on `Y`. Its range runs over all
lines, `N/q` of them, which is more than `2^{k/2−3}/q^2`.

*Proof.* A progression inside the line has `n₀ ≡ r` and `d ≡ 0` modulo `q^{D−1}`: `q` choices for each.
Then `ln q = ln N/D = ck ln k/D` with `D = k^{a+o(1)}`. ∎

**Proposition 3 (where (S) can hold at all).** For every `c` in the template's region below `1/8`, and
every outer colouring `c₀` produced by the template's local lemma (all three families), some proper `Y` has
**no** induced class anywhere. This follows directly from Theorem 1 of `key-measurable-colorings`: below
`1/8` the template gives a good member of `𝒞(c₀)`. Like that theorem, this inherits the conditional status
of the template (`c < 1/8` rests on the source's lemmas). In detail, the template's theorem (`source-only-1-8`, Theorem 9 with §7 of
`source-only-1-16`) gives, with positive probability, a coloring `c₀∘L ⊕ 1_F∘κ` without monochromatic
progressions, where `F` is the set of flipped keys. Then `Y = F` is proper and has no induced class
(Proposition 3 of `key-measurable-colorings`). Since (S), read as a closure, must hold for every such
`c₀`, it can only hold for `N >= k^{(1/8 + ε)k}`. Below `1/8` its multiplicity version fails in the
strongest way, with zero induced classes.

## What this says about (S)

* **The range of a proof of (S) is large.** Its possible witnesses number more than `2^{k/2−3}` rich
  progressions (Corollary 1′). One line carries `q^2 = e^{o(k)}` of them (Proposition 2), so the range
  meets more than `2^{k/2−3}/q^2` lines, or uses progressions that no line contains.
* **Fixed local arguments cannot decide (S); adaptive ones are not excluded.** An argument confined to
  a given fibre piece, or to a given set of fewer than `2^{k/2−3}/q^2` lines, cannot force an induced
  class: a uniform proper `Y` avoids all of them. An argument that first locates a line or a piece from
  `Y`, as P1a's Theorem 2 locates a 3-AP inside `S_J` and then uses Lemma E, has a range over all lines,
  and this note says nothing against it. The route this leaves open is the P1a route: show that every
  proper `Y` has, somewhere it chooses, a local structure that forces an induced class. It must then deal
  with exact equality `Y_P = {c₀ ≠ β} ∩ P` on all `k` positions, where P1a only places three keys.
* **The multiplicity in (S) must be counted over a large range.** On any family of fewer than `2^{k/2−3}`
  rich progressions fixed in advance, the count can be zero.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-supersaturation-is-global/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, JSON summary equal to `RESULT.json`.
Standard library only, exact rationals, a few seconds.

## Checks in `verify.py`

1. The per-progression bound, exhaustively on random toys (`k <= 8`, up to 6 keys, multiplicity at most 2):
   under a uniform `Y`, `P(Y_P = prescribed)` is exactly `2^{−#distinct keys} <= 2^{−k/2}`, or `0` when a key carries both colours.
2. The line count: for toy moduli `N = q^D`, the progressions inside `r + q^{D−1}ℤ` are exactly `q^2`.
3. The scale comparison `2 ln q < (k/2 − 3) ln 2` at the 18 template points of `ap-free-frozen-sets`
   (`D = ⌈k^a⌉`, `ln q = ck ln k/D`), with the margin in `log₂` (at least 212).
4. A toy line: for `q = 37` and `k = 13`, where `q^2 · 2^{1−k} < 1`, a uniform colouring of `ℤ/q` has no
   monochromatic `k`-AP with positive probability. The exact expectation is computed, and one explicit good
   colouring is found and checked.
5. Negative controls: the bound read in positions (`2^{−k}`) fails on a multiplicity-two toy, and dropping the
   step condition `d ≡ 0` counts `qN` progressions starting on the line, all but `q^2` of which leave it.
