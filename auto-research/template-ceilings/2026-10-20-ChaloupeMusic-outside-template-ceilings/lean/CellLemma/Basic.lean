import Mathlib

/-!
# Cell lemma for cyclic progressions (`C = 1`)

Formalizes item 1 of "No-go for one named class" in
`../README.md` (package `outside-template-ceilings`).

* `pigeon_residues`: more than `m ^ D` integer vectors contain two distinct ones
  that are congruent modulo `m`.
* `segment_in_box`: a half-open interval contains the `m + 1` equally spaced
  points between two of its points.
* `cell_lemma`: for any lattice `Λ = φ(ℤ^ι)` in `ℚ^κ`, a half-open box of widths
  `≤ 1` holding more than `(k-1)^|ι|` lattice points contains a `k`-term
  progression `x + j v` of lattice points with `v ≠ 0` and `|v_i| < 1`.
* `cyclic_cell_lemma`: the instance `Λ = ℤ^D + ℤ·u`, `u = (1/q, …, 1/q^D)`,
  stated on `ℤ/q^D`: there are `m, d` with `q^D ∤ d` such that every
  `(m + j d)·u`, `j < k`, has a lift in the box.
-/

namespace CellLemma

/-- The half-open box `∏ᵢ [a i, a i + w i)`. -/
def InBox {κ : Type*} (a w : κ → ℚ) (x : κ → ℚ) : Prop :=
  ∀ i, a i ≤ x i ∧ x i < a i + w i

