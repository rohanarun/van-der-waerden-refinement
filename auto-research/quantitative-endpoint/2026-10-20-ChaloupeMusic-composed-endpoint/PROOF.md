# The composed endpoint bound: seven-eighths loss with retuned constants

## 1. Claim and status

All logarithms are natural, and `t = log k`. This is a conditional proof draft, not an independently
reviewed theorem. It combines two contributions built on open PR #12 (head `029431bb`, cited as "#12"):

* **N1b** (`2026-10-20-ChaloupeMusic-seven-eighths/`, head `8c2b34f`): a remainder-free canonical
  partition, which allows `M = ⌊k/32⌋`, `D ∝ sqrt(k)/t^{5/2}` and `p ∝ t^{7/2}/sqrt(k)`. Its Lemmas 5.1–5.3
  and interface extensions (I1)–(I2) are used here and cited as "N1b".
* **N1a** (`2026-10-20-ChaloupeMusic-endpoint-constants/`, head `a8a9edc` on branch `sprint2/N1a`): five
  scale-free lemmas A–E. They are restated in Section 2 with their proofs in brief; the full text is
  N1a's Section 2.

It adds two arithmetic lemmas (D′ and D″) on a product displayed in PR #9, Section 8.3, step 4.

**Conditional theorem.** Assume the finite source interfaces of #12, Section 2, and the finite factors of
PR #9 displayed in its Sections 7.3, 8.2 and 8.3 (which #12's Appendix A already imports). For every integer
`k >= 2^739` and every integer `r >= 2`,

```math
 W_r(k)>\left(\frac{k^{1/8}}{e^{C}(\log k)^{7/8}}\right)^{k\lfloor\log_2 r\rfloor}, \tag{1}
```

where the constant `C` depends on which bound is used for the class product of PR #9, Section 8.3, step 4.
The three tiers are proved and checked separately, so contesting one does not affect the others.

| tier | class product | `C` | `c = 1/9` from | coefficient at `2^1024` |
|---|---|---:|---|---:|
| D″ (this note, reading of Section 2) | `45^{k/2}` | `71/20` | `2^960` | `> 0.1119` |
| D′ (this note) | `19^k` | `403/100` | `2^1015` | `> 0.1112` |
| D (N1a) | `37^k` | `35/8` | `2^1054` | `> 0.1107` |

| | constant | power of `log k` | range | `c = 1/9` from |
|---|---:|---:|---|---|
| #12 | `e^{20}` | 1 | `2^1024` | `2^4096` |
| N1a | `e^{9/2}` | 1 | `2^1024` | `2^1163` |
| N1b | `e^{35/2}` | 7/8 | `2^739` | `2^2504` |
| here, tier D″ | `e^{71/20}` | 7/8 | `2^739` | `2^960` |
| here, tier D′ | `e^{403/100}` | 7/8 | `2^739` | `2^1015` |
| here, tier D | `e^{35/8}` | 7/8 | `2^739` | `2^1054` |

Every tier of (1) beats each of #12, N1a and N1b on that bound's own range (`k >= 2^1024` for #12 and
N1a, `k >= 2^739` for N1b). This holds even without the `(log k)^{1/8}` factor, since
`71/20 < 403/100 < 35/8 < 9/2 < 35/2`. No coefficient above `1/8` is claimed.

## 2. Ingredients

**From N1b.**

* The canonical partition (N1b Lemma 5.1): for `h <= k/2`, `⌈k/h⌉` consecutive blocks with lengths in
  `[⌈h/2⌉, h]`, a function of the label word.
* The regularity of short blocks (N1b Lemma 5.2): the nonregular fraction is at most `D(12η + 3/h_0)`.
* Eligibility (N1b Lemma 5.3).
* The truncation constant (I1) and the anchored count (I2) for patterns of every length `ℓ ∈ [h/2, h]`:
  at most `h·A_h` triples `(t, ℓ, word)` through a label.

In (I2), eligibility is now asked with **at least `(1 − ε_reg)ℓ` regular positions** instead of `ℓ/2`. The
count is unchanged, since its proof does not use the threshold. Every heavy-containing block of an actual
long-period progression satisfies the stronger condition by Lemma 5.2. So every Family 2 event tests
`l >= (1 − ε_reg)⌈h/2⌉ >= (1 − ε_reg)h/2` labels.

**From N1a** (restated; proofs in N1a, Section 2).

