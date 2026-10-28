# Algebraic band rules cannot split every single-label block

**Status:** negative result (structural research note), with proofs and exact
finite checks. No new bound is claimed. In the regime `a < 1/2` of the
template, the note closes one named class of candidates for "door 1"
(structured flips), the only known route past `1/8` in the current template.
It closes the class up to total modulus `q^{1−o(1)}`. Beyond that it says
nothing.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.

**Depends on** (both are local, unmerged contributions of the same sprint):

* radar-99, `short-period-sensitivity/2026-10-20-ChaloupeMusic-single-label-obstructions`
  (local commit `4e0f252`): Lemma A (one moving coordinate), Lemma B (every
  box word is reached), Proposition P2. The mesh, label and coordinate helpers
  of `verify.py` are transcribed from its verifier.
* radar-c1, `structured-flips/2026-10-20-ChaloupeMusic-single-label-lenses`
  (local commit `b5a6c38`, branch `sprint2/N2`): Lemma 1 (exact lens: on a
  single-label progression the band is `⌊θ + vj⌋ + λ²e²j²`), Lemma R
  (reduction of (I) on one fibre to a `k`-AP transversal problem) and
  Proposition B (periodic rules of period at most `E_max`, with patches on
  exact squares, are constant on a block). Theorem 1 below is the CRT
  companion announced there.

**Sources:** the construction, meshes, keys and flips are those of OpenAI,
*Quantitative Superexponential Bounds for van der Waerden Numbers*, pinned in
`source-manifest.json` (Sections 2 and 6).

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-20-ChaloupeMusic-algebraic-band-rules/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary printed before it equal to `RESULT.json`. It runs in about two seconds
on the standard library only.

## The question

Door 1 (the synthesis of the sprint, "La sortie qui reste") freezes a
structured set `X_s` of keys, `c_1 = c_0 ⊕ 1_{X_s}`, and flips the other keys
independently with probability `p = k^{-b}`. It needs:

* **(I)** every case (ii) progression `P` is cut by `X_s`: `X_s` contains at
  least one key of `P` on its dominant colour, and **not all** of them
  (non-saturation). If every dominant key is frozen, `c_1` swaps the dominant
  positions to the other colour, and `P` is monochromatic, or nearly so, for
  every draw;
* **(II)** no rich progression has more than `εk` keys in `X_s`.

Then `b` is no longer bounded by `a`, and every `c < 1/4` would follow.

For a single-label progression `B` (one full label, so `c_0` is constant on
`B`), `c_1` is monochromatic on `B` exactly when `X_s` contains **none or
all** of the keys of `B`. On single-label blocks, (I) with its non-saturation
clause therefore reads "`X_s` **splits** `κ(B)`". A block whose keys all lie
in `X_s` is as bad as a block that misses it, and worse, since nothing random
is left on it.

The deliverable (b) of the sprint plan asks for a class of `X_s`, containing
the periodic rules (closed by P2) and the CRT unions, that provably fails (I).

## Result

Keys are `κ(n) = (W(n), t(n))`, with `W` the `V`-word of `y(n)` and
`t = ⌊‖q ỹ(n)‖²⌋` the band. Write `□_ℓ` for the squares of `ℤ/ℓ`,
`0` included, and `NR_ℓ` for the non-residues.

**Definition (algebraic band rule).** Fix `L_0 ≥ 1` and a finite set `𝓛` of
odd primes. For every `V`-word `W`, choose any Boolean function
`F_W : ℤ/L_0 × {0,1}^𝓛 → {0,1}` and sets `T_{W,ℓ} ⊆ ℤ/ℓ`, and put

```
X_s = { (W, t) : F_W( t mod L_0 , (1[t mod ℓ ∈ T_{W,ℓ}])_{ℓ∈𝓛} ) = 1 }.
```

Each `T = T_{W,ℓ}` must satisfy one of

* **(G-i)** `T − □_ℓ ≠ ℤ/ℓ` ("square-blind"), or
* **(G-ii)** `2k|T| < ℓ` ("sparse").

