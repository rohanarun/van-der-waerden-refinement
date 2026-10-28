# Lean: the finite core of the key-measurable reduction

**Status:** formalization, Lean 4.21.0 and Mathlib v4.21.0. Builds with no
`sorry`. Every constant of the namespace depends only on `propext`,
`Classical.choice` and `Quot.sound`.

It formalizes Theorem 1 of `2026-10-27-ChaloupeMusic-key-measurable-colorings`
(PR #22), its Proposition 3, and the finite core of its Proposition 2 (each
half alone is satisfiable). It also adds Theorem 1 at a fixed frozen set.

**Base commit:** `061401f` (`research/door-one-continued`, PR #22).

## What the formal statements say, and what they do not

The finite core is an **identity of classes**. Every outcome of the method is
a member `c₀∘L ⊕ 1_Y∘κ` of the class `𝒞(c₀)`, with `Y = X Δ F`. Conversely,
each member is reached with positive probability. In the fixed-`X` form, it
is reached whenever `Y ⊇ X`. The proofs are short, because the statements are
close to definitions.

What makes Theorem 1 a theorem in the note is what surrounds it, and that is
**not formalized**:
* the template data: `N = k^{ck}`, `|𝒦| = N^{o(1)}`, and admissibility of `c₀`
  (the first local-lemma family);
* the Corollary, which reads "`1/8` for every frozen `X`" as a van der Waerden
  upper bound for `𝒞` at `N = k^{(1/8+ε)k}`;
* the random benchmark, (D) and (S);
* in Proposition 2.2, the two counts that make the union bound small:
  `m ≥ k/2`, since a key occupies at most two positions (Lemma 3 of
  `source-only-1-16`), and `T = e^{o(k)}`, from the slow-word counts of
  `exact-door-one-condition`. The finite statement **receives them as
  hypotheses** (`hm`, `hT`) and proves nothing about them;
* in Proposition 2.1, the step "`c₀` is `γ`-rich on every rich progression,
  so none of them is monochromatic". `hR` assumes it, and `rich_alone` then
  only replaces `Y = ∅` by `c₀∘L`;
* the interaction, "every proper `Y` contains an induced class". That is the
  open question itself.

Admissibility is only a hypothesis on `c₀`. The statements hold for every
`c₀`, so they hold in particular for admissible ones.

The formal content is what a reader should not have to take on trust. The
reduction loses nothing:
* the success event of the method, at any rate `p ∈ (0, 1)`, is exactly
  "some good member of the class is reachable";
* reachability from `X` is exactly `Y ⊇ X`;
* the monochromatic event is exactly the induced-class condition.

The same statement holds for every finite family of progressions, so nothing
depends on arithmetic.

## Reproduce

```sh
cd auto-research/structured-flips/2026-10-27-ChaloupeMusic-key-measurable-lean/lean
lake build && lake env lean Axioms.lean        # the proof
cd .. && python3 -B verify.py                  # the evidence and the definitions
```

**Only `lake build` proves anything.** `verify.py` does not run Lean. It uses
only the standard library and runs in under a second. Expected output: exit
code 0, last line `Test passé : all checks pass`, and a JSON summary equal to
`RESULT.json`.

It checks two things. First, it checks the recorded evidence
(`lean/evidence/`). `lean/record-evidence.sh` rebuilds, runs the audit and
writes the SHA-256 of the sources in one pass. `verify.py` refuses evidence
whose recorded fingerprints differ from the sources. The fingerprints are a
declaration, not a proof: they catch a stale record, not a forged one.
Second, it checks that a hand transcription of the definitions says what the
note means.

`lake build` needs the Mathlib v4.21.0 build, which `lake` fetches the first
time. `Axioms.lean` prints `#print axioms` for every constant of the
`KeyMeasurable` namespace, auxiliary `_proof_*` constants included. Its
output is `lean/evidence/axioms.txt`.

## Model

In `lean/KeyMeasurable/Basic.lean`:

* positions `V`, labels `Λ`, keys `K` (a `Fintype`);
* `L : V → Λ`, `κ : V → K`, `c₀ : Λ → Bool`;
* colors are `Bool`, and `⊕` is `xor`;
* the progressions are an arbitrary `Ps : Finset (Finset V)`.

| Lean | Meaning |
|---|---|
| `Good Ps f` | no `P ∈ Ps` is monochromatic under `f` |
| `member c₀ L κ Y` | `c₀∘L ⊕ 1_Y∘κ`, a member of `𝒞(c₀)` |
| `final c₀ L κ X F` | `c₀∘L ⊕ 1_X∘κ ⊕ 1_F∘κ`, the method's coloring when the free keys of `F ⊆ Xᶜ` flip |
| `weight X p F` | `p^{\|F\|}(1−p)^{\|Xᶜ \ F\|}`, the probability that exactly `F` flips |
| `probGood Ps c₀ L κ X p` | `∑_{F ⊆ Xᶜ} weight X p F · [Good Ps (final … X F)]` |
| `presc c₀ L κ P β` | `(κ(P ∩ {c₀ ≠ β}), κ(P ∩ {c₀ = β}))`: the keys that must lie in `Y`, and the keys that must miss it, for `P` to be monochromatic in `β` |
| `kAPs N k` | the sets `{a + i d : i < k}` of `ZMod N` with exactly `k` points |

The law of the iid Bernoulli(`p`) flips is written as an explicit finite sum,
with no measure theory. `weight_sum` checks that it has mass `1`. `kAPs` keeps
only progressions with `k` distinct points, so a progression that wraps onto
itself is not counted.

## Statements

```lean
theorem weight_sum (X : Finset K) (p : ℝ) :
    ∑ F ∈ Xᶜ.powerset, weight X p F = 1

theorem probGood_pos_iff … (h0 : 0 < p) (h1 : p < 1) :
    0 < probGood Ps c₀ L κ X p ↔ ∃ F ∈ Xᶜ.powerset, Good Ps (final c₀ L κ X F)

-- Theorem 1 at a fixed frozen set
theorem fixed_iff … (X : Finset K) (h0 : 0 < p) (h1 : p < 1) :
    0 < probGood Ps c₀ L κ X p ↔ ∃ Y : Finset K, X ⊆ Y ∧ Good Ps (member c₀ L κ Y)

-- Theorem 1
theorem method_iff_class (Ps : Finset (Finset V)) (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K) :
    (∃ (X : Finset K) (p : ℝ), 0 < p ∧ p < 1 ∧ 0 < probGood Ps c₀ L κ X p) ↔
      ∃ Y : Finset K, Good Ps (member c₀ L κ Y)

-- Proposition 3
theorem mono_iff … (Y : Finset K) (P : Finset V) (β : Bool) :
    (∀ x ∈ P, member c₀ L κ Y x = β) ↔
      P.filter (fun x => κ x ∈ Y) = P.filter (fun x => c₀ (L x) ≠ β)

-- the van der Waerden instance: a specialization, with the same proof
theorem method_iff_class_kAPs (N k : ℕ) [NeZero N] … :
    (∃ X p, 0 < p ∧ p < 1 ∧ 0 < probGood (kAPs N k) c₀ L κ X p) ↔
      ∃ Y, Good (kAPs N k) (member c₀ L κ Y)
theorem card_kAPs_6_3 : (kAPs 6 3).card = 8 := by decide    -- checked by the kernel
theorem card_kAPs_7_3 : (kAPs 7 3).card = 21 := by decide
theorem kAPs_eq_empty_of_lt (h : N < k) : kAPs N k = ∅      -- every coloring is good
theorem kAPs_zero (N : ℕ) [NeZero N] : kAPs N 0 = {∅}       -- no coloring is good

-- Proposition 2.1: the rich half alone
theorem rich_alone (R : Finset (Finset V)) … (hR : Good R (fun n => c₀ (L n))) :
    Good R (member c₀ L κ ∅)

-- Proposition 2.2: the slow half alone (T = number of distinct prescriptions)
theorem mono_iff_presc … :
    (∀ x ∈ P, member c₀ L κ Y x = β) ↔
      (presc c₀ L κ P β).1 ⊆ Y ∧ Disjoint (presc c₀ L κ P β).2 Y
theorem card_bad_le (S : Finset (Finset V)) … (m : ℕ) (hm : ∀ P ∈ S, m ≤ (P.image κ).card) :
    (univ.filter fun Y => ¬ Good S (member c₀ L κ Y)).card ≤
      ((S ×ˢ univ).image fun Pβ => presc c₀ L κ Pβ.1 Pβ.2).card * 2 ^ (Fintype.card K - m)
theorem slow_alone … (hm : ∀ P ∈ S, m ≤ (P.image κ).card)
    (hT : ((S ×ˢ univ).image fun Pβ => presc c₀ L κ Pβ.1 Pβ.2).card < 2 ^ m) :
    ∃ Y : Finset K, Good S (member c₀ L κ Y)
```

`method_iff_class_kAPs` adds nothing to `method_iff_class`: it is the
instance, and is meaningful for `2 ≤ k ≤ N`. The degenerate lengths are
stated so that no one reads a vacuous case as content.

`final_eq_member` (`final … X F = member … (X Δ F)`) carries both directions.
The witness for `(2 ⇒ 1)` is `X = Y`, with the empty flip set, which has
weight `(1 − p)^{|Yᶜ|} > 0`. The note's version asks `|𝒦| p < 1` and gets a
probability at least `1 − |𝒦| p`. Positivity needs no condition on `p` beyond
`p < 1`, and the stronger bound is not formalized. Under `fixed_iff`, the
witness is `F = Y \ X`.

Proposition 2.2 counts the note's union bound. `T` counts distinct
**prescriptions**: pairs of key sets (keys that must be in `Y`, keys that
must miss it), with both colors `β` included, and not progressions. A
prescription is determined by the note's pair (key word, `c₀`-color word)
together with `β`, but distinct words can give the same prescription. So
`T ≤ 2 ×` (the number of the note's pairs), and `hT` follows from the note's
hypothesis as soon as `2 ×` (that number) `< 2^m`.

Example: `ℤ/4`, `k = 2`, `κ : 0 ↦ a, 1 ↦ b, 2 ↦ b, 3 ↦ a`, and `c₀`
constant. `{0, 1}` and `{2, 3}` give two key words, hence four pairs with
`β`, but only two prescriptions, so `T = 2`.

Each prescription with at least `m` keys fixes `Y` on those keys
(`presc_union`: the two halves cover `κ(P)`). So it is met by at most
`2^{|K| − m}` key sets (`card_prescribed_le`). When its two halves share a
key, it is met by none. The lemma does not assume `P` nonempty. For `m = 0`,
an empty `P` is never good and the bound holds trivially. The decidability
in the statement of `card_bad_le` is classical.

## Checks in `verify.py`

1. The fingerprints in `lean/evidence/sources.sha256` match the six Lean
   files of the package. If a theorem is added or changed after the evidence
   was recorded, the check fails, even under `--write`, unless someone
   recomputes the fingerprints by hand. They are a declaration. Then a lint, not a proof: no `sorry`,
   `admit`, axiom declaration, `native_decide`, `implemented_by` or `extern`
   outside comments. It is a regular expression, which nested comments or a
   `--` inside a string can fool. The check that counts is `#print axioms`.
   The toolchain and the Mathlib pin are `v4.21.0`.
2. `evidence/axioms.txt` lists the 54 constants it announces. Each one uses
   only `propext`, `Classical.choice` and `Quot.sound`. The sixteen statements
   named in this README are among them, including the kernel-checked counts of
   `kAPs`.
3. `evidence/build.txt` records the build. The record only says that a build
   ran; the build is the proof.
4. A hand transcription of the definitions (`Good`, `member`, `final`,
   `weight`, `probGood`), enumerated exhaustively with exact rationals on 60
   random toys. The toys have 9 positions, 5 keys, 3 labels and 4 to 13
   three-point sets. 6 of them have an empty family, 6 an added empty set and
   6 an added one-point set.
   * 3 840 cases for `weight_sum`, `probGood_pos_iff` and `fixed_iff`, with
     `p ∈ {1/5, 1/2}`;
   * `method_iff_class` on all 60 toys, which have both outcomes (33 toys
     with a good member, 27 without);
   * 28 992 cases of `mono_iff`.
5. Proposition 2 on 200 random toys, with the same transcription. The toys
   have 10 positions, 3 to 7 keys and 1 to 5 sets of 2 to 5 points. 29 of
   them have an empty set added, so `m = 0`; 29 have an added one-point set,
   and 10 have an empty family.
   * `rich_alone` on the 53 toys where its hypothesis `hR` holds;
   * `mono_iff_presc` and `presc_union` on every `Y`;
   * `card_bad_le` on all 200 toys. The bound is attained on 33 of them, all
     with disjoint failure events, 10 of them degenerate. That shows only
     that the count is exact on disjoint events;
   * `slow_alone` on the 57 toys where `T < 2^m`.

The toys test the transcription, not the Lean terms, which are
noncomputable. They check that the definitions say what the note means.
The proof is the Lean build.
