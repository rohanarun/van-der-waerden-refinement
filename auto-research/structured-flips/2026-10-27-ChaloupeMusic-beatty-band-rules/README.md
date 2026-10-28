# Beatty band rules leave a slow block constant

**Status:** structural research (negative: one class closed, the
one-frequency band rules in the boxes `W` of the aligned family; one
one-way reduction).
Complete proofs, with exact finite checks. Two standard facts of analytic
number theory are cited, not reproved: Weyl's inequality in Vaughan's form,
and the Erdős–Turán inequality. No bound on `c` is claimed.

**The object.** Door 1 succeeds at `c` exactly when the class
`𝒞 = {c₀∘L ⊕ 1_Y∘κ}` has a member with no monochromatic `k`-AP
(`key-measurable-colorings`, Theorem 1). There is no condition on the density
of `Y`. On a single-label block the full label is constant, so `c₀∘L` is
constant too, and the block is monochromatic as soon as `1_Y` is constant on
its keys: `Y` contains all of them (saturates) or none (misses). In
door-1 language, such a block is monochromatic for every flip assignment.

**Scope.** The theorem lives in the boxes `W` reached by the aligned
family: first `D − 1` coordinates at the cell of `0`, last coordinate in a
`V` interval `I_D ⊆ [1/8, 3/8]`. There are `O(k²)` such boxes, one per
`I_D`. A rule that reads one frequency elsewhere but something else on these
boxes is not covered.

**Result.** Suppose that, in one box `W`, the rule of `Y` reads the band `b`
through a single real frequency: `b ∈ Y ⟺ {αb + β} ∈ A`, with
`A ⊆ ℝ/ℤ` a union of `M_A` arcs. Then some slow block of `W` has `Y`
constant on its keys (Theorem 5). This holds for **every real `α`**,
rational or not, with no exceptional set, as long as
`M_A ≤ (q/λ)^{1/7−o(1)}`. Rules of this kind include:

