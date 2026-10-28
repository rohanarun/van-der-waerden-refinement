#!/usr/bin/env python3
"""Exact checks for the retuned endpoint constants, not a formal proof.

Base: PR #12 head 029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5 on repository
commit 63bef9ca996786a41169de4a0c3d6b3b47b0fe96.

Every analytic inequality of the retuned construction is reduced to a sum of
terms a * t^j * exp(-d t), each nonincreasing on [T0, oo), whose rational
upper bounds at T0 add up to at most a stated target. A nonincreasing sum
below its target at T0 stays below it for every real t >= T0, so each
certificate covers all larger t, not a grid. Logarithms of rationals are
enclosed by exact atanh series. Only the standard library is used.
Assertions are not used for checks; failures raise VerificationError.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from decimal import Decimal, getcontext, MAX_EMAX, MIN_EMIN, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

# Retuned constants (PR #12 values in comments).
T0 = 709            # PR #12: 512.  1024*log 2 > 709, so k >= 2^1024 gives t >= T0.
AD = 4              # u = e^{t/2}/(AD t^3)            PR #12: 4096
BH = 5              # h0 = ceil(BH D t^3)             PR #12: 256
BS = 4096           # Ms = ceil(BS D t)               PR #12: 4096
AP = 8              # p = AP t^4 / sqrt(k)            PR #12: 65536
C = Q(9, 2)         # F = k(t/8 - log t - C)          PR #12: 20
G = Q(25, 8)        # gamma = 1/2 - G/t               PR #12: 4
EREG = Q(1, 4)      # eps_reg = EREG/t, eta = eps_reg/(8D)   PR #12: 1
DS = Q(1, 16)       # delta_s, s-light threshold      PR #12: 1/2


class VerificationError(RuntimeError):
    """A stated finite check did not hold."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


# --------------------------------------------------------------------------
# Exact enclosures of logarithms and roots.

def _atanh_enclosure(y: Q, terms: int = 60) -> tuple[Q, Q]:
    """0 <= y < 1: enclose atanh(y) = sum y^(2n+1)/(2n+1)."""
    s = Q(0)
    power = y
    for n in range(terms):
        s += power / (2 * n + 1)
        power *= y * y
    tail = power / ((2 * terms + 1) * (1 - y * y))
    return s, s + tail


def log_bounds(x: Q) -> tuple[Q, Q]:
    """Rational lo <= log x <= hi for rational x > 0."""
    require(x > 0, 'log of a nonpositive number')
    if x < 1:
        lo, hi = log_bounds(1 / x)
        return -hi, -lo
    # Reduce by powers of 2 to keep y small.
    n = 0
    while x >= 2:
        x /= 2
        n += 1
    lo_y, hi_y = _atanh_enclosure((x - 1) / (x + 1))
    l2_lo, l2_hi = _atanh_enclosure(Q(1, 3))
    return 2 * lo_y + n * 2 * l2_lo, 2 * hi_y + n * 2 * l2_hi


def log_hi(x) -> Q:
    return log_bounds(Q(x))[1]


def log_lo(x) -> Q:
    return log_bounds(Q(x))[0]


SQRT2_HI = Q(141422, 100000)
CBRT2_HI = Q(126, 100)


def root_checks() -> None:
    require(SQRT2_HI ** 2 >= 2, 'sqrt(2) upper bound fails')
    require(CBRT2_HI ** 3 >= 2, 'cbrt(2) upper bound fails')


# --------------------------------------------------------------------------
# Monomial certificates: a * t^j * exp(-d t), nonincreasing on [T0, oo).

def _exp_neg_upper(x: Q) -> Q:
    """Upper bound for exp(-x), x >= 0, using e >= 2."""
    n = x.numerator // x.denominator
    return Q(1, 1 << n)


def _t0_power_upper(j: Q, t0: int) -> Q:
    if j.denominator == 1:
        return Q(t0) ** int(j)
    if j == Q(-1, 2):
        # largest r = m/10 with r^2 <= t0 gives t0^(-1/2) <= 1/r
        m = math.isqrt(100 * t0)
        return Q(10, m)
    raise VerificationError(f'unsupported exponent {j}')


