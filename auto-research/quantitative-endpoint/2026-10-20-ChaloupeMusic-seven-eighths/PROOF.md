# A seven-eighths logarithmic loss at the conditional 1/8 endpoint

## 1. Claim, status, and what changes

All logarithms are natural. This is a conditional proof draft, not an independently reviewed theorem.
It modifies PR #12 (`2026-10-15-1337isnot1337-logarithmic-loss/PROOF.md`, head `029431bb`, cited below
as "#12") and keeps its finite source interfaces (#12, Section 2) unchanged, with the two extensions
stated in Section 2 below.

**Conditional theorem.** Assume the finite source interfaces of #12, Section 2. For every integer
`k >= 2^739` and every integer `r >= 2`,

```math
 W_r(k)>\left(\frac{k^{1/8}}{e^{35/2}(\log k)^{7/8}}\right)^{k\lfloor\log_2 r\rfloor}. \tag{1}
```

The construction works for every prime `k < P <= 2k^2`. In particular, for every integer `k >= 2^2504`,

```math
 W_r(k)>k^{(k/9)\lfloor\log_2 r\rfloor}. \tag{2}
```

Compared with #12, which proves `(k^{1/8}/(e^{20}\log k))^{k\lfloor\log_2 r\rfloor}` for `k >= 2^1024`,
the base of (1) is larger by the factor `e^{5/2}(\log k)^{1/8} > 1` for every `k >= 2^1024`. The
coefficient of `k log log k` in the exponent drops from 1 to 7/8. The `c = 1/9` threshold drops from
`2^4096` to `2^2504`. These bounds do not assert `c > 1/8`.

**The one new ingredient.** #12 (like the source and `sharpened-region-proof.md`) partitions a
long-period progression into full blocks of the closest-return length `h` plus a remainder of fewer
than `h` positions. The heavy positions of the remainder are lost, which costs up to `h <= 2M` positions
in the dichotomy, #12 (25), and forces `M <= k/t`. Here the progression is partitioned **without
remainder** into blocks whose lengths lie in `[h/2, h]` (Lemma 5.1). Every such block still has pairwise
distinct labels, its eligibility proof is unchanged, and its nonregular fraction at most triples
(Lemma 5.2). The dichotomy then loses nothing to the return block, and `M` can be `⌊k/32⌋`. Everything
else is #12's argument at new scales.

**Where `7/8` comes from.** The flip probability is `p = 16384 t^{7/2}/sqrt(k)` instead of
`65536 t^4/sqrt(k)`, because `D` grows like `sqrt(k)/t^{5/2}` instead of `sqrt(k)/t^3`. The extra
`t^{1/2}` comes from `M = Θ(k)` in the first local-lemma family. Since `log N ≈ γkL/2` with
`L = log(1/p)`, the factor `t^{-1/2}` in `p` gains `(k/8) log t`. The constant `16384` instead of
`65536` is a separate saving of order `k`, unrelated to `M`. Case (ii) is compared with the full exponent
of `e^{−pk/4}` (as in #12's own bound on the event, and PR #9 (11.5)), where #12 (31) compared with
`pk/16`.

## 2. Interfaces

The geometry, word-count, digit-rank and affine-key-word interfaces are those of #12, Section 2,
including (3)–(8) there and the error `E = 10k + 100Dt + 6 log q` of #12 (6)–(7). Their stated scope
(`k >= 16`, `1 <= D <= k/64`, `q = P^e`, `H = k^{-2}`, `J <= k^6`, the source meshes, `D, h_0, M <= k`)
holds at the scales of Section 4. Two statements are used in a slightly extended form. Both extensions
are re-proved from the arguments that #12 imports (PR #9, Section 4.3, and the source, Section 03).

**(I1) Truncation constant.** #12 (4) is stated with `B_0 = ⌈128/ε_reg + 4⌉`, the value for
`η = ε_reg/(8D)`. Its proof (PR #9 (4.6); source, Lemma `count:local`) only uses that the truncated
output on an arc of length `4H` has at most `16/η + 4 <= B_0 D` breakpoints (source, Lemma
`mesh:truncated`), together with `B_0 D >= 49` for the stationary coordinates. Here
`η = 1/(24Dt)`, so `16/η + 4 = 384Dt + 4`, and we take

```math
 B_0=\lceil 384t+4\rceil \le 385t .
```

**(I2) Patterns of every length `ℓ <= h`.** For `h_0 < h <= 2M`, `t in {0,...,h-1}^D` and
`1 <= ℓ <= h`, a *length-`ℓ` pattern* is the recorded word at positions `0 <= z < ℓ` of the paths of
#12 (4) / source (`count:local-paths`). It is *eligible* when conditions (ii)–(iii) of the source's
Definition `count:eligible` hold, and condition (i) holds with `ℓ/2` in place of `h/2`: at least `ℓ/2`
positions are regular, and their labels are pairwise distinct.

*Count.* Through a fixed full label, the number of triples `(t, ℓ, eligible length-ℓ word)` with
`⌈h/2⌉ <= ℓ <= h` is at most `h·A_h`, with `A_h` as in #12 (4) and `B_0` as in (I1).

*Proof.* Fix `ℓ`. The proof of PR #9 (4.6) runs unchanged with the positions restricted to `z < ℓ`: the
anchor has `ℓ <= h` choices; in each scalar coordinate the target ranges are the same (`|z − z_0| < ℓ <= h`)
and at most `B_0 D ℓ <= B_0 D h` comparison lines arise (at most 4 per position in first-system
coordinates, 49 in stationary ones, `B_0 D` in rotating ones); the vector `t` has `h^D` choices. Hence at
most `A_h` words for each `ℓ`, and at most `h/2 + 1 <= h` values of `ℓ`. ∎

## 3. The dilation

Unchanged from #12, Section 3: for `x >= 16`, `π(x) <= 10x/log x`, and

```math
 \log\lambda\le\pi(h_0)\log(2M)\le 60h_0 \tag{3}
```

whenever `log h_0 >= t/3` and `log(2M) <= 2t`, both shown in Section 4.

## 4. Variable parameters

For real `t = log k >= 512`, set

```math
 u=\frac{e^{t/2}}{4096\,t^{5/2}},\quad D=\lceil u\rceil,\quad
 M=\left\lfloor\frac k{32}\right\rfloor,\quad
 h_0=\lceil 256\,D t^3\rceil,\quad M_s=\lceil 4096\,D t\rceil,
```
```math
 \epsilon=\epsilon_{\rm reg}=\frac1t,\quad \eta=\frac1{24Dt},\quad \epsilon_s=\frac14,\quad \delta_s=\frac12,
 \quad \gamma=\frac12-\frac3t,\quad p=\frac{16384\,t^{7/2}}{\sqrt k},
 \quad F=k\left(\frac t8-\frac78\log t-\frac{35}2\right). \tag{4}
```

Construct `λ` from `M, h_0` as in the source. Choose any prime `k < P <= 2k^2`, and let `q` be the least
positive power of `P` with `D log q >= F`. Then `F <= D log q <= F + D log P <= F + 3Dt`.

The following hold for every `t >= 512`. Each "monomial" bound is a statement `A t^j e^{-dt} <= B` for all
`t >= 512`, certified in `verify.py` from the sign of `j − dt` and the value at `t = 512` with `e >= 2`.
Bounds involving `sqrt(t)` are squared first, so all certified degrees are integers.

| Bound | Reduction | Certificate |
|---|---|---|
| (4.1) `u >= 1`, hence `u <= D <= 2u` | `4096^2 t^5 e^{-t} <= 1` | monomial |
| (4.2) `k/33 <= M <= k/32` | `1056 e^{-t} <= 1` | monomial |
| (4.3) `sqrt(k t)/16 <= h_0 <= sqrt(k t)/7` | `h_0 >= 256 u t^3`; `h_0 <= 257 D t^3 <= 514 u t^3` | exact |
| (4.4) `log h_0 >= t/3` | `t/2 + (1/2) log t − log 16 >= t/3` | `t/6 >= 3` |
| (4.5) `h_0 < 2M`, `2M < k < P` | `(33/14)^2 t e^{-t} < 1` | monomial |
| (4.6) `M_s <= 4097 D t <= 8194 u t <= k` | `(8194/4096)^2 t^{-3} e^{-t} <= 1` | monomial |
| (4.7) `D <= k/64` | `(128/4096)^2 t^{-5} e^{-t} <= 1` | monomial |
| (4.8) `p <= 1/2` | `4·16384^2 t^7 e^{-t} <= 1` | monomial |
| (4.9) `log t <= t/32` | value at 512 and monotonicity | as in #12 |
| (4.10) `L := log(1/p) = t/2 − (7/2) log t − 14 log 2 >= t/4` | `t/4 − (7/64)t >= 14 log 2` | exact, by (4.9) |
| (4.11) `F >= kt/32 > 0` | `3t/32 − (7/256) t >= 35/2` | exact, by (4.9) |
| (4.12) `Q := log q <= 512 sqrt(k) t^{7/2} + 3t` | `Q <= F/u + 3t`, `F <= kt/8` | exact |
| (4.13) `6Q + 100Dt <= k` | three monomials, each `<= 1/3` | monomials |
| (4.14) `J <= 2k^3 t + 2 <= k^6` | `(D+1)Q <= kt/4 + k`; `(2t+2) e^{-3t} <= 1` | monomial |

From (4.13): `E <= 11k` and `log T_K <= 6Q + 32Dt <= k`, as in #12. In (4.12), `log P <= 2t + log 2 <= 3t`.

## 5. Geometry at these scales

**Smallness conditions.** With `H = k^{-2}` and `H_x = H/λ`:

* `2M/k <= 1/16` (stationary eligibility, source Section 05), since `M <= k/32`;
* `4MH/k <= 1/(8k^2) <= η`, since `3Dt <= k^2`;
* `k/M >= 32`, so a heavy label (multiplicity `m_* > k/M`) has `m_* − 1 >= k/(2M)`, as the drift lemma requires;
* `4MH <= 1/(8k)`, which gives the path lemma `(1 − 2MH)/(2M) > H`, the heavy-width bound `2H + 4MH/h < 1`, the short-period motion `4MH/h < 1/2`, `|v − λu| <= 6MH/k < 1`, and Lemma 1 of `short-period-runs-proof.md` (`2MH_x < 1/2`).

**Lemma 5.1 (canonical partition).** Let `1 <= h <= k/2`, `n = ⌈k/h⌉`, and write `k = n⌊k/n⌋ + ρ` with
`0 <= ρ < n`. The *canonical partition* of `{0, ..., k−1}` for `h` consists of `n` consecutive blocks,
the first `ρ` of length `⌊k/n⌋ + 1` and the others of length `⌊k/n⌋`. Every block length lies in
`[⌈h/2⌉, h]`.

*Proof.* Since `n >= k/h`, `k/n <= h`, so `⌈k/n⌉ <= h` because `h` is an integer. Since `n >= 2` and
`k >= (n−1)h + 1`,

```math
 \frac kn-\frac{h+1}2\ \ge\ \frac{(n-1)h+1}n-\frac{h+1}2=\frac{(n-2)(h-1)}{2n}\ \ge 0,
```

so `⌊k/n⌋ >= ⌊(h+1)/2⌋ = ⌈h/2⌉`. ∎

The partition depends only on `h` and `k`. In every use below, `h` is the closest-return gap of the heavy
label of smallest first occurrence, which is a function of the full-label word alone (#12, Section 6;
`sharpened-region-proof.md`, Change 3). The partition of an actual progression is therefore a function
of its label word, and every event defined from it below is well defined. In the long-period range
`h <= 2M <= k/16`, so the hypothesis `h <= k/2` holds.

**Lemma 5.2 (regularity of short blocks).** Let `h_0 < h <= 2M`, let `i` be a rotating coordinate for
`(h, t)` (so `s_i = h/gcd(h, λt_i)` satisfies `h_0 < s_i <= h`), and let a block of an actual long-period
progression have length `ℓ` with `h/2 <= ℓ <= h`. Then at most a fraction `4η + 1/s_i + (4ηs_i + 1)/ℓ`
of its positions are nonregular in coordinate `i`. Summed over the at most `D` rotating coordinates, the
nonregular fraction is at most

```math
 D\left(12\eta+\frac3{h_0}\right)=\frac1{2t}+\frac{3D}{h_0}\le\frac1{2t}+\frac3{256t^3}\le\frac1t .
```

*Proof.* As in the source (Section 05, "Longer periods"), the actual value at block position `z` is
within `(z/h)|v_i| <= |v_i| <= 4MH/k < η` of the grid value `y_i(n_{j_0}) + zλt_i/h`. The map
`z ↦ zλt_i/h mod 1` has exact period `s_i` and visits each of the `s_i` grid points once per period, so
over `z < ℓ` each grid point is visited at most `⌈ℓ/s_i⌉ <= ℓ/s_i + 1` times. A nonregular position has
its grid value within `2η` of the cut, and an arc of length `4η` contains at most `4ηs_i + 1` grid points
(source). Hence the fraction is at most `(4ηs_i + 1)(1/s_i + 1/ℓ)`. Using `s_i <= h <= 2ℓ` and
`h_0 < s_i, h`, this is at most `4η + 1/h_0 + 8η + 2/h <= 12η + 3/h_0`. ∎

For a full block (`ℓ = h`) the source obtains `4η + 1/s_i`. The full-residue property is used only here.

**Lemma 5.3 (eligibility).** In a long-period progression (`h_0 < h <= 2M`), every block of the
canonical partition that contains a heavy index is an eligible length-`ℓ` pattern in the sense of (I2),
with at least `(1 − 1/t)ℓ` regular positions.

*Proof.* We go through the source's long-period paragraph sentence by sentence. A block starting at
`j_0` has the form of the paths with starting points `x(n_{j_0})`, `y(n_{j_0})` and the same
`h, t, u, v`, restricted to `z < ℓ`. Its regular fraction is at least `1 − 1/t` by Lemma 5.2. Its labels
are pairwise distinct by the path lemma, since `ℓ <= h` consecutive indices are pairwise incongruent
modulo `h`. The bounds `|u_i| <= H_x` and `|v_i| <= H` are those of the drift lemma. For the stationary
condition, fix the heavy index `j_*` in the block and a stationary coordinate `i`. Every block index `j`
has `|j − j_*| <= ℓ − 1 < h`, so the source's estimate
`dist(y_i(n_j), y_i(n_{j_*})) <= (|j − j_*|/h)|v_i| <= |v_i| <= (2M/k)L_*` holds verbatim, and the
neighbourhood lemma gives `|V(y_i(n_j))| >= L_*/16 >= |v_i|` by `2M/k <= 1/16`. No other sentence of the
paragraph uses that a block is full. ∎

## 6. The outer families

Assign an independent fair bit `ξ_β` to each literal full label.

**Family 1** (#12 (22), with the canonical partition). For every actual full-label word, let `S` be the
set of light positions outside the blocks of the canonical partition that contain a heavy index; if
there is no heavy label, `S` is every position. Exclude
`|Σ_β w_β(ξ_β − 1/2)| > k/t`. Since `Σ w_β^2 <= (k/M)|S| <= k^2/M`, weighted Hoeffding gives probability
at most `2 exp(−2M/t^2)`; the weight is `z_1 = exp(−M/t^2)`. There is one event per actual word.

**Family 2** (patterns of (I2)). For every `h_0 < h <= 2M`, every `t`, every `⌈h/2⌉ <= ℓ <= h`, and every
eligible length-`ℓ` recorded word, exclude a deviation greater than `l/t` on its `l` regular labels. Here
`l >= ℓ/2 >= h/4`, the tested labels are distinct, Hoeffding gives `2 exp(−2l/t^2)`, and the weight is
`z_2 = exp(−l/t^2)`. Events are indexed by `(h, t, ℓ, word)`. If two indices record the same word they
give identical events; both are kept and both are counted below, which only overcounts the incident
weight. Every heavy-containing canonical block of every long-period progression is an instance
(Lemma 5.3), whatever its position in the progression: the start points `x, y` of a pattern are free
real parameters. Blocks without a heavy index are not needed (they lie in `S`).

**Family 3** (#12, unchanged). Short-period words with at least `k/2` s-light positions; a `1/4` fraction
of each bit there; probability `<= 2 exp(−M_s/16)`, weight `z_3 = exp(−M_s/32)`.

**Incident weights.** At any fixed label:

* `I_1 <= T_glob z_1`. By #12 (3) with `J <= k^6` and (3),
  `log T_glob <= 42Dt + 4D log λ <= 42Dt + 240 D h_0 <= 84ut + 240·257·4 u^2 t^3`, that is

  ```math
  \log T_{\rm glob}\le \frac{84}{4096}\,\frac{\sqrt k}{t^{3/2}}+\frac{246720}{4096^2}\,\frac{k}{t^2}. \tag{5}
  ```

  With `M/t^2 >= k/(33t^2)` and `1/33 − 246720/4096^2 − 3/200 > 0`, three monomials give
  `log I_1 <= −t − 4 <= −log(48k)`.
* `I_2 <= Σ_{h_0<h<=2M} h·A_h·e^{−h/(4t^2)}`. #12 (19), `log A_h <= 15Dt` for `h <= k`, holds verbatim:
  its proof uses `B_0 <= 512t` and `log(B_0 D h + 1) <= log(512t) + 2t <= 3t`, and here `B_0 <= 385t`.
  With `h/(4t^2) >= 64Dt` for `h > h_0` and at most `2M <= k` values of `h`,
  `I_2 <= k^2 e^{15Dt − 64Dt} <= e^{2t − 49t} <= 1/(48k)`.
* `I_3 <= A_s e^{−M_s/32} <= e^{40Dt − 128Dt} <= 1/(48k)` (#12 (20) holds for `D, h_0, M <= k`).

Each event uses at most `k` variables, so its total neighbour weight is at most `1/16`. Every weight is
`e^{−w}` with `w >= 1` (`l/t^2 >= h_0/(4t^2) >= 64Dt`, `M/t^2 >= 1`, `M_s/32 >= 128Dt`). The criterion
(#12 (24)) `e^{−w−1/8} >= 2e^{−2w}` holds, and the finite asymmetric local lemma gives one colouring
avoiding all three families.

## 7. The outer dichotomy

Fix a progression with a heavy label whose closest return satisfies `h_0 < h <= 2M`. Let `E_pos` be the
union of the canonical blocks that contain a heavy index, and `S` the remaining positions. A block without
a heavy index consists of light positions, so `S` is exactly the light-position set of Family 1, and
**`|E_pos| + |S| = k`**: there is no remainder. By Lemma 5.3 and Family 2, each block of `E_pos` of length
`ℓ` has at least `(1/2 − 1/t)(1 − 1/t)ℓ = A_0 ℓ` positions of each bit. By Family 1, `S` has at least
`|S|/2 − k/t` of each bit. Since `A_0 <= 1/2`, each bit occupies at least

```math
 A_0|E_{\rm pos}|+\frac{|S|}2-\frac kt\ \ge\ A_0k-\frac kt\ \ge\ \Bigl(\frac12-\frac5{2t}\Bigr)k\ >\ \gamma k. \tag{6}
```

This replaces #12 (25), `A_0(k − h) − k/t`. The term in `h`, which forced `M <= k/t` there, is gone. If no
heavy label exists, Family 1 gives `(1/2 − 1/t)k` directly. So every progression that is not
`γ`-rich has a heavy label with short closest return, and is affine with single runs, as in #12, Section 7.

## 8. Rich events

As in #12, Section 8, with `Γ = γkL/2 − D log q`. By (4),

```math
 \frac{\gamma L}2=\frac t8-\frac78\log t-\frac72\log2-\frac34+\frac{21\log t}{4t}+\frac{21\log 2}{t},
```

so, using `D log q <= F + 3Dt` and `log 2 <= 0.69315`,

```math
 \Gamma\ \ge\ k\Bigl(\frac{35}2-\frac72\log 2-\frac34\Bigr)-3Dt\ \ge\ 14.32\,k-3Dt\ \ge\ 14k, \tag{7}
```

because `100Dt <= k` by (4.13), so `3Dt <= 3k/100`. The rank split of #12 (27) is unchanged, and
`R_k <= 4(D+1)e^{E−Γ} <= 8k e^{−3k} < 1/4`.

## 9. Non-rich events

As in #12, Section 9.

*Many s-light positions.* `2 T_K 2^k p^{k/16} <= 2 e^{2k − kt/64} < 1/4`, by `log T_K <= k` and `L >= t/4`.

*Few s-light positions.* `B_run = h_0(M_s+1)(2k^3)^{M_s}`, so
`log B_run <= 2t + M_s(3t+1) <= 2t + 7 sqrt(k) t^{−1/2}`, by (4.6). With (4.12),

```math
 \log T_K+\log B_{\rm run}+\log 8\le 3072\sqrt k\,t^{7/2}+20t+3+\Bigl(7+\tfrac1{64}\Bigr)\frac{\sqrt k}{t^{1/2}}
 \le 3073\sqrt k\,t^{7/2}<4096\sqrt k\,t^{7/2}=\frac{pk}4, \tag{8}
```

and the total is less than `1/4`. Equations (7) to (8) bound the probability of a bad progression by
`3/4`, so a valid cyclic two-colouring exists, with `N = q^D >= e^F`. The digit product of the source
gives (1) for every `k` with `log k >= 512`, which includes every `k >= 2^739` since `739 log 2 > 512`.

## 10. The `1/9` threshold

`F >= kt/9` is `g(t) := t/72 − (7/8) log t − 35/2 >= 0`. The function `g` increases for `t > 63`. At
`t = 1735`, `g >= 1735/72 − (7/8)·7.4593 − 35/2 > 0`, with the rational upper bound
`log 1735 <= 7.4593` certified in `verify.py`. Every `k >= 2^2504` has `t >= 2504 log 2 >= 1735.6`, which
proves (2).

## Appendix. What is and is not re-proved

Re-proved here: Lemmas 5.1–5.3, the extension (I2) of the anchored count to short patterns, the rewritten
dichotomy (6), and every inequality of Sections 4–10 at the new scales. Imported unchanged: the finite
interfaces of #12, Section 2 (geometry, global and short-period word counts, digit-rank counts with
`E = 10k + 100Dt + 6 log q`, affine key words), #12's dilation bound, its Family 3, the rank split,
and the source's digit product. #12's Family 1 is used with `S` redefined through the canonical
partition (Section 6). Its probability and weight are unchanged; `S` itself changes. The local lemma, Hoeffding's inequality, and the encodings of
PR #9 are not formalized.
