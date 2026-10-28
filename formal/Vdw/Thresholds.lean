import Vdw.Bounds
namespace Vdw
-- Kernel-checked dyadic comparisons; this does not prove analytic monotonicity.
theorem dyadic_from_small {A u : ℚ} {t j n w : ℕ}
    (hu : 0≤u) (hw : w≤n) (hs : A*(t : ℚ)^j ≤ u*2^w) :
    A*(t : ℚ)^j ≤ u*2^n := by
  exact le_trans hs (mul_le_mul_of_nonneg_left
    (pow_le_pow_right₀ (by norm_num : (1 : ℚ)≤2) hw) hu)

-- k>=16
theorem pr9_literal_PR6_check_0 : (4/1 : ℚ) ≤ (33554432/1 : ℚ) := by norm_num

-- logk>=1
theorem pr9_literal_PR6_check_1 : (1/1 : ℚ) ≤ (16777216/1 : ℚ) := by norm_num

-- anchor entropy
theorem pr9_literal_PR6_check_2 : (14720000/1 : ℚ) ≤ (16777216/1 : ℚ) := by norm_num

-- third incidence entropy
theorem pr9_literal_PR6_check_3 : (5040000/1 : ℚ) ≤ (16777216/1 : ℚ) := by norm_num

-- regular fraction
theorem pr9_literal_PR6_check_4 : (1/140737488355328 : ℚ) ≤ (1/200 : ℚ) := by norm_num

