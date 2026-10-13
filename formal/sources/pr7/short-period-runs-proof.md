# Short-period runs: every coefficient below 1/8, explicit 1/9

This removes the inequality `2a < 1 - b` from the affine estimate. Together
with the rich condition `2c < γb` of `digit-rank-proof.md`, it proposes

```math
W_r(k)>k^{(1/9)k\lfloor\log_2 r\rfloor}
```

for sufficiently large k, with the threshold independent of r. It also
admits every fixed c below 1/8. Compared with the source's 1/100000 the ratio
is 100000/9 (about 11111); compared with the previous explicit choice 2/25 it
is 25/18. The endpoint 1/8 is the supremum of the region, not a claimed
value. No explicit finite threshold is obtained.

## Credit and dependencies

The rich-event estimate is that of `digit-rank-proof.md` (built on
`rank-certificate-proof.md` and on the repeated-key structure of the
unmerged upstream proposal
[rohanarun/van-der-waerden-refinement#4](https://github.com/rohanarun/van-der-waerden-refinement/pull/4)).
The outer coloring, the dichotomy, keys, and digit product are those of
`sharpened-region-proof.md` and the pinned OpenAI source, with one extra
family of local-lemma events added below. The upstream barrier proposal
[rohanarun/van-der-waerden-refinement#3](https://github.com/rohanarun/van-der-waerden-refinement/pull/3)
lists the `k^{2a}` label entropy as a rigid feature of this template. The
argument below keeps the label entropy, but no longer pays for it in the
affine estimate.

## Where `2a < 1 - b` came from

The source bounds the number of affine signatures `(c_0(n_j), κ(n_j))_j`
by `T_glob (k(Dq^2+2))^3`, where `T_glob` counts full label words. The key
word is cheap: its boxes cost `exp(O(D log k))` and its bands `q^6`. The
expensive part is the outer color word, which is paid for through the label
word: `log T_glob = O(k^{2a} log^3 k)`. The affine estimate needs the whole
count to be `exp(o(pk))`, hence `2a < 1 - b`.

The color word is only needed for progressions that are **not**
`γ`-rich, since rich ones are covered by the rich-event estimate. Those
have a rigid shape.

## The shape of a non-rich progression

Use the parameters of `sharpened-region-proof.md`: `D = ceil(k^a)`,
`M = ceil(k^m)` (here `m` is the exponent of `M`, not the source's mesh
count), `h_0 = D ceil(log k)^2`, the dilation `λ`, and the meshes `U`
(width `H_x = H/λ`) and `V`. By the sharpened dichotomy, a nonzero-step
progression that is not `γ`-rich has a heavy label (full multiplicity
`> k/M`); take the one of smallest first occurrence, as in that note. Its
closest return `h` satisfies `h <= h_0`, its y-representatives are
affine, and by the source's drift and path lemmas (Section 5, "Closest
return and drift" and "Rational path and separated residues")

```math
x(n_j)=x(n_0)+\frac jh(t+u),\qquad \tilde y(n_j)=A+jw\qquad(0\le j<k),
```

with `1 <= h <= h_0`, `t in {0, ..., h-1}^D`, `|u_i| <= 2M H_x/k`, and
`k|w_i| <= 4MH/h < 1/2` (the source's short-period bound; in particular
`|w_i| < 1/(k-1)`). Call a label word of this form, for any real
parameters in these ranges, a **short-period word**. The path `A + jw` is
not required to stay in the representative cube; dropping that condition
only enlarges the family.

**Lemma 1 (runs).** Let `P` be an actual progression that is not `γ`-rich,
with `h` the closest return of its heavy label. Then the occurrences of
any one full label in `P` form a single run: one residue class mod `h`,
consecutive within that class. (This is a statement about actual
progressions. It can fail for an abstract short-period word, for example
with `t = 0`, and it is used below only for actual progressions.)

*Proof.* Indices incongruent mod `h` have distinct labels, by the source's
path lemma, which also proves `gcd(t_1, ..., t_D, h) = 1`. In class `r`, `ytilde(n_{r+sh}) = A + (r+sh) w` is a real
affine path inside the representative cube. On the circle,
`x(n_{r+sh}) = x(n_r) + s u` moves monotonically, by at most
`k|u_i|/h <= 2M H_x < 1/2` in total. A box is a product of half-open
intervals, so a path that is monotone in every coordinate enters it at most
once.

**Lemma 2 (few short-period words through a label).** For every full label
`β`, the number of short-period words containing `β` is at most
`exp(O(D log k))`.

*Proof.* Anchor at a position `j_0` where `β` occurs (at most `k`
choices). Choose `h <= h_0` and `t` (`h_0^{D+1}` choices). In each
x-coordinate the word is fixed by the anchor offset inside the `U`-interval
of `β` and by `u_i`. At each position the point ranges over a known arc of
length at most `H_x(1 + 4M/h)` (anchor offset plus drift in either
direction), so it meets at most `4M/h + 2` `U`-endpoints. That is at most
`k(4M+2)` lines in two parameters, so `O(k^2 M^2)` outcomes by the
arrangement lemma. In each y-coordinate the
anchor offset in the `V`-interval of `β` and `w_i` give at most `k(|V| + 1)`
lines, so `O(k^2 |V|^2)` outcomes. Multiply over `2D` coordinates; since
`log h_0, log M, log |V| = O(log k)`, the total is `exp(O(D log k))`.

## A third family of local-lemma events

Put `M_s = D ceil(log k)^2` and fix `δ_s in (0, 1)`. For a short-period
word `W`, call a label of `W` **s-light** if its multiplicity in `W` is at
most `k/M_s`, and let `k_L(W)` be the number of positions with s-light
labels. For every short-period word with `k_L(W) >= δ_s k`, add the
event

```math
E_W:\quad\Bigl|\sum_{\beta\ \text{s-light}}w_\beta\bigl(\xi_\beta-\tfrac12\bigr)\Bigr|
\ \ge\ \epsilon\,k_L(W),
```

where `w_β` is the multiplicity and `ξ_β` the label bit. By Hoeffding's
inequality for the independent bounded terms `w_β ξ_β`,

```math
\Pr(E_W)\le2\exp\Bigl(-\frac{2\epsilon^2k_L^2}{\sum w_\beta^2}\Bigr)
\le2\exp\bigl(-2\epsilon^2\delta_sM_s\bigr),
```

since `sum w_β^2 <= (k/M_s) k_L`. Give `E_W` the weight
`z = exp(-ε^2 δ_s M_s)`. By Lemma 2, the weight of third-family
events through one label is

```math
\iota_3\le\exp\bigl(O(D\log k)-\epsilon^2\delta_sD\lceil\log k\rceil^2\bigr),
```

which is smaller than any power of `k` for large `k`. The first and second
families of `sharpened-region-proof.md` have incident weights per label at
most `ι_1 <= k T_glob exp(-ε^2(δ M - 1))` (a bound on the total
first-family weight, used per label) and
`ι_2 <= sum_{h > h_0} (CDh)^{6D} exp(-ε^2 h/2)`. Both are also
smaller than any power of `k`, because `2a < m` and `h_0 = D ceil(log k)^2`.

* For an event of the first two families testing `l` labels, the neighbours
  add at most `l (ι_1 + ι_2 + ι_3)`. This is below `ε^2 l/4`,
  so their criterion is unchanged.
* For `E_W`, the neighbours add at most `k (ι_1 + ι_2 + ι_3) = o(1)`,
  and `2 exp(-2ε^2 δ_s M_s) <= z e^{-o(1)}`.

The asymmetric local lemma therefore gives one outer coloring that satisfies
all three families. In particular, every short-period word with
`k_L >= δ_s k` has at least `(1/2 - ε) k_L` s-light positions of
each color.

## The new estimate for non-rich progressions

**Theorem.** Assume `b < a` and `a + b < 1`, and use the outer coloring
above. The probability `A'_k` that some progression that is not
`γ`-rich is monochromatic tends to zero, uniformly over the allowed
source primes.

*Proof.* Fix a target color `β_0` and a non-rich progression `P`. It is
short-period, so its key word `K(P) = (κ(n_j))_j` is that of an affine
progression. Its boxes are fixed by `D` two-parameter arrangements, one per
y-coordinate, and its
bands by `(θ_0, θ_1, θ_2)`, as in the source. So the key words
of all non-rich progressions number at most

```math
\exp\bigl(O(D\log k)\bigr)\,C\bigl(k(Dq^2+2)\bigr)^3=\exp\bigl(6\log q+O(D\log k)\bigr).
```

Let `k_L` be the number of positions of `P` with s-light labels.

*Case (i): `k_L >= δ_s k`.* By the third family, at least
`(1/2 - ε) δ_s k` s-light positions have the color opposite to
`β_0`. All of these need a flip, and by multiplicity two they carry at
least `x = ceil((1/2 - ε) δ_s k/2)` distinct keys. So the event
lies in `{at least x keys of K(P) are flipped}`, whose probability is at
most

```math
\binom{k}{x}p^x\le\Bigl(\frac{ekp}{x}\Bigr)^x=\exp\bigl(-(b-o(1))\,x\log k\bigr)
=\exp\bigl(-\Omega(k\log k)\bigr).
```

Only `K(P)` indexes this cover; no color word is used.

*Case (ii): `k_L < δ_s k`.* At least `(1 - δ_s) k` positions carry
labels of multiplicity `> k/M_s`, so there are at most `M_s` such labels. By
Lemma 1 each one is a single run. Encode the period `h <= h_0` once, and
then each run by its class `r < h`, its first and last positions, and its
color: at most `h_0 exp(M_s(3 log k + 1) + log M_s) = exp(O(D log^3 k))`
choices. Together with
`K(P)`, the runs fix the flip prescribed at every heavy position. The event
lies in the event that these prescriptions hold, which has probability at
most `(1-p)^{(1 - δ_s) k/2}`, because `p <= 1 - p` and the heavy
positions carry at least `(1 - δ_s) k/2` distinct keys.

Summing over the two targets and over all codes,

```math
A'_k\le 2e^{6\log q+O(D\log k)}\Bigl(e^{-\Omega(k\log k)}
+e^{O(D\log^3k)}\,e^{-(1-\delta_s)pk/2}\Bigr).
```

Here `log q = c k^{1-a} log k (1 + o(1))` and `pk = k^{1-b}`. So
`A'_k = o(1)` when `b < a` (for the `6 log q`) and `a < 1 - b` (for the
`D log^3 k`). No count of full label words is used.

The rich progressions are covered by the rich-event estimate of
`digit-rank-proof.md`, under `2c < γb`; that estimate never used the
affine count. Every progression is rich or non-rich, so `R_k + A'_k < 1`
eventually, and the digit product gives the theorem uniformly in `r`.

## Sufficient region and supremum

```math
a,b,c>0,\quad 2a<m<1,\quad b<a,\quad a+b<1,
```

```math
0<\epsilon<\tfrac12,\quad 0<\epsilon_{\rm reg}\le\tfrac12,\quad 0<\delta,\ \delta_s<1,\quad
\gamma<(\tfrac12-\epsilon)(1-\epsilon_{\rm reg})(1-\delta),\quad 2c<\gamma b .
```

Compared with `digit-rank-proof.md`, the inequality `2a < 1 - b` is replaced
by `a + b < 1`, which already follows from `b < a < 1/2`. So the binding
constraints are now `2a < m < 1` (the first local-lemma family) and `b < a`
(the band entropy), giving `b < a < 1/2` and

```math
c<\frac{\gamma b}2<\frac12\cdot\frac12\cdot\frac12=\frac18 .
```

Every fixed `c < 1/8` is admitted: let `ε, ε_reg, δ -> 0`,
`γ -> 1/2`, `a -> 1/2`, `b -> a` from below, and `m in (2a, 1)`. The
endpoint is not asserted, and `audit_math.py` rejects it.

The supremum `1/8` is again `γb/2` at the caps `γ < 1/2` and
`b < 1/2`. The cap on `b` now comes from `b < a` and `2a < m < 1`.

## Explicit choice

```math
a=\tfrac{49}{100},\quad m=\tfrac{99}{100},\quad b=\tfrac{97}{200},\quad
\delta=\epsilon=\epsilon_{\rm reg}=\tfrac1{200},\quad
\delta_s=\tfrac12,\quad\gamma=\tfrac{97}{200},\quad c=\tfrac19 .
```

| Inequality | Positive margin |
|---|---:|
| m > 2a | 1/100 |
| m < 1 | 1/100 |
| b < a | 1/200 |
| a + b < 1 | 1/40 |
| 0 < δ_s < 1 | 1/2 |
| γ < (1/2−ε)(1−ε_reg)(1−δ) | 40499/8000000 |
| 2c < γb, as γb/2 − c | 4681/720000 |

The last entry is

```math
\frac12\Bigl(\frac{97}{200}\Bigr)^2-\frac19=\frac{9409}{80000}-\frac19
=\frac{84681-80000}{720000}=\frac{4681}{720000}.
```

These parameters violate the old affine gap: `1 - b - 2a = -93/200 < 0`. So
the choice lies outside the region of `digit-rank-proof.md`, and indeed
`1/9 > 1/12`. `parameters.json` stores it under `short_period_proposals`.
`audit_math.py` checks every margin exactly and that the old gap fails. It
rejects five boundary controls: `b = a`, `m = 2a`, `c = γb/2`, γ at
the balance bound, and `c = 1/8`.

## What is and is not claimed

New here:

* the third local-lemma family, made affordable by Lemma 2;
* the run structure of Lemma 1;
* the two-case estimate for non-rich progressions, which never counts full
  label words.

Imported:

* the rich-event estimate of `digit-rank-proof.md`, which rests on the
  restated upstream repeated-key facts;
* the sharpened dichotomy and its two families;
* the source's drift and path lemmas;
* the two-point norm-band lemma.

None of this has been independently reviewed. Passing the scripts
establishes the inequalities, not the transfer as a theorem. No finite
coloring, finite van der Waerden record, or runtime improvement follows. The
threshold is not explicit. With exponent gaps of 1/200 it is astronomically
large: `log k` must be in the thousands.
