# A ceiling of 1/24 for the key-flip architecture

This note records why the sharpened region of `sharpened-region-proof.md`
stops at 1/24, and why that number is a property of the proof
*architecture* rather than of its parameters. It is the van der Waerden
analogue of the matrix-profile obstruction in `research-note.tex`: a
statement about what a family of arguments can prove, not a statement
about the true growth of van der Waerden numbers. Nothing here is a
lower bound on the best possible coefficient.

## The template

Every argument in this repository, and the source manuscript, has the
following shape. Write `D = ceil(k^a)`, `N = q^D >= k^{ck}`, and
`p = k^{-b}`.

* **(T1) Outer coloring.** A coloring `c_0` of `Z/N` that factors through
  a label word of entropy `log T_glob`, chosen by a local lemma so that
  every progression is either *balanced* (at least `gamma k` positions
  of each outer color) or *affine* in the centered second coordinates.
* **(T2) Keys and flips.** A key map `kappa` on `Z/N` such that every key
  occurs at most `mu` times on any progression, and an independent
  Bernoulli(`p`) flip per key. The final coloring is `c_0 + E_kappa`.
* **(T3) Rich bound.** A union bound over the `N^2` progressions:
  `R_k <= 2 q^{2D} p^{gamma k/mu}`, so `2c < gamma b/mu`.
* **(T4) Affine bound.** A union bound over affine *signatures* (outer
  color word and key word), `A_k <= 2 T_aff (1-p)^{k/mu}`, so
  `log T_aff = o(pk)`, where `log T_aff` contains both `log T_glob` and
  the key-word entropy along affine progressions.

In the source, `mu = 4`, `gamma = 1/100`, `b = 1/20`, `c = 1/100000`. In
the sharpened region, `mu = 2`, `gamma -> 1/2`, `b -> 1/3`, `c -> 1/24`.

## The proposition

**Proposition.** In the template with `mu = 2`, key-word entropy
`(6 + o(1)) log q` along affine progressions, and
`log T_glob = k^{2a + o(1)}`, every admissible `c` satisfies `c < 1/24`.

*Proof.* (T3) with `mu = 2` gives `c < gamma b / 4`. The outer coloring
places at most half of the positions on the minority color, so
`gamma <= 1/2`. (T4) needs `6 log q = 6 c k^{1-a} log k (1 + o(1))`
to be `o(k^{1-b})`, hence `b < a`, and needs `k^{2a+o(1)} = o(k^{1-b})`,
hence `2a + b <= 1`. Equality is not excluded by the unspecified `o(1)`:
for example, `k^{2a}/log k` is `k^{2a+o(1)}` and is `o(k^{1-b})`
when `2a+b=1`. Nevertheless, `b < a` gives
`3b < 2a+b <= 1`, so `b < 1/3`. Thus
`c < (1/2)(1/3)/4 = 1/24`. The supremum is approached, not attained,
exactly as in the sharpened region. ∎

The exact-arithmetic check `template_ceiling` in `audit_math.py`
maximizes `b` under `b <= a`, `2a + b <= 1` by linear programming and
multiplies by the balance supremum `1/2` and the factor `1/4`.

## Why each template constant is rigid

These are explanations, not theorems; each describes an attempt to move
the constant and the specific place where it fails.

**`gamma <= 1/2`.** This is already the best possible fraction of a
minority color. The sharpened region reaches it up to `epsilon`.

**`mu = 2` (the two-point norm band).** A key must be a function of the
point `z = q y~(n)` alone, and the band is `floor(|z|^2)`. On a line
through its nearest point `z_0` to the origin, the two points
`z_0 +- u e` have identical squared norm, so any band of a quadratic (or
any shifted norm `|z - v|^2`) admits two occurrences. Distinguishing the
pair needs a functional `xi` with `|<xi, e>| >= 1` for the line's unit
direction `e`; since the realizable directions are essentially
arbitrary in `R^D`, that needs about `D` functionals, and each one adds
`2 log q` to the affine key-word entropy, giving `2D log q = 2ck log k`,
which is never `o(pk)`. Modular bands (`floor(|z|^2) mod R`) fail on
lines with `sigma^2 = R`, where every point shares a band; wider bands
raise `mu` linearly while lowering the entropy only logarithmically.
Replacing a key by the fine grid cell of `z` (side below `1/sqrt D`)
gives `mu = 1`, but any two distinct group elements are already
separated by at least one after the `q` scaling, so that is an
independent bit per element, a uniformly random coloring, which fails
once `N > 2^{k/2}`.

