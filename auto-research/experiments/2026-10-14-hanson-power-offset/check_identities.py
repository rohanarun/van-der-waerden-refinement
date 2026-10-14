#!/usr/bin/env python3
"""Optional symbolic cross-check, tested with SymPy 1.14.0; no file writes."""
import json
import sympy as S


def equal(actual, expected, label):
    if S.simplify(actual - expected) != 0:
        raise ValueError(label)


def main():
    lam, s, a, b, x = S.symbols('lambda s a b x', positive=True)
    d = 1 + lam
    F = d * b - lam
    G = a + lam * (b - 1)
    f = F**s * G
    raw = s * d * F**(s - 2) * ((s - 1) * d * G + 2 * lam * F)
    equal(S.diff(f, b, 2), raw, 'raw second derivative')
    curve = (1 - lam) / d
    equal(raw.subs(s, curve),
          2 * curve * d * lam * F**(curve - 2) * (b - a),
          'second derivative on parameter curve')
    seam = (1 - d * x)**s * (1 / x - lam) - 1 / x + 1
    seam_limit = S.expand(S.series(seam, x, 0, 1).removeO()).coeff(x, 0)
    equal(seam_limit, 1 - lam - s * d, 'seam Taylor coefficient')
    interior = ((1 - d * x)**s * (1 / x + 1 - lam)
                - 2 * (1 / x + 1)
                + (1 + d * x)**s * (1 / x + 1 + lam)) / x
    interior_limit = S.expand(S.series(interior, x, 0, 1).removeO()).coeff(x, 0)
    equal(interior_limit, s * d * (s * d + lam - 1), 'interior Taylor coefficient')
    z = S.symbols('z', positive=True)
    lower_bound = d * z**s * (z + 2) - 3 * (z + lam)
    equal(S.diff(lower_bound, z, 2),
          d * s * z**(s - 2) * ((s + 1) * z + 2 * (s - 1)),
          'tripling lower bound second derivative')
    equal(S.diff(lower_bound, z).subs({s: curve, z: 1}),
          1 - 2 * lam, 'tripling lower bound initial slope')
    print(json.dumps({'status': 'passed', 'identities': 6,
                      'sympy': S.__version__,
                      'scope': 'Symbolic identities only; domain signs and Taylor remainders are justified in README.md.'}, indent=2))


if __name__ == '__main__':
    main()
