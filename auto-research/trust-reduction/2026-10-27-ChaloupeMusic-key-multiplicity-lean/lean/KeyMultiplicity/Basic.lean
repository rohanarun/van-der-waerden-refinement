import Mathlib

/-!
# Lemma 3 of `source-only-1-16`: a key occurs at most twice on a progression

Source: `Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers`
(OpenAI, 23/09/2026), §02 (`02-setup.tex`), §05 (`05-dichotomy.tex`) and §06
(`06-perturbation.tex`), with the parameters of `source-only-1-16` §2. Line
numbers refer to those files; the correspondence table is in the README.
-/

namespace KeyMultiplicity

open Finset Real

/-! ## The cyclic model and the key (source §02, §06) -/

/-- The centred representative `ỹ_i(n) ∈ [-1/2, 1/2)` of
`y_i(n) = λ x_i(n)`, `x_i(n) = n / q^i mod 1`, for `i = 1, …, D`
(02-setup l. 113-121); coordinate `i : Fin D` is the source's `i + 1`. -/
noncomputable def yt (q D lam : ℕ) (n : ZMod (q ^ D)) (i : Fin D) : ℝ :=
  (lam * n.val : ℝ) / (q : ℝ) ^ (i.val + 1)
    - round ((lam * n.val : ℝ) / (q : ℝ) ^ (i.val + 1))

/-- `f(n) = ‖q ỹ(n)‖²` (06-perturbation l. 15). -/
noncomputable def f (q D lam : ℕ) (n : ZMod (q ^ D)) : ℝ :=
  ∑ i, ((q : ℝ) * yt q D lam n i) ^ 2

/-- The key `κ(n) = ((V(y_i(n)))_i, ⌊f(n)⌋)` (06-perturbation l. 15), for a
mesh `V` read on the centred representatives. -/
noncomputable def key {β : Type*} (V : ℝ → β) (q D lam : ℕ) (n : ZMod (q ^ D)) :
    (Fin D → β) × ℤ :=
  (fun i => V (yt q D lam n i), ⌊f q D lam n⌋)

/-- The source's dilation `λ = ∏_{ℓ ≤ h₀ prime} ℓ^{⌊log(2M)/log ℓ⌋}`
(02-setup l. 24), with `⌊log(2M)/log ℓ⌋ = Nat.log ℓ (2M)`. -/
noncomputable def lam (h₀ M : ℕ) : ℕ :=
  ∏ ℓ ∈ (range (h₀ + 1)).filter Nat.Prime, ℓ ^ Nat.log ℓ (2 * M)

/-- `a_ℓ = α (e^{ℓR/m} − 1)` (02-setup l. 143-147). -/
noncomputable def meshA (α R : ℝ) (m : ℕ) (ℓ : ℤ) : ℝ :=
  α * (exp (ℓ * R / m) - 1)

/-- The adaptive mesh `V` (02-setup l. 149-153; zero to the right, l. 155-156): label `(false, ℓ)` for
`[-1/2 + a_ℓ, -1/2 + a_{ℓ+1})`, label `(true, ℓ)` for `[1/2 − a_{ℓ+1}, 1/2 − a_ℓ)`;
zero goes to the interval on its right. -/
noncomputable def meshV (α R : ℝ) (m : ℕ) (s : ℝ) : Bool × ℤ :=
  if s < 0 then (false, ⌊(m / R) * log (1 + (s + 1 / 2) / α)⌋)
  else (true, ⌈(m / R) * log (1 + (1 / 2 - s) / α)⌉ - 1)

/-! ## The mesh -/

