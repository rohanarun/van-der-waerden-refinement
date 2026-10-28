import Profile.Constant

/-!
# Theorem 4, `Po` side: the five further families hold for `Po`

K1 (Kronecker substitution), K2 (stride), K3 (multiples), K4 (Clebsch–Gordan of order `k`),
K5 (alternating sector chains). The tensor side of Theorem 4 (that every symmetrized profile
satisfies them) is not formalized here.
-/

set_option linter.unusedSectionVars false

namespace Profile

open Finset

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

theorem Po_pos {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) : 0 < (Po a b : K) := by
  have haK : (1 : K) ≤ a := by exact_mod_cast ha
  have hbK : (1 : K) ≤ b := by exact_mod_cast hb
  rcases le_total a b with h | h
  · rw [Po_of_le h]; have := H_pos (K := K) a; apply mul_pos this; linarith
  · rw [Po_of_ge h]; have := H_pos (K := K) b; apply mul_pos this; linarith

theorem L_pos {a : ℕ} (ha : 1 ≤ a) : 0 < (L a : K) := by
  rw [← Po_diag]; exact Po_pos ha ha

theorem Po_row_concaveFrom (a : ℕ) : ConcaveFrom (fun x => (Po a x : K)) 1 :=
  fun _ hc => Po_row_concave hc

theorem Po_col_concaveFrom (b : ℕ) : ConcaveFrom (fun x => (Po x b : K)) 1 :=
  fun _ hc => Po_col_concave hc

/-! ## Facts on concave sequences used below -/

/-- Restriction to an arithmetic progression keeps concavity. -/
theorem ConcaveFrom.step {f : ℕ → K} {m : ℕ} (hf : ConcaveFrom f m) {x : ℕ} (hx : m ≤ x)
    {s : ℕ} (hs : 1 ≤ s) : f x + f (x + 2 * s) ≤ 2 * f (x + s) := by
  obtain ⟨n, rfl⟩ : ∃ n, s = n + 1 := ⟨s - 1, by omega⟩
  have hlow := hf.sum_lower hx n
  have hup := hf.sum_upper (i := x + n + 1) (by omega) (n + 1)
  have hr := hf.incr_anti (i := x + n) (j := x + n + 1) (by omega) (by omega)
  rw [show x + n + 1 + (n + 1) = x + 2 * (n + 1) by ring] at hup
  rw [show x + (n + 1) = x + n + 1 by ring]
  push_cast at hup
  have hn : (0 : K) ≤ (n : K) + 1 := by positivity
  nlinarith

/-- Symmetric pairs: `f(c+d) + f(c-d) ≤ 2 f(c)` for `d < c`. -/
theorem ConcaveFrom.pair {f : ℕ → K} (hf : ConcaveFrom f 1) {c d : ℕ} (hdc : d < c) :
    f (c + d) + f (c - d) ≤ 2 * f c := by
  rcases Nat.eq_zero_or_pos d with rfl | hd
  · simp; linarith
  have := hf.step (x := c - d) (by omega) (s := d) hd
  rw [show c - d + 2 * d = c + d by omega, show c - d + d = c by omega] at this
  linarith

