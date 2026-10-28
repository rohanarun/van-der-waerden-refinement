"""Checks for the off-diagonal window 4 <= l < p0(k) of ap-free-frozen-sets.

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass;
the JSON summary must equal RESULT.json; --write regenerates it).

  1. Exact small values of W(l, k) in the split form ([N] = S + A, no l-AP
     in S, no k-AP in A), by exhaustive search, for (l, k) = (3, 3), (3, 4),
     (3, 5), (4, 4).  Known values: 9, 18, 22, 35.  (Proposition 1 has a
     two-line proof and bites only at sizes where r_l(N) < N/k, far beyond
     exhaustive reach, so it is not tested on small cases.)
  2. Proposition 2 (first moment): whenever 3 ln N < k and
     N^2 (3 ln N / k)^l < 1, a split of [N] exists; checked as an
     inequality chain on exact small cases, and the threshold l_rand
     evaluated at the template points.
  3. Template numerics (Decimal, 60 digits) at the 21 points of
     ap-free-frozen-sets: ln N0 with N0 = 2 Y0, p0(k), l_rand(N0), the
     first-moment lower bound for ln W at l = p0 - 1, the log-power
     exponent kappa a closing bound on r_l must beat, and the O'Bryant
     density exponent at the worst useful length.
"""
import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 60
FAIL = []
OUT = {}


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print('FAIL', msg)


