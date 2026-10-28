# The retuned endpoint bound: k >= 2^370, and C within 0.05 of the template floor

## 1. Claim and status

All logarithms are natural, and `t = log k`. This is a conditional proof draft, not an independently
reviewed theorem. It reruns the composed endpoint (`2026-10-20-ChaloupeMusic-composed-endpoint/`, head
`ebfae63`, cited as "composed") with new constants and a lower starting point. The architecture, the
families, the lemmas and the error table are the composed endpoint's, unchanged.

**Conditional theorem.** Assume the finite source interfaces of PR #12, Section 2, and the finite factors
of PR #9 that the composed endpoint imports. For every integer `k >= 2^370` and every integer `r >= 2`,

```math
 W_r(k)>\left(\frac{k^{1/8}}{e^{C}(\log k)^{7/8}}\right)^{k\lfloor\log_2 r\rfloor}, \tag{1}
```

with `C` from the table. The six tiers are proved and checked separately.

| Lemma A | class product | `C` | `c = 1/9` from | composed `C` | template floor `C^*` |
|---|---|---:|---|---:|---:|
| Rosser–Schoenfeld | D″, `45^{k/2}` | `173/50 = 3.46` | `2^950` | `71/20` (`2^960`) | `3.41219` |
| Rosser–Schoenfeld | D′, `19^k` | `199/50 = 3.98` | `2^1009` | `403/100` (`2^1015`) | `3.93275` |
| Rosser–Schoenfeld | D, `37^k` | `108/25 = 4.32` | `2^1048` | `35/8` (`2^1054`) | `4.26599` |
| Erdős (as composed) | D″ | `7/2` | `2^954` | `71/20` | `3.41219` |
| Erdős (as composed) | D′ | `201/50 = 4.02` | `2^1014` | `403/100` | `3.93275` |
| Erdős (as composed) | D | `109/25 = 4.36` | `2^1053` | `35/8` | `4.26599` |

The range starts at `k >= 2^370` instead of `2^739`, in every tier. Each `C` beats the composed constant of
its class tier and stays above the floor `C^*` of `2026-10-26-ChaloupeMusic-template-limit/`
(Theorem B). The Rosser–Schoenfeld tiers are within `0.055` of that floor. No coefficient above `1/8` is
claimed.

## 2. What changes

**Lemma A′ (Rosser–Schoenfeld).** For `1 <= h_0 <= 2M`,

```math
 \log\lambda<1.01624\,\bigl(h_0+\sqrt{2M}+\log_2(2M)\,(2M)^{1/3}\bigr).
```

*Proof.* N1a's Lemma A writes `log λ = Σ_{j>=1} ϑ(min(h_0, (2M)^{1/j}))`. The terms `j >= 3` vanish
for `j > log_2(2M)` and are each at most `ϑ((2M)^{1/3})`. Rosser and Schoenfeld, *Approximate formulas for
some functions of prime numbers*, Illinois J. Math. 6 (1962), 64–94, inequality (3.16) (Theorem 9):
`ϑ(x) < 1.01624 x` for every real `x > 0`. ∎

The Erdős tiers keep N1a's Lemma A, `ϑ(x) < x log 4`, unchanged. Write `c_A` for `1.01624` or `log 4`.

**Parameters.** As in the composed endpoint, Section 3, with

```math
 u=\frac{e^{t/2}}{A_D\,t^{5/2}},\quad h_0=\lceil B_h D t^3\rceil,\quad p=\frac{A_p\,t^{7/2}}{\sqrt k},
```

| Lemma A | `A_D` | `B_h` | `A_p` |
|---|---:|---:|---:|
| Rosser–Schoenfeld | `73/4` | `91/20` | `59/2` |
| Erdős | `85/4` | `227/50` | `69/2` |

against `22, 5, 36` in the composed endpoint. Unchanged: `D = ⌈u⌉`, `M = ⌊k/32⌋`,
`M_s = ⌈4096 Dt⌉`, `ε = 1/t`, `ε_reg = 1/(64t)`, `η = ε_reg/(24D)`, `B_0 = ⌈24576t + 4⌉`,
`δ_s = 1/16`, `γ = 1/2 − (257/128)/t`, `F = k(t/8 − (7/8) log t − C)`. The choice of `q` is unchanged.

**Starting point `t >= 256`.** `k >= 2^370` gives `t >= 370 log 2 > 256`. The composed endpoint used
`t >= 512` in four places, which are redone below. Every monomial certificate `A t^j e^{−dt} <= B` is
re-certified at `t_0 = 256` (`verify.py`, one list per Lemma A tier).

## 3. The inequalities at the new constants

Names in parentheses are the checks in `verify.py`.

**Scales** (composed, Section 4). `u >= 2^100` (`u_at_least_2^100`), so `ρ = 1/u <= 2^{−100}` and
`D >= 2^100`, and `u >= 4t` (`u_above_4t`). `B_h D t^3 + 1 <= sqrt(kt)/4`, because `B_h(1+ρ)/A_D < 1/4`
in both tiers (`h0_plus_one_term`). The other scale conditions are the composed ones, re-certified at 256.
The short-block regularity budget is `12ε_reg/24 + 3/(B_h t^3) <= ε_reg`.

**First family** (composed, Section 5). In units of `16t^2/k`, the leading terms are

