import Profile.Defs

/-!
# Theorem 1 (i): `Po` is admissible

(N), (S), separate concavity (C), shifted tripling (T), the rank envelope at `t = 3/4` in the
cube form `Po^3 ≤ (a+b-1)^4`, monotonicity, and `Po ≤ P_*` in the cube form
`H_u^3 ≤ (3u-1)/2`.
-/

set_option linter.unusedSectionVars false

namespace Profile

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

/-- (N) -/
theorem Po_one_left {b : ℕ} (hb : 1 ≤ b) : Po 1 b = (b : K) := by
  rw [Po_of_le hb, H_one]; push_cast; ring

/-- (C), rows: the second difference centred at `c + 1 ≥ 2` is `≤ 0`. -/
theorem Po_row_concave {a c : ℕ} (hc : 1 ≤ c) :
    Po a c + Po a (c + 2) ≤ 2 * (Po a (c + 1) : K) := by
  have hc' : (1 : K) ≤ c := by exact_mod_cast hc
  rcases le_or_gt a c with h | h
  · rw [Po_of_le h, Po_of_le (by omega : a ≤ c + 1), Po_of_le (by omega : a ≤ c + 2)]
    push_cast; nlinarith [H_pos (K := K) a]
  have h1 := H_succ' (K := K) hc
  have h2 := H_succ' (K := K) (by omega : 1 ≤ c + 1)
  push_cast at h2
  rcases Nat.lt_or_ge (c + 1) a with h' | h'
  · -- three points left of the seam: the second difference is `-2 H_{c+1} (a-c-1)/(3(c+1)(3c+1))`
    rw [Po_of_ge h.le, Po_of_ge (by omega : c + 1 ≤ a), Po_of_ge (by omega : c + 2 ≤ a)]
    have ha : (c : K) + 2 ≤ a := by exact_mod_cast h'
    have key : 2 * (H (c + 1) * ((a : K) + ((↑(c + 1) : K) - 1) / 2))
        - H c * ((a : K) + ((c : K) - 1) / 2) - H (c + 2) * ((a : K) + ((↑(c + 2) : K) - 1) / 2)
        = 2 * H c * ((a : K) - c - 1) / (9 * c * (c + 1)) := by
      rw [h2, h1]; push_cast; field_simp; ring
    have : 0 ≤ 2 * H c * ((a : K) - c - 1) / (9 * c * (c + 1)) := by
      have := H_pos (K := K) c
      apply div_nonneg _ (by positivity)
      apply mul_nonneg (by positivity); linarith
    linarith
  · -- the seam: `a = c + 1`, second difference `0`
    obtain rfl : a = c + 1 := by omega
    rw [Po_of_ge (by omega : c ≤ c + 1), Po_of_le le_rfl, Po_of_le (by omega : c + 1 ≤ c + 2), h1]
    apply le_of_eq; push_cast; field_simp; ring

/-- (C), columns, by symmetry. -/
theorem Po_col_concave {b c : ℕ} (hc : 1 ≤ c) :
    Po c b + Po (c + 2) b ≤ 2 * (Po (c + 1) b : K) := by
  rw [Po_symm c, Po_symm (c + 2), Po_symm (c + 1)]; exact Po_row_concave hc

