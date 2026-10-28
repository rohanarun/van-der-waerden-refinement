#!/usr/bin/env python3
"""First-family circularity: exact checks (standard library only).

Base commit: 63bef9ca996786a41169de4a0c3d6b3b47b0fe96.

1. Injective x-labels.  The x-label of n in Z/q^D is (U(x_i(n)))_{i<=D},
   x_i(n) = (n mod q^i)/q^i, U the partition of [0,1) into intervals of
   width H_x = 1/(k^2 lambda).  If q*H_x < 1 the x-label determines n.
   Checked exhaustively on small (q, D, k, lambda); controls with q*H_x >= 1
   must collide, within the fibre bound (floor(q H_x) + 1)^D, and the set of
   in-fibre differences must stay within (2 q H_x + 1)^D.  For an injective
   case, the k(N-1) progressions through 0 must have distinct label words.
2. Regime.  With D = ceil(k^a), M = ceil(k^m), h_0 = D or D*ceil(ln k)^2,
   lambda = prod_{l <= h_0} l^floor(ln 2M / ln l), and ln q <= c k^{1-a} ln k
   + ln(2k^2), the sufficient condition for q*H_x < 1 is evaluated with
   pi(x) > x/ln x (x >= 17).  For a < 1/2 the sufficient condition for
   q >= 400 k^3 lambda (the range where the concurrent single-label
   obstruction is proved) is evaluated with
   pi(x) < 1.25506 x/ln x.  Decimal arithmetic, 80 digits.
3. Short periods.  No 2-colouring of (Z/2)^D (D = 2, 3) or of AG(2,3)
   avoids a monochromatic affine line; AG(2,5) has one that does (stored
   certificate), so the plane statement stops at h = 3.

Prints a JSON report; exit 0 and stdout byte-identical to RESULT.json.
Assertions are load-bearing: run with `python3 -B verify.py`, never -O.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product
from math import floor
import json

getcontext().prec = 80


# 1. Injective x-labels -----------------------------------------------------

def x_label(n, q, D, Hx):
    return tuple(floor(Fraction(n % q ** i, q ** i) / Hx) for i in range(1, D + 1))


def fibres(q, D, k, lam):
    Hx = Fraction(1, k * k * lam)
    count = {}
    for n in range(q ** D):
        lab = x_label(n, q, D, Hx)
        count[lab] = count.get(lab, 0) + 1
    return max(count.values()), q * Hx


def difference_set(q, D, k, lam):
    Hx = Fraction(1, k * k * lam)
    N = q ** D
    def close(t):              # circle distance of t in [0,1) to 0 is < H_x
        return min(t, 1 - t) < Hx
    return sum(1 for delta in range(N)
               if all(close(Fraction(delta % q ** i, q ** i)) for i in range(1, D + 1)))


def words_through_zero(q, D, k, lam):
    Hx = Fraction(1, k * k * lam)
    N = q ** D
    lab = [x_label(n, q, D, Hx) for n in range(N)]
    words = set()
    for j0 in range(k):
        for d in range(1, N):
            n0 = (-j0 * d) % N
            words.add(tuple(lab[(n0 + j * d) % N] for j in range(k)))
    return len(words), k * (N - 1)


INJECTIVE = [(11, 3, 3, 2), (13, 3, 3, 2), (7, 4, 3, 1)]
CONTROLS = [(11, 3, 3, 1), (13, 3, 3, 1), (29, 2, 3, 1)]


def check_injectivity():
    out = {}
    for q, D, k, lam in INJECTIVE + CONTROLS:
        worst, qHx = fibres(q, D, k, lam)
        assert worst <= (floor(qHx) + 1) ** D, (q, D, k, lam)
        diffs = difference_set(q, D, k, lam)
        assert diffs <= (2 * qHx + 1) ** D, (q, D, k, lam)
        if qHx < 1:
            assert worst == 1, ('label not injective although qH_x < 1', q, D, k, lam)
        else:
            assert worst > 1, ('control did not collide', q, D, k, lam)
        out[f'q={q},D={D},k={k},lambda={lam}'] = {
            'qH_x': str(qHx), 'largest_fibre': worst, 'difference_set': diffs,
            'injective': worst == 1}
    distinct, expected = words_through_zero(11, 3, 3, 2)
    assert distinct == expected
    out['words_through_0 (q=11,D=3,k=3,lambda=2)'] = {
        'distinct': distinct, 'k(N-1)': expected}
    return out


# 2. Regime -----------------------------------------------------------------

def ln(x):
    return Decimal(x).ln()


def ceil_dec(x):
    i = int(x)
    return i if Decimal(i) == x else i + 1


def regime(k_exp10, a, m, c, sharpened):
    k = Decimal(10) ** k_exp10
    lk = ln(k)
    D = Decimal(ceil_dec(k ** Decimal(a)))
    M = Decimal(ceil_dec(k ** Decimal(m)))
    h0 = D * Decimal(ceil_dec(lk)) ** 2 if sharpened else D
    assert h0 >= 17 and h0 <= 2 * M
    c = Decimal(c.numerator) / Decimal(c.denominator)
    ln2M = ln(2 * M)
    ln_lambda_min = Decimal('0.5') * (h0 / ln(h0)) * ln2M
    ln_lambda_max = Decimal('1.25506') * (h0 / ln(h0)) * ln2M
    ln_q_max = c * k * lk / D + ln(2 * k * k)
    ln_q_min = c * k * lk / D
    injective = ln_q_max < 2 * lk + ln_lambda_min          # q H_x < 1
    single_label = ln_q_min >= ln(400) + 3 * lk + ln_lambda_max   # q >= 400 k^3 lambda
    return injective, single_label


def check_regime():
    c, m = Fraction(1, 9), '0.99'
    out = {}
    for a in ('0.55', '0.6', '0.75'):
        for k_exp10 in (50, 200, 1000):
            for sharpened in (False, True):
                inj, sl = regime(k_exp10, a, m, c, sharpened)
                assert inj and not sl, (a, k_exp10, sharpened)
        out[f'a={a}'] = 'qH_x < 1 (x-label injective) for k = 10^50, 10^200, 10^1000, h_0 = D and D ceil(ln k)^2'
    for a in ('0.4', '0.45'):
        for k_exp10 in (50, 200, 1000):
            inj, sl = regime(k_exp10, a, m, c, True)
            assert sl and not inj, (a, k_exp10)
        out[f'a={a}'] = 'q >= 400 k^3 lambda (single-label regime) for k = 10^50, 10^200, 10^1000, h_0 = D ceil(ln k)^2'
    inj, sl = regime(200, '0.5', m, c, True)
    out['a=0.5 (boundary, k=10^200, sharpened h_0)'] = {'injective': inj, 'single_label': sl}
    return out


# 3. Short periods ----------------------------------------------------------

def affine_lines(h, D):
    pts = list(product(range(h), repeat=D))
    idx = {p: i for i, p in enumerate(pts)}
    lines = set()
    for p in pts:
        for t in pts:
            if any(t):
                line = frozenset(idx[tuple((x + j * s) % h for x, s in zip(p, t))]
                                 for j in range(h))
                if len(line) == h:
                    lines.add(line)
    return len(pts), [sorted(l) for l in lines]


def mono_free(col, lines):
    return all(len({col[i] for i in l}) == 2 for l in lines)


def every_colouring_has_mono_line(h, D):
    n, lines = affine_lines(h, D)
    for mask in range(2 ** n):
        col = [(mask >> i) & 1 for i in range(n)]
        if mono_free(col, lines):
            return False, len(lines)
    return True, len(lines)


AG25_CERTIFICATE = '0101010101000110100000111'


def check_short_periods():
    out = {}
    for h, D in ((2, 2), (2, 3), (3, 2)):
        forced, nlines = every_colouring_has_mono_line(h, D)
        assert forced, (h, D)
        out[f'(Z/{h})^{D}'] = {'affine_lines': nlines, 'monochromatic_line_forced': True}
    n, lines = affine_lines(5, 2)
    col = [int(ch) for ch in AG25_CERTIFICATE]
    assert len(col) == n and mono_free(col, lines)
    out['(Z/5)^2 control'] = {'affine_lines': len(lines),
                              'monochromatic_line_forced': False,
                              'certificate': AG25_CERTIFICATE}
    return out


if __name__ == '__main__':
    report = {
        'base_commit': '63bef9ca996786a41169de4a0c3d6b3b47b0fe96',
        'injectivity': check_injectivity(),
        'regime': check_regime(),
        'short_periods': check_short_periods(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
