# Every c < 1/8 (explicit 1/9) from the source's proofs alone, replayed

**Status:** research note with a complete proof relative to the pinned OpenAI
source. Prepared with Claude (Anthropic). Not reviewed by a human, not formally
verified.

**Result.** For every fixed `c < 1/8` there is `K_0`, independent of `r`, with

```math
W_r(k)>k^{ck\lfloor\log_2 r\rfloor}\qquad(k\ge K_0,\ r\ge2).
```

The explicit choice is the repository's `c = 1/9`. What changes is the base it
rests on: **the proofs of the OpenAI source (Sections 02 to 07) only**,
replayed under the inequalities of the companion note's §2. The
companion note [`../2026-10-26-ChaloupeMusic-source-only-1-16/`](../2026-10-26-ChaloupeMusic-source-only-1-16/)
proved links (P2), (O) and (R) of the `1/9` chain, and found that link (K),
the rich-event estimate `2c < γb`, was the only one still needed above
`1/16`. This note proves (K) in full: the repeated-key facts of PR #4
(restated in `rank-certificate-proof.md`, Section 1) and Lemmas A\* and C\*
of `digit-rank-proof.md`. Every step was re-derived; two repairs are
needed, none of which changes a constant that matters (§9).

Together the two notes give the whole `1/9` argument as one proof from the
source alone. No step is imported from PRs #2, #4, #6 or #7.

## 1. Setting

Use the parameters, coloring and dichotomy of the companion note: §2 there
(parameters and source lemmas, with the side-condition table), Lemma 3
(multiplicity two), Proposition 5 (outer coloring), Theorem 6 (dichotomy),
§7 (non-rich progressions). Its region is kept, except that the rich
condition `c < γb/4` becomes

```math
2c<\gamma b .
```

Nothing in the companion note used `c < γb/4` outside its §6, which this note
replaces. In particular `b < a`, `a + b < 1`, `2a < m < 1` are unchanged.

For a progression `n_j = n_0 + jd` (`d ≠ 0`, `0 ≤ j < k`) write
`Y_j = ỹ(n_j)`, `Q(j) = (V(y_i(n_j)))_{i≤D}` its box, `f_j = q²|Y_j|²`, and
`κ_j = (Q(j), ⌊f_j⌋)` its key (source §06). `q` is a power of the prime
`P > k ≥ 3`, so `q` is odd. Recall `|Y_{j,i} − Y_{j',i}| ≤ 2H` when
`Q(j) = Q(j')` (mesh widths, source §02), `y_i(z) ∈ q^{−i}Z/Z`, and
`q|Y(z)| ≥ 1` for `z ≠ 0` (key separation, source §06).

Fix a target colour. The event that the progression is monochromatic in it
prescribes `E_κ = 1` on the set `F` of keys at **flipped** positions (outer
colour opposite to the target) and `E_κ = 0` elsewhere; an event with a key
prescribed both ways is empty and discarded. With `P_1` the flipped positions,
`r` the flipped keys occurring twice and `s` those occurring once, Lemma 3
gives `|P_1| = 2r + s`, `|F| = r + s`. A γ-rich progression has `|P_1| ≥ γk`.

## 2. Repeated boxes

Assume some box repeats. A **return gap** is `g = j' − j > 0` with
`Q(j) = Q(j')`. Let `h` be the gcd of all return gaps.

**Lemma R1 (common return).** There are `t ∈ {0,…,h−1}^D` and `B ∈ R^D` with
`y(d) ≡ t/h + B (mod Z^D)` and `|B_i| ≤ 2H/h`. `h` is itself a return gap,
two positions with equal boxes are congruent modulo `h`, and `β := hB` equals
`Y(hd)`, with `q|β| ≥ 1` and `β_i ∈ q^{−i}Z`.

*Proof.* For a return pair `(j, j+g)`, `v = Y_{j+g} − Y_j` has `|v_i| ≤ 2H`
and `v ≡ g y(d)`. Two pairs with the same gap give vectors whose difference
is integral and of size `< 4H < 1`, so `v = v_g` depends on `g` only. For two
gaps, `g'v_g − g v_{g'}` is integral of size `≤ 2H(g + g') < 4kH < 1`, hence
zero: `v_g = gB` for one `B`, and `|B_i| ≤ 2H/g ≤ 2H/h`. Bézout gives
`h y(d) ≡ hB`, so `y(d) − B ≡ t/h` for an integral `t`, reduced modulo `h`.
For a return pair `(j, j+g)`, the point `Y_j + hB` lies on the segment from
`Y_j` to `Y_{j+g}`, inside their common half-open box, hence in
`[−1/2,1/2)^D`; it is congruent to `y(n_{j+h})`, so it is `Y_{j+h}` and
`Q(j+h) = Q(j)`. Every return gap is a multiple of `h`. Since
`h ≤ k < P`, `hd ≠ 0`; `Y(hd)` is the centered representative of
`h y(d) ≡ hB`, and `|hB_i| ≤ 2H < 1/2`, so `Y(hd) = β`. Separation gives
`q|β| ≥ 1`, and `y_i(hd) ∈ q^{−i}Z/Z` gives `β_i ∈ q^{−i}Z`. ∎