def term_upper(coefficient: Q, j: Q, d: Q, t0: int = T0) -> Q:
    require(coefficient >= 0 and d >= 0, 'invalid term')
    if d > 0:
        require(d * t0 >= j, 'term is not nonincreasing on [T0, oo)')
    else:
        require(j <= 0, 'pure power must have nonpositive degree')
    return coefficient * _t0_power_upper(Q(j), t0) * _exp_neg_upper(d * t0)


def certify(name: str, terms: list[tuple[Any, Any, Any]], target: Q,
            t0: int = T0) -> dict[str, Any]:
    total = sum((term_upper(Q(a), Q(j), Q(d), t0) for a, j, d in terms), Q(0))
    require(total <= target, f'{name}: sum {float(total)} exceeds target {float(target)}')
    return {'name': name, 'terms': len(terms), 'upper_sum_at_T0': f'{float(total):.6g}',
            'target': f'{float(target):.6g}'}


# --------------------------------------------------------------------------
# The certificates. Notation: k = e^t, s = e^{t/2}, u = s/(AD t^3),
# rho = 1/u = AD t^3 e^{-t/2}, D = ceil(u) <= u(1+rho) <= 2u. Every
# coefficient below is computed from the constants in P, so a mutated
# constant is tested by the same certificate (see negative_controls).

def params() -> dict[str, Any]:
    return {'T0': T0, 'AD': Q(AD), 'BH': Q(BH), 'BS': Q(BS), 'AP': Q(AP), 'C': Q(C),
            'G': Q(G), 'EREG': Q(EREG), 'DS': Q(DS)}


def h0_scale(P: dict[str, Any]) -> Q:
    """h0 <= BH u(1+rho) t^3 + 1 <= c_h0 * s, with c_h0 = 2 BH/AD + 1/2."""
    return 2 * P['BH'] / P['AD'] + Q(1, 2)


def first_family(P: dict[str, Any]) -> dict[str, Any]:
    AD, BH, t0 = P['AD'], P['BH'], P['T0']
    L4, L441 = log_hi(4), log_hi(441)
    main = 4 * BH * L4 / AD ** 2                 # 4 log4 * BH D^2 t^6 / k
    terms = [
        (main, 0, 0),
        (3 * main * AD, 3, Q(1, 2)),             # main * 3 rho
        (4 * SQRT2_HI * L4 / AD, Q(-1, 2), 0),   # sqrt(2M) term
        (4 * SQRT2_HI * L4, 3, Q(1, 2)),         # its rho part, t^(5/2) <= t^3
        (8 * L4 / AD, 0, Q(1, 2)),               # the +1 in h0
        (16 * CBRT2_HI * L4 / AD, 1, Q(1, 6)),   # (2M)^(1/3) log_2(2M) term
        (64 / AD, 1, Q(1, 2)),                   # 32 D t
        (4 * L441 / AD, 0, Q(1, 2)),             # 2 D log 441
        (1, 4, 1), (5, 3, 1),                    # (log 96 + 1/8 + t) t^3/k
        (2, 1, 1),                               # 2M t/k >= 2 - 2t/k
    ]
    return certify('first_family', terms, Q(2), t0)


def second_family(P: dict[str, Any]) -> list[dict[str, Any]]:
    AD, BH, EREG_, t0 = P['AD'], P['BH'], P['EREG'], P['T0']
    K2 = 128 * BH / (EREG_ * AD ** 2)            # B0 D h0 ~ K2 k / t^2
    out = [certify('second_family_log_ratio', [
        (5 * EREG_ / 128, -1, 0),                # B0 <= (128/EREG) t + 5
        (6 * AD, 3, Q(1, 2)),                    # (1+a)(1+rho)^2 - 1 - a <= 6 rho
        ((128 / EREG_ + 1) * 2 / (AD * K2), 0, Q(1, 2)),
        (1 / K2, 2, 1)], Q(1, 100), t0)]
    c_phi = log_hi(h0_scale(P)) + 2 * log_hi(9) + 4 * log_hi(K2) + Q(4, 100)
    lead = BH - Q(9, 2)                          # phi(h0) <= -D(lead t - c_phi) + ...
    require(lead > 0, 'second family: BH must exceed 9/2')
    margin = lead * t0 - c_phi
    budget = log_hi(h0_scale(P)) + log_hi(96) + Q(1, 8)
    require(budget <= 6, 'second family constant budget fails')
    out.append(certify('second_family_margin',
                       [(Q(5, 2) * AD, 4, Q(1, 2)), (6 * AD, 3, Q(1, 2))], margin, t0))
    return out


