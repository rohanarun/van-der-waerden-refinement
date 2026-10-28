# The exact form of Door 1: one condition, two thresholds

**Status:** structural research, with proofs. It contains three things. (1) The
exact condition that a frozen key set `X` must meet on rich progressions,
which is weaker than the literal (II), and a proof that it suffices. It is
the same condition as (I), with a different threshold. The proof also needs
a clause on case (i) that the track's (I) + (II) left out; it is mild. (2) A re-reading of
the existing closures under it. One closure falls (dense rules); every other
holds. (3) Two structural facts. The reduction puts no ceiling on `b`, so
"every `c < 1/4`" is the choice `b = 1` and not a ceiling. And a key set
that splits every progression is already a coloring of `ℤ/N` by itself. No
new bound is claimed, and no admissible `X` is known.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96` (through
`pr/exits-past-1-8`, `83b872a`).

**Sources:** `short-period-runs-proof.md` (case (ii)). The rich-side
estimate is Theorem 9 of the trust-reduction note
`trust-reduction/2026-10-26-ChaloupeMusic-source-only-1-8` (radar-3a, commit
`6494b2c`, not in this tree), together with its companion `source-only-1-16`
(Lemma 3, multiplicity two; Theorem 6, the dichotomy; Theorem 8, the non-rich
progressions). The frozen-key reduction and conditions (I), (II) are from the
`structured-flips` track (see `NOTICE.md`).

## Reproduce

```sh
python3 -B auto-research/structured-flips/2026-10-26-ChaloupeMusic-exact-door-one-condition/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and a JSON
summary equal to `RESULT.json`. Standard library only, exact rationals, a few
seconds.

## Setting

As in the track: `c₀` is the outer coloring (through labels), `κ(n)` the key
of `n`, and `X` a fixed set of keys. The coloring is `c₁ = c₀ ⊕ 1_X`. Keys
outside `X` receive iid Bernoulli(`p`) flips, with `p = k^{−b}`. Keys in `X`
are **frozen**: they are flipped once and receive no random flip. For a
progression `P` (`k` positions) and a target color `β`, write

* `C_β(P)` for the positions of `P` with `c₀ = β`, and `X_P` for the
  positions of `P` whose key is in `X`;
* `D_β(P) = {c₁ ≠ β} ∩ P = C_{¬β}(P) Δ X_P`, the positions that still need a
  random flip to reach `β`.

A key occupies at most two positions of a progression (Lemma 3 of
`source-only-1-16`; four in the source). Counts in **positions** and in
**keys** therefore differ by a factor of at most 2. Each statement below says
which count it uses.

## 1. The exact event

**Proposition 1.** `P` is monochromatic in `β` under the final coloring
exactly when (a), (b) and (c) all hold:

* (a) no key carries positions of both `c₁`-colors on `P`;
* (b) no position of `D_β(P)` has its key in `X`;
* (c) every key of `D_β(P)` receives its random flip, and every other key of
  `P` outside `X` does not.

If (a) or (b) fails, the probability is `0`. Otherwise it is
`p^{#keys(D_β)} (1−p)^{#keys(P \ D_β) \ X}`.

*Proof.* Each position must end at `β`. A position of a frozen key ends at
`c₁`, so it must already be at `β`: this is (b). A free key flips all its
positions together, so its positions in `D_β` and outside `D_β` cannot both
be fixed: this is (a). The rest is (c). ∎

**What is dangerous.** By (b), the event is empty as soon as `X_P` meets
both color classes of `c₀`. Indeed, a frozen key in `C_β` has `c₁ ≠ β` and
blocks `β`, and a frozen key in `C_{¬β}` blocks `¬β` in the same way. The
event is also empty when one key carries both `c₀`-colors. Otherwise `X_P`
lies inside **one** class `C_{¬β}`, and the cost is
`p^{#keys(C_{¬β} \ X_P)}`. The danger is therefore that `X_P` covers almost
all of one class, the minority class **or the majority one**. `X_P` equal to
the majority class turns `P` monochromatic in the minority color with
probability `(1−p)^{…}`, close to `1` (check 2 of `verify.py`). The remark of
the single-label lenses note (`2026-10-20-…-single-label-lenses`, "On (II)")
already had this form; the remark of B3 in the keyed-local-lemma note
("the harmful event is `X ∩ κ(P)` = the minority side") misses the
majority case. The referee found the same correction in its review of B3.

