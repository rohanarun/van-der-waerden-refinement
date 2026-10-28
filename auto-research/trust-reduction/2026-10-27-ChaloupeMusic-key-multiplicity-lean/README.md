# Lean: a key occurs at most twice on a progression

**Status:** formalization, Lean 4.21.0 and Mathlib v4.21.0. Builds with no
`sorry`. Every constant of the namespace depends only on `propext`,
`Classical.choice` and `Quot.sound`.

It formalizes Lemma 3 of `2026-10-26-ChaloupeMusic-source-only-1-16` (this
track, PR #19): on a progression `n_j = n₀ + jd`, `d ≠ 0`, `0 ≤ j < k`, of
`ℤ/q^D`, every key occurs at most twice. Hence such a progression carries at
least `⌈k/2⌉` distinct keys. The key is the source's, with its adaptive mesh:
nothing is abstracted away.

**Base commit:** `84ed864` (PR #19).

## Why it matters

Several results use the bound `⌈k/2⌉`:
* the rich estimate of `source-only-1-16` §6 (`γk/2` distinct keys);
* the slow half of the key-measurable reduction, whose Lean statement in
  PR #23 (`key-measurable-lean`) receives `m ≥ k/2` as a hypothesis (`hm`);
* the `2^{−⌈k/2⌉}` per progression of the line-witness note (PR #23).

`hm_bridge` states the hypothesis in the form of PR #23. There, `hm` reads
`m ≤ (P.image κ).card` for every `P ∈ S`, with `P : Finset V` and `κ`
valued in a finite type `K`. Here `V = ℤ/q^D`, and `K` is the range of the
key, which is finite (`key_range_finite`). For every family `S` of `k`-term
progressions with nonzero step, `hm` holds with `m = ⌈k/2⌉`. The two packages
live on different branches, so this is proved in this package's own terms.
It is not a Lean `import` of PR #23.

## The statements

All are in `lean/KeyMultiplicity/Basic.lean`, namespace `KeyMultiplicity`.

* `lemma3`: the source's key, all parameters instantiated. `P` is prime,
  `e > 0`, `2 ≤ k < P` and `h₀ < P`. The mesh has `α = q^{−(D+1)}`,
  `R = log(1 + 1/(2α))` and `m = ⌈k²R⌉`, and the dilation is `λ = lam h₀ M`.
  Conclusion: for every key `κ₀`, `#{j < k : κ(n₀ + jd) = κ₀} ≤ 2`, and
  `(k + 1)/2 ≤ #{κ(n₀ + jd) : j < k}`.
* `mult_le_two` and `distinct_keys`: the same conclusions, for any mesh
  `V : ℝ → β`. Two centred representatives with the same `V`-label must be at
  most `w` apart, with `k w < 1`. Instead of the dilation, the hypothesis is
  `gcd(λ, P) = 1`.
* `meshV_spec` and `meshV_of_mem`: `meshV` is exactly the source's
  partition. A label `(false, ℓ)` means `s + 1/2 ∈ [a_ℓ, a_{ℓ+1})`, and a
  label `(true, ℓ)` means `1/2 − s ∈ (a_ℓ, a_{ℓ+1}]`, with `0 ≤ ℓ < m`. The
  first theorem gives this direction. The second gives the converse: a point
  of a named interval gets that label. So the named intervals are pairwise
  disjoint.
* `meshV_width`: two points with the same label are less than `H` apart
  when `R ≤ mH` and `α ≤ 1/2`. The source proves `≤ 2H`.
* `lam_coprime`: the step where "`λ` has only prime factors `≤ h₀`" enters.
  If `h₀ < P`, then `gcd(λ, P) = 1`.
* `separation`: if `n ≠ n'` then `‖qỹ(n) − qỹ(n')‖² ≥ 1`. It uses only
  `gcd(λ, q) = 1`.
* `terms_ne`: if `P > k` and `d ≠ 0`, the `k` terms are distinct, so a step
  of small order cannot fold the progression.
* `yt_affine` and `three_affine`: the affinity inside a small box.
* `three_point_left` and `three_point_right`: the three-point identity.
* `no_three`: three positions never share a key.
* `key_range_finite` and `hm_bridge`: the bridge to PR #23, above.

## Correspondence with the source

The source is the OpenAI preprint `Quantitative-Superexponential-Bounds-for-
van-der-Waerden-Numbers-September-23-2026`, pinned in `source-manifest.json`.
Line numbers refer to `build/sections/*.tex`. The note is
`source-only-1-16/README.md` at `84ed864`.

| Lean | Source | Note |
|---|---|---|
| `ZMod ((P ^ e) ^ D)`, `q = P ^ e` | `q` a power of the prime `P`, 02 l. 84-85; `G = ℤ/q^D`, l. 104 | §2, l. 87-88 |
| `n₀ + j * d`, `j < k`, `d ≠ 0` | (setup:cyclic), 02 l. 106-108 | §3, l. 126 |
| `k < P` (in `terms_ne`) | "every nonzero element … has order at least `P > k`", 02 l. 109-110 | — |
| `yt q D lam n i` | `x_i(n) = n/q^i`, `y_i = λx_i`, `ỹ ∈ [−1/2, 1/2)^D`, 02 l. 113-121 | §2, l. 89 |
| `lam h₀ M`, with `Nat.log ℓ (2M)` | (setup:dilation-definition), 02 l. 24-27 | §2, l. 87 |
| `h₀ < P` (in `lam_coprime`) | `gcd(λ, q) = 1`, 02 l. 90-92 | §2 table, l. 103 |
| `α = q^{−(D+1)}` | (setup:mesh-parameters), 02 l. 93-95 | §2, l. 89 |
| `R`, `m = ⌈k²R⌉`, `meshA` (`a_ℓ`) | (mesh:definition), 02 l. 143-147 | — |
| `meshV`, `meshV_spec`, `meshV_of_mem` | (mesh:intervals), 02 l. 149-153; zero goes to the interval on its right, l. 155-156 | — |
| `H = 1/k²` (in `lemma3`) | (setup:parameters), 02 l. 13-19 | §2, l. 87 |
| `f`, `key` | (perturb:keys), 06 l. 15-19 | §2, l. 90 |
| `separation` | 06 l. 44-66 | §3, l. 129-130 |
| `three_affine` | (dichotomy:affinity), 05 l. 11-31 | §3, l. 129 |
| `mult_le_two`, `lemma3` | Lemma perturb:multiplicity, 06 l. 29-32 (bound four) | Lemma 3, l. 126-134 (bound two) |

The source's parameter values (`D = ⌈k^{1/10}⌉`, …) and the note's
(`D = ⌈k^a⌉`, `h₀ = DL²`, …) are not needed. `lemma3` holds for every `D`,
`e > 0`, `M` and `h₀ < P`, and for every `k ≥ 2` below `P`, with no
threshold on `k`.

## The proof, and where it differs from the note

The first two steps are the note's, after the source:
1. **Separation.** Take the least `i` with `q^i ∤ λ(n − n')`. In
   coordinate `i`, `q(ỹ_i(n) − ỹ_i(n'))` is a nonzero integer.
2. **Affinity.** If three positions share a box, the integer
   `(j₃−j₂)(M₂−M₁) − (j₂−j₁)(M₃−M₂)` has absolute value `< kw < 1`, so it
   is zero. The three points `qỹ(n_j)` are then collinear, at parameters
   `j₁ < j₂ < j₃`.

The last step follows **PR #10, not the note's half-lines**. PR #10 is by
rohanarun: `formal/Vdw/Geometry.lean`, `no_three_in_unit_band`, added in
`815a4c0` and unchanged at the PR head `a46ef51`. The note argues on the two
half-lines from the nearest point of the line. Here, coordinate by
coordinate, the identity of PR #10 reads

```
(j₂−j₁)·[(j₃−j₂)f₁ + (j₂−j₁)f₃ − (j₃−j₁)f₂] = (j₃−j₂)(j₃−j₁)‖z₂−z₁‖²,
(j₃−j₂)·[same]                              = (j₂−j₁)(j₃−j₁)‖z₃−z₂‖².
```

Three squared norms in one band `[m, m+1)` make the bracket smaller than
`j₃ − j₁`. Separation makes both norms at least one. The first identity then
gives `j₃ − j₂ < j₂ − j₁`, and the second gives the reverse. The conclusion
is the same as the note's.

## What is not formalized

* The existence of `P`, that is the source's Lemma setup:prime. `P` is
  given, with `k < P` and `h₀ < P`.
* Everything after Lemma 3 in the note. The rich estimate, for example,
  uses Lemma 3 but is not formalized here.
* The minimality of `q` (the least power of `P` that is at least
  `k^{ck/D}`). It plays no role in Lemma 3, and `lemma3` holds for every
  power.

## Checks beyond the build

`verify.py` replays a hand transcription of the definitions. It uses exact
rationals for `ỹ`, `f` and the band. For the mesh it uses 80-digit decimals,
and certifies every floor, ceiling and interval comparison by a margin of
`10⁻⁴⁰`. There is one exact contact, `s = 0` at the end `a_m = 1/2`, and it
is set exactly. The mesh (`α`, `m`) of each toy is recorded in
`RESULT.json`, so a change of mesh scale changes the result.

On toys in the regime of `lemma3`, `meshV` agrees with a direct search of the
source's intervals on 10,815 points. No key occurs three times, and there are
at least `⌈k/2⌉` keys, on all 50,572 progressions. The bound is tested on
three kinds of progressions:
* **Exhaustive, on the five smallest toys.** There `q < k²`, so every term
  is alone in its box: two terms share a box only if every coordinate moves
  by less than the mesh width (`< 1/k²`), and the separating coordinate moves
  by a nonzero multiple of `1/q`. The check is met trivially.
* **Sampled, on two larger toys.** A uniform step moves every coordinate by
  little only with probability about `(7/q)^D`. No key occurs twice there
  either.
* **Random short steps with `q > k²`.** Here the bound is exercised. Each
  coordinate moves by at most `3/q` modulo `1/q^i`, and `n₀` is random; there
  are 3,000 draws on each of `q = 125, D = 2`, `q = 625, D = 2` and
  `q = 125, D = 3`. A key occurs twice on 1, 5 and 1 of them. Three or more
  terms share a box, so that only the band keeps their keys apart, on 68,
  1,261 and 21.

The lower bound is reached as well: on `q = 625`, some progression with
`k = 4` carries only `2 = ⌈k/2⌉` distinct keys (`fewest_distinct_keys` in
`RESULT.json`). A witness built by hand (`q = 125`, `D = 3`, `k = 4`) also
has a key twice.

Four mutants each make a key occur three times:
* without the band;
* without the box;
* with `k ≥ P`, where a step of order 5 folds the progression;
* with `λ = P`.

The proof uses `k w < 1`, and nothing shows that this hypothesis is
necessary. Meshes coarser than the source's, with `m = ⌈kR⌉`, `⌈R⌉` or
`⌈R/4⌉` instead of `⌈k²R⌉`, were tried on 1,000 short steps of
`q = 625, D = 2`. None of them makes a key occur three times. The measurement
is recorded in `RESULT.json`. The mutant without the box shows that some
mesh is needed.

Last, `verify.py` checks `MANIFEST.json`: every listed file must have its recorded sha256, and `--write` records the new hash of `RESULT.json` only when every other check passes. A file changed by one byte fails.

The axiom audit runs `#print axioms` on every constant whose name starts with
`KeyMultiplicity`. A private or `_root_` declaration would escape that filter;
there is none. The audit of `lemma3` and `hm_bridge` is transitive anyway, so
it covers everything they use.

## Reproduce

```sh
cd auto-research/trust-reduction/2026-10-27-ChaloupeMusic-key-multiplicity-lean/lean
lake build && lake env lean Axioms.lean        # the proof
cd .. && python3 -B verify.py                  # the evidence, the transcription, the mutants
```

**Only `lake build` proves anything.** `verify.py` does not run Lean. It
checks that the recorded evidence (`lean/evidence/`) belongs to these
sources, and replays the transcription. The fingerprints it checks are a
declaration: they catch a stale record, not a forged one.
`lean/record-evidence.sh` rebuilds the package and re-records the build, the
`#print axioms` audit of the whole namespace and the fingerprints, in one
pass.
