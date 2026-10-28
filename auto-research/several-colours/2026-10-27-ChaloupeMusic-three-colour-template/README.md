# The template with r colours: W_3(k) > k^{k/7}, relative to the source and PR #19

**Status:** research note, with a complete proof **relative to** the pinned
OpenAI source and the two trust-reduction notes of PR #19, which is **not
merged**. The `1/9` compared below is the repository's own (#19, internal to
this repository), not a published bound. It replays those notes
with an outer colouring and flips that take `r` values, and lists every step
where the number of colours enters. Not reviewed by a human, not formally
verified.

**Result.** Write `c_r = liminf_k ln W_r(k)/(k ln k)`.

> **Theorem.** Assume the source's lemmas and the notes `source-only-1-16`
> and `source-only-1-8` (PR #19, not merged). Fix `r ≥ 2`. For every `c < (1 − 1/r)/4` there is `K_0(r, c)`
> such that, for `k ≥ K_0`, some colouring `ℤ/Nℤ → ℤ/r`, with
> `N = q^D ≥ k^{ck}`, has no monochromatic cyclic `k`-term progression. In
> particular `W_r(k) > k^{ck}`. Explicitly, `W_3(k) > k^{k/7}` for large `k`.

The source gives `c_r ≥ c⌊log₂ r⌋` with `c = 10^{−5}`. The repository's #19
raises the two-colour coefficient to `1/9` (every `c < 1/8`). For the
certificates of `one-eighth-barrier` (#23), at fixed `a`, it is capped at
`1/8`. For `r = 3` the product gives `1/9`, and at most `1/8`. The theorem gives `1/7`, and every `c < 1/6`.

The construction is cyclic, so it composes in mixed base (§ 5). This gives
`c_{3·2^m} ≥ 1/7 + m/9`. Every `r` with `r ≥ 3·2^{⌊log₂ r⌋−1}` gains
`1/7 − 1/9 = 2/63` over `⌊log₂ r⌋/9` (`r = 3, 6, 7, 12, …, 15, 24, …`).
For `r = 4, 5` the product of two-colour colourings stays better: its
`2/9` against the direct `3/16` and `1/5`.

**What is new.** The source is two-coloured by declaration (02-setup, "the
two-color construction"). Its construction uses two colours throughout: the
outer colouring in bits (04-outer), the Bernoulli flips modulo 2
(06-perturbation), the two targets. The **final** number of colours `r` of
`W_r` enters only through the digit product (07-transfers) and through a
separate theorem at fixed `k` (07, "Growth in the number of colors",
`W_r(k) > exp((log r)²/(64 log 2))` for `r ≥ 256`), which does not touch
`c_r`. Nowhere does its `c₀` take more than two values. Fox
and Hunter (arXiv:2606.02541) give nothing at the scale `k ln k` for fixed
`r`; their Theorem 2 needs `r ≥ (log k)^{3/ε}`. As far as R's check of the
texts goes (the referee's reading of Fox–Hunter, Hunter, BCT and Kim), no
published bound gives `c_3` above the product's.

**Base commit:** `e302239` (#23). The two notes replayed,
`trust-reduction/2026-10-26-ChaloupeMusic-source-only-1-16` and
`…-source-only-1-8`, are in #19 (`research/trust-reduction`, head
`84ed864`), not in this tree. They are cited by section and statement.

## Reproduce

```sh
python3 -B auto-research/several-colours/2026-10-27-ChaloupeMusic-three-colour-template/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. Standard library only, about a second.

## 1. The construction

Take every parameter, mesh, label `L(n)`, key `κ(n)` and the modulus
`N = q^D` exactly as in `source-only-1-16`, § 2. (Its `ε_r` is the
regularity constant of that note; it does not depend on the number `r` of
colours.) Labels are written `ℓ`, targets `β`. `q` is a power of a prime
`P ∈ (k, 2k²]`. The changes are two:

* the outer colouring is a map `c_* : 𝓛 → ℤ/r`, and `c₀ = c_*∘L`;
* the flips are independent `E_κ ∈ ℤ/r` with `P(E_κ = 0) = 1 − p` and
  `P(E_κ = v) = p/(r−1)` for `v ≠ 0`, `p = k^{−b}`;

and the colouring is `C(n) = c₀(n) + E_{κ(n)} mod r` on `ℤ/N`. For a
progression and a **target** `β ∈ ℤ/r`, "monochromatic in `β`" prescribes
`E_{κ(n)} = β − c₀(n)` at every position. The **flipped** positions
`P_1(β)` are those with `c₀(n) ≠ β`; they need `E ≠ 0`.

A progression is **γ-rich** if `|P_1(β)| ≥ γk` for **every** `β ∈ ℤ/r`,
that is, `max_β #{j : c₀(n_j) = β} ≤ (1 − γ)k`.

## 2. The steps, one by one

The left column is the step of the two-colour chain; the right column says
what changes at `r` colours, with the proof when something changes.

**Steps with no colour in them.** The parameters, the side-condition table
(`source-only-1-16`, § 2), multiplicity two (Lemma 3: a key occupies at most
two positions of a progression, a geometric fact about keys), Lemma 4
(short-period words through a label), the counts `T_glob`, `T_key` and the
local patterns, the drift, path and long-period lemmas of the source (§ 05),
and the counting of `source-only-1-8` (repeated boxes, discrete data, digit
rank, Lemmas A\* and C\*, the progression count) carry no colour. They are
used unchanged.

### 2.1 Outer colouring (Proposition 5 of `source-only-1-16`)

**Proposition 5_r.** For large `k` (depending on `r`) there is
`c_* : 𝓛 → ℤ/r` such that, in each of the three tested families of
Proposition 5, **each colour** occurs on more than `(1/r − ε)` of the tested
positions: in family 1 on every `S ∈ {S_all, S_out}` with `|S| ≥ δk`; in
family 2 on the regular positions of every eligible pattern; in family 3
(weighted by multiplicities) on the s-light positions of every short-period
word with `k_L ≥ δ_s k`.

*Proof.* Independent uniform `ξ_ℓ ∈ ℤ/r`, one per label `ℓ ∈ 𝓛`. Same events and dependency graph,
with "some colour `v` occurs on at most `(1/r − ε)l` positions" in families
1 and 2, and "`|Σ_ℓ w_ℓ(1[ξ_ℓ = v] − 1/r)| ≥ εk_L` for some `v`" in
family 3. For each fixed `v`, `1[ξ_ℓ = v] ∈ [0, 1]` has mean `1/r`, so
Hoeffding gives `e^{−2ε²l}` in families 1 and 2, and `2exp(−2ε²δ_s M_s)` in
family 3. A union over `r` colours gives `P(E) ≤ r e^{−2ε²l}` and
`P(E) ≤ 2r exp(−2ε²δ_s M_s)`. Keep the weights `z_E = e^{−ε²l}` and
`exp(−ε²δ_s M_s)`, with the same incident weights `ι_1, ι_2, ι_3`: these
count events, not colours. The two final comparisons become
`l(ε² − 2k^{−2}) ≥ ln r` and `exp(−ε²δ_sM_s − 2/k) ≥ 2r exp(−2ε²δ_sM_s)`.
Both hold for large `k`, since `l ≥ min(δM − 1, h₀/2) → ∞`, `M_s → ∞`, and
`r` is fixed. ∎

The condition `2a < m` comes from `ι_1` (`T_glob` against `e^{−ε²δk^m}`) and
does not change. The proof above needs nothing else. A remark, **not proved
here** and not used: necessary constraints of the first family at two
colours have been reported (`D < √(k ln 2)(1 + o(1))`). At `r ≥ 3` the
corresponding lower bound on a bad event would be "colour `v` is absent from
the row", of probability at least `(1 − 1/r)^k`, giving
`D < √(k ln(r/(r−1)))(1 + o(1))`, about `0.64√k` at `r = 3`. That is
stronger than at two colours, but every fixed `a < 1/2` satisfies it, since
`D = ⌈k^a⌉ = o(√k)`.

### 2.2 Dichotomy (Theorem 6)

**Theorem 6_r.** Every cyclic progression with `d ≠ 0` is γ-rich, or it has
the short-period form of Theorem 6, provided

```
γ < (1 − 1/r − (r−1)ε)(1 − ε_r)(1 − δ).
```

*Proof.* Proposition 5_r gives, on each tested set `S`,
`#{c₀ = v} > (1/r − ε)|S|` for every `v`. So for **each** `β`,
`#{c₀ ≠ β} = Σ_{v≠β} #{c₀ = v} > (r−1)(1/r − ε)|S|
= (1 − 1/r − (r−1)ε)|S|`. This is a bound for every target and every
progression, not an average. A progression using only two colours,
half-and-half, would violate it: every non-short-period progression has every
colour at least `(1/r − ε)` times on its tested sets. Theorem 6's proof then
runs verbatim, with the bound above in place of `(1/2 − ε)|S|`:

* no heavy label: `S = S_all` is everything, so `|P_1(β)| > (1 − 1/r − (r−1)ε)k`;
* `h > h₀`: heavy blocks (family 2) and `S_out` (family 1) are disjoint and
  cover at least `k − h` positions, or the heavy blocks alone cover
  `k − h − δk`. So `|P_1(β)| ≥ (1 − 1/r − (r−1)ε)(1 − ε_r)(1 − δ)k − h ≥ γk`;
* `h ≤ h₀`: the short-period form, unchanged (it uses no colour). ∎

At `r = 2` this is `(1/2 − ε)(1 − ε_r)(1 − δ)`, the published cap.

### 2.3 Rich progressions (Theorem 9 of `source-only-1-8`)

**Theorem 9_r.** If `2c < γb`, the probability that some γ-rich progression
is monochromatic tends to zero.

*Proof.* Fix a target `β` and a γ-rich progression. The event prescribes
`E = β − c₀(n) ≠ 0` on `P_1(β)` and `E = 0` elsewhere. A key at two positions
with different prescriptions makes the event empty, as at `r = 2`. Two
positions of `P_1(β)` with different outer colours now count among them,
which only removes events. With `F` the flipped keys,
`|P_1| = 2r' + s`, `|F| = r' + s` (Lemma 3), and `|P_1| ≥ γk`. The proof
of Theorem 9 bounds the event by "these `⌈θ_R k⌉` keys are all flipped" or
by "`|F| > (γ − θ_R)k` keys are flipped". At `r` colours,
`P(E_κ ≠ 0) = p` and `P(E_κ = v) = p/(r−1) ≤ p`, so both bounds hold as
written. In the second branch (`|F| > (γ − θ_R)k` keys with prescribed
nonzero values) there is an extra factor `(r−1)^{−|F|} ≤ 1`, not used. The counts
(Lemmas A\*, C\*) carry no colour. The sum runs over `r` targets instead
of `2`, a factor `r/2`. ∎

### 2.4 Non-rich progressions (Theorem 8 of `source-only-1-16`)

**Theorem 8_r.** Under `b < a` and `a + b < 1`, the probability that some
non-rich progression is monochromatic tends to zero.

*Proof.* Fix a target `β₀`.

* **Case (i), `k_L ≥ δ_s k`.** Proposition 5_r (family 3) puts more than
  `(1 − 1/r − (r−1)ε)k_L ≥ (1 − 1/r − (r−1)ε)δ_s k` s-light positions at
  colours `≠ β₀`. They need `E ≠ 0`, and carry at least half as many
  distinct keys. The event lies in "at least `x` distinct keys of the key word
  have `E ≠ 0`", with `x = ⌈(1 − 1/r − (r−1)ε)δ_s k/2⌉`, of probability
  at most `C(k, x)p^x = exp(−Ω(k log k))`.
* **Case (ii), `k_L < δ_s k`.** As at `r = 2`, record `h`, and for each of
  the fewer than `M_s` s-heavy labels its first and last index and its outer
  colour, now in `ℤ/r`. That is at most `h₀(M_s + 1)(2k²)^{M_s} r^{M_s}
  = exp(O(D log³ k))` codes, since `r` is fixed. With the key word, a code
  fixes the required value of `E` at every s-heavy position. The s-heavy
  positions carry at least `(1−δ_s)k/2` distinct keys. Each key's prescribed
  value has probability `1 − p` (value `0`) or `p/(r−1)` (a nonzero value),
  at most `max(1 − p, p/(r−1)) = 1 − p` since `p ≤ 1/2`. The keys are
  independent, so the event has probability at most `(1 − p)^{(1−δ_s)k/2}`,
  exactly as at `r = 2`.

The sum over `r` targets, `T_key` key words and the codes is

```
A'_k ≤ r T_key (e^{−Ω(k log k)} + e^{O(D log³ k)} e^{−(1−δ_s)k^{1−b}/2}),
```

which tends to zero under `b < a` and `a + b < 1`, as in `source-only-1-16`
(`T_key = exp(6 log q + O(D log k))` carries no colour). ∎

**Why the slow side does not move.** A block of one label (case (ii)) is
monochromatic as soon as no key flips, with probability `(1 − p)^{#keys}`,
whatever `r` is. The constraints `b < a` and `a + b < 1` come from that
event, and from counting key words and codes (`r` enters only as
`ln r · M_s`). The lower bounds of `single-label-obstructions` (#14) also hold
at `r` colours, since `(1 − p)^k` is unchanged, so `b < a` stays necessary.

### 2.5 The output, and composition (§ 07 of the source)

`R_k + A'_k < 1` for large `k`, so some value of the flips gives
`C : ℤ/N → ℤ/r` with no monochromatic cyclic `k`-term progression of nonzero
step. `N = q^D` with `q` a power of `P > k`, so `N/gcd(d, N)` is a power of
`P` for every `d ≢ 0`, hence at least `P > k`: there is no degenerate
progression. Restricting to `{0, …, N−1}` gives `W_r(k) > N ≥ k^{ck}`.

**Mixed base.** Let `C_i : ℤ/N_i → [r_i]` be cyclic colourings with no
monochromatic cyclic `k`-AP, each `N_i` a power of a prime `> k`. Colour
`x ∈ [0, N_0⋯N_{s−1})` by `(C_i(x_i))_i`, where `x_i` are the mixed-base digits.
For `0 < d < ΠN_i`, take the largest `i` with `N_0⋯N_{i−1} | d`, and put
`e = d/(N_0⋯N_{i−1})`. Digits below `i` stay fixed, and
`⌊(a + jd)/(N_0⋯N_{i−1})⌋ = ⌊a/(N_0⋯N_{i−1})⌋ + je`. So digit `i` runs through
a cyclic progression of step `e mod N_i ≠ 0` (maximality of `i`). It is not
monochromatic under `C_i`, so the tuple is not constant. Hence
`W_{Πr_i}(k) > ΠN_i`. This is the source's digit product with mixed
radices; check 5 runs it exhaustively on small cases. Those are outside
the regime of the theorem: they test the composition step only.

## 3. Region and explicit choice

The region at `r` colours is that of `source-only-1-8`, § 8, with the cap of
Theorem 6_r:

```
0 < b < a,  a + b < 1,  2a < m < 1,  0 < (r−1)ε < 1 − 1/r,  0 < ε_r ≤ 1/2,  0 < δ, δ_s < 1,
γ < (1 − 1/r − (r−1)ε)(1 − ε_r)(1 − δ),   0 < c < γb/2.
```

It forces `a < 1/2`, `b < a`, `γ < 1 − 1/r`, so `c < (1 − 1/r)/4`. Every
`c < (1 − 1/r)/4` is reached by letting `ε, ε_r, δ → 0`, `γ → 1 − 1/r`,
`a → 1/2⁻`, `b → a⁻`, `m ∈ (2a, 1)`. The thresholds in `k` are not
explicit, as in #19, and depend on `r`.

**Explicit choice at `r = 3`:** the repository's tuple, with only `γ` and `c`
changed.

| a | m | b | ε = ε_r = δ | δ_s | γ | c |
|---|---|---|---|---|---|---|
| 49/100 | 99/100 | 97/200 | 1/200 | 1/2 | 13/20 | 1/7 |

| inequality | exact margin |
|---|---:|
| `b < a` | 1/200 |
| `a + b < 1` | 1/40 |
| `2a < m` | 1/100 |
| `m < 1` | 1/100 |
| `0 < ε`, `2ε < 2/3` | 1/200 |
| `0 < ε_r ≤ 1/2` | 1/200 |
| `0 < δ, δ_s < 1` | 1/200 |
| `γ < (2/3 − 2ε)(1 − ε_r)(1 − δ)` | 1397/12000000 |
| `c < γb/2` | 827/56000 |

At `r = 2` the same formulas, with `γ = 97/200` and `c = 1/9`, give the
published margins of `source-only-1-8` (cap `40499/8000000`,
`γb/2 − c = 4681/720000`). Check 1 compares them.

## 4. Scope

* **The 1/8 barrier (#23)** is about the two-colour coefficient: "(fixed
  `r`; Fox–Hunter's growing `r` is outside it)", with `c₀` and flips binary.
  The construction here is outside its class (`c₀` and flips in `ℤ/r`), so
  there is no contradiction. The analogue of that barrier for `r` colours
  would cap this method at `(1 − 1/r)a/2 < (1 − 1/r)/4`: `γ ≤ 1 − 1/r` on
  the rich side, `b < a < 1/2` on the slow side. It is not proved here.
* **Fox–Hunter, Theorem 2** (`r ≥ (log k)^{3/ε}`, coefficient
  `≈ (1 − ε) ln r`) is far above `(1 − 1/r)/4` for large `r`. The two
  results do not overlap: fixed `r` here, growing `r` there.
* At `r = 4, 5`, the direct coefficients (`< 3/16`, `< 1/5`) are below the
  product of two two-colour ones (`2/9` explicit, `< 1/4`). The gain is at
  `r` with a factor `3` left over: `r ≥ 3·2^{⌊log₂ r⌋ − 1}`.

## What `verify.py` checks

1. The `r = 2` instance of the region reproduces the published margins of
   `source-only-1-8` exactly.
2. The `r = 3` tuple satisfies every inequality of the region, with the
   exact margins of § 3. `1/7 > 1/8 > 1/9`. The cap is recomputed from its
   proof, as a sum over the `r − 1` other colours, for `r = 2, …, 8`. Each
   margin row of § 3, the tuple row, and the headline statements are read in
   this README and must equal what the check recomputes.
3. For `r ≤ 48`: the best mixed-base sum of the explicit `c₂ = 1/9`,
   `c₃ = 1/7`, against `⌊log₂ r⌋/9`. The gain is exactly `2/63`, at
   `r = 3, 6, 7, 12, …, 15, 24, …, 31, 48`.
4. `max(1 − p, p/(r−1)) = 1 − p` on an exact grid, `p ≤ 1/2`, `2 ≤ r < 20`.
   The passage of Proposition 5 to `r` colours (union over `r` colours, the
   comparisons in `ln r`) is asymptotic, and is proved in the text, not
   checked.
5. The mixed-base product, exhaustively at `k = 4`, outside the theorem's
   regime. Cyclic colourings of `ℤ/11` (2 colours), `ℤ/5` and `ℤ/7`
   (3 colours) without monochromatic cyclic 4-APs are found by search.
   Their products (6 or 9 colours, intervals of 35 to 77) have no
   monochromatic 4-AP of `ℤ`. Control: a constant factor breaks it.
6. Mutants, each of which must be caught: the cap **formula** with `ε` in
   place of `(r−1)ε` (caught by the margin row, and by the cap's proof),
   `c = 1/6` at this tuple, the `r = 3` coefficient at `r = 2`, and `b = a`.

## What is not claimed

* The source's lemmas and the two trust-reduction notes are not re-proved.
  Every step where a colour enters is redone in § 2; the others are used as
  published.
* `K_0(r, c)` is not explicit.
* No barrier at `r` colours is proved (§ 4).
* No claim for `r = 4, 5` beyond the product.
