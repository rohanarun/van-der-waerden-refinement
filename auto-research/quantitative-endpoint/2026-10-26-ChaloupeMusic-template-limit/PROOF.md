# The seven-eighths loss is the limit of the union-bound template

## 1. Claims and status

All logarithms are natural, and `t = log k`. This is a proof draft, not an independently reviewed theorem.
It concerns the proofs of the conditional endpoint bound

```math
 W_r(k)>\left(\frac{k^{1/8}}{e^{C}(\log k)^{\theta}}\right)^{k\lfloor\log_2 r\rfloor} \tag{1}
```

in open PR #12 (`θ = 1`, `C = 20`), N1b (`2026-10-20-ChaloupeMusic-seven-eighths/`, `θ = 7/8`, `C = 35/2`)
and the composed endpoint (`2026-10-20-ChaloupeMusic-composed-endpoint/`, `θ = 7/8`, `C = 71/20` under
Lemma D″). All three prove (1) with `N = q^D >= e^F` and the same chain: an outer colouring from three
local-lemma families, a dichotomy, and union bounds over rich and non-rich progressions. Section 2 calls
the inequalities that this chain must satisfy *the template*. They involve parameters
`D, M, h_0, ε_1, ε_2, γ, p, q`, chosen freely as functions of `k`.

**Theorem A (exponent).** Every parameter choice that satisfies the template has
`F <= k(t/8 − (7/8) log t + O(1))`. So no choice of parameters in the template proves (1) with `θ < 7/8`.

**Theorem B (constant).** Every parameter choice that satisfies the template has

```math
 \frac Fk\ \le\ \frac t8-\frac78\log t-C^*+o(1),\qquad
 C^*=\frac12\bigl(\log10+\ell_{\rm cls}\bigr)+\frac12+\frac14\log\bigl(18\sqrt2\bigr), \tag{2}
```

where `ℓ_cls` is the per-position logarithm of the class product of PR #9, Section 8.3, step 4, in the
tier used. So a template proof of (1) with `θ = 7/8` for all large `k` needs `C >= C^*`.

| tier (class product) | `ℓ_cls` | `C^*` | delivered `C` | gap |
|---|---|---:|---:|---:|
| D″ (`45^{k/2}`) | `(1/2) log 45` | `3.41219…` | `71/20` | `0.1378` |
| D′ (`19^k`) | `log 19` | `3.93275…` | `403/100` | `0.0973` |
| D (`37^k`) | `log 37` | `4.26599…` | `35/8` | `0.1090` |

**Ledger.** The proof attributes `7/8` term by term (Section 4). Any route to `θ < 7/8` has to break one of
the four inequalities named there.

| source of the loss | share of `7/8` |
|---|---:|
| non-rich union over affine key words: `p >= 12 log q/k`, with `log q = F/D` of order `kt/D` | `1/4` |
| second-family entropy `>= 9 D log D` (order `Dt`) against a tail `h ε_2^2` | `1/8` |
| first-family tolerance `ε_1` (Hoeffding `ε_1^2` in `D^2`, then `ε_1` lost from `γ`) | `1/4` |
| second-family tolerance `ε_2` (Hoeffding `ε_2^2` in `h_0`, then `ε_2` lost from `γ`) | `1/4` |

The optimum of the template has `ε_1, ε_2 = (1 + o(1))/t`, which is the choice of PR #12, N1b and the
composed endpoint.

## 2. The template

Fix `k`, a tier, and parameters. Write `F = D log q`, `f = F/k`, `L = log(1/p)`, and let
`e^* = (1/2)(log 10 + ℓ_cls)`. The proofs cited in Section 1 succeed only if all of the following hold.
Each item cites the step that forces it, and each is weaker than what that step actually checks.

* **(T1) Stationary scale.** `M <= k/32`. The source's stationary eligibility needs `2M/k <= 1/16`
  (N1b, Section 5).
* **(T2) First family.** `T_glob e^{−2Mε_1^2} <= 1`, where `kε_1` is the additive tolerance of Family 1.
  Its events have Hoeffding bound `2 exp(−2Mε_1^2)`, the template counts the events through a label by
  the bound `T_glob` of #12 (3), and the incident weight must be below `1/(48k)`. That bound is
  `[9(3k^2(k^2λ+J)+1)^2]^{2D} >= λ^{4D}`. By N1a's Lemma A identity,
  `log λ = Σ_{j>=1} ϑ(min(h_0, (2M)^{1/j})) >= ϑ(h_0)` since `h_0 <= 2M`, where `ϑ` is Chebyshev's
  function. So (T2) implies
  `4Dϑ(h_0) <= kε_1^2/16`.
