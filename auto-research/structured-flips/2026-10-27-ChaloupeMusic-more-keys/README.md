# More keys for X: what a refinement of the key map buys and costs

**Status:** structural research, negative, with proofs. Door 1 asks for a
frozen key set `X`, and the source's keys give `X` only `N^{o(1)}` bits. This
note asks what changes if the key map is refined so that `X` gets `N^{Ω(1)}`
bits. The answer depends on which layer is refined. Refining the flip layer
is fatal for every `p`. Refining only the `X` layer costs a factor `2^k` on the
non-rich union bound and changes nothing on the rich side. It makes a random
`X` fail with high probability, and it leaves Door 1's per-fibre requirement
on single-label blocks unchanged. Whether that requirement blocks Door 1 is
open (steps (D) and (S) of `2026-10-27-ChaloupeMusic-key-measurable-colorings`).
No new bound is claimed, and no `c > 1/8`.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, through
`pr/door-one` (`00375ff`).

**Sources:** the frozen-key reduction and Theorem 2 of
`2026-10-26-ChaloupeMusic-exact-door-one-condition` (this track), Theorem 1
and Lemmas A–C of the single-label obstructions note (PR #14, radar-99),
Lemma R of `2026-10-20-ChaloupeMusic-single-label-lenses` (this track),
Proposition 5′ and (G♭) of the rich-cover barrier (PR #21), and § 2 of
radar-7b's `piste-C` note (not in this tree). See `NOTICE.md`.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-more-keys/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and a JSON
summary equal to `RESULT.json`. Standard library only, under a second.

## Setting

`κ` is the source key map, `κ(n) = (V-box of ỹ(n), ⌊‖qỹ(n)‖²⌋)`. A
**refinement** is a map `κ_f` with `κ_f(n) = κ_f(n′) ⇒ κ(n) = κ(n′)`. Write
`F_f` for its largest fibre, so `|κ_f(ℤ/N)| ≥ N/F_f`. "`N^{β}` bits for `X`"
means `F_f ≤ N^{1−β}`. Everything below holds in the scope of Lemma C of the
single-label note, `λ ≤ q/(400k³)`. This includes the whole short-period
region `a < 1/2`, which is where Door 1 lives.

Two designs:

* **One layer:** the flips and `X` both live on `κ_f`.
* **Two layers:** the iid flips stay on `κ`, and `X` is a set of fine keys.
  A position `n` is frozen when `κ_f(n) ∈ X`. It then ends at
  `c₀(n) ⊕ 1`. Otherwise it ends at `c₀(n) ⊕ E_{κ(n)}`.

The count that governs everything is
`K(κ_f)`, the largest number of single-label blocks (Lemma C, step `e = 1`)
with pairwise disjoint `κ_f`-key sets. Write `κ = log_k ln K` for its
exponent. (The Greek letter is overloaded with the key map only in this one
sentence: from here on, `κ` with no argument is this exponent.)

## 1. How many independent single-label blocks a refinement creates

**Lemma G.** A family `𝓑` of position-disjoint blocks of `k` positions has a
subfamily with pairwise disjoint `κ_f`-key sets of size at least
`|𝓑| / (k(F_f − 1) + 1)`.

*Proof.* Greedy. A block shares a key with at most `k(F_f − 1)` other
positions, hence with at most that many other blocks. ∎

**Corollary G.** `K(κ_f) ≥ N / (20k · (k(F_f − 1) + 1)) ≥ N/(20k² F_f)`.
For the source keys, `K(κ) ≥ (k²/2 − 4)^{D−1} q/(20k)` (Theorem 1 of the
single-label note). So `ln K(κ) ≥ (c − o(1)) k^{1−a} ln k`, and
`κ ≥ 1 − a > 1/2` for **every** refinement. With `N^{β}` bits,
`ln K ≥ βck ln k − O(ln k)`, which is far above `k ln 2`.

*Proof.* Lemma C applies to every low part `r ∈ [0, q^{D−1})`. It gives at
least `q/(20k)` blocks per `r`, all with constant full label, whose positions
`r + q^{D−1}m` are pairwise distinct. So `|𝓑| ≥ N/(20k)`, and Lemma G gives
the rest. ∎

On a single-label block, `c₀` is constant **whatever the outer coloring**,
and its `k` positions carry `k` distinct `κ`-keys (Lemma C), hence `k`
distinct `κ_f`-keys.

## 2. One layer: the flips cannot be refined

**Theorem A.** Let the flips be iid Bernoulli(`p`) on `κ_f`, with any
`p ∈ [0, 1]`, any outer coloring and no `X`. Then
`Pr[no monochromatic progression] ≤ exp(−K(κ_f)·((1−p)^k + p^k)) ≤ exp(−K(κ_f)·2^{1−k})`.

*Proof.* A block is monochromatic when its `k` flips agree. The blocks of the
disjoint family are independent. ∎

So a one-layer refinement with `ln K(κ_f) ≥ k ln 2 + ω(1)` fails with high
probability **for every `p`**, and `N^{β}` bits is far past that. This
generalizes Theorem 1 of the single-label note (`P3`, the `e = 1` family): the
condition `pk(1+p) > ln K` is what produced `b < a` and `a + b < 1` there,
and refining only raises `K`. In exponents, iid flips need `b < 1 − κ`. With
`2c < γb` and `γ < 1/2`, every iid-flip proof on any refinement has
**`c < (1 − κ)/4 ≤ a/4 < 1/8`**, and the ceiling drops as the key map gets
finer.

**Observation A′.** If `X` is random (each fine key with probability `ρ`,
independently) and the flips live on the same keys, the final coloring is iid
flips at rate `π = ρ + (1−ρ)p`. A random `X` on one layer is therefore
Theorem A again (check 4 of `verify.py`).

This is the probabilistic form of radar-7b's Proposition (`piste-C` § 2). That
Proposition says a union bound whose index contains the key word allows at
most `k e^{2pk}` keys in the non-rich part. **For one layer, the fibres
`N^{1−o(1)}` are the central obstacle:** one layer cannot have `N^{Ω(1)}`
keys at all. Two layers escape it, because the non-rich index no longer
contains the fine key word (§ 3).

## 3. Two layers: the price on the non-rich side is `2^k`

**Proposition 1′.** In the two-layer design, `P` is monochromatic in `β`
exactly when (a) and (b) both hold:

* (a) no coarse key has a free position in `D_β(P) = {c₁ ≠ β} ∩ P` and
  another free position outside it;
* (b) no frozen position lies in `D_β(P)`.

When they hold, the probability is `p^{#κ(free part of D_β)}` times
`(1−p)^{#κ(other free positions)}`. This is Proposition 1 of the exact-form
note, read with "coarse keys of free positions" (check 1, exhaustive; counting
fine keys instead fails).

**Theorem B.** Theorem 2 of the exact-form note holds for the two-layer
design. Only the case (ii) threshold changes:

> **(I′_w), two layers:** `w` coarse keys with
> `w b ln k ≥ (1+δ)(H + k ln 2)`.

(II′_θ) and (I′_η) are unchanged, still in positions, and the conclusion is
still `2c < θb` for every `b > 0`.

*Proof.*

* *Rich progressions.* The union is over the `N²` progressions, and `X_P` is a
  function of `P`. The certificates of Theorem 9 of `source-only-1-8` are sets
  of coarse keys of free positions of `D_β(P)`. Each such key has a flip
  variable, and these variables are independent across distinct keys. The
  counts read no color and no `X`. Nothing changes.
* *Case (i).* A non-empty event still needs `⌈ηk/2⌉` distinct coarse keys
  flipped. The index becomes the key word plus the set `Q ⊆ [k]` of frozen
  positions, at most `2T_key·2^k = e^{o(k ln k)}` indices against
  `e^{−Ω(k ln k)}` each.
* *Case (ii).* The key word and its code fix the coarse keys and `C_β`, but no
  longer `X_P`. Adding `Q` to the index fixes it. So there are at most
  `e^{H}·2^k` indices, and each non-empty event has probability at most
  `p^{w}`. ∎

`H = 6 ln q + O(D ln³ k) = o(k)`, so the threshold goes from
`w ≍ k^{1−a}/b` to `w ≍ k ln 2/(b ln k)`. At `k = 10^{400}` and `b = 1`,
`w/k ≈ 7.6·10^{−4}` (check 5). Non-saturation stays a vanishing fraction of
`k`. **This is the whole cost of the refinement on the non-rich union bound.**

**The rich barrier (G♭) is unchanged.** The flips are on `κ`, so the covers
are covers by coarse key sets, and Proposition 5′ of PR #21 applies verbatim:
its hypothesis (G♭) concerns the coarse keys only. In the one-layer design,
the barrier would become unconditional as soon as `β > b/(4c)`. Indeed
`ν(F ⊇ S) ≤ 4k² F_f²/N² ≤ 4k² N^{−2β}` for `|S| ≥ 2`, and this is at most
`p^{|S|}` up to `|S| = k/2`. But Theorem A has already closed that design.

**P1–P3 under two layers.** They concern iid flips on `κ`, and the flips stay
there. Theorem 1 (`b < a`, `a + b < 1`) and P2 (periodic flips) still bind
any proof that pays case (ii) with flips. Door 1 escapes them by freezing, as
before. The refinement neither helps nor hurts that escape.

## 4. Two layers: what the extra bits can and cannot do for X

**Lemma F (a fibre is already separated).** On the fibre
`Φ_r = {r + q^{D−1}m′ : m′ ∈ ℤ/q}`, the coarse key `κ` takes each value at
most twice on `{|ỹ_D| ≥ 1/8}`.

*Proof.* Coordinates `< D` are fixed on `Φ_r` (Lemma A). `qy_D` advances by
`λ` per step of `m′`, so `s = qỹ_D` has a fixed fractional part, and `m′ ↦ s`
is injective (`gcd(λ, q) = 1`). The band is `⌊C(r) + s²⌋`, with `C(r)` fixed.
Suppose `s ≠ s′` share a band, both with `|s| ≥ q/8`. If they have the same
sign, then `|s² − s′²| ≥ 1·(q/4) > 1`, which is impossible. So they have
opposite signs and `|s + s′| < 4/q`. That interval has length `8/q < 1` and
holds one value of the fractional class, so there is at most one such `s′`. ∎

(Check 2: exhaustive on 60 fibres. Control: points spaced `1/q²` share bands
by the hundreds.)

**Corollary F (fibre invariance).** For every refinement `κ_f`, the traces
`{X ∩ Φ_r^{≥1/8} : X ⊆ κ_f(ℤ/N)}` are the same as with `κ`, except for
splitting the `±s` pairs. The refinement gains no freedom **inside** a fibre.
It only removes the couplings **between** fibres that share a coarse key.

All of Door 1's single-label blocks lie inside one fibre (Lemma A). Lemma R of
the single-label lenses note reads `X` only through
`S_J = {m : r + q^{D−1}m has its key in X}`, a subset of a fibre, and never
uses the key map otherwise. So **Lemma R holds verbatim for every
refinement**. In every box of the `P1` region, `X` has density at least
`ρ_AP(Y₀, k)/2` on 9/10 of the points, with `ln Y₀ = (1 − o(1)) ln q`. The
per-fibre requirement is therefore the same as with the source keys. For an
`X` of random type, which pays the rich side by its density, it asks for a set
of density `k^{−1/2−δ}` meeting every `k`-AP of `[Y₀]`. For other `X` it asks
only for (H) on each piece. The same holds for the other closures that read `X`
fibre by fibre: the lens identity (Theorem A of that note), P1a's AP-free
sets, and P1b's clique bound, which reads label colors. The `N^{β}` bits act
only across fibres and on rich progressions. Inside the fibres the requirement
is **unchanged**. This note does not show that it blocks: the fibres alone are
satisfiable (Proposition 2 of `key-measurable-colorings`), and whether the
interaction of the two families blocks is exactly (D) and (S) there.

**Theorem C (a random X fails (I′) with N^{β} bits).** Let `X` be random on
`κ_f`, each fine key independently with probability `ρ`, for any `ρ`. Then:

1. `Pr[(I′) holds on every single-label block] ≤ exp(−K(κ_f)(ρ^k + (1−ρ)^k))`;
2. `Pr[c₁ has no single-label block entirely frozen] ≤ exp(−K(κ_f) ρ^k)`. An
   entirely frozen block is monochromatic for **every** flip assignment.

*Proof.* On a block `B` with constant `c₀ = α`: target `α` needs
`X ∩ B ≠ ∅`, which fails with probability `(1−ρ)^k`. Target `¬α` needs at
least `w ≥ 1` free keys, which fails when `B` is fully in `X`, with
probability `ρ^k`. The disjoint family is independent. ∎

So a random `X` needs `ln K ≤ k ln 2` to have a chance, and
`ρ ≥ (1 − o(1)) ln K / k`. In exponents, **`b_X ≤ 1 − κ`**. For the
source keys this is `b_X ≤ a`, the C1 bound of the track, now derived from
`K`. With `N^{β}` bits no density works. Proposition 5 of the exact-form note
then puts the first-moment ceiling of a random `X` at
`c < b b_X/(4(b + b_X)) < b_X/4 ≤ (1 − κ)/4 ≤ a/4 < 1/8`. This is the
**same ceiling as iid flips**, and it also drops with refinement.

**Proposition D ((II′) at second order).** Assume Proposition 5's family `𝓕`
has `|𝓕| ≥ N²/2`; this is a sketch there, through R1 and Theorem 6. Then some
step `d` that is a unit has `≥ N/2 − N/P` starts in `𝓕`: the average runs
over all steps, and the non-units are a fraction `1/P` of them (`N = q^D`,
`q` a power of the prime `P > k`). Cut its orbit into the `⌊N/k⌋`
consecutive blocks `{n₀ + jkd + id : i < k}`; the `k` phases of the cut cover
every start, so one phase holds `≥ (N/2 − N/P)/k − 1` progressions of `𝓕`,
pairwise position-disjoint. Lemma G then gives
`M ≥ ((N/2 − N/P)/k − 1)/(k(F_f−1)+1)` of them
with disjoint fine keys.
For a random `X`, `Pr[(II′_θ) holds] ≤ exp(−M ρ^{(1/2−θ)k+1}(1−ρ)^k)`.
With `N^{β}` bits, this is `o(1)` as soon as **`βc > (1/2 − θ) b_X`**. For
`θ = 1/4`, `b_X = 1/5`, `c = 1/9`, that means `β > 9/20` (check 5).

*Proof.* Proposition 5's lower bound on each failure probability, and
independence across the disjoint subfamily. ∎

This answers the brief's last question. No setting makes a random `X` pass
(II′) "at second order". A second moment can only certify that failures
**exist** (`Pr[Z > 0] ≥ E[Z]²/E[Z²]`), never that they don't. A random `X`
passes only where its first moment is small, and § 4 already caps that region
below `1/8`. More bits make the failures more independent, so they turn the
first-moment obstruction into a high-probability failure. With coarse keys
that conversion was missing, which is the remark at the end of Proposition 5.

## 5. The trade-off, exactly

The exponent `κ = log_k ln K(κ_f)` satisfies `κ ≥ 1 − a > 1/2` for every
refinement, and refining raises it.

| route | constraint from `K` | rich side | ceiling |
|---|---|---|---|
| iid flips on `κ_f` (one layer) | `b < 1 − κ` (Theorem A) | `2c < γb`, `γ < 1/2` | `(1−κ)/4 ≤ a/4 < 1/8` |
| random `X` on `κ_f` | `b_X ≤ 1 − κ` (Theorem C) | first moment, Prop. 5 | `(1−κ)/4 ≤ a/4 < 1/8` |
| deterministic `X` on `κ_f`, flips on `κ` | non-rich: `+k ln 2` (Theorem B) | `2c < θb`, unchanged | as before: Lemma R unchanged (Corollary F) |

**Statement.** Every refinement of the key map that gives `X` `N^{Ω(1)}` bits
does one of two things:

* it refines the flips, and then fails for every `p` (Theorem A); or
* it refines `X` alone. It then leaves the per-fibre requirement on
  single-label blocks unchanged, because inside each fibre the coarse keys
  already separate the points (Lemma F, Corollary F). It closes the
  random-`X` route outright (Theorem C). And it costs `2^k` on the non-rich
  union bound (Theorem B).

The bits only act across fibres and on rich progressions. There, (II′) is
already satisfied by any `X` that splits or leaves `θk`, so they would serve a
deterministic `X` that is anti-random at order `≥ 3`, which no one has. **No
`c > 1/8` follows. More bits do not change what Door 1 asks inside a fibre.
Whether that requirement, together with the rich side, blocks Door 1 is open:
it is (D) and (S) of `key-measurable-colorings`.**

Scope: refinements of the source key map, in the region `λ ≤ q/(400k³)`
(every `a < 1/2`), with iid flips on one of the two layers and
"single-label" in the sense of Lemma C. Not covered: key maps that are not
refinements, such as coarser ones or different geometry; non-iid flips; and
anything when `a > 1/2`, where single-label blocks do not exist (Lemma D of
the single-label note).

## What `verify.py` checks

1. **Proposition 1′, exhaustively**, on 500 random two-layer instances
   (`k ≤ 9`, coarse multiplicity `≤ 2`, random splits, random `X`,
   `p = 1/5`). Control: counting fine keys instead of coarse ones disagrees.
2. **Lemma F**: on 60 fibres (`q ∈ {101, …, 1009}`, random `λ`, `s₀`,
   `C`), at most 2 points per band on `{|s| ≥ q/8}`. Control: points spaced
   `1/q²` reach multiplicity 401.
3. **Lemma G**: the greedy subfamily meets `|𝓑|/(k(F−1)+1)` on 200 random key
   maps. Control (6b): the bound without the factor `k` is false.
4. **Theorem A**: `(1−p)^k + p^k ≥ 2^{1−k}` on a grid. **Observation A′**: on a
   toy instance, the exact law of random `X` plus flips on the same keys is
   iid(`π`). Control: with coarse flips it is not.
5. **Exponents**: the case (ii) threshold `w/k` at `k = 10^{400}` (two layers
   and coarse); the ceilings `(1−κ)/4` for iid flips and for random `X` on a
   grid of `a < 1/2`, all below `1/8`; the threshold `β* = (1/2 − θ)b_X/c`;
   the trivial barrier `b/(4c) < 1`.
6. **Negative controls**, each required to fail.
7. **Provenance**: MANIFEST hashes; summary equal to `RESULT.json`.

## What is not claimed

* No admissible `X`, no new bound on `c`.
* Theorem B relies on Theorem 2 of the exact-form note, hence on Theorems 6,
  8 and 9 of the trust-reduction notes (refereed publishable, not in this
  tree). Proposition D relies on the `|𝓕| ≥ N²/2` sketch of Proposition 5.
* The `2^k` of Theorem B is the price of this union bound, not a lower bound.
* Corollary F transfers only the closures that read `X` fibre by fibre. It
  says nothing about a deterministic `X` that would use the bits across
  fibres to be anti-random on rich progressions. That is the one door this
  note leaves open, and it is Door 1's remaining question with or without
  refinement.
