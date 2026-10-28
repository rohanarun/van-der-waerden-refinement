"""Checks for 'Door 1 is a van der Waerden problem on key-measurable colorings'.

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass;
the JSON summary must equal RESULT.json; --write regenerates it).

  1. Theorem 1 on random toys (Z/N, a label map, a key map with each key on
     at most two positions of any progression, random outer coloring c0):
     for every frozen set X and every p in {1/7, 1/3}, the exact probability
     (all flips enumerated) that no progression is monochromatic is positive
     iff some Y in the class X xor (subset of free keys) is good; and some
     (X, p) succeeds iff the class {c0 xor 1_Y} has a good member.
  2. Proposition 3 on the same toys: with no random flip, P is monochromatic
     in beta iff the set of positions whose key is in Y equals the class
     {c0 != beta} on P, exactly.
  3. Digit transversals: S = {x in [p^L] : some base-p digit of x is 0}
     meets every progression of length >= p in [p^L], exhaustively for
     (p, L) in {(3,3), (3,4), (5,2), (5,3), (7,2)}; its density is
     1 - (1 - 1/p)^L exactly, and it also contains a whole progression
     (step p from 0), so it is a hitting set but not proper.  At the
     template scale the exponent
     -log_k(density) tends to a (table at the 21 points of P1a's model).
  4. The random benchmark: closure through 'density x supersaturation' at
     coefficient c needs every proper Y to have density >= k^(-4c+o(1));
     with the proved density 1/(2k) this reaches only c > 1/4, with
     density k^(-a) it reaches c > a/4 < 1/8.
  5. Behrend warning: a Behrend sphere set in [N] with no 3-term
     progression, against the expected number of 3-APs of a random set of
     the same density (supersaturation at the random count fails for APs).
"""
import json
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product
from pathlib import Path

getcontext().prec = 60
FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL', msg)


rng = random.Random(20261027)


