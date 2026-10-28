"""Checks for 'Lean: a key occurs at most twice on a progression (Lemma 3)'.

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass;
the JSON summary must equal RESULT.json; --write regenerates it, and writes
nothing when a check fails).

Only `lake build` proves anything.  This script does not run Lean: it checks
that the recorded evidence belongs to the sources in the package, and replays a
hand transcription of the definitions on small cases, with mutants.  To rebuild
and re-record the evidence: lean/record-evidence.sh.

  1. evidence/sources.sha256 matches every Lean source in the package (a
     declaration: recomputed by hand it passes, so it catches a stale record,
     not a forged one).  Then a lint, not a proof: no sorry, admit, axiom
     declaration, native_decide, implemented_by, extern or set_option outside
     comments; Lean 4.21.0 and Mathlib v4.21.0 pinned.
  2. evidence/axioms.txt (#print axioms on every constant whose name starts
     with KeyMultiplicity): the announced count, only propext,
     Classical.choice and Quot.sound, and the named statements present.
     Private or _root_ declarations would escape this prefix filter (there
     are none); #print axioms on lemma3 and hm_bridge is transitive and
     covers everything they use.
  3. evidence/build.txt records a build of KeyMultiplicity.
  4. A hand transcription of yt, f, key, lam (exact rationals) and meshV
     (decimal, 80 digits, every floor, ceiling and interval comparison
     certified by a margin of 1e-40; the one exact contact, s = 0 at the end
     a_m = 1/2, is set exactly), replayed in the regime of `lemma3` (P prime,
     e >= 1, 2 <= k < P, h0 < P).  meshV agrees with a direct search of the
     source's intervals.  No key occurs three times and there are at least
     ceil(k/2) distinct keys: on every progression of the exhaustive toys,
     where q < k² puts every term in its own box, so the check is met
     trivially there; on sampled progressions of larger toys; and on random
     short steps with q > k², where the bound is exercised (a key twice, and
     three terms in one box that only the band separates).  A witness built
     by hand also has a key twice.  The mesh (alpha, m) of each toy is
     recorded.  It tests the transcription, not the Lean terms, which are
     noncomputable.
  5. Mutants: each must make some key occur three times or more on a
     progression of the toys.  M1 drops the band from the key; M2 drops the
     box; M3 drops k < P (a step of small order folds the progression); M4
     drops gcd(lambda, P) = 1 (lambda = P).  Then a measurement, not a
     check: meshes coarser than the source's (k R, R, R/4 instead of k² R).
"""
import hashlib
import json
import math
import random
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE / 'lean'
OUT = {}
FAIL = []


def check(ok, msg):
    if not ok:
        FAIL.append(msg)
        print('FAIL:', msg)


# 1. Sources: the recorded fingerprints must match them (a declaration, not a proof)
recorded = {}
for line in (LEAN / 'evidence' / 'sources.sha256').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    recorded[name] = digest
LEAN_FILES = ['KeyMultiplicity.lean', 'KeyMultiplicity/Basic.lean', 'Axioms.lean',
              'lakefile.toml', 'lean-toolchain', 'lake-manifest.json']
check(sorted(recorded) == sorted(LEAN_FILES), 'sources.sha256 lists other files')
for name in LEAN_FILES:
    check(hashlib.sha256((LEAN / name).read_bytes()).hexdigest() == recorded.get(name),
          f'{name} differs from the sources that produced evidence/: rerun record-evidence.sh')
check('"name": "key_multiplicity"' in (LEAN / 'lake-manifest.json').read_text(), 'manifest name')
SOURCES = ['KeyMultiplicity.lean', 'KeyMultiplicity/Basic.lean', 'Axioms.lean']
FORBIDDEN = ['sorry', 'admit', 'native_decide', 'implemented_by', 'extern', 'set_option']
for name in SOURCES:
    text = (LEAN / name).read_text()
    code = re.sub(r'/-.*?-/', '', text, flags=re.S)
    code = re.sub(r'--[^\n]*', '', code)
    for w in FORBIDDEN:
        check(re.search(r'\b' + w + r'\b', code) is None, f'{name} contains {w}')
    check(re.search(r'^\s*axiom\b', code, flags=re.M) is None, f'{name} declares an axiom')