* **Lemma A.** For `1 <= h_0 <= 2M`,
  `log λ < log 4·(h_0 + sqrt(2M) + log_2(2M)·(2M)^{1/3})`. The identity
  `log λ = Σ_{j>=1} θ(min(h_0, (2M)^{1/j}))` is combined with Erdős's bound `θ(x) < x log 4`.
* **Lemma B.** If every event uses at most `k` independent label variables and has
  `P(E) <= Pbar(E) <= e^{−1/8}/2`, and if for every variable `Σ_{E∋x} Pbar(E) e^{1/8} <= 1/(16k)`, then
  the weights `z_E = Pbar(E) e^{1/8}` satisfy the asymmetric local lemma. It suffices that each of the
  three families has incident weight at most `1/(48k)`.
* **Lemma C.** If the rank-`R` certificates number at most `exp(R log q + E_c)`, the progressions with a
  repeated key at most `exp((2D − R) log q + E_p)`, `Ebar = (E_c + E_p)/2`, and
  `Γ = γkL/2 − D log q > |E_c − E_p|/2`, then the probability of a monochromatic `γ`-rich progression is
  at most `2[2(D+1) e^{Ebar − Γ} + e^{−2Γ}]`.
* **Lemma D.** `Π_a(1 + K_a^2) <= 5^{k/2}` in PR #9 (7.7), and the class product of PR #9 Section 8.3,
  step 4, is at most `37^k`.
* **Lemma E.** With the s-light threshold `δ_s k`, the third family has `Pbar = 2 exp(−δ_s M_s/8)`. In
  case (i) at least `δ_s k/8` distinct keys must flip. In case (ii) at least `(1 − δ_s)k/2` distinct keys
  are prescribed.

**New: Lemma D′.** In PR #9, Section 8.3, step 4, class `a` has at most `2K_a(2K_h + 5) + 1` band words,
where `K_a >= 1` is its number of positions and `K_h = ⌈k/h⌉`. Over the collision classes,

```math
 \prod_a\bigl(2K_a(2K_h+5)+1\bigr)\le19^{\,\sum_aK_a}\le19^k .
```

*Proof.* Class `a < h` has `K_a = ⌈(k − a)/h⌉ >= ⌈(k − h + 1)/h⌉ >= ⌈k/h⌉ − 1` positions, so
`K_h <= K_a + 1`, and the factor is at most `4K_a^2 + 14K_a + 1`. This is `19` at `K_a = 1`. For `K >= 1`
the ratio `(4(K+1)^2 + 14(K+1) + 1)/(4K^2 + 14K + 1)` is at most its value `45/19 < 19` at `K = 1`.
Hence `4K^2 + 14K + 1 <= 19^K` for every integer `K >= 1`. The classes are disjoint, so `Σ_a K_a <= k`. ∎

**New: Lemma D″ (collision classes have at least two positions).** Under the same notation,

```math
 \prod_{a\in\Sigma}\bigl(2K_a(2K_h+5)+1\bigr)\le45^{\,\sum_{a\in\Sigma}K_a/2}\le45^{k/2}.
```

*The reading of PR #9.* Line numbers refer to `effective-completion/PROOF.md` at PR #9 head `89660352`. The
reading was written up by the N1a session (radar-dd) and validated by the referee session.

1. Line 410 defines collision classes: "Call a residue class a collision class when it contains a repeated
   key; write its positions `a+sh`, `0 <= s < K_a`". Line 408 says that every occurrence of a box lies in one
   residue class modulo `h`.
2. Line 428 chooses one repeated pair per collision class. This defines `Σ`; noncollision classes get an
   absence symbol.
3. The quantities `σ_a`, `ζ_a`, `v_a`, `c_a` of Section 7.4 are defined from the chosen pair, hence only for
   `a ∈ Σ`. Section 8 fixes data with `Σ ≠ ∅` and `V_0 = span{v_a : a ∈ Σ}`.
4. Section 8.3 counts "sets of keys at arbitrary selected positions in collision classes" (line 547). Its
   band form (8.9) (line 555) and steps 1–4 use `τ_a`, `c_a`, `ζ_a`, that is, classes `a ∈ Σ`.
5. Step 4 (lines 585–588) bounds "a class" by `2K_a(2K_h+5) + 1` band words and takes the product over the
   classes of that count, that is, over `a ∈ Σ`.

*Why `K_a >= 2`.* A class in `Σ` contains a repeated key, which occupies two distinct positions
`a + s_1 h` and `a + s_2 h` of that class, by line 408. So `K_a >= 2`.