-- Pigeonhole on residues modulo `m`: the index of `m ℤ^ι` in `ℤ^ι` is `m ^ |ι|`.
theorem pigeon_residues {ι α : Type*} [Fintype ι] [DecidableEq ι] [DecidableEq α]
    (m : ℕ) (hm : 0 < m) (P : Finset α) (c : α → ι → ℤ)
    (hP : m ^ Fintype.card ι < P.card) :
    ∃ x ∈ P, ∃ y ∈ P, x ≠ y ∧ ∃ w : ι → ℤ, c y - c x = (m : ℤ) • w := by
  let T : Finset (ι → ℤ) := Fintype.piFinset fun _ => Finset.Ico (0 : ℤ) m
  have hT : T.card = m ^ Fintype.card ι := by
    simp [T, Fintype.card_piFinset, Int.card_Ico]
  have hmaps : ∀ p ∈ P, (fun i => c p i % (m : ℤ)) ∈ T := by
    intro p _
    simp only [T, Fintype.mem_piFinset, Finset.mem_Ico]
    intro i
    exact ⟨Int.emod_nonneg _ (by exact_mod_cast hm.ne'),
      Int.emod_lt_of_pos _ (by exact_mod_cast hm)⟩
  obtain ⟨x, hx, y, hy, hne, heq⟩ :=
    Finset.exists_ne_map_eq_of_card_lt_of_maps_to (hT ▸ hP) hmaps
  refine ⟨x, hx, y, hy, hne, fun i => (c y i - c x i) / m, ?_⟩
  funext i
  have hd : (m : ℤ) ∣ c y i - c x i := Int.ModEq.dvd (congrFun heq i)
  simp [Int.mul_ediv_cancel' hd]

-- Convexity of a half-open interval, in the form used by the lemma:
-- `m V = Y - X` and `0 ≤ j ≤ m` put `X + j V` between `X` and `Y`.
theorem segment_in_box {A W X Y V m j : ℚ} (hm : 1 ≤ m) (hV : m * V = Y - X)
    (hX : A ≤ X ∧ X < A + W) (hY : A ≤ Y ∧ Y < A + W) (hj0 : 0 ≤ j) (hjm : j ≤ m) :
    A ≤ X + j * V ∧ X + j * V < A + W := by
  have hm0 : 0 < m := by linarith
  have hid : m * (X + j * V) = (m - j) * X + j * Y := by
    have : m * (j * V) = j * (Y - X) := by rw [← hV]; ring
    linarith [this]
  constructor
  · have h1 : (m - j) * A ≤ (m - j) * X := mul_le_mul_of_nonneg_left hX.1 (by linarith)
    have h2 : j * A ≤ j * Y := mul_le_mul_of_nonneg_left hY.1 hj0
    have : m * A ≤ m * (X + j * V) := by nlinarith
    exact le_of_mul_le_mul_left this hm0
  · have : m * (X + j * V) < m * (A + W) := by
      rcases lt_or_eq_of_le hjm with hlt | heq
      · have h1 : (m - j) * X < (m - j) * (A + W) :=
          mul_lt_mul_of_pos_left hX.2 (by linarith)
        have h2 : j * Y ≤ j * (A + W) := mul_le_mul_of_nonneg_left hY.2.le hj0
        nlinarith
      · subst heq
        have h2 : j * Y < j * (A + W) := mul_lt_mul_of_pos_left hY.2 hm0
        nlinarith
    exact lt_of_mul_lt_mul_left this hm0.le

/-- **Cell lemma, abstract form.** `φ` parametrizes a lattice `Λ = φ(ℤ^ι)`.
A half-open box of widths `≤ 1` holding more than `(k-1)^|ι|` points of `Λ`
contains `k` points `φ x + j φ v` (`j < k`) of `Λ`, with `φ v ≠ 0` and every
coordinate of `(k-1) φ v` in `(-1, 1)`. -/
theorem cell_lemma {ι κ : Type*} [Fintype ι] [DecidableEq ι]
    (φ : (ι → ℤ) →+ (κ → ℚ))
    (k : ℕ) (hk : 2 ≤ k) (a w : κ → ℚ) (hw : ∀ i, w i ≤ 1)
    (P : Finset (κ → ℚ)) (hPΛ : ∀ p ∈ P, p ∈ Set.range φ)
    (hPB : ∀ p ∈ P, InBox a w p)
    (hcard : (k - 1) ^ Fintype.card ι < P.card) :
    ∃ x v : ι → ℤ, φ v ≠ 0 ∧ (∀ i, ((k - 1 : ℕ) : ℚ) * |φ v i| < 1) ∧
      ∀ j : ℕ, j < k → InBox a w (φ (x + (j : ℤ) • v)) := by
  classical
  let c : (κ → ℚ) → ι → ℤ := fun p => if h : p ∈ Set.range φ then h.choose else 0
  have hc : ∀ p ∈ P, φ (c p) = p := by
    intro p hp
    simp only [c, dif_pos (hPΛ p hp)]
    exact (hPΛ p hp).choose_spec
  obtain ⟨x, hx, y, hy, hne, v, hv⟩ :=
    pigeon_residues (k - 1) (by omega) P c hcard
  have hm1 : (1 : ℚ) ≤ ((k - 1 : ℕ) : ℚ) := by exact_mod_cast (by omega : 1 ≤ k - 1)
  -- `(k-1) φ v = y - x`, coordinate by coordinate
  have hkey : ∀ i, ((k - 1 : ℕ) : ℚ) * φ v i = y i - x i := by
    intro i
    have h := congrArg φ hv
    rw [map_sub, map_zsmul, hc x hx, hc y hy] at h
    have h' := congrFun h i
    simp only [Pi.sub_apply, Pi.smul_apply, zsmul_eq_mul] at h'
    rw [h']; push_cast; ring
  refine ⟨c x, v, ?_, ?_, ?_⟩
  · intro h0
    apply hne
    funext i
    have := hkey i
    rw [h0] at this
    simp at this
    linarith
  · intro i
    have hb := hkey i
    have hxi := hPB x hx i
    have hyi := hPB y hy i
    have hwi := hw i
    have habs : |y i - x i| < 1 := by
      rw [abs_lt]; constructor <;> linarith
    rwa [← hb, abs_mul, abs_of_pos (by linarith)] at habs
  · intro j hj i
    have hjm : (j : ℚ) ≤ ((k - 1 : ℕ) : ℚ) := by exact_mod_cast (by omega : j ≤ k - 1)
    have hpt : φ (c x + (j : ℤ) • v) i = x i + (j : ℚ) * φ v i := by
      rw [map_add, map_zsmul, hc x hx]
      simp only [Pi.add_apply, Pi.smul_apply]
      simp only [zsmul_eq_mul, Int.cast_natCast]
    rw [hpt]
    exact segment_in_box hm1 (hkey i) (hPB x hx i) (hPB y hy i) (by positivity) hjm

-- A step with all coordinates in `(-1, 1)` that is not zero is not in `ℤ^κ`:
-- it is a nonzero step of the torus.
theorem not_integral_of_small {κ : Type*} {v : κ → ℚ} (h0 : v ≠ 0)
    (h1 : ∀ i, |v i| < 1) : ¬ ∀ i, ∃ z : ℤ, v i = z := by
  intro hint
  apply h0
  funext i
  obtain ⟨z, hz⟩ := hint i
  have := h1 i
  rw [hz] at this ⊢
  have hz' : |z| < 1 := by exact_mod_cast this
  have : z = 0 := Int.abs_lt_one_iff.mp hz'
  simp [this]

/-! ## The torus lattice `ℤ^D + ℤ·u`, `D = n + 1` -/

/-- `u = (1/q, 1/q², …, 1/q^D)`. -/
noncomputable def u (q n : ℕ) : Fin (n + 1) → ℚ := fun i => 1 / (q : ℚ) ^ (i.val + 1)

/-- Points of `Λ = ℤ^D + ℤ·u`. -/
def InLattice (q n : ℕ) (x : Fin (n + 1) → ℚ) : Prop :=
  ∃ (m : ℤ) (z : Fin (n + 1) → ℤ), x = (m : ℚ) • u q n + fun i => (z i : ℚ)

theorem pow_mul_u {q n : ℕ} (hq : q ≠ 0) (i : Fin (n + 1)) :
    (q : ℚ) ^ (n + 1) * u q n i = (q : ℚ) ^ (n - i.val) := by
  have hq' : (q : ℚ) ≠ 0 := by exact_mod_cast hq
  have hsplit : (q : ℚ) ^ (n + 1) = (q : ℚ) ^ (i.val + 1) * (q : ℚ) ^ (n - i.val) := by
    rw [← pow_add]; congr 1; omega
  rw [hsplit, u]
  field_simp

/-- Coordinates of `Λ` in the basis `e₀, …, e_{D-2}, u`. -/
noncomputable def coord (q n : ℕ) : (Fin (n + 1) → ℤ) →+ (Fin (n + 1) → ℚ) where
  toFun c := fun i => (c (Fin.last n) : ℚ) * u q n i +
    if i = Fin.last n then 0 else (c i : ℚ)
  map_zero' := by funext i; simp
  map_add' := by
    intro c c'; funext i
    simp only [Pi.add_apply, Int.cast_add]
    split_ifs <;> ring

theorem mem_range_coord {q n : ℕ} (hq : q ≠ 0) (x : Fin (n + 1) → ℚ) :
    x ∈ Set.range (coord q n) ↔ InLattice q n x := by
  constructor
  · rintro ⟨c, rfl⟩
    refine ⟨c (Fin.last n), fun i => if i = Fin.last n then 0 else c i, ?_⟩
    funext i
    simp only [coord, AddMonoidHom.coe_mk, ZeroHom.coe_mk, Pi.add_apply, Pi.smul_apply,
      smul_eq_mul]
    split_ifs <;> simp
  · rintro ⟨m, z, rfl⟩
    let zl := z (Fin.last n)
    refine ⟨fun i => if i = Fin.last n then m + (q : ℤ) ^ (n + 1) * zl
      else z i - (q : ℤ) ^ (n - i.val) * zl, ?_⟩
    funext i
    have h := pow_mul_u hq i
    simp only [coord, AddMonoidHom.coe_mk, ZeroHom.coe_mk, Pi.add_apply, Pi.smul_apply,
      smul_eq_mul, if_pos rfl]
    by_cases hi : i = Fin.last n
    · subst hi
      simp only [if_pos rfl, add_zero]
      push_cast
      have h' : (q : ℚ) ^ (n + 1) * u q n (Fin.last n) = 1 := by
        rw [h]; simp
      linear_combination (zl : ℚ) * h'
    · simp only [if_neg hi]
      push_cast
      linear_combination (zl : ℚ) * h

/-- **Cell lemma for cyclic progressions (`C = 1`).** Let `N = q^D` and let a
half-open box `B̃` of widths `≤ 1` hold more than `(k-1)^D` points of
`Λ = ℤ^D + ℤ·u`. Then there are `m, d ∈ ℤ` with `d ≢ 0 (mod N)` such that, for
every `j < k`, the representative `(m + j d)·u` of `m + j d ∈ ℤ/N` has a lift in
`B̃`, and the `k` terms are distinct in `ℤ/N` (`N ∤ (i - j) d` for `j < i < k`):
the cell contains a `k`-term progression of `ℤ/N`. -/
theorem cyclic_cell_lemma (q n k : ℕ) (hq : q ≠ 0) (hk : 2 ≤ k)
    (a w : Fin (n + 1) → ℚ) (hw : ∀ i, w i ≤ 1)
    (P : Finset (Fin (n + 1) → ℚ)) (hPΛ : ∀ p ∈ P, InLattice q n p)
    (hPB : ∀ p ∈ P, InBox a w p) (hcard : (k - 1) ^ (n + 1) < P.card) :
    ∃ m d : ℤ, (∀ i j : ℕ, j < i → i < k → ¬ ((q : ℤ) ^ (n + 1) ∣ ((i : ℤ) - j) * d)) ∧
      ∀ j : ℕ, j < k → ∃ z : Fin (n + 1) → ℤ,
        InBox a w ((((m + j * d : ℤ)) : ℚ) • u q n + fun i => (z i : ℚ)) := by
  have hcard' : (k - 1) ^ Fintype.card (Fin (n + 1)) < P.card := by simpa using hcard
  obtain ⟨x, v, hv0, hv1, hbox⟩ := cell_lemma (coord q n) k hk a w hw P
    (fun p hp => (mem_range_coord hq p).2 (hPΛ p hp)) hPB hcard'
  obtain ⟨m, zx, hx⟩ := (mem_range_coord hq _).1 ⟨x, rfl⟩
  obtain ⟨d, zv, hvd⟩ := (mem_range_coord hq _).1 ⟨v, rfl⟩
  refine ⟨m, d, ?_, ?_⟩
  · -- `s = i - j ∈ [1, k-1]`: `s φ v` is nonzero and small, hence not in `ℤ^D`.
    rintro i j hji hik ⟨t, ht⟩
    have hsd : ((i - j : ℕ) : ℚ) * d = (q : ℚ) ^ (n + 1) * t := by
      rw [Nat.cast_sub hji.le]; exact_mod_cast ht
    have hsk : ((i - j : ℕ) : ℚ) ≤ ((k - 1 : ℕ) : ℚ) := by exact_mod_cast (by omega)
    have hs0 : ((i - j : ℕ) : ℚ) ≠ 0 := by exact_mod_cast (by omega : i - j ≠ 0)
    apply not_integral_of_small (v := ((i - j : ℕ) : ℚ) • coord q n v)
      (smul_ne_zero hs0 hv0)
    · intro l
      have := hv1 l
      simp only [Pi.smul_apply, smul_eq_mul, abs_mul, Nat.abs_cast]
      nlinarith [abs_nonneg (coord q n v l)]
    · intro l
      refine ⟨t * (q : ℤ) ^ (n - l.val) + ((i - j : ℕ) : ℤ) * zv l, ?_⟩
      rw [hvd]
      have h := pow_mul_u hq l
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      push_cast
      linear_combination (u q n l) * hsd + (t : ℚ) * h
  · intro j hj
    refine ⟨zx + (j : ℤ) • zv, ?_⟩
    have := hbox j hj
    rw [map_add, map_zsmul, hx, hvd] at this
    have hpt : ((((m + j * d : ℤ)) : ℚ) • u q n + fun i => ((zx + (j : ℤ) • zv) i : ℚ)) =
        ((m : ℚ) • u q n + fun i => (zx i : ℚ)) +
          (j : ℤ) • ((d : ℚ) • u q n + fun i => (zv i : ℚ)) := by
      funext i
      simp only [Pi.add_apply, Pi.smul_apply]
      simp only [smul_eq_mul, zsmul_eq_mul]
      push_cast
      ring
    rw [hpt]
    exact this

end CellLemma