A residue class `a` modulo `h` (`0 ≤ a < h`) is a **collision class** if two
of its positions carry the same key. Its positions are `a + sh`,
`0 ≤ s < K_a`, with `K_a ≤ K := ⌈k/h⌉`. Both positions of a repeated key lie
in one class (equal boxes, R1).

**Lemma R2 (collision classes are affine).** `Y_{a+sh} = Y_a + sβ` for
`0 ≤ s < K_a`.

*Proof.* `y(n_{a+sh}) ≡ Y_a + sβ`, since `st` is integral. In a coordinate
with `β_i = 0` there is nothing to prove. Otherwise the total motion is
`(K_a − 1)|β_i| ≤ 2kH < 1/2`. If some `Y_{a,i} + sβ_i` left `[−1/2,1/2)`,
the closed real segment would meet the cut, every sample would have
`ρ(y_i) ≤ (k/h)|β_i|`, and, since `α ≤ q^{−D} ≤ |β_i|`, every sample's
interval would have width at most `2H((k/h)+1)|β_i| < |β_i|`. Distinct samples
of the class are at circle distance at least `|β_i|` in this coordinate, so
all boxes of the class would be distinct, contradicting the repeated key. ∎

**Lemma R3 (carries).** Put `A = Y_0` and define `m_j ∈ Z^D` by
`Y_j = A + (j/h)(t+β) − m_j`. For `0 ≤ j < h`, `m_{j,i} ∈ [−1, h−1]`. The
**augmented word** `(Q(j), m_j)_{j<k}` takes at most `exp(O(D log k))` values
over all progressions.

*Proof.* `y(n_j) ≡ A + j y(d)`, so `m_j` is integral, and
`m_{j,i} = ⌊A_i + (j/h)(t_i+β_i) + 1/2⌋`. For `j < h`, `(j/h)t_i ≤ (h−1)²/h =
h − 2 + 1/h`, so the argument of the floor lies in `[−2H, h − 1 + 1/h + 2H)`. For the count,
in coordinate `i` put `σ = (t_i + β_i)/h ∈ (−1, 1)`; the unreduced value
`A_i + jσ` lies in `(−k−1, k+1)`, and `(V(Y_{j,i}), m_{j,i})` is fixed by its
comparisons with `τ + z` for the `|V| + 1` mesh endpoint values `τ` and
`|z| ≤ k + 2`. These are `O(k²|V|)` lines in `(A_i, σ)`; the arrangement
count gives `O(k⁴|V|²)` outputs per coordinate. ∎

**Lemma R4 (vertex constraint).** Let `a` be a collision class, `a + s_1h`
and `a + s_2h` (`s_1 < s_2`) a pair with one key, `σ_a = s_1 + s_2`,
`w = |β|²`, `W = q²w`. Then

```math
\zeta_a:=q^2\bigl(2\langle Y_a,\beta\rangle+\sigma_a w\bigr)\in(-1,1),\qquad
f_{a+sh}=q^2|Y_a|^2+s(s-\sigma_a)W+s\,\zeta_a\quad(0\le s<K_a).
\tag{1}
```

*Proof.* By R2, `f_{a+sh} = q²(|Y_a|² + 2s⟨Y_a,β⟩ + s²w)`, so
`f_{a+s_2h} − f_{a+s_1h} = (s_2 − s_1)ζ_a`. Equal bands give a difference of
absolute value `< 1`. Substituting `2q²⟨Y_a,β⟩ = ζ_a − σ_aW` gives the
formula. ∎

Fix `σ_a` by a rule from the positions of repeated keys (say, the first pair).

## 3. Discrete data and digit rank

The **discrete data** of a progression with a repeated key are `h`, `t`, the
augmented word, and the set of positions of repeated keys. They determine the
collision classes `Σ`, `a_0 = min Σ`, every `σ_a`, the vectors
`Δm_a = m_a − m_{a_0}` (`|Δm_{a,i}| ≤ h`) and `c_a = (a − a_0)/h ∈ [0, 1)`.
They take at most `k^{D+1} · exp(O(D log k)) · 2^k = exp(O(D log k + k))`
values.

