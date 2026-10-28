import Mathlib

/-!
# Door 1 as a problem on key-measurable colorings: the finite core

Theorem 1 of `key-measurable-colorings` (PR #22). The method colors `n` by
`c₀(L n) ⊕ 1_X(κ n) ⊕ E_{κ n}`, with iid Bernoulli(`p`) flips `E` on the keys
outside the frozen set `X`. It succeeds (some `X` and `p ∈ (0,1)` give a good
coloring with positive probability) if and only if the class
`𝒞(c₀) = {c₀∘L ⊕ 1_Y∘κ : Y ⊆ 𝒦}` has a good member.

The progressions are an arbitrary finite family `𝒫` of subsets of `V`: the
statement holds for every family, and `kAPs N k` (the `k`-term progressions of
`ZMod N` with `k` distinct points) is one instance. The law of the flips is
the explicit finite sum over the flipped set `F ⊆ Xᶜ`; `weight_sum` shows it
has mass `1`. Nothing asymptotic is formalized.
-/

namespace KeyMeasurable

open Finset

variable {V Λ K : Type*} [Fintype K] [DecidableEq K]

/-- No set of the family is monochromatic. -/
-- noncomputable: no compiled code, so the audit lists only the logic's constants.
noncomputable def Good (Ps : Finset (Finset V)) (f : V → Bool) : Prop :=
  ∀ P ∈ Ps, ∀ β : Bool, ∃ x ∈ P, f x ≠ β

/-- The member `c₀∘L ⊕ 1_Y∘κ` of the class `𝒞(c₀)`. -/
noncomputable def member (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K) (Y : Finset K) : V → Bool :=
  fun n => xor (c₀ (L n)) (decide (κ n ∈ Y))

/-- The method's coloring `c₀∘L ⊕ 1_X∘κ ⊕ 1_F∘κ`, where `F ⊆ Xᶜ` is the set
of free keys whose flip came up `1`. -/
noncomputable def final (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K) (X F : Finset K) : V → Bool :=
  fun n => xor (c₀ (L n)) (xor (decide (κ n ∈ X)) (decide (κ n ∈ F)))

/-- The probability that the flipped set is exactly `F`, at rate `p`. -/
noncomputable def weight (X : Finset K) (p : ℝ) (F : Finset K) : ℝ :=
  p ^ F.card * (1 - p) ^ (Xᶜ \ F).card

open Classical in
/-- The probability that the method's coloring is good. -/
noncomputable def probGood (Ps : Finset (Finset V)) (c₀ : Λ → Bool) (L : V → Λ)
    (κ : V → K) (X : Finset K) (p : ℝ) : ℝ :=
  ∑ F ∈ Xᶜ.powerset, if Good Ps (final c₀ L κ X F) then weight X p F else 0

/-- The flips define a probability law on the flipped sets. -/
theorem weight_sum (X : Finset K) (p : ℝ) :
    ∑ F ∈ Xᶜ.powerset, weight X p F = 1 := by
  have h : ∀ F ∈ Xᶜ.powerset,
      weight X p F = p ^ F.card * (1 - p) ^ (Xᶜ.card - F.card) := by
    intro F hF
    rw [weight, card_sdiff (mem_powerset.mp hF)]
  rw [sum_congr rfl h, sum_pow_mul_eq_add_pow]
  simp

theorem weight_nonneg (X : Finset K) {p : ℝ} (h0 : 0 ≤ p) (h1 : p ≤ 1)
    (F : Finset K) : 0 ≤ weight X p F :=
  mul_nonneg (pow_nonneg h0 _) (pow_nonneg (by linarith) _)

omit [Fintype K] in
/-- Every outcome of the method lies in the class: `Y = X Δ F`. -/
theorem final_eq_member (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K) (X F : Finset K) :
    final c₀ L κ X F = member c₀ L κ (symmDiff X F) := by
  funext n
  by_cases h1 : κ n ∈ X <;> by_cases h2 : κ n ∈ F <;>
    simp [final, member, mem_symmDiff, h1, h2]

theorem weight_pos (X : Finset K) {p : ℝ} (h0 : 0 < p) (h1 : p < 1)
    (F : Finset K) : 0 < weight X p F :=
  mul_pos (pow_pos h0 _) (pow_pos (by linarith) _)

/-- At a rate in `(0, 1)`, the method succeeds with positive probability iff
some flipped set `F ⊆ Xᶜ` gives a good coloring. -/
theorem probGood_pos_iff (Ps : Finset (Finset V)) (c₀ : Λ → Bool) (L : V → Λ)
    (κ : V → K) (X : Finset K) {p : ℝ} (h0 : 0 < p) (h1 : p < 1) :
    0 < probGood Ps c₀ L κ X p ↔
      ∃ F ∈ Xᶜ.powerset, Good Ps (final c₀ L κ X F) := by
  classical
  unfold probGood
  constructor
  · intro hpos
    obtain ⟨F, hFm, hF⟩ := exists_lt_of_sum_lt (by simpa using hpos :
      ∑ F ∈ Xᶜ.powerset, (0 : ℝ) <
        ∑ F ∈ Xᶜ.powerset, if Good Ps (final c₀ L κ X F) then weight X p F else 0)
    by_cases hg : Good Ps (final c₀ L κ X F)
    · exact ⟨F, hFm, hg⟩
    · simp [hg] at hF
  · rintro ⟨F, hFm, hg⟩
    calc (0 : ℝ) < if Good Ps (final c₀ L κ X F) then weight X p F else 0 := by
          rw [if_pos hg]; exact weight_pos X h0 h1 F
      _ ≤ _ := by
          refine single_le_sum (f := fun F =>
              if Good Ps (final c₀ L κ X F) then weight X p F else 0)
            (fun F _ => ?_) hFm
          dsimp only
          split_ifs
          · exact weight_nonneg X h0.le h1.le F
          · exact le_rfl

/-- **Theorem 1 at a fixed frozen set.** For `p ∈ (0, 1)`, the method with
frozen set `X` succeeds with positive probability iff some member of the class
with `Y ⊇ X` is good. -/
theorem fixed_iff (Ps : Finset (Finset V)) (c₀ : Λ → Bool) (L : V → Λ)
    (κ : V → K) (X : Finset K) {p : ℝ} (h0 : 0 < p) (h1 : p < 1) :
    0 < probGood Ps c₀ L κ X p ↔ ∃ Y : Finset K, X ⊆ Y ∧ Good Ps (member c₀ L κ Y) := by
  rw [probGood_pos_iff Ps c₀ L κ X h0 h1]
  constructor
  · rintro ⟨F, hFm, hg⟩
    have hd : Disjoint X F := disjoint_left.mpr fun a ha hb =>
      (mem_compl.mp (mem_powerset.mp hFm hb)) ha
    refine ⟨X ∪ F, subset_union_left, ?_⟩
    rwa [final_eq_member, hd.symmDiff_eq_sup, sup_eq_union] at hg
  · rintro ⟨Y, hXY, hg⟩
    refine ⟨Y \ X, mem_powerset.mpr (fun k hk => by simp_all), ?_⟩
    have hd : Disjoint X (Y \ X) := disjoint_sdiff
    rwa [final_eq_member, hd.symmDiff_eq_sup, sup_eq_union, union_sdiff_of_subset hXY]

/-- **Theorem 1.** The method succeeds for some frozen set and some rate in
`(0, 1)` if and only if the class `𝒞(c₀)` contains a good coloring. -/
theorem method_iff_class (Ps : Finset (Finset V)) (c₀ : Λ → Bool) (L : V → Λ)
    (κ : V → K) :
    (∃ (X : Finset K) (p : ℝ), 0 < p ∧ p < 1 ∧ 0 < probGood Ps c₀ L κ X p) ↔
      ∃ Y : Finset K, Good Ps (member c₀ L κ Y) := by
  constructor
  · rintro ⟨X, p, h0, h1, hpos⟩
    obtain ⟨Y, -, hY⟩ := (fixed_iff Ps c₀ L κ X h0 h1).mp hpos
    exact ⟨Y, hY⟩
  · rintro ⟨Y, hY⟩
    exact ⟨Y, 1 / 2, by norm_num, by norm_num,
      (fixed_iff Ps c₀ L κ Y (by norm_num) (by norm_num)).mpr ⟨Y, subset_rfl, hY⟩⟩

omit [Fintype K] in
/-- **Proposition 3.** `P` is monochromatic in `β` under `c₀∘L ⊕ 1_Y∘κ` iff
the positions of `P` whose key lies in `Y` are exactly its `c₀`-class `≠ β`. -/
theorem mono_iff (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K) (Y : Finset K)
    (P : Finset V) (β : Bool) :
    (∀ x ∈ P, member c₀ L κ Y x = β) ↔
      P.filter (fun x => κ x ∈ Y) = P.filter (fun x => c₀ (L x) ≠ β) := by
  rw [filter_inj']
  refine forall₂_congr fun x _ => ?_
  by_cases h : κ x ∈ Y <;> cases hc : c₀ (L x) <;> cases β <;> simp [member, h, hc]

/-! ## Proposition 2: each half alone is satisfiable

The rich half is `Y = ∅`. The slow half is the finite core of the note's union
bound: it runs over distinct prescriptions (key word and `c₀`-color word), not
over progressions. The inputs `m ≥ k/2` and `T = e^{o(k)}` are the note's
hypotheses and enter here as parameters. -/

omit [Fintype K] in
/-- **Proposition 2.1.** `Y = ∅` leaves `c₀∘L`, which is good on the rich
progressions by hypothesis. -/
theorem rich_alone (R : Finset (Finset V)) (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K)
    (hR : Good R (fun n => c₀ (L n))) : Good R (member c₀ L κ ∅) := by
  have h : member c₀ L κ ∅ = fun n => c₀ (L n) := by funext n; simp [member]
  rwa [h]

/-- The prescription of `(P, β)`: the keys that must lie in `Y`, and the keys
that must miss it, for `P` to be monochromatic in `β`. -/
noncomputable def presc (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K) (P : Finset V)
    (β : Bool) : Finset K × Finset K :=
  ((P.filter fun x => c₀ (L x) ≠ β).image κ, (P.filter fun x => c₀ (L x) = β).image κ)

omit [Fintype K] in
theorem mono_iff_presc (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K) (Y : Finset K)
    (P : Finset V) (β : Bool) :
    (∀ x ∈ P, member c₀ L κ Y x = β) ↔
      (presc c₀ L κ P β).1 ⊆ Y ∧ Disjoint (presc c₀ L κ P β).2 Y := by
  have key : ∀ x, member c₀ L κ Y x = β ↔ (κ x ∈ Y ↔ c₀ (L x) ≠ β) := by
    intro x
    by_cases h : κ x ∈ Y <;> cases hc : c₀ (L x) <;> cases β <;> simp [member, h, hc]
  simp only [key, presc, image_subset_iff, mem_filter, disjoint_left, mem_image]
  constructor
  · intro h
    refine ⟨fun x hx => (h x hx.1).2 hx.2, ?_⟩
    rintro a ⟨x, ⟨hxP, hc⟩, rfl⟩ haY
    exact (h x hxP).1 haY hc
  · rintro ⟨h1, h2⟩ x hx
    exact ⟨fun hy hc => h2 ⟨x, ⟨hx, hc⟩, rfl⟩ hy, fun hc => h1 x ⟨hx, hc⟩⟩

omit [Fintype K] in
theorem presc_union (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K) (P : Finset V) (β : Bool) :
    (presc c₀ L κ P β).1 ∪ (presc c₀ L κ P β).2 = P.image κ := by
  ext a
  simp only [presc, mem_union, mem_image, mem_filter]
  constructor
  · rintro (⟨x, ⟨hx, -⟩, rfl⟩ | ⟨x, ⟨hx, -⟩, rfl⟩) <;> exact ⟨x, hx, rfl⟩
  · rintro ⟨x, hx, rfl⟩
    by_cases h : c₀ (L x) = β
    · exact Or.inr ⟨x, ⟨hx, h⟩, rfl⟩
    · exact Or.inl ⟨x, ⟨hx, h⟩, rfl⟩

/-- The key sets `Y` that meet `C = A ∪ B` exactly in `A` number at most
`2^{|K| − |C|}`: `Y` is fixed on `C`. -/
theorem card_prescribed_le (A B : Finset K) (m : ℕ) (hm : m ≤ (A ∪ B).card) :
    ((univ : Finset (Finset K)).filter fun Y => A ⊆ Y ∧ Disjoint B Y).card
      ≤ 2 ^ (Fintype.card K - m) := by
  classical
  calc _ ≤ ((univ \ (A ∪ B)).powerset).card := by
        refine card_le_card_of_injOn (fun Y => Y \ (A ∪ B)) (fun Y _ => ?_) ?_
        · simpa using sdiff_subset_sdiff (subset_univ Y) subset_rfl
        · intro Y hY Z hZ hYZ
          simp only [coe_filter, mem_univ, true_and, Set.mem_setOf_eq] at hY hZ
          ext a
          by_cases ha : a ∈ A
          · simp [hY.1 ha, hZ.1 ha]
          by_cases hb : a ∈ B
          · simp [disjoint_left.mp hY.2 hb, disjoint_left.mp hZ.2 hb]
          have := congrArg (a ∈ ·) hYZ
          simpa [ha, hb] using this
    _ = 2 ^ (Fintype.card K - (A ∪ B).card) := by
        rw [card_powerset, card_sdiff (subset_univ _), card_univ]
    _ ≤ 2 ^ (Fintype.card K - m) :=
        Nat.pow_le_pow_right (by norm_num) (Nat.sub_le_sub_left hm _)

open Classical in
/-- **Proposition 2.2, counting form.** If every slow progression carries at
least `m` distinct keys, at most `T · 2^{|K| − m}` key sets `Y` fail on the
slow family, where `T` is the number of distinct prescriptions. -/
theorem card_bad_le (S : Finset (Finset V)) (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K)
    (m : ℕ) (hm : ∀ P ∈ S, m ≤ (P.image κ).card) :
    ((univ : Finset (Finset K)).filter fun Y => ¬ Good S (member c₀ L κ Y)).card ≤
      ((S ×ˢ (univ : Finset Bool)).image fun Pβ => presc c₀ L κ Pβ.1 Pβ.2).card *
        2 ^ (Fintype.card K - m) := by
  classical
  set W := (S ×ˢ (univ : Finset Bool)).image fun Pβ => presc c₀ L κ Pβ.1 Pβ.2
  calc _ ≤ (W.biUnion fun w =>
          (univ : Finset (Finset K)).filter fun Y => w.1 ⊆ Y ∧ Disjoint w.2 Y).card := by
        refine card_le_card fun Y hY => ?_
        simp only [Good, mem_filter, mem_univ, true_and, not_forall, not_exists,
          not_not] at hY
        obtain ⟨P, hP, β, hmono⟩ := hY
        simp only [mem_biUnion, mem_filter, mem_univ, true_and]
        exact ⟨presc c₀ L κ P β, mem_image.mpr ⟨(P, β), by simp [hP], rfl⟩,
          (mono_iff_presc c₀ L κ Y P β).mp fun x hx => by
            simpa using not_and.mp (hmono x) hx⟩
    _ ≤ ∑ w ∈ W, ((univ : Finset (Finset K)).filter
          fun Y => w.1 ⊆ Y ∧ Disjoint w.2 Y).card := card_biUnion_le
    _ ≤ W.card * 2 ^ (Fintype.card K - m) := by
        refine sum_le_card_nsmul _ _ _ fun w hw => ?_
        obtain ⟨⟨P, β⟩, hPβ, rfl⟩ := mem_image.mp hw
        refine card_prescribed_le _ _ m ?_
        rw [presc_union]
        exact hm P (mem_product.mp hPβ).1

/-- **Proposition 2.2.** Fewer than `2^m` distinct prescriptions, each on at
least `m` keys: some key set `Y` colors no slow progression monochromatically. -/
theorem slow_alone (S : Finset (Finset V)) (c₀ : Λ → Bool) (L : V → Λ) (κ : V → K)
    (m : ℕ) (hm : ∀ P ∈ S, m ≤ (P.image κ).card)
    (hT : ((S ×ˢ (univ : Finset Bool)).image fun Pβ => presc c₀ L κ Pβ.1 Pβ.2).card < 2 ^ m) :
    ∃ Y : Finset K, Good S (member c₀ L κ Y) := by
  classical
  set T := ((S ×ˢ (univ : Finset Bool)).image fun Pβ => presc c₀ L κ Pβ.1 Pβ.2).card
  have hbad := card_bad_le S c₀ L κ m hm
  have hlt : T * 2 ^ (Fintype.card K - m) < 2 ^ Fintype.card K := by
    rcases Nat.eq_zero_or_pos T with h0 | hpos
    · rw [h0, zero_mul]; positivity
    · obtain ⟨w, hw⟩ := card_pos.mp hpos
      obtain ⟨⟨P, β⟩, hPβ, -⟩ := mem_image.mp hw
      have hmK : m ≤ Fintype.card K :=
        (hm P (mem_product.mp hPβ).1).trans (card_le_univ _)
      calc T * 2 ^ (Fintype.card K - m) < 2 ^ m * 2 ^ (Fintype.card K - m) :=
            Nat.mul_lt_mul_of_pos_right hT (by positivity)
        _ = 2 ^ Fintype.card K := by rw [← pow_add, Nat.add_sub_cancel' hmK]
  by_contra hno
  push_neg at hno
  have hcard : (univ : Finset (Finset K)).card ≤ T * 2 ^ (Fintype.card K - m) := by
    refine le_trans (card_le_card fun Y _ => ?_) hbad
    simp [hno Y]
  rw [card_univ, Fintype.card_finset] at hcard
  omega

/-- The `k`-term progressions `{a, a + d, …, a + (k-1)d}` of `ZMod N` with `k`
distinct points (a progression that wraps onto itself is not counted). -/
noncomputable def kAPs (N k : ℕ) [NeZero N] : Finset (Finset (ZMod N)) :=
  ((univ : Finset (ZMod N × ZMod N)).image fun ad =>
      (range k).image fun i : ℕ => ad.1 + (i : ZMod N) * ad.2).filter fun P => P.card = k

theorem mem_kAPs {N k : ℕ} [NeZero N] (P : Finset (ZMod N)) :
    P ∈ kAPs N k ↔
      (∃ a d : ZMod N, (range k).image (fun i : ℕ => a + (i : ZMod N) * d) = P) ∧
        P.card = k := by
  simp [kAPs]

/-- Checked by the kernel. In `ZMod 6`: the six blocks of step `±1`, plus
`{0, 2, 4}` and `{1, 3, 5}`; step `3` wraps onto two points. In `ZMod 7`: seven
starting points times three steps up to sign, so 21 of the 35 three-point sets
(`{0, 1, 3}` is not one). -/
theorem card_kAPs_6_3 : (kAPs 6 3).card = 8 := by decide

theorem card_kAPs_7_3 : (kAPs 7 3).card = 21 := by decide

/-- Degenerate lengths: beyond `N` there is no progression (every coloring is
good), and length `0` gives only the empty set (no coloring is good). -/
theorem kAPs_eq_empty_of_lt {N k : ℕ} [NeZero N] (h : N < k) : kAPs N k = ∅ := by
  ext P
  simp only [kAPs, mem_filter, notMem_empty, iff_false, not_and]
  intro _ hP
  have := card_le_univ P
  rw [ZMod.card] at this
  omega

theorem kAPs_zero (N : ℕ) [NeZero N] : kAPs N 0 = {∅} := by
  ext P
  simp [kAPs, eq_comm]

/-- Theorem 1 for the van der Waerden family on `ZMod N`: a specialization of
`method_iff_class`, with the same proof. It is meaningful for `2 ≤ k ≤ N`; see
`kAPs_eq_empty_of_lt` and `kAPs_zero` for the degenerate lengths. -/
theorem method_iff_class_kAPs (N k : ℕ) [NeZero N] (c₀ : Λ → Bool)
    (L : ZMod N → Λ) (κ : ZMod N → K) :
    (∃ (X : Finset K) (p : ℝ), 0 < p ∧ p < 1 ∧ 0 < probGood (kAPs N k) c₀ L κ X p) ↔
      ∃ Y : Finset K, Good (kAPs N k) (member c₀ L κ Y) :=
  method_iff_class _ c₀ L κ

end KeyMeasurable
