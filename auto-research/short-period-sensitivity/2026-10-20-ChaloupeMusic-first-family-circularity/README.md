# Past √k coordinates the first local-lemma family is circular

**Status:** research note, negative result about the proof template. It gives
no bound on van der Waerden numbers, and it does not show that any
inequality is necessary for them.
**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.

## Question

The short-period region (`short-period-runs-proof.md`) has supremum 1/8
because `b < a` and `2a < m < 1` cap `b` at 1/2. The constraint `2a < m`
(F in `2026-10-20-erwan-binding-lever`) comes from the first local-lemma
family:

```math
\iota_1\le kT_{\rm glob}e^{-\epsilon^2(\delta M-1)},\qquad \log T_{\rm glob}=O(D\log\lambda).
```

Taking `a > 1/2` (more than √k coordinates) would need F to fail only
because of how the count is done. We show that F does not fail that way.
Past `a = 1/2` the first family stops being a counting problem and asks the
outer colouring for more than the theorem the template proves.

## Results

Notation follows `sharpened-region-proof.md`: `N = q^D`,
`x_i(n) = (n mod q^i)/q^i`, `U` the partition of `[0,1)` into intervals of
width `H_x = 1/(k²λ)`, and the x-label `(U(x_i(n)))_{i≤D}`.

**Lemma 1 (injective x-labels).** If `qH_x < 1`, that is `λ > q/k²`, the
x-label determines `n ∈ Z/N`.

*Proof.* Let `n ≠ n′` and write `n − n′ = q^v u` with `v < D` and `q ∤ u`.
Then `x_{v+1}(n) − x_{v+1}(n′) ≡ u/q (mod 1)`, which is at circle distance at
least `1/q > H_x` from 0. Two points of one interval of length `H_x` are
closer than `H_x`, so the labels differ in coordinate `v+1`. ∎

More generally, a fibre of the x-label has at most `(⌊qH_x⌋ + 1)^D`
elements: once the lower digits are fixed, each base-`q` digit of `n` lies in
an interval of length `qH_x`. The set `Δ` of differences between two
elements of one fibre has at most `(2qH_x + 1)^D` elements.

**Lemma 2 (when Lemma 1 applies).** Take any `h_0` with `D ≤ h_0 ≤ 2M`,
which covers the sharpened choice `h_0 = D⌈log k⌉²` (the construction
already needs `h_0 < 2M`), and `λ = ∏_{ℓ ≤ h_0} ℓ^{⌊log 2M/log ℓ⌋}`.

- For fixed `a > 1/2`, `0 < c`, `a < m < 1`, we have `qH_x → 0`.
- For fixed `a < 1/2` and the sharpened `h_0`, we have `q ≥ 400k³λ` for
  large `k`.

*Proof.* Since `h_0 ≤ 2M`, every prime `ℓ ≤ h_0` has
`log 2M/log ℓ ≥ 1`, and `⌊x⌋ ≥ x/2` for `x ≥ 1` gives
`log λ ≥ ½ π(h_0) log 2M`. For `D ≥ 17`, `π(h_0) ≥ π(D) > D/log D`
(Rosser), and `log D ≤ a log k + k^{−a}`. So
`log λ ≥ (m/(2a))·k^a·(1 − o(1))`, which is at least `k^a/(4a)` for large
`k` because `m > a > 1/2`.
Meanwhile `log q ≤ c k^{1−a} log k + log(2k²)`, by the choice of `q` in the
source. For `a > 1/2` the ratio `k^a/(k^{1−a} log k)` diverges, so
`log(qH_x) = log q − 2 log k − log λ → −∞`.

For `a < 1/2`, `π(x) < 1.25506 x/log x` (Rosser–Schoenfeld) gives
`log λ = O(k^a log² k) = o(k^{1−a} log k)`, while `log q ≥ c k^{1−a} log k`. ∎

`verify.py` evaluates both sufficient conditions in 80-digit decimal
arithmetic at `k = 10^50, 10^200, 10^1000`, for `a ∈ {0.55, 0.6, 0.75}` and
for `a ∈ {0.4, 0.45}`.

Every admissible `h_0` here is at least `D`. The nonregular fraction
`D(4η + 1/h_0) ≤ ε_reg` already requires it, and the second family requires
`h_0 ≳ D log D` regardless. Its eligible patterns include an abstract
pattern for every rotation vector `t ∈ [0,h)^D` of order `h`, so the
`(CDh)^{6D}` count is not loose in its `h^D` factor.

**Proposition 3 (the first family becomes the whole problem).** Assume
`qH_x < 1`.

1. A progression has `k` distinct terms (every nonzero element has order at
   least `P > k`). By Lemma 1 it has `k` distinct labels, so no progression
   has a heavy label.
2. In the sharpened dichotomy, every nonzero-step progression then has
   `S` = all positions, `w_max = 1`, and a single row: the whole progression.
   Property (i) of the outer colouring reads: every nonzero-step `k`-AP of
   `Z/N` has at least `(1/2 − ε)k` positions of each outer colour. Such a
   `c_0` has no monochromatic `k`-AP by itself, so `W_2(k) > N` would follow
   without keys or flips. The non-rich case of `short-period-runs-proof.md`
   is empty.