/-- With `f(0) := 2f(1) - f(2) ≥ 0` the extended sequence is concave from `0`, so `f(x)/x` is
nonincreasing: `x f(y) ≤ y f(x)` for `1 ≤ x ≤ y`. -/
theorem ConcaveFrom.ratio_anti {f : ℕ → K} (hf : ConcaveFrom f 1) (h0 : f 2 ≤ 2 * f 1)
    {x y : ℕ} (hx : 1 ≤ x) (hxy : x ≤ y) : (x : K) * f y ≤ y * f x := by
  set g : ℕ → K := fun n => if n = 0 then 2 * f 1 - f 2 else f n with hg
  have hg0 : 0 ≤ g 0 := by simp [g]; linarith
  have hgc : ConcaveFrom g 0 := by
    intro b _
    rcases Nat.eq_zero_or_pos b with rfl | hb
    · simp [g]
    · simp only [g, if_neg (show b ≠ 0 by omega), if_neg (show b + 2 ≠ 0 by omega),
        if_neg (show b + 1 ≠ 0 by omega)]
      exact hf b hb
  have hgf : ∀ n, 1 ≤ n → g n = f n := fun n hn => by simp [g, show n ≠ 0 by omega]
  -- one step: `(n+1) g(n) ≥ n g(n+1) + g(0)`, from the chord through `0, n, n+1`
  have step : ∀ n : ℕ, 1 ≤ n → (n : K) * g (n + 1) ≤ ((n : K) + 1) * g n := by
    intro n hn
    obtain ⟨k, rfl⟩ : ∃ k, n = k + 1 := ⟨n - 1, by omega⟩
    have hlow := hgc.sum_lower (x := 0) le_rfl k
    have hr := hgc.incr_anti (i := k) (j := k + 1) (by omega) (by omega)
    simp only [zero_add] at hlow
    push_cast
    nlinarith
  induction y, hxy using Nat.le_induction with
  | base => exact le_of_eq (by ring)
  | succ y hxy ih =>
    have hy : 1 ≤ y := le_trans hx hxy
    have hs := step y hy
    rw [hgf y hy, hgf (y + 1) (by omega)] at hs
    have hxK : (1 : K) ≤ x := by exact_mod_cast hx
    have hyK : (1 : K) ≤ y := by exact_mod_cast hy
    push_cast
    -- `y · x f(y+1) ≤ x (y+1) f(y) ≤ (y+1) y f(x)`
    have h1 : (y : K) * ((x : K) * f (y + 1)) ≤ (y : K) * (((y : K) + 1) * f x) := by
      calc (y : K) * ((x : K) * f (y + 1)) = (x : K) * ((y : K) * f (y + 1)) := by ring
        _ ≤ (x : K) * (((y : K) + 1) * f y) :=
            mul_le_mul_of_nonneg_left hs (by linarith)
        _ = ((y : K) + 1) * ((x : K) * f y) := by ring
        _ ≤ ((y : K) + 1) * ((y : K) * f x) :=
            mul_le_mul_of_nonneg_left ih (by linarith)
        _ = (y : K) * (((y : K) + 1) * f x) := by ring
    exact le_of_mul_le_mul_left h1 (by linarith)