*Proof of the bound.* As in D′, the factor is at most `4K_a^2 + 14K_a + 1`. This equals `45 = 45^{2/2}` at
`K_a = 2`. For `K >= 2` the ratio `(4(K+1)^2 + 14(K+1) + 1)/(4K^2 + 14K + 1)` is at most its value
`79/45 < sqrt(45)` at `K = 2`. Hence `4K^2 + 14K + 1 <= 45^{K/2}` for every integer `K >= 2`. The classes of
`Σ` are disjoint, so `Σ_{a∈Σ} K_a <= k`. ∎

Without `K_a >= 2` the bound fails: a class of length 1 contributes up to `19 > sqrt(45)`, and `verify.py`
exhibits `(k, h)` where the product over all classes exceeds `45^{k/2}`.

N1a's Lemma D bounds every factor by its value at `K_h` and the number of classes by `2k/K_h`, which gives
`37^k`. D′ uses each class's own length, and D″ also uses that classes of `Σ` have length at least 2. Like
Lemma D, both re-bound PR #9's displayed product and do not re-derive the encoding that produces it. D″
depends in addition on the reading above.

## 3. Parameters

For real `t >= 512`, put

```math
 u=\frac{e^{t/2}}{22\,t^{5/2}},\quad D=\lceil u\rceil,\quad M=\Bigl\lfloor\frac k{32}\Bigr\rfloor,\quad
 h_0=\lceil5Dt^3\rceil,\quad M_s=\lceil4096\,Dt\rceil,
```
```math
 \epsilon=\frac1t,\quad\epsilon_{\rm reg}=\frac1{64t},\quad\eta=\frac{\epsilon_{\rm reg}}{24D},\quad
 B_0=\lceil24576\,t+4\rceil,\quad\delta_s=\frac1{16},\quad
 \gamma=\frac12-\frac{257}{128\,t},\quad p=\frac{36\,t^{7/2}}{\sqrt k},
```
```math
 F=k\Bigl(\frac t8-\frac78\log t-C\Bigr),\qquad C=\frac{403}{100}. \tag{2}
```

Family 1 keeps #12's additive tolerance `k/t`. Family 3 keeps the fraction `1/4`. As in #12, `q` is the
least power of a prime `k < P <= 2k^2` with `D log q >= F`, so `F <= D log q <= F + D(2t + log 2)` and
`Q := log q <= F/u + 3t`.

Write `ρ = 1/u`. Every analytic inequality below is reduced to terms `A t^j e^{−dt}` that are
nonincreasing on `[512, ∞)`. `verify.py` certifies each from its value at `t = 512` with `e >= 2`.

## 4. Scales and geometry

* `u >= 8` and `ρ <= 2^{−200}`, so `u <= D <= (1 + 2^{−200})u` and `D <= sqrt(k)`.
* `k/33 <= M <= k/32`, so `2M/k <= 1/16` and `k/M >= 32`.
* `5ut^3 <= h_0 <= 5Dt^3 + 1 <= sqrt(kt)/4 < 2M`.
* `M_s <= k`, `p <= 1/2`, and `L = log(1/p) = t/2 − (7/2) log t − log 36 >= t/4`.
* `F >= kt/32`.
* `Q <= (11/4) sqrt(k) t^{7/2} + 3t`.
* `J <= k^6`.
* `4MH/k <= 1/(8k^2) <= η`.
* The nonregular fraction of a canonical block is at most
  `D(12η + 3/h_0) <= 1/(128t) + 3/(5t^3) <= ε_reg` (N1b Lemma 5.2), since `h_0 >= 5Dt^3`.
* `B_0 D >= 16/η + 4` and `B_0 D >= 49`, as (I1) requires.

These are the conditions of N1b, Section 5, at the new constants.

## 5. The outer colouring

Weights follow Lemma B. Each family's incident weight is shown to be at most `1/(48k)`.

**Family 1** (N1b, with `S` from the canonical partition). `Pbar = 2 exp(−2M/t^2)`, with one event per
word. The condition is `log T_glob + log 96 + 1/8 + t <= 2M/t^2`. By #12 (3), `J <= k^6` and Lemma A, with
`log_2(2M) <= 2t`,

```math
 \log T_{\rm glob}\le4D\Lambda+32Dt+2D\log441,\qquad
 \Lambda=\log4\,\bigl(h_0+\sqrt{2M}+2t(2M)^{1/3}\bigr).
```

Multiply the condition by `16t^2/k`, and use `2M/t^2 >= k/(16t^2) − 2/t^2`. The leading terms are

```math
 \frac{320\log4\,(1+\rho)^2}{22^2}+\frac{16\log4\,(1+\rho)}{22\sqrt t}\ \le\ 0.91657+0.04461 ,
```

