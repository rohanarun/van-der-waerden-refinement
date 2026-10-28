# Rules correlated with the outer colouring: what choosing `c₀` after `X` buys

**Status:** structural research, with proofs. No admissible `X` is proposed and
no bound on `c` is claimed. The note asks one question of Door 1: can the outer
colouring `c₀` be chosen **after** the frozen set `X`, so that it splits every
rich progression on which `X` is large, instead of asking `X` to avoid them?
(II′) allows this, because a split progression is harmless (Proposition 1 of
`2026-10-26-…-exact-door-one-condition`).

**What a positive answer would give.** The template then puts no ceiling on
`c`. Suppose that, at parameters `(a, m, b, c)` of the region, some `X` passes
(I′) on `𝒫_short` and satisfies the count of Theorem B (dangerous traces only).
Then Theorem 2 of `exact-door-one-condition` gives every `c` with
`2c < (γ − ε)b`. No other inequality of the template binds:

* the non-rich union no longer needs `b < a` or `a + b < 1`;
* the rich cost is Theorem 9 of `source-only-1-8`, with `θ` for `γ`, and (G♭)
  of the rich-cover note does not enter;
* (I′_w) gets easier as `b` grows, since `w ∝ H/(b log k)` with
  `H = O(c k^{1−a} log k)`.

So passing `1/8` needs exactly `b > 2c/(γ − ε) > 1/2` and a positive answer
to Q-S1b (§ 6) at those parameters. **Q-S1b is then the only lock.** A positive
answer for every `c` would give `W_2(k) ≥ k^{ω(k)}`. That is far beyond the
source, and it is one reason to expect the answer no.

It contains four results.

* **(A) Refined keys are free.** Keys `κ⁺(n) = (L(n), ⌊f(n)⌋)`, which carry the
  full label, change no estimate of the region. `c₀` becomes a function of the
  key, so a rule can read `c₀`. *Proved.*
* **(B) A splitting criterion** (with a dense form, Corollary B′). A fourth local-lemma family for `c_*` splits
  every rich progression with `|X_P| ≥ εk`, giving (II′) with `θ = γ − ε`, for
  **any** `X`, dense or sparse. The only condition is that the **dangerous**
  `X`-subsets are few: `e^{o(M)}` per label word and `e^{o(h)}` per eligible
  pattern, where dangerous means large on a row or on a pattern. A count is
  also necessary for every certificate in the class of the clique bound, at the
  scale `e^{O(k)}` per label (Proposition E). *Proved.*
* **(C) What (I′) costs.** For `b > a`, any `X` with which the template
  succeeds has, on the band line of a generic label, at least
  `q^{1−o(1)}` alternations between `X` and its complement. *Proved.*
* **(D) The gap.** Warren's bound verifies (B) only for rules with at most
  `e^{O(log² k)}` band intervals per label. (C) demands `q^{1−o(1)}`. The gap
  holds for every admissible cutoff `h_0`. So (B) is never verified, by this
  route, for a rule that passes (I′). *Proved.* Whether some (I′)-capable rule
  still has few realised subsets is the open question left (§ 6).