/-- The ratio step behind (T) left of the seam: `H_h (2a+h-1) ≤ H_a (2h+a-1)` for `a ≥ h ≥ 1`;
numerator minus denominator of the ratio is `2(a-h)(a-h+1)`. -/
theorem tripling_aux {h : ℕ} (hh : 1 ≤ h) :
    ∀ a, h ≤ a → H h * (2 * (a : K) + h - 1) ≤ H a * (2 * (h : K) + a - 1) := by
  intro a ha
  induction a, ha using Nat.le_induction with
  | base => apply le_of_eq; ring
  | succ a ha ih =>
    have ha1 : 1 ≤ a := le_trans hh ha
    have haK : (1 : K) ≤ a := by exact_mod_cast ha1
    have hah : (h : K) ≤ a := by exact_mod_cast ha
    have hhK : (1 : K) ≤ h := by exact_mod_cast hh
    rw [H_succ' ha1]; push_cast
    have hHa := H_pos (K := K) a
    have hHh := H_pos (K := K) h
    -- `H_h(2a+h+1) ≤ H_h(2a+h-1)·q ≤ H_a(2h+a-1)·q = H_{a+1}(2h+a)` with
    -- `q = (3a+1)(2h+a) / (3a(2h+a-1))`
    have hq : (2 * (a : K) + h + 1) * (3 * a * (2 * h + a - 1))
        ≤ (2 * a + h - 1) * ((3 * a + 1) * (2 * h + a)) := by nlinarith
    have hpos : (0 : K) < 3 * a * (2 * h + a - 1) := by nlinarith
    rw [show H a * (3 * (a : K) + 1) / (3 * a) * (2 * h + (a + 1) - 1)
        = H a * (2 * h + a - 1) * ((3 * a + 1) * (2 * h + a)) / (3 * a * (2 * h + a - 1)) by
          field_simp; ring]
    rw [le_div_iff₀ hpos]
    calc H h * (2 * ((a : K) + 1) + h - 1) * (3 * a * (2 * h + a - 1))
        = H h * ((2 * (a : K) + h + 1) * (3 * a * (2 * h + a - 1))) := by ring
      _ ≤ H h * ((2 * a + h - 1) * ((3 * a + 1) * (2 * h + a))) :=
          mul_le_mul_of_nonneg_left hq hHh.le
      _ = H h * (2 * a + h - 1) * ((3 * a + 1) * (2 * h + a)) := by ring
      _ ≤ H a * (2 * h + a - 1) * ((3 * a + 1) * (2 * h + a)) :=
          mul_le_mul_of_nonneg_right ih (by positivity)

/-- (T), rows: `P(a, 3h+a-1) ≥ 3 P(a,h)`, with equality for `h ≥ a`. -/
theorem Po_row_tripling {a h : ℕ} (ha : 1 ≤ a) (hh : 1 ≤ h) :
    3 * Po a h ≤ (Po a (3 * h + a - 1) : K) := by
  rw [Po_of_le (by omega : a ≤ 3 * h + a - 1)]
  rw [show ((↑(3 * h + a - 1) : ℕ) : K) = 3 * h + a - 1 by
    rw [Nat.cast_sub (by omega)]; push_cast; ring]
  rcases le_total a h with hah | hah
  · rw [Po_of_le hah]; apply le_of_eq; ring
  · rw [Po_of_ge hah]
    have := tripling_aux (K := K) hh a hah
    nlinarith

theorem Po_col_tripling {b h : ℕ} (hb : 1 ≤ b) (hh : 1 ≤ h) :
    3 * Po h b ≤ (Po (3 * h + b - 1) b : K) := by
  rw [Po_symm h, Po_symm (3 * h + b - 1)]; exact Po_row_tripling hb hh

/-- `H_u^3 ≤ (3u-1)/2`, i.e. `Po ≤ P_* = ((3u-1)/2)^(1/3) (v + (u-1)/2)`; the step is
`27u^3(3u+2) - (3u+1)^3(3u-1) = 6u+1`. -/
theorem H_cube_le {u : ℕ} (hu : 1 ≤ u) : H u ^ 3 ≤ (3 * (u : K) - 1) / 2 := by
  induction u, hu using Nat.le_induction with
  | base => rw [H_one]; norm_num
  | succ u hu ih =>
    have huK : (1 : K) ≤ u := by exact_mod_cast hu
    rw [H_succ' hu, div_pow, mul_pow, div_le_iff₀ (by positivity)]; push_cast
    have hc : (0 : K) ≤ (3 * u + 1) ^ 3 := by positivity
    calc H u ^ 3 * (3 * (u : K) + 1) ^ 3 ≤ (3 * u - 1) / 2 * (3 * u + 1) ^ 3 :=
          mul_le_mul_of_nonneg_right ih hc
      _ ≤ (3 * (u + 1) - 1) / 2 * (3 * u) ^ 3 := by nlinarith

/-- `Po ≤ P_*` pointwise, cube form. -/
theorem Po_cube_le_Pstar_cube {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) :
    (Po a b : K) ^ 3 ≤ (3 * (min a b : K) - 1) / 2
      * ((max a b : K) + ((min a b : K) - 1) / 2) ^ 3 := by
  rcases le_total a b with h | h
  · rw [Po_of_le h, min_eq_left (by exact_mod_cast h), max_eq_right (by exact_mod_cast h),
      mul_pow]
    exact mul_le_mul_of_nonneg_right (H_cube_le ha) (by
      have : (1 : K) ≤ a := by exact_mod_cast ha
      have : (1 : K) ≤ b := by exact_mod_cast hb
      apply pow_nonneg; linarith)
  · rw [Po_of_ge h, min_eq_right (by exact_mod_cast h), max_eq_left (by exact_mod_cast h),
      mul_pow]
    exact mul_le_mul_of_nonneg_right (H_cube_le hb) (by
      have : (1 : K) ≤ a := by exact_mod_cast ha
      have : (1 : K) ≤ b := by exact_mod_cast hb
      apply pow_nonneg; linarith)

/-- (E_{3/4}) in cube form: `Po(a,b)^3 ≤ (a+b-1)^4`. -/
theorem Po_envelope {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) :
    (Po a b : K) ^ 3 ≤ ((a : K) + b - 1) ^ 4 := by
  have key : ∀ u v : ℕ, 1 ≤ u → u ≤ v →
      (H u * ((v : K) + ((u : K) - 1) / 2)) ^ 3 ≤ ((u : K) + v - 1) ^ 4 := by
    intro u v hu huv
    have huK : (1 : K) ≤ u := by exact_mod_cast hu
    have huvK : (u : K) ≤ v := by exact_mod_cast huv
    have hH := H_cube_le (K := K) hu
    have hw0 : (0 : K) ≤ (v : K) + ((u : K) - 1) / 2 := by linarith
    have hw : (0 : K) ≤ ((v : K) + ((u : K) - 1) / 2) ^ 3 := pow_nonneg hw0 3
    rw [mul_pow]
    calc H u ^ 3 * ((v : K) + ((u : K) - 1) / 2) ^ 3
        ≤ ((u : K) + v - 1) * ((v : K) + ((u : K) - 1) / 2) ^ 3 :=
          mul_le_mul_of_nonneg_right (by linarith) hw
      _ ≤ ((u : K) + v - 1) * ((u : K) + v - 1) ^ 3 := by
          apply mul_le_mul_of_nonneg_left _ (by linarith)
          apply pow_le_pow_left₀ hw0; linarith
      _ = ((u : K) + v - 1) ^ 4 := by ring
  rcases le_total a b with h | h
  · rw [Po_of_le h]; exact key a b ha h
  · rw [Po_of_ge h, show (a : K) + b - 1 = b + a - 1 by ring]; exact key b a hb h

/-- Monotone along rows: the increment is `H_a` right of the seam and
`H_b (a + 2b)/(3b)` left of it. -/
theorem Po_row_mono {a b : ℕ} (hb : 1 ≤ b) : Po a b < (Po a (b + 1) : K) := by
  have hbK : (1 : K) ≤ b := by exact_mod_cast hb
  rcases le_or_gt a b with h | h
  · rw [Po_of_le h, Po_of_le (by omega : a ≤ b + 1)]; push_cast
    nlinarith [H_pos (K := K) a]
  · rw [Po_of_ge h.le, Po_of_ge (by omega : b + 1 ≤ a), H_succ' hb]; push_cast
    have haK : (b : K) + 1 ≤ a := by exact_mod_cast h
    have := H_pos (K := K) b
    rw [← sub_pos]
    have e : H b * (3 * (b : K) + 1) / (3 * b) * (a + (b + 1 - 1) / 2) - H b * (a + (b - 1) / 2)
        = H b * (a + 2 * b) / (3 * b) := by field_simp; ring
    rw [e]; positivity

theorem Po_col_mono {a b : ℕ} (ha : 1 ≤ a) : Po a b < (Po (a + 1) b : K) := by
  rw [Po_symm a, Po_symm (a + 1)]; exact Po_row_mono ha

theorem Po_row_mono_le {a b b' : ℕ} (hb : 1 ≤ b) (hbb : b ≤ b') : Po a b ≤ (Po a b' : K) := by
  induction b', hbb using Nat.le_induction with
  | base => exact le_rfl
  | succ b' hbb ih => exact ih.trans (Po_row_mono (le_trans hb hbb)).le

theorem Po_col_mono_le {a a' b : ℕ} (ha : 1 ≤ a) (haa : a ≤ a') : Po a b ≤ (Po a' b : K) := by
  rw [Po_symm a, Po_symm a']; exact Po_row_mono_le ha haa

end Profile
