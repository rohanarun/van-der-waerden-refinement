# Retuned constants at the conditional 1/8 endpoint

## 1. Claim, status, and what changes

All logarithms are natural, and `t = log k`. This note builds on the
contribution `2026-10-15-1337isnot1337-logarithmic-loss`
(PR #12, head `029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5`). It keeps that
construction, its event families and its finite source interfaces, and
changes numerical constants and four estimates. It is a conditional proof
draft, not an independently reviewed theorem.

**Conditional theorem.** Assume the finite source interfaces of PR #12,
Section 2, and the finite factors of PR #9 displayed in its Sections 7.3,
8.2 and 8.3, which PR #12's Appendix A already imports. For every integer
`k >= 2^1024` and every integer `r >= 2`,

```math
W_r(k)>\left(\frac{k^{1/8}}{e^{9/2}\log k}\right)^{k\lfloor\log_2 r\rfloor}. \tag{1}
```

Moreover

```math
W_r(k)>k^{(k/9)\lfloor\log_2 r\rfloor}\quad(k\ge2^{1163}),\qquad
W_r(k)>k^{(1093/10000)\,k\lfloor\log_2 r\rfloor}\quad(k\ge2^{1024}). \tag{2}
```

PR #12 proves (1) with `e^{20}` in place of `e^{9/2}`, the coefficient 1/9 from
`k >= 2^4096`, and, at `k = 2^1024`, a coefficient of about 0.0876. Nothing here
passes 1/8, and the denominator `log k` remains.

| Quantity | PR #12 | here |
|---|---:|---:|
| `t0` (`k >= 2^1024` means `t >= 1024 log 2 > 709`) | 512 | 709 |
| `u = e^{t/2}/(A_D t^3)`, `A_D` | 4096 | 4 |
| `h0 = ceil(B_H D t^3)`, `B_H` | 256 | 5 |
| `M_s = ceil(B_S D t)`, `B_S` | 4096 | 4096 |
| `p = A_p t^4/sqrt(k)`, `A_p` | 65536 | 8 |
| `eps_reg = e_2/t`, `eta = eps_reg/(8D)`, `e_2` | 1 | 1/4 |
| s-light threshold `delta_s` | 1/2 | 1/16 |
| `gamma = 1/2 - g/t`, `g` | 4 | 25/8 |
| `C` in `F = k(t/8 - log t - C)` | 20 | 9/2 |

`M = floor(k/t)`, `eps = 1/t`, the additive tolerance `k/t` of the first
family, the fraction 1/4 of the third family, and the forms of `u`, `M`,
`h0`, `M_s`, `p` are those of PR #12. In particular the second-order term
`k log log k` is untouched.

The gain comes from five lemmas in Section 2. Each is independent of the
scales `M`, `D`, `p`, so it can be reused on another parameter choice. Their
effect on the binding rich-event inequality is, in units of `k`:

| Source of loss | PR #12 | here |
|---|---:|---:|
| digit-rank error `E` (PR #12: `E <= 11k`, needs `Gamma >= E`) | 10 | `(1/2) log 370 = 2.957` |
| `(1/4) log A_p` | 2.773 | 0.520 |
| `g/4` | 1 | 0.781 |
| total, compared with `C` | 13.77 + slack (C = 20) | 4.258 + 0.242 (C = 9/2) |

## 2. Five lemmas

**Lemma A (dilation).** For `1 <= h0 <= 2M`, the dilation
`lambda = prod_{l <= h0 prime} l^{floor(log(2M)/log l)}` satisfies

```math
\log\lambda<\log4\,\Bigl(h_0+\sqrt{2M}+\log_2(2M)\,(2M)^{1/3}\Bigr). \tag{A}
```

*Proof.* The exponent of `l` counts the `j >= 1` with `l^j <= 2M`, so

```math
\log\lambda=\sum_{j\ge1}\vartheta\bigl(\min(h_0,(2M)^{1/j})\bigr).
```

The term `j = 1` is at most `theta(h0)`, the term `j = 2` at most
`theta(sqrt(2M))`, and every term with `j >= 3` at most `theta((2M)^{1/3})`.
Terms vanish once `(2M)^{1/j} < 2`, so at most `log_2(2M)` of them are
nonzero. Erdős's bound `theta(x) < x log 4` (all real `x >= 1`) finishes the
proof. That bound follows by induction: primes in `(m+1, 2m+1]` divide
`binom(2m+1, m) <= 4^m`, so `theta(2m+1) - theta(m+1) <= m log 4`. ∎

PR #12 used `log lambda <= pi(h0) log(2M) <= 60 h0`. At the scales below,
(A) gives `log lambda <= (1.39 + o(1)) h0`.

**Lemma B (local-lemma weights).** Consider a finite family of bad events,
each using at most `k` independent label variables. Suppose that each event
`E` has a bound `P(E) <= Pbar(E) <= e^{-1/8}/2`, and that for every variable
`x`

```math
\sum_{E\ni x}\bar P(E)e^{1/8}\le\frac1{16k}. \tag{B}
```

Then the weights `z_E = Pbar(E) e^{1/8}` satisfy the asymmetric local lemma,
so some outcome avoids every event.

*Proof.* Each `z_F <= 1/2`, so `1 - z_F >= exp(-2 z_F)`. The neighbours of
`E` share one of its at most `k` variables, so their weights sum to at most
`1/16`. Hence `z_E prod_{F ~ E}(1 - z_F) >= z_E e^{-1/8} = Pbar(E) >= P(E)`. ∎

PR #12 used `z_E = exp(-w)` for `P(E) <= 2exp(-2w)`. Lemma B keeps the full
Hoeffding exponent, which doubles the entropy each family can afford.

**Lemma C (asymmetric rich split).** In PR #12, Section 8, suppose that for
each digit rank `0 <= R <= D` the certificates number at most
`exp(R log q + E_c)` and the progressions with a repeated key at most
`exp((2D - R) log q + E_p)`. Put `Ebar = (E_c + E_p)/2` and
`Gamma = gamma k L/2 - D log q`. If `Gamma > |E_c - E_p|/2`, then the
probability that some gamma-rich progression is monochromatic is at most

```math
2\bigl[\,2(D+1)e^{\bar E-\Gamma}+e^{-2\Gamma}\bigr]. \tag{C}
```

*Proof.* Take `T_R = (R log q + Gamma + (E_c - E_p)/2)/L`. Then
`0 < T_R < gamma k`, because `R <= D` and `gamma k L = 2 Gamma + 2 D log q`.
Both exponents of PR #12's split become `Ebar - Gamma`:

```math
R\log q+E_c-T_RL=\bar E-\Gamma,\qquad
(2D-R)\log q+E_p-(\gamma k-T_R)L=\bar E-\Gamma .
```

The no-repeat class contributes `q^{2D} p^{gamma k} = e^{-2 Gamma}`. Sum over
the two targets, the `D + 1` ranks and the two cases. ∎

PR #12 used one error `E >= max(E_c, E_p)` for both cases, which needs
`Gamma >= E` instead of `Gamma >= Ebar`.

**Lemma D (arithmetic on PR #9's displayed factors).** In PR #9:

- Section 7.3 encodes one repeated pair per collision class, with
  `prod_a (1 + K_a^2)` choices and `sum_a K_a = k`.
- Step 4 of Section 8.3 gives at most `2K_a(2K_h + 5) + 1` band words per
  class, over at most `h` classes, with `K_a <= K_h = ceil(k/h)` and
  `h K_h <= 2k`, where `h < k` (Section 7.2).

Then

```math
\prod_a(1+K_a^2)\le5^{k/2},\qquad
\prod_a\bigl(2K_a(2K_h+5)+1\bigr)\le37^k. \tag{D}
```

*Proof.* `1 + K^2 <= 5^{K/2}` for every integer `K >= 0`: it holds for
`K <= 2` (with equality at 2), and the ratio
`(1 + (K+1)^2)/(1 + K^2)` is at most `sqrt 5` for `K >= 2`.

For the classes, every factor is at most `P(K_h) = 4K_h^2 + 10K_h + 1`, and
there are at most `h <= 2k/K_h` of them. Since `h < k`, `K_h >= 2`. The
quantity `P(K)^{2/K}` is at most `37 = P(2)` for every integer `K >= 2`.
`verify.py` checks `P(K)^2 <= 37^K` for `2 <= K < 4000`, and `P(K) <= 4^K`
covers larger `K`. ∎

PR #12 used `4^k` and `256^k`. With the subsets (`2^k`), the certificate
error now has `k`-coefficient `log 74 + (1/2) log 5` and the progression
error `(1/2) log 5`, so `Ebar` has `k`-coefficient `(1/2) log 370`.

**Lemma E (s-light threshold).** Use PR #12's third family with the s-light
threshold `delta_s k` instead of `k/2`, keeping the 1/4 fraction. Its events
have probability at most `2 exp(-delta_s M_s/8)` by weighted Hoeffding,
since `sum w^2 <= (k/M_s) k_L` and `k_L >= delta_s k`. In the non-rich
case (i), at least `delta_s k/4` positions need a flip, carried by at least
`delta_s k/8` distinct keys. In case (ii), more than `(1 - delta_s)k`
positions are s-heavy (multiplicity greater than `k/M_s`), so the run code
prescribes at least `(1 - delta_s)k/2`
distinct keys. With `delta_s = 1/16`, these numbers are `k/128` and
`15k/32`, against PR #12's `k/16` and `k/4`.

## 3. Parameters

For real `t = log k >= 709`, put `s = e^{t/2}` and

```math
u=\frac{s}{4t^3},\quad D=\lceil u\rceil,\quad M=\lfloor k/t\rfloor,\quad
h_0=\lceil5Dt^3\rceil,\quad M_s=\lceil4096Dt\rceil,
```
```math
\epsilon=\frac1t,\quad\epsilon_{\rm reg}=\frac1{4t},\quad
\eta=\frac{\epsilon_{\rm reg}}{8D},\quad\delta_s=\frac1{16},\quad
\gamma=\frac12-\frac{25}{8t},\quad p=\frac{8t^4}{s},\quad
F=k\Bigl(\frac t8-\log t-\frac92\Bigr). \tag{3}
```

As in PR #12, `q` is the least power of a source prime `k < P <= 2k^2`
with `D log q >= F`. So `F <= D log q <= F + D(2t + log 2)`.

Write `rho = 1/u = 4t^3 e^{-t/2}`, so that `D <= u(1 + rho) <= 2u`. Every
inequality below that involves `t` is reduced to a sum of terms
`a t^j e^{-dt}`, each nonincreasing on `[709, oo)`, with an exact rational
bound at 709. `verify.py` names each certificate.

## 4. Scales, geometry and entropy

- `u >= 1` (`u_at_least_one`), `p <= 1/2` (`flip_probability`), and
  `L = log(1/p) = t/2 - 4 log t - log 8 >= t/4`. The last uses
  `log t <= t/32` for `t >= 512`, as in PR #12, and `t/8 >= log 8`.
- `h0 < 2M` (`h0_below_2M`), `D <= k/64`, `M_s <= k`, `2M/k <= 2/t <= 1/16`,
  and `4MH/k <= 4/(k^2 t) <= eta = 1/(32Dt)` (`rotating_drift`).
- `D(4 eta + 1/h0) = 1/(8t) + D/h0 <= 1/(8t) + 1/(5t^3) <= eps_reg`.
- `(D + 1) log q <= kt`, so `J <= 2k^3 t + 2 <= k^6` (`mesh_count`). In
  detail, `(D + 1) log q <= 2D log q <= 2F + 2D(2t + log 2)`, with
  `2F <= kt/4` and `2D(2t + log 2) <= (s/t^3)(2t + 1) <= 3s/t^2`. Since
  `e^{-t/2} <= 1/2` (`mesh_D_log_q`), `3s/t^2 <= 3k/(2t^2) <= 3kt/4`.

These are the conditions of PR #12, Section 5. The remaining source
conditions follow from `H = k^-2`, `k >= 16` and `M <= k/t`, as there.

**Global words.** PR #12's count (3), with `3k^2(k^2 lambda + J) + 1 <= 7k^8 lambda`
and Lemma A, gives

```math
\log T_{\rm glob}\le4D\Lambda+32Dt+2D\log441,\qquad
\Lambda=\log4\,\bigl(h_0+\sqrt{2M}+2t(2M)^{1/3}\bigr), \tag{4}
```

using `log_2(2M) <= 2t`.

**Local and short-period words.** PR #12's counts (4) and (5) are used as
stated, with `B_0 = ceil(128/eps_reg + 4) <= 512t + 5`.

## 5. The outer colouring

The three families of PR #12, Section 6, are kept, with Lemma E's threshold
in the third. Weights follow Lemma B, so it suffices that the incident
weight of each family at each label is at most `1/(48k)`.

**First family.** Each event has `Pbar = 2exp(-2M/t^2)`, as in PR #12 (21)-(22).
There is at most one event per word, so the condition is
`log T_glob + log 96 + 1/8 + t <= 2M/t^2`. Multiply by `t^3/k`. Use
`2Mt/k >= 2 - 2t/k`, (4), `D^2 <= u^2(1+rho)^2 = k(1+rho)^2/(16t^6)` and
`h0 <= 5Dt^3 + 1`. The condition then follows from

```math
\tfrac54\log4\,(1+3\rho)+\sqrt2\log4\,(1+\rho)\,t^{-1/2}
+2\log4\,e^{-t/2}+4\cdot2^{1/3}\log4\;te^{-t/6}
+16te^{-t/2}+\log441\;e^{-t/2}+(t^4+5t^3+2t)e^{-t}\le2 . \tag{5}
```

The terms come, in order, from `5Dt^3` in `h0`, from `sqrt(2M)`, from the
`+1` in `h0`, from `log_2(2M)(2M)^{1/3}`, from `32Dt`, from `2D log 441`, and
from `log 96 + 1/8 + t` and `2Mt/k >= 2 - 2t/k`. Every term is
nonincreasing on `[709, oo)`, and the sum is at most `1.807` at `t = 709`
(`first_family`). The leading term `(5/4) log 4 = 1.733` is
`4 B_H log 4/A_D^2`.

**Second family.** For `h0 < h <= 2M`, eligible patterns through a label
number at most `A_h` (PR #12 (4)). Each event, on `l >= h/2` regular labels,
has `Pbar = 2exp(-2l/t^2) <= 2exp(-h/t^2)`. Put

```math
\phi(h)=(D+1)\log h+2D\log9+4D\log(B_0Dh+1)-h/t^2 .
```

Since `phi'(h) <= (5D + 1)/h - 1/t^2 < 0` for `h >= h0 >= (5D + 1)t^2`, the
incident weight is at most `2M · 2e^{1/8} e^{phi(h0)}`.

Now `B_0 D h0 + 1 <= (160k/t^2) X`, with `X - 1 <= 1/100`
(`second_family_log_ratio`), and `h0 <= 3s`. Together with
`h0/t^2 >= 5Dt`, these give

```math
\phi(h_0)\le-D\bigl(\tfrac t2-26\bigr)+\tfrac t2+\log3 .
```

Here `26 >= log 3 + 2 log 9 + 4 log 160 + 0.04`. The condition becomes
`u(t/2 - 26) >= 2.5t + 6`, that is
`(2.5t + 6)rho <= t/2 - 26` (`second_family_margin`).

**Third family.** `Pbar = 2exp(-M_s/128) <= 2exp(-32Dt)` by Lemma E. With
`J <= k^6`, `k(4M + 4) + 1 <= k^2` and `2k(J + 1) + 1 <= 3k^7`, PR #12 (5) gives

```math
\log A_s\le D(18.5t+7\log3)+1.5t+\log3 .
```

The condition `log A_s + log 96 + 1/8 + t <= 32Dt` holds because
`11t - 7 log 3 - 6 >= 0` (`third_family`).

Lemma B then gives one outer colouring that avoids all three families.

## 6. The outer dichotomy

As in PR #12, Section 7, each bit occupies at least `A_0(k - h) - k/t`
positions, with `A_0 = (1/2 - 1/t)(1 - 1/(4t))` and `h <= 2M <= 2k/t`.
Exactly,

```math
\Bigl(\tfrac12-\tfrac1t\Bigr)\Bigl(1-\tfrac1{4t}\Bigr)\Bigl(1-\tfrac2t\Bigr)-\tfrac1t
-\Bigl(\tfrac12-\tfrac{25}{8t}\Bigr)=\frac5{2t^2}-\frac1{2t^3}\ge0 ,
```

so every progression that is not gamma-rich has a heavy label with short
closest return (`dichotomy`). In general, `g = e_1 + e_2/2 + 1 + e_3` with
`e_1 = e_3 = 1` (the two tolerances), `e_2 = 1/4`, and the `1` that comes
from the lost return block.

## 7. Rich events

**The exponent.** Expanding `gamma k L/2`, and using
`D log q <= F + D(2t + log 2)`,

```math
\Gamma\ge k\Bigl(\tfrac92-\tfrac34\log2-\tfrac{25}{32}\Bigr)
+k\,\frac{2g\log t+(g/2)\log8}{t}-D(2t+\log2)
\ge3.19889k-D(2t+\log2).
```

**The errors.** PR #9's displayed factors are the ones tabulated in PR #12's
Appendix A, with Lemma D in place of `4^k` and `256^k`. With `J <= k^6`,
`D <= s` and `D + 4 <= 5s`, they give

```math
E_c\le6\log q+D(25.5t+\log150822)+30t+c_c+k\bigl(\log74+\tfrac12\log5\bigr),
```
```math
E_p\le4\log q+D(17t+\log3969)+2t+\log100+\tfrac k2\log5,
```

with `c_c = log 16 + 3 log 3 + 4 log 5 + 3 log 114`. Hence, with `c_D = (1/2) log(150822 · 3969)` and `c_0 = (c_c + log 100)/2`,

```math
\bar E\le5\log q+D(21.25t+c_D)+16t+c_0+\tfrac k2\log370 .
```

**The bound.** Put `kappa = 9/2 - (3/4) log 2 - 25/32 - (1/2) log 370`, so
that `kappa >= 0.24213`. Lemma C's probability (C) is at most `1/4` as soon
as `Gamma - Ebar >= log 64 + t/2`, since `D + 1 <= 2D <= 2s`. That
inequality holds because

```math
\frac{5\log q}k+\frac{D(23.25t+c_D+\log2)}k+\frac{16.5t+c_0+\log64}k\le\kappa ,
```

using `log q <= s t^4/2 + 2t + 1` (`rich_side`).

The cut condition of Lemma C also holds. Here `E_c >= E_p`, and

```math
\frac{E_c-E_p}2\le\log q+D\bigl(4.25t+\tfrac12\log38\bigr)+14t+\tfrac{c_c-\log100}2+\tfrac k2\log74 .
```

With `9/2 - (3/4) log 2 - 25/32 - (1/2) log 74 >= 1.0468`, this gives
`Gamma > (E_c - E_p)/2` (`rich_cut`). `verify.py` records the
`k`-coefficients `(1/2) log 370 = 2.9568` here and `10` in PR #12.

## 8. Non-rich events

**Case (i): at least `k/16` s-light positions.** By Lemma E, at least
`k/128` distinct keys must flip. The PR #12 union over key words and subsets
gives a total of at most `2 T_K 2^k p^{k/128}`. Since `L >= t/4`, this is at
most `1/8` as soon as

```math
\log2+\frac{\log T_K+\log16}k\le\frac t{512}.
```

Here `log T_K <= 6 log q + D(16t + log 144) + 4.5t + log 128` by PR #12 (8).
At `t = 709` the right side is `1.3848` and the left side `0.6932 + o(1)`
(`case_i`).

**Case (ii): fewer s-light positions.** Each event has probability at most
`exp(-(15/32)pk)`, with `(15/32)pk = 3.75 s t^4`. Its code count is PR #12's
`B_run = h0 (M_s + 1)(2k^3)^{M_s}`, so
`log B_run <= 8192 s/t + 4t + 10`. We have `6 log q <= 3 s t^4 + 12t + 6`, and
the remaining terms divided by `s t^4` are below `0.75 - 4.6·10^{-11}`
(`case_ii`). The total is at most `1/8`.

Sections 7 and 8 bound the failure probability by
`1/4 + 1/8 + 1/8 < 1`. A valid cyclic two-colouring of size `N = q^D >= e^F`
exists, and the digit product gives (1).

## 9. Thresholds

**Coefficient 1/9.** `F >= kt/9` when `t/72 - log t - 9/2 >= 0`. This
function increases for `t >= 72` and is positive at `t = 806`, where it
exceeds `0.0023`. And `k >= 2^1163` gives `t >= 1163 log 2 > 806`. The
function is negative at `1162 log 2`, so the argument stops at `2^1163`.

**All `k >= 2^1024`.** The coefficient `1/8 - (log t + 9/2)/t` increases for
`t >= 1`. At `t = 709.78 <= 1024 log 2` it is at least `1093/10000`.

**Generic coefficient.** For `0 < c < 1/8`, `Delta = 1/8 - c`, and `j` least
with `2^j >= 2/Delta`, PR #12's formula holds with 9/2 in place of 20:
`K(c) = 2^{n(c)}` with `n(c) = max(1024, ceil(4(j + 9/2)/Delta))`. The proof
of PR #12, Section 10, does not depend on the value of `C`.

## 10. Verification boundary

`verify.py` uses exact fractions, and encloses logarithms by atanh series.
It certifies every analytic inequality above for all real `t >= 709`, checks
the exact identities, Lemma D's integer inequalities and the thresholds, and
replays the main inequalities from the definitions in 90-digit decimal
arithmetic at eight values of `t`. Its negative controls change one
constant at a time and require the corresponding certificate to fail.

These checks do not formalise the local lemma or the imported geometric and
digit-rank encodings of PR #9 and the source. Lemma D re-bounds two of
PR #9's displayed finite products. It relies on their displayed form, not on
a re-derivation of the encodings that produce them.