```math
 \frac{64\,B_h\,c_A(1+3\rho)}{A_D^2}+\frac{16\,c_A(1+\rho)}{A_D\sqrt t}\ \le\
 \begin{cases}0.88851+0.05569 & \text{(Rosser–Schoenfeld)}\\ 0.89202+0.06524 & \text{(Erdős)}\end{cases}
```

with `sqrt(t) >= 16` (was `22.6`). The five small terms are the composed ones, each at most `1/200` at
`t >= 256`. The totals are `0.96920` and `0.98226`.

**Second family** (composed, Section 5). With `h_0 <= sqrt(kt)/4`, `B_0 <= 24577t` and
`D <= (1+ρ)u`, `B_0Dh_0 + 1 <= c_B k/t` with `c_B = 24577(1+ρ)/(4A_D) + 1/100`. Then

```math
 \phi(h_0)\le-D\,m(t)+t+\log t,\qquad m(t)=(B_h-\tfrac92)\,t+\tfrac72\log t-c_2,\qquad
 c_2=2\log9+4\log c_B+B_h\,\epsilon_{\rm reg}t .
```

`m` is nondecreasing, and `m(256) >= 4.466` (Rosser–Schoenfeld) or `>= 2.514` (Erdős). So
`D m(t) >= D >= 4t >= 3t + log t + log 192 + 1/8`, which is the condition. The composed endpoint used
`D >= 8` and a margin of order `t` here. The margin `B_h − 9/2` drops from `1/2` to `1/20` or `1/25`,
because `D >= 2^100` does the work. `φ` is decreasing from `h_0`, since `(1 − ε_reg)B_h t >= 7`.

**Third family.** Unchanged (`M_s`, `δ_s` and `A_s` do not depend on the new constants).

**Rich events** (composed, Section 7). `κ = C − (1/4) log A_p − 257/512 − (1/2)(log 10 + ℓ_cls)` must exceed
`0.007`, and the cut margin `C − (1/4) log A_p − 257/512 − (1/2)(log 2 + ℓ_cls)` must reach `0.8`.

| tier | `κ >=` | cut margin `>=` |
|---|---:|---:|
| RS-D″ / RS-D′ / RS-D | `0.00899` / `0.00843` / `0.01519` | `0.8137` / `0.8131` / `0.8199` |
| E-D″ / E-D′ / E-D | `0.00984` / `0.00929` / `0.01605` | `0.8145` / `0.8140` / `0.8207` |

The six monomials of the remaining terms are re-certified at 256 (`rich_*`).

**Case (i)** (composed, Section 8). The composed endpoint used `L >= t/4` and `t/512 >= 1`, which fails at
`t = 256`. Instead, `L/t = 1/2 − ((7/2) log t + log A_p)/t` increases for `t >= 3`, so for `t >= 256`,
`L/128 >= (t/256) L(256)/128 >= L(256)/128`. With `L(256) = 128 − (7/2) log 256 − log A_p`, this exceeds
`log 2 + 3/100` by at least `0.0987` or `0.0975`. The three `caseI_*` monomials bound
`(log T_K + log 16)/k` by `3/100`.

**Case (ii).** `log B_run <= 2t + b sqrt(k) t^{−1/2}` with `b = 4097(1+ρ)(3 + 1/256)/A_D`, and the condition is

```math
 \frac{6A_D}8+\frac b{t^4}+\frac{17(1+\rho)}{A_D t^5}+\frac1{100}\ <\ \frac{15}{32}A_p
```

at `t = 256`. The ratio of the two sides is below `0.99056` (Rosser–Schoenfeld) and `0.98613` (Erdős).

The failure probability is below `1/4 + 1/8 + 1/8 < 1`, and the digit product gives (1) for `t >= 256`.

## 4. Thresholds

As in the composed endpoint, Section 9: `F >= kt/9` iff `g(t) = t/72 − (7/8) log t − C >= 0`, `g` increases
for `t > 63`, and `g` is certified positive at `t = n log 2` (lower bound for `log 2`) and negative at
`(n − 1) log 2` (upper bound), for the `n` of the table in Section 1. The coefficient of (1) at `k = 2^1024`
exceeds `0.11203` (RS-D″) and `0.11197` (E-D″).

## 5. Against the template floor

`2026-10-26-ChaloupeMusic-template-limit/` proves that no parameter choice in this template gives a
constant below `C^* = (1/2)(log 10 + ℓ_cls) + 1/2 + (1/4) log(18√2)` for all large `k`. `verify.py`
recomputes `C^*` with certified bounds and checks `C > C^*` in every tier (`template_floor`). This is a
consistency check: a `C` below `C^*` would mean a mistake here or there. The remaining gap under D″,
`3.46 − 3.41219`, is mostly `c_A = 1.01624` instead of `1`, the margin `B_h − 9/2`, `δ_s = 1/16`, the
`sqrt(2M)` term, and rounding.

## 6. Boundary

Re-proved here: Lemma A′ (from Rosser–Schoenfeld, cited with its exact statement and range), and every
inequality of the composed Sections 4–9 at the new constants and `t >= 256`, with their certificates.
Imported unchanged: the composed endpoint's lemmas and error table, N1b's Lemmas 5.1–5.3 and (I1)–(I2),
N1a's Lemmas B–E, #12's interfaces and Family 3, and PR #9's displayed factors. A 90-digit decimal replay
of every inequality on a grid of `t` from 256 to `10^5` finds no failure (`decimal_replay`). It is a
control, not a proof.
