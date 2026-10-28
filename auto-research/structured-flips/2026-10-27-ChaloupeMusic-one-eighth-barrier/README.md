# The 1/8 barrier of the frozen-key method, in one statement

**Status:** synthesis note, with two short propositions assembled from
published results and proved here. It states in one theorem what the
`structured-flips`, `short-period-sensitivity` and `trust-reduction` notes
prove about the coefficient `c` of the method. It also says exactly what
object would lift the barrier. Each closed route is given with its statement
and the note that closes it. No new bound on `W_r(k)` is claimed, and the
barrier is a statement about **one method**, not about van der Waerden
numbers (§ 1, Scope).

**Base commit:** `061401f` (PR #22, `research/door-one-continued`), which
contains the notes of PRs #16, #20 and #22. The notes of PRs #14, #19 and #21
are not in this tree. They are cited at the pinned heads listed in
`NOTICE.md`. `line-witnesses` is in this PR.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-one-eighth-barrier/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. Standard library only, under a second. With
`--git`, it also checks the anchors of the out-of-tree notes in the pinned
commits, if they can be reached.

## 1. The method, and the scope of the statement

**The template** (OpenAI source, Sections 2 to 7, in the parameters of
`trust-reduction/…-source-only-1-16`, § 2). Here `N = q^D`, `D = ⌈k^a⌉`,
`ln q = (c + o(1)) k^{1−a} ln k`, and the dilation `λ` is a product of the
prime powers up to `h₀ = D⌈ln k⌉²`. Each `n ∈ ℤ/N` has a label `L(n)` and a
key `κ(n) = (V-box of ỹ(n), ⌊‖qỹ(n)‖²⌋)`. There are `|𝒦| = N^{o(1)}` keys,
and a key occupies at most two positions of a progression (Lemma 3 of
`source-only-1-16`). An **outer colouring** `c₀ = c_*∘L` comes from the
template's local lemma over independent label bits (Proposition 5 there).
Call such a `c₀` admissible.

**The method.** It chooses an admissible `c₀`, a **frozen** key set
`X ⊆ 𝒦` and a rate `p = k^{−b}`. It colours

```
C(n) = c₀(L(n)) ⊕ 1_X(κ(n)) ⊕ E_{κ(n)},     E_κ iid Bernoulli(p) on the keys outside X,
```

and proves, by a **certificate**, that `C` has no monochromatic `k`-term
progression in `ℤ/N` with positive probability. Then `W_2(k) > N = k^{ck}`,
and the source's digit product gives `W_r(k) > k^{ck⌊log₂ r⌋}`. The case
`X = ∅` is the template itself. By the dichotomy (Theorem 6 of
`source-only-1-16`), every progression is **rich** (each outer colour
`≥ γk` times) or **slow**: a short-period word, case (i) or case (ii) of its
Theorem 8.

**What is achieved.** Every `c < 1/8`, explicitly `c = 1/9`, from the
source's proofs alone (#19, `source-only-1-8`, Theorem 9 and § 8). Its region
is `b < a`, `a + b < 1`, `2a < m < 1` and `2c < γb` with `γ < 1/2`. The
certificate is a union bound by sub-prescriptions, with `X = ∅`.

**The exact frozen-key condition.** The conditions (I′_η), (I′_w) and
(II′_θ) of `exact-door-one-condition` (#20, § 2) read "split, or leave
enough to flip", on case (i), case (ii) and rich progressions respectively.
They give every `c` with `2c < θb`, for every `b > 0` (Theorem 2 there), with
no ceiling on `b` (Proposition 4).

**Scope.** The coefficient is the two-colour one, so `r` is fixed (`r = 2`,
then the digit product). It is **not** a ceiling for `W_r(k)`. Fox and
Hunter prove `W_r(k) ≥ r^{(1−ε)k ln k}` for `r ≥ (ln k)^{3/ε}` and `k` large
(Theorem 2 of arXiv:2606.02541, as quoted in the source's introduction).
That is a coefficient `(1 − ε) ln 2 > 1/8` in the normalisation
`k^{ck⌊log₂ r⌋}`, for `r` growing with `k`. Their random shifted products are
not of the form above. Templates of other shapes are priced, at first order
only, in `outside-template-ceilings` (#16). They are outside this statement.

## 2. The statement

Write `𝒞_LL` for the class of local-lemma criteria of
`keyed-local-lemma-and-large-moduli` (#20, Part A): every criterion that reads
only the event–variable incidence and the marginals, and is sound for every
system with that incidence and those marginals. This class contains the
union bound, the asymmetric local lemma, Shearer's criterion, the cluster
expansion, Moser–Tardos and the variable-version local lemma. The
**canonical events** are one event per pair `(P, β)`, with `P` a
progression and `β` a target colour: "`P` is monochromatic in `β`" for
flips, or the failure of (I′)/(II′) at `(P, β)` for a random `X`. They are
indexed by the pair, as in `local-lemma-hub` (#14), even when two of them
coincide.

> **Theorem (the 1/8 barrier).** Fix the template above. The statement is about
> the two-colour coefficient `c` of `W_2(k) > k^{ck}`, hence about a fixed number
> `r` of colours through the digit product. It is not about `r` growing with `k`:
> Theorem 2 of Fox–Hunter (`r ≥ (ln k)^{3/ε}`) is outside its scope (§ 1).
>
> **(A) The region.** The template's asymmetric local-lemma criterion for
> `c₀` fails, whatever its weights, whenever `λ > q/(400k³)`: for every fixed
> `a > 1/2`, and in the window of the Remark of `first-family-circularity`.
> So `a < 1/2`.
>
> **Fixed `a`.** Like the template's region (#19, `source-only-1-16` § 2,
> "Fix rational exponents"), (B) is stated for a fixed `a < 1/2`. Sequences
> `a_k → 1/2⁻` with `ln E = o(ln q)` are **not covered**. Take for instance
> `a = 1/2 − O(ln ln k/ln k)`, so that `ln λ ≍ ln q` while
> `q ≥ 400k³λ` still holds. There, the hub may have `E = O(1)` and gives only
> `b ≤ 1`, hence only `c ≤ 1/4` through K1.
>
> **(B) The certificates.** Fix `a < 1/2`. Suppose a certificate of one of the
> following kinds concludes at `(a, c)` for all large `k`. Then `c ≤ a/4`,
> so `c < 1/8`.
>
> * **K1 (iid flips, local lemma).** `X = ∅`, and a criterion of `𝒞_LL` on
>   the canonical events indexed by `(P, β)`: *unconditional*. With coinciding
>   events merged: *conditional* on (G♭)(ii) (Proposition 1, Remark 3).
> * **K2 (iid flips, union bound by sub-prescriptions).** `X = ∅`, and
>   covers of the coherent rich events, as in every rich estimate of the
>   repository. The bound `b < a` is unconditional. The rich half `c ≤ b/4`
>   is *conditional* on (G♭) of `rich-cover-barrier` (#21), for every
>   `θ, δ > 0`: on part (ii), and on part (i) beyond `σ₄`, where (i) is not
>   proved.
> * **K3 (random frozen set).** `X` has a product law of constant marginal
>   `ρ ≤ 1/2`, there are iid flips at **any** rate `b` on the other keys, and
>   a criterion of `𝒞_LL` on the canonical failure events of (I′) and
>   (II′_θ). Then `c ≤ (1/2 − θ)a/2`. Indexed by `(P, β)`: *unconditional*.
>   With coinciding events merged: *conditional* on (G♭)(ii) (Proposition 2,
>   Remark 3).
>
> **(C) Beyond certificates.** For every `c` and every `k`, the following are
> equivalent.
>
> 1. Some admissible `c₀`, frozen set `X` and rate `p` make `C` good with
>    positive probability at `N = k^{ck}`.
> 2. **(Ω_c)** Some admissible `c₀` and some key set `Y ⊆ 𝒦` make
>    `c₀∘L ⊕ 1_Y∘κ` free of monochromatic `k`-term progressions in `ℤ/N`.
>    In terms of positions: `Y` properly 2-colours every slow progression,
>    and for every rich `P` and every `β`, the positions of `P` whose key lies
>    in `Y` are not exactly the class `{c₀ ≠ β} ∩ P`.
>
> So the method passes `1/8` if and only if `(Ω_c)` holds for some
> `c > 1/8`. "`1/8` is the limit of the method for every frozen set" is a van
> der Waerden upper bound for the class `𝒞(c₀) = {c₀∘L ⊕ 1_Y∘κ}`. It is not
> a bound on `b`.

**Sources of each part.**

* (A) is Proposition 3 and Lemma 2 of `first-family-circularity` (#14). Past
  `a = 1/2` the x-labels are injective, and the first family must balance
  every `k`-AP of `ℤ/N`. The asymmetric criterion fails for every choice of
  weights. The window `q/(400k³) < λ ≤ q/k²` (`a = 1/2 + o(1)`) is its
  Remark.
* K2, flip side: Theorem 1 of `single-label-obstructions` (#14). Every
  sub-prescription union bound totals at least `K(1−p)^k`, and this forces
  `b < a` and `a + b < 1`. By `binding-lever` (#14), `b < a` is the only
  inequality whose relaxation alone moves `sup c`. K2, rich side:
  Proposition 5′ of `rich-cover-barrier` (#21). Every cover bound costs
  `≥ 1` when `c > b/4`, under (G♭). Part (i) of (G♭) is proved up to `σ₄`
  (Lemma "rank ≥ 4"). The note says: "What remains open is (i) on
  `σ₄ < |J| < δk` and (ii)". So K2 needs both.
* K1 and K3 are Propositions 1 and 2 below. Their flip sides are Lemma H and
  Theorem 1 of `local-lemma-hub` (#14). Their rich sides are Theorem A of
  `keyed-local-lemma-and-large-moduli` (#20), applied to the family of
  item 2 of `rich-cover-barrier` (#21).
* (C) is Theorem 1, its Corollary and Proposition 3 of
  `key-measurable-colorings` (#22).

**On `b`.** In K3 and in (C), `b` is free. Proposition 4 of
`exact-door-one-condition` shows that the reduction puts no ceiling on `b`.
Corollary A2 of `keyed-local-lemma-and-large-moduli` closed uniform laws at
`1/8` only for `b ≤ 1`. Proposition 2 removes that restriction, because it
reads the case (ii) side through the hub of `local-lemma-hub`, not through a
block of length `2k − 1`.

**On density.** `(Ω_c)` asks for no density. Necessarily, `Y` has density at
least `1/(2k)` on every single-label fibre piece ((H) of
`ap-free-frozen-sets`, #20). The threshold `k^{−1/2}` belongs to the random
benchmark only. A random-like `Y` of density `k^{−b_Y}` has induced classes
in expectation once `c > b_Y/4` (Proposition 5 of `exact-door-one-condition`),
so passing `1/8` that way needs `b_Y > 1/2`. A random `Y` is proper at
density `k^{−a+o(1)}` (C1, Proposition 7 of `slow-word-transversal-density`).
It cannot be sparser: by Theorem C of `more-keys`, a random `Y` fails (I′) with
high probability unless `b_Y ≤ a + o(1)`.

## 3. The two assembled propositions

Both use the same three published facts.

* **(T) The clique bound.** Theorem A of
  `keyed-local-lemma-and-large-moduli`. If a criterion of `𝒞_LL` certifies,
  then `Σ_{E ∋ κ} μ(E) < 1` for every random key `κ`. Summed over the keys:
  `Σ_E μ(E)·|K(E)| < |𝒦|`, and `ln|𝒦| = o(ln N)` (Corollary A1 there).
* **(H) The hub.** Lemma H of `local-lemma-hub`, for `λ ≤ q/(400k³)`, which
  holds for every fixed `a < 1/2` (Lemma 2 of `first-family-circularity`). It
  gives `E = ⌊q/(64k³λ)⌋` single-label progressions `P_1, …, P_E` through
  one key `κ₀`. Each has `k` distinct keys and constant `c₀ = v`, and their
  key sets are pairwise distinct. Moreover
  `ln E ≥ ln q − ln λ − 3 ln k − ln 67` (Theorem 1 there).
  **The size of `E`.** The dilation is the product of the prime powers up
  to `h₀ = D⌈ln k⌉²`, each at most `2M`. For fixed `a < 1/2`,
  Rosser–Schoenfeld gives `ln λ = O(k^a ln² k)`, while
  `ln q ≥ c k^{1−a} ln k` (Lemma 2 of `first-family-circularity`, second
  bullet, which also gives `q ≥ 400k³λ`). Since `a < 1 − a`,
  `ln λ = o(ln q)`, and so `ln E = (c − o(1)) k^{1−a} ln k`. The `o(1)` is
  slow. At `k = 2^739` and `a = 0.49`, the bound on `ln λ` is still 40 % of
  `ln q`, so `ln E ≥ 0.59 ln q` (check 2). The exponent `b_X` is unaffected:
  it stays within `0.02` of `a`. Here
  `λ = q^{o(1)}`, not `q·k^{−O(1)}`. The latter happens only past
  `a = 1/2`, which (A) excludes. Each `P_e` is a case (ii) progression: its
  single label is heavy, so `k_L = 0`.
* **(F) A rich family.** At least `N(N−1) − N²(1/λ + k²/(2N)) ≥ N²/3`
  pairs `(n₀, d)` have `k` distinct full labels. This is the count in the
  proof of Lemma B1 of `keyed-local-lemma-and-large-moduli`, used in its
  Corollary A2 (2). With no heavy label, such a progression is `γ`-rich
  (Theorem 6 of `source-only-1-16`, first case). Item 2 of
  `rich-cover-barrier` shows that at most `kN²(4/k² + 1/q)^D = o(N²)`
  progressions repeat a V-box. That leaves at least `N²/4` `γ`-rich
  progressions with no repeated V-box, and the count is rigorous. It is
  labelled a sketch in `exact-door-one-condition` and `more-keys` only
  because they reach it through R1 and Theorem 6. The `k` keys of these progressions are
  distinct, since the key contains the V-box. For the majority colour `β`
  of `c₀` on `P`, the minority class `C_{¬β}(P)` has `s ≤ k/2` positions.

**Proposition 1 (K1).** Let `0 < b`, `X = ∅`, and let a criterion of `𝒞_LL`
certify the canonical events of the flips. Then `b ≤ a + o(1)` and
`2c ≤ b/2 + o(1)`, so `c ≤ a/4`.

*Proof.* Flip side: this is Theorem 1(1) of `local-lemma-hub`, the
variable-only case. The `E` events "`P_e` monochromatic in `v`" all contain
`κ₀` and have probability `(1−p)^k`, so `E(1−p)^k < 1`, that is
`k(p + p²) > ln E`, which gives `k^{1−b} ≳ k^{1−a} ln k`. Rich side: every key
is random (`0 < p < 1`). For `P ∈ (F)`, the event "`P` monochromatic in `β`"
asks for the `s` minority keys flipped and the others not, so its
probability is `p^s(1−p)^{k−s} ≥ p^{k/2}(1−p)^k`. By (T),
`(N²/4)·p^{k/2}(1−p)^k·k < |𝒦|`. In logarithms,
`2ck ln k − (b/2) k ln k − 2k^{1−b} < o(k ln k)`. ∎

**Proposition 2 (K3).** Let `X` contain each key independently with
probability `ρ ∈ (0, 1/2]`. Let the flips have any rate, and let a criterion
of `𝒞_LL` certify the canonical failure events of (I′_w), (I′_η) and
(II′_θ), for some `θ > 0`. Then `ρ > ln E/(k + ln E)`, so
`b_X := −log_k ρ ≤ a + o(1)`, and `2c ≤ (1/2 − θ)b_X + o(1)`. Hence
`c ≤ (1/2 − θ)a/2 < a/4`, whatever `b`.

*Proof.* All keys are random, since `0 < ρ < 1`. Every event below is an
event about `X` alone. The flips and their rate `b` do not enter.

*Hub.* At `(P_e, v)`, condition (I′_w) asks that either `X_P` meet
`C_v(P_e) = P_e`, or `C_{¬v}(P_e) \ X_P` carry at least `w ≥ 1` keys. The
second option is empty, since `C_{¬v}(P_e) = ∅`. The threshold `w` depends on
`b`, but this event does not. So the failure is exactly
`{X ∩ κ(P_e) = ∅}`. Its probability is `(1−ρ)^k`, because the `k` keys of
`P_e` are distinct. These `E` events are pairwise distinct (distinct key
sets), and they all contain `κ₀`. By (T), `E(1−ρ)^k < 1`. Since
`ln(1/(1−ρ)) ≤ ρ/(1−ρ)`, this gives `ρ > ln E/(k + ln E) ≥ ln E/(2k)`. With
the size of `E` in (H),
`ln(1/ρ) ≤ ln k + ln 2 − ln ln E = (a + o(1)) ln k`, so `b_X ≤ a + o(1)`.
Only `λ ≤ q/(400k³)` is used, and it holds for every fixed `a < 1/2`.

*Rich side.* By Proposition 5 of `exact-door-one-condition`, the failure of
(II′_θ) at `(P, β)`, for `P ∈ (F)` and `β` the majority colour, contains the
following event. `X` contains the keys of `s − ⌈θk⌉ + 1` chosen minority
positions, and none of the majority keys. Its probability is at least
`ρ^{(1/2−θ)k+1}(1−ρ)^k ≥ ρ^{(1/2−θ)k+1} 2^{−k}`, for `ρ ≤ 1/2`. The exponent
of `ρ` is the density of `X` and not the flip rate: `b` does not enter here
either. By (T), `(N²/4)·ρ^{(1/2−θ)k+1}2^{−k}·k < |𝒦|`. In logarithms,
`2ck ln k − ((1/2 − θ)k + 1)·b_X ln k − k ln 2 < o(k ln k)`.

So the constraint on `c` comes from the law of `X` alone. Theorem 2's
`2c < θb` is a sufficient condition for the flips, and it is not used. ∎

*Where this differs from Corollary A2 of the keyed-local-lemma note.* A2(1)
applies Theorem A to the `k` windows of one block of length `2k − 1`
(Lemma H at `e = 1` only). That gives `k(1−ρ)^k < 1`, so only
`b_X ≤ 1`, and then `c ≤ b/(4(1 + b))`, which exceeds `1/8` for `b > 1`.
Here Theorem A is applied to all `E` steps of the hub through `κ₀`, so
`E(1−ρ)^k < 1` with `ln E = k^{1−a+o(1)}`.

*Where this differs from Theorem C of `more-keys`.* Theorem C bounds the
probability of the good event:
`Pr[(I′) on every single-label block] ≤ exp(−K(ρ^k + (1−ρ)^k))`, for every
`ρ ∈ (0, 1)`. So a random `X` fails (I′) **with high probability** unless
`b_X ≤ 1 − κ ≤ a`. That bound stays positive, and a certificate only has to
show a positive probability. A local lemma does certify such small
probabilities when the bad events are independent, as Theorem C's `K`
key-disjoint blocks are. So Theorem C does not exclude a certificate. What
excludes one is the hub: its `E` events **share** the key `κ₀`, and (T)
caps their total mass at `1`. The two statements give the same exponent,
`b_X ≤ a`. Theorem C speaks of the typical `X`, and Proposition 2 of
certificates in `𝒞_LL`.

*On `ρ ≤ 1/2`.* The hub step holds for every `ρ ∈ (0, 1)`. Only the rich step
uses `ρ ≤ 1/2`.

For `ρ > 1/2`, the factor `(1−ρ)^k` of the rich step is no longer
`e^{−o(k ln k)}`, and the rich step says nothing. The hub step still holds,
but it is empty there, since `ρ > 1/2` already means `b_X < log_k 2`. Other laws are covered as follows.

* A product law with varying marginals is Corollary A3 of
  `keyed-local-lemma-and-large-moduli`. Beyond `1/8`, the certificate
  contains a deterministic set doing door 1's job, up to `N^{2−Ω(1)}` rich
  exceptions.
* For `d`-wise independent laws, see Theorem 1 and Corollary 4 of
  `moment-certificates` (#22).
* For random `X` on refined keys, see Theorem C and Proposition D of
  `more-keys` (#22).

**Remark 3 (merged events).** A criterion may merge canonical events that
coincide as events, for example two rich progressions with the same key word
and the same colour word. The hub events are pairwise distinct, so the flip
sides are unchanged. The rich sides then need **many distinct key words**:
at most `N^{τ+o(1)}` progressions of (F) per key word, for every `τ > 0`.
This is what the count of regime 3 in Proposition 5′ of `rich-cover-barrier`
gives under (G♭)(ii). Here `θ_♭` and `δ` are the parameters of (G♭), not
the `θ` of (II′_θ). Fix `⌊δk⌋` of the keys at their positions. The
progressions carrying them number at most
`k^{δk} e^{O(D log k)} (1 + 4q√D)^{θ_♭ D} = N^{θ_♭ + δ/c + o(1)}`, so
`τ = θ_♭ + δ/c`. So the merged
versions of K1 and K3 are as conditional as K2. Corollary A2 of the
keyed-local-lemma note indexes its events by progressions, as here.

## 4. The ledger of closed routes

In each row, "closes" means that the stated class provably fails, at the
stated scope. The note named is where the statement is proved. In the third
column, `(Ω)` means the closure applies to a witness `Y` of (C) directly, at
`p = 0`. It does so whenever the closure exhibits a single-label block that
is entirely in `Y` or entirely outside it: such a block is monochromatic
under `c₀∘L ⊕ 1_Y∘κ`.

### 4.1 Iid flips (the template's own certificates)

| route | statement | note (PR) |
|---|---|---|
| sub-prescription union bounds | `K ≥ (k²/2−4)^{D−1}q/(20k)` key-disjoint single-label blocks force `b < a`, `a + b < 1` | `single-label-obstructions`, Thm 1 (#14) |
| periodic band flips | flips depending on the band mod `L ≤ q/(400k³λ)`: some progression is monochromatic for every assignment | `single-label-obstructions`, Prop. P2 (#14) |
| which inequality binds | only `b < a` (B) raises `sup c` when relaxed alone | `binding-lever` (#14) |
| first family past `a = 1/2` | injective x-labels; circular; criterion fails | `first-family-circularity`, Prop. 3 (#14) |
| local lemma over the flips | `b < a` for every graph-only or variable-only criterion on the canonical events; re-chosen families are complete (Prop. 2) or contain door 1 (Prop. 3) | `local-lemma-hub`, Thm 1 (#14) |
| rich side, covers | `c ≤ b/4`, conditional on (G♭)(ii) and on (G♭)(i) beyond `σ₄` | `rich-cover-barrier`, Prop. 5′ (#21) |
| rich side, local lemma | `c ≤ b/4` | Proposition 1 here, from (T) and (F) |
| refined keys, one layer | `Pr[success] ≤ exp(−K 2^{1−k})` for every `p`; iid flips need `b < 1 − κ ≤ a` | `more-keys`, Thm A (#22) |

### 4.2 Random or designed frozen sets

| route | statement | note (PR) |
|---|---|---|
| local lemma on a random `X` | any criterion of `𝒞_LL` is a first moment, `Σ_rich μ(B_P) < 4\|𝒦\|/k` | `keyed-local-lemma…`, Thm A, Cor. A1 (#20) |
| uniform product laws | `c ≤ (1/2−θ)a/2` for every `b`, for a constant marginal `ρ ≤ 1/2` and events indexed by `(P, β)` (merged: conditional on (G♭)(ii)) | Proposition 2 here (extends Cor. A2 of #20) |
| varying marginals | beyond `1/8` the certificate contains a deterministic door-1 set, up to `N^{2−Ω(1)}` rich exceptions | `keyed-local-lemma…`, Cor. A3 (#20) |
| first moment of a random-like `X` | certifies nothing beyond `c < b·b_X/(4(b+b_X)) < b_X/4` | `exact-door-one-condition`, Prop. 5 (#20) |
| `d`-wise independence, hashing | moments of order `m` read only `mk`-marginals; certified at least to `γa/4`, never beyond `a/4` | `moment-certificates`, Thm 1, Cor. 4 (#22) |
| second moment, Janson | certifies iff `S₁ − 2S₂/n* < 1`, so only with extreme clustering; Janson bounds only from above | `moment-certificates`, Thms 2, 3, Prop. 6 (#22) |
| more keys for `X` | random `X` fails (I′) with high probability; Lemma R unchanged inside fibres; non-rich price `2^k` | `more-keys`, Thms B, C, Cor. F (#22) |

### 4.3 Deterministic rules

| route | statement | note (PR) |
|---|---|---|
| residue rule `X_ℓ`, `ℓ ≈ √k` | meets, without saturating, every `e = 1` block at `b_X → 1/2`, but is constant on blocks with `ℓ \| e` | `single-label-lenses`, Thm A, Cor. A (#16) |
| periodic band rules, `L ≤ E_max`, square patches | constant on a shifted-squares block `(Ω)` | `single-label-lenses`, Prop. B (#16) |
| algebraic band rules (CRT, characters, sparse polynomials, any truth table) | saturated or untouched blocks below total modulus `q^{1−o(1)}` `(Ω)` | `algebraic-band-rules`, Thm 1, Cors 2, 3 (#16) |
| index-side 3-AP-free `I_X(P)`, quadratic triple (Q) | impossible with (I) for large `k` (Kelley–Meka / Bloom–Sisask) | `ap-free-frozen-sets`, Lemma E, Thm 2 (#20) |
| band-side 3-AP-free sets | closed only if the fibre weights are flat | `ap-free-frozen-sets`, Prop. 4 (#20), **conditional** |
| index-side `ℓ`-AP-free, `4 ≤ ℓ < p₀(k)` | reduced to `W(ℓ, k) ≤ Y₀`; open both ways, closes under (Cl), opens only under (Op) | `ap-free-frozen-sets`, Thm 3 (#20); `off-diagonal-window`, Props 1, 2 (#20), **open** |
| dense rules, literal (II) | fail at every modulus | `keyed-local-lemma…`, Lemma B1, Cor. B1′ (#20); **falls** under (II′): `exact-door-one-condition`, § 4 |
| any rule, pair statistics | exactly the random second moment along progressions | `keyed-local-lemma…`, Lemma B2 (#20) |
| Weil or Deligne along rich progressions | empty by length for `ℓ ≥ q^{1−o(1)}`; for `k·2^{s+1} ≪ ℓ ≲ k²`, no window of bands is polynomial outside an `O(1/m)` fraction | `non-polynomial-bands`, Thm 3, Cor. 4 (#22) |
| digit rules (any base, shift, positions) | on a piece of length `≥ 8k³`, a `k`-AP inside or outside `(Ω)` | `digit-transversals-saturate`, Thm 1, Cor. 1 (#22) |
| rules linear in the base-`q` digits | constant along a slow step unless `Π M_ℓ ≥ (E′+1)^D = N^{1−o(1)}`, with `E′ = ⌊q/(k⁶λ²)⌋` (not the `E` of the hub) `(Ω)` | `digit-transversals-saturate`, Thm 2 (#22) |
| few runs per label (thresholds, few intervals or pieces) | for `b > a`, every working `X` has `q^{1−o(1)}` alternations on a label's band line | `colour-correlated-rules`, Thm C (#22) |
| choosing `c₀` after `X` | free (Prop. A); splits large traces if dangerous traces are `e^{o(M)}` per word (Thm B, B′); a count is necessary in `𝒞_LL` (Prop. E); Warren certifies only `e^{O(log² k)}` intervals | `colour-correlated-rules` (#22) |
| sparse half of Q-S1b | equivalent to the row form of door 1 | `dangerous-traces-scope`, Prop. 1 (#22) |
| splitting every progression | circular: a full vdW colouring | `exact-door-one-condition`, Prop. 4.2 (#20) |

### 4.4 The two steps of the random benchmark

Through the random benchmark, a closure at `1/8` would be a density step (D)
plus a supersaturation step (S). This is not a necessity (§ (D)/(S) of
`key-measurable-colorings`).

| step | statement | note (PR) |
|---|---|---|
| (D), proved | density `≥ 1/(2k)` on every fibre piece, which reaches only `c > 1/4` with a perfect (S) | `key-measurable-colorings`, § (D) (#22) |
| (D), fractional barrier | counting, averaging and LP stop at `1/k`, also inside `𝒞` | `slow-word-transversal-density`, Thms 1, 9 (#22) |
| (D), carry-free boxes | a quadratic set meets every signed line at `O(log p/p)`: boxes cannot prove (D) | `slow-word-transversal-density`, Prop. 6 (#22) |
| (D), digit-linear sets | density `≥ k^{−a−o(1)}`, at the right exponent | `slow-word-transversal-density`, Cor. 4 (#22) |
| (D), witness | random key sets are proper at `k^{−a+o(1)}`; no deterministic proper witness is known | `slow-word-transversal-density`, Prop. 7; `digit-transversals-saturate`, Cor. 1 (#22) |
| (S), range | any proof, adaptive or not, has a range of more than `2^{k/2−3}` witnesses; fixed lines or pieces cannot prove it | `supersaturation-is-global`, Prop. 1, Cor. 1′, Prop. 2 (#22) |
| (S), below `1/8` | some proper `Y` has no induced class at all (inherits the template's conditional status) | `supersaturation-is-global`, Prop. 3 (#22) |
| line witnesses | for fixed `a < 1/2` and fixed `c`, and every `c₀`, a uniform `Y` makes no progression of a line `r + q^{D−1}ℤ` monochromatic, with probability `1 − e^{−(ln 2/2 − o(1))k}`; an argument whose final witness is a line progression (the Lemma E case of the P1a route) proves no upper bound on `𝒞(c₀)`, and no (S) under Prop. 2.2 of `key-measurable-colorings` | `line-witnesses`, Thm A, Cor. A2 (this PR) |

## 5. What is open, as published

* **The object `(Ω_c)`, `c > 1/8`.** A key-measurable colouring that is
  proper on the slow words and has no induced class on the rich ones. By the
  benchmark it must be anti-random on rich progressions: a key-measurable
  Behrend-type set (`key-measurable-colorings`, Answer to S6). No candidate
  is known.
* **(D) at `k^{−a}` for arbitrary sets**, which needs carries between scales
  (`slow-word-transversal-density`, § 5). Inside `𝒞`, a closure must act on
  lenses with `λe` divisible by many primes, or with non-integer slope (§ 6
  there).
* **(S) by arguments that choose their line or piece from `Y`**, the P1a
  route (`supersaturation-is-global`, "What this says about (S)"), with
  witnesses off the lines; line witnesses (Lemma E) are excluded,
  unconditionally for an upper bound on 𝒞 and under Prop. 2.2 for (S)
  (line-witnesses, Cor. A2.3).
* **A rule with few realised dangerous subsets** that passes (I′) (Q-S1b,
  `colour-correlated-rules` § 6). Its dense half lives at the fine scale
  (`dangerous-traces-scope` § 2).
* **Second-moment certificates with extreme clustering**
  (`moment-certificates`, Theorem 3). None is known, and none is excluded.
* **Sparse large-modulus rules.** These are not refuted by the affine
  progressions (`keyed-local-lemma…`, "Where (b) stands"), nor by
  pseudo-random residue sets (`algebraic-band-rules`, "What is not claimed").
* **Conditional closures.** On the rich side, (G♭)(ii), and (G♭)(i) beyond
  `σ₄` for K2 (Remark 3 needs (ii) only). Also flat
  fibre weights for band-side AP-free sets, and the window `4 ≤ ℓ < p₀(k)`.
* **Sequences `a_k → 1/2⁻` with `ln E = o(ln q)`.** In this regime `ln λ`
  is of the order of `ln q`, and the hub gives only `b ≤ 1` (§ 2, Fixed `a`).
  It is not covered by (B). Whether the template's other families exclude
  it is not examined here.
* **Outside this method.** The asymmetric-flip exception of
  `outside-template-ceilings` (an AP-sparse generic hitting set), and the
  regime of growing `r` (Fox–Hunter).

## What is not claimed

* Anything about sequences `a_k → 1/2⁻` with `ln E = o(ln q)`. (B) is stated
  for a fixed `a < 1/2`, as is the template's region.
* No bound on `W_r(k)`, and no ceiling for `W_r(k)`: the statement concerns
  the two-colour coefficient of one method (§ 1, Scope).
* (B) covers the certificate kinds K1 to K3, as defined. A criterion that
  reads the measure, such as the lopsided local lemma on non-monotone events
  or a direct computation of `P(⋂ Eᶜ)`, is outside `𝒞_LL`. A direct
  computation for a deterministic `X` **is** (C).
* K2's rich half is conditional on (G♭)(ii) and on (G♭)(i) beyond `σ₄`. The
  merged versions of K1 and K3 are conditional on (G♭)(ii).
* Propositions 1 and 2 are assembled here from published statements, and
  their proofs are the text above. The facts used ((T), (H), (F), Lemma 3,
  Theorem 6, Proposition 5) are cited, not re-proved. Like every note of the
  track, they rest on the source's lemmas.
* The `(Ω)` marks of § 4 read the cited proofs at `p = 0`. One untouched
  single-label block is already monochromatic there.
* The ledger states each closure at the scope its note gives. A row is not
  stronger than its note.

## Checks in `verify.py`

0. **The statement.** Three sections are frozen by the sha256 of their
   text, recorded in `verify.py`: § 2 (the theorem and its sources), § 4
   (the ledger) and "What is not claimed". Any change to them fails until
   the recorded hash is changed on purpose. Eleven key sentences are also
   checked verbatim: the scope, (A), fixed `a`, (B) with the status of K1, K2 and K3,
   (C), and the conclusions of Propositions 1 and 2. The remaining sections
   (§ 1, § 3, § 5, the checks) are not frozen.
1. **Every reference.** For each note cited, every statement named in § 2
   to § 4 must occur, verbatim, in the README of that note. This gives 121
   anchors in 24 notes.
   * The 92 anchors of the 17 notes in this tree are always checked.
   * The 29 anchors of the 7 notes of PRs #14, #19 and #21 are checked only
     with `--git`, at their pinned commits, and their README hashes are
     compared with those recorded. With `--git`, an unreachable commit is a
     failure. The output and `RESULT.json` give the two counts separately.
2. **Propositions 1 and 2 at the 18 template points** of
   `ap-free-frozen-sets` (`k = 2^739, 2^1024, 2^4096`,
   `a ∈ {0.3, 0.45, 0.49}`, `c ∈ {1/9, 1/4}`), in exact `Decimal`
   arithmetic. The checks are:
   * the scope condition `λ ≤ q/(400k³)` of Lemma H;
   * `ln E ≥ 0.59 ln q`;
   * the forced rate `p` and marginal `ρ`, both `> ln E/(k + ln E)`, with
     exponents `b` and `b_X` within `0.02` of `a`.

   The ceilings `b/4` and `(1/2 − θ)b_X/2` and their margin below `1/8` are
   recorded. That margin follows from `b_X ≤ a + 0.02` with `a ≤ 0.49`, and
   is not an independent test.
3. **The hub inequality, exactly.** On toy stars (`k ≤ 12`, `ρ` on a grid of
   step `1/400`), `E(1−ρ)^k < 1` holds exactly when `ρ > 1 − E^{−1/k}`, and
   the bound `ln E/(k + ln E)` lies below that threshold. A control shows
   that the block of A2(1) (`E = k`) gives only `b_X` close to `1`.
4. **The ledger is closed.** Every row of § 4 cites a checked note or a
   proposition of this note.
5. **Provenance.** The MANIFEST hashes are checked, also under `--write`,
   except for `RESULT.json`, which `--write` regenerates. The summary must
   equal `RESULT.json`. Only `--manifest` rewrites `MANIFEST.json`, together
   with `RESULT.json`.
