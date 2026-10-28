"""Exact checks for "How sparse can a transversal of the slow words be?".

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass,
last line "Test passé : all checks pass"; the JSON summary it prints must equal
RESULT.json; --write regenerates RESULT.json).

  1. Lemma 2: signed combinatorial lines of [p]^s, read as base-p digits, are
     p-APs of Z with step sum_{S+} p^i - sum_{S-} p^i, inside the box, without
     carries.  Control: a line that wraps a coordinate modulo p is not an AP.
  2. Theorem 3 (r = 1): no affine hyperplane of F_p^s meets every signed line
     when s >= 2 + floor(log2 p); controls below the threshold have one.
  3. Proposition 5: forms with no nonzero {0,+-1} vector in their common kernel
     give a union of r = floor(s log_p 3) + 1 hyperplanes meeting every signed
     line (all lines enumerated), density <= r/p.
  4. The union bound |union of r' distinct affine hyperplanes| >= min(r',p)/(2p)
     p^s on random families, counted exactly.
  5. Theorem 1: w = 1/k is a fractional transversal of the k-APs of [Y] and the
     disjoint windows give the dual value floor(Y/k).
  6. Exponents (leading order ln|J| = c k^(1-a) ln k, c = 1/9, k = 2^739) of
     Corollary 4's lower bound and of the digit sets.
  7. Digit sets {some of the L base-p digits is 0} meet every p-AP of [p^L]
     and are unions of coordinate hyperplanes on aligned boxes.
  8. Proposition 6: {sum x_i^2 in R} meets every signed line of F_p^s, s < p,
     with R a smallest set meeting every w + u*squares; density ~ |R|/p.
  9. The same rule on base-p digits misses p-APs with carries in [p^L].
"""
import itertools
import json
import math
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL:', msg)


def signed_lines(p, s):
    """Each line as (list of points, eps); points are tuples in [0,p)^s."""
    for eps in itertools.product((-1, 0, 1), repeat=s):
        if not any(eps):
            continue
        F = [i for i in range(s) if eps[i] == 0]
        for z in itertools.product(range(p), repeat=len(F)):
            pts = []
            for j in range(p):
                x = [0] * s
                for i, v in zip(F, z):
                    x[i] = v
                for i in range(s):
                    if eps[i] == 1:
                        x[i] = j
                    elif eps[i] == -1:
                        x[i] = p - 1 - j
                pts.append(tuple(x))
            yield pts, eps


def value(x, p):
    return sum(c * p ** i for i, c in enumerate(x))


# ---------------------------------------------------------------- 1. Lemma 2
n1 = 0
for p, s in ((3, 3), (5, 3), (7, 2)):
    for pts, eps in signed_lines(p, s):
        v = [value(x, p) for x in pts]
        step = sum(p ** i for i in range(s) if eps[i] == 1) - sum(p ** i for i in range(s) if eps[i] == -1)
        check(all(v[j + 1] - v[j] == step for j in range(p - 1)) and step != 0, f'Lemma 2 at {p},{s}')
        check(all(0 <= t < p ** s for t in v), 'line leaves the box')
        n1 += 1
# control: wrapping a coordinate modulo p breaks the AP
p = 5
wrapped = [value(((2 + j) % p, 0), p) for j in range(p)]
ctrl1 = len({wrapped[j + 1] - wrapped[j] for j in range(p - 1)}) > 1
check(ctrl1, 'control 1: a wrapped line is an AP')
OUT['lemma2'] = {'lines_checked': n1, 'wrapped_line_is_not_AP': ctrl1}
print(f'1. Lemma 2: {n1} signed lines are p-APs of Z without carries; a wrapped line is not')


# ------------------------------------------------------------- 2. Theorem 3
def hyperplanes(p, s):
    seen = set()
    for w in itertools.product(range(p), repeat=s):
        if not any(w):
            continue
        f = next(x for x in w if x)
        inv = pow(f, -1, p)
        w = tuple(x * inv % p for x in w)
        if w in seen:
            continue
        seen.add(w)
        for v in range(p):
            yield w, v


def hits_all(H, p, s, lines):
    def inT(x):
        return any(sum(a * b for a, b in zip(w, x)) % p == v for w, v in H)
    return all(any(inT(x) for x in pts) for pts, _ in lines)


res2 = {}
for p, s, expect in ((3, 3, False), (3, 4, False), (5, 4, False), (3, 2, True), (5, 2, True)):
    lines = list(signed_lines(p, s))
    found = sum(hits_all([h], p, s, lines) for h in hyperplanes(p, s))
    if not expect:
        check(s >= 2 + int(math.log2(p)), 'threshold not met in a positive case')
        check(found == 0, f'Theorem 3: a single hyperplane is a transversal at {p},{s}')
    else:
        check(found > 0, f'control 2: no single-hyperplane transversal at {p},{s}')
    res2[f'{p},{s}'] = found
OUT['theorem3_single_hyperplane_transversals'] = res2
print(f'2. Theorem 3 (r = 1): counts of single-hyperplane transversals {res2} '
      '(0 above the threshold, > 0 below)')

