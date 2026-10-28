# Single-label progressions make `b < a` and `a + b < 1` necessary for these union bounds

**Status:** negative result (research note), with proofs and exact finite
checks. No new bound is claimed. The note answers, for one class of proofs,
the open question of this track: can the case (ii) band words be paid for
some other way?

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, plus the track
README of `2026-10-20-erwan-binding-lever`.

**Sources:** the construction, meshes, keys and flips are those of OpenAI,
*Quantitative Superexponential Bounds for van der Waerden Numbers*, pinned
in `source-manifest.json` (Sections 2 and 6), with the sharpened choices
`h_0 = D⌈log k⌉²` and `M = ⌈k^m⌉` of `sharpened-region-proof.md`.

## Reproduce

```sh
python3 -B auto-research/short-period-sensitivity/2026-10-20-ChaloupeMusic-single-label-obstructions/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. It takes about three seconds, plus about a
minute for the PR7 window, and uses only the standard library.

## Result

Every proof in this repository fixes an outer coloring `c*`, then flips each
key `κ(n) = (V-word of y(n), ⌊‖q ỹ(n)‖²⌋)` independently with probability
`p`. It concludes with a union bound in which, for each progression `P` and
each target color, the event "`P` is monochromatic in that color" is covered
by a **sub-prescription of `P`**: an event `{E|_S = π_P|_S}`, where
`∅ ≠ S ⊆ κ(P)` and `π_P` is the flip pattern that the target forces on
`P`.

This is the shape of:

* the source's rich and affine bounds;
* the repeated-key and rank certificates;
* the digit-rank bound;
* both cases of `short-period-runs-proof.md`.

Call such a union bound a **sub-prescription union bound**.

1. **Theorem 1.** Assume `λ ≤ q/(400k³)`. There are
   `K ≥ (k²/2 − 4)^{D−1} · q/(20k)` progressions that each stay inside a
   single full label and have pairwise disjoint key sets. Consequently, for
   every outer coloring `c*`:
   * every sub-prescription union bound totals at least `K(1−p)^k`;
   * `P_p(no monochromatic progression) ≤ exp(−K(1−p)^k)`, with no
     restriction on the proof.

   A sub-prescription union bound below 1 therefore needs
   ```
   pk(1+p) > (D−1)·ln(k²/2 − 4) + ln q − ln(20k).
   ```
   On the exponent scale (`D = k^a`, `p = k^{−b}`, `ln q ≈ c k^{1−a} ln k`)
   this is **`b < a` and `a + b < 1`**, both strict:
   * the `ln q` term gives `b < a`, inequality B of the binding-lever note;
   * the `2(D−1) ln k` term gives `a + b < 1`, inequality R.

   Together they give `b < 1/2`, hence `c < 1/8` through `2c < γb`, `γ < 1/2`.
   No recount of key words or color codes of this kind can remove B or R.
2. **Proposition P2 (periodic flips).** Suppose the flip of a key depends on
   its full label and on its band only modulo `L ≤ q/(400k³λ)`. Then some
   progression is monochromatic **for every flip assignment**. This covers
   every combination of modular band layers, with `L` the lcm of the moduli.
3. **The literal PR7 tuple** (`a = 49/100, m = 99/100, b = 97/200, c = 1/9`).
   For every `k` from `10^{200.2}` to `10^{402.0}`:
   * `ln K − k(p + p²) ≥ 5`, so every sub-prescription union bound is at
     least `e^5`;
   * `P_p(success) ≤ exp(−e^5)`.

   The "sufficiently large k" of `short-period-runs-proof.md` therefore
   exceeds `10^{402}` for this tuple. This is consistent with the conservative
   `K = 2^{33554432}` of open PR #9. Open PR #12 uses `k`-dependent parameters
   with `pk = 128 ln q` and is not affected.

### What is not claimed

* That no good flip assignment exists: a random one is almost never good,
  that is all.
* Anything about union bounds that cover one progression with events
  outside its own keys. Two events on a single key cover everything, so some
  restriction of this kind is necessary.
* Anything against a local lemma over the flips. The `K` events are
  independent, and the local lemma tolerates any number of independent
  events. In particular, nothing here opposes `a + b ≥ 1` for a local-lemma
  proof. A sketch below indicates why `b < a` probably survives one.
* Anything about structured flips that are neither iid nor periodic.
* Anything when `λ > qH/(k−1)`, which holds for every `a > 1/2` once `k` is
  large: there, single-label progressions do not exist (Lemma D).

## Setting

* `q` is a power of a prime `P ∈ (k, 2k²]`, `gcd(λ, q) = 1`, `H = k^{−2}`,
  `α = q^{−(D+1)}`.
* `U` has intervals of width `H/λ`; `V` is the source's adaptive mesh.
* Labels are `L(n) = (U(x_i(n)), V(y_i(n)))_{i≤D}`, and `f(n) = ‖q ỹ(n)‖²`.
* The final color is `C(n) = c*(L(n)) + E_{κ(n)} mod 2`, where the `E_κ` are
  iid Bernoulli(`p`) with `p ≤ 1/2`.
* Throughout: `λ ≤ q/(400k³)` (so `q ≥ 400k³`) and `α ≤ 1/8`. The dilation
  satisfies `λ ≥ 30`, since `2·3·5 | λ` as soon as `h_0 ≥ 5` and `2M ≥ 5`.

## Lemma A (one moving coordinate)

Let `0 ≤ r < q^{D−1}`, `m ∈ ℤ`, `e ≥ 1`, and `n_j = r + q^{D−1}(m + je)`. Then:

* for `i < D`, `x_i(n_j)` and `y_i(n_j)` do not depend on `j`, because
  `q^{D−1}je/q^i ∈ ℤ`;
* in coordinate `D`, `x_D` advances by `e/q` and `y_D` by `λe/q`.

Suppose the two real segments swept in coordinate `D` lie inside one `U`
interval and one `V` interval. Then `L(n_j)` is constant, so `c*(L(n_j))` is
constant for every `c*`. Moreover `q ỹ_D(n_j) = s + jλe` with
`s = q ỹ_D(n_0)`, so

```
f(n_j) = C + (s + jλe)²,    C = Σ_{i<D} (q ỹ_i(n_0))².
```

When `r = 0`, `C = 0` and `s` is an integer.

## Lemma B (every box word is reached)

Let `I_1, …, I_{D−1}` be `V` intervals of length at least `2/q`. Write
`u = λr mod q^{D−1} = Σ_t u_t q^t` in base `q`. Then `y_i(r) = (u mod q^i)/q^i`
lies in `[u_{i−1}/q, (u_{i−1}+1)/q)`. Choose each `u_{i−1}` so that this
cell lies inside `I_i`, and set `r = λ^{−1}u mod q^{D−1}`. Adding `q^{D−1}m`
does not change `y_i` for `i < D`.

The `V` intervals contained in `{1/8 ≤ |Y| ≤ 3/8}` have lengths between `H/32`
and `H`, by the source's width lemma with `ρ ∈ [1/8, 3/8]`. Since
`q ≥ 64k²`, each has length at least `2/q`. There are at least `k²/2 − 4` of
them per coordinate.

## Lemma C (many good blocks for each word)

Fix `r` and `e = 1`, and take blocks `m ∈ {tk, …, tk + k − 1}` with
`0 ≤ t < T = ⌊q/k⌋ − 1`. Count the blocks whose start has
`ỹ_D ∈ J = [1/8, 3/8 − kλ/q]`, an interval of length `ℓ ≥ 0.2475`:

* The starts advance by `δ = λk/q < 1` mod 1 and make at least `λ − 2`
  complete turns. Each complete turn puts at least `ℓ/δ − 1` of them in
  `J`, so at least `(λ − 2)(ℓ/δ − 1) ≥ q/(5k) − λ` blocks qualify, using
  `λ ≥ 30`.
* The `x_D` ranges of distinct blocks are disjoint, so each of the `k²λ`
  boundaries of `U` spoils at most one block.
* There are at most `8k² + 2` boundaries of `V` in `[1/8, 3/8]`. Each spoils
  at most one block per turn, so at most `λ + 1` blocks.

With `λ ≤ q/(400k³)`, at least
`q/(5k) − 10k²λ − 20k² ≥ q/(8k) ≥ q/(20k)` good blocks remain.

Inside a block, `s ≥ q/8` and consecutive values of `f` differ by at least
`2sλ ≥ 1`, so the block has `k` distinct keys. Across blocks of the same `r`,
distinct `m < q` give distinct `s` with the same fractional part. All are at
least `q/8`, so distinct `s` give squares differing by at least 1: their key
sets are disjoint. Distinct `V` words in coordinates `< D` give disjoint key
sets trivially.

## Theorem 1

Choose one `r` per `V` word from Lemma B and all good blocks from Lemma C.
This gives `K ≥ (k²/2 − 4)^{D−1} · q/(20k)` single-label progressions
`B_1, …, B_K` with pairwise disjoint key sets.

Fix `c*`. Each `B_i` is monochromatic as soon as its `k` keys are all
unflipped, so `P(B_i mono) ≥ (1−p)^k`. These events are independent, so
`P(no mono) ≤ (1 − (1−p)^k)^K ≤ exp(−K(1−p)^k)`.

In a sub-prescription union bound, take the target that equals `c*` on
`B_i`. It is covered by an event `{E|_S ≡ 0}` with `∅ ≠ S ⊆ κ(B_i)`, of
probability `(1−p)^{|S|} ≥ (1−p)^k`. Since the key sets are disjoint, that
event serves no other `B_j`. The total is therefore at least `K(1−p)^k`. ∎

## Proposition P2

Take `r = 0` and `e = L ≤ q/(400k³λ)`. A good block exists by the argument
of Lemma C. Its full label is constant, and its bands are
`(s + jλL)² ≡ s² (mod L)`. Any rule `E(full label, band mod L)` is therefore
constant along it, and the block is monochromatic whatever the rule.

## Lemma D (scope)

If `λ > qH/(k−1)`, no `k`-term progression with `d ≠ 0` stays in one label.

Proof. Inside one `U` interval, the affinity lemma gives
`x̂_i(n_j) = A_i + jB_i` with `(k−1)|B_i| ≤ H/λ`. Let `v` be the `q`-valuation
of `d`, as in the source's multiplicity lemma. Then `x_{v+1}(d)` is a nonzero
multiple of `1/q`, so `|B_{v+1}| ≥ 1/q`.

Since `ln λ ≥ (1 − o(1))h_0 = k^{a+o(1)}` and `ln q = k^{1−a+o(1)}`, this holds
for every `a > 1/2` once `k` is large. The first local-lemma family
(`2a < m < 1`) is what currently forbids that regime.

## Sketch, not a theorem: a local lemma over the flips

Inside one box, the steps `e = 1, …, E_max ≈ q/(400k³λ)` give single-label
progressions with distinct `θ_2 = λ²e²`. Suppose that, for each `e`, some
`(r, m)` in the same box word puts one prescribed key at position 0. Then one
key lies in at least `E_max` signatures, each of probability at least
`(1−p)^k`, and the asymmetric criterion fails once `E_max(1−p)^k > pk`.
Existence of these `(r, m)` is plausible, since `C_r` varies finely with `r`,
but it is not proved here.

## Open: structured flips

With `r` fixed, a box's single-label band sets are the images under
`x ↦ ⌊C + x²⌋` of arithmetic progressions `x = s + jΔ`, with
`Δ ∈ λ·[1, E_max]`. Structured flips that beat `b < a` would need a set of
bands of density `k^{−b}` meeting every such image, for every `C` that occurs
in the box. Two observations bound this:

* **Unions of residue classes.** Take classes modulo primes `ℓ ≤ k`. Such a
  set misses an AP of step `Δ` only if every `ℓ` divides `Δ`. It must
  therefore have `Σ ln ℓ ≥ ln(N/k)`, hence density
  `Σ 1/ℓ ≥ ln(N/k)/(k ln k)`. This is a `log k` gain over random sets, and
  `b < a` still holds on the exponent scale.
* **The key does not know `C`.** `C` varies with `r` within one box, so a
  rule written in `⌊√(band − C_0)⌋` sees the progressions of another `r`
  shifted by `(C − C_0)/(2x)`.

A general lower bound is an asymmetric van der Waerden question at the scale
`N = exp(k^{1−a})`. For comparison, `w(3, k) ≤ exp(k^{1−c})` (Schoen) lives at
the same scale. No such bound is claimed here.

## Checks in `verify.py`

1. On 300 random instances, with exact fractions:
   `f(n_j) = (s + jλe)²` and `ỹ_i = 0` for `i < D`.
2. On `q = 2^61 − 1`, `D = 3`, `k = 12`, `λ = 840`, with the source's `U` and
   adaptive `V` meshes (200-digit decimals): 400 random blocks out of 400
   stay in one full label.
3. 50 blocks have pairwise disjoint key sets.
4. P2 for `L = 2^10`, `3^7·5` and `2^20`: bands are constant mod `L` and
   exact bands are distinct.
5. Negative controls, all rejected:
   * the step `L + 1` moves the band mod `L`;
   * a step 1000 times above the bound leaves the label;
   * a block straddling a `U` boundary is detected.
6. 36 distinct `V` words in coordinates `< D` are reached through Lemma B,
   with one single-label progression each and pairwise disjoint key sets.
7. Exponent table: `ln(K(1−p)^k)` is positive at `b = a` and `b > a`. For the
   PR7 choice it is negative at `k = 10^{1000}`.
8. Scope: on `ℤ/7³`, every `λ > qH/(k−1)` leaves no nonzero step inside one
   `U` cell.
9. PR7 window, by interval arithmetic on `ln k` with cells of width `0.01`,
   using monotone bounds:
   * `ln q ≥ (ck/D) ln k`;
   * `ln λ ≤ 1.25506 (h_0/ln h_0) ln(2M + 2)` (Rosser–Schoenfeld);
   * `D − 1 ≥ k^a − 1`;
   * `ln(1/(1−p)) ≤ p + p²`.

   Lower bounds are taken at the left end of each cell and upper bounds at
   the right end.

The finite checks illustrate the lemmas; the proofs are the text above.