**`b < a` (the `6 log q`).** The band word along an affine progression
is `floor(theta_0 + theta_1 j + theta_2 j^2)` with
`|theta_2| <= Dq^2 / (4k^2)`, `|theta_1| <= Dq^2/k`, `theta_0 <= Dq^2/4`;
counting words at the natural resolutions `1/k^2`, `1/k`, `1` gives
`q^{6 - o(1)}` words, so the arrangement bound is tight up to constants.
Any post-processing `g(band)` with fibers of size `F` keeps the same
arrangement bound while raising `mu` to about `2F`.

**`2a + b <= 1` (the necessary label-entropy exponent condition).** The
sharpened sufficient region still uses `2a+b<1` to absorb its logarithmic
factors; the template's unspecified `o(1)` only forces the weak inequality.
`log T_glob` is dominated
by `2D log lambda`, two real parameters per first-system coordinate at
mesh scale `H/lambda`. That mesh scale is what certifies that the
second-system rational step is a multiple of `lambda`; coarsening it
produces coordinates whose rotation denominators can be as small as 2,
and then up to half the positions of a block are nonregular in that
coordinate. The dilation itself needs the full `l`-primary part of every
period up to `2M` for every prime `l <= h_0`. Since `h_0 <= 2M`,
each such prime has `x = log(2M)/log l >= 1`, and
`x/2 <= floor(x) <= x`. Therefore the exact sum and its bounds are

```math
\log\lambda
=\sum_{\substack{\ell\le h_0\\\ell\ \mathrm{prime}}}
\left\lfloor\frac{\log(2M)}{\log\ell}\right\rfloor\log\ell,
\qquad
\frac12\pi(h_0)\log(2M)\le\log\lambda\le\pi(h_0)\log(2M).
```

Also `h_0 >= D/epsilon` is forced by the
nonregular fraction `sum_i 1/s_i` over up to `D` rotating coordinates.
Hence `log T_glob >= D * h_0 / log h_0 >= D^{2 - o(1)}`.

**The exponent 2 in `q^{2D}`.** A Lovász-local-lemma pass over the flip
bits, with one event per progression, replaces `N^2` by
`N * k^2 * max_kappa |kappa^{-1}(kappa)|`. Counting base-`q` digits
shows a key's fiber has at most `(2q/k^2 + 1)^D = N k^{-2D} 2^D`
elements, and `k^{2D} = k^{2k^a}` is negligible against `N = k^{ck}`.
So the local lemma recovers the union bound exactly. Making the
construction invariant under a unit subgroup of `Z/N` would reduce the
count, but invariance under `1 + q^{D-1} Z` forces the coloring to
factor through `Z/q^{D-1}`, which makes every progression with step
`q^{D-1}` monochromatic.

**AND-ing two flip layers.** Requiring two independent flips per
position doubles the flip count to `gamma k` but squares the effective
probability to `k^{-2b}`; the affine bound then needs `2b < min(a, 1-2a)`,
and the product `gamma * (2b) / 4` has the same supremum `1/24`.

**Moving the band into the outer coloring.** Coloring bands
deterministically balances affine progressions without flips, but on a
non-affine block the band word has entropy about `D log q`, while the
local-lemma tail is only `exp(-theta h)` with `h <= 2M`, so the
dependency weights diverge. A fixed parity rule fails on lines with
`sigma = sqrt 2`, where every band index is even.

## What would be needed

A coefficient above 1/24 by this route needs one of: a key with
`mu = 1` whose word along affine progressions has `o(pk)` entropy; a
count of affine signatures that avoids `log q` altogether; a label
system with entropy `k^{a + o(1)}` that still controls rational returns;
or a replacement for the `N^2` union bound. Each of these is a change of
construction, not of parameters. Candidate directions outside the
template include annulus constructions with independently chosen radii
(Green; Hunter) and iterated cyclic products; none is attempted here.

The original source and attribution are linked in the README. This note
is a research draft and has not been independently reviewed.
