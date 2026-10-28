import Profile.Admissible

/-!
# Theorem 1 (ii): `Po` is the least element

A function `P` on pairs of positive integers with `P(1,1) ≥ 1`, discrete concavity in each
coordinate separately and shifted tripling in each coordinate dominates `Po` pointwise.
Symmetry is not assumed. With Theorem 1 (i), `Po` is the least profile satisfying
(S), (N), (C), (T).
-/

set_option linter.unusedSectionVars false

namespace Profile

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

/-! ## Concave sequences -/

/-- `f` is discretely concave on `[m, ∞)`. -/
def ConcaveFrom (f : ℕ → K) (m : ℕ) : Prop := ∀ b, m ≤ b → f b + f (b + 2) ≤ 2 * f (b + 1)

theorem ConcaveFrom.incr_anti {f : ℕ → K} {m : ℕ} (hf : ConcaveFrom f m) {i j : ℕ}
    (hi : m ≤ i) (hij : i ≤ j) : f (j + 1) - f j ≤ f (i + 1) - f i := by
  induction j, hij using Nat.le_induction with
  | base => exact le_rfl
  | succ j hij ih => have := hf j (le_trans hi hij); linarith

/-- `f(i+n) - f(i) ≤ n (f(i+1) - f(i))`. -/
theorem ConcaveFrom.sum_upper {f : ℕ → K} {m : ℕ} (hf : ConcaveFrom f m) {i : ℕ} (hi : m ≤ i)
    (n : ℕ) : f (i + n) - f i ≤ n * (f (i + 1) - f i) := by
  induction n with
  | zero => simp
  | succ n ih =>
    have := hf.incr_anti hi (Nat.le_add_right i n)
    rw [← add_assoc]; push_cast; linarith

/-- `f(x+n+1) - f(x) ≥ (n+1) (f(x+n+1) - f(x+n))`. -/
theorem ConcaveFrom.sum_lower {f : ℕ → K} {m : ℕ} (hf : ConcaveFrom f m) {x : ℕ} (hx : m ≤ x)
    (n : ℕ) : ((n : K) + 1) * (f (x + n + 1) - f (x + n)) ≤ f (x + n + 1) - f x := by
  induction n with
  | zero => simp
  | succ n ih =>
    have := hf (x + n) (by omega)
    rw [show x + (n + 1) + 1 = x + n + 2 by ring, show x + (n + 1) = x + n + 1 by ring]
    push_cast
    nlinarith

/-- A concave sequence that is `≥ 0` at `x` and `z` is `≥ 0` in between. -/
theorem ConcaveFrom.nonneg_between {f : ℕ → K} {m : ℕ} (hf : ConcaveFrom f m) {x y z : ℕ}
    (hx : m ≤ x) (hxy : x ≤ y) (hyz : y ≤ z) (h0x : 0 ≤ f x) (h0z : 0 ≤ f z) : 0 ≤ f y := by
  rcases Nat.eq_or_lt_of_le hxy with rfl | hxy'
  · exact h0x
  obtain ⟨n, rfl⟩ : ∃ n, y = x + n + 1 := ⟨y - x - 1, by omega⟩
  -- `r` is the last increment before `y`; `f y - f x ≥ (y-x) r` and `f z - f y ≤ (z-y) r`
  have hlow := hf.sum_lower hx n
  have hup := hf.sum_upper (i := x + n + 1) (by omega) (z - (x + n + 1))
  have hr := hf.incr_anti (i := x + n) (j := x + n + 1) (by omega) (by omega)
  rw [show x + n + 1 + (z - (x + n + 1)) = z by omega] at hup
  have hzy : (0 : K) ≤ ((z - (x + n + 1) : ℕ) : K) := Nat.cast_nonneg _
  set r := f (x + n + 1) - f (x + n)
  have hup' : f z - f (x + n + 1) ≤ ((z - (x + n + 1) : ℕ) : K) * r := by
    calc f z - f (x + n + 1) ≤ ((z - (x + n + 1) : ℕ) : K) * (f (x + n + 1 + 1) - f (x + n + 1)) :=
          hup
      _ ≤ ((z - (x + n + 1) : ℕ) : K) * r := mul_le_mul_of_nonneg_left hr hzy
  by_contra hneg
  push_neg at hneg
  -- `f y < 0 ≤ f x` makes `r < 0`, and then `f z < f y < 0`
  have hn1 : (0 : K) < (n : K) + 1 := by positivity
  have hr0 : r < 0 := by
    by_contra hr0; push_neg at hr0
    have : 0 ≤ ((n : K) + 1) * r := mul_nonneg hn1.le hr0
    linarith
  have : ((z - (x + n + 1) : ℕ) : K) * r ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hzy hr0.le
  linarith

