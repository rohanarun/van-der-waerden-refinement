#!/usr/bin/env python3
"""Literature calibration of the uniform coefficient: checks for README.md.

Base commit: 63bef9ca996786a41169de4a0c3d6b3b47b0fe96. Standard library only.
Run:  python3 -B verify.py          (assertions are load-bearing; never -O)
      python3 -B verify.py --write  (regenerates RESULT.json)

What is checked:
  1. the normalization r^{alpha k ln k} = k^{alpha ln2 k log2 r};
  2. the digit product behind Proposition 1, exhaustively on small cases:
     a cyclic 2-coloring of Z/N without monochromatic k-term progressions
     (nonzero step, degenerate ones included, as in the source's
     Proposition 7.1), and its product on [0, N^m) without monochromatic
     progressions; then the averaging step of Proposition 2 (a class of
     density >= 2^-m), which is plain pigeonhole;
  3. that the bases are the largest within the searched ranges, for k = 3, 4;
  4. negative controls: a base that is a valid *interval* coloring but not a
     valid cyclic one makes the product fail, so the cyclic hypothesis is
     load-bearing; a base with a monochromatic progression is caught;
  5. the crossover exponents 2/(1 - c/ln 2) of Proposition 3.
"""
from fractions import Fraction as Q
from itertools import product
import json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def cyclic_mono(col, k):
    """True if some a, a+d, ..., a+(k-1)d (d != 0 mod N) is monochromatic."""
    N = len(col)
    for d in range(1, N):
        for a in range(N):
            c = col[a]
            if all(col[(a + j * d) % N] == c for j in range(1, k)):
                return True
    return False


def interval_mono(col, k):
    """True if [0, len(col)) holds a monochromatic k-AP with step d >= 1."""
    M = len(col)
    for d in range(1, (M - 1) // (k - 1) + 1):
        for a in range(M - (k - 1) * d):
            c = col[a]
            if all(col[a + j * d] == c for j in range(1, k)):
                return True
    return False


def has_ap(S, k):
    S = sorted(S); T = set(S)
    for i, a in enumerate(S):
        for b in S[i + 1:]:
            d = b - a
            if all(a + j * d in T for j in range(2, k)):
                return True
    return False


def first_cyclic_coloring(N, k):
    """Exhaustive search, color of 0 fixed to 0 (swap symmetry)."""
    for tail in product((0, 1), repeat=N - 1):
        col = (0,) + tail
        if not cyclic_mono(col, k):
            return col
    return None


def digit_product(col, m):
    N = len(col)
    out = []
    for n in range(N ** m):
        digits, x = [], n
        for _ in range(m):
            digits.append(col[x % N]); x //= N
        out.append(tuple(digits))
    return out


def check_product(k, N, m):
    col = first_cyclic_coloring(N, k)
    assert col is not None, (k, N)
    assert not cyclic_mono(col, k)
    big = digit_product(col, m)
    assert not interval_mono(big, k), (k, N, m)
    classes = {}
    for n, c in enumerate(big):
        classes.setdefault(c, []).append(n)
    S = max(classes.values(), key=len)
    assert Q(len(S), N ** m) >= Q(1, 2 ** m)
    assert not has_ap(S, k)
    # negative control: an interval-valid, cyclic-invalid base must fail
    bad = next(c for c in product((0, 1), repeat=N)
               if not interval_mono(c, k) and cyclic_mono(c, k))
    assert interval_mono(digit_product(bad, m), k), (k, N, m)
    return {"k": k, "N": N, "m": m, "base": "".join(map(str, col)),
            "classes": 2 ** m, "largest_class": len(S), "length": N ** m}


def main():
    res = {"_scope": "checks of README.md; no new bound on W_r(k)"}

    # 1. normalization
    for k in (10 ** 3, 10 ** 6, 2 ** 960):
        for r in (2, 3, 256, 10 ** 9):
            for alpha in (Q(1, 9), Q(1, 2), Q(1)):
                lhs = float(alpha) * math.log(k) * math.log(r)
                rhs = float(alpha) * math.log(2) * math.log2(r) * math.log(k)
                assert math.isclose(lhs, rhs, rel_tol=1e-12)
    res["normalization"] = "r^{a k ln k} = k^{a ln2 k log2 r}; FH Thm 2 <-> c = (1-eps) ln 2"

    # 2-4. digit product (Proposition 1) and averaging (Proposition 2)
    # largest N with a cyclic coloring, by exhaustive search over
    # N <= 13 (k = 3), N <= 19 (k = 4), N <= 21 (k = 5): 4, 11, 20;
    # N_cyc is not monotone (k = 4: N = 5, 6, 7, 11). Maximality is
    # re-checked below for k = 3, 4; for k = 5 it is not re-run (minutes).
    for k, Nmax, top in ((3, 13, 4), (4, 19, 11)):
        assert first_cyclic_coloring(top, k) is not None
        assert all(first_cyclic_coloring(N, k) is None
                   for N in range(top + 1, Nmax + 1)), k
    cases = []
    for k, N, m in ((3, 4, 2), (3, 4, 3), (4, 11, 2), (4, 7, 3), (5, 19, 2), (5, 20, 2)):
        cases.append(check_product(k, N, m))
    res["digit_product_cases"] = cases
    # a negative control that must be caught directly
    assert cyclic_mono((0, 0, 0, 1, 1), 3)
    assert interval_mono(digit_product((0, 0, 0, 1, 1), 2), 3)

    # 5. crossover exponents of Proposition 3 (Fox-Hunter Corollary 5.1:
    # r >= (ln k)^{2+alpha} gives exponent 1 - 2/(2+alpha) - eps), and the
    # calibration ratios
    ln2 = math.log(2)
    cross = {}
    for name, c in (("1/9", 1 / 9), ("1/8", 1 / 8), ("1/16", 1 / 16)):
        eps = 1 - c / ln2
        assert 0 < eps < 1
        cross[name] = {"r_exponent": round(2 / eps, 4),
                       "fraction_of_ln2": round(c / ln2, 4)}
    assert 2.38 < cross["1/9"]["r_exponent"] < 2.39
    assert 2.43 < cross["1/8"]["r_exponent"] < 2.45
    assert 2.19 < cross["1/16"]["r_exponent"] < 2.20
    res["crossover"] = cross
    res["ln2"] = round(ln2, 6)

    out = HERE / "RESULT.json"
    text = json.dumps(res, indent=2, sort_keys=True) + "\n"
    if "--write" in sys.argv:
        out.write_text(text)
        print("RESULT.json written")
    else:
        assert out.read_text() == text, "RESULT.json differs; rerun with --write"
        print("OK: all checks pass and match RESULT.json")


if __name__ == "__main__":
    main()
