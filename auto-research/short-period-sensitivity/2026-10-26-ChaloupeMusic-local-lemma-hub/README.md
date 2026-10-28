# The local lemma over iid flips still needs `b < a`, and `R` never mattered

**Status:** negative result (research note), with proofs and exact finite
checks. No new bound is claimed. It extends
`2026-10-20-ChaloupeMusic-single-label-obstructions` (P1–P3) from union
bounds to local lemmas, and says exactly which local lemmas it covers.

**Base commit:** `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`, plus the three
earlier notes of this track.

**Sources:** the construction, meshes, keys and flips of OpenAI,
*Quantitative Superexponential Bounds for van der Waerden Numbers*, pinned
in `source-manifest.json` (Sections 2 and 6), in the notation of
`single-label-obstructions` (Setting, Lemmas A–D).

## Reproduce

```sh
python3 -B auto-research/short-period-sensitivity/2026-10-26-ChaloupeMusic-local-lemma-hub/verify.py
```

Expected: exit code 0, last line `Test passé : all checks pass`, and the JSON
summary equal to `RESULT.json`. It takes about two seconds and uses only the
standard library.

## Question

P1 and P3 show that every sub-prescription union bound over iid flips needs
`b < a` (inequality B) and `a + b < 1` (inequality R). Their `K` events are
independent, so they say nothing against a local lemma. Can a local lemma
over the same flips relax B or R?

## Answer

1. **B survives every local lemma that reads only the dependency structure
   and the probabilities of the canonical events** (Theorem 1). One key lies
   in `E ≈ q/(64k³λ)` single-label progressions. That is enough, whether the
   criterion reads a dependency graph (Shearer, asymmetric, lopsided, cluster
   expansion) or the event–variable incidence (Moser–Tardos, Kolipaka–Szegedy,
   the variable-version bound of He, Li, Liu, Wang and Xia).
2. **Nothing more can be closed for "the local lemma" in general**
   (Propositions 2 and 3). If the events may be re-chosen, a refined family
   passes the test exactly when `P_p(no monochromatic progression) > 0`, and
   a cover family contains door 1 (structured flips). Beyond the canonical
   family, the question is no longer about the local lemma.
3. **R does not matter for `c`** (Section R). Under F and B, `a + b < 2a < 1`
   holds anyway. Whatever a local lemma does to R, `sup c = 1/8`: the
   binding-lever row "drop R only" applies unchanged. No edge between the P3
   events and the rest needs to be found.

## The canonical family

Fix an outer coloring `c*`. For every `k`-term progression `P` and color `v`,
the **canonical event** `B_{P,v}` is "`P` is monochromatic in `v`". It is
determined by the flips of the keys `κ(P)`, its natural variable set. A
local lemma over the flips, in the usual form, takes these events as they are.

Two kinds of criteria:

* **graph-only:** the input is a graph `G` on the events and their
  probabilities, and the criterion is valid for every probability space in
  which `G` is a lopsidependency graph. Every such criterion is implied by
  Shearer's, so it fails when the probabilities lie outside Shearer's region
  for `G`.
* **variable-only:** the input is the event–variable incidence and the
  probabilities, and the criterion is valid for every system of events
  determined by independent variables with that incidence. This is the
  setting of Moser–Tardos. Its exact region can be strictly larger than
  Shearer's when the incidence has cycles (Kolipaka–Szegedy; He–Li–Liu–Wang–Xia
  2017), and ours has cycles. So it needs its own counter-model.

## Lemma H (a hub)

Assume `λ ≤ q/(400k³)` and `D ≥ 2`, and set `E = ⌊q/(64k³λ)⌋`. There is
`n_0 = q^{D−1}m` such that the `E` progressions

```
P_e = { n_0 + q^{D−1} j e : 0 ≤ j < k },    1 ≤ e ≤ E,
```

all stay inside the full label of `n_0`, each has `k` distinct keys, all
contain `κ_0 = κ(n_0)`, and their key sets are pairwise distinct.

*Proof.* Take `r = 0` in Lemma A. For `i < D`, `x_i` and `y_i` vanish along
every `P_e`. In coordinate `D`, `x_D = (m + je)/q` and `y_D = λ(m + je)/q`
mod 1, as long as there is no wrap.

* *Choice of `m`.* The `U` cells are `[t, t+1)·H/λ`. As `m` runs through the
  left half of cell `t`, `y_D` runs through `[t/k², t/k² + 1/(2k²))` mod 1,
  in steps `λ/q ≤ H/(400k)`. Choose `t` with this range inside
  `[1/8 + H, 3/8 − H]`. A `V` cell meeting that range either lies in
  `{1/8 ≤ |Y| ≤ 3/8}`, with length at least `H/32` (Lemma B), or sticks out
  of it, with length greater than `H`. The range, of length `H/2`, therefore
  contains at most 17 boundaries of `V`, and a gap of length at least `H/36`
  between two of them. Its left part, of length at least `H/36 − H/64 > H/100`,
  contains some `y_D(m)`.
