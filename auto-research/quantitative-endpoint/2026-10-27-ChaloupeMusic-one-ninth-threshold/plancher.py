"""The floor of the 1/9 threshold for the union-bound template, in exact arithmetic (PROOF.md, Section 2).

Assume (T1)-(T6) of 2026-10-26-ChaloupeMusic-template-limit and f = F/k >= t/9. Section 2 of PROOF.md derives

    f < psi(s)/2 - e*,  psi(s) = (1/2 - s)(A + 2 log(s/2)),  0 < s = eps_1 + eps_2 < 1/2,
    A = t/2 - (1/2) log(576 (1 - delta) l_D) + eta - log(4t/3),  l_D = 4(t/9 + e*) + log(4t/3),

with delta = 2*10^-8 (theta(x) >= (1 - delta) x for x >= e^45) and eta = 2^-100. psi is concave, so a
tangent bounds its maximum. On an interval [ta, tb] of t, A is bounded at tb and t/9 at ta; the interval
is closed when psi_max/2 - e* <= ta/9, a contradiction. Logarithms are certified rational bounds.
"""
import math
from fractions import Fraction as Q

from logs import ln_lo, ln_up

DELTA = Q(2, 10 ** 8)
ETA = Q(1, 2 ** 100)
CLASSES = {"D2": (45, Q(1, 2)), "D1": (19, Q(1)), "D0": (37, Q(1))}


def e_star(cls):
    """e* = (1/2)(log 10 + l_cls), as an interval."""
    base, expo = CLASSES[cls]
    return (ln_lo(10) + expo * ln_lo(base)) / 2, (ln_up(10) + expo * ln_up(base)) / 2


def a_up(ta, tb, es_lo, delta=DELTA):
    l_d = 4 * (ta / 9 + es_lo) + ln_lo(4 * ta / 3)
    return tb / 2 - ln_lo(576 * (1 - delta) * l_d) / 2 + ETA - ln_lo(4 * ta / 3)


def psi_max_up(A):
    """Upper bound for max over 0 < s < 1/2 of (1/2 - s)(A + 2 log(s/2)), by the tangent at s0."""
    a = float(A)
    lo, hi = 1e-9, 0.4999                      # psi' decreases; bisection for psi'(s) = 0, floats only to pick s0
    for _ in range(200):
        m = (lo + hi) / 2
        if -(a + 2 * math.log(m / 2)) + (0.5 - m) * 2 / m > 0:
            lo = m
        else:
            hi = m
    s0 = Q(lo).limit_denominator(10 ** 12)
    h = Q(1, 2) - s0
    l_lo, l_up = ln_lo(s0 / 2), ln_up(s0 / 2)
    val = h * (A + 2 * l_up)
    d_lo = -(A + 2 * l_up) + h * 2 / s0
    d_up = -(A + 2 * l_lo) + h * 2 / s0
    return val + max(d_up * h, -d_lo * s0, Q(0)), s0


def closes(ta, tb, cls, delta=DELTA):
    es_lo, es_up = e_star(cls)
    pm, s0 = psi_max_up(a_up(ta, tb, es_lo, delta))
    return pm / 2 - es_lo <= ta / 9, pm / 2 - es_lo - ta / 9, s0


def floor_cover(t_from, t_to, cls, delta=DELTA):
    """Cover [t_from, t_to] by closed intervals; returns their number, or raises at the first that fails."""
    ta, n = Q(t_from), 0
    if not ta < t_to:
        raise AssertionError("floor: empty range")
    while ta < t_to:
        step = Q(64)
        while True:
            tb = min(ta + step, Q(t_to))
            ok, gap, _ = closes(ta, tb, cls, delta)
            if ok:
                break
            step /= 2
            if step < Q(1, 2 ** 20):
                raise AssertionError(f"floor: interval at t = {float(ta)} does not close")
        ta, n = tb, n + 1
    return n


def margin_at(t, cls, delta=DELTA):
    """psi_max/2 - e* - t/9 at a single t (negative: the template cannot give 1/9 at this k)."""
    return closes(Q(t), Q(t), cls, delta)[1]
