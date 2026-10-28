#!/usr/bin/env python3
"""Exact sensitivity analysis of the short-period region (c < 1/8).

Base commit: 63bef9ca996786a41169de4a0c3d6b3b47b0fe96.

The short-period region of short-period-runs-proof.md bounds the flip
exponent b only through three inequalities (m is a free auxiliary exponent):

  (F)  2a < m < 1   first local-lemma family, iota_1 = k T_glob e^{-eps^2 delta M}
  (B)  b < a        case (ii): band entropy 6 log q = O(k^{1-a} log k) vs pk
  (R)  a + b < 1    case (ii): run code e^{O(D log^3 k)} vs pk

and the coefficient through 2c < gamma*b with gamma < 1/2, so
sup c = sup(b) / 4.  Eliminating m, (F) is a < 1/2 (it is a < 1 if (F) is
replaced by the weaker a < m < 1 that h_0 < 2M < k still needs).

We compute sup b exactly (vertex enumeration in Fractions over the closed
polygon) for every combination of keeping or relaxing (F), (B), (R), and for
the family (B_theta): b < theta*a.  scipy's LP is used only as a cross-check.
Run with plain `python3 -B verify.py` (assertions are load-bearing; never -O).
"""
from fractions import Fraction as Q
from itertools import combinations
import json, sys

def sup_b(cons):
    """cons: list of (alpha, beta, rhs) meaning alpha*a + beta*b <= rhs.
    Returns max b over the closed polygon (bounded by 0<=a<=1, 0<=b<=1)."""
    cons = cons + [(Q(-1),Q(0),Q(0)),(Q(0),Q(-1),Q(0)),(Q(1),Q(0),Q(1)),(Q(0),Q(1),Q(1))]
    best = None
    for (a1,b1,r1),(a2,b2,r2) in combinations(cons,2):
        det = a1*b2-a2*b1
        if det == 0: continue
        a = (r1*b2-r2*b1)/det; b = (a1*r2-a2*r1)/det
        if all(al*a+be*b <= rh for al,be,rh in cons):
            best = b if best is None or b > best else best
    return best

F_strong = (Q(1),Q(0),Q(1,2))     # 2a < m < 1  ->  a <= 1/2
F_weak   = (Q(1),Q(0),Q(1))       # a < m < 1   ->  a <= 1
B = lambda th=Q(1): (-th,Q(1),Q(0))  # b <= theta*a
R = (Q(1),Q(1),Q(1))              # a + b <= 1

cases = {
  'current region (F,B,R)':            [F_strong,B(),R],
  'relax F only (a<m<1 kept)':         [F_weak,B(),R],
  'drop R only':                       [F_strong,B()],
  'drop B only':                       [F_strong,R],
  'relax F and drop R':                [F_weak,B()],
  'relax F and drop B':                [F_weak,R],
}
out = {}
for name,cons in cases.items():
    sb = sup_b(cons); out[name] = {'sup_b':str(sb),'sup_c':str(sb/4)}

# Expected exact values.
assert out['current region (F,B,R)']['sup_c'] == '1/8'
assert out['relax F only (a<m<1 kept)']['sup_c'] == '1/8'   # no gain
assert out['drop R only']['sup_c'] == '1/8'                 # no gain
assert out['drop B only']['sup_c'] == '1/4'                 # the single lever
assert out['relax F and drop R']['sup_c'] == '1/4'          # needs two changes
assert out['relax F and drop B']['sup_c'] == '1/4'

# Weakening B to b < theta*a (theta >= 1) gives sup c = theta/(4(1+theta)).
theta_table = {}
for th in [Q(1),Q(3,2),Q(2),Q(3),Q(5),Q(10)]:
    sc = sup_b([F_strong,B(th),R])/4
    assert sc == th/(4*(1+th)), (th,sc)
    theta_table[str(th)] = str(sc)
# Strengthening B (theta < 1) lowers the ceiling to theta/8: a negative control.
for th in [Q(1,2),Q(3,4)]:
    assert sup_b([F_strong,B(th),R])/4 == th/8

# The repo's explicit point c=1/9 lies in the current region (independent check).
a,m,b,g,c = Q(49,100),Q(99,100),Q(97,200),Q(97,200),Q(1,9)
assert 2*a < m < 1 and b < a and a+b < 1 and 2*c < g*b and g < Q(1,2)

# Floating-point cross-check with scipy, if available (not a premise).
try:
    from scipy.optimize import linprog
    def lp(cons):
        A=[[float(x),float(y)] for x,y,_ in cons]; r=[float(z) for *_,z in cons]
        res=linprog(c=[0,-1],A_ub=A,b_ub=r,bounds=[(0,1),(0,1)],method='highs')
        assert res.success; return -res.fun
    for name,cons in cases.items():
        assert abs(lp(cons)-float(Q(out[name]['sup_b'])))<1e-9, name
    print('scipy cross-check: passed', file=sys.stderr)
except ImportError:
    print('scipy cross-check: skipped (scipy not installed)', file=sys.stderr)

out['_theta_family_sup_c']=theta_table
json.dump(out, sys.stdout, indent=2); print()