def third_family(P: dict[str, Any]) -> dict[str, Any]:
    exponent = P['DS'] * P['BS'] / 8             # weight exponent >= exponent * D t
    c_s = log_hi(h0_scale(P)) + 2 * log_hi(9) + 2 * log_hi(3)
    lhs = (exponent - Q(37, 2)) * P['T0'] - c_s - (Q(5, 2) * P['T0'] + 6)
    require(exponent > 21, 'third family exponent too small for monotonicity')
    require(lhs >= 0, 'third family margin fails')
    return {'name': 'third_family', 'exponent_per_Dt': str(exponent),
            'margin_at_T0': f'{float(lhs):.6g}'}


def rich_constant(P: dict[str, Any] | None = None) -> dict[str, Any]:
    """kappa = C - (1/4) log AP - G/4 - (1/2) log 370 must be positive."""
    P = P or params()
    kappa_lo = P['C'] - log_hi(P['AP']) / 4 - P['G'] / 4 - Q(1, 2) * log_hi(370)
    require(kappa_lo > 0, 'rich constant is not positive')
    return {'kappa_lower': kappa_lo, 'kappa_lower_float': f'{float(kappa_lo):.6f}'}


def rich_side(P: dict[str, Any]) -> dict[str, Any]:
    AD, t0 = P['AD'], P['T0']
    kappa = rich_constant(P)['kappa_lower']
    cD = (log_hi(441 * 3 * 114) + log_hi(3969)) / 2 + log_hi(2)
    c0 = (log_hi(16) + 3 * log_hi(3) + 4 * log_hi(5) + 3 * log_hi(114) + log_hi(100)) / 2 \
        + log_hi(64)
    terms = [
        (5 * AD / 8, 4, Q(1, 2)), (10, 1, 1), (5, 0, 1),       # 5Q/k
        ((2 / AD) * (Q(93, 4) + cD), 0, Q(1, 2)),              # D(23.25 t + cD)/k
        (Q(33, 2), 1, 1), (c0, 0, 1),                          # (16.5 t + c0)/k
    ]
    return certify('rich_side', terms, kappa, t0)


def rich_cut(P: dict[str, Any]) -> dict[str, Any]:
    """Lemma C needs Gamma > |E_c - E_p|/2, so that 0 < T_R < gamma k."""
    AD, t0 = P['AD'], P['T0']
    kappa_cut = P['C'] - log_hi(P['AP']) / 4 - P['G'] / 4 - Q(1, 2) * log_hi(74)
    require(kappa_cut > 0, 'rich cut constant is not positive')
    terms = [(AD / 8, 4, Q(1, 2)), (2, 1, 1), (1, 0, 1),        # log q / k
             ((2 / AD) * Q(37, 4), 0, Q(1, 2)),                 # D(6.25 t + 3)/k
             (14, 1, 1), (15, 0, 1)]                            # (14 t + 15)/k
    return certify('rich_cut', terms, kappa_cut, t0)