## 2. The condition, and why it suffices

Theorem 6 of `source-only-1-16` splits the progressions into rich and
non-rich ones. Theorem 8 splits the non-rich ones into case (i)
(`k_L ≥ δ_s k`) and case (ii). Non-rich progressions have at most
`T_key = exp(6 log q + O(D log k)) = e^{o(k log k)}` key words. Case (ii)
words with their codes number `e^{H}`, where `H = 6 log q + O(D log³ k)`.

**(II′_θ)**, for every rich progression `P` and each `β`: either `X_P` meets
`C_β(P)`, or `|C_{¬β}(P) \ X_P| ≥ θk` **positions**.

**(I′_η)**, for every case (i) progression `P` and each `β`: either `X_P`
meets `C_β(P)`, or `|C_{¬β}(P) \ X_P| ≥ ηk` **positions**, for some fixed
`η > 0`.

**(I′_w)**, for every case (ii) progression `P` and each `β`: either `X_P`
meets `C_β(P)`, or `C_{¬β}(P) \ X_P` carries at least `w` **keys**, with
`w b log k ≥ (1+δ)H`.

The three conditions are the same statement, "split, or leave enough to
flip". Only the threshold changes, and it is set by the entropy of each
family: `θk` positions against the `N²` rich progressions, any fixed
fraction against the `e^{o(k log k)}` case (i) words, and `w` keys against
the `e^{H}` case (ii) words with their codes.

**A clause the track's (I) + (II) left out.** The literal (II) speaks of
rich progressions and (I) of case (ii). Nothing constrained `X` on case (i),
where `X` could saturate the positions that must flip. (I′_η) is that
missing clause. It is mild: any fixed `η` works, and the literal (II)
extended to case (i) gives it (Corollary 3).

**Theorem 2.** Fix any `b > 0`, any key set `X` satisfying (II′_θ),
(I′_η) and (I′_w), and the rest of the region of `source-only-1-8`: `a < m/2 < 1/2`,
together with the conditions on `ε, ε_r, δ, δ_s`, which only concern `c₀`.
If `2c < θb`, the probability that some progression is monochromatic tends
to `0`. The conditions `b < a` and `a + b < 1` are not needed, and there is
no condition on the density of `X`.

*Proof.* Split the pairs `(P, β)` with a non-empty event (Proposition 1) into
four groups.

* *Rich progressions.* By (II′_θ), `D_β(P) = C_{¬β}(P) \ X_P` has at least
  `θk` positions, and none of its keys is in `X`. Theorem 9 of
  `source-only-1-8` uses three things only: a set `P₁` of at least `γk`
  "flipped" positions; Lemma 3 (`|P₁| = 2r + s`); and Lemmas A\* and C\*,
  which count key sets and progressions by their discrete data (boxes,
  return structure, digit rank) and never read a color. Replace `c₀` by `c₁`
  in it, `P₁` by `D_β(P)`, and `γ` by `θ` (the threshold of (II′); the
  per-rank split `θ_R` of Theorem 9 is unchanged, now with `0 < θ_R < θ`).
  Each certificate is a set of keys
  of `D_β(P)`, so these keys are free, and "all of them flipped" has
  probability `p^{⌈θ_R k⌉}` or `p^{|F|}`, exactly as there. Every step then
  goes through with `θ` in place of `γ`, and the total is
  `exp(−μk log k + o(k log k))`, with `μ = (θb − 2c)/2`.
* *Case (i).* As in Theorem 8: a non-empty event lies in "at least
  `x = ⌈ηk/2⌉` distinct keys of the key word are flipped", of probability at
  most `C(k, x)p^x ≤ (ekp/x)^x = exp(−Ω(k log k))` for every `b > 0`, against
  `2T_key = e^{o(k log k)}` words.
* *Case (ii).* The key word and the code fix the keys, hence `X_P`, and they
  fix `C_β`. By (I′_w), each non-empty event has probability at most `p^w`.
  The total is at most `2e^{H} p^{w} = exp(H − w b log k) → 0`.
* *Empty events* (split by `X`, or carrying a key with both colors) cost
  nothing.

These events cover every monochromatic progression, and no independence is
used. ∎