# ------------------------------------------------------------ toys
def toy(N, k, nkeys, nlabels):
    """Random label and key maps on Z/N; keys reassigned until every key
    occupies at most two positions of every k-AP (as in the template)."""
    while True:
        key = [rng.randrange(nkeys) for _ in range(N)]
        lab = [rng.randrange(nlabels) for _ in range(N)]
        aps = []
        for d in range(1, N // 2 + 1):
            for x in range(N):
                P = [(x + j * d) % N for j in range(k)]
                if len(set(P)) == k:
                    aps.append(tuple(P))
        aps = sorted(set(tuple(sorted(P)) for P in aps))
        if all(max(sum(1 for n in P if key[n] == kk) for kk in set(key[n] for n in P)) <= 2
               for P in aps):
            c0 = [rng.randrange(2) for _ in range(nlabels)]
            return key, lab, c0, aps


def good(color, aps):
    return all(len({color[n] for n in P}) > 1 for P in aps)


def coloring(key, lab, c0, Y):
    return [c0[lab[n]] ^ (1 if key[n] in Y else 0) for n in range(len(key))]


eq_cases = 0
prop3_cases = 0
for trial in range(12):
    N, k, nkeys, nlabels = 14, 3, 7, 4
    key, lab, c0, aps = toy(N, k, nkeys, nlabels)
    keys = sorted(set(key))
    goodY = set()
    for bits in product((0, 1), repeat=len(keys)):
        Y = frozenset(kk for kk, b in zip(keys, bits) if b)
        col = coloring(key, lab, c0, Y)
        if good(col, aps):
            goodY.add(Y)
        # Proposition 3, at p = 0
        for P in aps:
            for beta in (0, 1):
                mono = all(col[n] == beta for n in P)
                YP = {i for i, n in enumerate(P) if key[n] in Y}
                cls = {i for i, n in enumerate(P) if c0[lab[n]] != beta}
                check(mono == (YP == cls), 'Prop 3: mono iff Y_P is the class')
                prop3_cases += 1
    any_success = False
    for xbits in product((0, 1), repeat=len(keys)):
        X = frozenset(kk for kk, b in zip(keys, xbits) if b)
        free = [kk for kk in keys if kk not in X]
        for p in (Fraction(1, 7), Fraction(1, 3)):
            ok = Fraction(0)
            for fb in product((0, 1), repeat=len(free)):
                F = frozenset(kk for kk, b in zip(free, fb) if b)
                if X ^ F in goodY:
                    w = Fraction(1)
                    for b in fb:
                        w *= p if b else 1 - p
                    ok += w
            reachable = any((X ^ frozenset(kk for kk, b in zip(free, fb) if b)) in goodY
                            for fb in product((0, 1), repeat=len(free)))
            check((ok > 0) == reachable, 'Thm 1: P(good) > 0 iff a good Y is reachable')
            any_success |= ok > 0
            eq_cases += 1
    check(any_success == bool(goodY), 'Thm 1: some (X, p) succeeds iff the class has a good member')
OUT['theorem1_cases'] = eq_cases
OUT['prop3_cases'] = prop3_cases
print(f'1. Theorem 1: {eq_cases} (toy, X, p) cases, success iff a good key-measurable Y exists')
print(f'2. Proposition 3: {prop3_cases} (Y, P, beta) cases, mono iff Y_P equals the class')


# ------------------------------------------------------------ digit sets
def digit_set(p, L):
    M = p ** L
    S = set()
    for x in range(M):
        y, has0 = x, False
        for _ in range(L):
            if y % p == 0:
                has0 = True
            y //= p
        if has0:
            S.add(x)
    return M, S


digits = {}
for p, L in ((3, 3), (3, 4), (5, 2), (5, 3), (7, 2)):
    M, S = digit_set(p, L)
    hit = all(any(x + j * d in S for j in range(p))
              for d in range(1, M) for x in range(M - (p - 1) * d))
    check(hit, f'digits: an AP of length {p} misses S in [{p}^{L}]')
    check(Fraction(len(S), M) == 1 - Fraction(p - 1, p) ** L, 'digit density')
    # not proper (radar-dd, S7): the step-p progression from 0 lies inside S
    check(all(j * p in S for j in range(min(p, M // p))), 'digits: S should contain a whole AP')
    digits[f'{p}^{L}'] = f'{len(S)}/{M}'
OUT['digit_transversals'] = digits

LN2 = Decimal(2).ln()


def scale(log2k, a, c):
    """ln Y0 in P1a's template model; digit density with p ~ k prime:
    1 - (1 - 1/k)^(ln Y0 / ln k) <= ln Y0 / (k ln k)."""
    k = Decimal(2) ** log2k
    lnk = log2k * LN2
    D = (k ** Decimal(a)).to_integral_value(rounding='ROUND_CEILING')
    h0 = D * lnk.to_integral_value(rounding='ROUND_CEILING') ** 2
    lnlam = Decimal('1.25506') * h0 / h0.ln() * lnk
    lnq = Decimal(c) * k * lnk / D
    lnY0 = lnq - lnlam - 2 * lnk - Decimal(2048).ln()
    dens = lnY0 / (k * lnk)
    return float(-dens.ln() / lnk)


tab = {}
for log2k in (739, 1024, 4096):
    for a in ('0.3', '0.45', '0.49'):
        tab[f'k=2^{log2k},a={a}'] = round(scale(log2k, a, Decimal(1) / 9), 4)
for name, e in tab.items():
    a = float(name.split('a=')[1])
    check(a - 0.02 < e < a + 0.02, f'{name}: digit exponent {e} far from a')
OUT['digit_exponent_vs_a'] = tab
print(f'3. digit transversals hit every AP of length p ({len(digits)} cases, exhaustive); '
      f'-log_k(density) at scale Y0: ' + ', '.join(f'{n}: {e}' for n, e in tab.items() if '739' in n))

# ------------------------------------------------------------ benchmark
bench = {}
for label_, bY in (('proved density 1/(2k)', Fraction(1)), ('density k^-a, a = 49/100', Fraction(49, 100)),
                   ('density k^-a, a = 1/2 (limit)', Fraction(1, 2))):
    bench[label_] = str(bY / 4)
check(bench['proved density 1/(2k)'] == '1/4', 'benchmark: 1/(2k) gives 1/4')
check(Fraction(bench['density k^-a, a = 49/100']) < Fraction(1, 8), 'benchmark: a < 1/2 stays below 1/8')
OUT['benchmark_closure_from_c_above'] = bench
print('4. benchmark closure threshold c > b_Y/4: ' + ', '.join(f'{n} -> {v}' for n, v in bench.items()))


# ------------------------------------------------------------ Behrend
def behrend(dim, base):
    """Digits < base/2 in 'dim' digits of base 'base', on the most popular sphere."""
    spheres = {}
    for digs in product(range(base // 2), repeat=dim):
        r = sum(x * x for x in digs)
        x = sum(dd * base ** i for i, dd in enumerate(digs))
        spheres.setdefault(r, []).append(x)
    best = max(spheres.values(), key=len)
    return base ** dim, sorted(best)


Nb, B = behrend(6, 10)
Bs = set(B)
threeAPs = sum(1 for i, x in enumerate(B) for y in B[i + 1:] if 2 * y - x in Bs)
dens = len(B) / Nb
expected = dens ** 3 * Nb * Nb / 4
check(threeAPs == 0, 'Behrend set has a 3-AP')
check(expected > 1, 'random count should exceed 1')
OUT['behrend'] = {'N': Nb, 'size': len(B), 'three_APs': threeAPs, 'random_expected_3APs': round(expected, 2)}
print(f'5. Behrend: |B| = {len(B)} in [{Nb}], 0 three-term APs, a random set of this density '
      f'expects {expected:.1f}')

out = json.dumps(OUT, indent=2, sort_keys=True) + '\n'
res = Path(__file__).with_name('RESULT.json')
if '--write' in sys.argv:
    res.write_text(out)
elif not res.exists() or res.read_text() != out:
    check(False, 'RESULT.json differs from the computed summary')
if FAIL:
    print(f'{len(FAIL)} check(s) failed')
    raise SystemExit(1)
print('Test passé : all checks pass')