The class contains:

* every rule periodic in the band modulo `L_0` (`𝓛 = ∅`), the class of P2;
* residue unions, the CRT construction: `T = {ρ_ℓ}` (G-i), `F = OR`;
* the non-residue rules "`t − c` is a non-residue mod `ℓ`", i.e.
  `χ_ℓ(t − c) = −1`: `T = c + NR_ℓ` has density `1/2` and satisfies (G-i),
  since `c ∉ T − □_ℓ`. Their complements `χ_ℓ(t − c) ∈ {0, 1}` are in the
  class through `F`. The rule "`t − c` is a nonzero square" taken alone is
  **not** in the class: `T = c + (□_ℓ ∖ {0})` fails (G-i) and (G-ii) for
  every prime `5 ≤ ℓ < 200` (checked);
* polynomial conditions `P_W(t) mod ℓ ∈ S_W` with `P_W` non-constant mod `ℓ`,
  `deg P_W ≤ d` and `2kd|S_W| < ℓ` (G-ii), whose coefficients may depend on
  the box coordinates in any way (a constant `P_W` gives `T = ∅` or `ℤ/ℓ`);
* any Boolean combination of these with a periodic part (XOR, majority, a
  truth table).

**Theorem 1.** Let `D ≥ 3`, `gcd(λ, q) = 1`, `λ` even, `q ≥ 64k²`,
`H = k^{-2}`. Let `e ≥ 1` with `L_0 | λe/2`, let no prime of `𝓛` divide
`λ e L_0`, put `M = ∏_{ℓ∈𝓛} ℓ`, and assume

* **(S1)** `8 L_0 (M + 1) ≤ λe`;
* **(S2)** `(6k + 12) λe + 8 ≤ qH/32 − 2`;
* **(S3)** `32 k λe < q`.

Then there are at least

```
K = (k²/2 − 4)^{D−2} · (k²/4 − 2) · W,     W = ⌊(qH/32 − 2) / ((k+2) λe)⌋ − 4 ≥ 2,
```

single-label progressions `n_j = r + q^{D−1}(m + je)`, `0 ≤ j < k`, with
pairwise disjoint key sets, such that `X_s` contains either all or none of the
keys of each. Write `K = K_in + K_out` accordingly. Both cases are failures of
(I): a block inside `X_s` is saturated (all its keys are frozen), a block
outside is not touched.

**Corollary 2 (door 1).** For every algebraic band rule satisfying the
hypotheses, and every outer coloring `c_0`, with `c_1 = c_0 ⊕ 1_{X_s}` and
independent flips of probability `p` on the keys outside `X_s`:

* **inside** (`K_in` blocks): such a block has no random key, and `c_1` is
  constant on it, so it is monochromatic for every draw of the flips. If
  `K_in ≥ 1`, then `P(no monochromatic progression) = 0`, and no union bound
  can fall below 1.
* **outside** (`K_out` blocks): such a block is monochromatic as soon as none
  of its `k` keys flips, with probability `(1−p)^k`, and these events are
  independent across blocks. Hence
  `P(no monochromatic progression) ≤ exp(−K_out(1−p)^k)`, and every
  sub-prescription union bound totals at least `K_out(1−p)^k`: each event
  fixes flips on keys of a single block, as in radar-99's Theorem 1.

Since `K_in = 0` forces `K_out = K`, the rule fails in every case: either a
monochromatic progression for every draw, or the two bounds above with
`K_out = K`.