**Base commit:** `pr/door-one` (`00375ff`), on `63bef9c`.

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-27-ChaloupeMusic-colour-correlated-rules/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`. Standard
library only.

## Setting

As in `exact-door-one-condition`. The keys `κ` are those of the source, the
frozen set `X` is a set of keys, and `c₁ = c₀ ⊕ 1_X`. Keys outside `X` flip iid
with probability `p = k^{−b}`. The parameters are those of
`trust-reduction/…-source-only-1-16` §2: `D = ⌈k^a⌉`, `M = ⌈k^m⌉`,
`h_0 = DL²` with `L = ⌈ln k⌉`, `2a < m < 1`. `𝒫_short` is the set of
progressions in alternative (A) of its Theorem 6 (a heavy label, period
`h ≤ h_0`, affine). `𝒫_long` is the set of the other ones, all of them
`γ`-rich.

Theorem 2 of `exact-door-one-condition` puts (II′_θ) on the rich progressions
and (I′) on the non-rich ones. Rich progressions of `𝒫_short` can be moved to
the (I′) side without change. Theorem 8 of `source-only-1-16` counts them by
their key words and run codes, which use only the data of alternative (A) and
never non-richness. So below, (II′_θ) is required on `𝒫_long`, and (I′_η),
(I′_w) on `𝒫_short`, split by `k_L`.

## 1. (A) Refined keys

**Proposition A.** Replace `κ(n) = (V-box of y(n), ⌊f(n)⌋)` by
`κ⁺(n) = (L(n), ⌊f(n)⌋)`. All estimates of `source-only-1-16`, of
`source-only-1-8` and of Theorem 2 of `exact-door-one-condition` hold
unchanged in the region. In particular `c₀ = c_*∘L` is a function of `κ⁺`.

*Proof.* `κ⁺` is finer than `κ`, so multiplicity two (Lemma 3) holds. The
estimates read keys in four places.

1. *Lemma A\*.* The discrete data must now also fix the `U`-box word. Over all
   progressions, each `x`-coordinate is a circle path `x_i(n_0) + j x_i(d)`
   compared with the `k²λ` endpoints of `U`. That is `O(k³λ)` lines in two
   parameters, so `O(k⁶λ²)` outputs per coordinate and `exp(O(D log(kλ))) =
   exp(O(k^{2a} log³ k))` in all. This is `e^{o(k log k)}` because `2a < 1`.
2. *Lemma C\*.* It counts progressions. Its discrete data gain the same factor.
3. *Theorem 8, case (i).* The bound `T_key = e^{o(k log k)}` gains the same
   factor.
4. *Theorem 8, case (ii), and (I′_w).* The `x`-part of a short-period word is
   fixed by `h`, `t` and an arrangement in `(x_i, u_i)`, with `exp(O(D log k))`
   outputs (Lemma 4). So `H` grows by `O(D log k)`.

No other step reads a key. ∎

## 2. (B) Choosing `c₀` to split

For a frozen `X` (on `κ⁺`), write `X_P` for the positions of `P` whose key is
in `X`.

* For a label word `W`, `𝒮(W)` is the set of `X_P` over progressions `P` with
  label word `W`. Its **dangerous** part `𝒮_ε(W)` keeps the `S` that have at
  least `εM/4` points on some row of `S_all(W)` or of `S_out(W)`.
* For an eligible pattern `π` (source §03, condition (i) with `(1−ε_r)h`
  regular positions), `𝒮(π)` is the set of `X ∩ {regular positions}` over its
  realisations. Its dangerous part `𝒮_ε(π)` keeps the `S` with `|S| ≥ εh/8`.

**Theorem B.** Fix `ε ∈ (0, γ)` with `ε_r ≤ ε/8`. Suppose that, for large `k`,

```math
\log\max_W|\mathcal S_\varepsilon(W)|\le\tfrac{\varepsilon}{64}M,\qquad
\log\max_{\pi\ \text{of length}\ h}|\mathcal S_\varepsilon(\pi)|\le\tfrac{\varepsilon}{128}h\quad(h_0<h\le2M).
```

Then `c_*` can be chosen so that Proposition 5 of `source-only-1-16` still
holds and every `P ∈ 𝒫_long` with `|X_P| ≥ εk` has `X_P` meeting both colour
classes of `c₀`. Hence (II′_θ) holds on `𝒫_long` with `θ = γ − ε`, for this
`X`, whatever its density.

*Proof.* Add two event families to the local lemma of Proposition 5.

* **4a.** For each label word `W`, each `S_* ∈ {S_all(W), S_out(W)}` dealt into
  rows as in family 1, each row `r` and each `S ∈ 𝒮_ε(W)` with
  `|S ∩ r| ≥ εM/4`: the event "`c_*` is constant on the labels of `S ∩ r`".
  Labels in a row are distinct, so its probability is `2^{1−|S∩r|}`.
* **4b.** For each eligible pattern `π` of length `h` and each `S ∈ 𝒮_ε(π)` with
  `|S| ≥ εh/8`: the event "`c_*` is constant on the labels of `S`". Regular
  labels of a pattern are distinct, so its probability is `2^{1−|S|}`.

Give an event on `l` labels the weight `e^{−l/4}`. Since
`2^{1−l} ≤ e^{−l/4 − 2lι}` for `l ≥ 4` and `ι ≤ 1/10`, the criterion holds as
soon as the incident weight `ι` per label is small. The new incident weights
are:

* `ι_{4a} ≤ 2k·T_glob·max|𝒮_ε(W)|·e^{−εM/16} ≤ exp(O(k^{2a}log³k) + εM/64 − εM/16)`;
* `ι_{4b} ≤ Σ_{h>h_0}(C_rDh)^{6D}·max|𝒮_ε(π)|·e^{−εh/32} ≤ Σ_{h>h_0} exp(6D log(C_rDh) − εh/128)`.

Both are smaller than any power of `k`, because `2a < m` and
`6D log(C_rDh)/h ≤ 6 log(C_rD²L²)/L² → 0` for `h ≥ h_0`. The three old
families are unchanged, and their criteria absorb the extra `lι`.

Now take `P ∈ 𝒫_long` with `|X_P| ≥ εk`.

* *No heavy label.* Then `S_all = P`, which has at most `k/M` rows, so some row
  carries at least `εM` positions of `X_P`.
* *A heavy label and `h > h_0`.* The full blocks cover all but fewer than `h`
  positions, so `X_P` has at least `εk/2` positions in the heavy blocks or in
  `S_out`.
  * If at least `εk/4` are in `S_out`, some row of `S_out` carries `εM/4`.
  * Otherwise some heavy block (there are at most `k/h`) carries `εh/4`, so at
    least `εh/8` of its regular positions. The block is eligible (source §05,
    long periods), and `S = X_P ∩ {regular positions}` lies in `𝒮_ε(π)`.

In each case an avoided event of 4a or 4b makes `c_*` non-constant on the
labels of a subset of `X_P`. If `|X_P| < εk`, then
`|C_{¬β}(P) \ X_P| ≥ γk − εk`. ∎

**Corollary B′ (dense form).** Cut every row of `S_all(W)` and of `S_out(W)`
into consecutive **pieces**: a row of length below `2M` stays whole, and a longer
row is cut into pieces of length between `M` and `2M`. Each piece has length
between `δM − 1` and `2M`, its labels are distinct, and `W` has at most `2k`
pieces. Call `S ∈ 𝒮(W)` **dense** if some piece `ω` has `|S ∩ ω| ≥ (ε/4)|ω|`,
and `S ∈ 𝒮(π)` dense if `|S| ≥ εh/8`. Write `𝒮_dense` for these. If

```math
\log\max_W|\mathcal S_{\rm dense}(W)|\le\tfrac{\varepsilon\delta}{80}M,\qquad
\log\max_{\pi\ \text{of length}\ h}|\mathcal S_{\rm dense}(\pi)|\le\tfrac{\varepsilon}{128}h,
```

then the conclusion of Theorem B holds.

*Proof.* In family 4a, index the events by `(W, ω, S)` with `S` dense on the
piece `ω`. Such an event has probability `2^{1−|S∩ω|}` with
`|S ∩ ω| ≥ (ε/4)(δM − 1)`. The incident weight per label is then at most
`2k·T_glob·max|𝒮_dense(W)|·e^{−εδM/65}`, since the weight is `e^{−|S∩ω|/4}` and
`(ε/4)(δM − 1)/4 ≥ εδM/65` for large `M`. With the hypothesis this is
`exp(O(k^{2a} log³ k) − εδM/65 + εδM/80)`, again smaller than any power of `k`. Family 4b is unchanged. In the proof of Theorem B, replace "some row
carries" by an average over pieces. With no heavy label, the pieces partition
`P` and carry `|X_P| ≥ εk`, so some piece has density at least `ε ≥ ε/4`. With
a heavy label, if `|X_P ∩ S_out| ≥ εk/4`, the pieces of `S_out` (at most `k`
positions) give a piece of density at least `ε/4`. The block case is already
dense. ∎

So only traces that are dense somewhere, at density `ε/4` on at most `2M`
positions or `ε/8` on a pattern, have to be counted. A frozen set with no dense
trace has `|X_P| < εk` on every progression of `𝒫_long`. Then (II′) holds with
no splitting at all, and the question goes back to the sparse form of Door 1
(radar-2a's remark).

**Proposition E (a count is also necessary for the clique-bound class, at the scale `e^{O(k)}`).** Let
`c_*` be chosen by any criterion of the class 𝒞 of the keyed-local-lemma note
(Theorem A there: asymmetric LLL, Shearer, cluster expansion, Moser–Tardos,
variable LLL) over independent label bits. Suppose it certifies (II′_θ) on
`𝒫_long` together with the outer families. Then every label bit `v` satisfies

```math
\sum_{(W,S)\ni v}\mu_{W,S}<1 ,
```

where the sum runs over the distinct pairs (label word, realised `X_P`) of
progressions of `𝒫_long`. Here `μ_{W,S}` is the probability that `S` lies in one
class and leaves fewer than `θk` positions of that class. *Proof.* The bad event
of (II′_θ) at `P` depends only on `c_*` at the labels of `W`, and on `S = X_P`.
So it is one event per pair `(W, S)`. Theorem A of the keyed-local-lemma note
applies verbatim to it. ∎

So a randomly chosen `c₀` improves on the first moment of Proposition 5 of
`exact-door-one-condition` exactly by the **clustering** of dangerous
progressions on pairs `(W, S)`. Proposition 5 counts progressions (about
`N²`). Proposition E counts distinct pairs. With uniform bits,
`μ_{W,S} ≥ 2^{−k}`, so 𝒞 can absorb at most `e^{O(k)}` dangerous pairs per
label. That is `N^{o(1)}` on the scale of `k log k`.

**The gap between (B) and (E).** These two counts are not the same. Theorem B
**suffices** with `e^{o(M)}` dangerous traces per label word, and
`M = k^m ≪ k`. Proposition E **requires** at most `e^{O(k)}` dangerous pairs
per label. Between the two lies a range of clustering, from `e^{εM}` to
`e^{O(k)}` per label, in which a criterion of 𝒞 is neither shown to work nor
shown to fail. Q-S1b lives in that range, and above it.

## 3. (C) What (I′) costs

**Theorem C.** Assume `b > a`. Let `X` be any frozen set of keys `κ⁺`. There is a
label `L` and an integer interval `J_L` of length at least `q²/(80k²)` with the
following property. Let `T_L = {t : (L, t) ∈ X}`. If `T_L ∩ J_L` and
`J_L \ T_L` together have fewer than

```math
\rho_*=\frac{q}{240\,k^3\lambda\,(m_*+2)}-1,\qquad m_*=\lceil e^{3k^{1-b}}\rceil,
```

maximal runs, then the final colouring has a monochromatic progression with
probability `1 − o(1)`. Since `log λ = O(k^a log³ k)`, we have
`log ρ_* = log q − O(k^a log³ k + k^{1−b}) = (1 − o(1)) log q`.
The construction needs `q > k³λm_*`, which holds only for large `k`. At
`a = 49/100` the factor `log³ k` still wins at `k = 2^{1024}`, where
`log λ ≈ 3.1 log q`. By `k = 2^{4096}` the ratio is about `10^{−17}`, and the
gap of § 4 is `log R ≲ 2^{41}` against `log R ≳ 2^{2097}` (`verify.py`, check 4).

*Proof.* **The family of blocks.** Choose `r ∈ ℤ/q^{D−1}` such that, for every
`i < D`, `x̂_i` and `ỹ_i` of the positions `≡ r` lie at distance more than
`kλ/q` from every endpoint of `U` and `V`. As `n` ranges uniformly, each
coordinate fails with probability at most `|V|(2kλ/q + q^{−i}) + k²λ(2k/q + q^{−i})`,
which is `O(k⁴λ log k/q)`. A union bound over the `2D` coordinates leaves a good
`r`. Coordinates `i < D` of `n` depend only on `n mod q^{D−1}`. Put
`n_s = r + s q^{D−1}` (`s ∈ ℤ/q`). Then

```math
x_D(n_s)=x_D(r)+\tfrac sq,\qquad y_D(n_s)=\lambda x_D(n_s),
```

and the coordinates `i < D` do not move.

Choose a `U`-interval `J_U` whose image `λJ_U`, an arc of length `λH_x = H`,
lies in `{1/8 ≤ ỹ ≤ 1/4}`. Such an interval exists, because `aH mod 1` takes
every multiple of `H`. At most 18 `V`-intervals meet this arc, since their
widths are at least `H/16` there (source, mesh widths, `ρ ≥ 1/4`). So one of
them, `J_V`, meets it in an arc of length at least `H/18`. Its preimage `J′ ⊂ J_U`
has length at least `H_x/18`. Keep the `s` with `x_D(n_s)` in `J′`, at distance
more than `k/q` from its ends. There are at least `qH_x/20` of them. All the `n_s`
kept carry one label `L`.

For each kept `s`, let `P_s = {n_s + j : 0 ≤ j < k}` (step `d = 1`). Along
`P_s`, `x_i` moves by `j/q^i ≤ k/q` and `ỹ_i` by `jλ/q^i ≤ kλ/q`. By the choice of
`r` and of the margins, every position keeps the label `L`. So `P_s` is a
single-label block: `c₀` is constant on it, and it lies in `𝒫_short` with
`k_L = 0`. Write `A = ỹ(n_s)` and `w = λ(q^{−1}, …, q^{−D})`. Its bands are
`t_j = ⌊q²|A + jw|²⌋`. They lie in the two-sided window

```math
\bigl[t_0-kq\lambda(1+2/q)-1,\ t_0+kq\lambda(1+2/q)+2k^2\lambda^2\bigr],
```

because `|2jq²⟨A, w⟩| ≤ kqλ(1 + 2/q)`, where `A_1` may be negative, and
`j²q²|w|² ≤ 2k²λ²`. The window has length at most `2.01·kqλ` for large `k`.

**The starts are dense.** Here `t_0(s) = ⌊q²(C_* + ỹ_D(n_s)²)⌋` with `C_*`
fixed, and `ỹ_D` runs through an arithmetic progression of step `λ/q` across an
interval of length at least `H/20` inside `[1/8, 1/4]`. Consecutive starts differ
by at most `qλ`, and they sweep an interval `J_L` of length at least
`q²·(1/4)·H/20 = q²/(80k²)`. Two blocks whose windows are disjoint have
disjoint band sets, hence disjoint keys.

**Counting runs.** Suppose `T_L ∩ J_L` and `J_L \ T_L` have together fewer
than `ρ_*` maximal runs. Then some run meets `J_L` in an interval of length at
least `(m_* + 2)·3kqλ`. Trim `2kqλ` from both ends. The rest holds `m_*`
starts at spacing `3kqλ`, each available to within `qλ`. Each window reaches
at most `1.01·kqλ` on either side of its start, so it stays inside the run.
Two windows are disjoint, since `3kqλ − qλ > 2.01·kqλ`.

* If the run lies in `T_L`, one block is **saturated**: every key is frozen,
  and `c₁ = ¬c₀` on all of it. The block is monochromatic with probability 1.
* If the run lies outside `T_L`, the `m_*` blocks are **untouched** and
  key-disjoint. Each is monochromatic (colour `c₀`) when none of its at most
  `k` keys flips. So the probability that none is monochromatic is at most
  `(1 − (1−p)^k)^{m_*} ≤ exp(−m_* e^{−2pk}) ≤ exp(−e^{k^{1−b}}) → 0`.
  This uses `1 − p ≥ e^{−2p}` for `p ≤ 1/2`, and `pk = k^{1−b}`. ∎

So (C) is a necessary condition on the colouring itself, not only on the
template's certificate. It reads `T_L` on one label, and it holds for every
label this construction produces (any good `r`, any `J_U` with
`λJ_U ⊂ {1/8 ≤ ỹ ≤ 1/4}`). Every rule with fewer than `ρ_*` runs on such a
label therefore fails for `b > a`: threshold rules, unions of few band
intervals, rules with few polynomial pieces. Residue rules are not covered,
because a residue class has many runs; the algebraic-band-rules closure (moduli
up to `≈ q/(1536k³)`) treats them by another mechanism. (C) is the
interval-complexity counterpart of that closure.

## 4. (D) The gap

Suppose each `T_L` is a union of at most `R` intervals.

**Lemma D1 (Warren).** Then `log|𝒮(W)| = O(D log(kR))` and
`log|𝒮(π)| = O(D log(hR))`.

*Proof.* Progressions with label word `W` are points `(A, B) = (ỹ(n_0), ỹ(d))`
of `ℝ^{2D}`, with `ỹ_j = A + jB − m_j`. The carries `m_{j,i}` are fixed by the
signs of `A_i + jB_i − (z + 1/2)`, `|z| ≤ k + 1`. Membership of `(L_j, t_j)` in
`X` is fixed by the signs of `q²|ỹ_j|² − τ` at the `2R` ends `τ` of `T_{L_j}`.
That makes `s = O(k(R + Dk))` polynomials of degree at most 2 in `2D`
variables. Only finitely many points are realised, so each threshold can be
shifted by less than the smallest gap, making every sign strict without changing
any realised sign vector. By Warren's theorem (1968, Theorem 3) the complement of
`s ≥ n` real polynomial hypersurfaces of degree `≤ d` in `ℝ^n` has at most
`(4eds/n)^n` connected components. Each realised `X_P` is constant on a
component. The pattern case is the same, with parameters `(y, v) ∈ ℝ^{2D}` and
`h` positions. ∎

Theorem B then applies when `D log(kR) ≤ εh_0/C`, that is
`log R ≤ εL²/C − log k`. Theorem C requires `log R ≥ (1 − o(1)) log q ≥
(c/2) k^{1−a} log k`. These two ranges never meet.

Raising the cutoff does not close the gap. With `h_0 = Dk^σ`, the first family
needs `log T_glob = O(D² k^σ log k) = o(M)`, that is `σ < m − 2a < 1 − 2a`.
Theorem B then reaches `log R ≲ k^σ`, while Theorem C still demands
`log R ≳ k^{1−a}`, because `log λ = O(Dk^σ log k) = o(log q)`. Since
`σ < 1 − 2a < 1 − a`, the gap holds for every admissible `σ`.

## 5. What this says about the brief

* **The Weil route** is closed by S1a (`non-polynomial-bands`, radar-cc): along
  generic rich progressions the bands are not polynomial in `j`, and the
  windows are far too short anyway.
* **Correlating with `c₀`** is available at no cost (A). By (B) and (E), it
  reduces Door 1 on the rich side to a count. Dangerous progressions must
  cluster on `e^{o(M)}` pairs `(label word, X_P)` and on `e^{o(h)}` pattern
  subsets. Below that count, (II′) is free, for any density of `X`.
* **(I′) pushes the other way.** By (C), every working `X` alternates at least
  `q^{1−o(1)}` times on the band line of a label. By (D), the only general tool
  for counting realised subsets cannot handle such a rule.

## 6. Open question left

**(Q-S1b)** Is there a frozen set `X` passing (I′) for some `b > a`, hence with
`q^{1−o(1)}` alternations per label by (C), whose **dangerous** realised
subsets satisfy the hypothesis of Theorem B? Equivalently: do the dangerous
progressions with one label word cluster on `e^{o(M)}` traces? A negative
answer at the scale of Proposition E (more than `e^{O(k)}` dangerous pairs
through some label) closes every criterion of 𝒞. A negative answer only
between `e^{εM}` and `e^{O(k)}` leaves 𝒞 open. A rule whose alternations are
invisible from the progressions would answer yes. Such a rule, for instance, would depend on bands only
through a quantity constant along each label word, while still splitting
single-label blocks.

Heuristically the answer is no. Along a long-period eligible pattern, moving `y`
inside its box shifts the band at position `z` by `2q²⟨ỹ_z, δ⟩`, a different
linear form at each position. A rule with `q^{1−o(1)}` alternations then flips the
positions one at a time, which suggests `q^{1−o(1)} ≫ e^{εh_0}` realised subsets.
This is not a proof: a lower bound on realised **dangerous** subsets (those with
`|S| ≥ εh/8`) would be needed, and for a sparse `X` these are large deviations.
A proof of that lower bound closes S1b. A rule that avoids it opens Door 1 on the
rich side.

**Sauer–Shelah gives nothing more than Warren here.** If the traces
`{X_P : P ∼ W}` on a row have VC dimension `d`, then they number at most
`(eM/d)^d`. That is enough for Theorem B only when `d ≪ M/log M`. The
VC dimension of a family cut out by `2R` sign conditions of quadratics in `2D`
parameters is `O(D log(kR))` (the same arrangement count), that is
`O(D log q) = O(ck log k)` once `R ≥ q^{1−o(1)}`, and that is far above `M`. A
heuristic in the other direction: in `q²|A + jB − m_j|²`, the step `B` acts like
a frequency, as in the family `x ↦ sign sin(θx)`, which shatters arbitrarily
large sets. A rule with `q^{1−o(1)}` alternations should therefore shatter
about `log q` positions per direction of `B`, which gives `d` of order
`D log q ≫ M`. Making this rigorous for the **dangerous** traces is the lower
bound that would close S1b.

## What `verify.py` checks

1. **The core of Theorem C, exhaustively** on small integer lines. Starts are
   placed at spacing `≤ g < W`, windows are two-sided (`[s − W, s + W]`), and
   rules are unions of intervals. Check 1b replays the referee's control: at
   `q = 10007`, `D = 3`, `λ = 5`, `k = 8`, bands fall below `t_0`, so the
   one-sided window fails, while the two-sided window holds on 300 exact starts. With fewer than the stated number of runs there is always a
   saturated window or `m` disjoint untouched windows. Control: a rule
   alternating at scale `< W/2` leaves neither.
2. **The local-lemma inequalities of Theorem B**: `2^{1−l} ≤ e^{−l/4−2lι}` for
   `l ≥ 4`, `ι ≤ 1/10`, exactly on a grid; the controls `l = 2` and `ι = 1/4`
   are rejected.
3. **Lemma D1's count** on a toy: realised `X`-subsets of random quadratic
   families stay below Warren's bound.
4. **The exponent ledger** (in logarithms) at `k = 2^{4096}`, `a = 49/100`,
   `c = 1/9`, `b = 1`, for `σ` on a grid below `1 − 2a`. It compares Theorem B's
   reach `log R ≲ k^σ` with Theorem C's demand `log ρ_*`, and the cost
   `k^{2a} log³ k` of (A) with `k log k`. It also prints `log λ / log q` at
   `k = 2^{1024}` and `2^{4096}`.
5. **Provenance**: MANIFEST hashes.

## What is not claimed

* No admissible `X` and no bound on `c`. Theorem B gives (II′) only for rules
  that (D) shows Warren cannot certify when they pass (I′).
* Theorem C is a necessary condition for the colouring. It is not a closure of
  every rule: rules with `q^{1−o(1)}` alternations per label are untouched by it.
* Proposition E concerns criteria of the class 𝒞 with random label bits. A
  deterministic `c₀` escapes it, and must then split the dangerous
  progressions by itself.