/-! ## The hypotheses of Theorem 1 (ii) -/

/-- `P(1,1) ≥ 1`, separate concavity and shifted tripling, in both coordinates. -/
structure LowerAdmissible (P : ℕ → ℕ → K) : Prop where
  one : 1 ≤ P 1 1
  row_concave : ∀ a c, 1 ≤ a → 1 ≤ c → P a c + P a (c + 2) ≤ 2 * P a (c + 1)
  col_concave : ∀ b c, 1 ≤ b → 1 ≤ c → P c b + P (c + 2) b ≤ 2 * P (c + 1) b
  row_tripling : ∀ a h, 1 ≤ a → 1 ≤ h → 3 * P a h ≤ P a (3 * h + a - 1)
  col_tripling : ∀ b h, 1 ≤ b → 1 ≤ h → 3 * P h b ≤ P (3 * h + b - 1) b

theorem LowerAdmissible.transpose {P : ℕ → ℕ → K} (hP : LowerAdmissible P) :
    LowerAdmissible (fun a b => P b a) where
  one := hP.one
  row_concave a c ha hc := hP.col_concave a c ha hc
  col_concave b c hb hc := hP.row_concave b c hb hc
  row_tripling a h ha hh := hP.col_tripling a h ha hh
  col_tripling b h hb hh := hP.row_tripling b h hb hh

theorem Po_lowerAdmissible : LowerAdmissible (Po : ℕ → ℕ → K) where
  one := by rw [Po_one_left le_rfl]; norm_num
  row_concave _ _ _ hc := Po_row_concave hc
  col_concave _ _ _ hc := Po_col_concave hc
  row_tripling _ _ ha hh := Po_row_tripling ha hh
  col_tripling _ _ hb hh := Po_col_tripling hb hh

/-! ## The diagonal: `P(a,a) ≥ L_a` -/

