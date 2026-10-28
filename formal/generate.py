"""Translate pinned source data to explicit Lean propositions, never proof verdicts.

Python handles source association. Lean checks every emitted proposition.
Run with --check in CI to reject stale generated files.
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def verify_sources(root=ROOT):
    manifest = json.loads((root / 'SOURCES.json').read_text())
    for row in manifest['files']:
        data = (root / row['snapshot']).read_bytes()
        if hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError(f"Source mismatch: {row['snapshot']}")
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if blob != row['git_blob']:
            raise ValueError(f"Git blob mismatch: {row['snapshot']}")


def rat(x):
    q = Q(x)
    return f'({q.numerator}/{q.denominator} : ℚ)'


def load(pr, path):
    return json.loads((ROOT / 'sources' / f'pr{pr}' / path).read_text())


REGIONS = '''import Vdw.Bounds
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
'''


def parameters():
    out = [REGIONS]
    def emit(name, region, p, keys, extra=''):
        args = ' '.join(rat(p[k]) for k in keys)
        out.append(f'theorem {name} : {region} {args} {extra} := by\n'
                   '  norm_num [LegacyRegion, AffineRegion, RunRegion, OuterRegion]\n')
    base = ('a','m','b','delta','gamma','c')
    outer = ('a','m','b','delta','eps','eps_reg','gamma','c')
    for i,p in enumerate(load(1,'parameters.json')['proposals']):
        emit(f'pr1_parameters_{i}', 'LegacyRegion', p, base)
    for i,p in enumerate(load(2,'parameters.json')['sharpened_proposals']):
        emit(f'pr2_parameters_{i}', 'AffineRegion', p, outer, rat(4))
    text = (ROOT/'sources/pr4/repeated-key-certificate-proof.md').read_text()
    block = text.split('### An explicit choice')[1].split('The margins are:')[0]
    p4 = {}
    for key in ('a','m','b','gamma','tau','c'):
        token = ('\\'+key) if key in ('gamma','tau') else key
        match = re.search(re.escape(token)+r'=\\frac(?:\{(\d+)\}|(\d))(?:\{(\d+)\}|(\d))', block)
        if not match: raise ValueError(f'PR4 parameter not found: {key}')
        p4[key] = str(Q(int(match[1] or match[2]),int(match[3] or match[4])))
    balance = re.search(r'\\varepsilon=\\varepsilon_\{\\rm reg\}=\\delta=\\frac(?:\{(\d+)\}|(\d))(?:\{(\d+)\}|(\d))',block)
    if not balance: raise ValueError('PR4 balance parameters not found')
    for key in ('delta','eps','eps_reg'):
        p4[key]=str(Q(int(balance[1] or balance[2]),int(balance[3] or balance[4])))
    emit('pr4_parameters', 'AffineRegion', p4, outer, rat(3))
    out.append(f'theorem pr4_tau : {rat(p4["tau"])}={rat(p4["gamma"])}/3 := by norm_num\n')
    for pr, group, cost in [(6,'rank_certificate_proposals',Q(5,2)),(7,'digit_rank_proposals',Q(2))]:
        for i,p in enumerate(load(pr,'parameters.json')[group]):
            emit(f'pr{pr}_{group}_{i}', 'AffineRegion',p,outer,rat(cost))
    for i,p in enumerate(load(7,'parameters.json')['short_period_proposals']):
        emit(f'pr7_run_parameters_{i}','RunRegion',p,outer,rat(p['delta_s']))
    for name,cert in load(9,'effective-completion/THRESHOLDS.json')['literal_certificates'].items():
        p=cert['parameters']
        emit('pr9_'+name, 'RunRegion' if name.endswith('7') else 'AffineRegion',p,outer,
             rat(p['delta_s']) if name.endswith('7') else rat(Q(5,2)))
    out.append('end Vdw\n')
    return '\n'.join(out)


def thresholds():
    out=['''import Vdw.Bounds
namespace Vdw
-- Kernel-checked dyadic comparisons; this does not prove analytic monotonicity.
theorem dyadic_from_small {A u : ℚ} {t j n w : ℕ}
    (hu : 0≤u) (hw : w≤n) (hs : A*(t : ℚ)^j ≤ u*2^w) :
    A*(t : ℚ)^j ≤ u*2^n := by
  exact le_trans hs (mul_le_mul_of_nonneg_left
    (pow_le_pow_right₀ (by norm_num : (1 : ℚ)≤2) hw) hu)
''']
    for name,cert in load(9,'effective-completion/THRESHOLDS.json')['literal_certificates'].items():
        t=cert['t']
        for i,row in enumerate(cert['checks']):
            stem=f'pr9_{name}_check_{i}'
            out.append('-- '+row['name'])
            if 'lhs' in row:
                out.append(f'theorem {stem} : {rat(row["lhs"])} ≤ {rat(row["rhs"])} := by norm_num\n')
                continue
            A,d,u=map(Q,(row['A'],row['decay'],row['target']))
            j,n=row['log_degree'],row['floor_decay_t']
            # A small power sufficient to bound the rational lhs. The kernel
            # also checks w<=n, avoiding construction of millions of bits.
            ratio=A*t**j/u
            w=max(0,ratio.numerator.bit_length()-ratio.denominator.bit_length()+1)
            out.append(f'''theorem {stem} :
    0<{rat(d)} ∧ 0<{rat(u)} ∧ 0≤{rat(A)} ∧
    ({t} : ℚ)/2 ≥ ({j} : ℚ)/{rat(d)} ∧
    ({n} : ℚ) ≤ {rat(d)}*{t} ∧ {rat(d)}*{t} < {n}+1 ∧
    {rat(A)}*({t} : ℚ)^{j} ≤ {rat(u)}*2^{n} := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, ?_⟩
  apply dyadic_from_small (w := {w}) <;> norm_num
''')
    out.append('end Vdw\n')
    return '\n'.join(out)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true')
    args=parser.parse_args();verify_sources()
    for name,content in [('Parameters.lean',parameters()),('Thresholds.lean',thresholds())]:
        path=ROOT/'Vdw'/name
        if args.check:
            if path.read_text()!=content: raise ValueError(f'Stale generated file: {path}')
        else: path.write_text(content)
    print('Pinned source hashes and Lean data translation: passed')


if __name__=='__main__': main()