**Corollary 3.**
1. The literal (II) (at most `εk` keys of `X` on each rich `P`), together
   with `γ`-richness of `c₀`, gives (II′_θ) on the rich progressions with
   `θ = γ − 2ε`. A key occupies at most two positions, so `εk` keys remove at
   most `2εk` positions from `C_{¬β}`. The same bound on case (i)
   progressions gives (I′_η) with `η = (1/2 − ε)δ_s − 2ε`, by Proposition 5.3
   of `source-only-1-16`, if `ε` is small.
2. The (I) of the track (`X` meets the dominant color of each case (ii)
   word, and at least `ω(H/(b log k))` dominant keys stay outside `X`) gives
   (I′_w). Target `β` = dominant is blocked by the frozen dominant key. For
   target `β` = minority, either `X` also meets the minority (blocked), or
   `C_{¬β} \ X_P` is the free part of the dominant side.
3. With `θ → 1/2` and `b = 1`, every `c < 1/4`. This is the team's statement,
   now proved from Theorem 9, with (II′) in place of (II) and the factor 2
   of the multiplicity made explicit.

## 3. Two structural facts

**Proposition 4 (no ceiling on `b`, and the split regime is the whole
problem).**
1. Theorem 2 holds for every `b > 0`. The ceiling `1/4` of the synthesis
   comes from taking `b = 1`. With iid flips only, `b` was capped by case
   (ii) (`b < a`, `a + b < 1`). Under (I′) those constraints disappear, and
   `b` only enters through `2c < θb`. A larger `b` makes (I′_w) easier
   (`w ∝ H/(b log k)`), and it leaves (II′_θ) unchanged. This answers the
   referee's point (p1) on the keyed-local-lemma note: `b ≤ 1` is **not** a
   consequence of the reduction. Every limit on `c` must come from the
   existence of `X`.
2. As `b → ∞` (`p = 0`), the two conditions become one: no progression of
   `ℤ/N` is monochromatic under `c₁`. If `X` **splits** every progression
   (`X_P` meets both `c₀`-classes), `c₁` is a coloring of `ℤ/N` without a
   monochromatic `k`-term progression, with no randomness at all. That
   would give `W(k) > N = k^{ck}` for the chosen `c`, directly. The
   template then contributes nothing: the all-split regime **is** the van
   der Waerden problem. The same circularity holds for the first family
   beyond `a = 1/2` (radar-dd).
3. `θ ≤ 1/2` as soon as one rich `P` has `X_P = ∅`, since its smaller class
   has at most `k/2` positions. Going past `θ = 1/2` therefore requires `X`
   to meet every rich progression, and then to split each one it does not
   leave balanced.

So the template interpolates between iid flips (`X = ∅`, `θ = γ`, `b < a`)
and a deterministic coloring (`b = ∞`, every `P` split). Door 1 asks for a
point in between.

**Proposition 5 (first moment of a random-like `X`).** Let `X` be random,
each key independently with probability `ρ = k^{−b_X}`, `0 ≤ b_X ≤ 1`, and
let `𝓕` be a family of rich progressions in which no key carries both
`c₀`-colors. Then, for each `P ∈ 𝓕` and the majority color `β`,
`Pr[(II′_θ) fails at (P, β)] ≥ ρ^{(1/2−θ)k+1} (1−ρ)^k`. If `|𝓕| = N^{2−o(1)}`,
the expected number of failures tends to infinity as soon as
`2c > (1/2 − θ) b_X`. This is a first moment only: it does not show that a
random `X` fails with high probability. `X` carries only `|𝒦| = N^{o(1)}`
independent bits for `N²` strongly correlated events (a subfamily with
pairwise disjoint keys has `N^{o(1)}` members), so no second moment comes
for free.

*Proof.* `C_{¬β}` is the minority class, with at most `k/2` positions. The
failure event contains the following one: `X` contains keys covering all
but `⌊θk⌋` positions of the minority class (at most `k/2 − θk + 1` keys),
and `X` contains no key of the majority class (at most `k` keys). Here
`(1−ρ)^k = e^{−k^{1−b_X}} = e^{−o(k log k)}` when `b_X > 0`, and `e^{−1}`
when `b_X = 1`. ∎

The family exists. A progression with no repeated box has distinct keys.
By Lemma R1 of `source-only-1-8`, a return forces
`|h y(d) − t| ≤ 2H` in every coordinate for some `h ≤ k`. That is a set of
steps of density at most `k(4H)^D = o(1)`, since `4kH < 1`. And
non-rich progressions are those with a short-period label word
(Theorem 6), also `o(N²)`.

