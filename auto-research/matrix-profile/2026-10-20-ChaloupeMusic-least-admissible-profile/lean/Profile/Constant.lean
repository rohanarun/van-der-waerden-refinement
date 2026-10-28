import Profile.Least

/-!
# Corollary 2: sharp numbers and the constant `3/(2Γ(4/3))`

`κ_a = L_a / a^(4/3)`. Over any ordered field, in cube form: `κ_a` strictly increases and stays
below `(3/2)^(4/3)`; `H_a^3/a` increases and `H_a^3/(a-1/3)` decreases. Over `ℝ`: `κ_a` tends to
`3/(2Γ(4/3))`, by Euler's limit formula (`Real.GammaSeq_tendsto_Gamma`), and for every `N ≥ 1`
`(27/8) H_N^3/N ≤ κ^3 ≤ (81/8) H_N^3/(3N-1)`.
-/

set_option linter.unusedSectionVars false

namespace Profile

open Filter Topology

section Ordered

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

/-- `Po` attains the bound of Theorem 1 (ii) on the diagonal: `min P(a,a) = L_a`. -/
theorem diag_min {P : ℕ → ℕ → K} (hP : LowerAdmissible P) {a : ℕ} (ha : 1 ≤ a) :
    Po a a ≤ P a a ∧ Po a a = (L a : K) :=
  ⟨hP.Po_le ha ha, Po_diag a⟩

