# Door 1 is a van der Waerden problem on key-measurable colorings

**Status:** structural research note, with proofs of the reduction and
exact finite checks. It answers the "contre-pied" question of sprint 4
(S6): is there an upper bound that forbids `c > 1/8` for **every** frozen
key set, under (I′) and (II′)? Answer. The question is equivalent to a
van der Waerden upper bound for one explicit class of colorings, and
nothing in (I′), (II′) or `b` can supply it. The note locates where any
closure modeled on the random benchmark must go through: two steps, a
density step and a supersaturation step. It gives the state of each one.
No closure and no new bound are claimed.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, through
`pr/door-one` (`00375ff`, published as PR #20).

**Depends on:** `2026-10-26-ChaloupeMusic-exact-door-one-condition`
(Proposition 1, the exact event; Proposition 5, the random first moment) and
`2026-10-26-ChaloupeMusic-ap-free-frozen-sets` (the hitting bound (H), the
template model, and the digit sets).

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-key-measurable-colorings/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. It runs in under a second and uses only the
standard library.

## Setting

The template fixes two maps on `ℤ/N`, `N = k^{ck}` (times `⌊log₂ r⌋` in the
exponent for `r` colors): the label `L(n)` and the key `κ(n)`, with key set
`𝒦`, `|𝒦| = N^{o(1)}`. The method chooses an outer coloring `c₀` of the
labels, which must satisfy the first local-lemma family; call such `c₀`
**admissible**. It also chooses a frozen set `X ⊆ 𝒦` and a rate
`p ∈ (0, 1)`. The final coloring is `c₀(L(n)) ⊕ 1_X(κ(n)) ⊕ E_{κ(n)}`, with
iid Bernoulli(`p`) flips `E` on the keys outside `X`. Iid flips are the case
`X = ∅`.

Call a coloring **good** if no `k`-term progression of `ℤ/N` is
monochromatic. Call `Y` **key-measurable** if it is a set of keys, used as
`1_Y(κ(n))`, that is, a union of fibres of `κ`. The class is

```
𝒞(c₀) = { c₀∘L ⊕ 1_Y∘κ : Y ⊆ 𝒦 }.
```

It has `2^{|𝒦|} = 2^{N^{o(1)}}` members. It is **not** the set of all
colorings of `ℤ/N`, which would turn the question into `W(k)` itself: all its
content is that the coloring is fixed by one bit per key on top of `c₀`.

## Theorem 1 (exact reformulation)

For fixed template data, an admissible `c₀` and `N`, the following are
equivalent.

1. There are a frozen set `X` and a rate `p ∈ (0, 1)` such that the final
   coloring is good with positive probability.
2. `𝒞(c₀)` contains a good coloring.

*Proof.* (1 ⇒ 2) Fix a good outcome. Its coloring is
`c₀∘L ⊕ 1_Y∘κ` with `Y = X Δ {κ ∉ X : E_κ = 1}`. (2 ⇒ 1) If
`c₀∘L ⊕ 1_Y∘κ` is good, take `X = Y` and any `p` with `|𝒦| p < 1`.
With probability at least `1 − |𝒦| p > 0` no key flips, and the final
coloring is the good one. ∎

The method's goal is existence, so positive probability is the right
notion. Its certificates show more: the probability tends to `1`.

**What depends on the iid flips.** Only the certificates do. A given `X`
and `p` define a law on `𝒞(c₀)`: `Y = X Δ F`, with `F` an iid subset of the
free keys. Theorem 2 of `exact-door-one-condition` ((I′), (II′), `2c < θb`)
is a sufficient condition for this law to put mass on good members. The rate
`b`, the thresholds `θ`, `η`, `w`, and the conditions themselves are
properties of that law, not of the class. The class does not see them.

**Corollary.** "`1/8` is the true limit of the method, for every frozen
`X`" is equivalent to the following: for every admissible `c₀`, every
`ε > 0` and `k` large, **every** key-measurable coloring `c₀∘L ⊕ 1_Y∘κ` of
`ℤ/N`, with `N = k^{(1/8+ε)k}`, has a monochromatic `k`-term progression.
That is a van der Waerden upper bound for `𝒞`. In particular, no bound
"forbidding `b > 1/2`" can be the closure. Theorem 2 of
`exact-door-one-condition` has no ceiling on `b` (its Proposition 4.1), and
the class `𝒞` contains `X = ∅` with iid flips at every `b`.

This reading of `b` as a parameter of the law holds **for existence**, that
is, for a definitive closure. Closures of **classes of certificates** need no
van der Waerden bound and already exist: Theorem A of P1b
(`keyed-local-lemma-and-large-moduli`) and Proposition 5 of
`exact-door-one-condition` close given families of laws or certificates
without saying anything about `𝒞`. Only a closure for every frozen `X` at
once is a vdW upper bound for `𝒞`.

## Proposition 2 (each half alone is satisfiable)

Split the progressions into rich ones and the others (cases (i) and (ii),
the "slow words").

1. *Rich alone.* `Y = ∅` gives `c₀`, and `c₀` is `γ`-rich on every rich
   progression, so none of them is monochromatic.
2. *Slow alone.* A uniformly random `Y` makes no slow progression
   monochromatic, with probability `1 − o(1)`. A slow progression is
   monochromatic in `β` only if `Y` takes one prescribed value on each of
   its keys. There are at least `k/2` of these keys, since a key occupies at
   most two positions (Lemma 3 of `source-only-1-16`). That event has
   probability at most `2^{−k/2}`. It depends only on the key word and the
   `c₀`-color word of the progression. Slow progressions have
   `exp(6 log q + O(D log k)) = e^{o(k)}` key words
   (`exact-door-one-condition`, § 2), and their color words are read from
   short-period label words: `e^{o(k)}` of them for `a < 1/2` (labels number
   `e^{k^{2a+o(1)}}`). The union is `e^{o(k)} 2^{−k/2} → 0`.

So a closure must use the **interaction** of the two families. Neither one
alone obstructs anything.

## Proposition 3 (the interaction, exactly)

Let `c₁ = c₀∘L ⊕ 1_Y∘κ`, and for a progression `P` write `Y_P` for the
positions of `P` whose key is in `Y`. Then `P` is monochromatic in `β` under
`c₁` if and only if `Y_P = {c₀ ≠ β} ∩ P` as sets of positions. This is
Proposition 1 of `exact-door-one-condition` with no random flip.

So the Corollary's upper bound reads:

> every `Y` that **properly 2-colors the slow words**, meaning `c₁` makes no
> slow progression monochromatic, contains an **induced class** of some rich
> progression: `Y_P` equals one `c₀`-class of `P`.

This is an induced-configuration statement. `Y` must contain a whole class
of about `k/2` positions and miss the other class entirely.

## The random benchmark, and the two places where it can fail

For `Y` random of density `ρ = k^{−b_Y}`, the expected number of induced
classes on the `N^{2−o(1)}` rich progressions without a two-colored key is
at least `N^{2−o(1)} ρ^{k/2}(1−ρ)^{k}` (`exact-door-one-condition`,
Proposition 5). This tends to infinity once `c > b_Y/4`. A closure that
follows this benchmark needs two inputs.

* **(D) density.** Every `Y` that properly colors the slow words has
  density at least `k^{−b_Y}` along rich progressions, with `b_Y` as small as
  possible.
* **(S) supersaturation.** Every such `Y` has at least `N^{−o(1)}` times the
  random count of induced classes at its density.

Together they close every `c > b_Y/4`. The decomposition is the benchmark's,
not a necessity: a closure could use other structure. But it shows where
each known tool stands.

### (D): what is proved, and what is possible

* **Proved:** density at least `1/(2k)` on every single-label fibre piece,
  from (H) of `ap-free-frozen-sets`. `Y` meets every window of `k`
  consecutive points. With (S), this would close only **`c > 1/4`**
  (`b_Y ≤ 1`).
* **Needed for 1/8:** density `k^{−a−o(1)}` for every `a < 1/2`. Then
  (S) closes `c > a/4`, and `sup a/4 = 1/8` (check 4).
* **Possible, so (D) at `k^{−a}` would be sharp up to `k^{o(1)}`:** a
  uniformly random key set `Y` of density `ρ` is proper as soon as
  `ρ ≥ (2 + δ)H′/k`. Here `H′ = k^{1−a+o(1)}` is the
  log of the number of slow key words. Every slow word has at least `k/2`
  distinct keys, so it is missed with probability `≤ (1 − ρ)^{k/2}` and
  saturated with probability `≤ ρ^{k/2}`. The union bound runs over the
  `e^{H′}` distinct words (this is C1 of the track). The event
  `Y_P = {c₀ ≠ β} ∩ P` also depends on the color word of `c₀`, which the
  key word does not fix, and that is paid in two parts.
  * Case (ii): the run codes of Theorem 8 carry the color of each `s`-heavy
    label, a factor `exp(O(D ln³ k))`, so `H′ = 6 ln q + O(D ln³ k)`.
  * Case (i): at least `(1/2 − ε)δ_s k` light positions of color `≠ β` must
    lie in `Y`, with probability `C(k, x)ρ^x = e^{−Ω(k log k)}`, with no
    color word indexed.

  (Precision of the referee, (s3).) Such a `Y` is
  key-measurable and has density `k^{−a+o(1)}`.
* **Digit sets give hitting only, not properness** (correction of radar-dd,
  S7). The digit set `{x : some base-p digit of x is 0}`, with `p ≤ k`
  prime, meets every progression of length `≥ p`, with density
  `≈ ln Y₀/(k ln k) = k^{−a+o(1)}` at the fibre scale (check 3). But it also
  **contains** whole progressions, for instance every one of step `p`
  starting at a multiple of `p`. In a fibre piece such a block is
  single-label and entirely frozen, hence monochromatic for every draw, so
  the set is not proper. radar-dd proves, for every base, shift and set of
  positions, that such a set saturates some `k`-AP once the fibre piece has
  length at least `8k³`. Digit sets therefore show only that the **hitting**
  half of (D) cannot be pushed above `k^{−a+o(1)}`. No deterministic proper
  `Y` at density `k^{−a}` is known.
* **Literature on hitting sets for `k`-APs in `[M]`** (`f(M, k)`, the
  complement of `r_k`):
  * the lower bound `⌊M/k⌋` is elementary;
  * Brown and Freedman show `f(M, M^ε) ≪_ε M^{1−ε}` (as cited by
    Korsky, arXiv:2606.01780, which treats `k = √M`);
  * Korsky also remarks, without a source, that `f ∼ M/k` for `k = M^α`
    with `α > 1/2`;
  * Fox and Hunter (arXiv:2606.02541, Lemma 2.9) give hitting sets of
    density `ε` for `k ≥ e^{36/ε}` and `M ≤ 2.5^k`, which includes the
    scale `Y₀`. That is density `≥ 36/ln k`, weaker than digits here.
    These are hitting sets; none of them is claimed proper.

  Nothing known gives a lower bound above `M/k` at the scale
  `ln M = k^{1−a+o(1)}`. **(D) at `k^{−a}` is open.** It is a quantitative
  "complement of Szemerédi" statement with `k` growing: every `k`-AP-free set
  in `[M]` misses at least a `k^{−a−o(1)}` fraction, for
  `ln M ≈ c k^{1−a} ln k`.

### (S): where the benchmark is known to fail for APs

Supersaturation at the random count fails for arithmetic configurations. A
Behrend sphere set has no 3-term progression at a density where a random set
has many (check 5: 525 points in `[10⁶]`, zero 3-APs, against 36 expected).
Door 1's hope is exactly a Behrend-type phenomenon for induced classes: a
key-measurable `Y` that is dense on slow words and anti-random on rich
progressions. Known closures rule out parts of it:

* P1a: index-side 3-AP-free mechanisms;
* N2b: algebraic rules of small modulus;
* P1b B2: two-moment rules.

No general (S) is known for configurations of `k/2` points at density
`k^{−a}`. Szemerédi-type counting lemmas lose tower-type factors for fixed
lengths, and give nothing for lengths growing with `k`.

## Answer to S6

* **A definitive closure is not available**, and it cannot come from the
  certificates. By Theorem 1 it is a van der Waerden upper bound for
  key-measurable colorings at `N = k^{(1/8+ε)k}`, uniform over admissible
  `c₀`. This concerns the closure for every frozen `X`. Closures of given
  classes of certificates, such as P1b's Theorem A or Proposition 5 of
  `exact-door-one-condition`, need no such bound.
* **Where the obstruction gives way.** Through the random benchmark, the
  first gap is **(D)**. With the proved transversal density `1/(2k)`, even a
  perfect supersaturation step closes only `c > 1/4`. Reaching `1/8` needs
  the density `k^{−a}` of a proper slow-word transversal. A random key set
  shows that this is the right order up to `k^{o(1)}`, but no one has proved
  it as a lower bound. The second gap
  is **(S)**, where Behrend-type phenomena show that the random count is not
  automatic.
* **Coherent with the rest of the track.** `1/8 = sup a / 4` is the random
  benchmark at the random hitting density, which is Proposition 5 of
  `exact-door-one-condition` read as a property of the class. A Door-1 `X`
  beyond `1/8` would be a key-measurable Behrend-type set. A closure at
  `1/8` would be (D) + (S), or a vdW upper bound of a new kind for `𝒞`.

## What is not claimed

* No closure of Door 1, and no bound on `c`.
* That (D) and (S) are necessary for a closure. They are the steps of the
  benchmark argument. A closure could use other structure of `𝒞`.
* Proposition 2.2 uses the slow-word counts of `exact-door-one-condition`
  and `source-only-1-16` as stated there. The count of color words from
  short-period label words is a sketch at the level of those notes.
* The literature on hitting sets is cited from the abstracts and statements
  of arXiv:2606.01780 and arXiv:2606.02541 (read on 27/10/2026), not
  re-proved.

## Checks in `verify.py`

1. Theorem 1 on 12 random toys (`ℤ/14`, `k = 3`, 7 keys with multiplicity at
   most 2 on every progression, 4 labels). For every frozen `X` and
   `p ∈ {1/7, 1/3}`, with all flips enumerated: the probability of a good
   coloring is positive exactly when some reachable `Y = X Δ F` is good.
   Some `(X, p)` succeeds exactly when `𝒞` has a good member. 2 496 cases.
2. Proposition 3 on the same toys: `P` is monochromatic in `β` iff
   `Y_P = {c₀ ≠ β} ∩ P`. 209 664 cases.
3. Digit transversals meet every progression of length `p` in `[p^L]`,
   checked exhaustively for 5 pairs `(p, L)`; their density is
   `1 − (1 − 1/p)^L` exactly. Each one also contains a whole progression
   (step `p` from `0`): a hitting set, not a proper one. At the scale
   `Y₀` (P1a's model,
   `c = 1/9`), `−log_k` of the density is within `0.02` of `a`.
4. The benchmark thresholds: density `1/(2k)` gives `c > 1/4`; density
   `k^{−a}` gives `c > a/4 < 1/8`.
5. Behrend: a sphere set of 525 points in `[10⁶]` with no 3-AP, against an
   expected 36.2 for a random set of that density.