def without_lemma_D() -> dict[str, Any]:
    """PR #12's own Appendix A arithmetic (4^k, 256^k, 2^k), exact coefficients, C = 6."""
    P = params()
    P['C'] = Q(6)
    kappa = P['C'] - log_hi(P['AP']) / 4 - P['G'] / 4 - Q(13, 2) * log_hi(2)
    require(kappa > 0, 'C = 6 without Lemma D fails')
    kappa_cut = P['C'] - log_hi(P['AP']) / 4 - P['G'] / 4 - Q(9, 2) * log_hi(2)
    AD, t0 = P['AD'], P['T0']
    cD = (log_hi(441 * 3 * 114) + log_hi(3969)) / 2 + log_hi(2)
    c0 = (log_hi(16) + 3 * log_hi(3) + 4 * log_hi(5) + 3 * log_hi(114) + log_hi(100)) / 2 \
        + log_hi(64)
    certify('rich_side_without_lemma_D', [
        (5 * AD / 8, 4, Q(1, 2)), (10, 1, 1), (5, 0, 1),
        ((2 / AD) * (Q(93, 4) + cD), 0, Q(1, 2)), (Q(33, 2), 1, 1), (c0, 0, 1)], kappa, t0)
    certify('rich_cut_without_lemma_D', [
        (AD / 8, 4, Q(1, 2)), (2, 1, 1), (1, 0, 1), ((2 / AD) * Q(37, 4), 0, Q(1, 2)),
        (14, 1, 1), (15, 0, 1)], kappa_cut, t0)
    return {'C': '6', 'kappa_lower': f'{float(kappa):.6f}',
            'k_coefficient_of_Ebar': '13/2 log 2', 'other_certificates': 'unchanged'}


def case_i(P: dict[str, Any]) -> dict[str, Any]:
    AD, DS_, t0 = P['AD'], P['DS'], P['T0']
    require(Q(t0, 8) >= log_hi(P['AP']), 'L >= t/4 fails')
    target = DS_ * t0 / 32 - log_hi(2)           # exponent (DS/8) k L >= DS k t/32
    require(target > 0, 'case (i): distinct flips do not pay for subsets')
    terms = [(6 * AD / 8, 4, Q(1, 2)), (12, 1, 1), (6, 0, 1),
             ((2 / AD) * 21, 0, Q(1, 2)), (5, 1, 1), (8, 0, 1)]
    return certify('case_i', terms, target, t0)


def case_ii(P: dict[str, Any]) -> dict[str, Any]:
    AD, AP_, DS_, BS_, t0 = P['AD'], P['AP'], P['DS'], P['BS'], P['T0']
    target = (1 - DS_) * AP_ / 2 - 6 * AD / 8    # (15/32) p k against 6 log q
    require(target > 0, 'case (ii): flips do not pay for the band words')
    terms = [(8 * BS_ / AD, -5, 0), ((2 / AD) * 17, -6, 0), (31, 1, Q(1, 2)), (40, 0, Q(1, 2))]
    return certify('case_ii', terms, target, t0)


def dichotomy(P: dict[str, Any]) -> dict[str, Any]:
    """gap(x) = (1/2 - x)(1 - EREG x)(1 - 2x) - x - (1/2 - G x) >= 0 on (0, 1/T0]."""
    def gap(x: Q) -> Q:
        return (Q(1, 2) - x) * (1 - P['EREG'] * x) * (1 - 2 * x) - x - (Q(1, 2) - P['G'] * x)
    # gap is a cubic with gap(0) = 0: recover a1 x + a2 x^2 + a3 x^3 exactly.
    xs = [Q(1), Q(2), Q(3)]
    ys = [gap(x) for x in xs]
    # Solve the 3x3 Vandermonde-like system for a1, a2, a3.
    a3 = (ys[2] - 3 * ys[1] + 3 * ys[0]) / 6
    a2 = (ys[1] - 2 * ys[0]) / 2 - 3 * a3
    a1 = ys[0] - a2 - a3
    for x in (Q(1, 5), Q(1, 7), Q(2, 9)):
        require(gap(x) == a1 * x + a2 * x * x + a3 * x ** 3, 'dichotomy cubic recovery fails')
    xmax = Q(1, P['T0'])
    require(a1 >= 0 and a2 + min(a3, 0) * xmax >= 0, 'dichotomy fails: gamma too large')
    return {'name': 'dichotomy', 'a1': str(a1), 'a2': str(a2), 'a3': str(a3)}


