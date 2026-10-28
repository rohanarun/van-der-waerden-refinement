# Repeated keys cost nothing: every coefficient below 1/12, explicit 2/25

This sharpens the two new counts of `rank-certificate-proof.md` (Lemmas A
and C) so that the rich-event condition becomes

```math
2c<\gamma b ,
```

with everything else unchanged. The sharpened outer coloring, keys,
affine-signature count, and digit product are as before. With them, this
proposes

```math
W_r(k)>k^{(2/25)k\lfloor\log_2 r\rfloor}
```

for sufficiently large k, with the threshold independent of r, and admits
every fixed c below 1/12. Compared with the source's 1/100000 the ratio is
exactly 8000; compared with the previous explicit choices 1/16 and 1/25 it
is 32/25 and 2. The endpoint 1/12 is the supremum of the region, not a
claimed value. No explicit finite threshold is obtained.

`2c < γb` is exactly the condition that a union bound over all `q^{2D}`
progressions would give if no key ever repeated. In that sense the two-point
multiplicity no longer costs anything on the rich side. The coefficient
remains bounded by `γb/2 < (1/2)(1/3)/2 = 1/12`, because `γ < 1/2`
(balance) and `b < 1/3` (affine entropy) are untouched.

## Credit and dependencies

This note depends on `rank-certificate-proof.md`: its Sections 1 and 2
(facts (R1)–(R5) and the carry vectors `Δm_a`), the identity of its
Lemma A, and identity (4) of its Lemma C. Those in turn restate the
repeated-key structure of the unmerged upstream proposal
[rohanarun/van-der-waerden-refinement#4](https://github.com/rohanarun/van-der-waerden-refinement/pull/4),
pinned at
[`4b4e80e`](https://github.com/rohanarun/van-der-waerden-refinement/blob/4b4e80ea5e0ffec956577004905f22659af0bff5/repeated-key-certificate-proof.md).
The original construction is OpenAI's, at the pinned source revision linked
in the README.

## The idea

In `rank-certificate-proof.md` the certificate of Lemma A paid
`2 log q` for each direction of `V = span{Δm_a : a in Σ}`, because
it encoded each projection `<Y_{a_0}, v>` as a real number at resolution
`q^{-2}`. The count of Lemma C saved only `log q` per direction, because it
used one integer digit form per class. The worst case, `ρ = D/2`, cost
`5/2` in units of `D log q`.

Both sides are, however, made of base-`q` digits, and in the **same**
pattern:

* the start point `Y_{a_0}` has digits `y_l`, and `q^2 <Y_{a_0}, v>` is fixed,
  up to a bounded tail, by two integer forms in those digits;
* the step return `β` has digits `e_l`, and each vertex constraint fixes
  `q^2 <Δm_a, β>` to within 3. This fixes the same two integer forms
  in the `e_l`: the first exactly, the second up to 9 values.

Both are governed by one integer, the digit rank `R` below. The certificate
costs `R log q` and the progression count `(2D - R) log q`, whose sum is `2D`
for every `R`.

## Notation

Use the notation of `rank-certificate-proof.md`. For an integer vector
`v in Z^D`, define two coefficient vectors on digit positions
`l = 0, ..., D-1`:

```math
(S_1v)_l=v_{l+1},\qquad (S_2v)_l=v_{l+2}\quad(v_{D+1}:=0).
```

For a progression with collision classes `Σ` put
`V = span_Q{Δm_a : a in Σ}` and define its **digit rank**

```math
R=\dim_{\mathbb Q}\bigl(S_1V+S_2V\bigr)\in\{0,\dots,D\},
```

so `ρ <= R <= min(2ρ, D)`. With no repeated key, `R = 0`.

**Digits of a start point.** For `n in G` let `y_0, ..., y_{D-1}` be the
balanced base-`q` digits of `λn mod q^D` (`|y_l| <= (q-1)/2`, since
`q` is odd). Then `|sum_{l<i} y_l q^{l-i}| < 1/2`, so each coordinate is
exactly `Y_i(n) = sum_{l<i} y_l q^{l-i}`. Hence for every `v in Z^D`

```math
q^2\langle Y(n),v\rangle=q\langle S_1v,y\rangle+\langle S_2v,y\rangle
+\langle v,F\rangle,\qquad
F_i=\sum_{l\le i-3}y_l\,q^{\,l-i+2},\quad |F_i|\le1 .
\tag{5}
```

**Digits of the step return.** As in Lemma C,
`β_i = sum_{l<i} e_l q^{l-i}` with `|e_l| <= 2Hq + 2H`, and

```math
q^2\langle v,\beta\rangle=q\langle S_1v,e\rangle+\langle S_2v,e\rangle+R_v,
\qquad |R_v|\le\frac{3|v|_1}{k^2}.
\tag{6}
```

(`audit_math.py` checks (5) and (6) on exact instances.)

## Two counts with the same digit rank

**Lemma A\* (digit certificate).** Fix the discrete data of
`rank-certificate-proof.md`, Section 2, with digit rank `R`. The number of
literal key sets `{κ(n_j) : j in S}`, over all progressions with these
data and all sets `S` of positions in collision classes, is at most

```math
\exp\bigl(R\log q+O(\log q+D\log k+k)\bigr).
```

*Proof.* By the identity of Lemma A and (2), every position `j = a + sh` of
a collision class has

```math
f_j=G_j(U_1,U_2,W)-2q^2\langle Y_{a_0},\Delta m_a\rangle+(c_a+s)\zeta_a ,
```

where `G_j` is affine in the three global reals `q^2 U_1`, `q^2 U_2`, `W`
with coefficients fixed by the discrete data, and `ζ_a in (-1, 1)`.
Apply (5) at `n = n_{a_0}`:

```math
q^2\langle Y_{a_0},\Delta m_a\rangle
=q\langle S_1\Delta m_a,y\rangle+\langle S_2\Delta m_a,y\rangle
+\tau_a,\qquad
\tau_a=\langle\Delta m_a,F\rangle,\quad |\tau_a|\le Dh .
```

Encode a fixed-rule basis `u_1, ..., u_R` of
`S_1 V + S_2 V` chosen among the vectors `S_1 Δm_a`, `S_2 Δm_a`,
and the `R` integers `<u_r, y>`. Each has absolute value at most
`D h q`, so this costs `R(log q + O(log k))`. By linearity these values fix
`<S_1 Δm_a, y>` and `<S_2 Δm_a, y>` for every `a in Σ`.
The `τ_a` are the values at `Δm_a` of one linear functional,
`v -> <v, F>`, so they are affine in `ρ` real parameters
`φ_l = <v_l, F>` (for the basis `v_l` of `V` of Lemma A).

Each band is now `f_j = K_j + G_j(globals) - 2τ_a(φ) + (c_a + s) ζ_a`
with `K_j` known. Count band words in four steps, each by the source's
arrangement lemma (equality signs included, on the realizable set):

1. Since `0 <= f_j <= Dq^2/4`, `G_j` lies in
   `[-K_j - 2Dh - K, Dq^2/4 - K_j + 2Dh + K]`, an interval of length
   `O(Dq^2)`. The signs of `G_j - n` over the `O(kDq^2)` integers `n` in
   these intervals fix `floor(G_j)`. In dimension 3 this gives
   `exp(6 log q + O(log k))` outcomes.
2. Inside such a cell, the signs of `frac(G_j) - 2τ_a(φ) - δ` for
   `|δ| <= 2Dh + 2` fix `floor(frac(G_j) - 2τ_a)`. These are `poly(k)`
   affine functions of `(globals, φ)`, in dimension `3 + ρ`, giving
   `exp(O(D log k))` outcomes.
3. As in Lemma A, the order of the `ζ_a`-crossings within each class,
   and their positions relative to `+-1`, are fixed by `poly(k)` further
   affine signs. This gives `exp(O(D log k))` outcomes.
4. Each class then has at most `2K_a(2K+5) + 1` choices for its word,
   giving `exp(O(k))` in total.

The start point `n_0` and the step are never encoded.

**Lemma C\* (digit count).** The number of progressions `(n_0, d)` with at
least one repeated key and digit rank `R` is at most

```math
\exp\bigl((2D-R)\log q+O(\log q+D\log k+k)\bigr).
```

*Proof.* Encode as in Lemma C: `n_0`, the discrete data, and the cells of
`q^2 T` and `(k+1) q^2 w`. These fix `X_a` with
`|X_a - q^2 <Δm_a, β>| < 3` for every `a in Σ`, by (4). By (6),
with `|Δm_{a,i}| <= h`,
`|<S_2 Δm_a, e>| <= 4D(k+2)q/k^2 < q/8` and `|R_v| < 1`. Hence
`<S_1 Δm_a, e>` is the integer nearest `X_a/q`, and
`<S_2 Δm_a, e>` lies in the window `X_a - q<S_1 Δm_a, e> + [-4, 4]`
(at most 9 choices, recorded in the code). Take the fixed-rule basis `u_1, ..., u_R`
of `S_1 V + S_2 V` from these vectors, and a set `L` of `R` digit positions
with a nonsingular minor. Given `e` off `L`, the `R` values `<u_r, e>`
determine `e_L`. The count is
`q^D * 9^R * (4Hq + 4H + 1)^{D-R} * exp(O(log q + D log k + k))`.

## The rich-event estimate

**Theorem.** Under the sharpened outer input, if `2c < γb` then the
probability that some `γ`-rich progression is monochromatic tends to
zero, uniformly over the allowed source primes.

*Proof.* As in `rank-certificate-proof.md`, Section 4, with `ρ` replaced by
`R`. Put `κ_R = R/D` and `ν_R = (2D - R)/D`, so `κ_R + ν_R = 2`
**for every** `R`. Let `μ = (γb - 2c)/2 > 0` and
`θ_R = (κ_R c + γb - ν_R c)/(2b)`, which lies in
`(0, γ)`. Then

```math
b\theta_R-\kappa_Rc=b(\gamma-\theta_R)-\nu_Rc=\mu .
```

Progressions of digit rank `R` with at least `θ_R k` flipped keys in
collision classes are covered by Lemma A\* certificates of exactly
`ceil(θ_R k)` keys, with total probability
`exp(-μk log k + o(k log k))`. The others need more than
`(γ - θ_R) k` distinct flipped keys. They are counted by Lemma C\*,
or by the trivial `q^{2D}` when no key repeats, with the same bound. Summing
over the `D + 1` digit ranks and the two targets gives `o(1)`. The affine
estimate, outer dichotomy, and digit product are unchanged.

## Sufficient region and supremum

```math
a,b,c>0,\quad 2a<m<1,\quad b<a,\quad 2a<1-b,
```

```math
0<\epsilon<\tfrac12,\quad 0<\epsilon_{\rm reg}\le\tfrac12,\quad 0<\delta,\quad
\gamma<(\tfrac12-\epsilon)(1-\epsilon_{\rm reg})(1-\delta),\quad 2c<\gamma b .
```

Since `γ < 1/2` and `b < 1/3`, `c < γb/2 < 1/12`. Every fixed
`c < 1/12` is admitted by the same limits as before. The endpoint is not
asserted, and `audit_math.py` rejects it.

On the rich side, `2c < γb` is also exactly what the union bound
gives for progressions with no repeated key, which need `γk` distinct
flips. Going further therefore needs one of:

* a different idea for those progressions;
* `γ` above `1/2`;
* `b` above `1/3`, which needs a smaller affine signature count than the
  `k^{2a}` label entropy and the `q^6` band word allow.

None is attempted here.

## Explicit choice

Keep every exponent and balance constant of the 1/25 and 1/16 choices:

```math
a=\tfrac{333}{1000},\quad m=\tfrac45,\quad b=\tfrac{331}{1000},\quad
\delta=\epsilon=\epsilon_{\rm reg}=\tfrac1{200},\quad
\gamma=\tfrac{97}{200},\quad c=\tfrac2{25}.
```

| Inequality | Positive margin |
|---|---:|
| m > 2a | 67/500 |
| m < 1 | 1/5 |
| b < a | 1/500 |
| 2a < 1 − b | 3/1000 |
| γ < (1/2−ε)(1−ε_reg)(1−δ) | 40499/8000000 |
| 2c < γb, as γb/2 − c | 107/400000 |

The last entry is

```math
\frac12\cdot\frac{97}{200}\cdot\frac{331}{1000}-\frac2{25}
=\frac{32107}{400000}-\frac{32000}{400000}=\frac{107}{400000},
```

the same margin that certified 1/25 under `2c < γb/2`. Here the
coefficient is doubled. Also `μ = 107/400000`. Since
`2γb/5 = 32107/500000 < 2/25`, the choice lies outside the region of
`rank-certificate-proof.md`, so it is not a reparametrization of it.

`parameters.json` stores this choice under `digit_rank_proposals`.
`audit_math.py` checks:

* every margin, in exact fractions;
* `κ_R + ν_R = 2` for every `R`;
* both group margins on a grid of digit ranks;
* the decompositions (5) and (6), on exact instances;
* `ρ <= R <= min(2ρ, D)`, on random carry spans.

It also rejects five boundary controls: `b = a`, `b = 1 - 2a`,
`c = γb/2`, γ at the balance bound, and `c = 1/12`.

## What is and is not claimed

New here are the digit decompositions (5) and (6), and the observation that
the certificate and the progression count share the digit rank `R`. Lemmas
A\* and C\* replace Lemmas A, B, and C of `rank-certificate-proof.md`.

Everything else is imported:

* the repeated-key facts of upstream #4;
* the sharpened outer input;
* the two-point norm-band lemma;
* the source's lemmas.

None of this has been independently reviewed. Passing the scripts
establishes the inequalities and identities, not the transfer as a theorem.
No finite coloring, finite van der Waerden record, or runtime improvement
follows. The threshold is not explicit and may be very large.
