import Vdw.Bounds
import Mathlib.LinearAlgebra.Span.Basic

namespace Vdw
variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

-- coord n = d[n-1]/q + ... + d[0]/q^n, for arbitrary dimension n.
def coord (q : K) (d : ℕ → K) : ℕ → K
  | 0 => 0
  | n+1 => (d n + coord q d n)/q

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem coord_step (q : K) (d : ℕ → K) (n : ℕ) (hq : q ≠ 0) :
    q*coord q d (n+1) = d n+coord q d n := by
  rw [coord, mul_div_cancel₀ _ hq]

theorem two_digit_identity (q : K) (d : ℕ → K) (n : ℕ) (hq : q ≠ 0) :
    q^2*coord q d (n+2) = q*d (n+1)+d n+coord q d n := by
  have h0 := coord_step q d n hq
  have h1 := coord_step q d (n+1) hq
  have h2 := congrArg (fun x => q*x) h1
  nlinarith [h2]

theorem balanced_coord (q : K) (d : ℕ → K) (hq : 1<q)
    (hd : ∀ i, -(q-1)/2 ≤ d i ∧ d i ≤ (q-1)/2) (n : ℕ) :
    -(1/2 : K) < coord q d n ∧ coord q d n < 1/2 := by
  have hqp : 0<q := by linarith
  induction n with
  | zero => norm_num [coord]
  | succ n ih =>
    rw [coord]
    constructor
    · apply (lt_div_iff₀ hqp).2; linarith [ih.1, (hd n).1]
    · apply (div_lt_iff₀ hqp).2; linarith [ih.2, (hd n).2]

theorem return_digit_bound {q e x y H : K} (hq : 0 ≤ q)
    (hx : |x| ≤ H) (hy : |y| ≤ H) (he : e=q*y-x) :
    |e| ≤ (q+1)*H := by
  rw [he, abs_le]
  have hx' := abs_le.mp hx
  have hy' := abs_le.mp hy
  constructor <;> nlinarith [hx'.1, hx'.2,
    mul_le_mul_of_nonneg_left hy'.1 hq,
    mul_le_mul_of_nonneg_left hy'.2 hq]

-- The same digit forms determine all forms in their span. This does not
-- assume that arbitrary row data are geometrically realized by a progression.
omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem forms_determine_span {M : Type*} [AddCommGroup M] [Module K M]
    (S : Set M) (f g : M →ₗ[K] K) (h : ∀ v∈S, f v=g v)
    {v : M} (hv : v∈Submodule.span K S) : f v=g v := by
  induction hv using Submodule.span_induction with
  | mem x hx => exact h x hx
  | zero => simp
  | add x y hx hy ihx ihy => simp [ihx, ihy]
  | smul a x hx ih => simp [ih]
end Vdw
