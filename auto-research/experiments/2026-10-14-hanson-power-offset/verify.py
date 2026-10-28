#!/usr/bin/env python3
"""Exact supplementary checks; the all-input proof is in README.md.

No floats, third-party dependencies, imports of the base checker, writes,
network requests, or assertion statements are used.
"""
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SEED = 46
GRID = 16


def require(condition, message):
    if not condition:
        raise ValueError(message)


def floor_root(x, n):
    """Return floor(x**(1/n)) for integers x>=0,n>=1 by binary search."""
    require(x >= 0 and n >= 1, 'invalid integer root input')
    lo, hi = 0, 1 << ((x.bit_length() + n - 1) // n)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**n <= x:
            lo = mid
        else:
            hi = mid
    require(lo**n <= x < (lo + 1)**n, 'integer root bracket failed')
    return lo


def F(lam, x):
    return (1 + lam) * x - lam


def power_value(lam, s, a, b):
    """Exact P(a,b)**n where s=m/n is nonnegative rational."""
    u, v = sorted((Q(a), Q(b)))
    require(lam >= 0 and s >= 0 and u >= 1, 'outside stated family')
    return F(lam, u)**s.numerator * (v + lam * (u - 1))**s.denominator


@lru_cache(maxsize=None)
def interval(lam, s, a, b, bits):
    p = power_value(lam, s, a, b)
    n = s.denominator
    scale = 1 << bits
    scaled_num = p.numerator * scale**n
    low = floor_root(scaled_num // p.denominator, n)
    exact = low**n * p.denominator == scaled_num
    lower = Q(low, scale)
    upper = Q(low if exact else low + 1, scale)
    require(lower**n <= p <= upper**n, 'radical enclosure failed')
    return lower, upper


def second_difference(lam, s, a, b):
    """Certify the sign of P(a,b-1)-2P(a,b)+P(a,b+1)."""
    require(b >= 2, 'stencil crosses domain boundary')
    if b - 1 >= a:
        # The same positive radical is multiplied by an affine factor.
        g = lambda x: Q(x) + lam * (a - 1)
        require(g(b - 1) - 2 * g(b) + g(b + 1) == 0,
                'affine equality failed')
        return {'sign': 0, 'method': 'exact_affine_identity'}
    for bits in (64, 128, 256):
        l, c, r = [interval(lam, s, a, x, bits)
                   for x in (b - 1, b, b + 1)]
        lower, upper = l[0] - 2 * c[1] + r[0], l[1] - 2 * c[0] + r[1]
        if lower == upper == 0:
            return {'sign': 0, 'method': 'exact_rational_equality'}
        if upper < 0 or lower > 0:
            return {'sign': -1 if upper < 0 else 1,
                    'method': 'rational_interval', 'bits': bits,
                    'lower': str(lower), 'upper': str(upper)}
    raise ValueError(f'unresolved concavity interval: {lam=}, {s=}, {a=}, {b=}')


def compute_report():
    root_tests = 0
    for n in (1, 2, 3, 7, 63):
        for x in (1, 2, 17, 2**31 + 7):
            for delta in (-1, 0, 1):
                y = x**n + delta
                r = floor_root(y, n)
                require(r**n <= y < (r + 1)**n, 'root control failed')
                root_tests += 1
    for lam, s, a, b in ((Q(0), Q(1), 3, 5),
                         (Q(1, 2), Q(1, 3), 3, 3)):
        low, high = interval(lam, s, a, b, 64)
        require(low**s.denominator <= power_value(lam, s, a, b)
                <= high**s.denominator, 'interval control failed')

    # Four offsets in the 1/46 grid, deterministically selected by seed 46.
    extras = sorted({Q(1 + (SEED + 7 * i) % 22, 46) for i in range(4)})
    lambdas = sorted(set([Q(0), Q(1, 6), Q(1, 4), Q(1, 3), Q(1, 2)] + extras))
    counts = {'normalization': 0, 'symmetry': 0, 'diagonal': 0,
              'monotonicity': 0, 'tripling': 0, 'rank_envelope': 0,
              'concavity': 0, 'concavity_affine': 0,
              'concavity_rational_equalities': 0, 'concavity_intervals': 0}
    parameters = []
    for lam in lambdas:
        s = (1 - lam) / (1 + lam)
        m, n = s.numerator, s.denominator
        parameters.append({'lambda': str(lam), 's': str(s),
                           'diagonal_exponent': str(1 + s)})
        for a in range(1, GRID + 1):
            require(power_value(lam, s, 1, a) == Q(a)**n, 'normalization')
            require(power_value(lam, s, a, a) == F(lam, a)**(m + n), 'diagonal')
            counts['normalization'] += 1
            counts['diagonal'] += 1
            for b in range(1, GRID + 1):
                p = power_value(lam, s, a, b)
                require(p == power_value(lam, s, b, a), 'symmetry')
                require(p <= power_value(lam, s, a, b + 1), 'monotonicity')
                require(power_value(lam, s, a, 3 * b + a - 1) >= 3**n * p,
                        f'tripling: {lam=}, {a=}, {b=}')
                require(p <= Q(a + b - 1)**(m + n), 'rank envelope')
                for key in ('symmetry', 'monotonicity', 'tripling', 'rank_envelope'):
                    counts[key] += 1
                if b >= 2:
                    witness = second_difference(lam, s, a, b)
                    require(witness['sign'] <= 0, f'concavity: {lam=}, {a=}, {b=}')
                    counts['concavity'] += 1
                    category = {'exact_affine_identity': 'concavity_affine',
                                'exact_rational_equality': 'concavity_rational_equalities',
                                'rational_interval': 'concavity_intervals'}[witness['method']]
                    counts[category] += 1

    # Reconstruct the base profile through the general family, not its checker.
    lam, s = Q(1, 2), Q(1, 3)
    for a in range(1, 101):
        for h in range(1, 101):
            p = power_value(lam, s, a, h)
            require(power_value(lam, s, a, 3 * h + a - 1) >= 27 * p,
                    'base tripling replay')
            require(p <= Q(a + h - 1)**4, 'base envelope replay')

    negative = []
    lam, s, a, h = Q(3, 4), Q(1, 7), 2, 2
    lhs = power_value(lam, s, a, 3 * h + a - 1)
    rhs = 3**s.denominator * power_value(lam, s, a, h)
    require(lhs < rhs, 'too-large offset was not rejected')
    negative.append({'name': 'offset_above_half', 'lambda': str(lam),
                     's': str(s), 'a': a, 'h': h, 'inequality': 'tripling',
                     'lhs_to_denominator_power': str(lhs),
                     'rhs_to_denominator_power': str(rhs)})
    for name, s, a, b in (('power_below_curve', Q(1, 4), 2, 2),
                          ('power_above_curve', Q(1, 2), 4, 3),
                          ('zero_power', Q(0), 2, 2)):
        lam = Q(1, 2)
        witness = second_difference(lam, s, a, b)
        require(witness['sign'] > 0, f'negative control not rejected: {name}')
        negative.append({'name': name, 'lambda': str(lam), 's': str(s),
                         'a': a, 'b': b, 'inequality': 'separate_discrete_concavity',
                         'positive_second_difference': witness})
    return {'status': 'passed', 'assignment_seed': SEED,
            'base_commit': '63bef9ca996786a41169de4a0c3d6b3b47b0fe96',
            'result_type': 'analytic family characterization and scoped no-gain result',
            'mathematical_scope': 'lambda,s >= 0; scalar profile constraints only',
            'claim': 'constraints hold iff 0<=lambda<=1/2 and s=(1-lambda)/(1+lambda)',
            'minimum_diagonal_exponent': '4/3',
            'finite_domain': {'grid': '1<=a,b,h<=16; concavity centers b>=2',
                              'stencil_and_tripling_evaluations': 'include b+1 and 3h+a-1 outside the center grid',
                              'parameters': parameters, 'seed_offsets': [str(x) for x in extras],
                              'stopping_rule': 'complete every listed case; fail on any unresolved sign'},
            'counts': counts, 'integer_root_controls': root_tests,
            'base_profile_replay': {'tripling_pairs': 10000, 'envelope_pairs': 10000,
                                    'domain': '1<=a,h<=100'},
            'negative_controls': negative,
            'limitations': ['Finite checks supplement the written all-input proof.',
                            'No human review or formal proof certificate.',
                            'No tensor realizability, new matrix algorithm, or vdW coefficient.']}


def check_files():
    manifest = json.loads((HERE / 'MANIFEST.json').read_text())
    actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob('*')
              if p.is_file() and p != HERE / 'MANIFEST.json'}
    listed = set(manifest['files'])
    require(actual == listed, 'manifest file set differs from contribution files')
    for relative, expected in manifest['files'].items():
        p = (HERE / relative).resolve()
        require(p.is_relative_to(HERE), 'manifest path escapes contribution')
        require(sha256(p.read_bytes()).hexdigest() == expected,
                f'package hash mismatch: {relative}')
    pins = json.loads((HERE / 'SOURCES.json').read_text())
    for relative, expected in pins['base_files'].items():
        p = (ROOT / relative).resolve()
        require(p.is_relative_to(ROOT), 'source path escapes repository')
        require(sha256(p.read_bytes()).hexdigest() == expected,
                f'base source hash mismatch: {relative}')


def main():
    check_files()
    report = compute_report()
    require(report == json.loads((HERE / 'RESULT.json').read_text()),
            'computed result differs from saved RESULT.json')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
