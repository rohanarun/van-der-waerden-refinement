# Dense half of (G♭): in the Haar model, one height split fails for small θ; measurements and the open statement

**Status:** a negative result about one method, with proofs, plus measurements and an open statement. It does not change the status of the rich-side barrier of `2026-10-20-ChaloupeMusic-rich-cover-barrier` (#21): `c ≤ b/4` stays conditional on (G♭)(ii), and on (G♭)(i) beyond `σ₄`.

Three limits apply throughout.
- **The model.** Theorem B is proved for `B` uniform on the torus `R^D/Z^D`. (G♭) concerns `B = ỹ(d)` in the lattice `Λ` of the construction, where the theorem does not apply. A transfer would need a covering radius of `Λ` that is `≪ 1/k` in the relevant projections, and #21 gives only a separation.
- **The method.** The theorem concerns the height split defined in §B: a union bound for small determinant, a first moment in `A` for large determinant, and certificates of fixed rank `m`.
- **The range of `θ`.** It only covers `θ ≲ 1/s_a`, where `s_a = ⌊1/a⌋ + 2`.

**Base commit:** `98e6d36` (#21).

## Question

#21 reduces the rich-side barrier to (G♭), over a family of `N²/4` non-short-period progressions without a repeated V-box. The small-set half of (G♭) is proved up to `σ₄ = ck/((1+b+δ)D)`. Two parts remain open:
- (ii): `rank_J ≥ 2D + 3 − θD` for every `J` of `⌊δk⌋` positions, for every fixed `θ > 0`;
- (i) on `σ₄ < |J| < δk`.

This note addresses (ii). It contains:
- exact facts about relation lattices (§A);
- a proof that, for small `θ` and in the Haar model, one natural height split cannot prove (ii) (§B);
- measurements (§C);
- the missing statement, isolated (§D).

Notation is that of #21:
- `w_t = round(A + tB) ∈ Z^D` for `t < k`;
- `φ_t = A + tB − w_t ∈ C = [−1/2, 1/2)^D`;
- `V_J = span(w_{·,1}|_J, …, w_{·,D}|_J, 1, t)`;
- `d₁(J) = D + 2 − dim V_J`, the number of independent pure relations on `J`;
- the deficit identity `2D + 3 − rank_J = 2d₁ − 1 + dim(V_J ∩ T V_J)` (#21, §5′.1). The quantity `dim(V_J ∩ T V_J) − 1 ≥ 0` is the **mixed term**.

## A. Exact facts about relations

Let `L_J = {g ∈ Z^D : ⟨g, w_t⟩ is affine in t on J}`. For `|J| ≥ 2`:
- the affine coefficients `m₀(g), m₁(g)` are unique and additive in `g`;
- a relation with `g = 0` is trivial;
- so `L_J` is a primitive lattice of rank `d₁(J)`.

Write `G = L_J ⊗ R`, let `π_G` be the orthogonal projection onto `G`, and let `L* = {x ∈ G : ⟨x, L⟩ ⊆ Z}`.

**Lemma A0 (alignment).** Let `L = L_J` with `|J| ≥ 2`, and set:
- `n = max J − min J`;
- `γ = gcd(J − J)`, so that `γ ≤ n/(|J| − 1)`.

Then `γ m₁(g) ∈ Z` for every `g ∈ L`, and there are `μ₀, ℓ* ∈ γ⁻¹L*` such that, with `β = π_G B − ℓ*`, every `t ∈ J` satisfies
- `π_G w_t = μ₀ + tℓ*`;
- `π_G φ_t = π_G A − μ₀ + tβ`.

Moreover `nβ ∈ π_G((−1, 1)^D)`, so `|⟨g, B⟩ − m₁(g)| < ‖g‖₁/n` for every `g ∈ L`.

The same statement and proof hold for any primitive sublattice `L ⊆ L_J`, with `G = L ⊗ R`.

Conversely, if `π_G φ_t` is affine in `t` on `J` for some rational subspace `G`, then `G ∩ Z^D ⊆ L_J`.

*Proof.*
- **The slope lives in `γ⁻¹Z`.** For `t, t' ∈ J`, `m₁(g)(t − t') = ⟨g, w_t − w_{t'}⟩ ∈ Z`. By Bézout, `γ m₁(g) ∈ Z`.
- **The point `ℓ*`.** `γm₁` is a Z-linear form on `L`, so `m₁(g) = ⟨ℓ*, g⟩` for some `ℓ* ∈ γ⁻¹L*`.
- **The point `μ₀`.** `m₀` extends linearly to `G` and is represented by some `μ₀ ∈ G`. Then `π_G w_t = μ₀ + tℓ*` on `J`. Since `π_G Z^D ⊆ L*`, we get `μ₀ = π_G w_t − tℓ* ∈ γ⁻¹L*`.
- **The formula for `φ_t`.** Subtract `π_G w_t` from `π_G(A + tB)`.
- **The bound on `β`.** For the two extreme points `t, t'` of `J`, `nβ = ±π_G(φ_t − φ_{t'})` with `φ_t − φ_{t'} ∈ (−1, 1)^D`.
- **The converse.** `⟨g, w_t⟩ = ⟨g, A + tB⟩ − ⟨g, φ_t⟩` is affine on `J` for every `g ∈ G`. ∎

`γ ≥ 2` really happens. On the single-period instance of §C, `J = {t ≡ 0 mod 5}` has `γ = 5`, every coordinate is affine on `J` with slope `1/5`, and `dist(B₁, Z) ≈ 0.2`. #21, §5′.4 (`gβ_i ∈ Z`) treats this case.

**Lemma A1 (exact gain on the B side).** Let `L` be primitive of rank `m`, with basis matrix `M` (`m × D`), and let `K ⊂ G` be measurable. Let `B` be uniform on the torus. Then
- `Pr[π_G B ∈ L* + K] ≤ det(L) vol_m(K)`;
- equality holds when the translates `λ + K` (`λ ∈ L*`) are disjoint;
- for `K = π_G((−1, 1)^D)/n`, the right-hand side equals `(2/n)^m Σ_{|S|=m} |det M_S|`.

*Proof.*
- **The projection of `Z^D` is exactly `L*`.** The inclusion `π_G Z^D ⊆ L*` holds because `⟨π_G x, g⟩ = ⟨x, g⟩`. Conversely, `L` is a direct summand of `Z^D`, so every Z-linear form on `L` extends to `Z^D`, which gives `L* ⊆ π_G Z^D`.
- **Haar goes to Haar.** Hence `B ↦ π_G B mod L*` is a continuous surjective homomorphism `R^D/Z^D → G/L*`. It pushes Haar measure to Haar measure, and `G/L*` has volume `1/det L`.
- **The volume of `K`.** The zonotope `π_G([−1, 1]^D)` has volume `2^m Σ_S |det M_S| / det L` (projection of a cube, by Cauchy–Binet). ∎

**Lemma A2 (one instant, on the A side).** Let `φ` be uniform on `C` and let `f_L` be the density of `π_G φ`.
- For almost every `y`, `Σ_{λ ∈ L*} f_L(y + λ) = det L`.
- Hence, given `π_G φ ≡ y mod L*`, a fixed representative `y + λ` occurs with probability `f_L(y + λ)/det L`. These are the **label probabilities** of `L`.
- Their supremum `ρ(L)` lies in `[1/det L, 1]`. The lower bound is Vaaler's theorem: central sections of the unit cube have volume at least 1.
- `det L = 1` if and only if `L = Z^S` is a coordinate lattice, and then `ρ(L) = 1`.

*Proof.*
- **The sum is `det L`.** Same argument as Lemma A1, since `φ ↦ π_G φ mod L*` is the same pushforward.
- **`det L = 1` forces coordinates.** If `det L = 1`, then `L* = L` (because `[L* : L] = det(L)²`). So `v = π_G e_i` is an integer vector with `|v|² = ⟨v, e_i⟩ = v_i ≤ 1`, which forces `v ∈ {0, e_i}`. ∎

## B. In the Haar model, a height split cannot prove (ii) for small θ

**The method excluded.** It covers the event "some `J` with `|J| = ⌊δk⌋` has `d₁(J) ≥ m`" by certificates `(L, γ, ℓ₀)`:
- `L` is primitive of rank `m`, `γ ≤ Γ = ⌊(k − 1)/(⌊δk⌋ − 1)⌋`, and `ℓ₀ ∈ γ⁻¹L*`.
- By Lemma A0, a `J` with `L_J ⊇ L` and `gcd(J − J) = γ` forces two things:
  - the event `E_B(L, γ) = {π_G B ∈ γ⁻¹L* + π_G((−1,1)^D)/(γ(⌊δk⌋ − 1))}`;
  - `X_{L,γ,ℓ₀} ≥ ⌊δk⌋` for `ℓ₀ = μ₀`, where `X_{L,γ,ℓ₀} = #{t < k : π_G w_t = ℓ₀ + tℓ*}` and `ℓ*` is a point of `γ⁻¹L*` that `E_B(L, γ)` attaches to `B`.
- A threshold `H` splits the lattices:
  - if `det L ≤ H`, the certificate is paid by the union bound `Σ_γ Pr[E_B(L, γ)]`;
  - if `det L > H`, it is paid by Markov in `A`, as `Σ_{γ, ℓ₀} E[1_{E_B(L,γ)} X_{L,γ,ℓ₀}]/⌊δk⌋`.

**Theorem B.** Let `B` be uniform on the torus and `D = k^a`. Assume:
- `0 < a < 1/2` and `0 < δ < 1`;
- `s` is an integer with `(s − 1)a > 1`, for instance `s = ⌊1/a⌋ + 2`;
- `1 ≤ m ≤ D/(2s)` and `H ≥ 1`.

Then, for every large `k`, the bound that this method gives is at least `(D^s s^{1−s}/(mδk))^m ≥ (2s^{2−s}D^{s−1}/(δk))^m`, which tends to infinity. The same holds at `m = 1` as soon as `sa > 1`.

*Proof.*
- **Reduction to `γ = 1`.** Every term is at least its `γ = 1` part.
- **The levels share exactly `k` instants.** On `E_B(L, 1)` the translates are disjoint (see below), so `ℓ*` is unique and each `t < k` has exactly one level. Hence `Σ_{ℓ₀} X_{L,1,ℓ₀} = k` pointwise.
- **Each term is at least `Pr[E_B(L, 1)]`.** A high term is at least `Pr[E_B(L, 1)] · k/⌊δk⌋`, and a low term at least `Pr[E_B(L, 1)]`.
- **It remains to sum.** Whatever `H` is, the bound is at least `Σ_{L ∈ 𝓛} Pr[E_B(L, 1)]` for every family `𝓛` of rank-`m` lattices.

Take for `𝓛` the lattices spanned by `m` vectors with pairwise disjoint supports of size `s` and entries `±1`.
- **Primitive.** Each is primitive, since its entries are `±1` on disjoint blocks.
- **Distinct.** Distinct families give distinct `G`, because a `±1` vector of support `s` in `G` must be a generator, up to sign.
- **Many.** There are at least `(D^s/(2s^s))^m/m!` of them, because `D − ms ≥ D/2` leaves at least `(D/(2s))^s 2^{s−1}` choices for each generator.
- **Disjoint translates.** `L*` is spanned by the vectors `g_j/s`, so its nonzero points have length at least `1/√s`. The window `π_G((−1,1)^D)/(⌊δk⌋ − 1)` is a box of half-width `√s/(⌊δk⌋ − 1)` along each `g_j/|g_j|`. Its translates are therefore disjoint once `⌊δk⌋ − 1 > 2s`.
- **The B-gain.** Lemma A1, with `Σ_S |det M_S| = s^m`, gives `Pr[E_B(L, 1)] = (2s/(⌊δk⌋ − 1))^m ≥ (2s/(δk))^m`.
- **Conclusion.** Multiply, and use `m! ≤ m^m`. Finally, `D^{s−1}/k = k^{a(s−1)−1} → ∞`. ∎

**Why it fails.** On the B side the gain is exact: `2s/(δk)` per generator of support `s`, against of order `D^s` choices per generator. In expectation, the support-`s` relations that are nearly integral on `B` number `≍ D^s/k ≫ D` once `(s − 1)a > 1`. The first moment in `A` adds nothing, because the levels share exactly `k` instants.

**The range of `θ`.** Excluding `d₁ ≥ θD/2` needs certificates of rank `m ≈ θD/2`. The theorem therefore covers `θ ≤ 1/s`, that is `θ ≲ a/(1 + 2a)`, for every `0 < a < 1/2`. This is the relevant range for the barrier at `b/4`, which needs every `θ > 0`. A fixed `θ₀` would still give `c ≤ (δ + b/2)/(2 − θ₀)` (#21).

**What it does not exclude.**
- Bounds through moments of order `p ≥ 2` in `A`. `Σ_{ℓ₀} E[X^p]` is not fixed by the identity above.
- A deterministic equidistribution argument for the orbit `{A + tB}`.
- Certificates other than relation lattices, or of rank above `D/(2s)`.
- Any argument for `B ∈ Λ`.

## C. Measurements (not a theorem)

Setup:
- `A` and `B` are drawn at random, dyadic of denominator `2^{40}`, and `δ = 1/10`.
- Ranks are computed modulo `2^{61} − 1` and `2^{89} − 1`, taking the larger of the two. Since the rank modulo a prime is at most the rank over Q, every deficit reported is an **upper bound** on the true deficit.
- In the replay of `verify.py`, the maximum, the greedy result and every intersection with a nonzero mixed term are recomputed over Q with exact fractions; no difference was found.

**The measured family.** Relations `g` have:
- support `≤ 3`;
- coefficients `±1, ±2`;
- integer slope `m₁ = round(⟨g, B⟩)`;
- window `|⟨g,B⟩ − m₁| ≤ ‖g‖₁/(δk)`.

The level classes of such a relation are the classes of `⟨g, w_t⟩ − m₁t`.

**Greedy attack.** `J` starts as `[0, k)`. It is repeatedly intersected with the largest level class, among the relations of the family, that keeps `|J| ≥ δk`.

**Single-period instance.** `B_i ≈ 1/5` and `J = {t ≡ 0 mod 5}`. It is degenerate: every coordinate is affine on `J`. It belongs to the progressions that the rank-≥ 4 lemma of #21 removes (an `o(1)` fraction). What fails there is (G♭)(ii), not `c ≤ b/4`. It serves only as a positive witness: the greedy on the measured family (support `≤ 2` suffices, through the relations `e_i − e_j`) finds it, at deficit `2D` over Q (check 5a).

| D | k | a = log D/log k | deficit found (3 seeds) | final \|J\| | single-period instance | 2D |
|---|---|---|---|---|---|---|
| 8 | 1000 | 0.30 | 6, 6, 6 | 126–132 | 16 | 16 |
| 12 | 1000 | 0.36 | 10, 8, 10 | 113–143 | 24 | 24 |
| 16 | 1000 | 0.40 | 12, 12, 12 | 101–117 | 32 | 32 |
| 24 | 1170 | 0.45 | 14, 12, 14 | 123–148 | 48 | 48 |
| 32 | 2200 | 0.45 | 14, 14, 14 | 261–275 | 64 | 64 |
| 40 | 3600 | 0.45 | 14, 14, 16 | 373–475 | 80 | 80 |

`|J|` stays far above `2D + 3`, so these deficits do not come from a lack of room. Each relation keeps about 0.7 of `J`.

**Exact search on the family.** A branch and bound enumerates every intersection of level classes of the family that keeps at least `δk` positions. Its **maximal intersections** are those that no class of the family, of any index, can cut while keeping `δk` positions. The deficit only grows when `J` shrinks, so the maximum over maximal intersections is the maximum over all intersections. The search is exhaustive on this family, and computes the deficit of every maximal intersection.

| D | k | seed | level classes | maximal intersections | exact max deficit | greedy |
|---|---|---|---|---|---|---|
| 8 | 500 | 1 | 398 | 1852 | 8 (\|J\| = 51) | 6 |
| 8 | 500 | 2 | 390 | 1478 | 8 (\|J\| = 51) | 6 |
| 12 | 1000 | 1 | 673 | 5136 | 10 (\|J\| = 104) | 10 |

The exact maximum exceeds the greedy by at most one relation. Nothing is measured for arbitrary `J` outside this family.

The mixed term is not always zero. At `D = 8`, `k = 500`, seed 1, it equals 1 on 3 of the 1 852 maximal intersections, all certified over Q: 2 with deficit 5 and `d₁ = 2`, and 1 with deficit 7 and `d₁ = 3`. `RESULT.json` records the full deficit/`d₁`/mixed histogram.

The contradictor widened the family to the corrected window `‖g‖₁/(⌈δk⌉ − 1)`, coefficients up to `±3` and slopes `p/q` with `q ≤ 10`. On this case the maximum stays 8. The replay is in `RESULT.json` (block `widened`); its leaf count uses the earlier, looser criterion, a superset of the maximal intersections, which does not change the maximum.

**Boxes.** A second attack takes `J = {t : φ_{t,i} ∈ box for i ∈ S}`, for a random `S` and a random box of side `δ^{1/|S|}`. At `D = 12`, `k = 1000`, the worst of 50 draws per seed has deficit 2.

## D. The missing statement

Fix the family `𝓕` of (G♭): at least `N²/4` non-short-period progressions without a repeated V-box. By #21, a family of density at least `k^{−ηD}` with `η < 2` may be used instead.

> **(E_θ).** For every progression in `𝓕`, every rational subspace `G ⊆ R^D` with `dim G ≥ θD`, and every `J ⊆ [0, k)` with `|J| = ⌊δk⌋`, the points `π_G φ_t` (`t ∈ J`) are not of the form `α + tβ`.
>
> **(M_θ).** For every progression in `𝓕` and every `J` with `|J| = ⌊δk⌋`, `dim(V_J ∩ T V_J) − 1 ≤ θD`.

By Lemma A0, (E_θ) is equivalent to `d₁(J) < θD` for every such `J`, and this equivalence goes both ways. The deficit identity then gives two implications, each in one direction only:
- (G♭)(ii) at `θ` implies (E_{θ/2 + 1/D}) and (M_θ), because both terms of the identity are bounded by the deficit;
- (E_θ) and (M_θ), on the same family `𝓕`, together imply (G♭)(ii) at `3θ`.

(E_θ) alone does not imply (ii). (M_θ) is open: it is not proved here, and the measured mixed term is small but not zero. (G♭)(i) beyond `σ₄` is neither treated nor measured here.

Theorem B shows that (E_θ) does not follow, for small `θ` and in the Haar model, from a union over lattices together with a first moment in `A`. We know of no statement that would supply what is missing: a uniform control, over rational subspaces of dimension `θD`, of how often the orbit `{A + tB}` (`t < k`) takes a given label.

## Reproduce

Run `python3 -B verify.py` from this directory. It uses the standard library only and takes about 10 s. The last line must start with `Test passé`. The script checks:
- **0.** Every section except Reproduce, and `RESULT.json` outside its block `verify`, frozen by sha256.
- **1.** Lemma A0 with `γ`, on level classes with slopes `p/q`, `q ≤ 5`. Controls: the integer-slope version is refuted on the single-period instance, and a tenfold-smaller bound fails.
- **2.** Lemma A1, by exact count on a non-orthogonal toy. Control: the formula without the minors is rejected.
- **3.** Lemma A2 (`det 1` gives coordinates), exhaustively on `{−1,0,1}^4`.
- **4.** The evaluation of Theorem B's bound.
- **5.** The replay at `D = 8`, `k = 500`, seed 1: exhaustive search, `d₁` and mixed term of every maximal intersection, rank over Q where stated, greedy, and the witness.
- **6.** That `RESULT.json` equals the computation, and the MANIFEST.

`--write` regenerates `RESULT.json` (block `verify`) and the MANIFEST, and only when every other check passes; any other argument is refused.

The tables of §C come from the numpy scripts in `measure/`:
- `attaque.py 0.1 3 <D:k list>` for the greedy table;
- `exact.py D k 0.1 3 seed 2000000` for the exact table;
- `serie2.py 0.1 4 50 12:1000` for the boxes.

The ranks in these tables are computed modulo the two primes, so they are upper bounds on the deficit and are not certified over Q.

## What is not claimed

- No proof or disproof of (G♭)(ii), (E_θ), (M_θ), or (G♭)(i) beyond `σ₄`.
- Theorem B concerns `B` uniform on the torus, not `B ∈ Λ`. It concerns one method, the height split of §B with certificates of rank at most `D/(2s)`, and so only `θ ≲ 1/s_a`. It says nothing about moments of order at least 2, or about equidistribution arguments.
- The measurements are toy-sized (`D ≤ 40`), restricted to the family named in §C, and certified over Q only where stated.
- The barrier `c ≤ b/4` of #21 remains conditional.