from `5Dt^3` in `h_0` and from `sqrt(2M) <= sqrt(k)/4`. They are evaluated with `sqrt(t) >= 22.6`. The
other five terms (the `+1` in `h_0`, `(2M)^{1/3}`, `32Dt`, `2D log 441`, and `log 96 + 1/8 + t` with
`32/k`) are monomials, each at most `1/200`. The total is below `1`.

**Family 2.** For `h_0 < h <= 2M`, at most `h·A_h` events through a label, each with
`Pbar <= 2 exp(−(1 − ε_reg)h/t^2)`. With

```math
 \phi(h)=(D+2)\log h+2D\log9+4D\log(B_0Dh+1)-(1-\epsilon_{\rm reg})h/t^2 ,
```

the incident weight is at most `2M · 2e^{1/8} e^{φ(h_0)}`, because `φ` decreases for `h >= h_0`:
`(5D + 2)/h <= (1 − ε_reg)/t^2` there. With `log h_0 <= t/2 + (1/2) log t`,
`B_0 D h_0 + 1 <= 280 k/t`, and `h_0/t^2 >= 5Dt`,

```math
 \phi(h_0)\le-D\Bigl(\frac t2+\frac72\log t-27.02\Bigr)+t+\log t ,
```

which is at most `−2t − log 192 − 1/8`, since `D >= 8`.