**Corollary 3 (sizes).** Let `L_0' = L_0/gcd(L_0, λ/2)` and take
`e = L_0'·2^t` with `t ≥ 0` minimal such that `λe ≥ 8L_0(M+1)`. Then
`λe ≤ max(λL_0', 16 L_0 (M+1))` and `W ≥ q/(32k²(k+2)λe) − 6`. In the regime
`a < 1/2` of the template (`λ ≤ q/(400k³)`), on the exponent scale
(`D = k^a`, `ln q = c k^{1−a} ln k (1+o(1))`, `p = k^{−b}`, `b > a`),
`pk = k^{1−b} = o(ln q)`. Hence an algebraic band rule with
`ln(L_0' λ) ≤ (1−η) ln q` and `ln(L_0 M) ≤ (1−η) ln q` makes
`ln K ≥ η ln q (1 − o(1)) ≫ pk`, which is fatal. **An algebraic band rule
that cuts every single-label block needs total modulus `L_0 · ∏ℓ ≥ q^{1−o(1)}`.**
When moreover `a + b > 1`, the box words alone give
`ln K ≥ 2k^a ln k (1 − o(1)) ≫ k^{1−b}`, and `W ≥ 2` suffices: the rule needs
`L_0 (M+1) > q/(10^4 k³)` (or `λL_0'` above the same bound).

### Where this sits relative to P2 and Proposition B

A single-label block of step `e'` needs `(k−1)λe' < q·|V| < qH`, so every
step is below `e_1 = qH/((k−1)λ)`. P2 (and radar-c1's Proposition B)
**freezes** a periodic rule of modulus `L` by taking a step with `L | λe'`.
This works only when `L/gcd(L, λ) < e_1`. Theorem 1 freezes only the periodic
part `t mod L_0`, by the same mechanism (Lemma 4). It never freezes a
per-prime indicator: it sets all of them to 0 through `τ`. Under (S2) the
product `M = ∏ℓ` can reach `λe/(8L_0) ≈ q/(1536 k³ L_0)`, a factor of order
`λ/(1536 L_0)` beyond `e_1 ≈ q/(k³λ)`. For the source's `λ` (the product of
prime powers over the primes up to `h_0`), `ln λ ≥ θ(h_0) ≥ h_0/2`, so this
factor is `exp(Ω(k^a log² k))`.

A rule whose per-prime part has a modulus `ℓ < e_1` can already die by
freezing, and for an OR one such prime suffices. The block of step `e' = ℓ`
freezes `t mod ℓ`. In radar-c1's family its bands are `x_j² + u²` with
`x_j ≡ x_0 (mod ℓ)`. Inside one box word, `x_0` and `u` run over all residues
mod `ℓ`, since their ranges have length at least `q/(32k²) ≥ ℓ`, and every
residue mod an odd prime is a sum of two squares. The frozen value
`x_0² + u²` can therefore be put in `T_ℓ`, and the whole block then lies
inside `X_s`. `verify.py` exhibits such a block for rule 3 of the toy
(Checks, 4).

Theorem 1 adds the rules that no single step freezes into one value. The
simplest are the non-residue rules `χ_ℓ(t − c) = −1` modulo a prime `ℓ`
above `e_1` (rule 1 of the toy). They have density `1/2`, so neither freezing
nor counting kills them. Theorem 1 handles every Boolean combination in the
same way, with all indicators at 0, whatever the truth table.

## Proof

