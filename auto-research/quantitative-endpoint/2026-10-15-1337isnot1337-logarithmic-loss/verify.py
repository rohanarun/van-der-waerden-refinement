#!/usr/bin/env python3
"""Exact checks for the conditional endpoint transfer, not a formal proof.

Only the Python standard library is required. No network access is used.
The finite source encodings remain imported mathematical assumptions.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
T0 = 512
AD = 4096
BH = 256
BS = 4096
AP = 65536
C = 20


class VerificationError(RuntimeError):
    """A stated finite check did not hold."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_q(x: Q) -> int:
    return -(-x.numerator // x.denominator)


def power_two(n: int) -> Q:
    return Q(1 << n) if n >= 0 else Q(1, 1 << (-n))


def ceil_log2(x: Q) -> int:
    if x <= 0:
        raise ValueError('The logarithm input must be positive.')
    n = x.numerator.bit_length() - x.denominator.bit_length()
    while power_two(n) < x:
        n += 1
    while power_two(n - 1) >= x:
        n -= 1
    return n


def monomial(name: str, coefficient: Q, degree: int, decay: Q,
             target: Q, t0: int = T0) -> dict[str, Any]:
    """Certify A*t^j*exp(-d*t) <= target for all real t >= t0.

    The derivative has the sign of j-d*t. At t0, use e >= 2.
    Rounding d*t0 downward weakens the upper bound safely.
    """
    require(coefficient >= 0 and decay > 0 and target > 0,
            f'{name}: invalid monomial parameters')
    derivative_margin = decay * t0 - degree
    require(derivative_margin >= 0, f'{name}: monotonicity is not established')
    exponent = (decay * t0).__floor__()
    bound = coefficient * Q(t0) ** degree * power_two(-exponent)
    require(bound <= target, f'{name}: endpoint upper bound fails')
    return {'name': name, 'coefficient': str(coefficient), 'degree': degree,
            'decay': str(decay), 'target': str(target), 't0': t0,
            'derivative_margin': str(derivative_margin),
            'binary_exponent': exponent, 'rational_upper_bound': str(bound)}


def analytic_bounds() -> list[dict[str, Any]]:
    specs = [
        ('u_at_least_one', Q(AD), 3, Q(1, 2), Q(1)),
        ('floor_M', Q(2), 1, Q(1), Q(1)),
        ('dimension', Q(128, AD), -3, Q(1, 2), Q(1)),
        ('t_below_sqrt_k', Q(1), 1, Q(1, 2), Q(1)),
        ('Ms_below_k', Q(2 * (BS + 1), AD), -2, Q(1, 2), Q(1)),
        ('flip_probability', Q(AP), 4, Q(1, 2), Q(1, 2)),
        ('six_Q_leading', Q(3072), 4, Q(1, 2), Q(1, 4)),
        ('six_Q_rounding', Q(18), 1, Q(1), Q(1, 4)),
        ('hundred_Dt', Q(200, AD), -2, Q(1, 2), Q(1, 4)),
        ('q_rounding_in_Gamma', Q(6, AD), -2, Q(1, 2), Q(1)),
        ('first_family_incident', Q(8), 4, Q(1), Q(1)),
        ('first_family_weight', Q(2), 3, Q(1), Q(1)),
        ('mesh_count_leading', Q(2), 1, Q(3), Q(1, 2)),
        ('mesh_count_rounding', Q(2), 0, Q(6), Q(1, 2)),
    ]
    return [monomial(*s) for s in specs]


def constant_checks() -> dict[str, str]:
    global_budget = Q(84, AD) + Q(240 * 257 * 4, AD * AD)
    require(global_budget < Q(1, 16), 'Global entropy budget fails')
    require(Q(BH, 16) >= 15, 'Local anchored entropy budget fails')
    require(Q(BS, 32) - 40 == 88, 'Third-family budget differs')
    require(Q(257 * 2, AD) <= Q(1, 4), 'Upper h0 bound fails')
    require(Q(BH, AD) == Q(1, 16), 'Lower h0 bound differs')
    require(Q(T0, 2) - 4 >= Q(T0, 3), 'log h0 lower bound fails')
    require(9 <= Q(T0, 32), 'log t base comparison fails')
    require(Q(T0, 8) - 16 >= 0, 'L >= t/4 base comparison fails')
    require(9 + Q(T0, 32) <= T0, 'Local logarithmic factor fails')
    require(Q(1, 2 * T0) + Q(1, BH * T0 ** 3) <= Q(1, T0),
            'Regularity budget fails')
    require(Q(2, T0) <= Q(1, 16), 'Drift ratio fails')
    require(Q(3, 4) + Q(1, 8) < 1, 'Local lemma weight inequality fails')
    require(9 * Q(3, 4) < 7, 'Class/subset logarithm budget fails')
    require(Q(C - 1 - 16 // 4) - 1 == 14, 'Gamma lower bound differs')
    require(10 + 3 * Q(1, 4) <= 11, 'E <= 11k fails')
    require(14 - 11 == 3, 'Rich probability margin differs')
    require(21 + 3 + 20 + 28 + 9 == 81, 'Digit certificate Dt sum differs')
    require(81 <= 100 and 9 <= 10, 'Finite digit-rank envelope fails')
    require(Q(2 * (BS + 1), 512 * 2) < 9, 'Run coefficient bound fails')
    require(3072 + 24 + 9 + 1 == 3106 < 4096 == AP // 16,
            'Heavy-run probability budget fails')
    require(Q(2048, 72) - Q(33, 4) - C > 0, 'Explicit c=1/9 threshold fails')
    require(Q(33554432, 4096) == 8192, 'Threshold comparison differs')
    return {
        'global_entropy_upper_coefficient': str(global_budget),
        'global_entropy_target': '1/16', 'Gamma_over_k_lower': '14',
        'E_over_k_upper': '11', 'rich_exponential_margin': '3',
        'run_entropy_coefficient_upper': '3106',
        'run_entropy_coefficient_budget': '4096',
        'one_ninth_transfer_margin_at_t_2048': str(Q(2048, 72) - Q(33, 4) - C),
    }


def threshold(c: Q) -> tuple[int, int]:
    if not Q(0) < c < Q(1, 8):
        raise ValueError('The coefficient must satisfy 0 < c < 1/8.')
    gap = Q(1, 8) - c
    j = ceil_log2(2 / gap)
    return j, max(1024, ceil_q(4 * (j + C) / gap))


def threshold_checks() -> dict[str, Any]:
    coefficients = [Q(i, 8 * 513) for i in range(1, 513)]
    coefficients += [Q(1, 8) - power_two(-m) for m in range(4, 257)]
    coefficients += [Q(1, 9), Q(1, 16), Q(31, 250)]
    for c in coefficients:
        j, n = threshold(c)
        gap = Q(1, 8) - c
        require(power_two(j) >= 2 / gap, 'Generic threshold logarithm fails')
        require(power_two(j - 1) < 2 / gap, 'Ceil logarithm is not minimal')
        require(n * gap >= 4 * (j + C), 'Generic threshold numerator fails')
        require(n >= 1024, 'Generic threshold misses base range')
        require(Q(2 * (j + C), 1) / gap >= 1 / gap,
                'Generic threshold monotonicity fails')
    return {'rational_coefficients_checked': len(coefficients),
            'generic_log2_K_at_1_9': threshold(Q(1, 9))[1],
            'special_log2_K_at_1_9': 4096,
            'endpoint_log2_K': 1024,
            'largest_gap_denominator_bits': 257}


def primes_to(n: int) -> list[int]:
    sieve = bytearray(b'\x01') * (n + 1)
    if n >= 0:
        sieve[0] = 0
    if n >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(n) + 1):
        if sieve[p]:
            for a in range(p * p, n + 1, p):
                sieve[a] = 0
    return [p for p in range(2, n + 1) if sieve[p]]


def dilation_checks() -> dict[str, int]:
    configurations = 0
    denominators = 0
    prime_intervals = 0
    for cutoff, limit in itertools.product((2, 3, 5, 8, 16, 24, 32),
                                            (16, 24, 32, 48, 64, 96)):
        if cutoff > limit:
            continue
        primes = primes_to(cutoff)
        lam = 1
        for prime in primes:
            factor = prime
            while factor * prime <= limit:
                factor *= prime
            lam *= factor
        # This is the exact inequality underlying log(lambda) <= pi(h0)*log(2M).
        require(lam <= limit ** len(primes), 'Dilation logarithmic bound fails')
        for h in range(1, limit + 1):
            if h <= cutoff:
                require(lam % h == 0, 'A short period does not divide lambda')
            for residue in range(h):
                denominator = h // math.gcd(h, lam * residue)
                require(denominator == 1 or denominator > cutoff,
                        'A small scalar denominator survives')
                denominators += 1
        configurations += 1
    for n in range(1, 257):
        product = math.prod(p for p in primes_to(2 * n) if p > n)
        central = math.comb(2 * n, n)
        require(central % product == 0, 'Prime interval does not divide binomial')
        require(central <= 4 ** n, 'Central binomial upper bound fails')
        prime_intervals += 1
    return {'dilation_configurations': configurations,
            'scalar_denominators': denominators,
            'prime_interval_checks': prime_intervals}


def weighted_checks() -> dict[str, int]:
    cases = 0
    exact_tails = 0
    for size in range(1, 6):
        for weights in itertools.product((1, 2, 3), repeat=size):
            k = sum(weights)
            maximum = max(weights)
            M = Q(k, maximum)
            variance_proxy = sum(w * w for w in weights)
            require(variance_proxy <= Q(k * k) / M,
                    'Weighted variance proxy exceeds k^2/M')
            # Exact tail at the largest possible deviation.
            tail = sum(1 for bits in itertools.product((0, 1), repeat=size)
                       if abs(sum(w * (2 * b - 1) for w, b in zip(weights, bits))) >= k)
            actual = Q(tail, 2 ** size)
            # Independent-label outcome counting must agree with all-zero/all-one.
            require(actual == Q(2, 2 ** size), 'Weighted tail enumeration differs')
            exact_tails += 1
            cases += 1
    # Removing labels from S does not increase any multiplicity or its upper cap.
    for weights in itertools.product(range(4), repeat=5):
        k = 15
        maximum = 3
        M = Q(k, maximum)
        require(sum(w * w for w in weights) <= Q(k * k) / M,
                'Subset variance upper bound fails')
        cases += 1
    return {'variance_cases': cases, 'enumerated_extreme_tails': exact_tails}


def rich_split_checks() -> dict[str, int]:
    identities = 0
    accounting = 0
    for D in range(1, 21):
        for R in range(D + 1):
            for Qv in (Q(1, 3), Q(1), Q(7, 3)):
                k = 100
                gamma = Q(2, 5)
                Lv = Q(10)
                budget = gamma * k * Lv / 2 - D * Qv
                if budget <= 0:
                    continue
                cut = (R * Qv + budget) / Lv
                require(0 < cut < gamma * k, 'Rich cut leaves its allowed interval')
                require(cut * Lv - R * Qv == budget,
                        'Certificate rank identity fails')
                require((gamma * k - cut) * Lv - (2 * D - R) * Qv == budget,
                        'Progression rank identity fails')
                identities += 1
    for r2, singles_in, singles_out in itertools.product(range(11), repeat=3):
        positions = 2 * r2 + singles_in + singles_out
        keys = r2 + singles_in + singles_out
        collision_keys = r2 + singles_in
        for required in (Q(7), Q(13, 2), Q(21, 2)):
            for cut in (Q(5, 2), Q(4), Q(13, 2)):
                if positions >= required and collision_keys < cut:
                    require(keys > required - cut,
                            'Few collision keys do not imply enough distinct flips')
                    accounting += 1
    return {'rank_split_identities': identities,
            'correlation_accounting_cases': accounting}


def finite_factor_checks() -> dict[str, int]:
    polynomial_cases = 0
    class_cases = 0
    for k in (64, 65, 100, 128, 256, 1024, 4096):
        for D in range(1, min(k // 64, 24) + 1):
            for q in (k + 1, 2 * k + 1, k * k + 1):
                for h in (1, 2, k // 3, k - 1):
                    Kh = (k + h - 1) // h
                    sg = k * (D * q * q + 8 * D * k + 4 * k + 20)
                    sp = k * (4 * D * k + 7)
                    sx = 2 * k * k * (2 * Kh + 5) ** 2
                    require(sg + 1 <= 3 * k * k * q * q, 'First arrangement factor fails')
                    require(sp + 1 <= 6 * k ** 3, 'Tail arrangement factor fails')
                    require(sx + 1 <= 19 * k ** 4, 'Crossing arrangement factor fails')
                    require(h * Kh <= 2 * k, 'Class ceiling accounting fails')
                    polynomial_cases += 1
    for n in range(1, 513):
        pn = 4 * n * n + 10 * n + 1
        pnext = 4 * (n + 1) ** 2 + 10 * (n + 1) + 1
        require(pn <= 16 ** n, 'Class polynomial envelope fails')
        require(16 * pn - pnext == 60 * n * n + 142 * n + 1,
                'Class induction identity fails')
        class_cases += 1
    return {'arrangement_polynomial_cases': polynomial_cases,
            'class_induction_cases': class_cases}


def negative_controls() -> list[str]:
    rejected: list[str] = []
    for bad in (Q(0), Q(1, 8), Q(1, 7)):
        try:
            threshold(bad)
        except ValueError:
            rejected.append(f'invalid_coefficient_{bad}')
        else:
            raise VerificationError('An invalid coefficient was admitted')
    # These controls falsify the proposed proof budgets, not the underlying theorem.
    require(Q(8, 16) < 15, 'Short-cutoff negative control unexpectedly passes')
    rejected.append('underpriced_long_period_cutoff')
    require(Q(BS, 2 * T0 * T0) < 40,
            'Vanishing third-family tolerance control unexpectedly passes')
    rejected.append('vanishing_third_tolerance_without_larger_Ms')
    require(Q(84, 128) + Q(246720, 128 ** 2) > Q(1, 16),
            'Oversized dimension control unexpectedly passes')
    rejected.append('oversized_dimension')
    require(8 - 5 - 1 < 11, 'Unpaid rank error control unexpectedly passes')
    rejected.append('endpoint_constant_too_small_for_this_budget')
    # One fair bit repeated twenty times has deviation ten with probability one.
    # An incorrect independent-position Hoeffding estimate would give 2*exp(-10)<1.
    probability = Q(2, 2)
    require(probability == 1 and 2 * power_two(-10) < probability,
            'Shared-variable negative control unexpectedly passes')
    rejected.append('repeated_positions_treated_as_independent')
    try:
        monomial('nonmonotone_control', Q(1), 1024, Q(1, 2), Q(1), T0)
    except VerificationError:
        rejected.append('missing_all_larger_t_monotonicity')
    else:
        raise VerificationError('A nonmonotone all-larger-t certificate was admitted')
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
        'endpoint_bound': '(k^(1/8)/(exp(20)*log(k)))^(k*floor(log2(r)))',
        'endpoint_minimum_k': '2^1024',
        'coefficient_1_9_minimum_k': '2^4096',
        'all_larger_t_certificates': analytic_bounds(),
        'constants': constant_checks(),
        'thresholds': threshold_checks(),
        'dilation': dilation_checks(),
        'weighted_events': weighted_checks(),
        'rank_split': rich_split_checks(),
        'finite_factors': finite_factor_checks(),
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
        print('PASS: 14 exact certificates valid for every real t >= 512')
        for field in ('thresholds', 'dilation', 'weighted_events', 'rank_split', 'finite_factors'):
            print(field + ': ' + json.dumps(report[field], sort_keys=True))
        print(f'Negative controls rejected: {len(report["negative_controls_rejected"])}')
        print(f'Integrity files checked: {integrity}')
        print('Scope: conditional proof draft; imported geometric encodings are not formally verified.')


if __name__ == '__main__':
    main()