/-- `P(a,2) ≤ 2 P(a,1) = 2a` (this is K4'). -/
theorem Po_row_two_le {a : ℕ} (ha : 1 ≤ a) : Po a 2 ≤ 2 * (Po a 1 : K) := by
  rw [Po_symm a 1, Po_one_left ha]
  rcases Nat.lt_or_ge a 2 with h | h
  · obtain rfl : a = 1 := by omega
    rw [Po_one_left (by omega)]; norm_num
  · rw [Po_of_ge h, H_succ' (n := 1) le_rfl, H_one]
    have : (2 : K) ≤ a := by exact_mod_cast h
    push_cast; nlinarith

/-! ## The five families -/

/-- **K3.** `P(a, m b) ≤ m P(a, b)`. -/
theorem K3 {a b m : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) (hm : 1 ≤ m) : Po a (m * b) ≤ (m : K) * Po a b := by
  have := (Po_row_concaveFrom (K := K) a).ratio_anti (Po_row_two_le ha) hb
    (show b ≤ m * b from Nat.le_mul_of_pos_left b hm)
  simp only at this
  have hbK : (0 : K) < b := by exact_mod_cast hb
  push_cast at this
  nlinarith

/-- The pairing behind K4: `Σ_{i<n} f(c+n-1-2i) ≤ n f(c)` for `n ≤ c`. -/
theorem ConcaveFrom.sum_symm {f : ℕ → K} (hf : ConcaveFrom f 1) {c n : ℕ} (hnc : n ≤ c) :
    ∑ i ∈ range n, f (c + n - 1 - 2 * i) ≤ n * f c := by
  have hrefl : ∑ i ∈ range n, f (c + n - 1 - 2 * i) = ∑ i ∈ range n, f (c + 1 + 2 * i - n) := by
    rw [← Finset.sum_range_reflect]
    apply Finset.sum_congr rfl
    intro i hi
    rw [Finset.mem_range] at hi
    congr 1; omega
  have h2 : 2 * ∑ i ∈ range n, f (c + n - 1 - 2 * i) ≤ 2 * (n * f c) := by
    calc 2 * ∑ i ∈ range n, f (c + n - 1 - 2 * i)
        = ∑ i ∈ range n, (f (c + n - 1 - 2 * i) + f (c + 1 + 2 * i - n)) := by
          rw [Finset.sum_add_distrib, ← hrefl]; ring
      _ ≤ ∑ _i ∈ range n, 2 * f c := by
          apply Finset.sum_le_sum
          intro i hi
          rw [Finset.mem_range] at hi
          rcases le_total (2 * i + 1) n with h | h
          · have := hf.pair (c := c) (d := n - 1 - 2 * i) (by omega)
            rw [show c + (n - 1 - 2 * i) = c + n - 1 - 2 * i by omega,
              show c - (n - 1 - 2 * i) = c + 1 + 2 * i - n by omega] at this
            exact this
          · have := hf.pair (c := c) (d := 2 * i + 1 - n) (by omega)
            rw [show c + (2 * i + 1 - n) = c + 1 + 2 * i - n by omega,
              show c - (2 * i + 1 - n) = c + n - 1 - 2 * i by omega] at this
            linarith
      _ = 2 * (n * f c) := by rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul]; ring
  linarith

/-- **K4.** `k P(a,b) ≥ Σ_{i < min(b,k)} P(a, b+k-1-2i)`. -/
theorem K4 {a b k : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) :
    ∑ i ∈ range (min b k), Po a (b + k - 1 - 2 * i) ≤ (k : K) * Po a b := by
  have hf := Po_row_concaveFrom (K := K) a
  rcases le_total k b with h | h
  · rw [min_eq_right h]
    have := hf.sum_symm (c := b) (n := k) h
    exact this
  · rw [min_eq_left h]
    have hs := hf.sum_symm (c := k) (n := b) h
    simp only at hs
    have hr := hf.ratio_anti (Po_row_two_le ha) hb h
    simp only at hr
    calc ∑ i ∈ range b, Po a (b + k - 1 - 2 * i)
        = ∑ i ∈ range b, Po a (k + b - 1 - 2 * i) := by
          apply Finset.sum_congr rfl; intro i _; rw [Nat.add_comm b k]
      _ ≤ (b : K) * Po a k := hs
      _ ≤ (k : K) * Po a b := hr

/-- **K4'.** `P(a,2) ≤ 2a`. -/
theorem K4' {a : ℕ} (ha : 1 ≤ a) : Po a 2 ≤ 2 * (a : K) := by
  have := Po_row_two_le (K := K) ha
  rwa [Po_symm a 1, Po_one_left ha] at this

/-- `Po(a,h) ≤ ℓ(h) = H_a (h + (a-1)/2)` for every `h ≥ 1`, with equality for `h ≥ a`. -/
theorem Po_le_line {a h : ℕ} (hh : 1 ≤ h) : Po a h ≤ H a * ((h : K) + ((a : K) - 1) / 2) := by
  rcases le_total a h with hah | hah
  · rw [Po_of_le hah]
  · rw [Po_of_ge hah]
    have := tripling_aux (K := K) hh a hah
    linarith

/-- **K5.** `P(a, h_1+…+h_m + (a-1)⌊m/2⌋) ≥ Σ P(a,h_i)`, all `h_i ≥ 1`, `m ≥ 1`. -/
theorem K5 {a m : ℕ} (ha : 1 ≤ a) (hm : 1 ≤ m) (h : ℕ → ℕ) (hh : ∀ i ∈ range m, 1 ≤ h i) :
    ∑ i ∈ range m, (Po a (h i) : K) ≤ Po a (∑ i ∈ range m, h i + (a - 1) * (m / 2)) := by
  have haK : (1 : K) ≤ a := by exact_mod_cast ha
  have hsum : m ≤ ∑ i ∈ range m, h i := by
    calc m = ∑ _i ∈ range m, 1 := by simp
      _ ≤ ∑ i ∈ range m, h i := Finset.sum_le_sum hh
  rcases Nat.lt_or_ge m 2 with h1 | h2
  · obtain rfl : m = 1 := by omega
    simp
  have hB : a ≤ ∑ i ∈ range m, h i + (a - 1) * (m / 2) := by
    have : 1 ≤ m / 2 := by omega
    have := Nat.le_mul_of_pos_right (a - 1) this
    omega
  rw [Po_of_le hB]
  calc ∑ i ∈ range m, (Po a (h i) : K)
      ≤ ∑ i ∈ range m, H a * ((h i : K) + ((a : K) - 1) / 2) :=
        Finset.sum_le_sum fun i hi => Po_le_line (hh i hi)
    _ = H a * ((∑ i ∈ range m, (h i : K)) + m * (((a : K) - 1) / 2)) := by
        rw [← Finset.mul_sum, Finset.sum_add_distrib, Finset.sum_const, Finset.card_range,
          nsmul_eq_mul]
    _ ≤ H a * (((∑ i ∈ range m, h i + (a - 1) * (m / 2) : ℕ) : K) + ((a : K) - 1) / 2) := by
        apply mul_le_mul_of_nonneg_left _ (H_pos a).le
        push_cast
        rw [Nat.cast_sub ha]
        have hfl : (m : K) ≤ 2 * ((m / 2 : ℕ) : K) + 1 := by
          have : m ≤ 2 * (m / 2) + 1 := by omega
          exact_mod_cast this
        push_cast
        nlinarith

/-- The diagonal values grow at least like `κ_2^3 = L_2^3/2^4` in cube form:
`L_2^3 s^4 ≤ 16 L_s^3` for `s ≥ 2`. -/
theorem kappa_cube_ge_two {s : ℕ} (hs : 2 ≤ s) :
    L 2 ^ 3 * (s : K) ^ 4 ≤ 2 ^ 4 * L s ^ 3 := by
  induction s, hs using Nat.le_induction with
  | base => push_cast; apply le_of_eq; ring
  | succ s hs ih =>
    have := kappa_cube_strictMono (K := K) (a := s) (by omega)
    have hsK : (2 : K) ≤ s := by exact_mod_cast hs
    have hL := pow_pos (L_pos (K := K) (a := s) (by omega)) 3
    push_cast
    -- `L_2^3 (s+1)^4 s^4 ≤ 16 L_s^3 (s+1)^4 < 16 L_{s+1}^3 s^4`
    have h1 : L 2 ^ 3 * ((s : K) + 1) ^ 4 * (s : K) ^ 4
        ≤ 2 ^ 4 * L (s + 1) ^ 3 * (s : K) ^ 4 := by
      calc L 2 ^ 3 * ((s : K) + 1) ^ 4 * (s : K) ^ 4
          = (L 2 ^ 3 * (s : K) ^ 4) * ((s : K) + 1) ^ 4 := by ring
        _ ≤ (2 ^ 4 * L s ^ 3) * ((s : K) + 1) ^ 4 :=
            mul_le_mul_of_nonneg_right ih (by positivity)
        _ = 2 ^ 4 * (L s ^ 3 * ((s : K) + 1) ^ 4) := by ring
        _ ≤ 2 ^ 4 * (L (s + 1) ^ 3 * (s : K) ^ 4) := by linarith
        _ = 2 ^ 4 * L (s + 1) ^ 3 * (s : K) ^ 4 := by ring
    exact le_of_mul_le_mul_right h1 (by positivity)

theorem L_two : L 2 = (10 / 3 : K) := by
  rw [L, H_succ' (n := 1) le_rfl, H_one]; norm_num

/-- `L_{sc} ≤ L_s L_c`: `κ_{sc} < (3/2)^(4/3) ≤ κ_2^2 ≤ κ_s κ_c` for `s, c ≥ 2`. -/
theorem L_mul_le {s c : ℕ} (hs : 1 ≤ s) (hc : 1 ≤ c) : L (s * c) ≤ (L s * L c : K) := by
  have hL1 : L 1 = (1 : K) := by rw [L, H_one]; norm_num
  rcases Nat.eq_or_lt_of_le hs with rfl | hs2
  · rw [one_mul, hL1, one_mul]
  rcases Nat.eq_or_lt_of_le hc with rfl | hc2
  · rw [mul_one, hL1, mul_one]
  have hsK : (2 : K) ≤ s := by exact_mod_cast hs2
  have hcK : (2 : K) ≤ c := by exact_mod_cast hc2
  have h1 := kappa_cube_lt (K := K) (a := s * c) (by nlinarith)
  have h2 := kappa_cube_ge_two (K := K) (s := s) hs2
  have h3 := kappa_cube_ge_two (K := K) (s := c) hc2
  rw [L_two] at h2 h3
  have hLs := L_pos (K := K) hs
  have hLc := L_pos (K := K) hc
  have hLsc := L_pos (K := K) (a := s * c) (by nlinarith)
  push_cast at h1
  -- cubes: `L_{sc}^3 < (81/16)(sc)^4 ≤ L_s^3 L_c^3`
  have hprod : (81 / 16 : K) * ((s : K) * c) ^ 4 ≤ L s ^ 3 * L c ^ 3 := by
    have hs4 : (0 : K) ≤ (s : K) ^ 4 := by positivity
    have hc4 : (0 : K) ≤ (c : K) ^ 4 := by positivity
    have := mul_le_mul h2 h3 (by positivity) (by positivity)
    nlinarith
  have hcube : (L (s * c) : K) ^ 3 ≤ (L s * L c) ^ 3 := by rw [mul_pow]; linarith
  exact le_of_pow_le_pow_left₀ three_ne_zero (mul_pos hLs hLc).le hcube

/-- **K2.** `P(sc, sd) ≤ P(s,s) P(c,d)`. -/
theorem K2 {s c d : ℕ} (hs : 1 ≤ s) (hc : 1 ≤ c) (hd : 1 ≤ d) :
    Po (s * c) (s * d) ≤ (Po s s * Po c d : K) := by
  -- reduce to `c ≤ d` by symmetry
  wlog hcd : c ≤ d generalizing c d
  · rw [Po_symm (s * c), Po_symm c]; exact this hd hc (by omega)
  have hsK : (1 : K) ≤ s := by exact_mod_cast hs
  have hcK : (1 : K) ≤ c := by exact_mod_cast hc
  have hdK : (c : K) ≤ d := by exact_mod_cast hcd
  have hL := L_mul_le (K := K) hs hc
  rw [Po_of_le (Nat.mul_le_mul_left s hcd), Po_diag, Po_of_le hcd]
  simp only [L] at hL ⊢
  push_cast at hL ⊢
  have hHsc := H_pos (K := K) (s * c)
  have hHc := H_pos (K := K) c
  have hLs := L_pos (K := K) hs
  rw [L] at hLs
  -- linear in `X = d + (c-1)/2 ≥ (3c-1)/2`: the case `d = c` is `hL`, and the slope `s H_{sc}`
  -- is at most `L_s H_c` because `s (3c-1) ≤ 3sc - 1`
  set A : K := H (s * c)
  set B := (3 * (s : K) - 1) / 2 * H s * H c
  have hB : 0 < B := by simp only [B]; nlinarith
  have hL' : (3 * ((s : K) * c) - 1) * A ≤ (3 * c - 1) * B := by simp only [B]; linarith
  have hsc : (s : K) * (3 * c - 1) ≤ 3 * (s * c) - 1 := by nlinarith
  have hpos : (0 : K) < 3 * (s * c) - 1 := by nlinarith
  have hslope : (s : K) * A ≤ B := by
    have h1 : (s : K) * A * (3 * (s * c) - 1) ≤ B * (3 * (s * c) - 1) := by
      calc (s : K) * A * (3 * (s * c) - 1) = (s : K) * ((3 * ((s : K) * c) - 1) * A) := by ring
        _ ≤ (s : K) * ((3 * c - 1) * B) := mul_le_mul_of_nonneg_left hL' (by linarith)
        _ = ((s : K) * (3 * c - 1)) * B := by ring
        _ ≤ (3 * (s * c) - 1) * B := mul_le_mul_of_nonneg_right hsc hB.le
        _ = B * (3 * (s * c) - 1) := by ring
    exact le_of_mul_le_mul_right h1 hpos
  have hX : (0 : K) ≤ ((d : K) + ((c : K) - 1) / 2) - (3 * c - 1) / 2 := by linarith
  have key : A * ((s : K) * d + ((s : K) * c - 1) / 2)
      = ((s : K) * A - B) * (((d : K) + ((c : K) - 1) / 2) - (3 * c - 1) / 2)
        + B * ((d : K) + ((c : K) - 1) / 2) + ((3 * ((s : K) * c) - 1) * A - (3 * c - 1) * B) / 2 := by
    ring
  have hgoal : A * ((s : K) * d + ((s : K) * c - 1) / 2) ≤ B * ((d : K) + ((c : K) - 1) / 2) := by
    rw [key]
    have := mul_nonpos_of_nonpos_of_nonneg (by linarith : (s : K) * A - B ≤ 0) hX
    linarith
  simp only [B] at hgoal
  linarith

/-- The index comparison behind K1's tripling: the margin is `a - 1`. -/
theorem idx_margin (a b k x h : ℕ) (hk : k + 1 = a + b) (ha : 1 ≤ a) :
    3 * (b + k * h) + (a + k * x) - 1 ≤ b + k * (3 * h + x + 2) := by
  have : k * (3 * h + x + 2) = 3 * (k * h) + k * x + 2 * k := by ring
  omega

/-- **K1.** `P(a,b) P(c,d) ≤ P(a + K(c-1), b + K(d-1))` with `K = a+b-1`, via Theorem 1 (ii)
applied to `Q(c,d) = P(a + K(c-1), b + K(d-1)) / P(a,b)`. -/
theorem K1 {a b c d : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) (hc : 1 ≤ c) (hd : 1 ≤ d) :
    (Po a b * Po c d : K) ≤ Po (a + (a + b - 1) * (c - 1)) (b + (a + b - 1) * (d - 1)) := by
  set k := a + b - 1 with hk
  have hk1 : 1 ≤ k := by omega
  have hP := Po_pos (K := K) ha hb
  let Q : ℕ → ℕ → K := fun x y => Po (a + k * (x - 1)) (b + k * (y - 1)) / Po a b
  have hQ : LowerAdmissible Q := by
    refine ⟨?_, ?_, ?_, ?_, ?_⟩
    · simp only [Q, Nat.sub_self, mul_zero, add_zero]; rw [div_self hP.ne']
    · intro x y _ hy
      simp only [Q]
      rw [div_add_div_same, ← mul_div_assoc, div_le_div_iff_of_pos_right hP]
      have := (Po_row_concaveFrom (K := K) (a + k * (x - 1))).step
        (x := b + k * (y - 1)) (by omega) hk1
      simp only at this
      rw [show b + k * (y - 1) + 2 * k = b + k * (y + 2 - 1) by
          rw [show y + 2 - 1 = (y - 1) + 2 by omega]; ring,
        show b + k * (y - 1) + k = b + k * (y + 1 - 1) by
          rw [show y + 1 - 1 = (y - 1) + 1 by omega]; ring] at this
      exact this
    · intro y x _ hx
      simp only [Q]
      rw [div_add_div_same, ← mul_div_assoc, div_le_div_iff_of_pos_right hP]
      have := (Po_col_concaveFrom (K := K) (b + k * (y - 1))).step
        (x := a + k * (x - 1)) (by omega) hk1
      simp only at this
      rw [show a + k * (x - 1) + 2 * k = a + k * (x + 2 - 1) by
          rw [show x + 2 - 1 = (x - 1) + 2 by omega]; ring,
        show a + k * (x - 1) + k = a + k * (x + 1 - 1) by
          rw [show x + 1 - 1 = (x - 1) + 1 by omega]; ring] at this
      exact this
    · -- tripling in the second coordinate, with margin `a - 1`
      intro x h hx hh
      simp only [Q]
      rw [← mul_div_assoc, div_le_div_iff_of_pos_right hP]
      obtain ⟨h', rfl⟩ : ∃ h', h = h' + 1 := ⟨h - 1, by omega⟩
      obtain ⟨x', rfl⟩ : ∃ x', x = x' + 1 := ⟨x - 1, by omega⟩
      rw [show 3 * (h' + 1) + (x' + 1) - 1 - 1 = 3 * h' + x' + 2 by omega]
      simp only [Nat.add_sub_cancel]
      have htr := Po_row_tripling (K := K) (a := a + k * x') (h := b + k * h') (by omega)
        (by omega)
      have hmono := Po_row_mono_le (K := K) (a := a + k * x')
        (b := 3 * (b + k * h') + (a + k * x') - 1) (b' := b + k * (3 * h' + x' + 2)) (by omega)
        (idx_margin a b k x' h' (by omega) ha)
      linarith
    · -- tripling in the first coordinate, with margin `b - 1`
      intro y h hy hh
      simp only [Q]
      rw [← mul_div_assoc, div_le_div_iff_of_pos_right hP]
      obtain ⟨h', rfl⟩ : ∃ h', h = h' + 1 := ⟨h - 1, by omega⟩
      obtain ⟨y', rfl⟩ : ∃ y', y = y' + 1 := ⟨y - 1, by omega⟩
      rw [show 3 * (h' + 1) + (y' + 1) - 1 - 1 = 3 * h' + y' + 2 by omega]
      simp only [Nat.add_sub_cancel]
      have htr := Po_col_tripling (K := K) (b := b + k * y') (h := a + k * h') (by omega)
        (by omega)
      have hmono := Po_col_mono_le (K := K) (b := b + k * y')
        (a := 3 * (a + k * h') + (b + k * y') - 1) (a' := a + k * (3 * h' + y' + 2)) (by omega)
        (idx_margin b a k y' h' (by omega) hb)
      linarith
  have := hQ.Po_le hc hd
  simp only [Q] at this
  rw [le_div_iff₀ hP] at this
  linarith

/-- **Corollary 5.** `Po` satisfies (S), (N), (C), (T), K1–K5 and (E_{3/4}); being least for
(S), (N), (C), (T) alone, it is least for the enlarged system too. -/
theorem corollary5 {P : ℕ → ℕ → K} (hP : LowerAdmissible P) {a b : ℕ} (ha : 1 ≤ a)
    (hb : 1 ≤ b) : Po a b ≤ P a b ∧ (Po a b : K) ^ 3 ≤ ((a : K) + b - 1) ^ 4 :=
  ⟨hP.Po_le ha hb, Po_envelope ha hb⟩

end Profile
