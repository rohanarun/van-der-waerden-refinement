"""Exact checks for the model-derived parameter region and obstruction identity.

These checks verify the stated algebra. They do not formally verify the
upstream probability/geometric lemmas or establish literature priority.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parent
config=json.loads((ROOT/'parameters.json').read_text())
checks=[]
def margins(p):
    a,m,b,d,g,c=(Q(p[k]) for k in ('a','m','b','delta','gamma','c'))
    return {
        'dimension_grows':a,
        'period_less_than_heavy_cutoff':m-2*a,
        'global_entropy_less_than_M':m-3*a,
        'M_sublinear':1-m,
        'flip_probability_decays':b,
        'affine_global_entropy_gap':1-b-3*a,
        'affine_norm_entropy_gap':a-b,
        'light_color_margin':d/4-g,
        'long_block_color_margin':(1-d)/8-g,
        'rich_union_bound_gap':g*b/2-2*c,
        'drift_less_than_eta_gap':3-m-a,
    }
def valid(p):
    ms=margins(p)
    return all(v>=0 if k=='light_color_margin' else v>0 for k,v in ms.items())
for p in config['proposals']:
    assert valid(p),p
    checks.append({'name':p['name'],'factor_over_release':str(Q(p['c'])/Q(config['baseline_c'])),'margins':{k:str(v) for k,v in margins(p).items()}})
# Meaningful rejection controls: exact boundary must fail because logarithmic
# factors are not dominated by equal powers; zero rich exponent also fails.
p=dict(config['proposals'][-1]);p['b']=p['a'];assert not valid(p)
p=dict(config['proposals'][-1]);p['c']=str(Q(p['gamma'])*Q(p['b'])/4);assert not valid(p)
p=dict(config['proposals'][-1]);p['m']=str(3*Q(p['a']));assert not valid(p)

# Independent finite tests of the exact half-open norm-band lemma. The proof
# is analytic; these tests include unit-distance equality and t=0 cases.
points=[Q(i,4) for i in range(-20,21)];band_cases=0
for ts in combinations(points,3):
    if min(ts[i+1]-ts[i] for i in range(2))<1:continue
    for shift in (Q(0),Q(1,4),Q(1,2),Q(3,4)):
        bands=[(t*t+shift).__floor__() for t in ts]
        assert len(set(bands))>1
        band_cases+=1

# Symbolic proof identities for the matrix-profile obstruction.
r,x,A=s.symbols('r x A',positive=True)
assert s.expand((r-1)**3*(r+1))==s.expand(r**4-2*r**3+2*r-1)
f=(x/2)**s.Rational(1,3)*(2*A+x)/6
assert s.simplify(9*s.diff(f,x,2)-2**s.Rational(2,3)*(x-A)/(3*x**s.Rational(5,3)))==0
# Exact cube comparison avoids numerical cube roots for tripling.
def profile_cube(a,b):
    a,b=sorted((a,b));return Q(3*a-1,2)*Q(2*b+a-1,2)**3
tripling_cases=0
for a in range(1,101):
    assert profile_cube(1,a)==a**3
    assert profile_cube(a,a)==Q(3*a-1,2)**4
    for h in range(1,101):
        assert profile_cube(a,3*h+a-1)>=27*profile_cube(a,h)
        assert profile_cube(a,h)<=Q(a+h-1)**4
        tripling_cases+=1

out={'scope':'Exact algebra and finite checks only; not an independent formal proof of upstream results',
     'parameter_certificates':checks,'negative_controls_rejected':3,
     'half_open_band_test_cases':band_cases,'profile_exact_test_cases':tripling_cases,
     'symbolic_identities':'passed'}
(ROOT/'experiments'/'exact-audit.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