check((LEAN / 'lean-toolchain').read_text().strip() == 'leanprover/lean4:v4.21.0', 'toolchain')
check('rev = "v4.21.0"' in (LEAN / 'lakefile.toml').read_text(), 'mathlib pin')
print(f'1. sources: evidence recorded from these {len(LEAN_FILES)} files; lint clean '
      '(no sorry/admit/axiom/native_decide/implemented_by/extern/set_option)')

# 2. Axioms
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}
lines = (LEAN / 'evidence' / 'axioms.txt').read_text()
announced = int(re.match(r'(\d+) constants', lines).group(1))
entries = re.findall(r"'([^']+)' (depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",
                     lines)
check(len(entries) == announced, 'axioms.txt count')
used = set()
for name, _, axs in entries:
    check(name.startswith('KeyMultiplicity.'), f'foreign constant {name}')
    ax = {a.strip() for a in axs.replace('\n', ' ').split(',') if a.strip()}
    check(ax <= STANDARD, f'{name} uses {ax - STANDARD}')
    used |= ax
MAIN = ['meshA_le_iff', 'lt_meshA_iff', 'meshA_lt_iff', 'le_meshA_iff', 'meshV_spec',
        'meshA_le_half', 'meshA_nonneg', 'meshV_of_mem', 'meshA_gap', 'meshV_width', 'yt_mem', 'val_add_mul', 'yt_affine', 'separation',
        'terms_ne', 'three_affine', 'three_point_left', 'three_point_right', 'no_three',
        'mult_le_two', 'distinct_keys', 'lam_coprime', 'lemma3', 'key_range_finite', 'hm_bridge']
names = {n for n, _, _ in entries}
for m in MAIN:
    check('KeyMultiplicity.' + m in names, f'{m} missing from the audit')
OUT['axioms'] = {'constants': announced, 'axioms_used': sorted(used), 'statements': MAIN}
print(f'2. axioms: {announced} constants, axioms used {sorted(used)}')

# 3. Build
build = (LEAN / 'evidence' / 'build.txt').read_text()
check('Built KeyMultiplicity' in build and build.rstrip().endswith('Build completed successfully.'),
      'build.txt')
print('3. build: recorded (the proof is lake build itself, not this record)')

# 4. Hand transcription of KeyMultiplicity/Basic.lean
getcontext().prec = 80
MARGIN = Decimal('1e-40')


def certified_floor(x):
    """floor of a Decimal, refused when x is within MARGIN of an integer."""
    f = math.floor(x)
    check(min(x - f, f + 1 - x) > MARGIN, f'uncertified floor at {x}')
    return f


def yt(q, D, lam, n, i):
    """ỹ_{i+1}(n) = t - round t, t = lam n / q^(i+1), round t = floor(t + 1/2)."""
    t = Fraction(lam * n, q ** (i + 1))
    return t - math.floor(t + Fraction(1, 2))


def lam_of(h0, M):
    out = 1
    for l in range(2, h0 + 1):
        if all(l % p for p in range(2, int(l ** 0.5) + 1)):
            e = 0
            while l ** (e + 1) <= 2 * M:
                e += 1
            out *= l ** e
    return out