# ------------------------------------------------- 1. exact small values
def aps_ending_at(n, length):
    """All length-term APs in [0, n] whose last term is n (step >= 1)."""
    out = []
    for d in range(1, n // (length - 1) + 1):
        out.append([n - i * d for i in range(length)])
    return out


def splittable(N, l, k):
    """Is there S with no l-AP and [N] minus S with no k-AP?"""
    col = [None] * N

    def dfs(i):
        if i == N:
            return True
        for c, length in ((0, l), (1, k)):
            if all(not all(col[x] == c for x in ap[1:]) for ap in aps_ending_at(i, length)):
                col[i] = c
                if dfs(i + 1):
                    return True
                col[i] = None
        return False

    return dfs(0)


def W(l, k):
    N = max(l, k)
    while splittable(N, l, k):
        N += 1
    return N


Ws = {(3, 3): 9, (3, 4): 18, (3, 5): 22, (4, 4): 35}
found = {}
for (l, k), w in Ws.items():
    found[(l, k)] = W(l, k)
    check(found[(l, k)] == w, f'W({l},{k}) = {found[(l, k)]}, expected {w}')
OUT['W_small'] = {f'{a},{b}': v for (a, b), v in found.items()}
print(f'1. exact split values: {OUT["W_small"]} (known 9, 18, 22, 35)')

# ------------------------------------------------- 2. Proposition 2
def ap_count(N, length):
    return sum(N - (length - 1) * d for d in range(1, (N - 1) // (length - 1) + 1))


# exact first-moment chain on a mid-size case: N = 200, k = 120, l = 9
N_, k_, l_ = 200, 120, 9
rho = Fraction(3) * Fraction(math.log(N_)) / k_
e_S = ap_count(N_, l_) * rho ** l_
e_A = ap_count(N_, k_) * (1 - rho) ** k_
check(ap_count(N_, l_) <= Fraction(N_ * N_, 2 * (l_ - 1)), 'AP count bound')
check(e_S + e_A < 1, f'first moment: {float(e_S)} + {float(e_A)} not < 1')
print(f'2. Prop 2: at N = {N_}, k = {k_}, l = {l_}, expected bad APs '
      f'{float(e_S):.2e} + {float(e_A):.2e} < 1, so W({l_},{k_}) > {N_}')
OUT['prop2_instance'] = {'N': N_, 'k': k_, 'l': l_,
                         'expected_bad': f'{float(e_S + e_A):.6f}'}

# ------------------------------------------------- 3. template numerics
LN2 = Decimal(2).ln()


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def p0(lnk):
    p = 2
    while True:
        if is_prime(p):
            L = (lnk / Decimal(p).ln()).to_integral_value(rounding='ROUND_CEILING')
            if L * (1 - Decimal(1) / p).ln() >= -Decimal(4).ln():
                return p
        p += 1


def point(log2k, a=None, c=None, source=False):
    """Same model as ap-free-frozen-sets: D = ceil(k^a), h0 = D ceil(ln k)^2,
    ln q = c k ln k / D, ln lam <= 1.25506 (h0/ln h0) ln k; source: c = 1e-5,
    D = ceil(k^(1/10)), h0 = D^2, ln lam = h0 ln(2M), M = ceil(sqrt k).
    Y0 = q/(2048 k^2 lam) (Lemma R of single-label-lenses); N0 = 2 Y0."""
    k = Decimal(2) ** log2k
    lnk = log2k * LN2
    if source:
        c = Decimal('1e-5')
        Dd = (k ** (Decimal(1) / 10)).to_integral_value(rounding='ROUND_CEILING')
        h0 = Dd * Dd
        lnlam = h0 * (2 * k.sqrt().to_integral_value(rounding='ROUND_CEILING')).ln()
    else:
        Dd = (k ** Decimal(a)).to_integral_value(rounding='ROUND_CEILING')
        h0 = Dd * lnk.to_integral_value(rounding='ROUND_CEILING') ** 2
        lnlam = Decimal('1.25506') * h0 / h0.ln() * lnk
    lnq = Decimal(c) * k * lnk / Dd
    lnN0 = lnq - lnlam - 2 * lnk - Decimal(2048).ln() + LN2
    check(lnN0 > 4 * lnk, f'point 2^{log2k}: outside the regime')
    pp = p0(lnk)
    lrand = 2 * lnN0 / (k / (3 * lnN0)).ln()
    # first-moment lower bound on ln W(l, k) at l = p0 - 1: largest L with
    # l ln(k/(3L)) > 2L, solved by fixed-point iteration from L = l ln k
    l = Decimal(pp - 1)
    L = l * lnk
    for _ in range(200):
        L = l * (k / (3 * L)).ln() / 2
    lnW_rand = L
    kappa = (2 * k).ln() / lnN0.ln()
    n = math.ceil(math.log2(pp - 1))
    obryant = n * Decimal(2) ** (Decimal(n - 1) / 2) * lnN0 ** (Decimal(1) / n) - lnN0.ln() / (2 * n)
    return {
        'ln_N0_log2': round(float(lnN0.ln() / LN2), 2),
        'p0': pp,
        'l_rand_log2': round(float(lrand.ln() / LN2), 2),
        'first_moment_lnW_at_p0_minus_1_log2': round(float(lnW_rand.ln() / LN2), 2),
        'gap_log2': round(float((lnN0 / lnW_rand).ln() / LN2), 2),
        'kappa_needed': round(float(kappa), 4),
        'obryant_exponent_log2': round(float(obryant.ln() / LN2), 2),
        'ln_2k_log2': round(float((2 * k).ln().ln() / LN2), 2),
    }


table = {}
for log2k in (739, 1024, 4096):
    for a in ('0.3', '0.45', '0.49'):
        for c, cn in ((Decimal(1) / 9, '1/9'), (Decimal(1) / 4, '1/4')):
            table[f'k=2^{log2k},a={a},c={cn}'] = point(log2k, a, c)
    table[f'k=2^{log2k},source'] = point(log2k, source=True)
for name, row in table.items():
    check(row['first_moment_lnW_at_p0_minus_1_log2'] < row['ln_N0_log2'],
          f'{name}: known lower bound already opens the window')
    check(math.log2(row['p0']) < row['l_rand_log2'], f'{name}: p0 above l_rand')
    check(1 < row['kappa_needed'] < 2, f'{name}: kappa outside (1, 2)')
    check(row['obryant_exponent_log2'] > row['ln_2k_log2'], f'{name}: O\'Bryant density already >= 1/(2k)')
kmin = min(r['kappa_needed'] for r in table.values())
kmax = max(r['kappa_needed'] for r in table.values())
gmin = min(r['gap_log2'] for r in table.values())
OUT['template'] = table
OUT['summary'] = {'kappa_needed_range': [kmin, kmax], 'min_gap_log2_lnN0_over_lnW_known': gmin}
for name in ('k=2^739,a=0.3,c=1/9', 'k=2^739,a=0.49,c=1/9', 'k=2^4096,a=0.49,c=1/9', 'k=2^739,source'):
    r = table[name]
    print(f'3. {name}: log2 ln N0 = {r["ln_N0_log2"]}, p0 = {r["p0"]}, log2 l_rand = {r["l_rand_log2"]}, '
          f'log2 ln W_known(p0-1) = {r["first_moment_lnW_at_p0_minus_1_log2"]}, kappa = {r["kappa_needed"]}, '
          f'log2 O\'Bryant exponent = {r["obryant_exponent_log2"]} vs log2 ln 2k = {r["ln_2k_log2"]}')
print(f'   all 21 points: kappa in [{kmin}, {kmax}], ln N0 / ln W_known >= 2^{gmin}')

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