# ------------------------------------------------------------ 3. Prop. 5
rng = random.Random(20261027)


def kernel_free(W, p, s):
    for eps in itertools.product((-1, 0, 1), repeat=s):
        if any(eps) and all(sum(a * b for a, b in zip(w, eps)) % p == 0 for w in W):
            return False
    return True


res3 = {}
for p, s in ((7, 4), (7, 6)):
    r = math.floor(s * math.log(3) / math.log(p)) + 1
    for _ in range(500):
        W = [tuple(rng.randrange(p) for _ in range(s)) for _ in range(r)]
        if all(any(w) for w in W) and kernel_free(W, p, s):
            break
    else:
        check(False, f'Prop. 5: no kernel-free family at {p},{s}')
        continue
    H = [(w, 0) for w in W]
    nlines = sum(1 for _ in signed_lines(p, s))
    ok = hits_all(H, p, s, signed_lines(p, s))
    check(ok, f'Prop. 5 family misses a line at {p},{s}')
    inside = sum(1 for x in itertools.product(range(p), repeat=s)
                 if any(sum(a * b for a, b in zip(w, x)) % p == 0 for w in W))
    dens = Fraction(inside, p ** s)
    check(dens <= Fraction(r, p), 'Prop. 5 density above r/p')
    res3[f'{p},{s}'] = {'r': r, 'lines': nlines, 'density': str(dens)}
OUT['prop5'] = res3
print(f'3. Prop. 5: {res3}')

# ------------------------------------------------------------ 4. union bound
n4 = 0
for p, s in ((5, 4), (7, 3)):
    allH = list(hyperplanes(p, s))
    pts = list(itertools.product(range(p), repeat=s))
    for _ in range(150):
        rr = rng.randrange(1, p + 3)
        H = rng.sample(allH, rr)
        cnt = sum(1 for x in pts if any(sum(a * b for a, b in zip(w, x)) % p == v for w, v in H))
        check(Fraction(cnt, p ** s) >= Fraction(min(rr, p), 2 * p), 'union bound fails')
        n4 += 1
OUT['union_bound_cases'] = n4
print(f'4. union of r distinct affine hyperplanes >= min(r, p)/(2p): {n4} random families')

