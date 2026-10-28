# The least admissible matrix profile

**Result.** The scalar profile constraints that the 9/4 matrix-multiplication paper derives
have a *least element*, in closed form:

```math
P_\circ(a,b)=H_u\Bigl(v+\frac{u-1}{2}\Bigr),\qquad
H_u=\prod_{m=1}^{u-1}\Bigl(1+\frac1{3m}\Bigr)=\frac{\Gamma(u+1/3)}{\Gamma(4/3)\,\Gamma(u)},
\qquad u=\min(a,b),\ v=\max(a,b).
```

Every profile satisfying the listed constraints dominates `P_o` pointwise, and `P_o` satisfies
them and the rank envelope at `t = 3/4`. Three consequences:

1. **Sharp finite values.** The least possible diagonal value is
   `min P(a,a) = L_a = ((3a-1)/2) H_a` at every `a`. This is the intermediate bound (5.2) in the
   proof of the paper's growth lemma, attained at every `a` simultaneously; the lemma's stated
   bound `a^(4/3)` is not attained (`L_2 = 10/3 > 2^(4/3)`). For example `L_2 = 10/3`,
   `L_3 = 56/9`, `L_8 = 499928/19683`.
2. **Sharp constant.** `L_a / a^(4/3)` increases strictly to
   `kappa = 3/(2 Gamma(4/3)) = 1.67977...`, certified in `[1.679751, 1.679770]`. The repository's
   profile `P_*` has `(3/2)^(4/3) = 1.71707...`; the paper's final inequality uses `1`.
3. **A one-profile test for new constraints.** Adding further valid inequalities to the list can
   exclude `t = 3/4` (and so start to improve `omega <= 9/4` by this route) only if `P_o` violates
   them (Corollary 3 states the exact criterion). Five valid families that the paper does not use (Kronecker substitution, stride
   restriction, multiples, Clebsch-Gordan of order `k`, alternating sector chains) are proved
   here to hold for `P_o`. With all five added, `t = 3/4` is still admissible and `P_o` is still
   the least element: the 9/4 barrier of `research-note.tex` survives them.

This is structural research on the abstract obstruction. It is not a tensor character, it does
not change the matrix-multiplication exponent, and it does not touch the van der Waerden chain.
It has not been reviewed by a human.

Base: `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`. From the repository root:

```sh
python3 -B auto-research/matrix-profile/2026-10-20-ChaloupeMusic-least-admissible-profile/verify.py
```

Expected: exit 0, `"status": "passed"`, and stdout equal to `RESULT.json` (the script checks
this itself). Run it inside a full checkout of the base: it reads and hashes
`research-note.tex`, `profile_lp.py` and `experiments/matrix-profile.json` at the repository
root, so a copy of this folder alone fails its provenance checks. Standard library only, exact rational arithmetic, no network, no files written,
about one second. It is equally effective under `python3 -O` (no `assert`).

## Which direction is "stronger"

For a tensor character with parameter `t = (p_X+p_Y+p_Z)/3`, the paper's symmetrized profile
`P(a,b)` of polynomial multiplication `C(a,b)` satisfies (paper, (4.5), Lemmas 4.1 and 4.2):

* (S) `P(a,b) = P(b,a) > 0`, (N) `P(1,b) = b`;
* (C) separate discrete concavity: `P(a,b-1) - 2P(a,b) + P(a,b+1) <= 0` for `a >= 1, b >= 2`;
* (T) shifted tripling: `P(a, 3h+a-1) >= 3 P(a,h)` for `a, h >= 1`;
* (E_t) rank envelope: `P(a,b) <= (a+b-1)^(1/t)`.

