import Vdw.Bounds

namespace Vdw
variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

def quadratic (u v w x : K) : K := u*x^2+v*x+w

-- Any three samples at least one unit apart cannot occupy a single half-open
-- unit band when the leading quadratic coefficient is at least one.
theorem no_three_in_unit_band (u v w x y z t : K)
    (hu : 1 ≤ u) (hxy : 1 ≤ y-x) (hyz : 1 ≤ z-y)
    (hx : quadratic u v w x < t+1)
    (hy : t ≤ quadratic u v w y)
    (hz : quadratic u v w z < t+1) : False := by
  have ha : 0 < y-x := by linarith
  have hb : 0 < z-y := by linarith
  have hab : 1 ≤ (y-x)*(z-y) := by nlinarith
  have huab : 1 ≤ u*((y-x)*(z-y)) := by nlinarith
  have hleft := mul_lt_mul_of_pos_left hx hb
  have hright := mul_lt_mul_of_pos_left hz ha
  have hmid := mul_le_mul_of_nonneg_left hy (by linarith : 0 ≤ z-x)
  have hid : (z-y)*quadratic u v w x + (y-x)*quadratic u v w z
      - (z-x)*quadratic u v w y = u*((y-x)*(z-y))*(z-x) := by
    unfold quadratic; ring
  have hgap := mul_le_mul_of_nonneg_right huab (by linarith : 0 ≤ z-x)
  nlinarith

-- PR4's repeated-pair quadratic identity; all variables are universally quantified.
omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem pair_difference (u v w x y : K) :
    quadratic u v w y - quadratic u v w x = (y-x)*(u*(x+y)+v) := by
  unfold quadratic; ring

-- Half-open interval convexity includes the left endpoint and excludes the right.
theorem half_open_convex {lo hi x y r : K} (hx : lo ≤ x ∧ x < hi)
    (hy : lo ≤ y ∧ y < hi) (hr : 0 ≤ r ∧ r ≤ 1) :
    lo ≤ (1-r)*x+r*y ∧ (1-r)*x+r*y < hi := by
  have h1 : 0 ≤ 1-r := by linarith
  have ha := mul_le_mul_of_nonneg_left hx.1 h1
  have hb := mul_le_mul_of_nonneg_left hy.1 hr.1
  constructor
  · nlinarith
  · by_cases hzero : r=0
    · simp [hzero, hx.2]
    · have hc := mul_le_mul_of_nonneg_left (le_of_lt hx.2) h1
      have hd := mul_lt_mul_of_pos_left hy.2 (lt_of_le_of_ne hr.1 (Ne.symm hzero))
      nlinarith
end Vdw