3. The template's local-lemma criterion fails. The `k(N−1)` progressions
   through one element have pairwise distinct label words. This follows from
   Lemma 1, and `verify.py` checks it on a toy case. Each tests `l = k`
   labels with weight `e^{−ε²k}`, so the incident weight per label is at
   least `k(N−1)e^{−ε²k}`. That diverges, since `log N ≥ ck log k`, while the
   criterion needs it below `ε²/4`.

   No other choice of weights helps. Each first-family event has
   probability at least `exp(−k·I(ε) − O(log k))`, where
   `I(ε) = log 2 − H(1/2 − ε) = 2ε² + O(ε⁴)` is the binomial large-deviation
   rate. Each event has at least `d = k(N−1) − 1` neighbours. For an event
   `E*` of minimal weight `z*`, the asymmetric criterion would give
   `P(E*) ≤ z*(1 − z*)^d ≤ z* e^{−z* d} ≤ 1/(ed)`, which contradicts the
   lower bound because `log N ≥ ck log k`. This strengthening was pointed out
   in the adversarial pass.

This does not show that no balanced colouring of `Z/N` exists. It shows that
past `a = 1/2` the template requires an object stronger than its conclusion,
and that its own tool does not supply it.

**Remark (the intermediate window).** Suppose `q/(400k³) < λ ≤ q/k²`, so
that `1 ≤ qH_x < 400k`.

- Fibres have at most `F_L = (400k+1)^D` elements, and the difference
  set `Δ` at most `(800k+1)^D`.
- A progression repeats a label only if `sd ∈ Δ` for some `1 ≤ s < k`.
  Since `gcd(s, N) = 1`, at most `(k−1)|Δ|` steps `d` do so.
- At least `k(N − 1 − (k−1)|Δ|)` progressions through a given element
  therefore have all labels distinct. Within each position of that element,
  a word fixes the next label and so at most `F_L` steps, which gives at
  least `k(N−1−(k−1)|Δ|)/F_L` words.
- The incident weight per label is then at least
  `k(N−1−(k−1)|Δ|)F_L^{−1}e^{−ε²k}`, which diverges because
  `D log(800k) + ε²k = o(ck log k)`.

By Lemma 2, for fixed `a ≠ 1/2` this window is eventually empty.

**Lemma 4 (the smallest periods).** No 2-colouring of `(Z/2)^D` or of
`(Z/3)^D`, for `D ≥ 2`, avoids a monochromatic affine line.

*Proof.* For `h = 2`, the lines are the pairs `{x, x+t}`. Avoiding
monochromatic pairs makes the `2^D ≥ 4` points pairwise differently
coloured, which is impossible with two colours. For `h = 3`, the largest
line-free subset of `AG(2,3)` has 4 of the 9 points, so one colour class
contains a line. A coordinate plane of `(Z/3)^D` is a copy of `AG(2,3)`.
`verify.py` checks `(Z/2)^2`, `(Z/2)^3` and `(Z/3)^2` exhaustively. ∎

Short-period blocks with periods 2 and 3 therefore cannot be balanced by any
outer colouring when all their rotation directions occur, and the dilation
must keep those primes. Every direction `t/h` is realised by a step `d` with
`|h x_i(d) − t_i| ≤ h/(2q)`: choose the base-`q` digits of `d` from the lowest
up. This lies within the dichotomy's drift bound `2MH_x/k` when
`λ ≤ 4Mq/(hk³)`. That the resulting blocks are eligible, with the shared
base labels the lemma uses, is not checked here. The plane statement stops at `h = 3`: `AG(2,5)` has a
line-free 2-colouring, stored in `verify.py` as a certificate.

Whether some explicit colouring balances all rotation orbits of orders
`4 ≤ h ≲ D log D`, which would allow a small `λ`, is open. As a heuristic,
random colourings fail once `D log h ≫ h`.

## Consequence for the template

| Regime | What happens | Source |
|---|---|---|
| `λ ≤ q/(400k³)` (every fixed `a < 1/2`) | single-label progressions exist; union bounds that cover each progression by a sub-prescription of its own keys, with iid flips, need `b < min(a, 1−a)`; a local lemma over flips is not excluded | concurrent single-label note in this sprint, not yet submitted |
| `q/(400k³) < λ ≤ q/k²` (only `a = 1/2 + o(1)`) | first-family criterion fails | Remark above |
| `λ > q/k²` (every fixed `a > 1/2`) | x-labels injective; the first family must balance every `k`-AP of `Z/N`; criterion fails | Lemma 1, Proposition 3 |

Raising `a` past 1/2 therefore needs a balance argument that is not a local
lemma over independent label bits. Smarter counting of label words will not
do it: past `a = 1/2` the words are as numerous as the progressions.

## Reproduce

```sh
python3 -B auto-research/short-period-sensitivity/2026-10-20-ChaloupeMusic-first-family-circularity/verify.py
```

Expected: exit code 0 and stdout byte-identical to `RESULT.json`. The
verifier uses only the standard library and runs in under a second.

Negative controls:

- three `(q, D, λ)` with `qH_x ≥ 1` must collide, and do (largest fibres 8,
  8 and 16, within `(⌊qH_x⌋+1)^D`, and difference sets within
  `(2qH_x+1)^D`);
- `a = 0.4` and `a = 0.45` must fail the injectivity condition and meet the
  single-label one;
- `AG(2,5)` must admit a line-free colouring.

## Scope

- The statements concern the template: x-labels at `H/λ`, a dilation `λ`
  containing the prime powers up to `h_0`, and an outer colouring of
  independent label bits through the local lemma. They are not statements
  about `W_r(k)`.
- Lemma 1, Proposition 3 and Lemma 4 are proved here. Lemma 2 is proved
  asymptotically, and the decimal evaluations are spot checks.
- Finite checks illustrate the proofs and are not premises of them.
- The first row of the table rests on a concurrent, unsubmitted note and
  carries its own scope.