/-- `a_ℓ ≤ x ↔ ℓ ≤ (m/R) log(1 + x/α)`, the inversion behind `meshV`. -/
lemma meshA_le_iff {α R x : ℝ} {m : ℕ} (hα : 0 < α) (hR : 0 < R) (hm : 0 < m)
    (hx : 0 ≤ x) (ℓ : ℤ) :
    meshA α R m ℓ ≤ x ↔ (ℓ : ℝ) ≤ (m / R) * log (1 + x / α) := by
  have h1 : 0 < 1 + x / α := by positivity
  have hm' : (0 : ℝ) < m := by exact_mod_cast hm
  rw [meshA, mul_comm α, ← le_div_iff₀ hα, sub_le_iff_le_add', ← Real.le_log_iff_exp_le h1,
    div_le_iff₀ hm', mul_comm ((m : ℝ) / R), ← mul_div_assoc, le_div_iff₀ hR]

lemma lt_meshA_iff {α R x : ℝ} {m : ℕ} (hα : 0 < α) (hR : 0 < R) (hm : 0 < m)
    (hx : 0 ≤ x) (ℓ : ℤ) :
    x < meshA α R m ℓ ↔ (m / R) * log (1 + x / α) < ℓ := by
  rw [lt_iff_not_ge, lt_iff_not_ge, meshA_le_iff hα hR hm hx]

lemma meshA_lt_iff {α R x : ℝ} {m : ℕ} (hα : 0 < α) (hR : 0 < R) (hm : 0 < m)
    (hx : 0 ≤ x) (ℓ : ℤ) :
    meshA α R m ℓ < x ↔ (ℓ : ℝ) < (m / R) * log (1 + x / α) := by
  have h1 : 0 < 1 + x / α := by positivity
  have hm' : (0 : ℝ) < m := by exact_mod_cast hm
  rw [meshA, mul_comm α, ← lt_div_iff₀ hα, sub_lt_iff_lt_add', ← Real.lt_log_iff_exp_lt h1,
    div_lt_iff₀ hm', mul_comm ((m : ℝ) / R), ← mul_div_assoc, lt_div_iff₀ hR]

lemma le_meshA_iff {α R x : ℝ} {m : ℕ} (hα : 0 < α) (hR : 0 < R) (hm : 0 < m)
    (hx : 0 ≤ x) (ℓ : ℤ) :
    x ≤ meshA α R m ℓ ↔ (m / R) * log (1 + x / α) ≤ ℓ := by
  rw [← not_lt, ← not_lt, meshA_lt_iff hα hR hm hx]

lemma log_mesh_pos {α : ℝ} (hα : 0 < α) : 0 < log (1 + 1 / (2 * α)) :=
  Real.log_pos (by have : 0 < 1 / (2 * α) := by positivity
                   linarith)

/-- `meshV` is the source's partition: each label names the interval
(02-setup l. 149-153) that contains the point, with `0 ≤ ℓ < m`. -/
theorem meshV_spec (α : ℝ) (m : ℕ) (hα : 0 < α) (hm : 0 < m) (s : ℝ)
    (hs : s ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2)) :
    let R := log (1 + 1 / (2 * α))
    let ℓ := (meshV α R m s).2
    0 ≤ ℓ ∧ ℓ < m ∧
      if (meshV α R m s).1 then meshA α R m ℓ < 1 / 2 - s ∧ 1 / 2 - s ≤ meshA α R m (ℓ + 1)
      else meshA α R m ℓ ≤ s + 1 / 2 ∧ s + 1 / 2 < meshA α R m (ℓ + 1) := by
  intro R ℓ
  have hR : 0 < R := log_mesh_pos hα
  have hm' : (0 : ℝ) < m := by exact_mod_cast hm
  have hmR : 0 < (m : ℝ) / R := by positivity
  obtain ⟨hs1, hs2⟩ := hs
  -- `log (1 + x/α) < R` for `x < 1/2`, `≤ R` for `x ≤ 1/2`
  have hlt : ∀ x : ℝ, 0 ≤ x → x < 1 / 2 → log (1 + x / α) < R := fun x hx0 hx =>
    Real.log_lt_log (by positivity) (by
      have : x / α < 1 / (2 * α) := by rw [div_lt_div_iff₀ hα (by positivity)]; nlinarith
      linarith)
  have hle : ∀ x : ℝ, 0 ≤ x → x ≤ 1 / 2 → log (1 + x / α) ≤ R := fun x hx0 hx =>
    Real.log_le_log (by positivity) (by
      have : x / α ≤ 1 / (2 * α) := by rw [div_le_div_iff₀ hα (by positivity)]; nlinarith
      linarith)
  by_cases hs0 : s < 0
  · have hx0 : 0 ≤ s + 1 / 2 := by linarith
    have hL0 : 0 ≤ log (1 + (s + 1 / 2) / α) := Real.log_nonneg (by
      have : 0 ≤ (s + 1 / 2) / α := by positivity
      linarith)
    have hLR := hlt (s + 1 / 2) hx0 (by linarith)
    simp only [ℓ, meshV, if_pos hs0, Bool.false_eq_true, ↓reduceIte]
    refine ⟨Int.floor_nonneg.mpr (by positivity), Int.floor_lt.mpr ?_,
      (meshA_le_iff hα hR hm hx0 _).mpr (Int.floor_le _),
      (lt_meshA_iff hα hR hm hx0 _).mpr (by push_cast; exact Int.lt_floor_add_one _)⟩
    calc (m : ℝ) / R * log (1 + (s + 1 / 2) / α) < (m / R) * R :=
          mul_lt_mul_of_pos_left hLR hmR
      _ = ((m : ℤ) : ℝ) := by field_simp
  · have hx0 : 0 < 1 / 2 - s := by linarith
    have hL0 : 0 < log (1 + (1 / 2 - s) / α) := Real.log_pos (by
      have : 0 < (1 / 2 - s) / α := by positivity
      linarith)
    have hLR := hle (1 / 2 - s) hx0.le (by linarith)
    simp only [ℓ, meshV, if_neg hs0, ↓reduceIte]
    refine ⟨by have := Int.ceil_pos.mpr (mul_pos hmR hL0); omega, ?_,
      (meshA_lt_iff hα hR hm hx0.le _).mpr ?_, (le_meshA_iff hα hR hm hx0.le _).mpr ?_⟩
    · have : ⌈(m : ℝ) / R * log (1 + (1 / 2 - s) / α)⌉ ≤ m := Int.ceil_le.mpr (by
        calc (m : ℝ) / R * log (1 + (1 / 2 - s) / α) ≤ (m / R) * R :=
              mul_le_mul_of_nonneg_left hLR hmR.le
          _ = ((m : ℤ) : ℝ) := by field_simp)
      omega
    · push_cast; linarith [Int.ceil_lt_add_one ((m : ℝ) / R * log (1 + (1 / 2 - s) / α))]
    · push_cast; linarith [Int.le_ceil ((m : ℝ) / R * log (1 + (1 / 2 - s) / α))]

/-- `a_ℓ ≤ 1/2` for `ℓ ≤ m` (indeed `a_m = 1/2`). -/
lemma meshA_le_half {α : ℝ} {m : ℕ} (hα : 0 < α) (hm : 0 < m) (ℓ : ℤ) (hℓ : ℓ ≤ m) :
    meshA α (log (1 + 1 / (2 * α))) m ℓ ≤ 1 / 2 := by
  have hR := log_mesh_pos hα
  have hm' : (0 : ℝ) < m := by exact_mod_cast hm
  rw [meshA_le_iff hα hR hm (by norm_num), show 1 + 1 / 2 / α = 1 + 1 / (2 * α) by ring,
    div_mul_cancel₀ _ hR.ne']
  exact_mod_cast hℓ

lemma meshA_nonneg {α R : ℝ} {m : ℕ} (hα : 0 < α) (hR : 0 < R) (hm : 0 < m) (ℓ : ℤ)
    (hℓ : 0 ≤ ℓ) : 0 ≤ meshA α R m ℓ := by
  have : (0 : ℝ) ≤ ℓ * R / m := by have : (0 : ℝ) ≤ ℓ := by exact_mod_cast hℓ
                                   positivity
  unfold meshA
  have := one_le_exp this
  nlinarith

/-- The converse of `meshV_spec`: a point of the source's interval named
`(b, ℓ)`, `0 ≤ ℓ < m`, gets the label `(b, ℓ)`. So the named intervals are
pairwise disjoint and `meshV` is exactly the partition of 02-setup l. 149-156. -/
theorem meshV_of_mem (α : ℝ) (m : ℕ) (hα : 0 < α) (hm : 0 < m) (s : ℝ) (ℓ : ℤ)
    (hℓ0 : 0 ≤ ℓ) (hℓ : ℓ < m) :
    let R := log (1 + 1 / (2 * α))
    (meshA α R m ℓ ≤ s + 1 / 2 ∧ s + 1 / 2 < meshA α R m (ℓ + 1) → meshV α R m s = (false, ℓ)) ∧
      (meshA α R m ℓ < 1 / 2 - s ∧ 1 / 2 - s ≤ meshA α R m (ℓ + 1) →
        meshV α R m s = (true, ℓ)) := by
  intro R
  have hR : 0 < R := log_mesh_pos hα
  have h0 := meshA_nonneg hα hR hm ℓ hℓ0
  have hhalf := meshA_le_half hα hm (ℓ + 1) (by omega)
  constructor
  · rintro ⟨h1, h2⟩
    have hs : s < 0 := by linarith
    have hx : 0 ≤ s + 1 / 2 := by linarith
    simp only [meshV, if_pos hs, Prod.mk.injEq, true_and]
    rw [Int.floor_eq_iff]
    exact ⟨(meshA_le_iff hα hR hm hx ℓ).mp h1, by
      have := (lt_meshA_iff hα hR hm hx (ℓ + 1)).mp h2; push_cast at this; exact this⟩
  · rintro ⟨h1, h2⟩
    have hs : ¬ s < 0 := by linarith
    have hx : 0 ≤ 1 / 2 - s := by linarith
    simp only [meshV, if_neg hs, Prod.mk.injEq, true_and]
    have hc : ⌈(m : ℝ) / R * log (1 + (1 / 2 - s) / α)⌉ = ℓ + 1 := by
      rw [Int.ceil_eq_iff]
      constructor
      · have := (meshA_lt_iff hα hR hm hx ℓ).mp h1; push_cast; linarith
      · have := (le_meshA_iff hα hR hm hx (ℓ + 1)).mp h2; push_cast at this ⊢; exact this
    omega

/-- `a_{ℓ+1} − a_ℓ ≤ H` for `0 ≤ ℓ < m` when `R ≤ m H` and `α ≤ 1/2`. -/
lemma meshA_gap (α H : ℝ) (m : ℕ) (hα : 0 < α) (hα2 : α ≤ 1 / 2) (hm : 0 < m)
    (hmR : log (1 + 1 / (2 * α)) ≤ m * H) (ℓ : ℤ) (hℓ : ℓ < m) :
    let R := log (1 + 1 / (2 * α))
    meshA α R m (ℓ + 1) - meshA α R m ℓ ≤ H := by
  intro R
  have hR : 0 < R := log_mesh_pos hα
  have hm' : (0 : ℝ) < m := by exact_mod_cast hm
  have hθ : R / m ≤ H := by rw [div_le_iff₀ hm']; linarith
  have hθ0 : 0 < R / m := by positivity
  set E := exp (((ℓ : ℝ) + 1) * R / m) with hEdef
  have hE : α * E ≤ 1 := by
    have hℓ' : (ℓ : ℝ) + 1 ≤ m := by exact_mod_cast hℓ
    have : E ≤ exp R := exp_le_exp.mpr (by
      rw [div_le_iff₀ hm']; nlinarith)
    rw [exp_log (by positivity)] at this
    have h2 : α * (1 + 1 / (2 * α)) = α + 1 / 2 := by field_simp; ring
    nlinarith
  have hexp : exp ((ℓ : ℝ) * R / m) = E * exp (-(R / m)) := by
    rw [hEdef, ← exp_add]; congr 1; ring
  have h1 : 1 - exp (-(R / m)) ≤ R / m := by linarith [add_one_le_exp (-(R / m))]
  have h2 : 0 ≤ 1 - exp (-(R / m)) := by
    have := exp_le_one_iff.mpr (neg_nonpos.mpr hθ0.le); linarith
  have hgap : meshA α R m (ℓ + 1) - meshA α R m ℓ = α * E * (1 - exp (-(R / m))) := by
    simp only [meshA]; push_cast; rw [hexp]; ring
  rw [hgap]
  have hαE : 0 ≤ α * E := by positivity
  nlinarith

/-- Width of the mesh (02-setup l. 175, `|I| ≤ 2H`; here `< H`): two
representatives with the same label are less than `H` apart when `R ≤ m H`
(the source's `m = ⌈k² R⌉`, `H = k⁻²`, l. 143-147 and l. 13-19) and `α ≤ 1/2`. -/
theorem meshV_width (α H : ℝ) (m : ℕ) (hα : 0 < α) (hα2 : α ≤ 1 / 2)
    (hmR : log (1 + 1 / (2 * α)) ≤ m * H) (s t : ℝ)
    (hs : s ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2)) (ht : t ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2))
    (hst : meshV α (log (1 + 1 / (2 * α))) m s = meshV α (log (1 + 1 / (2 * α))) m t) :
    |s - t| < H := by
  have hm : 0 < m := by
    rcases Nat.eq_zero_or_pos m with h | h
    · subst h; have := log_mesh_pos hα; simp only [Nat.cast_zero, zero_mul] at hmR; linarith
    · exact h
  obtain ⟨hs0, hs1, hsI⟩ := meshV_spec α m hα hm s hs
  obtain ⟨-, -, htI⟩ := meshV_spec α m hα hm t ht
  have hgap := meshA_gap α H m hα hα2 hm hmR _ hs1
  rw [← hst] at htI
  simp only at hsI htI hgap
  split_ifs at hsI htI <;> rw [abs_lt] <;> constructor <;> linarith [hsI.1, hsI.2, htI.1, htI.2]

/-! ## The cyclic model -/

lemma yt_mem (q D lam : ℕ) (n : ZMod (q ^ D)) (i : Fin D) :
    yt q D lam n i ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2) := by
  unfold yt
  set t : ℝ := (lam * n.val : ℝ) / (q : ℝ) ^ (i.val + 1)
  rw [round_eq]
  constructor
  · linarith [Int.floor_le (t + 1 / 2)]
  · linarith [Int.lt_floor_add_one (t + 1 / 2)]

/-- `val(n₀ + j d) = val n₀ + j val d − N c` for an integer `c`. -/
lemma val_add_mul (N : ℕ) [NeZero N] (n₀ d : ZMod N) (j : ℕ) :
    ∃ c : ℤ, ((n₀ + j * d).val : ℤ) = n₀.val + j * d.val - N * c := by
  have h : ((((n₀ + j * d).val : ℤ) - (n₀.val + j * d.val) : ℤ) : ZMod N) = 0 := by
    push_cast; simp [ZMod.natCast_zmod_val]
  obtain ⟨c, hc⟩ := (ZMod.intCast_zmod_eq_zero_iff_dvd _ N).1 h
  exact ⟨-c, by linarith⟩

/-- Along a progression each centred coordinate is affine in `j` modulo
integers: `ỹ_i(n₀ + j d) = a + j b − M_j` (the torus line `z_j = a + j b` of
05-dichotomy l. 12). -/
lemma yt_affine (q D lam : ℕ) (hq : 0 < q) (n₀ d : ZMod (q ^ D)) (i : Fin D) (j : ℕ) :
    ∃ M : ℤ, yt q D lam (n₀ + j * d) i =
      (lam * n₀.val : ℝ) / (q : ℝ) ^ (i.val + 1) + j * ((lam * d.val : ℝ) / (q : ℝ) ^ (i.val + 1))
        - M := by
  haveI : NeZero (q ^ D) := ⟨by positivity⟩
  obtain ⟨c, hc⟩ := val_add_mul (q ^ D) n₀ d j
  have hcR : (((n₀ + j * d).val : ℕ) : ℝ) = n₀.val + j * d.val - ((q : ℝ) ^ D) * c := by
    exact_mod_cast hc
  have hqD : (q : ℝ) ^ D = (q : ℝ) ^ (i.val + 1) * (q : ℝ) ^ (D - (i.val + 1)) := by
    rw [← pow_add]; congr 1; omega
  refine ⟨lam * c * q ^ (D - (i.val + 1))
    + round ((lam * (n₀ + j * d).val : ℝ) / (q : ℝ) ^ (i.val + 1)), ?_⟩
  have hq' : (0 : ℝ) < (q : ℝ) ^ (i.val + 1) := by positivity
  unfold yt
  rw [hcR, hqD]
  push_cast
  field_simp
  ring

/-- Two different points of `ℤ/q^D` are at distance at least one after scaling
by `q` (06-perturbation l. 44-66, the separation (perturb:separation)). Only
`gcd(λ, q) = 1` is used. -/
theorem separation (q D lam : ℕ) (hq : 0 < q) (hlam : Nat.Coprime lam q)
    (n n' : ZMod (q ^ D)) (hnn : n ≠ n') :
    1 ≤ ∑ i, ((q : ℝ) * yt q D lam n i - (q : ℝ) * yt q D lam n' i) ^ 2 := by
  haveI : NeZero (q ^ D) := ⟨by positivity⟩
  set δ : ℤ := (n.val : ℤ) - n'.val with hδ
  have hδ0 : δ ≠ 0 := by
    intro h; apply hnn; apply ZMod.val_injective; omega
  have hδN : ¬ ((q ^ D : ℕ) : ℤ) ∣ δ := by
    intro h
    have h1 := ZMod.val_lt n; have h2 := ZMod.val_lt n'
    exact hδ0 (Int.eq_zero_of_dvd_of_natAbs_lt_natAbs h (by omega))
  set z : ℤ := lam * δ with hz
  have hzN : ¬ (q : ℤ) ^ D ∣ z := by
    intro h
    have hc : IsCoprime ((q ^ D : ℕ) : ℤ) (lam : ℤ) :=
      Nat.isCoprime_iff_coprime.mpr (Nat.Coprime.pow_left D hlam.symm)
    exact hδN (hc.dvd_of_dvd_mul_left (by push_cast; exact h))
  have hD : D ≠ 0 := by rintro rfl; exact hzN (by simp)
  have hex : ∃ a, ¬ (q : ℤ) ^ (a + 1) ∣ z := ⟨D - 1, by rwa [Nat.sub_add_cancel (by omega)]⟩
  classical
  set a := Nat.find hex with ha
  have haz : ¬ (q : ℤ) ^ (a + 1) ∣ z := Nat.find_spec hex
  have haD : a < D := by
    have := Nat.find_min' hex (show ¬ (q : ℤ) ^ (D - 1 + 1) ∣ z by
      rwa [Nat.sub_add_cancel (by omega)])
    omega
  have hqa : (q : ℤ) ^ a ∣ z := by
    rcases Nat.eq_zero_or_pos a with h0 | h0
    · rw [h0]; simp
    · have := Nat.find_min hex (show a - 1 < a by omega)
      rw [not_not, Nat.sub_add_cancel h0] at this
      exact this
  obtain ⟨u, hu⟩ := hqa
  have hqu : ¬ (q : ℤ) ∣ u := by
    rintro ⟨v, hv⟩; apply haz; exact ⟨v, by rw [hu, hv, pow_succ]; ring⟩
  let i : Fin D := ⟨a, haD⟩
  set t : ℝ := (lam * n.val : ℝ) / (q : ℝ) ^ (a + 1)
  set t' : ℝ := (lam * n'.val : ℝ) / (q : ℝ) ^ (a + 1)
  set m : ℤ := u - q * (round t - round t')
  have hm0 : m ≠ 0 := by
    intro h; apply hqu; exact ⟨round t - round t', by linarith⟩
  have hqR : (0 : ℝ) < q := by exact_mod_cast hq
  have hzR : (z : ℝ) = (lam : ℝ) * n.val - lam * n'.val := by
    rw [hz, hδ]; push_cast; ring
  have hcoord : (q : ℝ) * yt q D lam n i - (q : ℝ) * yt q D lam n' i = m := by
    have huR : (z : ℝ) = (q : ℝ) ^ a * u := by rw [hu]; push_cast; ring
    have : t - t' = (u : ℝ) / q := by
      simp only [t, t']
      rw [← sub_div, ← hzR, huR, pow_succ]
      field_simp
      ring
    simp only [yt, i, m]
    push_cast
    rw [show (q : ℝ) * (t - round t) - q * (t' - round t') = q * (t - t') - q * (round t - round t')
      by ring, this]
    field_simp
  have h1 : (1 : ℝ) ≤ |(m : ℝ)| := by
    rw [← Int.cast_abs]; exact_mod_cast Int.one_le_abs hm0
  calc (1 : ℝ) ≤ ((q : ℝ) * yt q D lam n i - (q : ℝ) * yt q D lam n' i) ^ 2 := by
        rw [hcoord, ← sq_abs]; nlinarith
    _ ≤ _ := Finset.single_le_sum
          (f := fun j => ((q : ℝ) * yt q D lam n j - (q : ℝ) * yt q D lam n' j) ^ 2)
          (fun j _ => sq_nonneg _) (Finset.mem_univ i)

/-- The `k` terms are distinct when `P > k` (02-setup l. 109-110). -/
theorem terms_ne (P e D k : ℕ) (hP : P.Prime) (hkP : k < P) (n₀ d : ZMod ((P ^ e) ^ D))
    (hd : d ≠ 0) {j j' : ℕ} (hj : j < j') (hj' : j' < k) :
    n₀ + j * d ≠ n₀ + j' * d := by
  intro h
  have h1 : ((j' - j : ℕ) : ZMod ((P ^ e) ^ D)) * d = 0 := by
    rw [Nat.cast_sub hj.le]; linear_combination -h
  have hc : Nat.Coprime (j' - j) ((P ^ e) ^ D) :=
    Nat.Coprime.pow_right _ (Nat.Coprime.pow_right _ (Nat.Coprime.symm
      ((Nat.Prime.coprime_iff_not_dvd hP).2 (Nat.not_dvd_of_pos_of_lt (by omega) (by omega)))))
  have hu : IsUnit ((j' - j : ℕ) : ZMod ((P ^ e) ^ D)) := by
    rw [← ZMod.coe_unitOfCoprime _ hc]; exact Units.isUnit _
  exact hd (hu.mul_right_eq_zero.mp h1)

/-! ## Multiplicity two (note §3, Lemma 3) -/

/-- Affinity inside a small box (05-dichotomy l. 11-31), for three indices:
the integer `(j₃−j₂)(M₂−M₁) − (j₂−j₁)(M₃−M₂)` has absolute value `< k w < 1`. -/
lemma three_affine (k : ℕ) (w : ℝ) (hw : 0 ≤ w) (hkw : k * w < 1) {x y z : ℕ}
    (hxy : x < y) (hyz : y < z) (hz : z < k) (a b : ℝ) (Mx My Mz : ℤ) {Yx Yy Yz : ℝ}
    (hYx : Yx = a + x * b - Mx) (hYy : Yy = a + y * b - My) (hYz : Yz = a + z * b - Mz)
    (h1 : |Yy - Yx| ≤ w) (h2 : |Yz - Yy| ≤ w) :
    ((z : ℝ) - y) * (Yy - Yx) = ((y : ℝ) - x) * (Yz - Yy) := by
  set E : ℤ := ((y : ℤ) - x) * (Mz - My) - ((z : ℤ) - y) * (My - Mx) with hEdef
  have hE : ((z : ℝ) - y) * (Yy - Yx) - ((y : ℝ) - x) * (Yz - Yy) = E := by
    rw [hEdef, hYx, hYy, hYz]; push_cast; ring
  have hxyR : (x : ℝ) < y := by exact_mod_cast hxy
  have hyzR : (y : ℝ) < z := by exact_mod_cast hyz
  have hzk : (z : ℝ) - x ≤ k := by
    have : (z : ℝ) ≤ k := by exact_mod_cast hz.le
    have : (0 : ℝ) ≤ x := Nat.cast_nonneg x
    linarith
  have hb : |((z : ℝ) - y) * (Yy - Yx) - ((y : ℝ) - x) * (Yz - Yy)| < 1 := by
    calc _ ≤ |((z : ℝ) - y) * (Yy - Yx)| + |((y : ℝ) - x) * (Yz - Yy)| := abs_sub _ _
      _ = ((z : ℝ) - y) * |Yy - Yx| + ((y : ℝ) - x) * |Yz - Yy| := by
          rw [abs_mul, abs_mul, abs_of_pos (sub_pos.mpr hyzR), abs_of_pos (sub_pos.mpr hxyR)]
      _ ≤ ((z : ℝ) - y) * w + ((y : ℝ) - x) * w := by
          gcongr
          · linarith
          · linarith
      _ = ((z : ℝ) - x) * w := by ring
      _ ≤ k * w := by gcongr
      _ < 1 := hkw
  rw [hE, ← Int.cast_abs] at hb
  have hE0 : E = 0 := Int.abs_lt_one_iff.mp (by exact_mod_cast hb)
  rw [hE0, Int.cast_zero] at hE
  linarith

/-- The three-point identity of PR #10 (rohanarun, `formal/Vdw/Geometry.lean`,
`no_three_in_unit_band`, commit `815a4c0`), on one coordinate of three
collinear points `p₁, p₂, p₃` at parameters `x < y < z`. -/
lemma three_point_left {x y z p1 p2 p3 : ℝ} (h : (z - y) * (p2 - p1) = (y - x) * (p3 - p2)) :
    (y - x) * ((z - y) * p1 ^ 2 + (y - x) * p3 ^ 2 - (z - x) * p2 ^ 2)
      = (z - y) * (z - x) * (p2 - p1) ^ 2 := by
  linear_combination (-(2 * (y - x) * p2 + (y - x) * (p3 - p2) + (z - y) * (p2 - p1))) * h

lemma three_point_right {x y z p1 p2 p3 : ℝ} (h : (z - y) * (p2 - p1) = (y - x) * (p3 - p2)) :
    (z - y) * ((z - y) * p1 ^ 2 + (y - x) * p3 ^ 2 - (z - x) * p2 ^ 2)
      = (y - x) * (z - x) * (p3 - p2) ^ 2 := by
  linear_combination (-2 * (z - y) * p2 + (z - y) * (p2 - p1) + (y - x) * (p3 - p2)) * h

/-- Three positions `x < y < z` of a progression with pairwise distinct terms
never share a key (note §3: affine line, separation, band). -/
lemma no_three {β : Type*} (q D k lam : ℕ) (hq : 0 < q) (hlq : Nat.Coprime lam q)
    (V : ℝ → β) (w : ℝ)
    (hV : ∀ s ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2), ∀ t ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2),
      V s = V t → |s - t| ≤ w)
    (hw : 0 ≤ w) (hkw : k * w < 1) (n₀ d : ZMod (q ^ D))
    (hdist : ∀ {j j' : ℕ}, j < j' → j' < k → n₀ + j * d ≠ n₀ + j' * d) (κ₀ : (Fin D → β) × ℤ)
    (x y z : ℕ) (hxy : x < y) (hyz : y < z) (hzk : z < k)
    (kx : key V q D lam (n₀ + x * d) = κ₀) (ky : key V q D lam (n₀ + y * d) = κ₀)
    (kz : key V q D lam (n₀ + z * d) = κ₀) : False := by
  have kxy := kx.trans ky.symm
  have kyz := ky.trans kz.symm
  simp only [key, Prod.mk.injEq] at kxy kyz
  -- collinearity, coordinate by coordinate
  have hrel : ∀ i : Fin D,
      ((z : ℝ) - y) * ((q : ℝ) * yt q D lam (n₀ + y * d) i - (q : ℝ) * yt q D lam (n₀ + x * d) i)
        = ((y : ℝ) - x) *
          ((q : ℝ) * yt q D lam (n₀ + z * d) i - (q : ℝ) * yt q D lam (n₀ + y * d) i) := by
    intro i
    obtain ⟨Mx, hMx⟩ := yt_affine q D lam hq n₀ d i x
    obtain ⟨My, hMy⟩ := yt_affine q D lam hq n₀ d i y
    obtain ⟨Mz, hMz⟩ := yt_affine q D lam hq n₀ d i z
    have h1 := hV _ (yt_mem q D lam _ i) _ (yt_mem q D lam _ i) (congrFun kxy.1 i).symm
    have h2 := hV _ (yt_mem q D lam _ i) _ (yt_mem q D lam _ i) (congrFun kyz.1 i).symm
    have := three_affine k w hw hkw hxy hyz hzk _ _ Mx My Mz hMx hMy hMz h1 h2
    linear_combination (q : ℝ) * this
  -- the identities, summed over the coordinates
  set B := ((z : ℝ) - y) * f q D lam (n₀ + x * d) + ((y : ℝ) - x) * f q D lam (n₀ + z * d)
    - ((z : ℝ) - x) * f q D lam (n₀ + y * d) with hB
  have hBsum : ∀ c : ℝ, c * B = ∑ i, c * (((z : ℝ) - y) * ((q : ℝ) * yt q D lam (n₀ + x * d) i) ^ 2
      + ((y : ℝ) - x) * ((q : ℝ) * yt q D lam (n₀ + z * d) i) ^ 2
      - ((z : ℝ) - x) * ((q : ℝ) * yt q D lam (n₀ + y * d) i) ^ 2) := by
    intro c
    simp only [hB, f, Finset.mul_sum, Finset.sum_add_distrib, Finset.sum_sub_distrib,
      mul_add, mul_sub]
  have hB1 : ((y : ℝ) - x) * B = ((z : ℝ) - y) * ((z : ℝ) - x) *
      ∑ i, ((q : ℝ) * yt q D lam (n₀ + y * d) i - (q : ℝ) * yt q D lam (n₀ + x * d) i) ^ 2 := by
    rw [hBsum, Finset.mul_sum]
    exact Finset.sum_congr rfl fun i _ => three_point_left (hrel i)
  have hB3 : ((z : ℝ) - y) * B = ((y : ℝ) - x) * ((z : ℝ) - x) *
      ∑ i, ((q : ℝ) * yt q D lam (n₀ + z * d) i - (q : ℝ) * yt q D lam (n₀ + y * d) i) ^ 2 := by
    rw [hBsum, Finset.mul_sum]
    exact Finset.sum_congr rfl fun i _ => three_point_right (hrel i)
  -- separation
  have hS1 := separation q D lam hq hlq _ _ (hdist hxy (by omega)).symm
  have hS3 := separation q D lam hq hlq _ _ (hdist hyz hzk).symm
  -- the band: three squared norms in `[m, m + 1)`
  have hxR : (x : ℝ) < y := by exact_mod_cast hxy
  have hyR : (y : ℝ) < z := by exact_mod_cast hyz
  have hfx := Int.floor_le (f q D lam (n₀ + x * d))
  have hfx' := Int.lt_floor_add_one (f q D lam (n₀ + x * d))
  have hfy := Int.floor_le (f q D lam (n₀ + y * d))
  have hfz' := Int.lt_floor_add_one (f q D lam (n₀ + z * d))
  rw [kxy.2] at hfx hfx'
  rw [← kyz.2] at hfz'
  have hBlt : B < (z : ℝ) - x := by
    have a1 := mul_lt_mul_of_pos_left hfx' (sub_pos.mpr hyR)
    have a2 := mul_lt_mul_of_pos_left hfz' (sub_pos.mpr hxR)
    have a3 := mul_le_mul_of_nonneg_left hfy (by linarith : (0 : ℝ) ≤ z - x)
    rw [hB]; nlinarith
  have hzx : (0 : ℝ) < z - x := by linarith
  have ha : ((z : ℝ) - y) * (z - x) < ((y : ℝ) - x) * (z - x) := by
    calc ((z : ℝ) - y) * (z - x) ≤ ((z : ℝ) - y) * (z - x) * _ :=
          le_mul_of_one_le_right (by nlinarith) hS1
      _ = ((y : ℝ) - x) * B := hB1.symm
      _ < ((y : ℝ) - x) * (z - x) := mul_lt_mul_of_pos_left hBlt (by linarith)
  have hb : ((y : ℝ) - x) * (z - x) < ((z : ℝ) - y) * (z - x) := by
    calc ((y : ℝ) - x) * (z - x) ≤ ((y : ℝ) - x) * (z - x) * _ :=
          le_mul_of_one_le_right (by nlinarith) hS3
      _ = ((z : ℝ) - y) * B := hB3.symm
      _ < ((z : ℝ) - y) * (z - x) := mul_lt_mul_of_pos_left hBlt (by linarith)
  have := lt_of_mul_lt_mul_right ha hzx.le
  have := lt_of_mul_lt_mul_right hb hzx.le
  linarith

/-- **Lemma 3, for any mesh of width `w` with `k w < 1`.** On a progression
`n_j = n₀ + j d`, `d ≠ 0`, `0 ≤ j < k`, of `ℤ/q^D`, `q = P^e` with `P > k`
prime and `λ` prime to `P`, every key occurs at most twice. -/
theorem mult_le_two {β : Type*} [DecidableEq β] (P e D k lam : ℕ) (hP : P.Prime)
    (hkP : k < P) (hlam : Nat.Coprime lam P) (V : ℝ → β) (w : ℝ)
    (hV : ∀ s ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2), ∀ t ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2),
      V s = V t → |s - t| ≤ w)
    (hkw : k * w < 1) (n₀ d : ZMod ((P ^ e) ^ D)) (hd : d ≠ 0)
    (κ₀ : (Fin D → β) × ℤ) :
    ((range k).filter fun j : ℕ => key V (P ^ e) D lam (n₀ + j * d) = κ₀).card ≤ 2 := by
  have hq : 0 < P ^ e := pow_pos hP.pos e
  have hlq : Nat.Coprime lam (P ^ e) := Nat.Coprime.pow_right _ hlam
  have hw : 0 ≤ w := by
    have := hV 0 ⟨by norm_num, by norm_num⟩ 0 ⟨by norm_num, by norm_num⟩ rfl
    simpa using this
  have no3 := fun x y z hxy hyz hzk kx ky kz =>
    no_three (P ^ e) D k lam hq hlq V w hV hw hkw n₀ d
      (fun hj hj' => terms_ne P e D k hP hkP n₀ d hd hj hj') κ₀ x y z hxy hyz hzk kx ky kz
  by_contra hcon
  push_neg at hcon
  obtain ⟨a, ha, b, hb, c, hc, hab, hac, hbc⟩ := Finset.two_lt_card.mp hcon
  simp only [mem_filter, mem_range] at ha hb hc
  rcases lt_or_gt_of_ne hab with h1 | h1 <;> rcases lt_or_gt_of_ne hac with h2 | h2 <;>
    rcases lt_or_gt_of_ne hbc with h3 | h3 <;>
    first
    | exact no3 a b c (by omega) (by omega) (by omega) ha.2 hb.2 hc.2
    | exact no3 a c b (by omega) (by omega) (by omega) ha.2 hc.2 hb.2
    | exact no3 b a c (by omega) (by omega) (by omega) hb.2 ha.2 hc.2
    | exact no3 b c a (by omega) (by omega) (by omega) hb.2 hc.2 ha.2
    | exact no3 c a b (by omega) (by omega) (by omega) hc.2 ha.2 hb.2
    | exact no3 c b a (by omega) (by omega) (by omega) hc.2 hb.2 ha.2

/-- Hence at least `⌈k/2⌉ = (k + 1) / 2` distinct keys on the progression. -/
theorem distinct_keys {β : Type*} [DecidableEq β] (P e D k lam : ℕ) (hP : P.Prime)
    (hkP : k < P) (hlam : Nat.Coprime lam P) (V : ℝ → β) (w : ℝ)
    (hV : ∀ s ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2), ∀ t ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2),
      V s = V t → |s - t| ≤ w)
    (hkw : k * w < 1) (n₀ d : ZMod ((P ^ e) ^ D)) (hd : d ≠ 0) :
    (k + 1) / 2 ≤ ((range k).image fun j : ℕ => key V (P ^ e) D lam (n₀ + j * d)).card := by
  have h := Finset.card_le_mul_card_image (f := fun j : ℕ => key V (P ^ e) D lam (n₀ + j * d))
    (range k) 2 (fun κ₀ _ => mult_le_two P e D k lam hP hkP hlam V w hV hkw n₀ d hd κ₀)
  rw [card_range] at h
  omega

/-- Where "`λ` has only prime factors `≤ h₀`" enters: `h₀ < P` makes the
source's `λ` prime to `P`, hence to `q` (02-setup l. 90-92). -/
theorem lam_coprime (h₀ M P : ℕ) (hP : P.Prime) (hh₀ : h₀ < P) : Nat.Coprime (lam h₀ M) P := by
  unfold lam
  apply Nat.Coprime.prod_left
  intro ℓ hℓ
  simp only [mem_filter, mem_range] at hℓ
  exact Nat.Coprime.pow_left _ ((Nat.coprime_primes hℓ.2 hP).mpr (by omega))

/-- **Lemma 3 with the source's key**: the mesh `V` of 02-setup l. 143-155 with
`α = q^{−(D+1)}` (l. 93-95), `R = log(1 + 1/(2α))` and `m = ⌈k² R⌉` (l. 143-147),
and the dilation `λ` of l. 24 with `h₀ < P`. -/
theorem lemma3 (P e D k h₀ M : ℕ) (hP : P.Prime) (he : 0 < e) (hk : 2 ≤ k)
    (hkP : k < P) (hh₀ : h₀ < P) (n₀ d : ZMod ((P ^ e) ^ D)) (hd : d ≠ 0) :
    let α : ℝ := ((P ^ e : ℕ) : ℝ) ^ (-((D : ℤ) + 1))
    let R := log (1 + 1 / (2 * α))
    let m := ⌈(k : ℝ) ^ 2 * R⌉₊
    (∀ κ₀, ((range k).filter fun j : ℕ =>
        key (meshV α R m) (P ^ e) D (lam h₀ M) (n₀ + j * d) = κ₀).card ≤ 2) ∧
      (k + 1) / 2 ≤ ((range k).image fun j : ℕ =>
        key (meshV α R m) (P ^ e) D (lam h₀ M) (n₀ + j * d)).card := by
  intro α R m
  have hq2 : 2 ≤ P ^ e := le_trans hP.two_le (Nat.le_self_pow he.ne' P)
  have hq2' : (2 : ℝ) ≤ ((P ^ e : ℕ) : ℝ) ^ (D + 1) := by
    have : 2 ≤ (P ^ e) ^ (D + 1) := le_trans hq2 (Nat.le_self_pow (by omega) _)
    exact_mod_cast this
  have hαeq : α = 1 / ((P ^ e : ℕ) : ℝ) ^ (D + 1) := by
    simp only [α]; rw [zpow_neg, one_div]; norm_cast
  have hα : 0 < α := by rw [hαeq]; positivity
  have hα2 : α ≤ 1 / 2 := by rw [hαeq]; exact one_div_le_one_div_of_le (by norm_num) hq2'
  have hkR : (0 : ℝ) < (k : ℝ) ^ 2 := by positivity
  have hmR : R ≤ m * (1 / (k : ℝ) ^ 2) := by
    have := Nat.le_ceil ((k : ℝ) ^ 2 * R)
    rw [mul_one_div, le_div_iff₀ hkR]; linarith
  have hV : ∀ s ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2), ∀ t ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2),
      meshV α R m s = meshV α R m t → |s - t| ≤ 1 / (k : ℝ) ^ 2 :=
    fun s hs t ht hst => (meshV_width α _ m hα hα2 hmR s t hs ht hst).le
  have hkw : (k : ℝ) * (1 / (k : ℝ) ^ 2) < 1 := by
    have hk1 : (1 : ℝ) < k := by exact_mod_cast (by omega : 1 < k)
    rw [show (k : ℝ) * (1 / (k : ℝ) ^ 2) = 1 / k by field_simp; ring]
    exact (div_lt_one (by linarith)).mpr hk1
  have hlam := lam_coprime h₀ M P hP hh₀
  exact ⟨fun κ₀ => mult_le_two P e D k _ hP hkP hlam _ _ hV hkw n₀ d hd κ₀,
    distinct_keys P e D k _ hP hkP hlam _ _ hV hkw n₀ d hd⟩

/-- The bridge to the hypothesis `hm` of `key-measurable-lean` (PR #23):
there `m ≤ (P.image κ).card` for every `P ∈ S`, with `P : Finset V` and `κ`
into a finite type `K`. Here `V = ℤ/q^D`, `K` is the (finite) range of the
key, and every member of `S` is a `k`-term progression of nonzero step. -/
theorem key_range_finite {β : Type*} (P e D lam : ℕ) (hP : P.Prime) (V : ℝ → β) :
    (Set.range (key V (P ^ e) D lam)).Finite := by
  haveI : NeZero ((P ^ e) ^ D) := ⟨by have := hP.pos; positivity⟩
  exact Set.finite_range _

theorem hm_bridge {β : Type*} [DecidableEq β] (P e D k lam : ℕ) (hP : P.Prime)
    (hkP : k < P) (hlam : Nat.Coprime lam P) (V : ℝ → β) (w : ℝ)
    (hV : ∀ s ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2), ∀ t ∈ Set.Ico (-1 / 2 : ℝ) (1 / 2),
      V s = V t → |s - t| ≤ w)
    (hkw : k * w < 1) (S : Finset (Finset (ZMod ((P ^ e) ^ D))))
    (hS : ∀ Q ∈ S, ∃ n₀ d : ZMod ((P ^ e) ^ D), d ≠ 0 ∧
      Q = (range k).image fun j : ℕ => n₀ + j * d) :
    ∀ Q ∈ S, (k + 1) / 2 ≤
      (Q.image fun n => (⟨key V (P ^ e) D lam n, n, rfl⟩ : Set.range (key V (P ^ e) D lam))).card := by
  intro Q hQ
  obtain ⟨n₀, d, hd, rfl⟩ := hS Q hQ
  rw [Finset.image_image, ← Finset.card_image_of_injective _ Subtype.val_injective,
    Finset.image_image]
  exact distinct_keys P e D k lam hP hkP hlam V w hV hkw n₀ d hd

end KeyMultiplicity