def analytic_certificates(P: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    P = P or params()
    AD, t0 = P['AD'], P['T0']
    out = []
    out.append(certify('u_at_least_one', [(AD, 3, Q(1, 2))], Q(1), t0))
    out.append(certify('flip_probability', [(P['AP'], 4, Q(1, 2))], Q(1, 2), t0))
    out.append(certify('h0_below_2M', [(P['BH'] / AD, 1, Q(1, 2)), (P['BH'], 4, 1), (3, 1, 1)],
                       Q(1), t0))
    out.append(certify('dimension_below_k_over_64', [(32, 0, Q(1, 2))], Q(1), t0))
    out.append(certify('Ms_below_k', [(2 * P['BS'] / AD + 1, 0, Q(1, 2)), (1, 0, 1)], Q(1), t0))
    out.append(certify('rotating_drift', [(128, 0, Q(3, 2))], Q(1), t0))
    out.append(certify('mesh_D_log_q', [(1, 0, Q(1, 2))], Q(1, 2), t0))
    out.append(certify('mesh_count', [(2, 1, 3), (2, 0, 6)], Q(1), t0))
    out.append(first_family(P))
    out.extend(second_family(P))
    out.append(third_family(P))
    out.append(rich_side(P))
    out.append(rich_cut(P))
    out.append(case_i(P))
    out.append(case_ii(P))
    out.append(dichotomy(P))
    return out


# --------------------------------------------------------------------------
# Exact constant and identity checks.

def exact_checks() -> dict[str, Any]:
    root_checks()
    out: dict[str, Any] = {}
    require(1024 * log_lo(2) >= T0, 'T0 does not cover k >= 2^1024')
    require(9 * log_hi(2) <= 16, 'log t <= t/32 base fails')
    require(Q(1, 8) + Q(1, 5 * T0 * T0) <= EREG, 'regularity budget fails')
    require(Q(2, T0) <= Q(1, 16), 'small block ratio fails')
    require((T0 + log_hi(2)) <= 2 * T0 * log_lo(2), 'log_2(2M) bound fails')
    require(Q(4, T0) + Q(1, 10 ** 6) <= 1, 'k(4M+4)+1 <= k^2 fails')
    require(G == 1 + 1 + EREG / 2 + 1, 'G is not e1 + e2/2 + 1 + e3')
    require(DS / 4 / 2 == Q(1, 128), 'case (i) accounting differs')
    require((1 - DS) / 2 == Q(15, 32), 'case (ii) accounting differs')
    # Arithmetic on PR #9's displayed products (Lemma D).
    for K in range(0, 4000):
        require((1 + K * K) ** 2 <= 5 ** K, 'pair product (1+K^2) <= 5^(K/2) fails')
    for K in range(2, 4000):
        P_K = 4 * K * K + 10 * K + 1
        require(P_K ** 2 <= 37 ** K, 'class factor P(K)^(2/K) <= 37 fails')
    require(4 * 4 + 10 * 2 + 1 == 37, 'class factor at K = 2 differs')
    require((log_hi(16) + 3 * log_hi(3) + 4 * log_hi(5) + 3 * log_hi(114) - log_lo(100)) / 2
            + log_hi(2) <= 15, 'rich cut constant budget fails')
    require(log_hi(Q(150822, 3969)) / 2 + log_hi(2) <= 3, 'rich cut D budget fails')
    out['kappa_lower'] = rich_constant()['kappa_lower_float']
    out['rich_k_coefficient_upper'] = f'{float(Q(1, 2) * log_hi(370)):.6f}'
    out['pr12_rich_k_coefficient'] = '10 (E <= 11k against Gamma >= 14k)'
    return out


def threshold(c: Q) -> tuple[int, int]:
    if not Q(0) < c < Q(1, 8):
        raise ValueError('The coefficient must satisfy 0 < c < 1/8.')
    gap = Q(1, 8) - c
    j = 0
    while Q(2) ** j < 2 / gap:
        j += 1
    n = -(-(4 * (j + C)).numerator * gap.denominator // ((4 * (j + C)).denominator * gap.numerator))
    return j, max(1024, n)


def threshold_checks() -> dict[str, Any]:
    out: dict[str, Any] = {}
    # (2): c = 1/9 for k >= 2^1163: t >= 1163 log 2 >= 806; f(t) = t/72 - log t - C
    # is increasing for t >= 72 and f(806) > 0. (At 1162 log 2 < 805.5, f < 0, so
    # 1163 is the least exponent this argument reaches.)
    require(1163 * log_lo(2) >= 806, '2^1163 does not give t >= 806')
    require(Q(806, 72) - log_hi(806) - C > 0, 'c = 1/9 threshold fails at t = 806')
    require(Q(8055, 10) / 72 - log_lo(Q(8055, 10)) - C < 0 and 1162 * log_hi(2) < Q(8055, 10),
            'the argument would reach 2^1162')
    out['one_ninth_minimum_k'] = '2^1163'
    out['one_ninth_margin_at_t_806'] = f'{float(Q(806, 72) - log_hi(806) - C):.6f}'
    # (3): for all k >= 2^1024, c(t) = 1/8 - (log t + C)/t is increasing, and at
    # t >= 709.78 (a lower bound for 1024 log 2) it is at least 1093/10000.
    t_low = Q(70978, 100)
    require(1024 * log_lo(2) >= t_low, '1024 log 2 lower bound fails')
    require((log_hi(t_low) + C) / t_low <= Q(1, 8) - Q(1093, 10000),
            'coefficient 1093/10000 at 2^1024 fails')
    out['coefficient_for_all_k_at_least_2^1024'] = '1093/10000'
    # Generic thresholds.
    coefficients = [Q(i, 8 * 513) for i in range(1, 513)]
    coefficients += [Q(1, 8) - Q(1, 2 ** m) for m in range(4, 257)]
    coefficients += [Q(1, 9), Q(1, 16), Q(31, 250)]
    for c in coefficients:
        j, n = threshold(c)
        gap = Q(1, 8) - c
        require(Q(2) ** j >= 2 / gap and Q(2) ** (j - 1) < 2 / gap, 'ceil log2 fails')
        require(n * gap >= 4 * (j + C) and n >= 1024, 'generic threshold fails')
    out['generic_coefficients_checked'] = len(coefficients)
    out['generic_log2_K_at_1_9'] = threshold(Q(1, 9))[1]
    return out


def theta_checks() -> dict[str, int]:
    """theta(x) < x log 4 (Erdos) on [2, 20000], and the dilation identity."""
    limit = 20000
    sieve = bytearray(b'\x01') * (limit + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(sieve[p * p::p]))
    theta = 0.0
    log4 = math.log(4)
    for n in range(2, limit + 1):
        if sieve[n]:
            theta += math.log(n)
        require(theta < n * log4 * (1 - 1e-9), 'theta(n) < n log 4 fails')
    # log lambda = sum_j theta(min(h0, (2M)^(1/j))), exactly, on small cases.
    cases = 0
    for h0 in (2, 3, 5, 8, 13, 30, 64):
        for two_m in (16, 50, 100, 1000, 4096):
            if h0 > two_m:
                continue
            primes = [p for p in range(2, h0 + 1) if sieve[p]]
            lam_log = sum(p_exp * math.log(p) for p in primes
                          for p_exp in [int(math.log(two_m) / math.log(p) + 1e-12)])
            ident = 0.0
            j = 1
            while 2 ** j <= two_m:
                bound = min(h0, int(round(two_m ** (1.0 / j) + 1e-9)))
                while bound ** j > two_m:
                    bound -= 1
                while (bound + 1) ** j <= two_m and bound + 1 <= h0:
                    bound += 1
                ident += sum(math.log(p) for p in primes if p <= bound)
                j += 1
            require(abs(lam_log - ident) < 1e-9, 'dilation identity fails')
            cases += 1
    return {'theta_checked_up_to': limit, 'dilation_identity_cases': cases}


# --------------------------------------------------------------------------
# Independent replay (decimal, log space) of the main inequalities from the
# definitions, at sample t. This is a cross-check, not a certificate.

def replay(t_int: int) -> dict[str, bool]:
    getcontext().prec = 90
    getcontext().Emax = MAX_EMAX
    getcontext().Emin = MIN_EMIN
    d = Decimal
    t = d(t_int)
    k = t.exp()
    s = (t / 2).exp()
    def ceil(x): return x.to_integral_value(rounding=ROUND_CEILING)
    def floor(x): return x.to_integral_value(rounding=ROUND_FLOOR)
    ln = lambda x: d(x).ln()
    u = s / (AD * t ** 3); D = ceil(u); M = floor(k / t)
    h0 = ceil(BH * D * t ** 3); Ms = ceil(BS * D * t)
    gamma = d(1) / 2 - d(G.numerator) / d(G.denominator) / t
    L = t / 2 - 4 * ln(t) - ln(AP)
    p = (-L).exp()
    Cd = d(C.numerator) / d(C.denominator)
    F = k * (t / 8 - ln(t) - Cd)
    logP = ln(2) + 2 * t
    Qv = F / D + logP
    logJ = ln(2) + 2 * t + ln((D + 1) * Qv)
    two_m = 2 * M
    Lam = ln(4) * (h0 + two_m.sqrt() + (two_m.ln() / ln(2)) * two_m ** (d(1) / 3))
    logTglob = 2 * D * (ln(9) + 2 * (ln(7) + 8 * t + Lam))
    logz = ln(2) + d(1) / 8
    target = -ln(48) - t
    B0 = ceil(128 * t / (d(EREG.numerator) / d(EREG.denominator)) + 4)
    def logAh(h): return (D + 1) * ln(h) + 2 * D * (ln(9) + 2 * ln(B0 * D * h + 1))
    logAs = t + (D + 1) * ln(h0) + D * (ln(9) + 2 * ln(k * (4 * M + 4) + 1)) \
        + D * (ln(9) + 2 * (ln(2) + t + logJ))
    Gamma = gamma * k * L / 2 - (F + D * logP)
    logBdisc = (D + 1) * t + D * (ln(9) + 2 * (ln(6) + 2 * t + logJ)) + k * ln(5) / 2
    Ec = logBdisc + D * ln(3 * D * k) + ln(16) + 3 * (ln(3) + 2 * t + 2 * Qv) \
        + 4 * ln(D + 4) + (D + 3) * (ln(6) + 3 * t) + (D + 3) * (ln(19) + 4 * t) \
        + k * ln(37) + k * ln(2)
    Ep = logBdisc + ln(100) + 2 * ln(D) + D * ln(9) + 4 * Qv
    Ebar = (Ec + Ep) / 2
    logTK = D * (ln(9) + 2 * (ln(3) + 2 * t + logJ)) + ln(16) + 3 * (t + ln(D) + 2 * Qv + d(10) ** -30)
    logBrun = ln(h0) + ln(Ms + 1) + Ms * (ln(2) + 3 * t)
    dsd = d(DS.numerator) / d(DS.denominator)
    return {
        'u>=1': u >= 1, 'h0<2M': h0 < two_m, 'p<=1/2': p <= d(1) / 2,
        'J<=k^6': logJ <= 6 * t,
        'first_family': logTglob + logz - 2 * M / t ** 2 <= target,
        'second_family': logAh(h0 + 1) + logz - (h0 + 1) / t ** 2 + two_m.ln() <= target,
        'third_family': logAs + logz - dsd * Ms / 8 <= target,
        'rich': ln(2) + ln(2 * (D + 1) * (Ebar - Gamma).exp() + (-2 * Gamma).exp()) <= -ln(4),
        'case_i': ln(2) + logTK + k * ln(2) - (dsd * k / 8) * L <= -ln(8),
        'case_ii': ln(2) + logTK + logBrun - p * (1 - dsd) * k / 2 <= -ln(8),
    }


def replay_checks() -> dict[str, Any]:
    grid = [709, 710, 750, 810, 1000, 2000, 5000, 20000]
    for t in grid:
        result = replay(t)
        failed = [name for name, ok in result.items() if not ok]
        require(not failed, f'replay fails at t={t}: {failed}')
    return {'replayed_t': grid, 'inequalities_per_t': len(replay(709))}


# --------------------------------------------------------------------------
# Negative controls: each mutated constant must break its certificate.

def negative_controls() -> list[str]:
    """Each mutated constant must make the corresponding real certificate fail."""
    rejected = []

    def expect_failure(label: str, check, **changes: Any) -> None:
        P = params()
        P.update({key: Q(value) if key != 'T0' else value for key, value in changes.items()})
        try:
            check(P)
        except VerificationError as error:
            rejected.append(f'{label}: {error}')
        else:
            raise VerificationError(f'negative control passed: {label}')

    expect_failure('C_21_5_breaks_rich_side', rich_side, C=Q(21, 5))
    expect_failure('u_scale_3_breaks_first_family', first_family, AD=3)
    expect_failure('flip_scale_6_breaks_case_ii', case_ii, AP=6)
    expect_failure('h0_scale_9_2_breaks_second_family', second_family, BH=Q(9, 2))
    expect_failure('gamma_slack_3_breaks_dichotomy', dichotomy, G=3)
    expect_failure('delta_s_1_64_breaks_case_i', case_i, DS=Q(1, 64))
    expect_failure('Ms_scale_1024_breaks_third_family', third_family, BS=1024)
    expect_failure('T0_300_breaks_case_i', case_i, T0=300)
    # Each control must leave the unmutated certificate passing.
    analytic_certificates(params())
    # PR #12's own class arithmetic (4^k, 256^k, 2^k) cannot carry C = 9/2.
    kappa_old = C - log_hi(AP) / 4 - G / 4 - Q(1, 2) * (13 * log_lo(2))
    require(kappa_old < 0, 'PR #12 arithmetic unexpectedly carries C = 9/2')
    rejected.append('pr12_class_arithmetic_cannot_carry_C_9_2')
    try:
        term_upper(Q(1), Q(800), Q(1, 2))
    except VerificationError:
        rejected.append('nonmonotone_term_refused')
    else:
        raise VerificationError('A nonmonotone term was admitted')
    for bad in (Q(0), Q(1, 8), Q(1, 7)):
        try:
            threshold(bad)
        except ValueError:
            rejected.append(f'invalid_coefficient_{bad}')
        else:
            raise VerificationError('An invalid coefficient was admitted')
    return rejected


def integrity_check() -> int:
    manifest_path = ROOT / 'MANIFEST.json'
    if not manifest_path.exists():
        return 0
    manifest = json.loads(manifest_path.read_text())
    for name, expected in manifest['sha256'].items():
        source = (ROOT / name).resolve()
        require(source.is_relative_to(ROOT.parent), 'Manifest path leaves contribution track')
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        require(actual == expected, f'Hash mismatch: {name}')
    return len(manifest['sha256'])


def run() -> dict[str, Any]:
    return {
        'status': 'PASS',
        'scope': 'Exact finite inequalities and controls; conditional proof is not formally verified',
        'base_commit': '63bef9ca996786a41169de4a0c3d6b3b47b0fe96',
        'builds_on': 'PR #12 head 029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5',
        'endpoint_bound': '(k^(1/8)/(exp(9/2)*log(k)))^(k*floor(log2(r)))',
        'endpoint_minimum_k': '2^1024',
        'coefficient_1_9_minimum_k': '2^1163',
        'constants': {'T0': T0, 'u_scale': AD, 'h0_scale': BH, 'Ms_scale': BS,
                      'flip_scale': AP, 'C': str(C), 'gamma_slack': str(G),
                      'eps_reg_scale': str(EREG), 'delta_s': str(DS)},
        'all_larger_t_certificates': analytic_certificates(),
        'without_lemma_D': without_lemma_D(),
        'exact_checks': exact_checks(),
        'thresholds': threshold_checks(),
        'theta_and_dilation': theta_checks(),
        'replay': replay_checks(),
        'negative_controls_rejected': negative_controls(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Print the complete deterministic report.')
    args = parser.parse_args()
    report = run()
    integrity = integrity_check()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        n = len(report['all_larger_t_certificates'])
        print(f'PASS: {n} exact certificates valid for every real t >= {T0}')
        print('endpoint: ' + report['endpoint_bound'] + ' for k >= 2^1024')
        print('c = 1/9 for k >= 2^1163; c = 1093/10000 for every k >= 2^1024')
        for field in ('exact_checks', 'thresholds', 'theta_and_dilation', 'replay'):
            print(field + ': ' + json.dumps(report[field], sort_keys=True))
        print(f'Negative controls rejected: {len(report["negative_controls_rejected"])}')
        print(f'Integrity files checked: {integrity}')
        print('Scope: conditional proof draft; imported geometric encodings are not formally verified.')


if __name__ == '__main__':
    main()