/-- `κ_a^3 = L_a^3/a^4` strictly increases: with `a = 1 + k`,
`(3a+1)^3(3a+2)^3 a - 27(3a-1)^3(a+1)^4` has positive coefficients in `k`. -/
theorem kappa_cube_strictMono {a : ℕ} (ha : 1 ≤ a) :
    L a ^ 3 * ((a : K) + 1) ^ 4 < L (a + 1) ^ 3 * (a : K) ^ 4 := by
  obtain ⟨k, rfl⟩ : ∃ k, a = k + 1 := ⟨a - 1, by omega⟩
  have hH := H_pos (K := K) (k + 1)
  rw [L, L, H_succ' (n := k + 1) (by omega)]
  push_cast
  have hk : (0 : K) ≤ k := Nat.cast_nonneg k
  rw [← sub_pos]
  have key : ((3 * ((k : K) + 1 + 1) - 1) / 2 * (H (k + 1) * (3 * ((k : K) + 1) + 1)
        / (3 * ((k : K) + 1)))) ^ 3 * ((k : K) + 1) ^ 4
      - ((3 * ((k : K) + 1) - 1) / 2 * H (k + 1)) ^ 3 * ((k : K) + 1 + 1) ^ 4
      = H (k + 1) ^ 3 * (4544 + 17936 * k + 27324 * k ^ 2 + 20007 * k ^ 3 + 7074 * k ^ 4
          + 972 * k ^ 5) / 216 := by
    field_simp; ring
  rw [key]; positivity

/-- `κ_a < (3/2)^(4/3)`, cube form: `L_a^3 < (81/16) a^4`. -/
theorem kappa_cube_lt {a : ℕ} (ha : 1 ≤ a) : L a ^ 3 < 81 / 16 * (a : K) ^ 4 := by
  have haK : (1 : K) ≤ a := by exact_mod_cast ha
  have hH := H_cube_le (K := K) ha
  have h3 : (0 : K) ≤ ((3 * (a : K) - 1) / 2) ^ 3 := by apply pow_nonneg; linarith
  rw [L, mul_pow]
  calc ((3 * (a : K) - 1) / 2) ^ 3 * H a ^ 3 ≤ ((3 * (a : K) - 1) / 2) ^ 3 * ((3 * a - 1) / 2) :=
        mul_le_mul_of_nonneg_left hH h3
    _ < 81 / 16 * (a : K) ^ 4 := by nlinarith

/-- `H_a^3/a` increases: `(3a+1)^3 - 27a^2(a+1) = 9a+1`. -/
theorem lower_seq_mono {a : ℕ} (ha : 1 ≤ a) :
    H a ^ 3 * ((a : K) + 1) ≤ H (a + 1) ^ 3 * a := by
  have haK : (1 : K) ≤ a := by exact_mod_cast ha
  have hH := pow_pos (H_pos (K := K) a) 3
  rw [H_succ' ha, div_pow, mul_pow, div_mul_eq_mul_div, le_div_iff₀ (by positivity)]
  have : 27 * (a : K) ^ 2 * (a + 1) ≤ (3 * a + 1) ^ 3 := by nlinarith
  nlinarith

/-- `H_a^3/(a-1/3)` decreases: `27a^3(3a+2) - (3a+1)^3(3a-1) = 6a+1`. -/
theorem upper_seq_anti {a : ℕ} (ha : 1 ≤ a) :
    H (a + 1) ^ 3 * (3 * (a : K) - 1) ≤ H a ^ 3 * (3 * a + 2) := by
  have haK : (1 : K) ≤ a := by exact_mod_cast ha
  have hH := pow_pos (H_pos (K := K) a) 3
  rw [H_succ' ha, div_pow, mul_pow, div_mul_eq_mul_div, div_le_iff₀ (by positivity)]
  have : (3 * (a : K) + 1) ^ 3 * (3 * a - 1) ≤ 27 * a ^ 3 * (3 * a + 2) := by nlinarith
  nlinarith

end Ordered

/-! ## The limit -/

open Real in
/-- `∏_{j=0}^{n} (4/3 + j) = (n + 4/3) n! H_{n+1}`, which turns Euler's sequence for `Γ(4/3)`
into `H`. -/
theorem prod_four_thirds (n : ℕ) :
    ∏ j ∈ Finset.range (n + 1), ((4 : ℝ) / 3 + j) = ((n : ℝ) + 4 / 3) * n.factorial * H (n + 1) := by
  induction n with
  | zero => simp [H_one]
  | succ n ih =>
    rw [Finset.prod_range_succ, ih, H_succ' (n := n + 1) (by omega), Nat.factorial_succ]
    push_cast
    field_simp
    ring

open Real in
theorem GammaSeq_four_thirds {n : ℕ} (hn : 1 ≤ n) :
    GammaSeq (4 / 3) n = (n : ℝ) ^ ((4 : ℝ) / 3) / (((n : ℝ) + 4 / 3) * H (n + 1)) := by
  have hf : (0 : ℝ) < n.factorial := by exact_mod_cast Nat.factorial_pos n
  have hH := H_pos (K := ℝ) (n + 1)
  rw [GammaSeq, prod_four_thirds]
  field_simp
  ring

/-- `κ_a = L_a / a^(4/3)`. -/
noncomputable def kappaSeq (a : ℕ) : ℝ := L a / (a : ℝ) ^ ((4 : ℝ) / 3)

/-- The sharp constant. -/
noncomputable def kappa : ℝ := 3 / (2 * Real.Gamma (4 / 3))

theorem kappaSeq_succ {n : ℕ} (hn : 1 ≤ n) :
    kappaSeq (n + 1) = (3 * (n : ℝ) + 2) / (2 * ((n : ℝ) + 4 / 3))
      * ((n : ℝ) / (n + 1)) ^ ((4 : ℝ) / 3) / Real.GammaSeq (4 / 3) n := by
  have hnR : (1 : ℝ) ≤ n := by exact_mod_cast hn
  have hH := H_pos (K := ℝ) (n + 1)
  have hp : (0 : ℝ) < (n : ℝ) ^ ((4 : ℝ) / 3) := Real.rpow_pos_of_pos (by linarith) _
  have hp1 : (0 : ℝ) < ((n : ℝ) + 1) ^ ((4 : ℝ) / 3) := Real.rpow_pos_of_pos (by linarith) _
  rw [GammaSeq_four_thirds hn, kappaSeq, L, Real.div_rpow (by positivity) (by positivity)]
  push_cast
  field_simp
  ring

/-- **Corollary 2, the limit.** `κ_a → 3/(2Γ(4/3))`. -/
theorem kappaSeq_tendsto : Tendsto kappaSeq atTop (𝓝 kappa) := by
  rw [← Filter.tendsto_add_atTop_iff_nat 1]
  have hG : Real.Gamma (4 / 3) ≠ 0 := (Real.Gamma_pos_of_pos (by norm_num)).ne'
  -- the rational factor
  have h1 : Tendsto (fun n : ℕ => (3 * (n : ℝ) + 2) / (2 * ((n : ℝ) + 4 / 3))) atTop (𝓝 (3 / 2)) := by
    have hinv := _root_.tendsto_inverse_atTop_nhds_zero_nat
    have hnum : Tendsto (fun n : ℕ => 3 + 2 * ((n : ℝ))⁻¹) atTop (𝓝 3) := by
      simpa using (hinv.const_mul 2).const_add 3
    have hden : Tendsto (fun n : ℕ => 2 + 8 / 3 * ((n : ℝ))⁻¹) atTop (𝓝 2) := by
      simpa using (hinv.const_mul (8 / 3)).const_add 2
    refine (hnum.div hden (by norm_num)).congr' ?_
    filter_upwards [eventually_ge_atTop 1] with n hn
    have : (0 : ℝ) < n := by exact_mod_cast hn
    field_simp
    ring
  -- `(n/(n+1))^(4/3) → 1`
  have h2 : Tendsto (fun n : ℕ => ((n : ℝ) / (n + 1)) ^ ((4 : ℝ) / 3)) atTop (𝓝 1) := by
    have := (tendsto_natCast_div_add_atTop (1 : ℝ)).rpow_const (p := (4 : ℝ) / 3)
      (Or.inl one_ne_zero)
    simpa using this
  have h3 := Real.GammaSeq_tendsto_Gamma (4 / 3)
  have hlim := (h1.mul h2).div h3 hG
  have hk : 3 / 2 * 1 / Real.Gamma (4 / 3) = kappa := by rw [kappa]; field_simp
  rw [hk] at hlim
  refine hlim.congr' ?_
  filter_upwards [eventually_ge_atTop 1] with n hn
  rw [kappaSeq_succ hn]
  rfl

theorem kappaSeq_cube (a : ℕ) : kappaSeq a ^ 3 = L a ^ 3 / (a : ℝ) ^ 4 := by
  have : ((a : ℝ) ^ ((4 : ℝ) / 3)) ^ 3 = (a : ℝ) ^ 4 := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (Nat.cast_nonneg a)]; norm_num
  rw [kappaSeq, div_pow, this]

/-- **Corollary 2, the bracket.** For every `N ≥ 1`,
`(27/8) H_N^3/N ≤ κ^3 ≤ (81/8) H_N^3/(3N-1)`. -/
theorem kappa_bracket {N : ℕ} (hN : 1 ≤ N) :
    27 / 8 * H N ^ 3 / N ≤ kappa ^ 3 ∧ kappa ^ 3 ≤ 81 / 8 * H N ^ 3 / (3 * N - 1) := by
  -- `s_a = H_a^3/a` and `t_a = H_a^3/(a-1/3)` both tend to `(8/27) κ^3`
  let s : ℕ → ℝ := fun n => H (n + 1) ^ 3 / ((n : ℝ) + 1)
  let t : ℕ → ℝ := fun n => 3 * H (n + 1) ^ 3 / (3 * (n : ℝ) + 2)
  have hκ3 : Tendsto (fun n : ℕ => kappaSeq (n + 1) ^ 3) atTop (𝓝 (kappa ^ 3)) :=
    ((Filter.tendsto_add_atTop_iff_nat 1).2 kappaSeq_tendsto).pow 3
  -- `s_n = (8/27) κ_{n+1}^3 ((n+1)/(n+2/3))^3`
  have hr : Tendsto (fun n : ℕ => (((n : ℝ) + 1) / ((n : ℝ) + 2 / 3)) ^ 3) atTop (𝓝 1) := by
    have hinv := _root_.tendsto_inverse_atTop_nhds_zero_nat
    have hnum : Tendsto (fun n : ℕ => 1 + ((n : ℝ))⁻¹) atTop (𝓝 1) := by
      simpa using hinv.const_add 1
    have hden : Tendsto (fun n : ℕ => 1 + 2 / 3 * ((n : ℝ))⁻¹) atTop (𝓝 1) := by
      simpa using (hinv.const_mul (2 / 3)).const_add 1
    have := ((hnum.div hden (by norm_num)).pow 3)
    simp only [div_one, one_pow] at this
    refine this.congr' ?_
    filter_upwards [eventually_ge_atTop 1] with n hn
    have : (0 : ℝ) < n := by exact_mod_cast hn
    congr 1; field_simp; ring
  have hs : Tendsto s atTop (𝓝 (8 / 27 * kappa ^ 3)) := by
    have := (hκ3.const_mul (8 / 27)).mul hr
    rw [mul_one] at this
    refine this.congr' ?_
    filter_upwards [eventually_ge_atTop 0] with n _
    rw [kappaSeq_cube, L]
    have hH := H_pos (K := ℝ) (n + 1)
    simp only [s]; push_cast
    field_simp
    ring
  have ht : Tendsto t atTop (𝓝 (8 / 27 * kappa ^ 3)) := by
    have hq : Tendsto (fun n : ℕ => 3 * ((n : ℝ) + 1) / (3 * (n : ℝ) + 2)) atTop (𝓝 1) := by
      have hinv := _root_.tendsto_inverse_atTop_nhds_zero_nat
      have hnum : Tendsto (fun n : ℕ => 3 + 3 * ((n : ℝ))⁻¹) atTop (𝓝 3) := by
        simpa using (hinv.const_mul 3).const_add 3
      have hden : Tendsto (fun n : ℕ => 3 + 2 * ((n : ℝ))⁻¹) atTop (𝓝 3) := by
        simpa using (hinv.const_mul 2).const_add 3
      have := hnum.div hden (by norm_num)
      rw [div_self (by norm_num)] at this
      refine this.congr' ?_
      filter_upwards [eventually_ge_atTop 1] with n hn
      have : (0 : ℝ) < n := by exact_mod_cast hn
      field_simp; ring
    have := hs.mul hq
    rw [mul_one] at this
    refine this.congr' ?_
    filter_upwards [eventually_ge_atTop 0] with n _
    simp only [s, t]
    field_simp
    ring
  have hsm : Monotone s := by
    refine monotone_nat_of_le_succ fun n => ?_
    have := lower_seq_mono (K := ℝ) (a := n + 1) (by omega)
    simp only [s]
    rw [div_le_div_iff₀ (by positivity) (by positivity)]
    push_cast at this ⊢
    linarith
  have hta : Antitone t := by
    refine antitone_nat_of_succ_le fun n => ?_
    have := upper_seq_anti (K := ℝ) (a := n + 1) (by omega)
    simp only [t]
    rw [div_le_div_iff₀ (by positivity) (by positivity)]
    push_cast at this ⊢
    nlinarith
  obtain ⟨n, rfl⟩ : ∃ n, N = n + 1 := ⟨N - 1, by omega⟩
  have hsN := hsm.ge_of_tendsto hs n
  have htN := hta.le_of_tendsto ht n
  simp only [s, t] at hsN htN
  push_cast
  constructor
  · rw [show 27 / 8 * H (n + 1) ^ 3 / ((n : ℝ) + 1) = 27 / 8 * (H (n + 1) ^ 3 / ((n : ℝ) + 1)) by
      ring]
    linarith
  · rw [show 81 / 8 * H (n + 1) ^ 3 / (3 * ((n : ℝ) + 1) - 1)
        = 27 / 8 * (3 * H (n + 1) ^ 3 / (3 * (n : ℝ) + 2)) by ring_nf]
    linarith

end Profile
