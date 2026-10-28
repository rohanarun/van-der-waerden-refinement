# The 1/9 threshold of the union-bound template: 2^940 proved, nothing in this chain between e^256 and 2^934

## 1. Claims and status

All logarithms are natural, `t = log k`, `f = F/k`. This is a conditional proof draft, not an independently
reviewed theorem. "Retuned" is `2026-10-26-ChaloupeMusic-retuned-endpoint/` (head `8916c20`), "template" is
`2026-10-26-ChaloupeMusic-template-limit/`, whose inequalities (T1)-(T6) are read off the proofs of PR #12,
N1b and the composed endpoint.

**Theorem T (threshold).** Assume the finite source interfaces of PR #12, Section 2, and PR #9's factors,
as the retuned endpoint does. Then `W_r(k) > k^{(k/9)⌊log_2 r⌋}` for every integer `r >= 2` and every
`k >= 2^940` under Lemma D″ (`2^1000` under D′, `2^1038` under N1a's D). The retuned endpoint gives
`2^950`, `2^1009`, `2^1048`.

**Theorem F (floor).** Under (T1)-(T6) alone, no parameter choice gives `F >= kt/9` for any `k` with
`e^256 <= k <= 2^934` under D″ (`2^994` under D′, `2^1032` under D). This is a floor for this chain only:
(T1)-(T6) are necessary for the cited proofs as written, not for every proof of the bound.

So the chain's 1/9 threshold lies in `(2^934, 2^940]` under D″. Section 4 says what fixes it.

## 2. Proof of Theorem F

Fix `t` and parameters satisfying (T1)-(T6), and suppose `f >= t/9`. Write `s = ε_1 + ε_2`,
`L = log(1/p)`, `e^* = (1/2)(log 10 + ℓ_cls)`.

1. **Flip rate.** (T5) gives `p >= 12 log q / k = 12f/D`, so `L <= log D − log(12f) <= log D − log(4t/3)`.
2. **Rich.** (T6) and (T4) give `f < γL/2 − e^* <= (1/2 − s)L/2 − e^*`. As `f > 0`, `L > 0` and `s < 1/2`,
   and `L > 4(f + e^*) >= 4(t/9 + e^*)`.
3. **Scale of D.** By 1 and 2, `log D >= L + log(12f) >= l_D := 4(t/9 + e^*) + log(4t/3)`.
4. **Second family.** (T3) with `h = h_0 + 1` reads `(h + 1)ε_2^2 >= (D+1) log h + 4D log(Dh)`. If `h < D`,
   the left side is below `D/4` (`ε_2 < 1/2`) and the right side above `4D`: impossible. So `h >= D`, and
   `(h_0 + 2)ε_2^2 >= 9D log D >= 9D l_D`.
5. **First family.** (T2) gives `4Dϑ(h_0) <= kε_1^2/16`. Here `h_0 >= D − 1 >= e^{l_D} − 1 >= e^45`, and
   Broadbent-Kadiri-Lumley-Ng-Wilk, Theorem 1 with `k = 0` and `X_0 = e^45`, give `ϑ(x) >= x(1 − m_0)` for
   `x >= X_0`, with `m_0 = ε(45) + 1.03883(e^{−45/2} + e^{−30} + e^{−36})`. Their Theorem 2 gives
   `|ψ(x) − x| <= ε(b)x` for all `x >= e^b`, with `ε(45) = 1.09073·10^{−8}` from their Table 8. So
   `m_0 < 1.1084·10^{−8} < δ = 2·10^{−8}` (`verify.py` checks it in rationals), `ϑ(h_0) >= (1 − δ)h_0`, and
   `h_0 <= kε_1^2/(64D(1 − δ))`.
6. **Combining 4 and 5.** `9D l_D <= ε_2^2(kε_1^2/(64D(1−δ)) + 2)`, so with `ε_2^2 < 1/4`,
   `D^2 <= a + D/(18 l_D)`, `a = kε_1^2ε_2^2/(576(1−δ)l_D)`. So `D^2(1 − x) <= a` with
   `x = 1/(18 l_D D)`, and `log D <= (1/2) log a − (1/2) log(1 − x) <= (1/2) log a + x`. For `t >= 256`,
   `l_D >= 70` and `D >= e^{l_D}`, so `x <= 2^{−100}`.
7. **Conclusion.** Insert 6 in 1 and 2, and use `log ε_1 + log ε_2 <= 2 log(s/2)`:

```math
 f<\tfrac12\,\psi(s)-e^*,\qquad \psi(s)=\Bigl(\tfrac12-s\Bigr)\Bigl(A+2\log\tfrac s2\Bigr),\qquad
 A=\tfrac t2-\tfrac12\log\bigl(576(1-\delta)\,l_D\bigr)+2^{-100}-\log\tfrac{4t}3 .
```

`ψ'' = −2/s − 1/s^2 < 0`, so `ψ` is concave on `(0, 1/2)`, and its tangent at any `s_0` bounds its maximum.
If `max ψ/2 − e^* <= t/9`, the assumption `f >= t/9` is contradicted. ∎

`plancher.py` runs this in exact arithmetic. It covers `t ∈ [256, 934 log 2]` by 96 intervals `[t_a, t_b]`,
with `A` bounded at `t_b` and `t/9` at `t_a` (`l_D` increases with `t`). At `t = 935 log 2` the bound is
positive: the argument says nothing there. The exact margins at `934 log 2` and `935 log 2` are in
`RESULT.json`. Compared with template-limit, Section 3, nothing is asymptotic: `log(12f)` is taken at
`f = t/9`, and `log D` is bounded below by `l_D` instead of `t/2 − O(log t)`.

## 3. Proof of Theorem T

**What changes from the retuned endpoint.** Three things. Everything else (families, lemmas, error table,
the choice of `q`, `M`, `M_s`, `ε_reg`, `η`, `B_0`, `δ_s`, `γ = 1/2 − G/t`, `G = 2 + 1/128`, Lemma A′ with
Rosser-Schoenfeld's `1.01624`) is the retuned endpoint's.

1. **`F = kt/9` directly**, instead of `F = k(t/8 − (7/8) log t − C)`. The digit product gives
   `W_r(k) > e^{F⌊log_2 r⌋}` as before. `F` enters the proof in four places: `log q <= F/D + log P` (in
   `E_c`, `E_p`, `T_K`), `Γ = γkL/2 − F − D log P`, and two size conditions. Larger `F` only hurts in the first
   two, and the size conditions are `F >= kt/32` and the bound `F <= kt/8` used by the monomials
   `Q_over_k`, `rich_5Q` and `caseI_6Q`. Both hold for `F = kt/9`.
2. **The rich inequality keeps its positive terms.** With `L = t/2 − (7/2) log t − log A_p` and
   `γ = 1/2 − G/t`,

```math
 \frac{\gamma L}2-\frac t9=h(t)-\frac{\log A_p}4-\frac G4+\frac74\,G\,\frac{\log t}t+\frac G2\,\frac{\log A_p}t,
 \qquad h(t)=\frac t{72}-\frac78\log t ,
```

   exactly, the identity of the retuned endpoint minus `t/9`. The retuned endpoint drops the last two terms
   to get a constant uniform in `t`. They are about `0.040` at `t ≈ 651`. The rich condition of the
   retuned endpoint, Section 3, becomes

```math
 h(t)-\frac{\log A_p}4-\frac G4+\frac74\,G\,\frac{\log t}t+\frac G2\,\frac{\log A_p}t-\bar k-S(t)>0,
 \qquad \bar k=\tfrac12(\log2+\ell_{\rm cls}+\log5),
```

   with `S(t) = (5Q + D(23.25t + 10.81) + 16.5t + 18.1)/k <= 4·10^{−6}` (four monomials certified at `T_0`).
   `h` increases for `t > 63`; `log t/t` decreases for `t > e`; and `log A_p (G/(2t) − 1/4)` decreases in
   `t` (its derivative is `−G log A_p/(2t^2)`). On each interval `[a, b]` the left side is therefore at least
   `h(a)`, plus the two `t`-dependent terms at `b`, minus the constants. `verify.py` covers
   `[N_0 log 2, N_0 log 2 + 64]` this way, and beyond bounds `log A_p (G/(2t) − 1/4)` below by `−log A_p/4`
   and uses `h` alone. The second rich inequality, `Γ > (E_c − E_p)/2`, reads
   `γL/2 − t/9 − (log 2 + ℓ_cls)/2 − S′(t) > 0` with `S′ = (Q + D(6.25t + 2.52) + 14t + 9.25)/k`. Term by term
   `S′ <= S` (`Q <= 5Q`, `6.25 <= 23.25`, `2.52 <= 10.81`, `14t + 9.25 <= 16.5t + 18.1`), and
   `(log 2 + ℓ_cls)/2 < k̄`, so the first inequality implies the second.
3. **Constants for `t >= T_0 = ⌊940 log 2⌋ = 651`.** Every monomial certificate is re-certified at `T_0`,
   and the residual terms of the rich inequality and of case (ii) at `10^{−6}` instead of `1/1000` and
   `1/100`. Then:
   * `B_h = 451/100` (retuned `91/20`). The second-family margin `m(T_0) = (B_h − 9/2)T_0 + (7/2) log T_0 − c_2`
     must reach `1`; at `T_0 = 651`, `B_h − 9/2 = 1/100` is enough (retuned needed `1/20` at `256`).
   * `A_D = 1805/100` (retuned `73/4`). It is bound by `h_0 <= sqrt(kt)/4`, that is `B_h(1+ρ)/A_D < 1/4`,
     not by the first family, which has slack (certified total `0.96136`, against `1`).
   * `A_p = 2568/100` (retuned `59/2`). Case (ii) needs `6F/(Dk)·sqrt(k) t^{−7/2} + … < (15/32)A_p`. With
     `F = kt/9` the first term is `6A_D/9`, where the retuned endpoint had `6A_D/8` from `F <= kt/8`.

The smallest `N_0` for which every budget and the rich cover pass is `940` (D″), `1000` (D′), `1038` (D).
At `N_0 − 1` the rich cover fails, so this certificate goes no lower. A 90-digit decimal replay of the
retuned endpoint's sixteen inequalities, with `F = kt/9`, on 65 values of `t` from `940 log 2` to `10^4`,
finds no failure, and finds the rich inequality negative at `939 log 2`. It is a control, not a proof.

## 4. What fixes the threshold

The threshold is the first `t` where the rich inequality of Section 3 holds. Under D″, at `t = 940 log 2`
(the sum is the margin, `3.3800 + 0.0399 − 2.1029 − 0.5020 − 0.8114 ≈ +0.0036`; the cover's worst interval
gives `0.00315`):

| term | value | from |
|---|---:|---|
| `h(t) = t/72 − (7/8) log t` | `3.3800` | the exponent `7/8` (template-limit, Theorem A) |
| `k̄` | `2.1029` | `2^k`, `5^{k/2}` and the class product of PR #9 |
| `G/4` | `0.5020` | the two tolerances `ε_1 = ε_2 = 1/t` paid in `γ` |
| `log A_p/4` | `0.81143` | the flip rate: `A_p >= (32/15)(6/9)A_D`, `A_D > 4B_h`, `B_h > 9/2` |
| kept terms, `(7/4)G log t/t + (G/2) log A_p/t` | `+0.03994` | dropped by the retuned endpoint |
| `S(t)` | `<= 4·10^{−6}` | residual terms |

One unit of `n` in `2^n` moves `h` by about `0.0087`. So each `0.01` of constant is worth about `1.15` in
`n`, and the lower-order terms only matter through these constants. Against the floor's computation
(Section 2), the remaining gap of six is mostly two constraints that (T1)-(T6) do not contain (approximate
attributions, not claims):
`h_0 <= sqrt(kt)/4`, which forces `A_D > 4B_h ≈ 18.04` where (T2)-(T3) alone allow about `16.4` (about `2.7`
in `n`), and the factor `15/32` of case (ii) (`δ_s = 1/16`) where (T5) has `1/2` (about `1.9`). The
tolerances held at `1/t` and the rounding of the constants account for the rest. Lowering the threshold
further, within this chain, means relaxing one of these: `h_0 <= sqrt(kt)/4` in the composed endpoint's scale
conditions, or `δ_s`. Below `2^934` the chain cannot go, whatever its constants (Theorem F).

## 5. Boundary

Proved here: Theorem F from (T1)-(T6) and the cited bound on `ϑ`; the inequalities of Section 3 at the new
constants and `t >= 651`, with their certificates. Imported unchanged: everything the retuned endpoint
imports, and its inequalities other than the rich one and case (ii), re-certified at `T_0`. The status of
the bound (conditional on PR #12's interfaces and PR #9's factors) is unchanged.