For `v ∈ Z^D` put `(S_1v)_l = v_{l+1}`, `(S_2v)_l = v_{l+2}` for
`0 ≤ l < D` (`v_{D+1} := 0`). With `V = span_Q{Δm_a : a ∈ Σ}`, the **digit
rank** is `R = dim(S_1V + S_2V) ∈ {0,…,D}`. Without repeated keys, `R = 0`.

**Digit expansions.** For `z ∈ G`, let `y_0,…,y_{D−1}` be the balanced base-`q`
digits of `λz mod q^D` (`|y_l| ≤ (q−1)/2`). Then
`Y_i(z) = Σ_{l<i} y_l q^{l−i}`, since this sum is congruent to `y_i(z)` and
of absolute value `< 1/2`. Hence, for `v ∈ Z^D`,

```math
q^2\langle Y(z),v\rangle=q\langle S_1v,y\rangle+\langle S_2v,y\rangle+\langle v,F\rangle,
\qquad F_i=\sum_{l\le i-3}y_lq^{\,l-i+2},\ |F_i|\le\tfrac12 .
\tag{2}
```

For `β = Y(hd)`, put `b_i = q^iβ_i ∈ Z`. From `y_i ≡ q y_{i+1}`,
`b_{i+1} ≡ b_i (mod q^i)`; with `e_0 = b_1` and
`e_i = (b_{i+1} − b_i)/q^i`,

```math
\beta_i=\sum_{l<i}e_lq^{\,l-i},\qquad |e_l|\le2Hq+2H,\qquad
q^2\langle v,\beta\rangle=q\langle S_1v,e\rangle+\langle S_2v,e\rangle+R_v,\ \ |R_v|\le3H|v|_1 .
\tag{3}
```

The last bound uses `|Σ_{l≤i−3} e_l q^{l−i+2}| ≤ (2Hq+2H)/(q−1) ≤ 3H`. The
vector `e` determines `β_D`, hence `λhd mod q^D`, hence `d` (`λ` and `h` are
units modulo `q`).

## 4. The certificate count

**Lemma A\*.** Fix discrete data of digit rank `R`. Over all progressions with
these data and all sets `S` of positions in collision classes, the literal key
sets `{κ_j : j ∈ S}` number at most `exp(R log q + O(log q + D log k + k))`.

*Proof.* By R3, `Y_a = Y_{a_0} + c_a(t + β) − Δm_a`. Expand `q²|Y_a|²`. The
terms containing `β` are `q²(c_a²(2⟨t,β⟩ + w) + 2c_a⟨Y_{a_0},β⟩ − 2c_a⟨Δm_a,β⟩)
= 2c_a q²⟨Y_a,β⟩ − c_a²W = c_aζ_a − (c_a² + c_aσ_a)W`, by R4. Hence

```math
q^2|Y_a|^2=q^2U_1+2c_aq^2U_2-(c_a^2+c_a\sigma_a)W-2q^2\langle Y_{a_0},\Delta m_a\rangle
+q^2\bigl(c_a^2|t|^2+|\Delta m_a|^2-2c_a\langle t,\Delta m_a\rangle\bigr)+c_a\zeta_a,
```

with `U_1 = |Y_{a_0}|²`, `U_2 = ⟨Y_{a_0}, t⟩`. Apply (2) at `z = n_{a_0}`:
`q²⟨Y_{a_0},Δm_a⟩ = q⟨S_1Δm_a,y⟩ + ⟨S_2Δm_a,y⟩ + τ_a`, `τ_a = ⟨Δm_a,F⟩`,
`|τ_a| ≤ Dh/2`. Choose by a fixed rule a basis `u_1,…,u_R` of
`S_1V + S_2V` among the vectors `S_1Δm_a, S_2Δm_a`, and record the `R`
integers `⟨u_r, y⟩`, each of absolute value at most `Dhq`: cost
`R(log q + O(log k))`. By linearity they fix every `⟨S_1Δm_a,y⟩` and
`⟨S_2Δm_a,y⟩`. Choose also a basis `v_1,…,v_ρ` of `V` among the `Δm_a`;
then `τ_a = Σ_l g_{al}φ_l` with known rationals `g_{al}` and real
`φ_l = ⟨v_l, F⟩`. By R4, every position `j = a + sh` of a collision class has

```math
f_j=G_j(\Theta)-2\tau_a(\varphi)+(c_a+s)\zeta_a ,
```

