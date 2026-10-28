import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/- Universal algebraic obligations. Probabilistic and geometric inputs are not asserted. -/
namespace Vdw
variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

theorem weak_entropy_ceiling {a b : K} (hba : b < a) (h : 2*a+b ≤ 1) :
    b < 1/3 := by linarith

theorem key_flip_ceiling {a b g c : K} (hb : 0 < b)
    (hba : b < a) (he : 2*a+b ≤ 1) (hg : g ≤ 1/2)
    (hc : c < g*b/4) : c < 1/24 := by
  have hthird := weak_entropy_ceiling hba he
  have hprod := mul_le_mul_of_nonneg_right hg (le_of_lt hb)
  linarith

-- The integer n is specified by the defining inequalities of floor(x).
theorem floor_half_bound (x : K) (n : ℤ) (hx : 1 ≤ x)
    (hl : (n : K) ≤ x) (hu : x < (n : K)+1) : x/2 ≤ (n : K) ∧ (n : K) ≤ x := by
  have hn : (0 : K) < (n : K) := by linarith
  have hnZ : 0 < n := by exact_mod_cast hn
  have hn1 : (1 : K) ≤ (n : K) := by exact_mod_cast hnZ
  constructor <;> linarith

theorem repeated_cover_split {F R g t k : K}
    (hpositions : g*k ≤ F+R) (hsmall : F < (g-t)*k) : t*k < R := by
  nlinarith

theorem repeated_cover_parameters {b g c : K} (h : c < g*b/3) :
    2*c < b*(g-g/3) ∧ c < b*(g/3) := by constructor <;> nlinarith

-- All normalized carry ranks, not just the three breakpoints sampled in Python.
theorem carry_rank_cost (t : K) : min (2*t) 1 + (2-t) ≤ 5/2 := by
  rcases le_total t (1/2) with h | h
  · have := min_le_left (2*t) (1 : K); linarith
  · have := min_le_right (2*t) (1 : K); linarith

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem matched_digit_cost (D R : K) : R+(2*D-R)=2*D := by ring

theorem run_ceiling {a b m g c : K} (hb : 0 < b) (hba : b<a)
    (ham : 2*a<m) (hm : m<1) (hg : g ≤ 1/2)
    (hc : 2*c < g*b) : c<1/8 := by
  have hp := mul_le_mul_of_nonneg_right hg (le_of_lt hb)
  linarith

-- PR9 Section 13: the entire parameter family for every c in the open interval.
theorem effective_parameter_family {c : K} (hc0 : 0<c) (hc : c<1/8) :
    let s := min (1/100) ((1/8-c)/4)
    let a := 1/2-2*s
    let b := 1/2-3*s
    let m := 1-3*s
    0<c ∧ 0<s ∧ s<1/2 ∧ 0<a ∧ 0<b ∧ 2*a<m ∧ m<1 ∧ b<a ∧ a+b<1 ∧
      b < (1/2-s)*(1-s)*(1-s) ∧ 2*c < b*b := by
  dsimp
  set s := min (1/100 : K) ((1/8-c)/4)
  have hs : 0<s := lt_min (by norm_num) (by linarith)
  have hs100 : s ≤ 1/100 := min_le_left _ _
  have hsDelta : s ≤ (1/8-c)/4 := min_le_right _ _
  have hsq : 0 ≤ s*s := mul_self_nonneg s
  have hcubic : s*s*s ≤ (1/100)*(s*s) := by
    nlinarith [mul_le_mul_of_nonneg_right hs100 hsq]
  refine ⟨hc0, hs, by linarith, by linarith, by linarith, by linarith,
    by linarith, by linarith, by linarith, ?_, ?_⟩
  · nlinarith
  · nlinarith
end Vdw