-- dimension
theorem pr9_literal_PR6_check_5 :
    0<(667/1000 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(128/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(667/1000 : ℚ) ∧
    (22380806 : ℚ) ≤ (667/1000 : ℚ)*33554432 ∧ (667/1000 : ℚ)*33554432 < 22380806+1 ∧
    (128/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/1 : ℚ)*2^22380806 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 8) <;> norm_num

-- short period cutoff
theorem pr9_literal_PR6_check_6 :
    0<(467/1000 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(8/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (2 : ℚ)/(467/1000 : ℚ) ∧
    (15669919 : ℚ) ≤ (467/1000 : ℚ)*33554432 ∧ (467/1000 : ℚ)*33554432 < 15669919+1 ∧
    (8/1 : ℚ)*(33554432 : ℚ)^2 ≤ (1/1 : ℚ)*2^15669919 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 54) <;> norm_num

-- small blocks
theorem pr9_literal_PR6_check_7 :
    0<(1/5 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(64/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(1/5 : ℚ) ∧
    (6710886 : ℚ) ≤ (1/5 : ℚ)*33554432 ∧ (1/5 : ℚ)*33554432 < 6710886+1 ∧
    (64/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/1 : ℚ)*2^6710886 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 7) <;> norm_num

-- rotating drift
theorem pr9_literal_PR6_check_8 :
    0<(1867/1000 : ℚ) ∧ 0<(1/200 : ℚ) ∧ 0≤(128/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(1867/1000 : ℚ) ∧
    (62646124 : ℚ) ≤ (1867/1000 : ℚ)*33554432 ∧ (1867/1000 : ℚ)*33554432 < 62646124+1 ∧
    (128/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/200 : ℚ)*2^62646124 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 15) <;> norm_num

-- dichotomy remainder
theorem pr9_literal_PR6_check_9 :
    0<(1/5 : ℚ) ∧ 0<(40499/8000000 : ℚ) ∧ 0≤(19701/10000 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(1/5 : ℚ) ∧
    (6710886 : ℚ) ≤ (1/5 : ℚ)*33554432 ∧ (1/5 : ℚ)*33554432 < 6710886+1 ∧
    (19701/10000 : ℚ)*(33554432 : ℚ)^0 ≤ (40499/8000000 : ℚ)*2^6710886 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 9) <;> norm_num

-- flip bias
theorem pr9_literal_PR6_check_10 :
    0<(331/1000 : ℚ) ∧ 0<(1/2 : ℚ) ∧ 0≤(1/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(331/1000 : ℚ) ∧
    (11106516 : ℚ) ≤ (331/1000 : ℚ)*33554432 ∧ (331/1000 : ℚ)*33554432 < 11106516+1 ∧
    (1/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/2 : ℚ)*2^11106516 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 2) <;> norm_num

-- first row size
theorem pr9_literal_PR6_check_11 :
    0<(4/5 : ℚ) ∧ 0<(1/200 : ℚ) ∧ 0≤(160001/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(4/5 : ℚ) ∧
    (26843545 : ℚ) ≤ (4/5 : ℚ)*33554432 ∧ (4/5 : ℚ)*33554432 < 26843545+1 ∧
    (160001/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/200 : ℚ)*2^26843545 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 25) <;> norm_num

-- second size
theorem pr9_literal_PR6_check_12 :
    0<(333/1000 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(320000/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(333/1000 : ℚ) ∧
    (11173625 : ℚ) ≤ (333/1000 : ℚ)*33554432 ∧ (333/1000 : ℚ)*33554432 < 11173625+1 ∧
    (320000/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/1 : ℚ)*2^11173625 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 19) <;> norm_num

-- third size
theorem pr9_literal_PR6_check_13 :
    0<(333/1000 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(320000/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(333/1000 : ℚ) ∧
    (11173625 : ℚ) ≤ (333/1000 : ℚ)*33554432 ∧ (333/1000 : ℚ)*33554432 < 11173625+1 ∧
    (320000/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/1 : ℚ)*2^11173625 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 19) <;> norm_num

-- first incidence
theorem pr9_literal_PR6_check_14 :
    0<(67/500 : ℚ) ∧ 0<(1/8000000 : ℚ) ∧ 0≤(281/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (3 : ℚ)/(67/500 : ℚ) ∧
    (4496293 : ℚ) ≤ (67/500 : ℚ)*33554432 ∧ (67/500 : ℚ)*33554432 < 4496293+1 ∧
    (281/1 : ℚ)*(33554432 : ℚ)^3 ≤ (1/8000000 : ℚ)*2^4496293 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 107) <;> norm_num

-- second incidence
theorem pr9_literal_PR6_check_15 :
    0<(333/1000 : ℚ) ∧ 0<(1/40000 : ℚ) ∧ 0≤(92/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(333/1000 : ℚ) ∧
    (11173625 : ℚ) ≤ (333/1000 : ℚ)*33554432 ∧ (333/1000 : ℚ)*33554432 < 11173625+1 ∧
    (92/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/40000 : ℚ)*2^11173625 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 22) <;> norm_num

-- rich inverse log
theorem pr9_literal_PR6_check_16 : (625/1048576 : ℚ) ≤ (857/1200000 : ℚ) := by norm_num

-- rich dimension error
theorem pr9_literal_PR6_check_17 :
    0<(667/1000 : ℚ) ∧ 0<(857/1200000 : ℚ) ∧ 0≤(10000/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(667/1000 : ℚ) ∧
    (22380806 : ℚ) ≤ (667/1000 : ℚ)*33554432 ∧ (667/1000 : ℚ)*33554432 < 22380806+1 ∧
    (10000/1 : ℚ)*(33554432 : ℚ)^0 ≤ (857/1200000 : ℚ)*2^22380806 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 25) <;> norm_num

-- rich digit error
theorem pr9_literal_PR6_check_18 :
    0<(333/1000 : ℚ) ∧ 0<(857/1200000 : ℚ) ∧ 0≤(10000/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(333/1000 : ℚ) ∧
    (11173625 : ℚ) ≤ (333/1000 : ℚ)*33554432 ∧ (333/1000 : ℚ)*33554432 < 11173625+1 ∧
    (10000/1 : ℚ)*(33554432 : ℚ)^0 ≤ (857/1200000 : ℚ)*2^11173625 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 25) <;> norm_num

-- affine full-label entropy
theorem pr9_literal_PR6_check_19 :
    0<(3/1000 : ℚ) ∧ 0<(1/4 : ℚ) ∧ 0≤(300/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (3 : ℚ)/(3/1000 : ℚ) ∧
    (100663 : ℚ) ≤ (3/1000 : ℚ)*33554432 ∧ (3/1000 : ℚ)*33554432 < 100663+1 ∧
    (300/1 : ℚ)*(33554432 : ℚ)^3 ≤ (1/4 : ℚ)*2^100663 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 86) <;> norm_num

-- affine band entropy
theorem pr9_literal_PR6_check_20 :
    0<(1/500 : ℚ) ∧ 0<(1/4 : ℚ) ∧ 0≤(300/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (1 : ℚ)/(1/500 : ℚ) ∧
    (67108 : ℚ) ≤ (1/500 : ℚ)*33554432 ∧ (1/500 : ℚ)*33554432 < 67108+1 ∧
    (300/1 : ℚ)*(33554432 : ℚ)^1 ≤ (1/4 : ℚ)*2^67108 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 36) <;> norm_num

-- k>=16
theorem pr9_literal_PR7_check_0 : (4/1 : ℚ) ≤ (33554432/1 : ℚ) := by norm_num

-- logk>=1
theorem pr9_literal_PR7_check_1 : (1/1 : ℚ) ≤ (16777216/1 : ℚ) := by norm_num

-- anchor entropy
theorem pr9_literal_PR7_check_2 : (14720000/1 : ℚ) ≤ (16777216/1 : ℚ) := by norm_num

-- third incidence entropy
theorem pr9_literal_PR7_check_3 : (5040000/1 : ℚ) ≤ (16777216/1 : ℚ) := by norm_num

-- regular fraction
theorem pr9_literal_PR7_check_4 : (1/140737488355328 : ℚ) ≤ (1/200 : ℚ) := by norm_num

-- dimension
theorem pr9_literal_PR7_check_5 :
    0<(51/100 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(128/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(51/100 : ℚ) ∧
    (17112760 : ℚ) ≤ (51/100 : ℚ)*33554432 ∧ (51/100 : ℚ)*33554432 < 17112760+1 ∧
    (128/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/1 : ℚ)*2^17112760 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 8) <;> norm_num

-- short period cutoff
theorem pr9_literal_PR7_check_6 :
    0<(1/2 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(8/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (2 : ℚ)/(1/2 : ℚ) ∧
    (16777216 : ℚ) ≤ (1/2 : ℚ)*33554432 ∧ (1/2 : ℚ)*33554432 < 16777216+1 ∧
    (8/1 : ℚ)*(33554432 : ℚ)^2 ≤ (1/1 : ℚ)*2^16777216 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 54) <;> norm_num

-- small blocks
theorem pr9_literal_PR7_check_7 :
    0<(1/100 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(64/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(1/100 : ℚ) ∧
    (335544 : ℚ) ≤ (1/100 : ℚ)*33554432 ∧ (1/100 : ℚ)*33554432 < 335544+1 ∧
    (64/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/1 : ℚ)*2^335544 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 7) <;> norm_num

-- rotating drift
theorem pr9_literal_PR7_check_8 :
    0<(38/25 : ℚ) ∧ 0<(1/200 : ℚ) ∧ 0≤(128/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(38/25 : ℚ) ∧
    (51002736 : ℚ) ≤ (38/25 : ℚ)*33554432 ∧ (38/25 : ℚ)*33554432 < 51002736+1 ∧
    (128/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/200 : ℚ)*2^51002736 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 15) <;> norm_num

-- dichotomy remainder
theorem pr9_literal_PR7_check_9 :
    0<(1/100 : ℚ) ∧ 0<(40499/8000000 : ℚ) ∧ 0≤(19701/10000 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(1/100 : ℚ) ∧
    (335544 : ℚ) ≤ (1/100 : ℚ)*33554432 ∧ (1/100 : ℚ)*33554432 < 335544+1 ∧
    (19701/10000 : ℚ)*(33554432 : ℚ)^0 ≤ (40499/8000000 : ℚ)*2^335544 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 9) <;> norm_num

-- flip bias
theorem pr9_literal_PR7_check_10 :
    0<(97/200 : ℚ) ∧ 0<(1/2 : ℚ) ∧ 0≤(1/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(97/200 : ℚ) ∧
    (16273899 : ℚ) ≤ (97/200 : ℚ)*33554432 ∧ (97/200 : ℚ)*33554432 < 16273899+1 ∧
    (1/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/2 : ℚ)*2^16273899 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 2) <;> norm_num

-- first row size
theorem pr9_literal_PR7_check_11 :
    0<(99/100 : ℚ) ∧ 0<(1/200 : ℚ) ∧ 0≤(160001/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(99/100 : ℚ) ∧
    (33218887 : ℚ) ≤ (99/100 : ℚ)*33554432 ∧ (99/100 : ℚ)*33554432 < 33218887+1 ∧
    (160001/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/200 : ℚ)*2^33218887 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 25) <;> norm_num

-- second size
theorem pr9_literal_PR7_check_12 :
    0<(49/100 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(320000/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(49/100 : ℚ) ∧
    (16441671 : ℚ) ≤ (49/100 : ℚ)*33554432 ∧ (49/100 : ℚ)*33554432 < 16441671+1 ∧
    (320000/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/1 : ℚ)*2^16441671 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 19) <;> norm_num

-- third size
theorem pr9_literal_PR7_check_13 :
    0<(49/100 : ℚ) ∧ 0<(1/1 : ℚ) ∧ 0≤(320000/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(49/100 : ℚ) ∧
    (16441671 : ℚ) ≤ (49/100 : ℚ)*33554432 ∧ (49/100 : ℚ)*33554432 < 16441671+1 ∧
    (320000/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/1 : ℚ)*2^16441671 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 19) <;> norm_num

-- first incidence
theorem pr9_literal_PR7_check_14 :
    0<(1/100 : ℚ) ∧ 0<(1/8000000 : ℚ) ∧ 0≤(281/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (3 : ℚ)/(1/100 : ℚ) ∧
    (335544 : ℚ) ≤ (1/100 : ℚ)*33554432 ∧ (1/100 : ℚ)*33554432 < 335544+1 ∧
    (281/1 : ℚ)*(33554432 : ℚ)^3 ≤ (1/8000000 : ℚ)*2^335544 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 107) <;> norm_num

-- second incidence
theorem pr9_literal_PR7_check_15 :
    0<(49/100 : ℚ) ∧ 0<(1/40000 : ℚ) ∧ 0≤(92/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(49/100 : ℚ) ∧
    (16441671 : ℚ) ≤ (49/100 : ℚ)*33554432 ∧ (49/100 : ℚ)*33554432 < 16441671+1 ∧
    (92/1 : ℚ)*(33554432 : ℚ)^0 ≤ (1/40000 : ℚ)*2^16441671 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 22) <;> norm_num

-- rich inverse log
theorem pr9_literal_PR7_check_16 : (625/1048576 : ℚ) ≤ (4681/2160000 : ℚ) := by norm_num

-- rich dimension error
theorem pr9_literal_PR7_check_17 :
    0<(51/100 : ℚ) ∧ 0<(4681/2160000 : ℚ) ∧ 0≤(10000/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(51/100 : ℚ) ∧
    (17112760 : ℚ) ≤ (51/100 : ℚ)*33554432 ∧ (51/100 : ℚ)*33554432 < 17112760+1 ∧
    (10000/1 : ℚ)*(33554432 : ℚ)^0 ≤ (4681/2160000 : ℚ)*2^17112760 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 23) <;> norm_num

-- rich digit error
theorem pr9_literal_PR7_check_18 :
    0<(49/100 : ℚ) ∧ 0<(4681/2160000 : ℚ) ∧ 0≤(10000/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (0 : ℚ)/(49/100 : ℚ) ∧
    (16441671 : ℚ) ≤ (49/100 : ℚ)*33554432 ∧ (49/100 : ℚ)*33554432 < 16441671+1 ∧
    (10000/1 : ℚ)*(33554432 : ℚ)^0 ≤ (4681/2160000 : ℚ)*2^16441671 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 23) <;> norm_num

-- heavy run entropy
theorem pr9_literal_PR7_check_19 :
    0<(1/40 : ℚ) ∧ 0<(1/8 : ℚ) ∧ 0≤(200/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (3 : ℚ)/(1/40 : ℚ) ∧
    (838860 : ℚ) ≤ (1/40 : ℚ)*33554432 ∧ (1/40 : ℚ)*33554432 < 838860+1 ∧
    (200/1 : ℚ)*(33554432 : ℚ)^3 ≤ (1/8 : ℚ)*2^838860 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 86) <;> norm_num

-- affine key entropy
theorem pr9_literal_PR7_check_20 :
    0<(1/200 : ℚ) ∧ 0<(1/8 : ℚ) ∧ 0≤(200/1 : ℚ) ∧
    (33554432 : ℚ)/2 ≥ (1 : ℚ)/(1/200 : ℚ) ∧
    (167772 : ℚ) ≤ (1/200 : ℚ)*33554432 ∧ (1/200 : ℚ)*33554432 < 167772+1 ∧
    (200/1 : ℚ)*(33554432 : ℚ)^1 ≤ (1/8 : ℚ)*2^167772 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := 36) <;> norm_num

end Vdw
