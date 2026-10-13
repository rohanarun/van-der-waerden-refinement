import Vdw.Geometry

namespace Vdw
variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

-- Distinct integer translates of an interval of width at most 1/2 are
-- separated by more than 1/2 between points in the half-open intervals.
theorem translated_intervals_separated (lo hi x y : K) (m n : ℤ)
    (hmn : m<n) (hwidth : hi-lo≤1/2)
    (hx : x<hi+(m : K)) (hy : lo+(n : K)≤y) : 1/2<y-x := by
  have hint : m+1≤n := by omega
  have hcast : (m : K)+1≤(n : K) := by exact_mod_cast hint
  linarith

-- PR7's circular argument needs BOTH the small interval and small path.
-- Monotonicity alone would not prevent leaving and re-entering a circle interval.
theorem short_path_uses_one_lift (lo hi x y : K) (m n : ℤ)
    (hwidth : hi-lo≤1/2) (hdiam : |y-x|<1/2)
    (hx : lo+(m : K)≤x ∧ x<hi+(m : K))
    (hy : lo+(n : K)≤y ∧ y<hi+(n : K)) : m=n := by
  rcases lt_trichotomy m n with h | h | h
  · have hgap := translated_intervals_separated lo hi x y m n h hwidth hx.2 hy.1
    have := (abs_lt.mp hdiam).2
    linarith
  · exact h
  · have hgap := translated_intervals_separated lo hi y x n m h hwidth hy.2 hx.1
    have := (abs_lt.mp hdiam).1
    linarith

-- Within the unique lift, every intermediate sample lies in the same interval.
theorem affine_interval_run (lo hi A v a b c : K) (hab : a≤b) (hbc : b≤c)
    (ha : lo≤A+a*v ∧ A+a*v<hi) (hc : lo≤A+c*v ∧ A+c*v<hi) :
    lo≤A+b*v ∧ A+b*v<hi := by
  rcases le_total 0 v with hv | hv
  · have h1 := mul_le_mul_of_nonneg_right hab hv
    have h2 := mul_le_mul_of_nonneg_right hbc hv
    constructor <;> linarith [ha.1, hc.2]
  · have h1 := mul_le_mul_of_nonpos_right hab hv
    have h2 := mul_le_mul_of_nonpos_right hbc hv
    constructor <;> linarith [hc.1, ha.2]
end Vdw
