# Every c < 1/16 (explicit 1/17) from the source's proofs alone, replayed

**Status:** research note with a complete proof relative to the pinned OpenAI
source. Prepared with Claude (Anthropic). Not reviewed by a human, not formally
verified.

**Result.** For every fixed `c < 1/16` there is `K_0`, independent of `r`, with

```math
W_r(k)>k^{ck\lfloor\log_2 r\rfloor}\qquad(k\ge K_0,\ r\ge2).
```

The explicit choice is `c = 1/17`. That is `100000/17 ≈ 5882` times the source's
`1/100000`. It is smaller than the repository's `1/9`, but it rests on a much
smaller base:

* the proofs of the OpenAI source (Sections 02 to 07), replayed under the
  inequalities of §2 below: with other values of `D, M, h_0, η` and with
  condition (i) of eligible patterns strengthened. §2 lists every place where
  the source's numerical values enter, and the inequality that replaces them;
* nothing else. The arguments added to the source are proved in full here.

In particular the proof uses **none** of the repeated-key, rank-certificate or
digit-rank chain (PRs #4, #6, #7: common returns, affine collision classes,
literal certificates, Lemmas A\*, C\*, facts R1 to R5). It also does not
import the "sharpened outer input" as an assertion: §4 and §5 prove it.

## 1. What "conditional" means in this repository

No refinement in this repository depends on a named conjecture or an unproved
hypothesis. "Conditional" (README lines 1, 5, 111, 273; PR #10,
`formal/CONDITIONAL-REVIEW.md`) means **conditional on correctness**: the
source's lemmas are assumed as stated, and each refinement adds arguments that
have only been reviewed by AI-assisted source reviews. The headline `1/9`
depends on five links:

| Link | Content | Where | Status before this note |
|---|---|---|---|
| (S) | Source geometry, counting, outer local lemma, dichotomy, perturbation, digit product | OpenAI §02–07 | Claimed theorem of the source (unrefereed preprint) |
| (P2) | A key occurs at most twice on a progression | merged PR #2 | Elementary; kernel-checked in PR #10 (`Geometry.lean`) |
| (O) | Sharpened outer input: `γ < (1/2−ε)(1−ε_reg)(1−δ)` | `sharpened-region-proof.md` | Argued as three changes to the source; **imported** by later notes ("precisely stated", `repeated-key-certificate-proof.md` l. 527) |
| (R) | Runs (Lemma 1), short-period word count (Lemma 2), third local-lemma family, two-case non-rich estimate | `short-period-runs-proof.md` | Argued; audit 2026-10-20: four non-blocking imprecisions (M1–M4) |
| (K) | Rich-event estimate `2c < γb` | PR #4, `rank-certificate-proof.md`, `digit-rank-proof.md` | Argued; PR #10 conditional review: pass |

So the question "is the condition provable" has no single answer: each link is
a claimed proof, to be checked, not a hypothesis to be established. This note
does three things:

1. It proves (O) and (R) completely, as one outer coloring with three event
   families and one non-rich estimate, with every source lemma quoted and its
   parameter transfer checked. M1 and M2 of the earlier audit are repaired in
   place (§4.3, §7).
2. It proves (P2) in four lines (§3), so it imports nothing from PR #2.
3. It shows that (K) is **not needed for any `c < 1/16`**: the source's own
   rich estimate, with multiplicity two, gives `2c < γb/2`. Combined with
   (R), which removes `2a < 1 − b`, this gives `c < γb/4 < 1/16`.

Thus everything below `1/16` depends on (S) only, and the remaining factor
`16/9` up to `1/9` depends on (S) plus (K).

