import Vdw.Bounds
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset

open scoped BigOperators
namespace Vdw

def FullEvent {Key : Type*} (bits : Key → Bool) (F Z : Set Key) : Prop :=
  (∀ key∈F, bits key=true) ∧ (∀ key∈Z, bits key=false)

theorem inconsistent_event_empty {Key : Type*} (bits : Key → Bool)
    (F Z : Set Key) (h : (F∩Z).Nonempty) : ¬FullEvent bits F Z := by
  intro he
  obtain ⟨key,hf,hz⟩ := h
  have := (he.1 key hf).symm.trans (he.2 key hz)
  cases this

-- Every member of a family assigned the same certificate lies in that one
-- all-flips event. This does not identify the full events with each other.
theorem assigned_union_covered {Key I : Type*} (bits : Key → Bool)
    (F Z : I → Set Key) (S : Set Key) (hsub : ∀ i, S⊆F i)
    (hunion : ∃ i, FullEvent bits (F i) (Z i)) : ∀ key∈S, bits key=true := by
  obtain ⟨i,hi⟩ := hunion
  intro key hk
  exact hi.1 key (hsub i hk)

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

theorem balanced_cover_margins {b g c kap nu cost : K}
    (hb : 0<b) (hc : 0≤c) (hcost : kap+nu≤cost)
    (hgap : cost*c<g*b) :
    let theta := (kap*c+g*b-nu*c)/(2*b)
    0 < (g*b-cost*c)/2 ∧
    (g*b-cost*c)/2 ≤ b*theta-kap*c ∧
    (g*b-cost*c)/2 ≤ b*(g-theta)-nu*c := by
  dsimp
  have hden : 2*b≠0 := ne_of_gt (by linarith)
  have hid := div_mul_cancel₀ (kap*c+g*b-nu*c) hden
  have hle := mul_le_mul_of_nonneg_right hcost hc
  refine ⟨by linarith, ?_, ?_⟩ <;> nlinarith [hid]

-- PR3's floor-sum estimate, uniformly over any finite family of positive
-- logarithmic weights. The hypotheses identify n as the appropriate floor.
theorem dilation_sum_bound {I : Type*} (S : Finset I) (w : I → K)
    (n : I → ℤ) (L : K) (hw : ∀ i∈S, 0<w i ∧ w i≤L)
    (hn : ∀ i∈S, (n i : K)*w i≤L ∧ L<((n i : K)+1)*w i) :
    (S.card : K)*L/2 ≤ ∑ i∈S, (n i : K)*w i ∧
    (∑ i∈S, (n i : K)*w i) ≤ (S.card : K)*L := by
  have hlo : ∀ i∈S, L/2≤(n i : K)*w i := by
    intro i hi
    have wi := hw i hi
    have ni := hn i hi
    have np : (0 : K)<(n i : K) := by
      by_contra h
      have hnp : (n i : K)≤0 := le_of_not_gt h
      have := mul_nonpos_of_nonpos_of_nonneg hnp (le_of_lt wi.1)
      nlinarith [wi.2,ni.2]
    have npos : 0<n i := by exact_mod_cast np
    have none : (1 : K)≤(n i : K) := by exact_mod_cast npos
    have := mul_le_mul_of_nonneg_right none (le_of_lt wi.1)
    nlinarith [ni.2]
  constructor
  · have h := Finset.sum_le_sum hlo
    simpa [Finset.sum_const, nsmul_eq_mul, mul_div_assoc] using h
  · have h := Finset.sum_le_sum (fun i hi => (hn i hi).1)
    simpa [Finset.sum_const, nsmul_eq_mul] using h
end Vdw