**Family 3** (#12, with Lemma E). `Pbar = 2 exp(−M_s/128) <= 2 exp(−32Dt)`. By #12 (5), with
`k(4M+4) + 1 <= k^2` and `2k(J+1) + 1 <= 3k^7`,
`log A_s <= D(18.5t + (1/2) log t + 6.6) + 1.5t + (1/2) log t`. Then
`log A_s + log 96 + 1/8 + t <= 32Dt` holds.

Lemma B gives one outer colouring that avoids all three families.

## 6. The outer dichotomy

As in N1b (6), with `A_0 = (1/2 − 1/t)(1 − ε_reg)`: each bit occupies at least `A_0 k − k/t` positions of a
long-period progression, and exactly

```math
 A_0-\frac1t-\gamma=\frac1{64t^2}>0 .
```

So every progression that is not `γ`-rich has a heavy label with short closest return. Here
`g = 257/128 = 1 + 1 + 1/128`: the two tolerances `1/t` and half of `ε_reg·t`. Nothing is lost to a return
block.

## 7. Rich events

**The exponent.** As in N1b (7) with general constants,

```math
 \frac{\gamma L}2=\frac t8-\frac78\log t-\frac{\log36}4-\frac g4+\frac{7g}4\frac{\log t}t+\frac g2\frac{\log36}t ,
```

so `Γ >= k(C − (1/4) log 36 − g/4) − D(2t + log 2)`.

**The errors.** These are PR #9's displayed factors, as tabulated in #12's Appendix A, at `J <= k^6`,
`D <= sqrt(k)`, `D + 4 <= 2 sqrt(k)`, `s_G + 1 <= 3k^2q^2`, `s_φ + 1 <= 6k^3`, `s_× + 1 <= 19k^4`. Each
factor's logarithm is a linear form in `Q`, `Dt`, `D`, `t` and `1`. `verify.py` (`error_bounds`) recomputes
the table from these formulas:

| factor (PR #9) | `Q` | `Dt` | `D` | `t` | `1` | in |
|---|---:|---:|---:|---:|---:|---|
| discrete data `k^{D+1} T_aug` (7.6)–(7.7) | | 17 | `log 9 + 2 log 7` | 1 | | `E_c`, `E_p` |
| integer projections `(3Dk)^D` (8.8) | | 3/2 | `log 3` | | | `E_c` |
| first arrangement `16(s_G+1)^3` | 6 | | | 6 | `log 16 + 3 log 3` | `E_c` |
| tail arrangement `(D+4)^2(s_φ+1)^{D+3}` | | 3 | `log 6` | 10 | `2 log 2 + 3 log 6` | `E_c` |
| crossing arrangement `(D+4)^2(s_×+1)^{D+3}` | | 4 | `log 19` | 13 | `2 log 2 + 3 log 19` | `E_c` |
| cells `100 D^2 q^4` (7.12) | 4 | | | 1 | `log 100` | `E_p` |
| second forms `9^D` (8.5) | | | `log 9` | | | `E_p` |

The `k`-linear factors come on top: the pairs `Π(1 + K_a^2) <= 5^{k/2}` (Lemma D) in both errors, the
subsets `2^k` in `E_c`, and the class product in `E_c`. Write `ℓ_cls` for the logarithm per position of the
class product: `(1/2) log 45` under D″, `log 19` under D′, `log 37` under D. Summing the table,

```math
 E_c\le6Q+k\bigl(\log2+\ell_{\rm cls}+\tfrac12\log5\bigr)+D(25.5t+11.93)+30t+23.1,
```
```math
 E_p\le4Q+\tfrac k2\log5+D(17t+8.29)+2t+4.61.
```

Hence `Ebar <= 5Q + (k/2)(log 10 + ℓ_cls) + D(21.25t + 10.11) + 16t + 13.86`, and
`(E_c − E_p)/2 <= Q + (k/2)(log 2 + ℓ_cls) + D(4.25t + 1.82) + 14t + 9.25`.

**The bound.** Put `κ = C − (1/4) log 36 − 257/512 − (1/2)(log 10 + ℓ_cls)`. The remaining terms of
`(Ebar − Γ + log 64 + t/2)/k` are monomials summing to less than `0.007`. When `κ > 0.007`, Lemma C's bound
is at most `1/4`, because `Γ >= log 64 >= log 4` handles its `e^{−2Γ}` term. The cut condition needs
`C − (1/4) log 36 − 257/512 − (1/2)(log 2 + ℓ_cls) >= 0.8`.

| tier | `(1/2)(log 10 + ℓ_cls)` | `C` | `κ` | cut margin |
|---|---:|---:|---:|---:|
| D″ | `2.10296` (`C` must exceed `3.5008`) | `71/20` | `>= 0.0492` | `>= 0.853` |
| D′ | `2.62351` (`C` must exceed `4.0213`) | `403/100` | `>= 0.0086` | `>= 0.813` |
| D | `2.95675` (`C` must exceed `4.3546`) | `35/8` | `>= 0.0204` | `>= 0.825` |

## 8. Non-rich events

By #12 (8), `log T_K <= 6Q + D(16t + 5) + 4.5t + 6`.

*Case (i), at least `k/16` s-light positions.* At least `k/128` distinct keys must flip (Lemma E). The
probability is at most `2 T_K 2^k p^{k/128} <= 1/8` as soon as
`log 2 + (log T_K + log 16)/k <= t/512`. This holds since `L >= t/4` and `t >= 512`.

*Case (ii).* At least `(15/32)k` distinct keys are prescribed (Lemma E), with
`log B_run <= 2t + 560 sqrt(k) t^{−1/2}`. So

```math
 \log T_K+\log B_{\rm run}+\log16\le\frac{33}2\sqrt k\,t^{7/2}+560\frac{\sqrt k}{\sqrt t}+D(16t+5)+24.5t+9
 <\frac{15}{32}pk=\frac{135}8\sqrt k\,t^{7/2},
```

and the probability is at most `1/8`.

The failure probability is below `1/4 + 1/8 + 1/8 < 1`. The digit product gives (1) for `t >= 512`, which
includes every `k >= 2^739`.

## 9. Thresholds

* `F >= kt/9` iff `g(t) := t/72 − (7/8) log t − C >= 0`. `g` increases for `t > 63`, and `k >= 2^n`
  gives `t >= n log 2`. With certified rational bounds for `log 2`:
  - `C = 71/20`: `g(960 log 2) > 0.0040`, so `c = 1/9` holds from `k >= 2^960`;
  - `C = 403/100`: `g(1015 log 2) > 0.0047`, from `k >= 2^1015`;
  - `C = 35/8`: `g(1054 log 2) > 0.0022`, from `k >= 2^1054`.
  `verify.py` also checks `g((n − 1) log 2) < 0` in each tier, so the exponent `n` cannot be lowered by
  this argument.
* The coefficient `1/8 − ((7/8) log t + C)/t` increases for `t >= 1`. At `t = 1024 log 2` it exceeds
  `0.1119`, `0.1112` and `0.1107` in the three tiers.

## 10. Boundary

Re-proved here: Lemmas D′ and D″ (D″ on the reading of PR #9 given in Section 2), the scale inequalities of Sections 4–9 at these constants, and their
certificates. Imported:

* N1b's Lemmas 5.1–5.3 and (I1)–(I2), with the stronger eligibility threshold, which is justified above;
* N1a's Lemmas A–E;
* #12's interfaces and its Family 3;
* PR #9's displayed factors.

The local lemma, Hoeffding's inequality and PR #9's encodings are not formalised.