Fix `r` (low digits), write `u = λr mod q^{D−1}`, `f = y_{D−1}(r) = u/q^{D−1}`
and `C = Σ_{i<D} (q ỹ_i(r))²`. For `n_j = r + q^{D−1}(m + je)` and
`s = q ỹ_D(n_0)`, Lemma A of radar-99 gives `ỹ_i(n_j) = ỹ_i(r)` for `i < D`
and `q ỹ_D(n_j) = s + jλe` while the `D`-th segment does not wrap. Moreover
`s ≡ λr/q^{D−1} ≡ f (mod 1)`, so `s = σ + f` with `σ ∈ ℤ` (radar-c1's Lemma 1).
Hence, with `α_0 = C + f²` and `φ = 2f`,

```
t_j = ⌊C + (σ + f + jλe)²⌋ = (σ + jλe)² + ⌊α_0 + φσ + φλe·j⌋.            (1)
```

**Lemma 1 (exact band polynomial).** Put `f* = 1/4 + L_0/(2λe)` and assume
`f ∈ [f*, f* + 2/q)`. Let `b_f = λe/2 + L_0`, `ζ = 2φ − 1`,
`T_s = ⌊λe/(8L_0)⌋`. Choose `σ_0` with `ψ_0 = frac(α_0 + φσ_0) < ζ`, put
`I_0 = ⌊α_0 + φσ_0⌋`, and `σ = σ_0 + 2τ` with `0 ≤ τ < T_s`. Then for every
`j < k`

```
t_j = Q_τ(j) := (σ_0 + 2τ + jλe)² + b_f·j + I_0 + τ.
```

*Proof.* `φλe = λe/2 + L_0 + β'` with `0 ≤ β' = 2(f − f*)λe < 4λe/q`, so
`⌊φλe⌋ = b_f`, and `β'(k−1) < 1/8` by (S3). Next,
`ζ = 2L_0/(λe) + 4(f − f*) ∈ (0, 1/4 + 8/q]` by (S1). Since `2φ = 1 + ζ`,
`α_0 + φσ = I_0 + τ + ψ_0 + ζτ`. Here
`ζτ < ζT_s ≤ 1/4 + (f − f*)λe/L_0 ≤ 1/4 + 1/32` by (S3). So
`ψ_0 + ζτ + β'j < (1/4 + 8/q) + 9/32 + 1/8 < 1` for `j < k`, and the floor in
(1) equals `I_0 + τ + b_f·j`. ∎

**Lemma 2 (the discriminant is a progression).** With `γ = (λe)²`,
`B = 2σλe + b_f` and `A = σ² + I_0 + τ` (so that `Q_τ(j) = γj² + Bj + A`),

```
B² − 4γA = K_0 + 8 λe L_0 τ,        K_0 = b_f² + 4λe b_f σ_0 − 4γ I_0.
```

*Proof.* Expand with `σ = σ_0 + 2τ`. The coefficient of `τ` is
`4λe(2b_f − λe) = 8λeL_0`. ∎

Let `ℓ` be an odd prime not dividing `λ e L_0`. From
`4γQ_τ(j) = (2γj + B)² − (B² − 4γA)`, and since `4γ = (2λe)²` is a nonzero
square, `Q_τ` takes on `ℤ/ℓ` exactly the values `□_ℓ + κ(τ)`, where
`κ(τ) = −(K_0 + 8λeL_0τ)/(4γ)`. By Lemma 2, `τ ↦ κ(τ)` is a bijection of
`ℤ/ℓ`.

**Lemma 3 (good residues).** Under (G-i), at least `ℓ − |T − □_ℓ| ≥ 1`
residues `τ mod ℓ` give `Q_τ(j) ∉ T` for every `j ∈ ℤ`. These are the `τ`
with `κ(τ) ∉ T − □_ℓ`. Under (G-ii), at most `2k|T| < ℓ` residues are bad.
For fixed `j` and `x ∈ T`, `Q_τ(j) − x` is a quadratic polynomial in `τ` with
leading coefficient `4 ≢ 0`, so it has at most two roots.

**Lemma 4 (constancy mod `L_0`).** If `L_0 | λe/2`, then `L_0` divides `γ`,
`2σλe` and `b_f`, so `Q_τ(j) ≡ A (mod L_0)` for all `j`.

**Proof of Theorem 1.** *Realization.* Choose the digits
`u_0, …, u_{D−3}` of `u` by Lemma B of radar-99, so that `y_i(r)` lies in any
prescribed `V`-interval of `{1/8 ≤ |Y| ≤ 3/8}`. Each has length at least
`H/32 ≥ 2/q`, and there are at least `k²/2 − 4` per coordinate. Put
`u_{D−2} = ⌈f* q⌉`. Then
`f = u_{D−2}/q + (u mod q^{D−2})/q^{D−1} ∈ [f*, f* + 2/q)` and `ỹ_{D−1} = f`.
In coordinate `D`, take a `V`-interval `I ⊂ [1/8, 3/8]`; there are at least
`k²/4 − 2` of them. The admissible `σ` form a range `S` of length at least
`qH/32 − 2`. Every `σ ∈ S` is realized by
`m = λ^{−1}(σ − ⌊λr/q^{D−1}⌋) mod q`.

*Windows.* Cut `S` into windows of length `L_w = (k+2)λe`. In a window
starting at `w`, the sequence `ψ(w + 2i) = frac(ψ(w) + iζ)` enters `[0, ζ)`
for some `i ≤ ⌈1/ζ⌉`, which gives `σ_0 ≤ w + λe/L_0 + 2`. For each `ℓ ∈ 𝓛`,
pick a good residue (Lemma 3). The CRT gives `τ* ∈ [0, M) ⊆ [0, T_s)` by
(S1). The block `σ* = σ_0 + 2τ*` ends before
`w + (5/4)λe/L_0 + 2 + (k−1)λe < w + L_w`. On it every indicator vanishes
(Lemma 3) and `t mod L_0` is constant (Lemma 4), so `F_W` is constant: all
keys of the block lie on the same side of `X_s`.

*One label.* The coordinates `x_i, y_i` with `i < D` are constant, and
`y_D` stays in `I`. Only `x_D` moves, by `e/q` per step. The block keeps its
`U`-interval unless its start has phase `frac(x_D(n_0)k²λ) ∈ [1 − ν, 1)`,
where `ν = (k−1)ek²λ/q`.

**U-phase lemma.** When `σ` increases by 1, `m` increases by
`λ^{−1} mod q`, and the phase increases by exactly `k²/q` mod 1, because
`λ^{−1}λ ≡ 1 (mod q)` and `k²λ` is an integer.

Since `|I| < H`, `S` spans less than one turn of the phase. The spoiled
starts in `S` therefore form at most two intervals, each of length at most
`(k−1)λe + 2 < L_w`, and at most four windows are lost. This leaves
`W = ⌊(qH/32 − 2)/L_w⌋ − 4` good windows, and (S2) gives `W ≥ 2`. The
condition `n_{k−1} < q^D` is the `U`-boundary at `x = 1`.

*Disjointness.* Distinct `V`-words give distinct keys. Within one word,
blocks of distinct windows have `σ`-ranges at distance at least 1 inside
`|x| ≥ q/8`. There `x ↦ ⌊C + x²⌋` separates points at distance 1. ∎

Corollaries 2 and 3 follow as in radar-99's Theorem 1. With the prescribed
`e`, `W ≥ (qH/32 − 2)/((k+2)λe) − 5`.

## What is not claimed

* **Moduli of size `q` or more.** Corollary 3 says an algebraic rule needs
  modulus `q^{1−o(1)}`. Beyond that it says nothing. The attack has only one
  free linear parameter (`τ`, range `λe/(8L_0)`), and the per-prime targets
  have density about `1/2`. A second parameter (radar-c1's family `x² + u²`
  or the integer part of `C`) cannot be combined with `τ` by this CRT argument.
* **Pseudo-random residue sets.** If `T − □_ℓ = ℤ/ℓ` and `|T| ≥ ℓ/(2k)`
  (for instance a random `T` with more than `2 log₂ ℓ` elements), no
  residue `τ` need be good, and such rules are not covered. The synthesis
  shows that a uniformly random `X_s` fails (II). Whether a pseudo-random
  residue rule can satisfy (I) and (II) is not addressed here.
* **Non-periodic rules.** Rules that read exact squares (patches; see
  radar-c1's family `x² + u²`), rules in `√(t − C_0)` (the key does not know
  `C`; radar-99, "Open: structured flips"), and Bohr sets of irrational
  frequency are outside the class.
* **(II).** Nothing here concerns rich progressions. The rules of the class
  are excluded by (I) alone.
* **The general question.** By radar-c1's Lemma R, door 1 with a sparse
  `X_s` requires `k`-AP transversals of density `k^{−1/2−δ}` in intervals of
  length `exp(Θ(k^{1−a} log k))`. Theorem 1 shows that no transversal of that
  kind comes from an algebraic band rule of modulus below `q^{1−o(1)}`. It
  says nothing about other transversals.

## Checks in `verify.py`

1. **Algebra.** On 31 random instances (`q = P^w`, `D = 3, 4`, various `λ`,
   `e`, `L_0`, low digits), for every `τ < T_s` and `j < k`: the band
   computed from the source's coordinates equals `Q_τ(j)`, and the
   discriminant equals `K_0 + 8λeL_0τ`. All in Fractions: 2,783 bands.
2. **U-phase.** On 200 random pairs, `phase(σ+d) − phase(σ) − dk²/q ∈ ℤ`.
3. **Toy instance in the regime of the theorem.** `q = 1009^6`, `D = 3`,
   `k = 24`, `λ = 720720`, `e = 2^18`, with (S1)–(S3) checked. Five rules:
   1. the non-residue rule `χ(t − c) = −1` modulo the prime `1000000007`;
   2. a random truth table on `(t mod 77`, four indicators mod 17, 19, 23, 29`)`,
      mixing singletons, a shifted non-residue set and a two-element set;
   3. the cubic condition `t³ + 2t + 7 ∈ {0,1,2} mod 1201`, for which (G-i)
      and (G-ii) both hold, OR the non-residue rule modulo `1000003`;
   4. the CRT union mod 17, 19, 23;
   5. a random 40-element residue set mod `4001`, which satisfies (G-ii) and
      not (G-i). This exercises the sparse branch alone.

   For each rule, on 8 coordinate-1 words and 2 coordinate-`D` intervals:
   32 blocks keep one full label, computed with the source's `U` mesh and
   adaptive `V` mesh to 200 digits. Their bands equal `Q_τ(j)`, every
   indicator is 0, `t mod L_0` is constant, and every key lies on one side
   of `X_s`. The 2,480 pairs of blocks within a rule share no key.
4. **Scope.**
   * Every single-label step of the toy is below `55210352`. The modulus
     `1000000007` of rule 1 is a prime, prime to `λ` and above that bound,
     so no step freezes rule 1.
   * An OR is frozen as soon as **one** of its moduli divides `λe'`. On an
     `r = 0` block of step `1201`, with labels checked on the source's
     meshes, the 24 bands are `≡ 140 (mod 1201)`, a value in the cubic's set.
     Rule 3 thus contains the whole block. This is radar-b0's
     counterexample to an earlier wording, reproduced here.
   * "`t − c` is a nonzero square" alone is outside the class for the 44
     primes `5 ≤ ℓ < 200`.
5. **Negative controls, all rejected:** `L_0 = 0` (`f = 1/4`) freezes the
   discriminant; at `r = 0` every block meets `0 mod ℓ`; a start outside the
   stretch breaks the band formula; `T = □_29` violates (G) and has no good
   residue; `τ* + 1` meets an indicator; `b_f + 1` is detected; `L_0 = 17`,
   which does not divide `λe/2`, lets `t mod 17` move.

**Mutation test** (run by hand, not part of `verify.py`). Each of the
following edits of `verify.py` makes it fail:

* `b_f + 1` (3,205 failed checks);
* `L_0/(λe)` in place of `L_0/(2λe)` (2,726);
* `T_s = λe/(2L_0)` (14, at `τ = 104`);
* slope `4λeL_0` in place of `8λeL_0` (128);
* the opposite sign of `κ` (128);
* `σ = σ_0 + τ` (382);
* `Q_τ` without `+τ` (2,838).

The arbiter's three mutations also fail:

* `e = 2^19`, which violates (S2) (3);
* top digit `⌊f*q⌋ − 1` (224);
* `κ` shifted by 1 for the non-residue rule (128).

The finite checks illustrate the lemmas; the proofs are the text above.
