# A rank-split cover of rich events: every coefficient below 1/15, explicit 1/16

This is a conditional refinement of the rich-event estimate in
`sharpened-region-proof.md`. It keeps that note's outer coloring, keys,
affine-signature count, and digit product unchanged, and replaces only the
union bound over rich progressions. It proposes

```math
W_r(k)>k^{(1/16)k\lfloor\log_2 r\rfloor}
```

for sufficiently large k, with the threshold independent of r, and admits
every fixed c below 1/15. Compared with the source's coefficient 1/100000
the ratio is exactly 6250; compared with this repository's previous explicit
choice 1/25 it is 25/16. The endpoint 1/15 is the supremum of the region, not
a claimed value. No explicit finite threshold is obtained.

## Credit and dependencies

The repeated-key structure used below, and the idea of covering rich events
by certificates whose entropy is about `q^D` rather than `q^{2D}`, are due to
the unmerged upstream proposal
[rohanarun/van-der-waerden-refinement#4](https://github.com/rohanarun/van-der-waerden-refinement/pull/4),
pinned at
[`4b4e80e`](https://github.com/rohanarun/van-der-waerden-refinement/blob/4b4e80ea5e0ffec956577004905f22659af0bff5/repeated-key-certificate-proof.md)
(author Artus Krohn-Grimberghe, initial argument attributed there to GPT-6
Pro). That note proves the sufficient condition `c < gamma*b/3`, hence
every `c < 1/18`, with the explicit choice 1/19. It is not merged into this
repository; the facts used from its Sections 2 to 4 are restated in Section 1
with short proofs.
The original construction is OpenAI's, at the pinned source revision linked
in the README; the two-point norm-band lemma, shortened dilation, and sharper
balance are from `research-note.tex` and `sharpened-region-proof.md`.

What is new here is a split of rich events by the **carry rank** of their
collision classes (Section 2), which gives two new counts:

* a cover of every flipped key in the collision classes, singles included,
  with entropy `q^{2 rho}` and no start point (Lemma A), and
* a count of the progressions themselves with entropy `q^{2D - rho}`
  (Lemma C).

Together with the anchored certificate (Lemma B, a mild extension of #4)
they give the sufficient condition `5c < 2 gamma b`.

## Setting and notation

Write, as in `sharpened-region-proof.md`, `D = ceil(k^a)`, `p = k^{-b}`,
`H = k^{-2}`, `N = q^D`, where `q` is the least power of the source prime
`P` in `(k, 2k^2]` with `q >= k^{ck/D}`, so `ck log k <= D log q <=
ck log k + D log(2k^2)`. Keys are the source's literal keys
`kappa(n) = (box of y(n), floor(f(n)))` with `f(n) = q^2 |Y(n)|^2`,
`Y(n) = ytilde(n)` the centered representative. All logarithms are natural.

Fix the outer coloring `c_0` and a target color. For a progression
`n_j = n_0 + j d` (`0 <= j < k`, `d != 0`) the event that it is
monochromatic in the target color prescribes `E_kappa = 1` on the set `F`
of keys at **flipped** positions (outer color opposite to the target) and
`E_kappa = 0` at the others. Events with a key prescribed both ways are
empty and are discarded. By the two-point lemma each key occurs at most
twice, so for a consistent event

```math
|P_1| = 2r + s,\qquad |F| = r + s,
```

where `P_1` is the set of flipped positions, `r` the number of flipped keys
occurring twice, and `s` the number occurring once. A progression is
`gamma`-rich when each outer color occurs at least `gamma k` times; then
`|P_1| >= gamma k` for either target.

## 1. Facts about repeated keys (from #4, Sections 2 to 4)

Suppose some second-coordinate box repeats along the progression. Let `h`
be the gcd of all box-return gaps.

**(R1) Common return.** There are `t in {0, ..., h-1}^D` and a real vector
`B` with `y(d) = t/h + B (mod Z^D)`, `|B_i| <= 2H/h`, and `h` is itself a
box-return gap. Every box (hence every key) occurs only in one residue class
mod `h`. With `beta = hB` one has `beta = Y(hd)` and `q|beta| >= 1`.

*Proof.* For a return gap `g`, the difference `v_g` of the two centered
representatives satisfies `|v_{g,i}| <= 2H` and `v_g = g y(d) mod Z^D`.
For two gaps, `g' v_g - g v_{g'}` is an integer vector of size
`< 2H(g+g') < 4kH < 1`, hence zero, so `v_g = gB` for one `B`. Bezout gives
`h(y(d) - B) in Z^D`. The point `Y_j + hB` is a convex combination of two
points of a half-open box, so `h` is a return gap. Finally `hd != 0` since
`h < P`, and the source's separation lemma gives `q|Y(hd)| >= 1`.

**(R2) Collision classes are affine.** Call a residue class `a mod h`
(`0 <= a < h`) a *collision class* if it contains a repeated key. Its
positions `a + s h`, `0 <= s < K_a <= ceil(k/h)`, satisfy

```math
Y_{a+sh}=Y_a+s\beta .
```

*Proof.* The class moves by at most `k|B_i| <= 2/k < 1/2` in each
coordinate. If the representatives left the real segment, some coordinate
with `B_i != 0` would meet a cut, every sample of the class would satisfy
`rho(y_i) <= k|B_i|`, and the adaptive-mesh width bound together with
`|hB_i| >= q^{-D} >= alpha` would give intervals of width
`<= 2H(k+h)|B_i| < h|B_i|`, too narrow to contain two distinct class
samples. This contradicts the repeated box.

**(R3) Carries.** Write `A = Y(n_0)` and define integer vectors `m_j` by

```math
Y_j=A+\frac{j}{h}(t+\beta)-m_j .
```

The word of boxes together with the carries `m_j` (the *augmented word*)
takes at most `T_aug = [9(6k^2J+1)^2]^D` values over all progressions,
where `J = |V| = O(k^3 log k)`; so `log T_aug = O(D log k)`. Moreover
`m_{j,i} in [-1, h-1]` for class starts `0 <= j < h`, so
`|Delta m_{a,i}| <= h` below.

**(R4) The vertex constraint.** Let `a` be a collision class and let
`a + s_1 h`, `a + s_2 h` (`s_1 < s_2`) carry one repeated key. Put
`w = |beta|^2`, `W = q^2 w`, and `sigma_a = s_1 + s_2`. Equal integer bands
give `|f_{a+s_2h} - f_{a+s_1h}| < 1`, and by (R2) this difference equals
`q^2 (s_2-s_1)(2<Y_a,beta> + sigma_a w)`. Hence

```math
\zeta_a:=q^2\bigl(2\langle Y_a,\beta\rangle+\sigma_a w\bigr),\qquad
|\zeta_a|<\frac1{s_2-s_1}\le1 .
\tag{1}
```

For each collision class, fix `sigma_a` from its innermost pair. Then for
every position of the class

```math
f_{a+sh}=q^2|Y_a|^2+s(s-\sigma_a)W+s\,\zeta_a .
\tag{2}
```

**(R5) #4's anchored identity.** With `C_a = a t/h - m_a` and
`theta_a = q^2|A + C_a|^2`, every position `j` of a collision class `a`
whose innermost pair sits at `j_1 < j_2` satisfies

```math
f_j=\theta_a+j(j-j_1-j_2)\,u+j\,\eta_a,\qquad
u=q^2|B|^2,\quad |\eta_a|<\frac{1}{j_2-j_1}\le\frac1h .
\tag{3}
```

This is #4's identity (16), applied also to positions that are not in pairs:
`f_j = theta_a + 2 j q^2 <A + C_a, B> + j^2 u`, and the pair fixes
`2 q^2 <A + C_a, B> = -(j_1 + j_2) u + eta_a`.

## 2. The carry rank of a progression

For a progression with at least one repeated key, let `Sigma` be its set of
collision classes, `a_0 = min Sigma`, and

```math
\Delta m_a=m_a-m_{a_0}\in\mathbb Z^D\quad(a\in\Sigma),\qquad
\rho=\operatorname{rank}_{\mathbb Q}\{\Delta m_a:a\in\Sigma\}\in\{0,\dots,D\}.
```

For a progression without repeated keys put `Sigma` empty and `rho = 0`.
For a fixed target, split the flipped keys into the `r + s_Sigma` keys at
flipped positions **inside** collision classes (all `r` repeated flipped keys
are there, together with `s_Sigma` singles) and the `s_out` singles outside.
So `|F| = r + s_Sigma + s_out` and `|P_1| = 2r + s_Sigma + s_out`.

All three counts below are encodings: a map from the counted objects to codes
that is injective, followed by a count of codes. Codes may describe
unrealizable data, which only enlarges the bound. The *discrete data* of a
progression are `h`, `t`, the augmented word, and the set of positions of
repeated keys. From the last two, `Sigma`, `a_0`, the nested pairs of #4, each
`sigma_a`, the vectors `Delta m_a`, and `rho` are all determined. The
discrete data take at most `k^{D+1} * T_aug * 2^k = exp(O(k + D log k))`
values. In every bound below, `O(.)` constants are absolute and uniform in
`rho`.

## 3. Three counts

**Lemma A (projection certificate).** Fix the discrete data, with rank
`rho`. The number of possible literal key sets `{kappa(n_j) : j in S}`, over
all progressions with these data and all sets `S` of positions in collision
classes, is at most

```math
\exp\bigl(2\rho\log q+O(\log q+D\log k+k)\bigr).
```

*Proof.* Choose, by a fixed rule, classes `a_1, ..., a_rho` in `Sigma` whose
vectors `v_l = Delta m_{a_l}` form a basis of the span of the `Delta m_a`,
and write `Delta m_a = sum_l g_{al} v_l` with rational `g_{al}`. Put
`c_a = (a - a_0)/h`, so that by (R3)
`Y_a = Y_{a_0} + c_a (t + beta) - Delta m_a`. Expanding `q^2|Y_a|^2` and
eliminating the cross terms `<Y_{a_0}, beta>` and `<Delta m_a, beta>` with (1)
at `a` alone (`zeta_{a_0}` cancels) gives the exact identity

```math
q^2|Y_a|^2=\Lambda_a(\Theta)+c_a\zeta_a,
```

```math
\Lambda_a(\Theta)=q^2U_1+2c_aq^2U_2-(c_a^2+c_a\sigma_a)W
-2q^2\sum_l g_{al}P_l+q^2\bigl(c_a^2|t|^2+|\Delta m_a|^2-2c_a\langle t,\Delta m_a\rangle\bigr),
```

with `U_1 = |Y_{a_0}|^2`, `U_2 = <Y_{a_0}, t>`, `P_l = <Y_{a_0}, v_l>`, and
the real parameter vector `Theta = (q^2 U_1, q^2 U_2, W, q^2 P_1, ..., q^2
P_rho)` of dimension `e = 3 + rho`. (`audit_math.py` checks this identity
and (2) symbolically.) By (2), every position `j = a + sh` of a collision
class has

```math
f_j=\Lambda_j(\Theta)+(c_a+s)\,\zeta_a,\qquad
\Lambda_j(\Theta)=\Lambda_a(\Theta)+s(s-\sigma_a)W,
```

where `Lambda_j` is affine in `Theta` with coefficients fixed by the discrete
data, `0 <= c_a + s <= K := ceil(k/h)`, and `zeta_a in (-1, 1)`. The start
point `n_0` does not appear.

Boxes are fixed by the augmented word, so we count band words in three
steps.

1. Since `0 <= f_j <= Dq^2/4`, the integer `n_j = floor(Lambda_j(Theta))`
   lies in `[-K-1, Dq^2/4 + K]`. The signs of the at most
   `s_1 = k(Dq^2 + 4K + 6)` affine functions `Lambda_j(Theta) - n` fix all
   `n_j`. By the arrangement lemma of the source (including equality signs,
   on any subset of parameter space) there are at most
   `(e+1)^2 (s_1+1)^e` outcomes.
2. Inside one such cell, `floor(f_j) = n_j + #{delta : ...}` is determined
   by the position of `zeta_a` relative to the points
   `(n_j + delta - Lambda_j(Theta))/(c_a + s)` with `|delta| <= K + 2`
   (positions with `c_a + s = 0` are already fixed). Their order within
   each class, and their positions relative to `+-1`, are fixed by the signs
   of at most `s_2 = 2k^2(2K+5)^2` affine functions of `Theta` (positive
   denominators cleared). This refines each cell into at most
   `(e+1)^2 (s_2+1)^e` parts.
3. Inside one part, the band word of class `a` is fixed by the position of
   `zeta_a` among at most `K_a(2K+5)` ordered points: at most
   `2K_a(2K+5) + 1` choices, chosen independently per class.

Multiplying, with `log s_1 = 2 log q + O(log k)`, `log s_2 = O(log k)`, and
`sum_a log(5(K+2)^2) <= h * O(log(k/h + 2)) = O(k)`, gives the bound. Adding
the `2^k` choices of `S` changes nothing.

**Lemma B (anchored certificate).** Under the same hypotheses, the number of
such key sets is also at most

```math
\exp\bigl(D\log q+O(\log q+D\log k+k)\bigr).
```

*Proof.* Encode also `n_0` (`q^D` choices). Then `A` and every
`theta_a = q^2|A + C_a|^2` are known, and (3) writes each band in a collision
class as `theta_a + j(j - j_1 - j_2) u + j eta_a` with one global real `u`
and one real `eta_a` per class, `|j eta_a| < k/h <= K`. The same three steps
with a one-dimensional `Theta = u` give `exp(2 log q + O(log k))` cells for
`u`, `poly(k)` refinements, and `prod_a (2K_a(2K+5)+1) = exp(O(k))`. For the
repeated keys alone this is #4's certificate count; (3) extends it to the
singles of the collision classes.

**Lemma C (rank count).** The number of progressions `(n_0, d)` with at least
one repeated key and rank `rho` is at most

```math
\exp\bigl((2D-\rho)\log q+O(\log q+D\log k+k)\bigr).
```

*Proof.* Let `b_i = q^i beta_i`, an integer with `|b_i| <= 2Hq^i`. Since
`y_i = q y_{i+1} (mod 1)`, `b_{i+1} = b_i (mod q^i)`; put `e_0 = b_1` and
`e_i = (b_{i+1} - b_i)/q^i`. Then

```math
\beta_i=\sum_{l<i}e_l\,q^{\,l-i},\qquad |e_l|\le 2Hq+2H,
```

and `e = (e_0, ..., e_{D-1})` determines `beta_D`, hence `hd`, hence `d`
(as `h < P`). There are at most `(4Hq + 4H + 1)^D <= q^D` such vectors.

Subtracting (1) at `a_0` from (1) at `a` gives the exact identity

```math
\langle\Delta m_a,\beta\rangle
=c_a(T+w)+\frac{\sigma_a-\sigma_{a_0}}2\,w+\frac{\zeta_{a_0}-\zeta_a}{2q^2},
\qquad T=\langle t,\beta\rangle .
\tag{4}
```

Encode `n_0`, the discrete data, `floor(q^2 T)` (`|T| < 2D/k`) and
`floor((k+1) q^2 w)` (`w <= 4DH^2`): `q^D exp(O(log q + D log k + k))`
choices. These fix a number `X_a` with
`|X_a - q^2 <Delta m_a, beta>| < 3`, because `|c_a| < 1` and
`|sigma_a - sigma_{a_0}|/2 < K <= k`, so each cell contributes less than 1
and the `zeta` term less than 1. Now

```math
q^2\langle\Delta m_a,\beta\rangle=qN_1^{(a)}+N_2^{(a)}+R^{(a)},\qquad
N_1^{(a)}=\sum_i\Delta m_{a,i}\,e_{i-1},\quad
N_2^{(a)}=\sum_i\Delta m_{a,i}\,e_{i-2},
```

with `|Delta m_{a,i}| <= h <= k` by (R3), so `|N_2| <= 4D(k+2)q/k^2 < q/8`
and `|R| <= 5D(k+1)H < 1` for large k. Hence `N_1^{(a)}` is the integer
nearest `X_a/q`, so it is determined. The integer forms
`e -> N_1^{(a)}` have coefficient matrix `(Delta m_{a,l+1})_{a,l}`, of rank
exactly `rho`. Fix by a rule `rho` rows and a set `L` of `rho` columns with
a nonsingular minor. Given `e` off `L`, the values `N_1^{(a)}` on those rows
determine `e_L` uniquely. So encoding `e` off `L` costs at most
`(4Hq + 4H + 1)^{D - rho} <= q^{D - rho}`, and the map to codes is injective.

## 4. The rich-event estimate

**Theorem.** Assume the sharpened outer input of `sharpened-region-proof.md`:
the frozen coloring `c_0` makes every nonzero-step cyclic progression
`gamma`-rich or affine. If

```math
5c<2\gamma b,
```

then the probability `R_k` that some `gamma`-rich progression is
monochromatic tends to zero, uniformly over the allowed source primes.

*Proof.* For `rho in {0, ..., D}` put

```math
\kappa_\rho=\frac{\min(2\rho,D)}{D},\qquad
\nu_\rho=\frac{2D-\rho}{D},\qquad
\kappa_\rho+\nu_\rho=
\begin{cases}2+\rho/D,&\rho\le D/2,\\ 3-\rho/D,&\rho\ge D/2,\end{cases}
\quad\le\frac52 ,
```

with equality only at `rho = D/2`. Let `mu = (gamma b - 5c/2)/2 > 0` and
`theta_rho = (kappa_rho c + gamma b - nu_rho c)/(2b)`, so that

```math
b\theta_\rho-\kappa_\rho c=b(\gamma-\theta_\rho)-\nu_\rho c
=\frac{\gamma b-(\kappa_\rho+\nu_\rho)c}{2}\ge\mu .
```

Since `2c < 5c/2 < gamma b`, one has `0 < theta_rho < gamma`. Fix a target
color and a progression of rank `rho` with a consistent event.

* If `r + s_Sigma >= theta_rho k`, select by a fixed rule positions in
  collision classes that carry exactly `R = ceil(theta_rho k)` distinct
  flipped keys (possible since `r + s_Sigma` is an integer `>= theta_rho k`). The event lies in `{E_kappa = 1 for those R keys}`, which
  has probability `p^R`. By Lemmas A and B, and the count of discrete data,
  these sets number at most
  `exp(min(2 rho, D) log q + o(k log k)) = exp(kappa_rho c k log k + o(k log k))`.
  Their total probability is at most
  `exp(-(b theta_rho - kappa_rho c) k log k + o(k log k))`.
* Otherwise `r < theta_rho k`, so
  `|F| = |P_1| - r > (gamma - theta_rho) k`. By Lemma C (or the trivial
  `N^2 = q^{2D}` when there is no repeated key), these progressions
  number at most `exp(nu_rho c k log k + o(k log k))`. Their total
  probability is at most
  `exp(-(b(gamma - theta_rho) - nu_rho c) k log k + o(k log k))`.

Both terms are at most `exp(-mu k log k + o(k log k))`, with `o(.)` uniform
in `rho`. Summing over the `D + 1` ranks and the two targets gives
`R_k = o(1)`. Different full events that share a certificate are covered
by one event, never identified. No independence between events is used.

The affine estimate `A_k = o(1)` (needing `b < a` and `2a + b < 1`), the
outer dichotomy, and the digit product are unchanged from
`sharpened-region-proof.md`. Hence `R_k + A_k < 1` eventually, and

```math
W_r(k)>k^{ck\lfloor\log_2r\rfloor}
```

for all sufficiently large k and every integer `r >= 2`, with a threshold
independent of r.

## 5. The sufficient region and its supremum

```math
a,b,c>0,\quad 2a<m<1,\quad b<a,\quad 2a<1-b,
```

```math
0<\epsilon<\tfrac12,\quad 0<\epsilon_{\rm reg}\le\tfrac12,\quad 0<\delta,\quad
\gamma<(\tfrac12-\epsilon)(1-\epsilon_{\rm reg})(1-\delta),\quad 5c<2\gamma b .
```

Only the last inequality differs from `sharpened-region-proof.md`, where it
read `2c < gamma b/2` (that is, `c < gamma b/4`), and from #4, where it reads
`c < gamma b/3`. Since `b < 1/3` and `gamma < 1/2`,
`c < 2 gamma b/5 < 1/15`. Every fixed `c < 1/15` is admitted by letting
`eps, eps_reg, delta -> 0`, `b -> 1/3` from below, `a` slightly above `b`,
and `m in (2a, 1)`. The endpoint 1/15 is not asserted; `audit_math.py`
rejects it.

The worst case is carry rank `rho = D/2`. There the projection certificate
and the anchored certificate both cost `q^D`, and Lemma C saves `q^{D/2}`.

## 6. Explicit choice

Keep every exponent and balance constant of the 1/25 choice and change only
the coefficient:

```math
a=\tfrac{333}{1000},\quad m=\tfrac45,\quad b=\tfrac{331}{1000},\quad
\delta=\epsilon=\epsilon_{\rm reg}=\tfrac1{200},\quad
\gamma=\tfrac{97}{200},\quad c=\tfrac1{16}.
```

| Inequality | Positive margin |
|---|---:|
| m > 2a | 67/500 |
| m < 1 | 1/5 |
| b < a | 1/500 |
| 2a < 1 − b | 3/1000 |
| gamma < (1/2−eps)(1−eps_reg)(1−delta) | 40499/8000000 |
| 5c < 2 gamma b, as 2 gamma b/5 − c | 857/500000 |

The last entry is

```math
\frac25\cdot\frac{97}{200}\cdot\frac{331}{1000}-\frac1{16}
=\frac{32107}{500000}-\frac{31250}{500000}=\frac{857}{500000}>0 ,
```

and `mu = 857/400000`. For comparison, the same parameters give
`gamma b/3 - 1/16 = -5393/600000 < 0`, so 1/16 lies outside #4's region.
Indeed 1/16 exceeds that region's supremum 1/18.

`parameters.json` stores this choice under `rank_certificate_proposals`.
`audit_math.py` checks:

* every margin, in exact fractions;
* the maximum `5/2` of `kappa + nu` at its breakpoints;
* the two group margins on a grid of ranks;
* the identities (2)–(4) and that of Lemma A, symbolically;
* the digit expansion of Lemma C on exact instances.

It also rejects five boundary controls: `b = a`, `b = 1 - 2a`,
`5c = 2 gamma b`, gamma at the balance bound, and `c = 1/15`.

## 7. What is and is not claimed

The new ingredients are Lemma A (the start-free projection certificate) and
Lemma C (the rank count of progressions), together with the rank split of
Section 4. Lemma B extends #4's certificate to singles in collision classes.
The repeated-key facts of Section 1 are #4's, restated with proofs. The
construction, keys, outer coloring, affine count, and digit product are
unchanged.

The result remains conditional on:

* the imported source lemmas;
* the sharpened outer input;
* the two-point norm-band lemma.

None of this has been independently reviewed. Passing the scripts
establishes the inequalities and identities, not the transfer as a theorem.
No finite coloring, finite van der Waerden record, or runtime improvement
follows. The threshold is not explicit and may be very large.
