"""Exact checks for "Beatty band rules leave a slow block constant".

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass,
last line "Test passé : all checks pass"; the JSON summary it prints must equal
RESULT.json; --write regenerates RESULT.json).  All randomness is seeded.

  1. Lemma 1: on the r = 0 family, n_j = q^(D-1) e (t + j), the band
     floor(sum_i (q y~_i(n_j))^2) equals d^2 (t + j)^2, d = lam e, computed
     from the coordinates of the source with exact fractions.
  2. Lemma 2 (straddle count), inside its regime Delta* <= 1: for random
     Beatty rules and steps, the number of starts t whose block is not
     constant never exceeds 2 M_A (L + 2)(3k + 2), L the sweep of the phase.
  3. Theorem 5 inside its regime (q = 2^61 - 1, k = 6, |I_D| = H = 1/k^2):
     for witness steps e (found by --search), every hypothesis is rechecked
     exactly, the mixed aligned starts are counted over all of T(d) and stay
     below the Lemma 2 bound, and more than 2k starts give constant blocks.
  4. Control: the same rules on blocks whose start s is not a multiple of d
     are mostly mixed; the choice s = d t is what freezes the phase.
  5. Lemma 4 (quadratic Dirichlet with a linear target) by exhaustive search
     at E = 3 * 10^5, kappa E = 1/30 (outside the proven regime: it tests
     the conclusion), over adversarial alpha (small and huge
     denominators, near-rationals, quadratic irrationals, random).  Control:
     at E = 12 some alpha has no such e, so the size hypothesis is not idle.
"""
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('ÉCHEC :', msg)


def frac(x):
    return x - math.floor(x)


def centred(x):
    """Representative of x mod 1 in [-1/2, 1/2)."""
    y = frac(x)
    return y - 1 if y >= Fraction(1, 2) else y


def dist_int(x):
    """Signed distance from x to the nearest integer, in [-1/2, 1/2)."""
    return centred(x)


class Rule:
    """Y = {t : frac(alpha t + beta) in A}, A a union of half-open arcs."""

    def __init__(self, alpha, beta, arcs):
        self.alpha, self.beta, self.arcs = alpha, beta, arcs
        self.ends = sorted({a for a, _ in arcs} | {b for _, b in arcs})

    def __contains__(self, t):
        x = frac(self.alpha * t + self.beta)
        return any(a <= x < b for a, b in self.arcs)

    @property
    def M(self):
        return len(self.arcs)


def random_arcs(rng, M, den=10**6):
    pts = sorted(rng.sample(range(1, den), 2 * M))
    return [(Fraction(pts[2 * i], den), Fraction(pts[2 * i + 1], den)) for i in range(M)]


def block_constant(rule, d, t, k):
    s = {(d * (t + j)) ** 2 in rule for j in range(k)}
    return len(s) == 1, s


# ------------------------------------------------------------------ 1. Lemma 1
def band_from_coordinates(n, q, D, lam):
    tot = Fraction(0)
    for i in range(1, D + 1):
        y = Fraction(lam * n % q**i, q**i)
        tot += (q * centred(y)) ** 2
    return math.floor(tot)