/-- The paper's Lemma 5.1 with exact constants and the column increment in place of symmetry. -/
theorem LowerAdmissible.diag {P : ℕ → ℕ → K} (hP : LowerAdmissible P) {a : ℕ} (ha : 1 ≤ a) :
    L a ≤ P a a := by
  induction a, ha using Nat.le_induction with
  | base => rw [L, H_one]; norm_num; exact hP.one
  | succ a ha ih =>
    have haK : (1 : K) ≤ a := by exact_mod_cast ha
    have hrow : ConcaveFrom (P (a + 1)) 1 := fun c hc => hP.row_concave (a + 1) c (by omega) hc
    have hcol : ConcaveFrom (fun x => P x a) 1 := fun c hc => hP.col_concave a c ha hc
    -- the row increment at the diagonal: `(3a+2) r ≥ 2 D_{a+1}` (row tripling at `h = a+1`)
    have htr := hP.row_tripling (a + 1) (a + 1) (by omega) (by omega)
    have hsum := hrow.sum_upper (i := a + 1) (by omega) (3 * a + 2)
    rw [show a + 1 + (3 * a + 2) = 3 * (a + 1) + (a + 1) - 1 by omega] at hsum
    -- it is at most the increment just before the diagonal
    have hanti := hrow.incr_anti (i := a) (j := a + 1) ha (by omega)
    -- the column increment at the diagonal: `(3a-1) c ≥ 2 D_a` (column tripling at `h = a`)
    have htc := hP.col_tripling a a ha ha
    have hcs := hcol.sum_upper (i := a) ha (3 * a - 1)
    simp only at hcs
    rw [show a + (3 * a - 1) = 3 * a + a - 1 by omega] at hcs
    rw [show ((3 * a - 1 : ℕ) : K) = 3 * a - 1 by rw [Nat.cast_sub (by omega)]; push_cast; ring]
      at hcs
    push_cast at hsum
    set D := P (a + 1) (a + 1)
    set r := P (a + 1) (a + 1 + 1) - D
    set c := P (a + 1) a - P a a
    have hr : 2 * D ≤ (3 * (a : K) + 2) * r := by linarith
    have hc : 2 * P a a ≤ (3 * (a : K) - 1) * c := by linarith
    have hH := H_pos (K := K) a
    rw [L] at ih
    -- `c ≥ H_a`
    have hcH : H a ≤ c := by
      by_contra hlt; push_neg at hlt
      have : (3 * (a : K) - 1) * c < (3 * (a : K) - 1) * H a :=
        mul_lt_mul_of_pos_left hlt (by linarith)
      nlinarith
    -- `D - P(a,a) = (D - P(a+1,a)) + c ≥ r + c`
    have hstep : r + c ≤ D - P a a := by simp only [r, c]; linarith
    rw [L, H_succ' ha]; push_cast
    rw [show (3 * ((a : K) + 1) - 1) / 2 * (H a * (3 * a + 1) / (3 * a))
        = (3 * a + 2) * (3 * a + 1) * H a / (6 * a) by field_simp; ring]
    rw [div_le_iff₀ (by positivity)]
    nlinarith

/-! ## Off the diagonal -/

/-- The tripling chain `h_0 = a`, `h_{j+1} = 3 h_j + a - 1`. -/
def chain (a : ℕ) : ℕ → ℕ
  | 0 => a
  | j + 1 => 3 * chain a j + a - 1

theorem chain_ge (a j : ℕ) (ha : 1 ≤ a) : a + j ≤ chain a j := by
  induction j with
  | zero => simp [chain]
  | succ j ih => simp only [chain]; omega

theorem LowerAdmissible.row {P : ℕ → ℕ → K} (hP : LowerAdmissible P) {a b : ℕ} (ha : 1 ≤ a)
    (hab : a ≤ b) : Po a b ≤ P a b := by
  -- `d = P(a,·) - Po(a,·)` is concave on `[a, ∞)`, where `Po(a,·)` is affine
  set d : ℕ → K := fun x => P a x - Po a x
  have hd : ConcaveFrom d a := by
    intro x hx
    have h1 := hP.row_concave a x ha (by omega)
    simp only [d]
    rw [Po_of_le hx, Po_of_le (by omega : a ≤ x + 1), Po_of_le (by omega : a ≤ x + 2)]
    push_cast
    linarith
  -- `d ≥ 0` along the chain, by tripling (exact for `Po` right of the seam)
  have hchain : ∀ j, 0 ≤ d (chain a j) := by
    intro j
    induction j with
    | zero =>
      simp only [d, chain]; rw [Po_diag]; linarith [hP.diag ha]
    | succ j ih =>
      have hj := chain_ge a j ha
      have htr := hP.row_tripling a (chain a j) ha (by omega)
      simp only [d, chain] at ih ⊢
      rw [Po_of_le (by omega : a ≤ 3 * chain a j + a - 1)]
      rw [Po_of_le (by omega : a ≤ chain a j)] at ih
      rw [show ((↑(3 * chain a j + a - 1) : ℕ) : K) = 3 * (chain a j : K) + a - 1 by
        rw [Nat.cast_sub (by omega)]; push_cast; ring]
      nlinarith
  -- every `b ≥ a` lies between two consecutive chain points
  have hex : ∃ j, b < chain a (j + 1) := ⟨b, by have := chain_ge a (b + 1) ha; omega⟩
  classical
  let j := Nat.find hex
  have hj : b < chain a (j + 1) := Nat.find_spec hex
  have hlow : chain a j ≤ b := by
    rcases Nat.eq_zero_or_pos j with h0 | hpos
    · rw [h0]; exact hab
    · have := Nat.find_min hex (show j - 1 < j by omega)
      rw [show j - 1 + 1 = j by omega] at this
      omega
  have := hd.nonneg_between (x := chain a j) (y := b) (z := chain a (j + 1))
    (by have := chain_ge a j ha; omega) hlow hj.le (hchain j) (hchain (j + 1))
  simp only [d] at this
  linarith

/-- **Theorem 1 (ii).** Every `LowerAdmissible` function dominates `Po` pointwise. -/
theorem LowerAdmissible.Po_le {P : ℕ → ℕ → K} (hP : LowerAdmissible P) {a b : ℕ} (ha : 1 ≤ a)
    (hb : 1 ≤ b) : Po a b ≤ P a b := by
  rcases le_total a b with h | h
  · exact hP.row ha h
  · rw [Po_symm]; exact hP.transpose.row hb h

end Profile
