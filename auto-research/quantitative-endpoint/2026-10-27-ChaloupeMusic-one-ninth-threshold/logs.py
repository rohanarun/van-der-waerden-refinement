"""Certified rational bounds for natural logarithms (the series of the retuned endpoint's verify.py)."""
import math
from fractions import Fraction as Q


def pow2(n):
    return Q(1 << n) if n >= 0 else Q(1, 1 << (-n))


def ln2_bounds(N=60):
    s = sum(Q(1, n * 2 ** n) for n in range(1, N + 1))
    return s, s + Q(1, (N + 1) * 2 ** N)


L2_LO, L2_UP = ln2_bounds()


def _series(y, N=60):
    y = Q(y)
    if y == 1:
        return Q(0), Q(0)
    z = (y - 1) / (y + 1)
    s = 2 * sum(z ** (2 * m + 1) / (2 * m + 1) for m in range(N))
    return s, s + 2 * abs(z) ** (2 * N + 1) / ((2 * N + 1) * (1 - z * z))


def _split(y):
    y = Q(y)
    e = math.floor(math.log2(y.numerator) - math.log2(y.denominator))
    while pow2(e) > y:
        e -= 1
    while pow2(e + 1) <= y:
        e += 1
    return e, y / pow2(e)                      # y = 2^e m, 1 <= m < 2


K = 200                                        # outward rounding to 2^-K keeps every bound certified


def _up(x):
    return Q(math.ceil(x * 2 ** K), 2 ** K)


def _down(x):
    return Q(math.floor(x * 2 ** K), 2 ** K)


def ln_up(y):
    """Upper bound for log y (y > 0): log is increasing, so y is first rounded up, the result up."""
    e, m = _split(y)
    return _up(e * (L2_UP if e >= 0 else L2_LO) + _series(_up(m))[1])


def ln_lo(y):
    e, m = _split(y)
    return _down(e * (L2_LO if e >= 0 else L2_UP) + _series(_down(m))[0])