class Mesh:
    """meshV with α = q^-(D+1), R = log(1 + 1/(2α)), m = ceil(k² R).

    `scale` replaces k² R by another multiple of R, for the probe of coarser
    meshes only."""

    def __init__(self, q, D, k, scale=None):
        self.alpha = Decimal(1) / Decimal(q) ** (D + 1)
        self.R = (1 + 1 / (2 * self.alpha)).ln()
        self.m = -certified_floor(-((Decimal(k) ** 2 if scale is None else scale) * self.R))
        # a_0 = 0 and a_m = α(e^R - 1) = 1/2 exactly; the decimals would leave
        # rounding noise at the two ends.
        self.a = ([Decimal(0)] + [self.alpha * ((Decimal(l) * self.R / self.m).exp() - 1)
                                  for l in range(1, self.m)] + [Decimal('0.5')])

    def label(self, s):
        # At s = 0 the argument is (m/R) R = m exactly.  Elsewhere the margin
        # certifies (s = -1/2 never occurs: q is odd in every toy).
        if s == 0:
            return (True, self.m - 1)
        s = Decimal(s.numerator) / Decimal(s.denominator)
        if s < 0:
            x = (self.m / self.R) * (1 + (s + Decimal('0.5')) / self.alpha).ln()
            return (False, certified_floor(x))
        x = (self.m / self.R) * (1 + (Decimal('0.5') - s) / self.alpha).ln()
        return (True, -certified_floor(-x) - 1)

    def search(self, s):
        """The source's interval containing s, found directly (02-setup l. 149-156),
        each comparison certified by MARGIN; the only exact contact allowed is
        s = 0 = 1/2 - a_m, the left end of the last right-hand interval."""
        exact0 = s == 0
        s = Decimal(s.numerator) / Decimal(s.denominator)
        half = Decimal('0.5')
        for l in range(self.m):
            if s < 0 and self.a[l] <= s + half < self.a[l + 1]:
                check(min(s + half - self.a[l], self.a[l + 1] - s - half) > MARGIN,
                      f'uncertified interval at {s}')
                return (False, l)
            if s >= 0 and half - self.a[l + 1] <= s < half - self.a[l]:
                lo = s - (half - self.a[l + 1])
                check((exact0 and l == self.m - 1 and lo == 0) or lo > MARGIN,
                      f'uncertified interval at {s}')
                check(half - self.a[l] - s > MARGIN, f'uncertified interval at {s}')
                return (True, l)
        return None


def keys(q, D, lam, mesh, n0, d, k, box=True, band=True):
    N = q ** D
    out = []
    for j in range(k):
        n = (n0 + j * d) % N
        ys = [yt(q, D, lam, n, i) for i in range(D)]
        f = sum((q * y) ** 2 for y in ys)
        out.append((tuple(mesh.label(y) for y in ys) if box else None,
                    math.floor(f) if band else None))
    return out


def max_mult(ks):
    return max(ks.count(x) for x in ks)


def is_prime(p):
    return p > 1 and all(p % r for r in range(2, int(p ** 0.5) + 1))


# (P, e, D, k, h0, M, exhaustive?)  -- the regime of lemma3: 2 <= k < P, h0 < P
TOYS = [(5, 1, 2, 3, 4, 2, True), (5, 1, 2, 4, 3, 3, True), (7, 1, 2, 6, 6, 2, True),
        (5, 1, 3, 4, 4, 2, True), (11, 1, 2, 10, 10, 3, True), (5, 3, 2, 4, 4, 2, False),
        (13, 1, 3, 12, 12, 4, False)]
