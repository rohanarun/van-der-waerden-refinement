# A local lemma on keyed frozen sets is a first moment; large-modulus band rules

**Status:** structural research note, with proofs and illustrative finite
checks. Part A is a negative result: a local-lemma certificate over a random
frozen set is a first moment, and uniform laws stay at `c ≤ 1/8` **when the
flip exponent satisfies `b ≤ 1`** (for `b > 1` Corollary A2 closes nothing
beyond `1/8`). Part B closes dense rules for the literal condition (II),
corrects the statement of the exact condition (II), and explains why sparse
large-modulus rules can be neither proved nor refuted by algebraic means.
**No new bound is claimed.**

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96` (repository),
on top of the `structured-flips` and `template-ceilings` packages of the same
track.

**Depends on:** the door 1 reduction (radar-1a and radar-7b, sprint synthesis
of 20 October 2026, "La sortie qui reste"); radar-7b's fibre proposition
(`piste-C.md` § 2, unmerged); radar-63's Lemma H (LL, `cd1de38`); the source's Sections 2 and 4 to 6 (keys, labels,
outer coloring, multiplicity lemma, affine signature count), pinned in
`source-manifest.json`.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-26-ChaloupeMusic-keyed-local-lemma-and-large-moduli/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
printed before it equal to `RESULT.json`. About ten seconds, standard library
only.

## Setting

`N = q^D`, `D = k^a`, `ln q = c k^{1−a} ln k`, `p = k^{−b}`. Keys are
`κ(n) = (V-word of y(n), ⌊‖q ỹ(n)‖²⌋)`, with key set `𝒦`; every
progression carries at least `k/4` distinct keys (source, multiplicity lemma).
Door 1 freezes `X ⊆ 𝒦`, colours `c₁ = c₀ ⊕ 1_X`, and flips the keys outside
`X` independently with probability `p`. It asks for

* **(I)** every case (ii) progression has a dominant key in `X`, and
  `ω(H/(b log k))` dominant keys outside `X`;
* **(II)** every rich progression has at most `εk` keys in `X`.

The reduction then gives every `c` with `2c < (1/2 − ε) b`. Write `A_w` for
the failure of (I) on the key word `w` (so `A_w ⊇ {X ∩ dom(w) = ∅}`) and
`B_P` for the failure of (II) on `P` (so `B_P ⊇ {|X ∩ κ(P)| ≥ ⌊εk⌋ + 1}`).

## Part A. Choosing X by a local lemma after freezing

**Model.** `X` is a function of independent random variables
`(ω_v)_{v ∈ 𝒱}`; the bit `1[κ ∈ X]` depends on `ω` restricted to
`S_κ ⊆ 𝒱`. A key is *random* when its bit is not constant. An event `E`
about `X` is determined by the bits of a key set `K(E)` (`κ(P)` for `B_P`,
the keys of `w` for `A_w`), hence by `vbl(E) = ⋃_{κ ∈ K(E)} S_κ`. This covers
product laws on the keys, and any law built from finer or coarser independent
seeds.

**The class 𝒞.** A criterion reads the incidence `(vbl(E))_E` and the
marginals `(μ(E))_E`, and is *sound* if, whenever it certifies, every system of
events `E'` determined by `vbl(E)` with `P(E') = μ(E)`, over independent
variables of **arbitrary** distributions, has `P(⋂ E'ᶜ) > 0`. The asymmetric
local lemma (source, Section 4), Shearer's criterion, the cluster expansion
criterion, Moser–Tardos, and the variable-version local lemma
(Kolipaka–Szegedy; He, Li, Liu, Wang, Xia) are all in `𝒞`: each is proved for
every system with the given incidence and marginals.

**Theorem A (clique bound).** If a criterion of `𝒞` certifies, then for
every `v ∈ 𝒱`, `Σ_{E : v ∈ vbl(E)} μ(E) < 1`. In particular, for every random
key `κ`, `Σ_{E : κ ∈ K(E)} μ(E) < 1`.

*Proof.* Suppose the sum is at least 1 for some `v`. Build a system with the
same incidence and marginals: `ω'_v` uniform on the circle `[0, 1)`; the
events `E_1, …, E_r` with `v ∈ vbl(E_i)` become `E'_i = {ω'_v ∈ I_i}`, where
the `I_i` are consecutive arcs of lengths `μ(E_i)` (an event that depends on a
subset of its variables is allowed); every other event `E` becomes
`{ω'_w < μ(E)}` for some `w ∈ vbl(E)`, `ω'_w` uniform (a constant event keeps
its constant value). The arcs have total length at least 1, so they cover the
circle and `P(⋂ E'ᶜ) = 0`, against soundness. For a random key, pick
`v ∈ S_κ`: every event through `κ` uses `v`. ∎

For the asymmetric local lemma itself the bound is one line. On a clique
`E_1, …, E_r` the condition gives
`Σ_i μ(E_i) ≤ Σ_i x_i Π_{j≠i}(1 − x_j) ≤ 1 − Π_j (1 − x_j) < 1`, since the
middle sum is the probability that exactly one of `r` independent
Bernoulli(`x_j`) occurs.

**Corollary A1 (a local lemma is a first moment).** Let `r(E)` be the number
of random keys of `E`. A certified family satisfies
`Σ_E μ(E) r(E) < |𝒦|` (sum Theorem A over the random keys). When every key
is random, each rich `P` has `r(B_P) ≥ k/4`, hence

```
Σ_{P rich} μ(B_P) < 4|𝒦|/k,      log|𝒦| ≤ D ln(2|V|) + ln(Dq²/4 + 1).
```

`log|𝒦| / log N ≤ ln(2|V|)/ln q + 2/D + o(1/D) → 0` for every `0 < a < 1`
(`verify.py`, table A5). A union bound needs `Σ μ(B_P) < 1`; the local lemma
allows `N^{o(1)}`. On the exponent scale (`k ln k`) the two coincide.

**Corollary A2 (uniform laws stay at 1/8 when b ≤ 1).** Let every key be in `X`
independently with probability `ρ = k^{−β}`, and let a criterion of `𝒞`
certify `{A_w} ∪ {B_P}`.

1. *(I) forces β ≤ 1 + o(1).* Take a single-label block of length `2k − 1`
   (radar-63, LL, Lemma H at `e = 1`, in the regime `λ ≤ q/(400k³)` of
   `a < 1/2`: the sweep `(2k − 2)/q` stays in one label and the bands
   `(s + jλ)²` are distinct; checked by the arbiter, sprint 3). Its `k`
   windows of length `k` are case (ii) progressions with constant `c₀`, and
   all of them contain the middle key. Theorem A at that key gives
   `k (1 − ρ)^k ≤ Σ_j μ(A_{w_j}) < 1`. Since `ln(1/(1 − ρ)) ≤ ρ/(1 − ρ)`,
   this gives `ρ > ln k/(k + ln k) ≥ ln k/(2k)`.
2. *(II) forces 2c ≤ εβ + o(1).* At least `N(N − 1) − N²(1/λ + k²/(2N))`
   ordered pairs `(n₀, d)` have `k` distinct full labels (proof of Lemma B1
   below), hence are rich (source, Section 4, balanced outer colouring (i));
   so at least `N²/3` rich progressions. Each has `μ(B_P) ≥ ρ^{⌊εk⌋+1}` (for `ε < 1/4`). Corollary A1
   gives `(N²/3) ρ^{εk+1} < 4|𝒦|/k`, i.e.
   `2c k ln k ≤ (εk + 1) β ln k + o(k ln k)`.

With the rich cost `2c < (1/2 − ε) b`, optimizing `ε` (for `ε ≥ 1/4` the
rich cost alone gives `c < b/8`):
`c < βb / (4(β + b)) ≤ b / (4(1 + b))`. **For `b ≤ 1` this is `c ≤ 1/8`.**
For `b > 1` the bound `b/(4(1 + b))` exceeds `1/8` and tends to `1/4`:
Corollary A2 then closes nothing beyond `1/8`. The synthesis' target "every
`c < 1/4`" is the limit `b → 1`, which suggests that the reduction uses
`b ≤ 1`, but this note does not prove it. The same holds when the marginals
lie in `[k^{−β−o(1)}, k^{−β+o(1)}]`.

**Corollary A3 (what a certificate beyond 1/8 must contain).** For a product
law with marginals `ρ_κ`, put `S = {κ : ρ_κ ≥ k^{−1−δ}}`. If a criterion of
`𝒞` certifies, then

* **(I′)** every single-label block of length `2k − 1` whose middle key is
  random has a window `w` with `Σ_{κ ∈ w} ln(1/(1 − ρ_κ)) > ln k`; the keys
  outside `S` contribute at most `2k^{−δ}` to that sum, so `w` meets `S`
  (if the middle key is surely in `X`, it lies in `S` itself);
* **(II′)** `#{P rich : |κ(P) ∩ S| > εk} < |𝒦| k^{(1+δ)(εk+1)}`, that is
  `N^{ε(1+δ)/c + o(1)}`.

Beyond `1/8` with `b ≤ 1` one needs `ε < 1/2 − 2c < 2c`, so (II′) allows
`N^{ε(1+δ)/c} ≪ N²` exceptions only. A local lemma over a product law
therefore produces nothing but a **deterministic** set `S` that does door 1's
job, up to `N^{2−Ω(1)}` rich exceptions. The randomness buys the exceptions,
not the structure.

**Granularity or intrinsic? (the question left by N3).** N3's cells fail by
Minkowski: a cell with more than `(k − 1)^D` points contains a whole `k`-term
progression, so cell events have probability `e^{−O(k)}`. That mechanism is
one of granularity, and it is gone at the level of keys, since no key occurs
more than four times on a progression. Theorem A is intrinsic. It holds at
every granularity of the randomness, because every event through a key reads
that key's variables. Only `|𝒦|` enters the bound. radar-7b's proposition
(`piste-C.md` § 2) shows that any key map compatible with the case (ii)
estimate has fibres `N^{1−o(1)}` on all but `N/k` elements, so the effective
number of keys is `N^{o(1)}` for every such map, not only for the source's.

The same proof applied to the flips themselves (keys as variables) gives
`Σ_{P rich} P(P mono) < 4|𝒦|/k` for any criterion of `𝒞`. This is a short
rigorous form of radar-7b's "le lemme local sur les flips ne rend rien",
without the degree estimate.

**Scope.** `𝒞` does not contain a direct computation of `P(⋂ Eᶜ)` under the
true measure. For deterministic `X` that computation **is** door 1. Nor does
it contain the lopsided local lemma, which reads the measure: `A_w` (miss
or saturate) is not monotone, so no negative-dependence graph comes for free.
Alteration (sample `X`, then delete the keys of each violated `B_P`) is not
covered by Theorem A. Its usual analysis needs the expected deletions,
`k Σ μ(B_P)`, to stay below the number of keys that (I) cannot spare, which
is again the first moment against `|𝒦|`. That last point is a remark, not a
theorem.

## Part B. Algebraic rules of modulus at least q^{1−o(1)}

**Lemma B1 (density).** Let `δ_X = |κ^{−1}(X)|/N` be the density of `X`
among positions, and `η = 2/λ + k²/N`. If `δ_X > 4ε + η`, some progression
with `k` distinct full labels (hence rich) has more than `εk` keys in `X`:
(II) fails.

*Proof.* Two positions `i < j` with equal full labels have equal `U`-labels in
coordinate `D`. Then `(j − i)d mod N` lies in an arc of `2H_x N + 1` residues,
and since `j − i < k < P` is invertible mod `N`, at most `2H_x N + 1` steps
`d` qualify. Over pairs `(n₀, d)`, `d ≠ 0`, the fraction with a repeated label
is at most `(k²/2)(2H_x + 1/N)·N/(N−1) ≤ η`, using `H_x = 1/(k²λ)`. For fixed
`d`, each `n_j` is uniform, so `Y = #{j : κ(n_j) ∈ X}` has
`E[Y] = kδ_X` exactly. Since `Y ≤ k`, some all-light `P` has
`Y ≥ k(δ_X − η)`, hence at least `Y/4 > εk` distinct keys in `X`. ∎

**Corollary B1′ (residue and character rules; literal (II)).** For `X_c = {(W, t) :
χ_ℓ(t − c) = −1}`, `ℓ` any odd prime, `(1/ℓ) Σ_c δ(X_c) = (ℓ − 1)/(2ℓ)`
exactly: for each band `t`, `(ℓ − 1)/2` shifts make `t − c` a non-residue. So
a proportion at least `1 − (ℓ + 1)/(2ℓ(1 − 4ε − η))` of the shifts fails (II)
outright (a third of them for `ε ≤ 1/32`, `ℓ, λ ≥ 100`). The same holds for
complements, residue rules, and every rule of density bounded below. Measured
on the toy, per shift: `δ ∈ [0.44, 0.51]`. **Dense algebraic rules are
closed for the literal (II), at every modulus.** For the exact condition below
they fail only heuristically. Door 1 wants a sparse `X` anyway.

**Lemma B2 (every rule has the random second moment).** Over uniform
`(n₀, d)` with `d ≠ 0`, the pair `(n_i, n_j)`, `i ≠ j`, is uniform among the
pairs of distinct positions, since `j − i` is invertible. Hence, for every
`X`, algebraic or not, `E[Y] = kδ_X` and
`E[Y(Y−1)] = k(k−1)·|κ^{−1}X|(|κ^{−1}X| − 1)/(N(N−1))`, exactly the values of
a uniformly random set of positions with the same size. The arbiter's remark
that "a modulus `~q` rule behaves like a random `X`" is therefore a theorem up
to order two, for every rule. Any proof of (II) for a sparse rule must use
correlations of order at least three, along every rich progression.

**Proposition B3 (the squares family).** Let `λ ≥ k` and
`n_j = λ^{−1}(a + j) mod N`, with `−q/2 ≤ a` and `a + k − 1 < q/2`. Then the
`k` full labels are distinct (so `P` is rich), and the bands are exactly
`(a + j)²`.

*Proof.* `λ n_j ≡ a + j (mod N)`, so `q ỹ_1(n_j) = a + j` and
`q ỹ_i(n_j) = (a + j)/q^{i−1}` for `i ≥ 2`. The band is
`⌊(a + j)²(1 + q^{−2} + …)⌋ = (a + j)²`, because `(a + j)² < q²/4`. For the
labels, `x_D(d) = (1/N + t)/λ` with `t ≡ −N^{−1} (mod λ)` a unit, so two
indices `j ≠ j'` with `|j − j'| < k ≤ λ` have `x_D` at circle distance at least
`1/λ − k/(λN) > H_x`. ∎

More generally, `λd ≡ s (mod N)` with every prefix `s mod q^i` small gives an
affine `ỹ`, and the labels are all distinct when `gcd(s, λ) = 1`. These
progressions are rich and affine at once, with bands
`(A + j)² + ⌊C + jθ + O(k²/q²)⌋` when `s = 1` (`A` an integer, `C ≥ 0`,
`|θ| ≤ 1`).

**The exact condition (II).** Write `X_P` for the positions of `P` whose key
lies in `X`. Those positions are frozen at `c₁ = c₀ ⊕ 1`; the other keys flip
independently with probability `p`. `P` is monochromatic in colour `β` exactly
when the flips correct the set `{c₁ ≠ β} = {c₀ ≠ β} Δ X_P`. Frozen positions
cannot be corrected, so this needs `X_P ∩ {c₀ = β} = ∅`. It also needs no key
shared between a position to flip and a position to keep, since a key occurs
up to four times and may carry both demands. When both hold, the probability is
`p^{f}(1 − p)^{g}`, where `f` counts the distinct keys of
`{c₀ ≠ β} ∖ X_P`. The danger is therefore `X_P` contained in **either** colour
class of `c₀` on `P` and covering most of it. `X_P` close to the minority side
makes `P` nearly monochromatic in the majority colour. `X_P` close to the
**majority** side switches the majority and makes `P` nearly monochromatic in
the minority colour. The exact (II) asks, for each of the two colours `β`,
either a frozen position of colour `β` (`X_P ∩ {c₀ = β} ≠ ∅`), or enough keys
to flip: `|κ({c₀ ≠ β} ∖ X_P)| ≥ θk`, where `θ` replaces `(1/2 − ε)/4` in
the rich cost (`2c < θ b`, up to the conventions of the reduction). Since
`|κ(S)| ≥ |S|/4` for any set `S` of positions, literal (II) (at most `εk` keys
in `X`, hence at most `4εk` frozen positions) implies the exact (II) with
`|{c₀ ≠ β} ∖ X_P| ≥ γk − 4εk` positions. The converse fails.

Two consequences of Proposition B3:

* any rule containing the squares of a box, for instance "`t` is a square"
  or "`χ_ℓ(t) ∈ {0, 1}`" taken alone, contains every key of some rich
  progression. Literal (II) fails there. The exact (II) holds: `X_P = P` meets
  both colour classes of `c₀` (balanced on `P`), so `P` is monochromatic in
  neither colour. **Literal (II) is strictly stronger than what door 1
  needs**;
* the rich progressions whose bands are algebraic in `j` are the affine ones.
  Their key words number at most `T_aff ≤ C·T_glob·(k(Dq² + 2))³ =
  e^{o(k log k)}` (the source's count of affine signatures, Section 6; a key
  word is a projection of a signature). Counting can never force a sparse rule (density `k^{−β}`, `β > 0`)
  to violate (II) on them: `e^{o(k log k)} k^{−βεk} → 0`. The generic rich
  progressions, the only ones numerous enough (`N²`), have bands
  `⌊q² Σ_i ⟨⟨α_i + jβ_i⟩⟩²⌋` (centred fractional parts, `D = k^a`
  coordinates), a bracket quadratic in `j` with no algebraic handle.

**Where (b) stands.** A sparse rule of modulus `ℓ ≥ q^{1−o(1)}` needs (II)
on windows of length `k = (ln ℓ)^{1/(1−a) + o(1)}`, read along bracket
quadratics. Character sum bounds start at length `ℓ^{1/4+o(1)}` (Burgess) or
`√ℓ` (Weil). Lemma B2 shows that pair statistics carry no information. This
note neither proves nor refutes (II) for such rules. It shows that the
algebraic structure available (affine rich progressions) is too small to
refute it, and that the dense rules fail.

## What is not claimed

* No bound beyond `1/8`, and no claim that door 1 is closed: Theorem A closes
  local-lemma certificates over random `X`, not deterministic `X`.
* Corollary A2's `1/8` uses the rich cost `2c < (1/2 − ε)b` of the reduction
  and `b ≤ 1`. With the radar-99 estimate of about `q⁴` case (ii) words per
  key (unproven), (I) would force `β ≤ a` and give `c < a/(4(1 + a)) < 1/12`.
* Corollary A2 closes uniform laws beyond `1/8` only for `b ≤ 1`.
* Lemma B1 and Corollary B1′ use the literal (II). For the exact (II), dense
  rules fail only heuristically: about `N² 2^{1−k} ≫ 1` progressions have
  `X_P` equal to one colour class of `c₀`. This is not proved.
* Corollary A2 (1) and A3 (I′) use single-label blocks of length `2k − 1`,
  from radar-63's Lemma H at `e = 1` (regime `λ ≤ q/(400k³)`), as checked by
  the arbiter.

## Checks in `verify.py`

* **A1**: 300 exact instances of
  `Σ_i x_i Π_{j≠i}(1 − x_j) ≤ 1 − Π(1 − x_j) < 1`.
* **A2**: 40 random graphs on 3 to 6 vertices containing a clique `K`, 15
  rational vectors each. 189 vectors lie in Shearer's region (independence
  polynomial positive on every induced subgraph, computed exactly), and all
  have `Σ_K p < 1`. All 275 vectors with `Σ_K p ≥ 1` lie outside it.