rng = random.Random(20261027)
n1 = 0
for q, D in ((10007, 3), (1009, 4), (65537, 2)):
    for _ in range(60):
        lam = rng.randrange(30, 400)
        while math.gcd(lam, q) != 1:
            lam += 1
        k = rng.randrange(3, 9)
        e = rng.randrange(1, 40)
        d = lam * e
        t = rng.randrange(1, max(2, q // (2 * d) - k))
        if d * (t + k - 1) >= q // 2:
            continue
        for j in range(k):
            n = q ** (D - 1) * e * (t + j)
            check(band_from_coordinates(n, q, D, lam) == (d * (t + j)) ** 2,
                  f'Lemma 1 fails at q={q} D={D} lam={lam} e={e} t={t} j={j}')
            n1 += 1
OUT['lemma1_positions'] = n1
print(f'1. Lemma 1: {n1} positions, band = d^2 (t+j)^2 exactly')


# ------------------------------------------------------------------ 2. Lemma 2
def straddle_stats(rule, d, k, tmin, tmax):
    eta = abs(dist_int(rule.alpha * d * d))
    L = eta * (tmax * tmax - tmin * tmin)
    bound = 2 * rule.M * (L + 2) * (3 * k + 2)
    mixed = sum(1 for t in range(tmin, tmax + 1) if not block_constant(rule, d, t, k)[0])
    return mixed, bound, eta


# In the regime of the lemma: alpha is built so that eta = ||alpha d^2|| is at most
# 1/((k-1)(2 t_max + k - 1)), i.e. Delta* <= 1.
rng = random.Random(7)
worst = Fraction(0)
n2 = informative = 0
for _ in range(150):
    k = rng.randrange(3, 9)
    M = rng.randrange(1, 5)
    d = rng.randrange(1, 60)
    tmin = rng.randrange(k * k, 30 * k * k)
    tmax = 3 * tmin
    cap = Fraction(1, (k - 1) * (2 * tmax + k - 1))
    eta = cap * Fraction(rng.randrange(1, 10**6), 10**6) * rng.choice((1, -1))
    alpha = (rng.randrange(10**6) + eta) / (d * d)
    rule = Rule(alpha, Fraction(rng.randrange(10**6), 10**6), random_arcs(rng, M))
    mixed, bound, eta_c = straddle_stats(rule, d, k, tmin, tmax)
    check(eta_c * (k - 1) * (2 * tmax + k - 1) <= 1, 'Lemma 2 case outside Delta* <= 1')
    check(mixed <= bound, f'Lemma 2 bound exceeded: {mixed} > {bound}')
    informative += bound < tmax - tmin + 1
    worst = max(worst, Fraction(mixed) / bound)
    n2 += 1
check(informative > 0, 'Lemma 2: no case where the bound is below the number of starts')
OUT['lemma2'] = {'cases_with_Delta_le_1': n2, 'bound_below_number_of_starts': informative,
                 'max_ratio_mixed_over_bound': str(round(float(worst), 4))}
print(f'2. Lemma 2: {n2} cases with Delta* <= 1, bound < #starts in {informative}, '
      f'max mixed/bound = {float(worst):.4f}')


# ------------------------------------------------------------------ 3. Theorem 5
# In the regime of the theorem: k = 6, and I_D = [1/8, 1/8 + H) a genuine V interval of
# length H = 1/k^2.  The steps e were found once by sampling (python3 verify.py --search,
# under borne.py); here every hypothesis is rechecked on them exactly.
Q61 = 2**61 - 1
LAM = 31
K3 = 6
YLO, LV = Fraction(1, 8), Fraction(1, K3 * K3)


def golden(den_digits):
    """A convergent of the golden ratio with a denominator of about 10^den_digits."""
    a, b = 1, 1
    while b < 10**den_digits:
        a, b = a + b, a
    return Fraction(a, b)


def t_range(d):
    tmin = math.ceil(Q61 * YLO / d)
    tmax = math.ceil(Q61 * (YLO + LV) / d) - 1 - (K3 - 1)
    return tmin, tmax


def admissible(rule, e):
    d = LAM * e
    tmin, tmax = t_range(d)
    eta = abs(dist_int(rule.alpha * d * d))
    return (eta <= Fraction(d, 10 * rule.M * K3 * Q61)
            and d <= Q61 * LV / (64 * rule.M * K3)
            and tmin >= K3 * K3 and tmax <= 3 * tmin
            and eta * (K3 - 1) * (2 * tmax + K3 - 1) <= 1)


def search_e(rule, rng, samples=30_000_000):
    E = int(Q61 * LV / (64 * rule.M * K3) // LAM)
    a = rule.alpha * LAM * LAM
    num, den = a.numerator, a.denominator
    scales = [(E // 2, E, samples)] + [(E >> (i + 1), E >> i, 20000) for i in range(1, 46)]
    for lo, hi, n in scales:
        if hi <= lo:
            continue
        for _ in range(n):
            e = lo + 1 + rng.randrange(hi - lo)
            r = num * e * e % den
            if Fraction(min(r, den - r), den) <= Fraction(LAM * e, 10 * rule.M * K3 * Q61):
                return e
    return None


rng = random.Random(61)
rules = {
    'golden_10^40': Rule(golden(40), Fraction(1, 3), [(Fraction(1, 10), Fraction(3, 10))]),
    'sqrt2_like': Rule(Fraction(math.isqrt(2 * 10**80), 10**40), Fraction(0),
                       [(Fraction(0), Fraction(1, 7)), (Fraction(1, 2), Fraction(5, 9))]),
    'random_3_arcs': Rule(Fraction(rng.randrange(10**50), 10**50 + 7), Fraction(2, 5),
                          random_arcs(rng, 3)),
    'rational_1/2': Rule(Fraction(1, 2), Fraction(0), [(Fraction(0), Fraction(1, 2))]),
    'near_rational_1/7': Rule(Fraction(1, 7) + Fraction(1, 10**30), Fraction(1, 11),
                              [(Fraction(0), Fraction(3, 7))]),
    # b mod M in R with M of the order of the band range (bands are about q^2/64 to
    # 9q^2/64), far above the moduli of N2b and P2: a sparse residue rule
    'residue_mod_q^2/500_R=3': Rule(Fraction(1, Q61 * (Q61 // 500) + 7), Fraction(0),
                                    [(Fraction(r, Q61 * (Q61 // 500) + 7),
                                      Fraction(r + 1, Q61 * (Q61 // 500) + 7))
                                     for r in (11, 10**30, 3 * 10**33)]),
    # the dense version: b mod M in [0, M/2), density 1/2, one arc
    'residue_mod_q^2/500_half': Rule(Fraction(1, Q61 * (Q61 // 500) + 7), Fraction(0),
                                     [(Fraction(0), Fraction(1, 2))]),
}
WITNESS_E = {                           # journal of the search: T1/journal/search.log
    'golden_10^40': 3072079371732, 'sqrt2_like': 2494809876279,
    'random_3_arcs': 1293609055353, 'rational_1/2': 4230782861208,
    'near_rational_1/7': 170107826, 'residue_mod_q^2/500_R=3': 472541515656,
    'residue_mod_q^2/500_half': 1684480363615,
}

if '--search' in sys.argv:
    for name, rule in rules.items():
        print(name, search_e(rule, random.Random(len(name))), flush=True)
    sys.exit(0)

res3 = {}
for name, rule in rules.items():
    e = WITNESS_E.get(name)
    check(e is not None and admissible(rule, e), f'Theorem 5: no admissible witness e for {name}')
    if e is None:
        continue
    d = LAM * e
    tmin, tmax = t_range(d)
    # Lemma 2 holds on any sub-range with tmax <= 3 tmin; a small e (major arc) has
    # millions of starts, so count on the first 50 000 of them
    tmax = min(tmax, tmin + 49999)
    mixed, bound, _ = straddle_stats(rule, d, K3, tmin, tmax)
    n_t = tmax - tmin + 1
    check(mixed <= bound, f'Theorem 5: mixed aligned starts exceed the Lemma 2 bound for {name}')
    check(n_t - mixed > 2 * K3, f'Theorem 5: fewer than 2k+1 constant blocks for {name}')
    first = next(t for t in range(tmin, tmax + 1) if block_constant(rule, d, t, K3)[0])
    res3[name] = {'e': e, 'starts': n_t, 'mixed': mixed, 'lemma2_bound': str(round(float(bound))),
                  'first_constant_t': first,
                  'first_constant_in_Y': block_constant(rule, d, first, K3)[1].pop()}
OUT['theorem5'] = res3
check({r['first_constant_in_Y'] for r in res3.values()} == {True, False},
      'Theorem 5: the first constant blocks do not show both outcomes')
print(f'3. Theorem 5 at q = 2^61-1, k = 6, |I_D| = H: {res3}')


# ------------------------------------------------------------------ 4. control
rng = random.Random(4)
res4 = {}
for name, rule in rules.items():
    e = res3.get(name, {}).get('e')
    if e is None:
        continue
    d = LAM * e
    mixed = tot = 0
    for _ in range(400):
        s = rng.randrange(Q61 // 8, 3 * Q61 // 8 - K3 * d)
        if s % d == 0:
            continue
        vals = {(s + j * d) ** 2 in rule for j in range(K3)}
        mixed += len(vals) == 2
        tot += 1
    res4[name] = f'{mixed}/{tot}'
# a rule that is a band residue of small modulus with d divisible by it is constant on
# every block, aligned or not: it is the only expected exception
generic = [v for n, v in res4.items() if n in ('golden_10^40', 'sqrt2_like', 'random_3_arcs')]
check(all(int(v.split('/')[0]) * 4 > int(v.split('/')[1]) for v in generic),
      'control 4: unaligned blocks are not mostly mixed for a generic rule')
OUT['control_unaligned_mixed'] = res4
print(f'4. Control, unaligned starts (mixed/total): {res4}')


# ------------------------------------------------------------------ 5. Lemma 4
def lemma4_min_e(alpha, kappa, E):
    num, den = alpha.numerator, alpha.denominator
    for e in range(1, E + 1):
        r = num * e * e % den
        if Fraction(min(r, den - r), den) <= kappa * e:
            return e
    return None


E5 = 300000
kap = Fraction(1, 30 * E5)
rng = random.Random(5)
alphas = {
    'golden': golden(30),
    'sqrt3_like': Fraction(math.isqrt(3 * 10**60), 10**30),
    '1/2': Fraction(1, 2), '1/3': Fraction(1, 3), '5/97': Fraction(5, 97),
    '1/(E^2+1)': Fraction(1, E5**2 + 1), '1/E^3': Fraction(1, E5**3),
    '1/2+1/(3E^2)': Fraction(1, 2) + Fraction(1, 3 * E5**2),
    '3/7+1/(5E)': Fraction(3, 7) + Fraction(1, 5 * E5),
    'random_1': Fraction(rng.randrange(10**40), 10**40 + 3),
    'random_2': Fraction(rng.randrange(10**40), 10**40 + 9),
}
res5 = {}
for name, a in alphas.items():
    e = lemma4_min_e(a, kap, E5)
    check(e is not None, f'Lemma 4: no e for {name}')
    res5[name] = e
OUT['lemma4_min_e'] = res5
print(f'5. Lemma 4 at E = {E5}, kappa E = 1/30: least e = {res5}')

# control: tiny E, the conclusion fails for some alpha
E0, kap0 = 12, Fraction(1, 30 * 12)
bad = None
for i in range(1, 4000):
    a = Fraction(i, 4001)
    if lemma4_min_e(a, kap0, E0) is None:
        bad = str(a)
        break
check(bad is not None, 'control 5: no alpha fails at E = 12')
OUT['lemma4_control_fails_at_E12'] = bad
print(f'   control: at E = 12, alpha = {bad} has no e')

# ------------------------------------------------------------------ summary
OUT['fails'] = len(FAIL)
print(json.dumps(OUT, sort_keys=True))
here = Path(__file__).parent
res = here / 'RESULT.json'
if '--write' in sys.argv and FAIL:
    print(f'Test échoué : {len(FAIL)} checks failed, RESULT.json not written')
    sys.exit(1)
if '--write' in sys.argv:
    res.write_text(json.dumps(OUT, sort_keys=True, indent=1) + '\n')
elif res.exists():
    check(json.loads(res.read_text()) == OUT, 'summary differs from RESULT.json')
man = here / 'MANIFEST.json'
if man.exists() and '--write' not in sys.argv:
    import hashlib
    m = json.loads(man.read_text())
    listed = sorted(f.name for f in here.iterdir() if f.is_file() and f.name != 'MANIFEST.json')
    check(sorted(m) == listed, 'MANIFEST does not list exactly the package files')
    for name, h in m.items():
        check(hashlib.sha256((here / name).read_bytes()).hexdigest() == h, 'MANIFEST hash ' + name)
if FAIL:
    print(f'Test échoué : {len(FAIL)} checks failed')
    sys.exit(1)
print('Test passé : all checks pass')