rng = random.Random(20261027)
progressions = spec_points = 0
meshes = []
for P, e, D, k, h0, M, full in TOYS:
    check(is_prime(P) and e >= 1 and 2 <= k < P and h0 < P, f'toy {P, e, D, k} out of regime')
    q, lam = P ** e, lam_of(h0, M)
    check(math.gcd(lam, P) == 1, 'lam_coprime')
    N = q ** D
    mesh = Mesh(q, D, k)
    meshes.append({'q': q, 'D': D, 'k': k, 'alpha': f'1/{q ** (D + 1)}', 'm': mesh.m})
    for n in range(N) if N <= 2000 else rng.sample(range(N), 2000):
        for i in range(D):
            y = yt(q, D, lam, n, i)
            check(Fraction(-1, 2) <= y < Fraction(1, 2), 'yt_mem')
            check(mesh.label(y) == mesh.search(y), f'meshV_spec at {y}')
            spec_points += 1
    pairs = ([(n0, d) for n0 in range(N) for d in range(1, N)] if full else
             [(rng.randrange(N), rng.randrange(1, N)) for _ in range(4000)])
    for n0, d in pairs:
        ks = keys(q, D, lam, mesh, n0, d, k)
        check(max_mult(ks) <= 2, f'mult_le_two fails at {P, e, D, k, n0, d}')
        check(len(set(ks)) >= (k + 1) // 2, 'distinct_keys')
        progressions += 1
# On the toys above no key occurs twice.  Two terms share a box only if every
# coordinate moves by less than the mesh width (< 1/k²), and the separating
# coordinate moves by a nonzero multiple of 1/q: with q < k² (the five
# exhaustive toys) every box holds one term, and a uniform step is short in
# every coordinate with probability about (7/q)^D.  So the bound is exercised
# on short steps: lam d = sum_i c_i q^i mod q^D with each c_i in [-3, 3], drawn
# at random with a random n0, in the regime of lemma3 with q > k².
SHORT = [(5, 3, 2, 4, 4, 2), (5, 4, 2, 4, 4, 2), (5, 3, 3, 4, 4, 2)]
short = []
for P, e, D, k, h0, M in SHORT:
    q, lam = P ** e, lam_of(h0, M)
    check(is_prime(P) and 2 <= k < P and h0 < P and q > k * k, 'short toy out of regime')
    N = q ** D
    mesh = Mesh(q, D, k)
    meshes.append({'q': q, 'D': D, 'k': k, 'alpha': f'1/{q ** (D + 1)}', 'm': mesh.m})
    inv = pow(lam, -1, N)
    twice = box3 = drawn = 0
    fewest = k
    while drawn < 3000:
        c = sum(rng.randint(-3, 3) * q ** i for i in range(D)) % N
        if c == 0:
            continue
        n0, d = rng.randrange(N), inv * c % N
        ks = keys(q, D, lam, mesh, n0, d, k)
        check(max_mult(ks) <= 2, f'mult_le_two fails at {P, e, D, k, n0, d}')
        check(len(set(ks)) >= (k + 1) // 2, 'distinct_keys')
        twice += max_mult(ks) == 2
        fewest = min(fewest, len(set(ks)))
        box3 += max_mult(keys(q, D, lam, mesh, n0, d, k, band=False)) >= 3
        drawn += 1
    check(twice > 0 and box3 > 0, f'short steps on {P, e, D, k} do not exercise the bound')
    short.append({'P': P, 'e': e, 'D': D, 'k': k, 'drawn': drawn, 'a_key_twice': twice,
                  'three_or_more_in_one_box': box3,
                  'fewest_distinct_keys': fewest})
    progressions += drawn
# A witness built by hand, in D = 3: q = 125, d = 125 t with lam t = q² - q + 1
# mod q², so y_2 moves by +1/q and y_3 by -1/q + 1/q².
q, lam = 125, lam_of(4, 2)
mesh = Mesh(q, 3, 4)
d = q * ((q * q - q + 1) * pow(lam, -1, q * q) % (q * q))
witness = None
for n0 in range(0, q ** 3, 7):
    ks = keys(q, 3, lam, mesh, n0, d, 4)
    check(max_mult(ks) <= 2, 'mult_le_two at the witness search')
    if max_mult(ks) == 2:
        twice_at = [j for j in range(4) if ks.count(ks[j]) == 2]
        witness = {'P': 5, 'e': 3, 'D': 3, 'k': 4, 'n0': n0, 'd': d, 'positions': twice_at}
        break
check(witness is not None, 'multiplicity two never attained')
OUT['transcription'] = {'toys': [list(t[:6]) for t in TOYS], 'meshes': meshes,
                        'progressions': progressions, 'mesh_points': spec_points,
                        'short_steps': short, 'key_twice_by_hand': witness}
print(f'4. transcription: {progressions} progressions, no key three times, >= ceil(k/2) keys; '
      f'meshV = direct search on {spec_points} points; short steps: '
      + '; '.join(f"q={x['P'] ** x['e']}, D={x['D']}: a key twice on {x['a_key_twice']}, "
                  f"three in a box on {x['three_or_more_in_one_box']}" for x in short)
      + f'; by hand {witness}')


# 5. Mutants: each must fall
def first_triple(q, D, lam, k, n0d, **kw):
    mesh = Mesh(q, D, k)
    for n0, d in n0d:
        if max_mult(keys(q, D, lam, mesh, n0, d, k, **kw)) >= 3:
            return [n0, d]
    return None


mutants = {}
# M1: no band.  P = 5, q = 125, D = 2, d = 125 t with lam t = 1 mod 125: the
# first coordinate stays at 0 and the second moves by 1/125, finer than the
# mesh near zero (width about 1/32 there), while the band reads j².
lam = lam_of(4, 2)
mutants['M1_no_band'] = first_triple(125, 2, lam, 4, [(0, 125 * pow(lam, -1, 125))], band=False)
# M2: no box: the key is the band alone.
mutants['M2_no_box'] = first_triple(5, 2, lam, 4, [(n0, d) for n0 in range(25)
                                                   for d in range(1, 25)], box=False)
# M3: no k < P.  P = 5, k = 11, d = 5 has order 5 in Z/25: terms j, j+5, j+10 coincide.
mutants['M3_k_ge_P'] = first_triple(5, 2, lam, 11, [(0, 5)])
# M4: no gcd(lambda, P) = 1: lambda = 5 collapses the first coordinate.
mutants['M4_lambda_P'] = first_triple(5, 2, 5, 4, [(n0, d) for n0 in range(25)
                                                   for d in range(1, 25)])
for name, wit in mutants.items():
    check(wit is not None, f'mutant {name} survives')
OUT['mutants'] = mutants
print('5. mutants: ' + ', '.join(f'{n} falls at (n0, d) = {w}' for n, w in mutants.items()))

# A measurement, not a check: coarser meshes (m = ceil(s R) for s = k, 1, 1/4
# instead of k²) on short steps of q = 625, D = 2, k = 4.  The proof uses
# k w < 1; these counts say whether the conclusion survives without it.
q, lam, k = 625, lam_of(4, 2), 4
inv = pow(lam, -1, q * q)
steps = []
while len(steps) < 1000:
    c = (rng.randint(-3, 3) + rng.randint(-3, 3) * q) % (q * q)
    if c:
        steps.append((rng.randrange(q * q), inv * c % (q * q)))
coarse = {}
for name, scale in [('k', Decimal(k)), ('1', Decimal(1)), ('1/4', Decimal('0.25'))]:
    mesh = Mesh(q, 2, k, scale)
    coarse[f'm = ceil({name} R) = {mesh.m}'] = sum(
        max_mult(keys(q, 2, lam, mesh, n0, d, k)) >= 3 for n0, d in steps)
OUT['coarser_meshes_three_times'] = coarse
print(f'   coarser meshes, progressions with a key three times out of 1000: {coarse}')

# 6. MANIFEST.json: every listed file has its recorded sha256.  RESULT.json
# is checked after --write, which records its new hash.
manifest = json.loads((HERE / 'MANIFEST.json').read_text())
for name, h in sorted(manifest.items()):
    if name != 'RESULT.json':
        f = HERE / name
        check(f.exists() and hashlib.sha256(f.read_bytes()).hexdigest() == h, f'MANIFEST: {name}')

if '--write' in sys.argv:
    if FAIL:
        print(f'{len(FAIL)} failure(s): RESULT.json not written')
        sys.exit(1)
    (HERE / 'RESULT.json').write_text(json.dumps(OUT, indent=2, ensure_ascii=False) + '\n')
    manifest['RESULT.json'] = hashlib.sha256((HERE / 'RESULT.json').read_bytes()).hexdigest()
    (HERE / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
check(json.loads((HERE / 'RESULT.json').read_text()) == OUT, 'RESULT.json differs')
check(hashlib.sha256((HERE / 'RESULT.json').read_bytes()).hexdigest() == manifest.get('RESULT.json'),
      'MANIFEST: RESULT.json')
print('6. MANIFEST.json: every listed file matches its recorded sha256')
if FAIL:
    print(f'{len(FAIL)} failure(s)')
    sys.exit(1)
print('Test passé')