* **A3**: 200 instances of the covering construction (arcs on a grid circle).
* **A4**: double counting `Σ_P μ(B_P) r(P) = Σ_κ Σ_{P∋κ} μ(B_P)` on the toy
  group (product law `ρ = 1/10`, `B_P = {≥ 2 keys}`).
* **A5**: `log|𝒦|/log N` for `a ∈ {0.2, 0.3, 0.45}`, `c ∈ {1/9, 1/8, 1/5}`,
  `log₂ k ∈ {2⁶, 2¹⁰, 2¹⁴}`: decreasing in `k`, below `0.01`.
* **B** (toy `q = 31`, `D = 2`, `k = 6`, `λ = 12`, the source's `U` and
  adaptive `V` meshes, all 922,560 pairs `(n₀, d)`): key multiplicity at most
  4; repeated-label pairs within the bound; `E[Y] = kδ_X` and
  `E[Y(Y−1)]` equal to the uniform pair value, **exactly**, for nine
  non-residue rules (`ℓ ∈ {37, 101, 211}`); the density lemma's bound; the
  exact shift averages `18/37` and `50/101`.
* **B6** (toy `q = 101`, `k = 6`, with `λ = 12` and with `λ = 40 > k²`): the
  95 progressions `λ^{−1}(a + j)` for each `λ` have six distinct `U` labels
  in coordinate `D` alone, as in the proof, hence six distinct full labels,
  and bands exactly `(a + j)²`.

At toy scale every key is a single position (`|𝒦| = N = 961`) and the density
lemma's bound is below 1. The toy checks the identities, not the asymptotics.
The proofs are the text above.

**Mutation test** (run by hand, not part of `verify.py`). These edits make it
fail: bands `(a + j)² + 1` in B6 (1,140 failed checks); shift average
`(ℓ + 1)/(2ℓ)` (2); clique threshold `9/10` in A2 (19); a `U` mesh coarser
by the factor `λ` (46, all from the `λ = 40` toy, where two terms are
`1/λ < 1/k²` apart in coordinate `D`).
