import Vdw.Bounds
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

open scoped BigOperators

namespace Vdw

-- The digit at a place dividing the progression difference is itself a
-- cyclic progression. There is no primality hypothesis on the base.
theorem progression_digit (N place a e j : ℕ) (hp : 0 < place) :
    ((a+j*(place*e))/place)%N = (a/place+j*e)%N := by
  congr 1
  have h : j*(place*e) = place*(j*e) := by ring
  rw [h, Nat.add_mul_div_left _ _ hp]

def CyclicAvoids (N k : ℕ) (C : ℕ → Bool) : Prop :=
  ∀ a d, d%N ≠ 0 → ∃ j, j<k ∧ C ((a+j*d)%N) ≠ C (a%N)

theorem nonzero_digit_place (N s d : ℕ) (hN : 1<N) (hd : 0<d)
    (hbound : d<N^s) : ∃ i e, i<s ∧ d=N^i*e ∧ e%N≠0 := by
  induction s generalizing d with
  | zero => simp at hbound; omega
  | succ s ih =>
    by_cases hz : d%N=0
    · have hNp : 0<N := by omega
      have heq : N*(d/N)=d := by simpa [hz] using Nat.mod_add_div d N
      have hdpos : 0<d/N := by
        apply Nat.pos_of_ne_zero
        intro hz'
        rw [hz', Nat.mul_zero] at heq
        omega
      have hsmall : d/N<N^s := by
        apply (Nat.div_lt_iff_lt_mul hNp).2
        simpa [pow_succ] using hbound
      obtain ⟨i,e,hi,hde,he⟩ := ih (d/N) hdpos hsmall
      refine ⟨i+1,e,by omega,?_,he⟩
      calc
        d=N*(d/N) := heq.symm
        _=N*(N^i*e) := by rw [hde]
        _=N^(i+1)*e := by rw [pow_succ]; ring
    · exact ⟨0,d,by omega,by simp,hz⟩

-- Once a nonzero digit-step is identified, a monochromatic product coloring
-- is impossible, regardless of carries in the other digits.
theorem digit_product_witness (N k place a e : ℕ) (C : ℕ → Bool)
    (hp : 0<place) (he : e%N ≠ 0) (hc : CyclicAvoids N k C) :
    ∃ j, j<k ∧ C (((a+j*(place*e))/place)%N) ≠ C ((a/place)%N) := by
  obtain ⟨j,hj,hcolor⟩ := hc (a/place) e he
  exact ⟨j,hj, by simpa only [progression_digit N place a e j hp] using hcolor⟩

-- Full product-coloring conclusion for every positive difference below N^s.
-- An interval progression in [0,N^s) is a special case of this statement.
theorem digit_product_avoids (N k s a d : ℕ) (C : ℕ → Bool)
    (hN : 1<N) (hd : 0<d) (hbound : d<N^s) (hc : CyclicAvoids N k C) :
    ∃ i<s, ∃ j<k, C (((a+j*d)/N^i)%N) ≠ C ((a/N^i)%N) := by
  obtain ⟨i,e,hi,hde,he⟩ := nonzero_digit_place N s d hN hd hbound
  have hp : 0<N^i := pow_pos (by omega) _
  obtain ⟨j,hj,hcolor⟩ := digit_product_witness N k (N^i) a e C hp he hc
  exact ⟨i,hi,j,hj,by simpa only [hde] using hcolor⟩

-- A strict union bound entails existence in any finite weighted space.
-- No independence is needed for this last step.
theorem exists_outside_bad {Ω : Type*} (space : Finset Ω)
    (weight : Ω → ℚ) (bad : Ω → Prop) [DecidablePred bad]
    (htotal : (∑ x∈space, weight x)=1)
    (hbad : (∑ x∈space.filter bad, weight x)<1) :
    ∃ x∈space, ¬bad x := by
  by_contra h
  have hall : ∀ x∈space, bad x := by simpa using h
  have heq : space.filter bad=space := Finset.filter_eq_self.mpr hall
  rw [heq, htotal] at hbad
  exact (lt_irrefl (1 : ℚ)) hbad
end Vdw