* every residue rule `b mod M ∈ R`, of **any** modulus `M`, whose `R` (or
  complement) has at most `(q/λ)^{1/7−o(1)}` runs of consecutive residues
  (Corollary 6). P2 (#14) closed every rule of the band modulo
  `L ≤ q/(400k³λ)`. N2b (#16) closed the periodic rules and the memberships
  `b mod ℓ ∈ T_ℓ` with each `T_ℓ` square-blind or sparse, for moduli up to
  about `q/(1536k³)`. Above those moduli, residue rules with few runs were
  open;
* the Beatty **rules** `{αb + β} ∈ [0, ρ)` at irrational `α`, which neither
  N2b nor P2 reaches. They are rules, not lenses. The closure goes through
  integer lenses `d²(t+j)²`. The Beatty **lenses** (non-integer slope) that
  `slow-word-transversal-density` (§ 6) left open remain open as a family.

Rules that read **several** frequencies at once are not closed. The proof
goes through unchanged once a simultaneous version of the Diophantine
Lemma 4 holds (§ 7). Among Bohr rules, a random one needs about `k^{1−a}`
frequencies to escape it. Rules of other kinds can escape the aligned family
with no frequency at all: Berlekamp read on `isqrt(b)` does (radar-89, T5;
not proved here).
§ 8 notes a one-way link with the Brown–Freedman function `f(N, k)`: a lower
bound on `f` would give route (D) of the closure.

**Base commit:** `061401f` (`research/door-one-continued`, PR #22).

**Depends on:** Lemma A and Lemma B of
`short-period-sensitivity/2026-10-20-ChaloupeMusic-single-label-obstructions`
(PR #14); Theorem 1 of
`structured-flips/2026-10-27-ChaloupeMusic-key-measurable-colorings` (#22).

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-beatty-band-rules/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. Standard library only, under a minute.

## Setting

As in the source and in PR #14: `q` is a power of a prime `P > k`, with
`gcd(λ, q) = 1`. For `n ∈ ℤ/q^D`, `x_i(n) = n/q^i mod 1` and
`y_i(n) = λn/q^i mod 1`, with `ỹ_i` the representative in `[−1/2, 1/2)`.
The `U` mesh on each `x_i` has intervals of width `H/λ`, `H = k^{−2}`. The
`V` mesh is the source's adaptive mesh; its intervals have length at most
`H`, and those inside `{1/8 ≤ |y| ≤ 3/8}` have length at least `H/32`
(PR #14, Lemma B). The band is `b(n) = ⌊Σ_i (q ỹ_i(n))²⌋`, the key is
`κ(n) = (V-box of ỹ(n), b(n))`, and the full label is `L(n)`. The letter
`t` is reserved for the start of a block.

Fix a `V` interval `I_D = [y_lo, y_hi)` of coordinate `D` inside
`[1/8, 3/8]`, of length `ℓ_V ≥ 1/(32k²)`. Let `W` be the box whose first
`D − 1` coordinates are the cells of `0` and whose last is `I_D`. A rule
`Y` restricted to `W` is a set of bands.

## 1. The aligned family

For `e ≥ 1` put `d = λe`, and for `t ≥ 0` consider the block

```
n_j = q^{D−1} e (t + j),   0 ≤ j < k.
```

**Lemma 1.** Let `T(d) = {t : y_lo ≤ dt/q and d(t + k − 1)/q < y_hi}`. If
`d(k − 1) ≤ q ℓ_V/2`, then `|T(d)| ≥ q ℓ_V/d − k`, and for all but at
most `2k` values of `t ∈ T(d)`, the block `(n_j)` has a constant full label,
lies in the box `W`, and has bands `b(n_j) = d²(t + j)²`.

*Proof.* For `i < D`, `q^{D−1}e(t+j)/q^i` is an integer, so
`x_i(n_j) = y_i(n_j) = 0`. In coordinate `D`, `y_D(n_j) = d(t+j)/q`, which
lies in `I_D` for `t ∈ T(d)`; as `I_D ⊆ [1/8, 3/8]`, `qỹ_D(n_j) = d(t+j)`
exactly. Hence the bands are `d²(t+j)²` (PR #14, Lemma A, with `r = 0`, so
`C = 0`). For the `U` label, `x_D(n_j) = e(t+j)/q`. Over `t ∈ T(d)`, these
values lie in `[y_lo/λ, y_hi/λ)`, of length `ℓ_V/λ ≤ H/λ`, so at most two `U`
boundaries fall there. A block's `x_D` range has length `e(k−1)/q`, and the
starts are spaced by `e/q`, so each boundary spoils at most `k` blocks. ∎

These are P1 blocks (`r = 0`) whose start `s = dt` is a **multiple of the
step**. That alignment freezes the phase of a Beatty rule (Lemma 2); check 4
shows that without it most blocks are mixed.

## 2. The straddle count

**Lemma 2.** Let `Y = {b : {αb + β} ∈ A}`, `A` a union of `M_A` half-open
arcs. Let `d ≥ 1`, `k ≥ 2`, `k² ≤ t_min ≤ t_max ≤ 3t_min`,
`η = ‖αd²‖`, and assume `Δ* = η(k−1)(2t_max + k − 1) ≤ 1`. The number of
`t ∈ [t_min, t_max]` for which `{d²(t+j)² : j < k}` is neither inside nor
disjoint from `Y` is at most

```
2 M_A (L + 2)(3k + 2),     L = η (t_max² − t_min²).
```

*Proof.* Write `αd² = z + η'` with `z ∈ ℤ` and `|η'| = η`. Since `(t+j)²` is
an integer, `α d²(t+j)² + β ≡ ψ(t+j) (mod 1)`, where `ψ(x) = β + η'x²`. If
`η' = 0`, every block is constant. If `η' < 0`, the reflection `x ↦ −x`
sends arcs to arcs, so assume `η' > 0`. The phases of block `t` are
`ψ(t) < ψ(t+1) < … < ψ(t+k−1) ≤ ψ(t) + Δ*`. Two reals `x < y` have different
memberships in the lift of `A` only if some lifted endpoint `ε + w`
(`ε` one of the at most `2M_A` endpoints, `w ∈ ℤ`) lies in `(x, y]`. So a
mixed block has `ψ(t) ∈ [ε + w − Δ*, ε + w)` for some `ε, w`.

For a fixed `(ε, w)`, `ψ` increases by at least `η(2t_min + 1)` per step,
so at most `Δ*/(η(2t_min+1)) + 1 ≤ (k−1)(6t_min + k − 1)/(2t_min + 1) + 1 ≤ 3k + 2`
values of `t` qualify (using `t_min ≥ k²`). The interval `[ψ(t_min), ψ(t_max)]` has
length `L`, so at most `L + Δ* + 1 ≤ L + 2` values of `w` occur for each `ε`. ∎

## 3. Quadratic Dirichlet with a linear target

Write `e(x) = exp(2πix)` and `‖x‖` for the distance to `ℤ`. Three facts are
used:

* **(F1) Dirichlet.** For every real `θ` and `Q ≥ 1` there is
  `1 ≤ r ≤ Q`, `gcd(b, r) = 1`, with `|θ − b/r| ≤ 1/(rQ)`.
* **(F2) Weyl differencing.** For `N` consecutive integers `I` and real
  `θ`: `|Σ_{n∈I} e(θn²)|² ≤ N + 2 Σ_{g=1}^{N−1} min(N, 1/‖2θg‖)`.
* **(F3) The reciprocal-sum lemma** (Vaughan, *The Hardy–Littlewood
  Method*, 2nd ed., 1997, Lemma 2.2 as it is cited in the literature; the
  numbering was not checked against the book). If `|γ − b/r| ≤ r^{−2}` with `gcd(b, r) = 1`, then
  `Σ_{g≤X} min(XY/g, 1/‖γg‖) ≤ C_V XY (1/r + 1/Y + r/(XY)) log(2Xr)`, where
  `C_V` is absolute.
* **(F4) Erdős–Turán** (Kuipers–Niederreiter, *Uniform Distribution of
  Sequences*, Ch. 2, Thm 2.5). For `x_1, …, x_N ∈ ℝ/ℤ`, every interval
  `J = [u, v) ⊆ [0, 1)` and every `H ≥ 1`:
  `|#{n : x_n ∈ J}/N − |J|| ≤ 6/(H+1) + (4/π) Σ_{h=1}^{H} (1/h) |N^{−1} Σ_n e(h x_n)|`.
  The same holds for an arc through `0`, such as `[−δ, δ]`. It is the
  complement of an interval, and the left side is unchanged under taking
  complements.

**Lemma 4.** There is an absolute `C` such that: for every real `α'`,
every integer `E ≥ 2` and every `κ > 0` with `κE ≤ 1/4` and

```
E (κE)³ ≥ C · log E · log²(2/(κE)),
```

some integer `1 ≤ e ≤ E` has `‖α' e²‖ ≤ κ e`.

*Proof.* Let `N = ⌊E/2⌋` (so `N ≥ E/3`), `I = (E − N, E] ∩ ℤ`,
`δ = κE/2`, `H = ⌈6/δ⌉` and `r₀ = ⌊κE²/32⌋`. Then `r₀ ≤ N` and
`2Hr₀ ≤ (24/(κE) + 2) κE²/32 ≤ E`. For each `h ≤ H`, apply (F1) to
`θ_h = 2hα'` with `Q = N²/r₀`: `r_h ≤ N²/r₀` and
`|θ_h − b_h/r_h| ≤ r₀/(r_h N²) ≤ r_h^{−2}`.

*Major arc: some `r_h ≤ r₀`.* Put `m = 2h r_h ≤ 2Hr₀ ≤ E`. Then
`|α' − b_h/m| ≤ r₀/(m N²)`, and `e = m` gives
`α'e² = b_h m + (α' − b_h/m) m²`, so
`‖α'e²‖ ≤ r₀ m/N² ≤ (9/32) κ e ≤ κe`.

*Minor arcs: every `r_h > r₀`.* By (F2) with `θ = hα'` and
`min(N, ·) ≤ min(N²/g, ·)` for `g ≤ N`, then (F3) with `X = Y = N`,
`γ = θ_h`:

```
|S_h|² ≤ N + 2C_V N² (1/r_h + 1/N + r_h/N²) log(2N r_h) ≤ C₁ N² log(2E³) / r₀,
```

where `S_h = Σ_{n∈I} e(hα'n²)`, because `1/r_h < 1/r₀`, `r_h/N² ≤ 1/r₀` and
`1/N ≤ 1/r₀`. By (F4) with `J = [−δ, δ]`,

```
#{n ∈ I : ‖α'n²‖ ≤ δ} ≥ N (2δ − δ − (4/π)(1 + ln H)(C₁ log(2E³)/r₀)^{1/2}),
```

which is positive once `r₀ ≥ C₂ (1 + ln H)² log E / δ²`. That is the
hypothesis, with `C` absolute. Every such `n` has `n ≥ E/2`, hence
`‖α'n²‖ ≤ κE/2 ≤ κn`. ∎

**No exceptional frequencies.** Lemma 4 has no hypothesis on `α'`. The
quasi-rational frequencies, the case where a Beatty rule looks like a residue
rule up to a slow drift, are exactly the major arcs. There a **small** `e`
(a multiple of the denominator) does the job. Check 5 runs it exhaustively at
`E = 3·10⁵`, `κE = 1/30` on adversarial `α'`. That is far outside the proven
regime (`E(κE)³ ≈ 11`): it tests the conclusion, not the lemma. It covers small and huge
denominators (`1/2`, `5/97`, `1/(E²+1)`, `1/E³`), near-rationals
(`1/2 + 1/(3E²)`, `3/7 + 1/(5E)`), quadratic irrationals and random reals,
and some `e` exists in every case. The control at `E = 12` finds an `α'`
with no `e`: the size hypothesis is not idle.

## 4. The theorem

**Theorem 5.** Let `Y ∩ W = {(W, b) : {αb + β} ∈ A}`, with `α, β` real and
`A ⊆ ℝ/ℤ` a union of `M_A ≥ 1` half-open arcs. There is an absolute `C₀`
such that, if

```
q ℓ_V / λ ≥ C₀ · M_A^7 · k^{13} · log³ q        and k ≥ 6,
```

some block of Lemma 1 in `W` has `1_Y` constant on its `k` keys. On that
block, `c₀∘L ⊕ 1_Y∘κ` is monochromatic, for every outer colouring `c₀`.

*Proof.* Put `E = ⌊q ℓ_V/(64 M_A k λ)⌋` and `κ = λ/(10 M_A k q)`, and apply
Lemma 4 to `α' = αλ²`. Here `κE ≤ ℓ_V/(640 M_A² k²) ≤ 1/4`, and
`E(κE)³ ≥ q ℓ_V⁴/(C λ M_A^7 k^7) ≥ q ℓ_V/(C′ λ M_A^7 k^{13})`, using
`ℓ_V ≥ 1/(32k²)`. The log factors are at most `C″ log³ q`, so the
hypothesis of Lemma 4 holds. It gives `e ≤ E` with
`η = ‖αd²‖ = ‖α'e²‖ ≤ κe = d/(10 M_A k q)`, where `d = λe ≤ q ℓ_V/(64 M_A k)`.

On `T(d)`, `t_min ≥ q/(8d) ≥ 8M_A k/ℓ_V ≥ k²` and `t_max ≤ 3t_min`
(since `I_D ⊆ [1/8, 3/8]`). Also
`Δ* ≤ ηkq/d ≤ 1/(10M_A) ≤ 1`, and

```
L ≤ η (t_max + t_min)(t_max − t_min) ≤ η · (3q/(4d)) · (q ℓ_V/d) ≤ (3/40) q ℓ_V/(M_A k d).
```

By Lemma 2, at most `2M_A(3k+2)L + 4M_A(3k+2) ≤ 0.5 q ℓ_V/d + 4M_A(3k+2)`
starts are mixed (`k ≥ 6`). By Lemma 1, at most `2k` are spoiled, out of at
least `q ℓ_V/d − k`. Since `q ℓ_V/(2d) ≥ 32 M_A k > 4M_A(3k+2) + 3k`, a
start remains whose block is single-label in `W` and constant in `Y`. ∎

**In the template.** `ln(q/λ) = (c − o(1)) k^{1−a} ln k` (the scale `Y₀` of
`ap-free-frozen-sets`). The hypothesis therefore holds for every `M_A`
up to `(q/λ)^{1/7 − o(1)}`, that is `exp((c/7 − o(1)) k^{1−a} ln k)` arcs.

**Both outcomes occur.** Theorem 5 gives a constant block. It does not say
which kind, and both happen: a saturated block (all `k` keys in `Y`, so the
frozen block is monochromatic for every flip assignment) or a missed block
(no key in `Y`, so the block has `c₁ = c₀`, constant). Check 3 requires
both among the first constant blocks of its seven rules at `q = 2⁶¹ − 1`
(field `first_constant_in_Y`). There, the saturated one comes from the rule
`α = 1/2` alone; the six others first meet a missed block. Either outcome
excludes `Y` from the good members of `𝒞`.

## 5. Residue rules of any modulus

**Corollary 6.** Let `Y ∩ W = {b : b mod M ∈ R}`, for any `M ≥ 2` and
`R ⊆ ℤ/M`. Let `ρ(R)` be the number of maximal cyclic runs of consecutive
residues in `R`, which is also the number of runs of its complement. If
`q ℓ_V/λ ≥ C₀ ρ(R)^7 k^{13} log³ q`, then some block of `W` has `Y`
constant on its keys.

*Proof.* `b mod M ∈ R ⟺ {b/M} ∈ ∪_{r∈R} [r/M, (r+1)/M)`, a union of
`ρ(R)` arcs. Apply Theorem 5 with `α = 1/M`, `β = 0`. ∎

The two closures fit together:

| modulus | sets `R` closed | source |
|---|---|---|
| `M ≤ q/(400k³λ)` | every `R` | P2 (#14) |
| `M ≤ q/(1536k³)` | periodic rules; memberships with square-blind or sparse `T_ℓ` | N2b (#16) |
| **any `M`** | `R` with at most `(q/λ)^{1/7−o(1)}` runs | Corollary 6 |

**Still open:** residue rules outside P2 and N2b with `R` broken into
more than `(q/λ)^{1/7}` runs. The band range is about `q²`, so such a rule has
`R` cut into pieces shorter than `q^{2 − 1/7}`. A random `R` is of this kind.
Below `1/8`, the template's own random set of flipped keys is a good member
of `𝒞` (`supersaturation-is-global`), so no closure can cover every rule of
this kind at those `c`.

## 6. Where this sits

* **Lenses.** On single-label blocks the bands form lenses
  `⌊θ + vj⌋ + λ²e²j²` (`single-label-lenses`, Lemma 1). The transversal
  note (§ 6) left two families open, lenses with divisible `λe` and Beatty
  lenses. Theorem 5 uses the integer lenses `d²(t+j)²` with aligned starts,
  and shows that one-frequency rules cannot treat them all: a step `e` with
  `αλ²e²` close to an integer, at the right scale, always exists (Lemma 4).
  Any step will do. The theorem does not need `λe` divisible by many primes.
* **S7 (digit transversals saturate).** S7 closes the digit rules on the
  fibre index. Here, on the band, a single digit condition
  `⌊b/p^u⌋ mod p ∈ R'` has the form `{b/p^{u+1}} ∈ A` with `|R'|` arcs, and
  falls under Theorem 5. A **union** over many positions `u` is a
  multi-frequency rule (§ 7).
* **Theorem 2 of S7 (kernel).** It needs moduli `N^{1−o(1)}` for rules that
  read linear forms of the digits. Corollary 6 is of another kind: it closes
  every modulus, provided `R` has few runs.

## 7. Several frequencies: what is missing

Let `Y ∩ W = {b : ({α_i b + β_i})_{i≤r} ∈ U}`, with `U ⊆ (ℝ/ℤ)^r` a union
of `M` boxes. The proofs of Lemma 2 and Theorem 5 apply coordinate by
coordinate. A block is constant if no coordinate's phase arc crosses one of
the at most `2M` face values of that coordinate. They therefore give a
constant block as soon as

```
(Q_r)   some e ≤ E has max_i ‖α_i λ² e²‖ ≤ κ e,
```

with `M_A` replaced by `rM`. Lemma 4 is `(Q_1)`. In the major-arc case of
its proof, a relation `h·α' ≈ b/m` does not make every `‖α'_i e²‖` small,
so the proof does not extend as it stands. Simultaneous small fractional
parts of quadratics are known only with exponents that decay with `r`
(Schmidt's theory). Counting points gives the expected scale: for random
`α_i`, the expected number of `e ≤ E` satisfying `(Q_r)` is about
`E (κE)^r`. It falls below `1` once `r ≳ ln E / ln(1/κE)`, which in the
template is `Θ(k^{1−a})`, the number of digit scales. This counts Bohr
rules only. Below `1/8` a random key set (a limit of Bohr rules with many
frequencies) is a good member.

Two routes to `(Q_r)` were tried (with radar-d2).

* **Nesting fails at `r = 2`.** Take `e = e₁e₂⋯e_r`, with each `e_i`
  given by Lemma 4 for one coordinate. A coordinate already handled has its
  error multiplied by `e_j²` at every later step. Lemma 4 only gives a
  precision of about `E_i^{−1/3}`, and no lower bound on `e_i`. With
  `ε_i = log E_i / log E`, the linear target then forces, **in the worst
  case over the earlier `e_j`** (each equal to `1`),
  `4ε_i ≥ 3(1 + Σ_{j>i} ε_j)`. That means `ε_r ≥ 3/4`, and then
  `ε_{r−1} > 1`: impossible. If the earlier `e_j` had their full size, the
  constraints could be met (for instance `ε = (13/14, 1/14)` at `r = 2`),
  but Lemma 4 does not give that.
* **Erdős–Turán–Koksma in dimension `r`.** For a box of side `δ` it needs
  frequencies up to `H ≈ δ^{−r}`. A major-arc step loses `H²`, so `δ`
  becomes about `δ^{2r+1}`. By our estimate, which is not proved here, this
  route gives at best `r ≲ ln k / ln ln k`. A box minorant of degree about
  `r/δ` (Barton–Montgomery–Vaaler type) might do better; it was not checked.

**Not claimed:** `(Q_r)` for `r ≥ 2`, and the closure of rules with two or
more frequencies. The heuristic says the line between closed and open runs at
about `k^{1−a}` frequencies for Bohr rules, not at `2`.

## 8. Route (D) of the closure: a one-way link with `f(N, k)`

This section concerns the **closure** route (D)+(S) of
`key-measurable-colorings`, not the object above. A good member of `𝒞` may
have any density. It must still meet every slow block, since a missed block
is monochromatic. By Lemma R of `single-label-lenses`, in every box of the
P1 region, at least 9/10 of the points lie in pieces where `Y` has density
at least `f(Y₀, k)/(2Y₀)`. Here `f(N, k)` is the least size of a set
meeting every `k`-term progression of `{0, …, N−1}` (Brown and Freedman,
J. Combin. Theory Ser. A 51 (1989) 244–249).

* **The direction proved.** A lower bound on `f` gives (D):
  `f(Y₀, k) ≥ Y₀ k^{−a−o(1)}`, at `ln Y₀ = (c − o(1)) k^{1−a} ln k`
  (that is, at `L = log_k Y₀ = (c − o(1)) k^{1−a}` scales), implies the
  density lower bound that route (D) needs. Equivalently, a key-measurable
  transversal of density `k^{−b}` would give `f(Y₀, k) ≤ (20/9) k^{−b} Y₀`
  (9/10 of the points, at density at least `f(Y₀, k)/(2Y₀)`).
* **The converse is not proved.** It would need to realise every
  transversal of `[Y₀]` as a key-measurable `Y` that is proper on all pieces
  at once. The keys are shared between fibres, so this does not follow. (D)
  may therefore be easier than the bound on `f`.
* **What is known about `f`.** `f(N, k) ≥ ⌊N/k⌋` (disjoint windows). Digit
  sets give `f(N, k)/N ≈ L/k` with `L = log_k N` scales, for `L < k`. At two
  scales, Truss (1991) proved `f(n², n) > n + √n/2 − 2`. Korsky
  (arXiv:2606.01780, v2 of 8 October 2026) proves `f(n², n) ≥ n + n^{1−o(1)}`
  and `f(p², p) ≤ 2p − (√2 − o(1))√(p/log p)`. He conjectures
  `f(n², n) = (2 − o(1))n` (Conjecture 1.3, stated in the paper, v2; not in
  the abstract).

So a bound that makes the scales of `[k^L]` add, at `L ≈ k^{1−a}`, would
suffice for (D). This is a sufficient condition, not a statement of
difficulty.

## What `verify.py` checks

1. Lemma 1 at 306 positions (`(q, D) = (10007, 3), (1009, 4), (65537, 2)`):
   computed from the coordinates with exact fractions, the band is
   `d²(t+j)²`.
2. Lemma 2 on 150 random rules and steps, all inside its regime
   (`α` built so that `Δ* ≤ 1`). The number of mixed blocks never exceeds
   the bound, and the bound is below the number of starts in some of the
   cases, so the check is not empty.
3. Theorem 5 inside its regime: `q = 2⁶¹ − 1`, `λ = 31`, `k = 6`, and
   `I_D = [1/8, 1/8 + H)`, an interval of length `H = 1/k²` (the adaptive `V`
   mesh is not built; the label is not recomputed, Lemma 1 is a proof). Seven
   rules: golden ratio (denominator about `10⁴⁰`), `√2`, random three-arc,
   `α = 1/2`, `1/7 + 10^{−30}`, and two residue rules of modulus about
   `q²/500` (three residues; half of them). The witness steps `e` come from
   a sampling search (`verify.py --search`). For each one, every hypothesis
   is checked exactly: `η ≤ d/(10M_A k q)`, `d ≤ qℓ_V/(64M_A k)`,
   `t_min ≥ k²`, `t_max ≤ 3t_min`, `Δ* ≤ 1`. Over all aligned starts in
   `T(d)` (the first 50 000 when there are more: the near-rational rule's
   witness is a small `e`, from a major arc), the mixed blocks are counted. Their number is at most the bound of
   Lemma 2, and more than `2k` starts give constant blocks. Both outcomes
   occur among the first constant blocks (required by the check; the
   saturated one is the rule `α = 1/2`).
4. Control: on starts `s` that are not multiples of `d`, the generic rules
   (golden ratio, `√2`, three arcs) give mixed blocks in 302, 302 and 358
   of 400 random starts (75 % to 90 %); the near-rational rule in 24. Alignment is
   what freezes the phase.
5. Lemma 4, exhaustive at `E = 3·10⁵`, `κE = 1/30`, for 11 adversarial
   `α'`. Control: at `E = 12`, `α' = 12/4001` has no `e`.

## What is not claimed

* Nothing about rules that read two or more frequencies jointly (§ 7),
  random-like rules, or residue rules whose `R` has more than
  `(q/λ)^{1/7}` runs outside P2 and N2b.
* No good member of `𝒞` is excluded beyond the rules stated, and none is
  constructed.
* § 8 is a one-way implication (a bound on `f` gives (D)). Nothing is
  proved about `f(N, k)`.
* The constants `C, C₀` are absolute but not computed. They come from the
  reciprocal-sum lemma (F3). Check 3 verifies the hypotheses of Lemmas 1–2
  directly on the `e` found, not through `C₀`.
* The direction "(D) implies a bound on `f`" (§ 8).
* No bound on `c`.
