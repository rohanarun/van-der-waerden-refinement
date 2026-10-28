import Profile.Families

/-!
# Corollary 3: the envelope witnesses at `t = 4/5`

On the diagonal, (E_t) at `t = 4/5` reads `L_a ≤ (2a-1)^(5/4)`, i.e. `L_a^4 ≤ (2a-1)^5`. It holds
for `1 ≤ a < 63` and fails at `a = 63`, so `t = 4/5` is not admissible and the first failure
is at `63`. Exact rational arithmetic, checked by kernel reduction (`decide +kernel`, no
`native_decide`) on a computable twin `Hq` of `H`. The witness at `t = 7/9` (`a = 2494`) is too
deep for kernel reduction and stays in `verify.py`.
-/

namespace Profile

/-- A computable twin of `H` over `ℚ`. -/
def Hq : ℕ → ℚ
  | 0 => 1
  | n + 1 => if n = 0 then 1 else Hq n * (3 * n + 1) / (3 * n)

theorem Hq_eq (n : ℕ) : Hq n = (H n : ℚ) := by
  induction n with
  | zero => simp [Hq, H_zero]
  | succ n ih =>
    rcases Nat.eq_zero_or_pos n with rfl | hn
    · simp [Hq, H_one]
    · rw [Hq, if_neg (by omega), ih, H_succ' hn]

theorem L_eq_Hq (a : ℕ) : (L a : ℚ) = (3 * a - 1) / 2 * Hq a := by rw [L, Hq_eq]

set_option maxRecDepth 100000 in
theorem envelope_four_fifths_holds_below_63 :
    ∀ a : ℕ, a < 63 → 1 ≤ a → (L a : ℚ) ^ 4 ≤ (2 * a - 1) ^ 5 := by
  have : ∀ a : ℕ, a < 63 → 1 ≤ a → ((3 * (a : ℚ) - 1) / 2 * Hq a) ^ 4 ≤ (2 * a - 1) ^ 5 := by
    decide +kernel
  intro a h1 h2; rw [L_eq_Hq]; exact this a h1 h2

set_option maxRecDepth 100000 in
theorem envelope_four_fifths_fails_at_63 : ((2 * 63 - 1 : ℕ) : ℚ) ^ 5 < (L 63 : ℚ) ^ 4 := by
  have : (125 : ℚ) ^ 5 < ((3 * 63 - 1) / 2 * Hq 63) ^ 4 := by decide +kernel
  rw [L_eq_Hq]; push_cast; norm_num at this ⊢; exact this

end Profile