where `G_j` is affine in `Θ = (q²U_1, q²U_2, W)` with constant term and
coefficients fixed by the data and the recorded integers (the constant term
is rational, not necessarily integral), `0 ≤ c_a + s < K + 1`, `ζ_a ∈ (−1,1)`.
Count the band words of collision classes in four steps, each by the
arrangement count of source §03 (equality signs included, on any subset of
parameter space):

1. `0 ≤ f_j ≤ Dq²/4` puts `G_j` in an interval of length
   `Dq²/4 + 2Dh + 2K + 2 = O(Dq²)`; the signs of `G_j − n` over the
   integers `n` there fix every `⌊G_j⌋`: `O(kDq²)` planes in dimension 3,
   `exp(6 log q + O(log k))` outcomes.
2. In one cell, `G_j − ⌊G_j⌋` is affine. The signs of
   `G_j − ⌊G_j⌋ − 2τ_a(φ) − δ`, `δ ∈ Z`, `|δ| ≤ Dh + 2`, fix
   `⌊G_j − 2τ_a⌋`: `poly(k)` hyperplanes in dimension `3 + ρ ≤ D + 3`,
   `exp(O(D log k))` outcomes.
3. In one part, `f_j = N_j + θ_j + (c_a+s)ζ_a` with `N_j` known and
   `θ_j ∈ [0,1)` affine. For `c_a + s > 0`, `⌊f_j⌋` is fixed by the position of
   `ζ_a` among the points `(δ − θ_j)/(c_a+s)`, `|δ| ≤ K + 2`. The order of
   these points within each class, and their positions relative to `±1`, are
   signs of `O(hK⁴)` affine functions (positive denominators cleared):
   `exp(O(D log k))` outcomes.
4. Then class `a` has at most `2K_a(2K+5) + 1` band words; the product over
   classes is `exp(h · O(log(k/h + 2))) = exp(O(k))`.

Boxes are in the discrete data, so the band words fix every key in a
collision class. The `2^k` choices of `S` cost `exp(O(k))`. ∎

## 5. The progression count

**Lemma C\*.** The progressions `(n_0, d)` with a repeated key and digit rank
`R` number at most `exp((2D − R) log q + O(log q + D log k + k))`.

*Proof.* Subtracting R4's definition of `ζ` at `a_0` from that at `a`, with
R3, gives the exact identity

```math
\langle\Delta m_a,\beta\rangle=c_a(T+w)+\tfrac12(\sigma_a-\sigma_{a_0})w+\tfrac1{2q^2}(\zeta_{a_0}-\zeta_a),
\qquad T=\langle t,\beta\rangle .
\tag{4}
```

Encode `n_0` (`q^D` choices), the discrete data, `⌊q²T⌋` (`|T| ≤ 2D/k`) and
`⌊(k+1)q²w⌋` (`w ≤ 4DH²`): together `q^D exp(O(log q + D log k + k))`. They
give a number `X_a` with `|X_a − q²⟨Δm_a,β⟩| < 3`: the error is at most
`c_a(1 + 1/(k+1)) + K/(k+1) + 1`, and `c_a(k+2)/(k+1) < 1` because
`h < k + 2`.

By (3), `q²⟨Δm_a,β⟩ = qN_1^a + N_2^a + R^a` with `N_1^a = ⟨S_1Δm_a, e⟩`,
`N_2^a = ⟨S_2Δm_a, e⟩`, `|N_2^a| ≤ Dh(2Hq + 2H) ≤ 2D(q+1)/k < q/8`
and `|R^a| ≤ 3HDh < 1` (both because `a < 1`). Hence `N_1^a` is the
integer nearest `X_a/q`, and `N_2^a` lies in `X_a − qN_1^a + (−4, 4)`.
Record, for each basis vector `u_r` of the form `S_2Δm_a`, which of these at
most 9 integers it is: `9^R` choices. Then `⟨u_r, e⟩` is known for every `r`.
Fix by a rule `R` digit positions `L` on which `(u_r)` has a nonsingular
minor, and record `e` off `L`: at most `(4Hq + 4H + 1)^{D−R} ≤ q^{D−R}`
choices. The `R` linear equations determine `e_L`, so `e`, so `d`. The map
from progressions to codes is injective. ∎

## 6. The rich estimate

**Theorem 9.** If `2c < γb`, the probability `R_k` that some γ-rich
progression is monochromatic tends to zero, uniformly over the allowed
primes.