* **(T3) Second family.** For `h = h_0 + 1`: `A_h e^{−(h+1)ε_2^2} <= 1`, where `ε_2 l` is the tolerance on
  a pattern's `l` regular labels. The template counts the triples through a label by `h·A_h` (N1b (I2)),
  and bounds each weight by the one at its smallest admissible `l`, which is at most `⌈h/2⌉` because
  blocks of length `⌈h/2⌉` occur. That weight is at least `2 exp(−(h+1)ε_2^2)`. The bound `A_h` of
  #12 (4) is `h^{D+1}[9(B_0Dh+1)^2]^{2D} >= h^{D+1}(B_0Dh)^{4D}` with `B_0 >= 1`, so
  (T3) implies `(D+1) log h + 4D log(Dh) <= (h+1)ε_2^2`.
* **(T4) Dichotomy.** `γ <= 1/2 − ε_1 − ε_2`. The template needs `γ < A_0 − ε_1` with
  `A_0 = (1/2 − ε_2)(1 − ε_reg)` (N1b (6), composed Section 6).
* **(T5) Non-rich, case (ii).** `6 log q <= pk/2`. The case needs
  `T_K e^{−(1−δ_s)pk/2} < 1`, with `T_K` the bound of #12 (8), which is at least
  `16(kDq^2)^3 >= q^6`.
* **(T6) Rich.** `γkL/2 − D log q > e^* k`. Lemma C needs `e^{Ē−Γ} < 1/4` with
  `Γ = γkL/2 − D log q`, and `Ē` contains the `k`-linear factors `2^k`, `Π(1+K_a^2) <= 5^{k/2}` (in both
  errors) and the class product (in `E_c`). Their average is `e^* k` (composed, Section 7).

Theorems A and B use (T1)–(T6) and nothing else, so they hold for every parameter choice, including
`k`-dependent constants, every `δ_s`, `M_s`, `ε_reg` and `η`.

## 3. Proof of Theorem B

Let `C_0 = C^* + 1`. If `f <= t/8 − (7/8) log t − C_0`, (2) holds. So assume

```math
 f>\frac t8-\frac78\log t-C_0. \tag{3}
```

All `o(1)` and `O(·)` below are as `t → ∞`, uniform in the parameters.

**Step 1 (flip rate).** (T5) and `log q = F/D` give `p >= 12f/D`, so `L <= log D − log(12f)`.

**Step 2 (rich).** (T4) and (T6) give

```math
 f<\frac12\Bigl(\frac12-\epsilon_1-\epsilon_2\Bigr)L-e^*. \tag{4}
```

So `L > 0`, `ε_1 + ε_2 < 1/2`, and `L > 4f`. With (3), `L >= t/2 − (7/2) log t − 4C_0`. With Step 1,
`log D >= L + log(12f) >= t/2 − O(log t)`.

**Step 3 (the two families).** By (T3), `(h+1)ε_2^2 >= D(5 log h + 4 log D) >= 9D log D`, since
`(h+1)ε_2^2 >= D log h` forces `h >= D` (because `ε_2 < 1/2` and `log h >= 1`). With Step 2,

```math
 (h_0+2)\,\epsilon_2^2\ \ge\ 9D\Bigl(\frac t2-O(\log t)\Bigr). \tag{5}
```

In particular `h_0 → ∞`. By (T2) and the prime number theorem, `ϑ(h_0) = (1 + o(1))h_0`, so
`h_0 <= (1 + o(1)) kε_1^2/(64D)`. Insert this in (5) and divide by `9Dt/2`. The term `2ε_2^2`
contributes `O(1/(Dt))`, and `D >= e^{t/3}`. This gives

```math
 D^2\le(1+o(1))\frac{k\,\epsilon_1^2\epsilon_2^2}{288\,t}. \tag{6}
```

**Step 4 (the logarithm of the flip rate).** By (6) with `ε_i < 1/2`, `log D <= t/2 + o(1)`. By (4) and
Step 1, `f < L/4 <= t/8 + o(1)`. So with (3), `log(12f) = log(3t/2) + o(1)`. Write `x_i = log(1/ε_i)`. Step 1
and (6) give `L <= B − x_1 − x_2`, with