* *One label.* `P_E` sweeps `x_D` over `(k−1)E/q < (H/λ)/64`, less than half
  a `U` cell, and `y_D` over `λ(k−1)E/q < H/64`, inside the gap. Every `P_e`
  sweeps a sub-range of these, so every `U` and `V` index stays that of `n_0`.
* *Keys.* `s = q·y_D(n_0) = λm mod q` is an integer at least `q/8`, and
  `f(n_0 + q^{D−1}je) = (s + jλe)²` exactly. Distinct values of `je` give
  distinct integers `s + jλe ≥ q/8`, hence distinct squares, hence distinct
  bands. So each `P_e` has `k` distinct keys, the one at `j = 0` is `κ_0`,
  and the smallest band after `s²`, namely `(s + λe)²`, tells `e` apart. ∎

The outer color `c*` is constant on all `kE` points of the star, since they
share one full label. Call it `v`. Then

* `D_e = B_{P_e, v}` = "every key of `P_e` unflipped", with probability `x = (1−p)^k`;
* `I_e = B_{P_e, 1−v}` = "every key of `P_e` flipped", with probability `y = p^k`.

For all `e, e′`, `D_e ∩ I_{e′} = ∅`: they disagree on `κ_0`.

## Theorem 1

Assume `λ ≤ q/(400k³)`, `D ≥ 2`, `p ≤ 1/2`. For every outer coloring `c*`:

1. **Variable-only.** If `E(1−p)^k ≥ 1`, no variable-only criterion applied
   to the canonical family concludes.
2. **Graph-only.** If `E(1−p)^k ≥ k ln(1/p) + ln 2`, no graph-only criterion
   applied to the canonical family concludes, whatever valid lopsidependency
   graph it is given.

Consequently either kind of criterion can conclude only if

```
k(p + p²) > ln E − ln(k ln(1/p) + ln 2),    ln E ≥ ln q − ln λ − 3 ln k − ln 67.
```

The last bound uses `⌊x⌋ ≥ 0.96x` for `x = q/(64k³λ) ≥ 6.25`.

On the exponent scale (`ln q ≈ c k^{1−a} ln k`, `ln λ = k^{a+o(1)}`,
`pk = k^{1−b}`, `a < 1/2`), this is **`b < a`**, strict as in P1.

*Proof of 1.* Build a variable model with the same incidence and the same
probabilities. Let the variable of `κ_0` be uniform on `[0, 1)`. Let `D_e` be
"it lies in `I_e`", where `I_1, …, I_E` are intervals of length `x` that cover
`[0, 1)`; this is possible since `Ex ≥ 1`. Each `D_e` is then determined by
`κ_0 ∈ κ(P_e)`, as the incidence allows. Realise every other event with its
own probability on any one of its variables. Some `D_e` always occurs, so
the model avoids nothing, and a valid variable-only criterion cannot
conclude on this input.

*Proof of 2.* In any probability space, two disjoint events `A`, `B` of
positive probability satisfy `P(A | B̄) = P(A)/(1 − P(B)) > P(A)`. So every
valid lopsidependency graph `G` joins every `D_e` to every `I_{e′}`. The
subgraph that `G` induces on the star contains `K_{E,E}`. Shearer's region
shrinks when edges are added and when one passes to an induced subgraph, so
it is enough that the star lies outside the region of `K_{E,E}`. The
independence polynomial of `K_{E,E}` gives

```
Z(−p) = (1 − x)^E + (1 − y)^E − 1 ≤ e^{−Ex} − Ey/2,
```

using `1 − e^{−t} ≥ t/2` for `t = Ey ≤ 1`. This is `≤ 0` as soon as
`Ex ≥ ln(2/(Ey))`, which follows from `Ex ≥ k ln(1/p) + ln 2`. If instead
`Ey > 1`, then `Z ≤ e^{−Ex} + e^{−1} − 1 < 0` directly, since `Ex ≥ ln 2`. Outside
Shearer's region there is a space with dependency graph `K_{E,E}` on these
events in which they cannot all be avoided (Shearer 1985). Extending it by
the other events, independently and with their probabilities, gives a space
for which `G` is valid and which avoids nothing. ∎

The theorem is about the canonical family only. Splitting its events can
help: the disjointified pieces of `D_1, …, D_E` have total mass
`P(∪ D_e) < 1` instead of `Ex`. Proposition 2 shows how far this goes.

### Why this is not P1 again

P1 needs many progressions with **disjoint** key sets. A local lemma ignores
those, so here the progressions must **share** a key. The obstruction then
loses P3's box-word factor `(k²/2 − 4)^{D−1}`: every single-label
progression through a key has that key's `V` word. What remains is the
`ln q` term, which is B.

## Proposition 2 (refined families are complete)