Its Lemma 5.1 gives `P(a,a) >= a^(4/3)` from (S), (N), (C), (T), hence `t <= 3/4` and
`omega <= 3t <= 9/4`. A *smaller* provable `t` is stronger. A profile satisfying all five
constraints at some `t` shows that these constraints cannot prove anything below `t`.
`research-note.tex` (Theorem "barrier") gives one at `t = 3/4`, namely
`P_*(a,b) = ((3u-1)/2)^(1/3)(v+(u-1)/2)`. A profile admissible at `t > 3/4` cannot exist (Lemma
5.1). So the set of admissible `t` for the listed constraints is exactly `(0, 3/4]`, already
before this note. What was open is the shape of the admissible set, which decides what an
additional constraint would have to do.

## Statements

Write `L_a = ((3a-1)/2) H_a`, so `P_o(a,a) = L_a` and `P_o(a,b) = L_a + H_a (b-a)` for `b >= a`.

**Theorem 1 (least element).** (i) `P_o` satisfies (S), (N), (C), (T) and (E_{3/4}), is
increasing in each coordinate, and `P_o <= P_*` pointwise.
(ii) Let `P` be any real function on pairs of positive integers with `P(1,1) >= 1`, discrete
concavity in each coordinate separately, and shifted tripling in each coordinate,
`P(a,3h+a-1) >= 3P(a,h)` and `P(3h+b-1,b) >= 3P(h,b)`. Then `P >= P_o` pointwise.
In particular every profile satisfying (S), (N), (C), (T) dominates `P_o`.

Symmetry is not needed in (ii); this is what makes Theorem 4 (K1) work.

**Corollary 2 (sharp numbers).** For every `a`, `min P(a,a) = L_a` over the profiles satisfying
(S), (N), (C), (T), with or without (E_t) for any `t <= 3/4`. The sequence
`kappa_a = L_a / a^(4/3)` is strictly increasing, below `(3/2)^(4/3)`, and tends to
`kappa = 3/(2 Gamma(4/3))`. For every `N`,
`(27/8) H_N^3/N <= kappa^3 <= (81/8) H_N^3/(3N-1)`; at `N = 10^4` this gives
`1.679751 <= kappa <= 1.679770` (exact rational comparison in `verify.py`, which also checks
that the unrounded bracket contains an independently computed value of `3/(2 Gamma(4/3))`).

| `a` | `L_a` (exact) | `L_a` | `P_*(a,a) = ((3a-1)/2)^(4/3)` | `a^(4/3)` |
|---|---|---|---|---|
| 1 | 1 | 1.0000 | 1.0000 | 1.0000 |
| 2 | 10/3 | 3.3333 | 3.3930 | 2.5198 |
| 3 | 56/9 | 6.2222 | 6.3496 | 4.3267 |
| 4 | 770/81 | 9.5062 | 9.7085 | 6.3496 |
| 5 | 3185/243 | 13.1070 | 13.3905 | 8.5499 |
| 6 | 12376/729 | 16.9767 | 17.3470 | 10.9027 |
| 7 | 138320/6561 | 21.0822 | 21.5443 | 13.3905 |
| 8 | 499928/19683 | 25.3990 | 25.9576 | 16.0000 |

The repository's exploratory LP (`experiments/matrix-profile.json`, grid `N = 100`) returned
`25.39897...`, `65.85272...`, `114.14111...` at `a = 8, 16, 24`; these are `L_8, L_16, L_24`
to relative error below `10^-12`. Theorem 1 explains the numbers: the restriction of `P_o` to
the grid is feasible for that LP and attains `L_a`, so the finite LP was already tight. `P_o`
is one minimiser; nothing says the LP's minimiser is unique.

**Corollary 3 (scope of the barrier).** For each `t`, the profiles satisfying (S), (N), (C), (T)
and (E_t) exist iff `P_o` satisfies (E_t), iff `t <= 3/4`; when they exist, `P_o` is the least.
For `t = 4/5` the diagonal envelope first fails at `a = 63`, for `t = 7/9` it fails at
`a = 2494` (exact witnesses). Consequently:

* any further constraint `X` that `P_o` satisfies leaves `t = 3/4` admissible: `X` cannot
  improve `9/4` by this route, whatever its form;
* if `X` is **downward closed** (whenever `P` satisfies it, so does every `P' <= P`; pure upper
  bounds `P(a,b) <= U_t(a,b)` such as the envelope), then `X` excludes `t` **iff** `P_o`
  violates it;
* for a **mixed** constraint relating values at different points (all five families below), a
  violation by `P_o` proves nothing by itself. The exact criterion is: the enlarged system
  excludes `t` iff none of its profiles stays inside (E_t); when it has a least element `P'`,
  iff `P'(a,b) > (a+b-1)^(1/t)` at some point. A strict violation at one point at `t = 3/4`
  excludes a whole interval of `t` below `3/4`, so improving `9/4` does **not** require a
  diagonal exponent above `4/3`. Example (found by the sprint's referee):
  `P~_c = c P_o` off the first row and column, with `P~_c(1,b) = b`, satisfies (S), (N), (C),
  (T) for every `c >= 1` and has diagonal exponent `4/3`; with `c = 81/56`, `P~(3,3) = 9`
  exceeds `5^(4/3) = 8.55`, so adding a valid constraint `P(3,3) >= 9`, if one existed, would
  exclude every `t > ln 5/ln 9 = 0.7325`. With K4' in the system, rows and columns 1 and 2 can
  never leave (E_{3/4}) (`P(a,2) <= 2a <= (a+1)^(4/3)`), so the point must have
  `min(a,b) >= 3`; there `P_o` is below the envelope by a factor at least `1.374`, attained at
  `(3,3)` (`9 * 5^(4/3)/56`; exact check on `3 <= a, b <= 120`).

**Theorem 4 (five further valid families hold for `P_o`).** For every tensor character, the
symmetrized profile satisfies the following, and so does `P_o`:

| | inequality | tensor fact | type |
|---|---|---|---|
| K1 | `P(a,b) P(c,d) <= P(a+K(c-1), b+K(d-1))`, `K = a+b-1` | Kronecker substitution `X = x^K`: `C(a,b) ⊗ C(c,d) <= C(a+K(c-1), b+K(d-1))` | mixed, lower bound on the right |
| K2 | `P(sc,sd) <= P(s,s) P(c,d)` | stride `x^i X^j -> x^(i+sj)`: `C(sc,sd) <= C(s,s) ⊗ C(c,d)` | mixed, upper bound on the left |
| K3 | `P(a,mb) <= m P(a,b)` | `C(a,mb) <= C(a,b) ⊗ B_X(m)` | mixed, upper bound on the left |
| K4 | `k P(a,b) >= sum_{i<min(b,k)} P(a, b+k-1-2i)` | `C(a,b) ⊗ B_X(k)` degenerates to `⊕ C(a, b+k-1-2i)` with a shared first leg (powers of the determinant) | mixed, upper bounds on the right |
| K4' | (b = 1, k = 2) `P(a,2) <= 2a` | special case | |
| K5 | `P(a, h_1+...+h_m + (a-1) floor(m/2)) >= sum_i P(a,h_i)` | alternating sectors `C, C^sigma, C, ...` | mixed, lower bound on the left |

K5 with `m = 3` and equal `h` is the paper's tripling; K4 with `k = 2` contains its
concavity. No claim is made that K1 to K5 are independent of (S), (N), (C), (T).

**Corollary 5.** The system (S), (N), (C), (T), K1-K5, (E_{3/4}) is satisfiable, with least
element `P_o`. These five tools, used with the paper's symmetrization, cannot improve
`omega <= 9/4` either.

## Proofs

Throughout, `H_1 = 1` and `H_{u+1} = H_u (3u+1)/(3u)`.

**Theorem 1 (i).** (N): `u = 1` gives `P_o(1,b) = b`. (S) holds by definition. Fix a row `a`.
For `b >= a` the row is affine, `H_a (b + (a-1)/2)`, slope `H_a > 0`. For `1 <= b <= a` it is
`H_b (a + (b-1)/2)`; its increments are `H_b (1 + (2a+b)/(3b))/2 > 0`. Second differences: at
a centre `b >= a+1` they vanish; at the seam `b = a`, using `H_{a-1} = H_a (3a-3)/(3a-2)`, the
second difference is `H_a((3a+1)/2 - (3a-1) + (3a-3)(3a-2)/(2(3a-2))) = 0`; at a centre
`2 <= b <= a-1` it equals `-2 H_b (a-b) / (3b(3b-2)) < 0`. Hence (C). For (T) with `h >= a`,
both sides use the affine branch and `P_o(a,3h+a-1) = 3 P_o(a,h)` exactly. For `h < a`, (T) is
`H_a (2h+a-1) >= H_h (2a+h-1)`. Put `R(a) = H_a(2h+a-1) / (H_h(2a+h-1))`; `R(h) = 1` and
`R(a+1)/R(a) = (3a+1)(2h+a)(2a+h-1) / (3a(2h+a-1)(2a+h+1)) >= 1`, because numerator minus
denominator is `2(a-h)(a-h+1) >= 0`. For `P_o <= P_*` it suffices that `H_u^3 <= (3u-1)/2`:
true at `u = 1`, and the ratio step `(3u+1)^3/(27u^3) <= (3u+2)/(3u-1)` holds because
`27u^3(3u+2) - (3u+1)^3(3u-1) = 6u+1`. The envelope follows as in the note:
`(3u-1)/2 <= a+b-1` and `v+(u-1)/2 <= a+b-1` give `P_o^3 <= (a+b-1)^4`.

**Theorem 1 (ii).** Let `D_a = P(a,a)`, `r_{a,b} = P(a,b+1) - P(a,b)` (row increments) and
`c_{a,b} = P(a+1,b) - P(a,b)` (column increments); by concavity both are nonincreasing in the
moving index. Row tripling at `h = a` gives `P(a,4a-1) >= 3D_a`, so the `3a-1` increments
`r_{a,a}, ..., r_{a,4a-2}` sum to at least `2D_a`, and the largest, `r_{a,a}`, is at least
`rho_a = 2D_a/(3a-1)`. Likewise `c_{b,b} >= rho_b` by column tripling. For `a >= 2`,

```math
D_a - D_{a-1} = r_{a,a-1} + c_{a-1,a-1} \ge r_{a,a} + c_{a-1,a-1} \ge \rho_a + \rho_{a-1}.
```

Substituting `D_a = (3a-1) rho_a / 2` gives `rho_a (3a-3) >= rho_{a-1} (3a-2)`, and
`rho_1 = D_1 >= 1 = H_1`; so `rho_a >= H_a` and `D_a >= L_a`. This is the paper's Lemma 5.1
with the column increment in place of symmetry, kept with its exact constants.
Off the diagonal, fix `a` and put `h_0 = a`, `h_{j+1} = 3h_j + a - 1`. By induction
`P(a,h_j) >= P_o(a,h_j)`: the base is `D_a >= L_a`, and
`P(a,h_{j+1}) >= 3P(a,h_j) >= 3P_o(a,h_j) = P_o(a,h_{j+1})` since tripling is tight for `P_o`
when `h >= a`. On each `[h_j, h_{j+1}]` the row of `P` is concave, so it lies above its chord,
which lies above the chord of `P_o`, which is `P_o` itself (affine there). So `P(a,b) >= P_o(a,b)`
for all `b >= a`. The same argument in column `b` gives `P(a,b) >= L_b + H_b(a-b) = P_o(a,b)`
for `a >= b`.

The admissible set is also closed under pointwise infimum (concavity, a lower-bound tripling,
symmetry and the boundary values all pass to infima), which gives a least element abstractly;
the argument above identifies it.

**Corollary 2.** `P_o` attains the bound of (ii) on the diagonal. Monotonicity of `kappa_a`:
`L_{a+1}/L_a = (3a+1)(3a+2)/(3a(3a-1))`, and `(L_{a+1}/L_a)^3 >= ((a+1)/a)^4` after clearing
denominators reads `(3a+1)^3(3a+2)^3 a - 27(3a-1)^3(a+1)^4 >= 0`; substituting `a = 1 + k`
gives `4544 + 17936k + 27324k^2 + 20007k^3 + 7074k^4 + 972k^5`, all coefficients positive.
`kappa_a < (3/2)^(4/3)` by `H_a^3 <= (3a-1)/2`. The limit: `H_a = Gamma(a+1/3)/(Gamma(4/3)Gamma(a))`
and `Gamma(a+1/3)/Gamma(a) ~ a^(1/3)`.
The bracket needs no inequality on the Gamma function: `H_a^3/a` increases, since
`(3a+1)^3 - 27a^2(a+1) = 9a+1`, and `H_a^3/(a-1/3)` decreases, since
`27a^3(3a+2) - (3a+1)^3(3a-1) = 6a+1`. Both sequences tend to `Gamma(4/3)^(-3)`, so
`(27/8) H_N^3/N <= kappa^3 <= (81/8) H_N^3/(3N-1)` for every `N`; `verify.py` evaluates both
sides exactly at `N = 10^4`. The upper end is very close to `kappa` (relative gap about
`10^-10`), the lower end within `1.2 * 10^-5`.

**Corollary 3.** If `t <= 3/4`, `P_o` satisfies (E_t) because `(a+b-1)^(4/3) <= (a+b-1)^(1/t)`.
If some profile satisfies (E_t), so does `P_o <= P`. If `t > 3/4`, `P_o(a,a) = L_a >= a^(4/3)`
exceeds `(2a-1)^(1/t)` for large `a`. The first two bullets on further constraints are
immediate from `P_o` being least. For the third: (E_t) is a pure upper bound, so a system with
least element `P'` is compatible with (E_t) iff `P'` is; and if `P'(a,b) > (a+b-1)^(4/3)` at one
point, the same strict inequality holds with `1/t` in place of `4/3` for all `t` close to
`3/4`, below it included, by continuity in `t`. For the referee's example: in a row `a >= 2`,
the second difference centred at `b = 2` is `c` times that of `P_o` minus `(c-1)a`, hence
`<= 0`; tripling at `h = 1` reads `c P_o(a,a+2) >= 3a`, true since `P_o(a,a+2) >= 3P_o(a,1)`;
all other second differences and tripling inequalities of rows `a >= 2` are those of `P_o`
multiplied by `c`, and row and column 1 are unchanged.

**Theorem 4, tensor side.** Each `lambda_pi` is a character, hence multiplicative,
restriction-monotone and degeneration-monotone (paper, Lemma 2.3), and restrictions commute
with permuting legs. So a restriction or degeneration between products of `C`'s and `B_X`'s
passes to `P` after taking the product over the six `pi` and the power `1/(6t)`, with
`prod_pi lambda_pi(B_X(m)) = m^(6t)` by the paper's (2.3) and (4.3).

* K1. Write a bivariate product with `deg_x < a, deg_X < c` times `deg_x < b, deg_X < d` and
  substitute `X = x^K`, `K = a+b-1`. On the first two legs the substitution is the coordinate
  projection onto exponents `i_1 + K i_2` (`i_1 < a`, resp. `< b`); on the third leg every
  exponent `M` has a unique form `m_1 + K m_2` with `m_1 < K`, and `i_1 + j_1 <= a+b-2 < K`, so
  the restricted univariate tensor `C(a+K(c-1), b+K(d-1))` maps onto `C(a,b) ⊗ C(c,d)`.
* K2. `x_{i_1,i_2} -> x_{i_1+s i_2}` (`i_1 < s`, `i_2 < c`) and the same on the second leg are
  bijections onto `[0,sc)` and `[0,sd)`; `z_{k_1,k_2} -> z_{k_1+s k_2}` is linear. The image of
  `C(s,s) ⊗ C(c,d)` is exactly `C(sc,sd)`.
* K3. `y_{j,l} -> y_{j+lb}`, `z_{k,l} -> z_{k+lb}` maps `C(a,b) ⊗ B_X(m)` onto `C(a,mb)`.
* K4. `C(a,b) ⊗ B_X(k)` is multiplication `V_{a-1} x (V_{b-1} ⊗ W_{k-1}) -> V_{a+b-2} ⊗ W_{k-1}`
  on bihomogeneous forms in `(u,v)` and `(s,w)`. With `D = uw - vs`, filter bidegree `(e,k-1)`
  by `F_i = D^i (V_{e-i} ⊗ W_{k-1-i})`. Diagonal substitution `(s,w) = (u,v)` of the cofactor
  identifies `F_i/F_{i+1}` with `V_{e+k-1-2i}` (the paper's exact sequence (4.7) in bidegree
  `(p,q)`: kernel `D V_{p-1,q-1}`, dimensions `(p+1)(q+1) - pq = p+q+1`). Multiplication by
  `f` in `(u,v)` preserves every `F_i` and acts on `F_i/F_{i+1}` as multiplication by `f`.
  Choose lifts at each level whose images are monomials, as in the paper; every slice is then
  block-triangular, level `i` of the input reaching output levels `>= i`, with diagonal blocks
  `C(a, b+k-1-2i)`. Weights `-i` on input level `i` (second leg), `+j` on output level `j`
  (third leg), `0` on the first leg keep exactly the diagonal blocks: a degeneration to
  `min(b,k)` blocks sharing the first leg. The shared-leg inequality (paper, Corollary 3.2)
  with weights proportional to the block values, applied to all six `lambda_pi` with the same
  weights, gives K4, exactly as in the paper's proof of Lemma 4.1 (`k = 2`).
* K5. Lay the sectors out in order: a `C`-sector has second-leg interval of length `h` and
  third-leg interval of length `h+a-1`; a `C^sigma`-sector has lengths `h+a-1` and `h`. Starting
  both legs at `0` and alternating `C, C^sigma, C, ...`, the two legs restart together after
  every `C^sigma`-sector, and the second leg ends at `B = sum h_i + (a-1) floor(m/2)`. When `m`
  is even the last `a-1` third-leg coordinates are unused and set to zero. Give weight `0` to
  `C`-sectors and `+1` / `-1` (second / third leg) to `C^sigma`-sectors. A term `y -> z = x+y`
  with `0 <= x < a` never goes from a `C`-sector to the next `C^sigma`-sector (`z - y >= a`), nor
  backwards from a `C`-sector into the previous `C^sigma`-sector (`z < y`), nor across a whole
  sector (`z - y >= a`); from a `C^sigma`-sector into a neighbouring `C`-sector it has weight
  `+1`. So the weight-zero part is the `m` matched sectors, each a full `C(a,h_i)` or
  `C(a,h_i)^sigma` (paper, proof of Lemma 4.2), sharing the first leg. Corollary 3.2 and the
  symmetrization `prod_pi lambda_pi(C^sigma) = prod_pi lambda_pi(C)` give K5 after optimizing
  the weights.

**Theorem 4, `P_o` side.**

* K1. Fix `a, b`, `K = a+b-1` and `Q(c,d) = P_o(a+K(c-1), b+K(d-1)) / P_o(a,b)`. Then
  `Q(1,1) = 1`; `Q` is concave in each coordinate (restriction of a concave sequence to an
  arithmetic progression); and `Q` satisfies tripling in each coordinate: with
  `H' = b+K(h-1)` and `e = a+K(c-1)`, `b+K(3h+c-2) - (3H'+e-1) = a-1 >= 0`, so monotonicity and
  tripling of `P_o` give `Q(c,3h+c-1) >= 3Q(c,h)`; the first coordinate is the same with margin
  `b-1`. Theorem 1 (ii) gives `Q >= P_o`, which is K1.
* K2. Take `c <= d`. The ratio `P_o(sc,sd) / (P_o(s,s)P_o(c,d))` equals
  `H_{sc} (s + ((s-1)/2)/(d + (c-1)/2)) / (L_s H_c)`, decreasing in `d`; at `d = c` it is
  `L_{sc}/(L_s L_c)`. If `s = 1` or `c = 1` this is `1`. Otherwise
  `kappa_{sc} < (3/2)^(4/3) <= kappa_2^2 <= kappa_s kappa_c`; the middle inequality is
  `(3/2)^4 <= L_2^6/2^8`, i.e. `81/16 <= 10^6/186624`.
* K3, K4. Extend row `a` by `g(0) = 2P_o(a,1) - P_o(a,2) = 2a - (4/3)(a+1/2) >= 0` (equality at
  `a = 1`); the extended row is concave with `g(0) >= 0`, so `g(x)/x` is nonincreasing, which
  is K3. For K4 with `b >= k`, the summed points are symmetric about `b` and concavity bounds
  each symmetric pair by `2P(a,b)`. For `b < k` they are `b` points symmetric about `k`, so the
  sum is at most `b P(a,k) <= k P(a,b)` by the same ratio monotonicity.
* K5. The row of `P_o` is concave and coincides with `ell(h) = H_a(h + (a-1)/2)` on
  `h >= a-1` (the seam increment is `H_a`), so `P_o(a,h) <= ell(h)` for all `h`. For `m >= 2`,
  `B >= a+1`, so `P_o(a,B) = ell(B) = H_a(sum h_i + (a-1)(floor(m/2) + 1/2)) >= sum ell(h_i)
  >= sum P_o(a,h_i)`; `m = 1` is trivial.

## What `verify.py` checks

All in exact rationals. Labels match `RESULT.json`.

* **A, grid evidence.** (S), (N), (C), (T) for `P_o` on rows `a <= 60`, columns `b <= 240`;
  (E_{3/4}) and monotonicity on `a, b <= 120` and `<= 60`; `H_u^3 <= (3u-1)/2` for `u <= 400`.
* **B, certificates.** Each identity used above is a polynomial of bounded degree after
  clearing denominators, and is checked on a product grid larger than its degree (a
  polynomial vanishing there is zero): the interior and seam second differences, the tripling
  ratio step, the cube step `6u+1`, the coefficients of the `kappa` step, the comparison
  `81/16 <= 10^6/186624`, the growth recursion `L_a = L_{a-1} + H_{a-1} + H_a` (`a <= 400`),
  tightness of tripling for `h >= a`, the lower-sequence step `9a+1`, the two integer
  comparisons excluding PR #11's family, and `(a+1)^4 - 8a^3 = (a^2-2a)^2 + 2a^2 + 4a + 1`.
* **C, least-element evidence.** `L_1..L_10` exactly; the repository LP minima against `L_8,
  L_16, L_24`; lowering any single symmetric pair of values of `P_o` by `10^-6` breaks a listed
  constraint at all 78 points of `a <= b <= 12`. This is consistent with Theorem 1 and does not
  prove it; the proof is above.
* **D, grid evidence.** K1 (`a,b,c,d <= 7`, 2,401 cases), K2 (`s,c,d <= 12`, 1,728), K3
  (9,000), K4 (7,600), K5 (39,050 chains, `m <= 5`): no violation, with the number of
  equalities.
* **E.** The envelope witnesses at `t = 4/5` (first failure `a = 63`, all `a < 63` checked) and
  `t = 7/9` (`a = 2494`); the `kappa` bracket at `N = 10^4`, which must contain, unrounded, the
  value of `3/(2 Gamma(4/3))` computed independently with mpmath to 48 decimals (the upper end
  is within about `2 * 10^-10` of `kappa`, so the check needs ten correct digits; an error of
  `10^-9` in the reference is detected); the referee's
  example `P~_{81/56}` (listed constraints on rows `<= 40`, columns `<= 200`, and
  `P~(3,3) = 9 > 5^(4/3)`); the envelope gap at `(3,3)` is the smallest on `3 <= a, b <= 120`.
* **F, negative controls, each required to fail.** Lowered `H_2`; growth factor
  `1 + 1/(3m+1)`; offset `1/2 +- 1/100`; one diagonal value lowered by 1%; a corrupted
  identity; the K1 and K2 checkers on `2P_o` and `P_o/2`; two wrong brackets for `kappa`
  (Wendel's upper factor with exponent 1 instead of 2, and the upper sequence at `3N` instead
  of `3N-1`) must miss the reference value, which shows that the reference check catches
  them. Also `P_o(a,a)^3 <= (2a-1)^4` up to `a = 400` as a positive control for the envelope
  at `3/4`.
* **Provenance.** sha256 of the three pinned base files and of every package file
  (`MANIFEST.json`), and equality of the printed report with `RESULT.json`.

Grid checks are evidence for the theorems, not their proofs; the certificates in B and the
witnesses in E are complete for what they state.

## Lean

`lean/` checks the profile side in Lean 4.21 with Mathlib: Theorem 1 (i) and (ii), Corollary 2
including `kappa_a -> 3/(2 Gamma(4/3))` (through Euler's limit formula in Mathlib) and the
bracket for every `N`, the `t = 4/5` witnesses of Corollary 3, and the `P_o` side of K1 to K5.
No `sorry` and no axiom beyond Lean's three standard ones, on every declaration. The tensor
side of Theorem 4 is not formalized. `lean/README.md` maps each statement to its Lean name.

## Relation to earlier work

* `research-note.tex`, Theorem "barrier": `P_*` shows that the listed constraints admit
  `t = 3/4`. `P_o` has the same offset `(u-1)/2` with the multiplier `H_u` in place of
  `((3u-1)/2)^(1/3)`; `P_o < P_*` off the first row and column.
* PR #11 (`bbMisk`, open, head `9c1f70f3`) characterizes the family
  `F(u)^s (v + lambda(u-1))`, `F(x) = (1+lambda)x - lambda`, and finds the minimal diagonal
  exponent `4/3` at `P_*`; it makes no claim outside that family. `P_o` is in no member of it,
  for any `lambda` and `s`: on row `u = 2` both profiles are affine in `v`, so equality forces
  `lambda = 1/2` and `(5/2)^s = 4/3`; on row `u = 3` it then forces `4^s = 14/9`. But
  `(5/2)^(6/19) > 4/3` gives `s < 6/19`, and `4^(6/19) < 14/9` then gives `4^s < 14/9`
  (integer comparisons `5^6 3^19 > 2^6 4^19` and `4^6 9^19 < 14^19`). The exponent `4/3` is minimal
  over all admissible profiles by the paper's Lemma 5.1; Theorem 1 adds the least element and
  the sharp constant. No overlap with PR #11's statements.
* `experiments/matrix-profile.json` and `profile_lp.py`: the floating LP minima are `L_a`;
  that file remains exploratory, and nothing here depends on it.

## Limits

`P_o` is an abstract profile; no tensor character is constructed and no claim about `omega`
is made beyond the scope statement of Corollary 3. Theorem 4 covers five named families; other
valid constraints (for example laser-method degenerations into fully independent blocks,
whose symmetrized form carries a factor `M^(1/t)`) are not examined here. Human mathematical
review and literature priority are not established; formal verification covers the profile side
only (`lean/`).