*Proof.* Fix a target and a γ-rich progression with a consistent event, of
digit rank `R`. Put `κ_R = R/D`, `ν_R = (2D − R)/D` (so `κ_R + ν_R = 2`),
`μ = (γb − 2c)/2 > 0` and `θ_R = (κ_Rc + γb − ν_Rc)/(2b)`. Then
`bθ_R − κ_Rc = b(γ − θ_R) − ν_Rc = μ`, and `0 < θ_R < γ` since
`γb − ν_Rc ≥ γb − 2c > 0` and `κ_R ≤ ν_R`. Split the flipped keys into the
`r + s_Σ` carried by positions of collision classes (all repeated flipped keys
are among them) and the `s_out` others.

* If `r + s_Σ ≥ θ_Rk`, select by a fixed rule positions of collision classes
  carrying exactly `⌈θ_Rk⌉` distinct flipped keys. The event lies in "these
  keys are all flipped", of probability `p^{⌈θ_Rk⌉}`. By Lemma A\* and the
  count of discrete data, these key sets number at most
  `exp(R log q + o(k log k)) = exp(κ_Rck log k + o(k log k))`, since
  `D log q = ck log k + O(D log k)`.
* Otherwise `r < θ_Rk` and `|F| = |P_1| − r > (γ − θ_R)k`. Lemma C\* (or the
  trivial `q^{2D}` when no key repeats) counts these progressions by
  `exp(ν_Rck log k + o(k log k))`.

Each part contributes at most `exp(−μk log k + o(k log k))`, with `o(·)`
uniform in `R`, because `log q = O(k^{1−a} log k)` and `D log k + k =
o(k log k)`. Sum over the `D + 1` ranks and the two targets. Events sharing a
certificate are covered by one event; no independence between events is
used. ∎

## 7. Conclusion

Replace §6 of the companion note by Theorem 9. With §7 there (`A'_k = o(1)`
under `b < a`, `a + b < 1`), `R_k + A'_k < 1` for large `k`, and the digit
product gives `W_r(k) > k^{ck⌊log₂ r⌋}` for every `r ≥ 2`.

## 8. Region, supremum, explicit choice

```math
0<b<a,\ a+b<1,\ 2a<m<1,\ 0<\varepsilon<\tfrac12,\ 0<\varepsilon_{\rm r}\le\tfrac12,\ 0<\delta,\delta_s<1,\
\gamma<(\tfrac12-\varepsilon)(1-\varepsilon_{\rm r})(1-\delta),\ 0<c<\tfrac{\gamma b}2 .
```

So `c < γb/2 < 1/8`, and every `c < 1/8` is reached by the limits of the
companion note. The explicit choice is that of `short-period-runs-proof.md`:

| a | m | b | ε = ε_r = δ | δ_s | γ | c |
|---|---|---|---|---|---|---|
| 49/100 | 99/100 | 97/200 | 1/200 | 1/2 | 97/200 | 1/9 |

with margins `b < a`: 1/200; `a + b < 1`: 1/40; `2a < m`: 1/100; `m < 1`:
1/100; `γ` below the balance cap: 40499/8000000; `γb/2 − c`: 4681/720000.

## 9. Repairs to the earlier text

None changes the region.

* **K1.** In Lemma A\* of `digit-rank-proof.md` the known part `K_j` of each
  band is rational, not integral (`c_a` has denominator `h`). Step 1 must
  count `⌊K_j + G_j⌋`, as done above by putting the constant into `G_j`.
* **K2.** Lemma C\* there records "at most 9 choices" for every `a ∈ Σ`, which
  would cost `9^{|Σ|}`, up to `9^h`. Only the basis vectors need it: `9^R`.
  (`9^h = exp(O(k))` would also be absorbed, so this is presentation only.)
## 10. What this does not claim

* The source's lemmas are not re-proved. The side-condition table of the
  companion note lists where their numerical values enter; this note adds
  `4kH < 1`, `2D(q+1)/k < q/8` and `3HDk < 1`, all implied by
  `0 < a < 1`.
* The threshold `K_0` is not explicit.
* `verify.py` checks the region and margins, the identity `κ_R + ν_R = 2` and
  both rank margins for every `R`, the exact identities of R4, Lemma A\* and
  (4) on random rational instances, the digit expansions (2) and (3) and the
  recovery of `e` in Lemma C\* on exact modular instances. The asymptotic
  counts are proved in the text, not checked.

## Reproduce

```sh
python3 auto-research/trust-reduction/2026-10-26-ChaloupeMusic-source-only-1-8/verify.py
```

Expected: `PASS`, with every negative control rejected and hashes matching
`MANIFEST.json`.