Let a local lemma use any events, each contained in one canonical event, that
together cover them. Take the canonical events in any order and replace each
by its part that none of the earlier ones covers. These pieces are disjoint,
their total mass is `P_p(some monochromatic progression)`, and they pass
Shearer's test even for the complete graph as soon as this is below 1. So a
refined family passes exactly when `P_p(no monochromatic progression) > 0`.
Since `0 < p < 1` and the space is finite, that holds exactly when some flip
assignment is good. No impossibility statement about refined families can
therefore be weaker than "no good flip assignment exists". The single-label
family has good assignments (one flip per progression suffices), so
Theorem 1 is about the canonical local lemma, not about existence.

## Proposition 3 (cover families contain door 1)

Let a local lemma use **covers**, i.e. events that contain canonical events,
as union bounds do. Suppose a set `X` of keys satisfies door 1: freezing the
keys of `X` as flipped and flipping the others iid with probability `p`, a
sub-prescription union bound totals `T < 1`. Then the following family
passes Shearer's test over iid flips of **all** keys:

* for each `κ ∈ X`, the single-key event `{E_κ = 0}`, of probability `1 − p`;
* the `T`-family, read as sub-prescriptions of keys outside `X`.

*Proof.* A canonical event that prescribes `0` on some `κ ∈ X` lies in
`{E_κ = 0}`. Any other one prescribes `1` on all of `X ∩ κ(P)`, so it lies
in the door-1 sub-prescription of the same progression and color. The
single-key events have pairwise disjoint variables, and none of them meets
the variables of the `T`-family. The dependency graph is therefore a union of
isolated vertices of probability `1 − p < 1` and a graph of total mass
`T < 1`, and both parts lie in Shearer's region. ∎

So a cover-family local lemma is at least as strong as door 1, and closing B
for it would close door 1. That is the work of the tracks P1a and P1b, not of
this note. `verify.py` (check 5) shows the two behaviours on a toy star. The
canonical family fails. `{hub unflipped}` together with the `I`-events passes
even the complete-graph test, since `3/4 + 12/64 < 1`.

## Section R: what the local lemma does to `a + b < 1`

* The P3 events have pairwise disjoint key sets. They are isolated in the
  incidence and can be made isolated in a lopsidependency graph, so they
  constrain no local lemma. Theorem 1's own necessary condition has no
  `(D−1) ln k` term, as noted above.
* We do not show that a local lemma reaches `a + b ≥ 1`: that would need the
  rest of case (ii) and the rich progressions. We do not need to. With F
  (`a < 1/2`, first local-lemma family) and B (Theorem 1), `a + b < 2a < 1`
  holds automatically.
* Exact LP (check 7): `sup c` is `1/8` for {F, B, R} and for {F, B}. It
  reaches `1/4` only if F is relaxed as well. Past `a = 1/2`, single-label
  progressions do not exist (Lemma D), so Theorem 1 is empty there. The
  regime is closed instead by `first-family-circularity`: the first family
  must balance every `k`-AP of `ℤ/N`.

So the binding-lever conclusion holds for local lemmas too: **R alone gains
nothing, and B is still the lever, now closed for the canonical local lemma
as well as for union bounds.**

## What is not claimed

* Anything about criteria that read both the variables and the conflict
  structure and go beyond Shearer on the conflict graph, for example
  sharpened lopsided Moser–Tardos criteria. Theorem 1.2 covers their Shearer
  form only.
* Anything about refined or cover families (Propositions 2 and 3 say why).
* That no good flip assignment exists.
* Anything when `λ > q/(400k³)`.

## Checks in `verify.py`

1. Lemma H on `q = 2^61 − 1`, `D = 3`, `k = 12`, `λ = 840`. The proof's
   procedure finds `n_0`, and the two endpoints certify the label for all
   `E = 24 821 426 517` steps. 202 sampled steps, including `e = 1` and
   `e = E`, are re-checked position by position, with keys equal to
   `(s + jλe)²`. Negative control: a step `1000E` leaves the label.
2. Keys: `k` distinct keys per sampled `P_e`, all through `κ_0`, key sets
   pairwise distinct.
3. `Z_{K_{s,t}}(−p) = ∏(1−x) + ∏(1−y) − 1` against brute force on 40 random
   instances.
4. Toy star (`k = 3`, `L = 4`, `p = 1/4`), over all `2^9` flip assignments:
   `P(no mono) = 14457/65536 > 0` matches the closed form. `D` and `I` are
   disjoint, and hub-only intervals of mass `27/64` cover `[0, 1)`.
5. Toy star, `L = 12`: the canonical `K_{12,12}` leaves the region
   (`Z ≈ −0.171`). The cover family (`15/16`) and the disjointified refinement
   (`≈ 0.885`) pass the complete-graph test. Negative control: `K_{4,4}`
   stays in the region.
6. Exponents at `k = 10^{400}, 10^{1000}, 10^{3000}`, with `ln λ` bounded as
   in `single-label-obstructions` and `λ ≤ q/(400k³)` checked at each: the
   obstruction holds at `b = a` and `b > a`, and is escaped inside `b < a`
   once `k` is large.
7. LP: `sup c = 1/8` for {F, B, R} and {F, B}, and `1/4` for {B} with F
   relaxed.

The finite checks illustrate the lemmas; the proofs are the text above.
