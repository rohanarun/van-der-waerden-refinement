import Vdw.Bounds
namespace Vdw
def LegacyRegion (a m b delta gamma c : ℚ) : Prop :=
  0<a ∧ 0<b ∧ 0<c ∧ 0<gamma ∧ 2*a<m ∧ 3*a<m ∧ m<1 ∧
  3*a+b<1 ∧ b<a ∧ gamma≤delta/4 ∧ gamma<(1-delta)/8 ∧
  4*c<gamma*b ∧ a+m<3

def OuterRegion (a m b delta eps er gamma c : ℚ) : Prop :=
  0<a ∧ 0<b ∧ 0<c ∧ 0<gamma ∧ 2*a<m ∧ m<1 ∧ b<a ∧
  0<eps ∧ eps<1/2 ∧ 0<er ∧ er≤1/2 ∧ 0<delta ∧ delta<1 ∧
  gamma<(1/2-eps)*(1-er)*(1-delta) ∧ a+m<3

def AffineRegion (a m b delta eps er gamma c cost : ℚ) : Prop :=
  OuterRegion a m b delta eps er gamma c ∧ 2*a+b<1 ∧ cost*c<gamma*b

def RunRegion (a m b delta eps er gamma c ds : ℚ) : Prop :=
  OuterRegion a m b delta eps er gamma c ∧ a+b<1 ∧ 2*c<gamma*b ∧ 0<ds ∧ ds<1

theorem pr1_parameters_0 : LegacyRegion (1/10 : ℚ) (1/2 : ℚ) (1/20 : ℚ) (1/10 : ℚ) (1/40 : ℚ) (1/4000 : ℚ)  := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr1_parameters_1 : LegacyRegion (1/5 : ℚ) (3/4 : ℚ) (1/6 : ℚ) (1/10 : ℚ) (1/40 : ℚ) (1/1000 : ℚ)  := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr1_parameters_2 : LegacyRegion (1/4 : ℚ) (4/5 : ℚ) (247/1000 : ℚ) (1/3 : ℚ) (41/500 : ℚ) (1/200 : ℚ)  := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr1_parameters_3 : LegacyRegion (1/4 : ℚ) (4/5 : ℚ) (2499/10000 : ℚ) (1/3 : ℚ) (83/1000 : ℚ) (1/193 : ℚ)  := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr2_parameters_0 : AffineRegion (333/1000 : ℚ) (4/5 : ℚ) (331/1000 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (97/200 : ℚ) (1/25 : ℚ) (4/1 : ℚ) := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr4_parameters : AffineRegion (333/1000 : ℚ) (4/5 : ℚ) (331/1000 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (97/200 : ℚ) (1/19 : ℚ) (3/1 : ℚ) := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr4_tau : (97/600 : ℚ)=(97/200 : ℚ)/3 := by norm_num

theorem pr6_rank_certificate_proposals_0 : AffineRegion (333/1000 : ℚ) (4/5 : ℚ) (331/1000 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (97/200 : ℚ) (1/16 : ℚ) (5/2 : ℚ) := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr7_digit_rank_proposals_0 : AffineRegion (333/1000 : ℚ) (4/5 : ℚ) (331/1000 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (97/200 : ℚ) (2/25 : ℚ) (2/1 : ℚ) := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr7_run_parameters_0 : RunRegion (49/100 : ℚ) (99/100 : ℚ) (97/200 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (97/200 : ℚ) (1/9 : ℚ) (1/2 : ℚ) := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr9_literal_PR6 : AffineRegion (333/1000 : ℚ) (4/5 : ℚ) (331/1000 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (97/200 : ℚ) (1/16 : ℚ) (5/2 : ℚ) := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

theorem pr9_literal_PR7 : RunRegion (49/100 : ℚ) (99/100 : ℚ) (97/200 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (1/200 : ℚ) (97/200 : ℚ) (1/9 : ℚ) (1/2 : ℚ) := by
  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]

end Vdw