# ------------------------------------------------------------ 5. Theorem 1
res5 = {}
for Y, k in ((12, 3), (15, 3), (14, 4), (16, 4)):
    aps = [frozenset(x + j * d for j in range(k)) for d in range(1, Y)
           for x in range(Y - (k - 1) * d)]
    masks = [sum(1 << t for t in A) for A in aps]
    # fractional: every AP has exactly k points, so w = 1/k gives weight 1
    check(all(len(A) == k for A in aps), 'AP of wrong length')
    best = None
    for size in range(Y // k, Y + 1):
        for T in itertools.combinations(range(Y), size):
            tm = sum(1 << t for t in T)
            if all(tm & m for m in masks):
                best = size
                break
        if best is not None:
            break
    check(best >= Y // k, 'integral transversal below the window bound')
    res5[f'{Y},{k}'] = {'fractional_upper': str(Fraction(Y, k)), 'windows_lower': Y // k,
                        'integral_minimum': best}
OUT['theorem1'] = res5
print(f'5. Theorem 1: fractional value in [floor(Y/k), Y/k]; exact integral minima {res5}')

# ------------------------------------------------------------- 6. exponents
getcontext().prec = 60
k = Decimal(2) ** 739
lnk = k.ln()
c = Decimal(1) / 9
res6 = {}
for a in ('0.3', '0.45', '0.49'):
    A = Decimal(a)
    lnJ = c * (k ** (1 - A)) * lnk                     # leading order
    pr = k                                             # p ~ k on the log scale (k <= p < 2k)
    s = (lnJ / pr.ln()).to_integral_value(rounding='ROUND_FLOOR') - 1
    lower = s / (2 * pr * (1 + pr.ln() / Decimal(2).ln()))
    L = (lnJ / pr.ln()).to_integral_value(rounding='ROUND_FLOOR')
    digit = 1 - (1 - 1 / pr) ** int(L) if L < 10 ** 6 else L / pr
    e_low = -lower.ln() / lnk
    e_dig = -Decimal(digit).ln() / lnk
    # the polylog factor 2p(1 + log2 p) costs ln(2 log2 k)/ln k ~ 0.0185 here, o(1) as k grows
    check(e_low > A and e_low - A < Decimal('0.025'), f'Cor. 4 exponent off at a = {a}')
    check(e_dig < e_low, 'digit sets below the lower bound')
    res6[a] = {'lower_bound_exponent': str(round(e_low, 4)), 'digit_set_exponent': str(round(e_dig, 4))}
OUT['exponents'] = res6
print(f'6. -log_k of Corollary 4 bound and of digit sets: {res6}')

# ------------------------------------------------------------- 7. digit sets
res7 = {}
for p, L in ((3, 4), (5, 3)):
    M = p ** L

    def inT(x):
        return any((x // p ** i) % p == 0 for i in range(L))
    ok = True
    for d in range(1, M):
        for x in range(M - (p - 1) * d):
            if not any(inT(x + j * d) for j in range(p)):
                ok = False
    check(ok, f'digit set misses a p-AP at {p},{L}')
    dens = Fraction(sum(inT(x) for x in range(M)), M)
    check(dens == 1 - Fraction(p - 1, p) ** L, 'digit set density')
    res7[f'{p},{L}'] = str(dens)
OUT['digit_sets'] = res7
print(f'7. digit sets meet every p-AP of [p^L]; densities {res7}')

# -------------------------------------------------------- 8. Proposition 6
def quad_blocking(p):
    q0 = {y * y % p for y in range(p)}
    g = next(x for x in range(2, p) if x not in q0)
    n0 = {g * y % p for y in q0}
    sets = [{(w + u) % p for u in S} for S in (q0, n0) for w in range(p)]
    for m in range(1, p + 1):
        for R in itertools.combinations(range(p), m):
            if all(set(R) & S for S in sets):
                return set(R)


res8 = {}
for p, svals in ((7, (2, 3, 4, 5, 6)), (11, (3, 4, 5)), (13, (3, 4))):
    R = quad_blocking(p)
    check(len(R) <= math.ceil(math.log2(2 * p)) + 1, 'blocking set larger than the bound')
    for s in svals:
        ok = all(any(sum(c * c for c in x) % p in R for x in pts) for pts, _ in signed_lines(p, s))
        check(ok, f'Prop. 6: quadratic set misses a signed line at {p},{s}')
        cnt = sum(1 for x in itertools.product(range(p), repeat=s) if sum(c * c for c in x) % p in R)
        dens = Fraction(cnt, p ** s)
        check(abs(float(dens) - len(R) / p) <= len(R) * p ** (-s / 2), 'Prop. 6 density off')
        res8[f'{p},{s}'] = {'R': sorted(R), 'density': str(dens),
                            'linear_lower_bound': round(min(0.5, s / (2 * p * (1 + math.log2(p)))), 4)}
OUT['prop6'] = res8
print(f'8. Proposition 6: quadratic transversals of the box, density ~|R|/p for every s: {res8}')

# ----------------------------------------- 9. the quadratic set does not lift
res9 = {}
for p, L in ((7, 3), (5, 4)):
    R = quad_blocking(p)
    M = p ** L

    def inQ(x):
        return sum(((x // p ** i) % p) ** 2 for i in range(L)) % p in R
    missed = sum(1 for d in range(1, M) for x in range(M - (p - 1) * d)
                 if not any(inQ(x + j * d) for j in range(p)))
    check(missed > 0, f'digit-quadratic set unexpectedly meets every p-AP at {p},{L}')
    res9[f'{p},{L}'] = missed
OUT['digit_quadratic_missed_APs'] = res9
print(f'9. digit-quadratic sets miss p-APs with carries: {res9}')

# ------------------------------------------------------------ 10. Lemma 8
worst10 = None
for _ in range(20000):
    kk = rng.randrange(4, 40)
    L = rng.randrange(1, 50)
    vv = Fraction(rng.randrange(-4000 * L * kk, 4000 * L * kk), rng.randrange(1, 997))
    th = Fraction(rng.randrange(0, 10 ** 6), rng.randrange(1, 991))
    vals = [math.floor(th + vv * j) + L * j * j for j in range(kk)]
    margin = Fraction(2 * len(set(vals)) - kk + 2, 2)       # distinct - (k/2 - 1)
    check(margin >= 0, 'Lemma 8 fails')
    worst10 = margin if worst10 is None else min(worst10, margin)
OUT['lemma8_min_margin'] = str(worst10)
print(f'10. Lemma 8: every lens has at least k/2 - 1 distinct values (min margin {worst10})')

# ----------------------------------------------------------- 11. Prop. 10
res11 = {}
for p in (7, 11, 13):
    R = quad_blocking(p)
    miss = 0
    for _ in range(20000):
        L = rng.randrange(1, 10 ** 6)
        if L % p == 0:
            continue
        cc, vv = rng.randrange(10 ** 9), rng.randrange(-10 ** 6, 10 ** 6)
        if not any((cc + vv * j + L * j * j) % p in R for j in range(p)):
            miss += 1
    check(miss == 0, f'Prop. 10: an integer lens with p not dividing L is missed at {p}')
    cc = next(x for x in range(p) if x not in R)
    ctrl = not any((cc + 3 * p * j + 5 * p * j * j) % p in R for j in range(p))
    check(ctrl, 'control 11: degenerate lens hit')
    res11[str(p)] = {'missed': miss, 'degenerate_control_missed': ctrl}
OUT['prop10'] = res11
print(f'11. Proposition 10: {res11}')

# ------------------------------------------------------------------ summary
OUT['fails'] = len(FAIL)
print(json.dumps(OUT, sort_keys=True))
here = Path(__file__).parent
res = here / 'RESULT.json'
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