```math
 B=\frac t2-\frac32\log t-\log\bigl(18\sqrt2\bigr)+o(1),
```

since `(1/2) log 288 + log(3/2) = log(12√2 · 3/2) = log(18√2)`.

**Step 5 (the tolerances).** Since (4) is increasing in `L`, and `0 < L <= B − x_1 − x_2`,

```math
 f<\frac B4-e^*-\sum_{i=1,2}\Bigl(\frac{x_i}4+\frac{\epsilon_i}2(B-x_1-x_2)\Bigr). \tag{7}
```

If `x_1 + x_2 >= 4 log t`, the sum is at least `log t`. Then
`f < t/8 − (11/8) log t + O(1)`, which contradicts (3) for large `t`. Otherwise `B − x_1 − x_2 >= B'`
with `B' = B − 4 log t`. Each summand is at least

```math
 \min_{x\in\mathbb R}\Bigl(\frac x4+\frac{B'}2e^{-x}\Bigr)=\frac{1+\log(2B')}4=\frac14\log t+\frac14+o(1),
```

attained at `e^{−x} = 1/(2B')`, that is `ε_i = (1 + o(1))/t`. So

```math
 f<\frac t8-\frac38\log t-\frac14\log(18\sqrt2)-e^*-\frac12\log t-\frac12+o(1)
 =\frac t8-\frac78\log t-C^*+o(1). \qquad\blacksquare
```

**Theorem A** follows. Every `ℓ_cls` in use is nonnegative, so `C^* >= 0`. (Chebyshev's
`ϑ(x) >= x/2` for large `x`, in place of the prime number theorem, gives Theorem A alone with a weaker
constant.)

**Corollary.** Suppose a template proof gives (1) with `θ = 7/8` and a constant `C` for all `k >= k_0`.
Then `f >= t/8 − (7/8) log t − C` for every large `t`, and (2) forces `C >= C^*`. ∎

## 4. The ledger

Each share is the coefficient of `log t` contributed to `f` by one step:

* `(1/4)·1`: Step 1. `log(12f) = log t + O(1)`, because `F` is of order `kt` and the non-rich union runs
  over at least `q^6` key words. So `L` loses `log t`, and (4) multiplies `L` by `1/4`.
* `(1/4)·(1/2)`: Step 3. The second-family entropy is of order `Dt`, which puts `t` in the denominator
  of (6). So `log D` loses `(1/2) log t`.
* `1/4 + 1/4`: Step 5. Each tolerance enters `log D` as `log ε_i`, and `γ` as `−ε_i`. The best balance
  costs `(1/4) log t` each.

Breaking the `7/8` needs one of the following:

1. A non-rich bound whose union is over `q^{o(1)}` words, or which prescribes far more than `k` keys.
2. A second-family count of `o(Dt)` per pattern.
3. A first-family union over fewer than `λ^{Θ(D)}` words. Then the factor `D h_0` in (T2) shrinks, and
   `ε_1` or `ε_2` leaves (6).
4. A concentration step whose tolerance is not paid in `γ`.

None is available in the cited proofs.

## 5. Where the delivered constants lose

At finite `t` the template's best constant is below `C^*`, and increases to it (`verify.py`, a numerical
optimisation, given as evidence only). The gap between the delivered `71/20` and `C^* = 3.41219…` comes
from:

* Erdős's `ϑ(x) < x log 4` in Lemma A, about `(1/8) log log 4 ≈ 0.041`;
* `h_0 = ⌈5Dt^3⌉` where `4.5Dt^3` is the entropy, about `(1/8) log(10/9) ≈ 0.013`;
* `δ_s = 1/16`, which prescribes `15k/32` keys rather than `k/2`, about `(1/4) log(16/15) ≈ 0.016`;
* the `sqrt(2M)` term of Lemma A, the small first-family terms, `ε_reg`, the margin `κ >= 0.007`, and the
  rounding of `A_p` and `C`, about `0.07` together.

These are approximate attributions, not claims.

## 6. Boundary

Proved here: Theorems A and B, and the corollary, from (T1)–(T6). Each of (T1)–(T6) is read off the cited
proofs. They are necessary for those proofs as written, not for every proof of (1). The prime number
theorem is used as a published theorem. Nothing here changes the conditional status of (1) or its
interfaces.