**Relation to the `1/24` ceiling.** The README of `main` (section "Why
`1/24` is a ceiling of this architecture", after `barrier-note.md`) bounds
every argument of one template by `1/24`. That template pays the affine case
with a union bound over affine signatures, which costs the `k^{2a}` label
entropy and forces `2a + b ≤ 1`. §7 below does not count signatures: non-rich
progressions are paid by their key words and run codes, which needs only
`a + b < 1`. The template's hypotheses therefore fail here, and there is no
contradiction. On `main`, `1/24` was the best coefficient not using (K); this
note raises it to every `c < 1/16`.

## 2. Parameters, and the source lemmas reused

Fix rational exponents and constants

```math
0<b<a,\quad a+b<1,\quad 2a<m<1,\quad 0<\varepsilon<\tfrac12,\quad 0<\varepsilon_{\rm r}\le\tfrac12,\quad 0<\delta,\delta_s<1,
```

```math
0<\gamma<(\tfrac12-\varepsilon)(1-\varepsilon_{\rm r})(1-\delta),\qquad 0<c<\gamma b/4 .
```

The inequality `a + b < 1` follows from the others; it is listed because §7
uses it.

Put `D = ⌈k^a⌉`, `M = ⌈k^m⌉`, `L = ⌈log k⌉`, `h_0 = M_s = D L²`, `p = k^{-b}`,
`H = k^{-2}`, `η = ε_r/(8D)`. Define `λ`, the prime `P ∈ (k, 2k²]`, `q`,
`N = q^D`, `G = Z/NZ`, the coordinates `x_i, y_i`, the representatives
`x̂ ∈ [0,1)^D`, `ỹ ∈ [−1/2,1/2)^D`, `H_x = H/λ`, `α = q^{−(D+1)}`, the meshes
`U, V`, labels `L(n)`, keys `κ(n)` and `f(n)` exactly as in source §02 and §06,
with these values. "Light" and "heavy" refer to multiplicity `≤ k/M` and
`> k/M` in the progression (source §04). All statements are for `k` larger
than a threshold depending only on the fixed constants above.

The source's proofs are replayed as written. They use its numerical
values only through the inequalities below, each of which holds for the
general parameters:

| Source lemma | Inequality used | Holds because |
|---|---|---|
| Dilation (§02) | none | — |
| Prime bound, `q`-bounds (§02) | none | — |
| `gcd(λ, q) = 1` (§02); key separation (§06) | `h_0 < P` | `h_0 = O(k^a log²k) < k` |
| Mesh widths, neighbourhoods (§02) | `α ≤ 1/4`, `H ≤ 1/8`; `R ≤ (D+1) log q = O(k log k)` | `D log q ≤ ck log k + D log(2k²)` |
| Truncated complexity (§02) | breakpoints `≤ 16/η + 4 = 128D/ε_r + 4` | definition of `η` |
| Arrangement count (§03) | none | — |
| Global words (§03) | `log T_glob = O(D(log k + log λ))` | `log λ ≤ h_0 log 2M`, so `log T_glob = O(k^{2a} log³k)` |
| Local patterns (§03) | per coordinate `9((128D/ε_r+5)h+1)²` outputs | bound becomes `(C_r Dh)^{6D}`, `C_r` depending on `ε_r` only |
| Affinity (§05) | `2kH < 1` | `H = k^{−2}` |
| Drift (§05) | `m_*−1 ≥ k/(2M)`; `6MH/k < 1` | `m < 1` |
| Path (§05) | `(1−2MH)/(2M) > H` | `m < 2` |
| Heavy width (§05) | `2H + 4MH/h < 1` | `m < 2` |
| Short periods (§05) | `4MH/h < 1/2`; `q^{−D} ≥ α`; `2H(k+1) < 1` | `m < 2` |
| Long periods (§05) | `4MH/k < η`; `2M/k ≤ 1/16`; `D(4η + 1/h_0) ≤ ε_r` | `a + m < 3`; `m < 1`; `ε_r/2 + 1/L² ≤ ε_r` |
| Affine key count (§06) | none (fixed dimension 3) | — |
| Digit product (§07) | none | — |

The only definitional change in the source is in eligible patterns (§03,
Definition "Eligible local patterns"): condition (i) asks for at least
`(1−ε_r)h` regular positions instead of `h/2`. Since `ε_r ≤ 1/2` this shrinks
the family, and the proof of the local count uses only conditions (ii), (iii)
and the regularity of the anchor, so the count holds as stated.

## 3. Multiplicity two (P2)

**Lemma 3.** On a progression `n_j = n_0 + jd`, `d ≠ 0`, `0 ≤ j < k`, every
key occurs at most twice.

*Proof.* As in source §06, the points `q ỹ(n_j)` sharing a key lie on one
affine line `z_0 + te` (`z_0 ⊥ e`, `|e| = 1`), are pairwise at distance at
least one, and have squared norms `t² + C'` in one interval `[m, m+1)`. Among
three parameters, two lie on the same closed half-line; their absolute values
`u < v` satisfy `v − u ≥ 1`, hence `v ≥ 1` and `v² − u² = (v−u)(v+u) ≥ 1`. Two
squared norms in `[m, m+1)` differ by less than one. ∎

## 4. One outer coloring with three families

### 4.1 Tested position sets

For a full-label word `W = (L(n_j))_{j<k}` of a cyclic progression, let
`S_all(W)` be its light positions. If `W` has a heavy label, let `β*` be the
heavy label whose first occurrence is smallest, and `h(W)` the smallest
positive difference between two of its occurrences. If `h(W) > h_0`, cut
`{0, …, h⌊k/h⌋−1}` into consecutive full blocks of length `h = h(W)`; let
`S_out(W)` be the positions of full blocks that contain no heavy position.
They are all light. Both sets are functions of `W`.

### 4.2 Short-period words

A **short-period word** is a word `(L(X_j, Y_j))_{j<k}` with

```math
X_j=x+\tfrac jh(t+u),\qquad Y_j=A+jw \pmod 1,
```

for some `1 ≤ h ≤ h_0`, `t ∈ {0,…,h−1}^D`, `x ∈ T^D`, `A ∈ R^D`, and real
`u, w` with `|u_i| ≤ 2MH_x/k`, `k|w_i| ≤ 4MH/h`. A label is **s-light** in it
if its multiplicity is at most `k/M_s`; `k_L(W)` counts the positions of
s-light labels.

**Lemma 4 (short-period words through a label).** For every full label `β`,
at most `exp(O(D log k))` short-period words contain `β`.

*Proof.* Choose the anchor `j_0` where `β` occurs (`k` choices), `h` and `t`
(`h_0^{D+1}` choices). In an `x`-coordinate, the value at `j` is the anchor
value (an arc of length `H_x`, given by `β`) plus a translation fixed by
`h, t, j, j_0`, plus `(j−j_0)u_i/h`, of size at most `2MH_x/h`. The target
arc has length at most `H_x(1+4M/h)` and meets at most `4M/h + 2`
`U`-endpoints, each with one lift in its real range: at most `k(4M+2)` lines
in the two parameters, so `O(k²M²)` outputs by the arrangement count. In a
`y`-coordinate, take the anchor's representative `a ∈ [−1/2, 1/2)` in the
`V`-interval of `β`; the value at `j` is `a + (j−j_0)w_i` modulo one, with
`|(j−j_0)w_i| < 1/2`, so its real value lies in `[−1, 1)` and each of the
`|V|` circle endpoints has at most three lifts there (this is the repair M1):
at most `3k|V|` lines, `O(k²|V|²)` outputs. Multiply over `2D`
coordinates; `log h_0, log M, log|V| = O(log k)`. ∎

### 4.3 The coloring

**Proposition 5.** For all large `k` there is `c_*: 𝓛 → {0,1}` such that:

1. for every word `W` of a cyclic progression and each `S ∈ {S_all(W), S_out(W)}`
   with `|S| ≥ δk`, each bit occurs on more than `(1/2−ε)|S|` positions of `S`;
2. for every `h_0 < h ≤ 2M`, `t`, and eligible pattern for `h, t`, each bit
   occurs on more than `(1/2−ε)` of its regular positions;
3. for every short-period word with `k_L ≥ δ_s k`, each bit occurs on more
   than `(1/2−ε)k_L` of its s-light positions.

*Proof.* Independent uniform bits `ξ_β`, `β ∈ 𝓛`. Events:

* **Family 1.** For each `(W, S)` as in 1, order `S` by grouping equal
  labels and deal it cyclically into `w_max ≤ k/M` rows (source §04). Each
  row has `l ≥ ⌊|S|/w_max⌋ ≥ δM − 1` distinct labels. Event: some bit occurs
  on at most `(1/2−ε)l` positions of the row. At most `2k T_glob` events.
* **Family 2.** For each `h, t` and eligible pattern, `l ≥ (1−ε_r)h ≥ h/2`
  distinct regular labels. Event: some bit on at most `(1/2−ε)l` of them.
* **Family 3.** For each short-period word `W` with `k_L ≥ δ_s k`, with
  `w_β` the multiplicity of the s-light label `β`: event
  `|Σ_β w_β(ξ_β − 1/2)| ≥ ε k_L`.

Hoeffding's inequality gives `P(E) ≤ 2e^{−2ε²l}` in families 1 and 2, and,
since `Σ w_β² ≤ (k/M_s) k_L`, `P(E) ≤ 2exp(−2ε²k_L M_s/k) ≤ 2exp(−2ε²δ_s M_s)`
in family 3. Weights: `z_E = e^{−ε² l}` in families 1, 2 and
`z_E = exp(−ε²δ_s M_s)` in family 3.

Incident weight through one label `β`, family by family:

* `ι_1 ≤ 2k T_glob e^{−ε²(δM−1)} = exp(O(k^{2a}log³k) − ε²δk^m/2)`, because
  `2a < m`;
* `ι_2 ≤ Σ_{h>h_0}(C_r Dh)^{6D}e^{−ε²h/2}`. For `h ≥ h_0 = DL²` and large `k`,
  `6D log(C_r Dh)/h ≤ 6 log(C_r D²L²)/L² ≤ ε²/4` (the left side decreases in
  `h` there), so each term is at most `e^{−ε²h/4}` and
  `ι_2 ≤ e^{−ε²h_0/4}/(1 − e^{−ε²/4})`;
* `ι_3 ≤ exp(O(D log k) − ε²δ_s D L²)` by Lemma 4.

Each is smaller than any power of `k`; take `k` with `ι := ι_1+ι_2+ι_3 ≤ k^{−2}`
and every `z_E ≤ 1/2`. Join two events when they share a label bit; this is a
dependency graph (source §04). With `log(1−z) ≥ −2z` on `[0, 1/2]`:

* an event of family 1 or 2 has `Σ_{Γ(E)} z_F ≤ lι`, and
  `z_E Π(1−z_F) ≥ e^{−ε²l − 2lι} ≥ 2e^{−2ε²l}` as soon as
  `l(ε² − 2k^{−2}) ≥ log 2`, which holds since `l ≥ min(δM−1, h_0/2) → ∞`;
* an event of family 3 uses at most `k` bits, so `Σ_{Γ(E)} z_F ≤ kι ≤ 1/k`,
  and `exp(−ε²δ_sM_s − 2/k) ≥ 2exp(−2ε²δ_sM_s)` since `M_s → ∞`.

The finite asymmetric local lemma (source §04) gives a choice avoiding every
event. Summing over rows gives 1. ∎

Put `c_0(n) = c_*(L(n))`.

## 5. The dichotomy

A progression is **γ-rich** if each bit occurs at least `γk` times among
`c_0(n_0), …, c_0(n_{k−1})`.

**Theorem 6.** Every cyclic progression with `d ≠ 0` is γ-rich, or it has a
heavy label, `h = h(W) ≤ h_0`, and, with `t, u` from the source's path lemma,

```math
x(n_j)=x(n_0)+\tfrac jh(t+u),\qquad \tilde y(n_j)=A+jw\quad(0\le j<k)
```

in `T^D` and `R^D` respectively, with `|u_i| ≤ 2MH_x/k` and `k|w_i| ≤ 4MH/h`;
indices incongruent modulo `h` carry distinct labels.

*Proof.* No heavy label: `S_all` is everything, and Proposition 5.1 gives
more than `(1/2−ε)k ≥ γk` of each bit. Otherwise apply the source's drift and
path lemmas to `β*`, giving `h = h(W) ≤ 2M`, `t, u, v` and the distinct-label
statement.

*`h ≤ h_0`.* The source's short-period paragraph (§05) uses only `h | λ`, the
motion bound and the step lattice, and gives `ỹ(n_j) = ỹ(n_0) + jw` with
`w = v/h`, `k|w_i| ≤ 4MH/h`.

*`h > h_0`.* The source's long-period paragraph shows: in each full block,
the nonregular fraction is at most `D(4η + 1/h_0) ≤ ε_r`, labels are
distinct, and every full block containing a heavy position is eligible, now in
the sense of §2. Proposition 5.2 gives each bit on more than
`(1/2−ε)(1−ε_r)h` positions of such a block. If `|S_out| ≥ δk`, Proposition
5.1 gives more than `(1/2−ε)|S_out|` more, on disjoint positions; heavy blocks
and `S_out` cover all full blocks, at least `k − h` positions. Otherwise heavy
blocks alone cover at least `k − h − δk`. In both cases each bit occurs at
least `(1/2−ε)(1−ε_r)(1−δ)k − h ≥ γk` times, since `h ≤ 2M = o(k)` and the
inequality on `γ` is strict. ∎

## 6. Rich progressions

Take independent bits `E_κ`, `P(E_κ = 1) = p`, and `C(n) = c_0(n) + E_{κ(n)}`.
For a γ-rich progression and a target colour, the at least `γk` positions of
the other outer colour all need a flip; by Lemma 3 they carry at least `γk/2`
distinct keys, fixed before sampling. With fewer than `q^{2D}` progressions,

```math
R_k\le2q^{2D}p^{\gamma k/2}\le\exp\Bigl(\bigl(2c-\tfrac{\gamma b}{2}\bigr)k\log k+2D\log(2k^2)+\log2\Bigr)=o(1),
```

because `2c < γb/2` and `D log k = o(k log k)`. This is the source's own
estimate with `4` replaced by `2`.

## 7. Non-rich progressions

**Lemma 7 (runs).** In a non-rich progression, the occurrences of any one
label form a single run: one residue class `r` modulo `h`, consecutive in it.

*Proof.* One class, by Theorem 6. For `j = r + sh`,
`x_i(n_j) = x_i(n_r) + s u_i` modulo one, a monotone circle path of total
length at most `(k/h)|u_i| ≤ 2MH_x < 1/2`. A half-open arc `I` of length
`H_x` has connected preimage under it: leaving `I` and coming back would
cover the complementary arc, of length `1 − H_x > 1/2`. In the
`y`-coordinates, `ỹ_i(n_j) = A_i + jw_i` is real affine and a `V`-interval is
a real interval. The intersection of the `2D` preimages is an interval of `s`.
∎

The **key word** of a non-rich progression, `(κ(n_j))_{j<k}`, is fixed by its
boxes and bands. Each box coordinate `V(A_i + jw_i)` is fixed by comparisons
with the `|V| + 1` endpoint values in `[−1/2, 1/2]`: `k(|V|+1)` lines in
`(A_i, w_i)`, `O(k²|V|²)` outputs. The bands `⌊f(n_j)⌋` are fixed as in
source §06 by `C(k(Dq²+2))³` sign vectors. So there are at most

```math
T_{\rm key}=\exp\bigl(6\log q+O(D\log k)\bigr)
```

key words of non-rich progressions.

**Theorem 8.** The probability `A'_k` that some non-rich progression is
monochromatic tends to zero.

*Proof.* Fix a target colour `β_0` and a non-rich progression; its label
word is a short-period word (Theorem 6, `X_j = x(n_j)`, `Y_j = y(n_j)`).

*Case (i), `k_L ≥ δ_s k`.* By Proposition 5.3 more than `(1/2−ε)δ_s k`
s-light positions have the colour `1 − β_0`. They need flips and carry at
least `x = ⌈(1/2−ε)δ_s k/2⌉` distinct keys of the key word. The event lies in
"at least `x` distinct keys of the key word are flipped", of probability at
most `C(k, x)p^x ≤ (ekp/x)^x = exp(−Ω(k log k))`.

*Case (ii), `k_L < δ_s k`.* The s-heavy labels number fewer than `M_s`, and by
Lemma 7 each is a run. Record `h`, and for each s-heavy label its first and
last index and its outer colour: at most `h_0(M_s+1)(2k²)^{M_s} =
exp(O(D log³k))` codes. With the key word, a code fixes the required flip at
every s-heavy position. These positions number at least `(1−δ_s)k` and carry
at least `(1−δ_s)k/2` distinct keys, so the event has probability at most
`(1−p)^{(1−δ_s)k/2} ≤ e^{−(1−δ_s)pk/2}` (zero if the prescriptions conflict).

Summing over both targets, key words and codes,

```math
A'_k\le2T_{\rm key}\Bigl(e^{-\Omega(k\log k)}+e^{O(D\log^3k)}e^{-(1-\delta_s)k^{1-b}/2}\Bigr).
```

Here `log q ≤ ck^{1−a} log k + O(log k)`. The first term vanishes since
`a > 0`; the second since `b < a` (for `6 log q`) and `a + b < 1` (for both
`O(D log k)`, the box part of the key word, and `O(D log³k)`; this is the
repair M2). ∎

## 8. Conclusion

Every nonzero-step progression is rich or non-rich, so `R_k + A'_k < 1` for
large `k`, uniformly over the allowed primes `P`. Some choice of the bits
`E_κ` gives a colouring of `Z/NZ` without monochromatic `k`-term progression,
with `N = q^D ≥ k^{ck}`. The source's digit product (§07) gives
`W_r(k) > N^{⌊log₂ r⌋} ≥ k^{ck⌊log₂ r⌋}` for every `r ≥ 2`, with a threshold
fixed before `r`.

## 9. Region, supremum and explicit choice

The region of §2 forces `a < m/2 < 1/2`, `b < a`, `γ < 1/2`, hence
`c < γb/4 < 1/16`. Every `c < 1/16` is reached by letting
`ε, ε_r, δ → 0`, `γ → 1/2`, `a → 1/2`, `b → a`, `m ∈ (2a, 1)`.

| Parameter | a | m | b | ε = ε_r = δ | δ_s | γ | c |
|---|---|---|---|---|---|---|---|
| Value | 497/1000 | 999/1000 | 99/200 | 1/1000 | 1/2 | 497/1000 | 1/17 |

| Inequality | Exact margin |
|---|---:|
| `b < a` | 1/500 |
| `a + b < 1` | 1/125 |
| `2a < m` | 1/200 |
| `m < 1` | 1/1000 |
| `γ < (1/2−ε)(1−ε_r)(1−δ)` | 1002499/1000000000 |
| `c < γb/4` | 36451/13600000 |

This tuple violates `2a < 1 − b` (merged PR #2's region): the proof needs §7.
The repository's `1/9` tuple violates `c < γb/4`: `1/9` needs (K).

## 10. What this does not claim

* The source's lemmas are not re-proved; §2 lists exactly where their numerical
  values enter. A gap in the source would affect this note as it affects every
  refinement.
* The threshold `K_0` is not explicit; with margins of `1/1000` it is
  astronomically large.
* Nothing here concerns (K). Whether `2c < γb` holds is unchanged by this note.
* `verify.py` checks the exact rational region, the margins, the supremum and
  the boundary controls. It does not check the asymptotic estimates, which
  are proved in the text.

## Reproduce

```sh
python3 auto-research/trust-reduction/2026-10-26-ChaloupeMusic-source-only-1-16/verify.py
```

Expected: `PASS`, 7 negative controls rejected, hashes matching `MANIFEST.json`.