Combined with `2c < θb`: the first moment of a random `X` does not certify
(II′) beyond `c < b·b_X / (4(b + b_X))`, whose supremum over `b` is
`b_X / 4 ≤ 1/4`. For `b_X = 0` (dense, constant density), each failure has
probability `e^{−O(k)} ≫ N^{−2}`: the first moment of a random dense `X`
certifies nothing for any `c > 0`. For a random `X` dense enough to satisfy
(I) by its own first moment, `b_X ≤ a` (C1, the random hitting cost
`~ log q / k = k^{−a+o(1)}`), and the first moment certifies nothing beyond
`c < a/4 < 1/8`. This is the remark of radar-dd's annex ("Gowers"), in the
same first-moment form, now with (II′) in place of (II). Under the uniform laws of A2, the result is
the bound of A2, with `1/2 − θ` in place of `ε`.

## 4. The closures, re-read under (II′)

| closure | uses the literal (II)? | under (II′) |
|---|---|---|
| Gowers remark (random `X`, radar-dd annex, synthesis) | yes | **holds**, in its first-moment form (Proposition 5): nothing certified beyond `c < a/4` |
| N2a, single-label lenses (PR #16): Theorem A, Proposition B, Lemma R | no, they concern (I) | **holds**. Its remark "On (II)" already had the exact form. Its bound `c < γ min(b_X, b)/2` for a random-like rule is an upper bound, and Proposition 5 refines it to `γ b b_X/(2(b + b_X))` |
| N2b, algebraic band rules (PR #16) | no, it concerns (I) (saturated or untouched blocks) | **holds** |
| N3, template ceilings (PR #16) | no. Its templates are oblivious perturbations, and their rich side is `Pr ≥ p^{k/2}` | **holds**. Its frame "`c > 1/8` needs `H ≪ k^{1/2}`" assumes that flips pay for the structured events, which Door 1 escapes by freezing; N3 already says so |
| P1a, AP-free frozen sets (`6426cad`): Theorems 2 and 3, Proposition 4 | it closes mechanisms whose purpose is the literal (II) (`\|X ∩ P\| ≤ r_ℓ(k)`), by their incompatibility with (I) | **holds**. The incompatibility does not read (II). These mechanisms would give (II), hence (II′), and they still fail (I). Nothing here extends P1a's window under (II′); the referee rejected that claim |
| P1b A1 (clique bound) | no | **holds** |
| P1b A2 (uniform laws, `c ≤ βb/(4(β+b))`) | yes (`μ(B_P) ≥ ρ^{εk+1}`) | **holds**, with `ε → 1/2 − θ`: the bad event of (II′) has `μ ≥ ρ^{(1/2−θ)k+1}(1−ρ)^k`, which gives the same bound (Proposition 5). Point (p1) remains: it is `≤ 1/8` only for `b ≤ 1`, and Proposition 4 says that nothing forces `b ≤ 1` |
| P1b A3 (beyond `1/8`, a deterministic `S` does Door 1 up to rich exceptions) | yes, (II′) of A3: `> εk` keys in `S` | **holds**, with its exception event read as "`S_P` inside one class, covering all but `θk`" (same product of margins) |
| P1b B1 (dense rules fail (II)) | yes | **falls.** A dense `X` puts many keys on rich progressions but splits most of them, and splitting is harmless. See § 5 |
| P1b B2 (two moments of any rule are those of a random set) | no | **holds**. (II′) needs correlations of order `≥ 3` too |
| P1b B3 (squares family) | its remark | **the proof holds.** Its remark is corrected in § 1: full saturation of a rich `P` (`X_P = P`) is harmless because it splits `P`. The harmful event is `X_P` inside one class, covering all but `θk` of it |
| P1, P3 (radar-99, PR #14), LL (radar-63) | no, they concern iid flips on case (ii) | **hold**. Door 1 is the exit they leave open |

## 5. What (II′) reopens, and why no candidate follows

The only closure that falls is B1: dense rules. Under (II′), a dense or
heavy `X` is allowed on a rich progression **provided it splits it**. Three
ways to use this were examined.

1. **Split everything.** Circular (Proposition 4.2): it is a full van der
   Waerden coloring of `ℤ/N`.
2. **Dense random-like.** Its first moment certifies nothing for any
   `c > 0` (Proposition 5 at `b_X = 0`). A random set misses one class of `e^{−O(k)}`-many rich
   progressions out of `N²`. To beat the first moment, a dense `X` would
   need to hit **both** classes of all but `N^{o(1)}` rich progressions.
   That is a deterministic transversal of the `2N^{2}` color classes, each
   of size `~k/2`, of the generic progressions, and any such transversal is
   anti-random at order `≥ 3` (B2).
3. **Split-repair (alteration).** Start from a sparse `X` that satisfies (I)
   and repair each violating rich `P` by adding one key of its other class.
   Heuristic obstacle, not a proof: the repair key lies on about
   `k·#(near-violations)/|𝒦|` other progressions with `|𝒦| = N^{o(1)}`, half
   of them in the same class, and each of those it pushes one step closer
   to a violation. When violations are many (`2c > (1/2−θ)b_X`), so are
   near-violations, and the repairs cascade. The same counting appears in
   P1b's clique bound, which applies to any certificate that reads label
   colors as independent variables.

**Answer to the brief's question 3.** (II′) is a real relaxation: it admits
`X` that put many keys on a rich progression, if they split it. It changes
the closure ledger in one place (B1). It does not change what the first moment of a random-like `X`
certifies (`b_X/4`, Proposition 5), and its extreme case
is circular. The open problem of Door 1, stated exactly, is now this. Find
`X` satisfying (I′_η) and (I′_w) such that every rich progression is either split by
`X`, or has `X_P` inside one class leaving at least `θk` positions, with
`θ > 2c/b`. No candidate is proposed.

## What `verify.py` checks

1. **Proposition 1, exhaustively** on 400 random small instances (`k ≤ 9`,
   keys of multiplicity `≤ 2`, random `c₀`, random `X`, `p = 1/5`). The
   probability of monochromatic in `β` is obtained by enumerating all
   flips, and it equals the formula exactly (Fractions).
2. **The majority case** (the referee's correction): an instance where `X_P`
   is the majority class gives probability `(1−p)^{…} > 0` of monochromatic
   in the minority color, a "minority-only" criterion misses it, and the
   exact criterion of § 1 catches it.
3. **Splitting**: on every instance where `X_P` meets both classes, the
   enumerated probability is `0`, for both targets.
4. **Corollary 3.1**: on random instances with at most `εk` keys of `X` and
   a `γ`-balanced `c₀`, `|C_{¬β} \ X_P| ≥ (γ − 2ε)k` holds whenever `X_P`
   lies in `C_{¬β}`. Control: with `γ − ε` instead of `γ − 2ε` (keys read as
   positions), a multiplicity-two counterexample exists.
5. **Proposition 5's lower bound**: for small `k`, the exact probability
   (over a random `X`) that (II′_θ) fails at the majority target is at least
   `ρ^{(1/2−θ)k+1}(1−ρ)^k`.
6. **Exponents**: `θb/2` at `θ = 1/2 − 1/100`, `b = 1` is below `1/4`; the
   optimum `b·b_X/(4(b+b_X))` and its supremum `b_X/4`; at `b_X = a = 49/100`
   it stays below `1/8` for every `b` tested (up to `10^6`).
7. **Negative controls**, each required to fail: the event formula without
   condition (b); the cost `p^{#keys(C_{¬β}) − |X ∩ P|}` read in positions;
   the "minority-only" harmful event.
8. **Provenance**: MANIFEST hashes; summary equal to `RESULT.json`.

## What is not claimed

* No admissible `X`, and no new bound on `c`.
* Theorem 2 relies on Theorem 9 of `source-only-1-8` and on Theorems 6 and 8
  of `source-only-1-16` (radar-3a, refereed publishable, not in this tree),
  and on the source lemmas they rely on. The replacement `c₀ → c₁` in
  Theorem 9 is checked line by line in the proof above, not mechanically.
* The `o(N²)` count of progressions with a repeated box or a non-rich word,
  in Proposition 5, is a sketch from R1 and Theorem 6.
* § 5.2 and § 5.3 are obstacles, not theorems. Only Proposition 4.2 (the
  all-split circularity) and Proposition 5 (the random first moment, an
  expectation and not a high-probability failure) are proved.
