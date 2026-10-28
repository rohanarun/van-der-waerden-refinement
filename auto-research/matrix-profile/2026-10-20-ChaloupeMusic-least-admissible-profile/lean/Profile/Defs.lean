import Mathlib

/-!
# The least admissible profile: definitions

Indices are natural numbers; every statement about the profile assumes its indices are `≥ 1`.
`H n = ∏_{m=1}^{n-1} (1 + 1/(3m))`, so `H 0 = H 1 = 1`, and
`Po a b = H u * (v + (u-1)/2)` with `u = min a b`, `v = max a b`.
Everything is stated over an arbitrary linearly ordered field `K` (ℚ and ℝ in particular).
-/

set_option linter.unusedSectionVars false

namespace Profile
open Finset

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

def H (n : ℕ) : K := ∏ m ∈ Ico 1 n, (1 + 1 / (3 * (m : K)))

def Po (a b : ℕ) : K :=
  if a ≤ b then H a * ((b : K) + ((a : K) - 1) / 2) else H b * ((a : K) + ((b : K) - 1) / 2)

/-- The diagonal value `Po a a`. -/
def L (a : ℕ) : K := (3 * (a : K) - 1) / 2 * H a

theorem H_zero : H 0 = (1 : K) := by simp [H]

theorem H_one : H 1 = (1 : K) := by simp [H]

theorem H_succ {n : ℕ} (hn : 1 ≤ n) : H (n + 1) = H n * (1 + 1 / (3 * (n : K))) := by
  unfold H; rw [Finset.prod_Ico_succ_top hn]

theorem H_succ' {n : ℕ} (hn : 1 ≤ n) : H (n + 1) = H n * (3 * (n : K) + 1) / (3 * n) := by
  have hn' : (0 : K) < n := by exact_mod_cast hn
  rw [H_succ hn]; field_simp

theorem H_pos (n : ℕ) : 0 < (H n : K) := by
  unfold H
  apply Finset.prod_pos
  intro m _
  positivity

theorem Po_of_le {a b : ℕ} (h : a ≤ b) : Po a b = H a * ((b : K) + ((a : K) - 1) / 2) := by
  simp [Po, h]

theorem Po_of_ge {a b : ℕ} (h : b ≤ a) : Po a b = H b * ((a : K) + ((b : K) - 1) / 2) := by
  unfold Po
  split_ifs with h'
  · obtain rfl : a = b := le_antisymm h' h
    rfl
  · rfl

theorem Po_symm (a b : ℕ) : Po a b = (Po b a : K) := by
  rcases le_total a b with h | h
  · rw [Po_of_le h, Po_of_ge h]
  · rw [Po_of_ge h, Po_of_le h]

theorem Po_diag (a : ℕ) : Po a a = (L a : K) := by
  rw [Po_of_le le_rfl, L]; ring

end Profile
